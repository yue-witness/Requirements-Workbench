#!/usr/bin/env python3
"""Dependency-free MCP server for the Requirements Analysis Workbench UI.

The server exposes a visual configuration resource and a matching structured
tool. The tools remain useful when a client cannot render MCP Apps UI.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


SERVER_NAME = "requirements-analysis-workbench"
SERVER_VERSION = "0.3.2"
RESOURCE_URI = "ui://requirements-analysis-workbench/workbench.html"
PLUGIN_ROOT = Path(__file__).resolve().parents[1]
UI_PATH = PLUGIN_ROOT / "ui" / "workbench.html"
MODULES = [
    "requirements",
    "fishbone",
    "context",
    "use-cases",
    "activity",
    "wireframe",
]


def _result(request_id: Any, value: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": value}


def _error(request_id: Any, code: int, message: str) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": code, "message": message},
    }


def _serialize(response: dict[str, Any]) -> str:
    """Serialize one MCP message without depending on the Windows code page."""

    return json.dumps(
        response,
        ensure_ascii=True,
        separators=(",", ":"),
    ) + "\n"


def _tool_definitions() -> list[dict[str, Any]]:
    ui_meta = {
        "ui": {"resourceUri": RESOURCE_URI},
        "openai/outputTemplate": RESOURCE_URI,
    }
    return [
        {
            "name": "open_workbench",
            "title": "Open Requirements Analysis Workbench",
            "description": (
                "Open the visual mode and module selector before a requirements-analysis run. "
                "This tool never confirms defaults. After calling it, stop the current turn and "
                "wait for an explicit save_workbench_selection result in a later user turn. "
                "Do not analyse requirements or create files while the state is awaiting_user_selection."
            ),
            "inputSchema": {"type": "object", "properties": {}},
            "annotations": {
                "readOnlyHint": True,
                "destructiveHint": False,
                "openWorldHint": False,
            },
            "_meta": ui_meta,
        },
        {
            "name": "save_workbench_selection",
            "title": "Save workbench selection",
            "description": (
                "Validate and explicitly confirm a Guided, Standard, or Professional mode and "
                "the enabled output modules. Analysis may start only after this tool returns "
                "confirmed=true."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "mode": {
                        "type": "string",
                        "enum": ["guided", "standard", "professional"],
                    },
                    "modules": {
                        "type": "array",
                        "items": {"type": "string", "enum": MODULES},
                        "minItems": 1,
                        "uniqueItems": True,
                    },
                    "traceguard": {"type": "boolean", "default": True},
                },
                "required": ["mode", "modules"],
                "additionalProperties": False,
            },
            "annotations": {
                "readOnlyHint": True,
                "destructiveHint": False,
                "openWorldHint": False,
            },
        },
    ]


def _selection_result(arguments: dict[str, Any]) -> dict[str, Any]:
    mode = str(arguments.get("mode", "")).lower()
    modules = arguments.get("modules", [])
    traceguard = bool(arguments.get("traceguard", True))

    if mode not in {"guided", "standard", "professional"}:
        raise ValueError("mode must be guided, standard, or professional")
    if not isinstance(modules, list) or not modules:
        raise ValueError("select at least one module")
    if len(modules) != len(set(modules)):
        raise ValueError("module selections must be unique")
    unknown = sorted(set(modules) - set(MODULES))
    if unknown:
        raise ValueError("unknown modules: " + ", ".join(unknown))

    selection = {
        "mode": mode,
        "modules": modules,
        "traceguard": traceguard,
    }
    return {
        "structuredContent": {
            "state": "selection_confirmed",
            "confirmed": True,
            "selection": selection,
        },
        "content": [
            {
                "type": "text",
                "text": (
                    f"Use {mode} mode with {len(modules)} enabled module(s): "
                    + ", ".join(modules)
                    + f". TraceGuard is {'enabled' if traceguard else 'disabled'}."
                ),
            }
        ],
    }


def _awaiting_selection_result() -> dict[str, Any]:
    """Return a non-selection result that keeps the analysis workflow blocked."""

    return {
        "structuredContent": {
            "state": "awaiting_user_selection",
            "confirmed": False,
            "selection": None,
            "modes": ["guided", "standard", "professional"],
            "modules": MODULES,
        },
        "content": [
            {
                "type": "text",
                "text": (
                    "WORKFLOW_BLOCKED: waiting for the user to apply a mode and at least "
                    "one module in the workbench. Do not analyse requirements, read analysis "
                    "references, create output files, or infer a default selection. End this "
                    "turn now. Continue only after save_workbench_selection returns confirmed=true."
                ),
            }
        ],
        "_meta": {
            "ui": {"resourceUri": RESOURCE_URI},
            "openai/outputTemplate": RESOURCE_URI,
        },
    }


def handle(message: dict[str, Any]) -> dict[str, Any] | None:
    method = message.get("method")
    request_id = message.get("id")

    if method == "initialize":
        requested_version = message.get("params", {}).get(
            "protocolVersion", "2025-06-18"
        )
        return _result(
            request_id,
            {
                "protocolVersion": requested_version,
                "capabilities": {"tools": {}, "resources": {}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
                "instructions": (
                    "When the user @mentions Requirements Analysis Workbench and supplies a "
                    "matching software idea, scenario, user-story collection, meeting note, or "
                    "requirements draft, open the workbench before analysis by default unless "
                    "the user explicitly declines the GUI. Opening the workbench sets state to "
                    "awaiting_user_selection and is a hard stop: end that turn without analysing "
                    "or creating files. Resume only after save_workbench_selection returns "
                    "confirmed=true from the user's explicit submission. Also open it whenever "
                    "the user asks for visual mode or module selection. "
                    "Keep TraceGuard results visible and require named approval for abstained high-impact items."
                ),
            },
        )

    if method in {"notifications/initialized", "notifications/cancelled"}:
        return None
    if method == "tools/list":
        return _result(request_id, {"tools": _tool_definitions()})
    if method == "resources/list":
        return _result(
            request_id,
            {
                "resources": [
                    {
                        "uri": RESOURCE_URI,
                        "name": "Requirements Analysis Workbench",
                        "description": "Visual mode and output-module configuration.",
                        "mimeType": "text/html;profile=mcp-app",
                    }
                ]
            },
        )
    if method == "resources/read":
        uri = message.get("params", {}).get("uri")
        if uri != RESOURCE_URI:
            return _error(request_id, -32002, f"Unknown resource: {uri}")
        return _result(
            request_id,
            {
                "contents": [
                    {
                        "uri": RESOURCE_URI,
                        "mimeType": "text/html;profile=mcp-app",
                        "text": UI_PATH.read_text(encoding="utf-8"),
                        "_meta": {"ui": {"prefersBorder": True}},
                    }
                ]
            },
        )
    if method == "tools/call":
        params = message.get("params", {})
        name = params.get("name")
        arguments = params.get("arguments", {})
        try:
            if name == "open_workbench":
                return _result(request_id, _awaiting_selection_result())
            if name == "save_workbench_selection":
                return _result(request_id, _selection_result(arguments))
            return _error(request_id, -32601, f"Unknown tool: {name}")
        except ValueError as exc:
            return _error(request_id, -32602, str(exc))

    if request_id is None:
        return None
    return _error(request_id, -32601, f"Unknown method: {method}")


def main() -> int:
    # MCP stdio is UTF-8. Codex may launch Python under a legacy Windows code
    # page, so configure both streams explicitly and keep responses ASCII-safe.
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    for raw_line in sys.stdin:
        line = raw_line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
            response = handle(message)
        except (json.JSONDecodeError, OSError) as exc:
            response = _error(None, -32700, str(exc))
        if response is not None:
            sys.stdout.write(_serialize(response))
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
