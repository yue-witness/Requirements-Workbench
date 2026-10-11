#!/usr/bin/env python3
"""Dependency-free MCP server for the Requirements Analysis Workbench.

The server exposes a visual configuration resource and a matching structured
tool. The tools remain useful when a client cannot render MCP Apps UI.

It also carries the whole workflow for hosts that load MCP servers but not the
bundled skills (Antigravity, DeepSeek Harness, Cursor, Windsurf, VS Code,
Gemini CLI, Claude Desktop, and others): the skills are published as MCP
prompts and resources, and the deterministic materialiser and TraceGuard run
as tools.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import sys
from pathlib import Path
from types import ModuleType
from typing import Any


SERVER_NAME = "requirements-analysis-workbench"
SERVER_VERSION = "0.5.0"
RESOURCE_URI = "ui://requirements-analysis-workbench/workbench.html"
PLUGIN_ROOT = Path(__file__).resolve().parents[1]
UI_PATH = PLUGIN_ROOT / "ui" / "workbench.html"
SKILLS_ROOT = PLUGIN_ROOT / "skills"
SCRIPTS_ROOT = PLUGIN_ROOT / "scripts"
SKILL_URI_PREFIX = "workbench://skills/"
WORKSPACE_ENV = "REQUIREMENTS_WORKBENCH_WORKSPACE"
SKILLS = {
    "analyze-requirements": (
        "Analyse a software idea, scenario, user stories, or notes into the "
        "selected requirements artefacts."
    ),
    "revise-requirements-module": (
        "Revise one existing output module while preserving every other module file."
    ),
    "traceguard-audit": (
        "Audit an existing bundle for evidence spans, consistency, change impact, "
        "rollback, and approvals."
    ),
}
MODULES = [
    "problem-vision-scope",
    "requirements",
    "fishbone",
    "context",
    "domain-model",
    "use-cases",
    "activity",
    "wireframe",
    "feasibility",
    "data-io",
    "lifecycle-roadmap",
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
    read_only = {
        "readOnlyHint": True,
        "destructiveHint": False,
        "openWorldHint": False,
    }
    writes_files = {
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
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
        {
            "name": "get_workflow_instructions",
            "title": "Get workflow instructions",
            "description": (
                "Return the full instructions of a bundled workflow skill. Call this first "
                "when the host has not loaded the Requirements Analysis Workbench skills."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {"skill": {"type": "string", "enum": list(SKILLS)}},
                "required": ["skill"],
                "additionalProperties": False,
            },
            "annotations": read_only,
        },
        {
            "name": "read_workflow_reference",
            "title": "Read workflow reference",
            "description": (
                "Read a Markdown reference used by a workflow skill, such as "
                "analyze-requirements/references/output-contract.md. Paths are relative "
                "to the skills directory."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
                "additionalProperties": False,
            },
            "annotations": read_only,
        },
        {
            "name": "materialize_analysis",
            "title": "Materialise analysis",
            "description": (
                "Validate canonical analysis JSON and write the selected module files plus "
                "analysis.json, manifest.json, review-index.md, traceability.csv, and "
                "TraceGuard reports. Supply analysis_path or an inline analysis object. "
                "Use absolute paths; relative paths resolve against "
                f"{WORKSPACE_ENV} or the server working directory. Set only to "
                "regenerate one module while preserving the other module files."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "analysis_path": {"type": "string"},
                    "analysis": {"type": "object"},
                    "output_dir": {"type": "string"},
                    "only": {"type": "string", "enum": MODULES},
                },
                "required": ["output_dir"],
                "additionalProperties": False,
            },
            "annotations": writes_files,
        },
        {
            "name": "traceguard_audit",
            "title": "Run TraceGuard audit",
            "description": (
                "Audit an analysis.json file and write traceguard.json and traceguard.md "
                "into output_dir. A pass means only that the deterministic checks passed."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "analysis_path": {"type": "string"},
                    "output_dir": {"type": "string"},
                },
                "required": ["analysis_path", "output_dir"],
                "additionalProperties": False,
            },
            "annotations": writes_files,
        },
        {
            "name": "traceguard_impact",
            "title": "Preview change impact",
            "description": (
                "Preview which modules a change to a shared stable ID affects. This never "
                "edits the bundle; the reviewer must still choose propagate, "
                "local-override, or cancel. Optionally writes the preview to output_path."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "analysis_path": {"type": "string"},
                    "element_id": {"type": "string"},
                    "change": {"type": "string"},
                    "action": {
                        "type": "string",
                        "enum": ["propagate", "local-override", "cancel"],
                        "default": "propagate",
                    },
                    "output_path": {"type": "string"},
                },
                "required": ["analysis_path", "element_id", "change"],
                "additionalProperties": False,
            },
            "annotations": writes_files,
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


def _load_script(name: str) -> ModuleType:
    """Import a bundled script once so tools share the CLI implementation."""

    module_name = f"requirements_workbench_{name}"
    if module_name in sys.modules:
        return sys.modules[module_name]
    spec = importlib.util.spec_from_file_location(module_name, SCRIPTS_ROOT / f"{name}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _resolve(path_text: Any, field: str) -> Path:
    if not isinstance(path_text, str) or not path_text.strip():
        raise ValueError(f"{field} must be a non-empty path")
    path = Path(path_text).expanduser()
    if not path.is_absolute():
        path = Path(os.environ.get(WORKSPACE_ENV) or os.getcwd()) / path
    return path.resolve()


def _skill_file(relative: Any) -> Path:
    """Resolve a path inside the bundled skills directory only."""

    if not isinstance(relative, str) or not relative.strip():
        raise ValueError("path must name a file inside the skills directory")
    root = SKILLS_ROOT.resolve()
    path = (root / relative.replace("\\", "/")).resolve()
    if root not in path.parents or path.suffix != ".md" or not path.is_file():
        raise ValueError(f"Unknown workflow reference: {relative}")
    return path


def _skill_files() -> list[Path]:
    return sorted(SKILLS_ROOT.rglob("*.md"))


def _host_notes(skill: str) -> str:
    return (
        "Host notes for this MCP session:\n"
        f"- Plugin root: {PLUGIN_ROOT}\n"
        f"- Relative reference paths in this guide are relative to {SKILLS_ROOT / skill}; "
        "read them with read_workflow_reference (for example "
        f"'{skill}/references/...') or from the file system.\n"
        "- Prefer the MCP tools materialize_analysis, traceguard_audit, and "
        "traceguard_impact over running scripts; they run the same code. Pass absolute "
        "paths inside the user's workspace.\n"
        "- If the host cannot render the visual workbench, use its structured "
        "question tool or ask in conversation, and wait for an explicit selection."
    )


def _workflow_text(skill: str) -> str:
    if skill not in SKILLS:
        raise ValueError("skill must be one of: " + ", ".join(SKILLS))
    body = (SKILLS_ROOT / skill / "SKILL.md").read_text(encoding="utf-8")
    return body.rstrip() + "\n\n---\n\n" + _host_notes(skill) + "\n"


def _text_result(text: str, structured: dict[str, Any] | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {"content": [{"type": "text", "text": text}]}
    if structured is not None:
        result["structuredContent"] = structured
    return result


def _run_quietly(function: Any, *args: Any) -> Any:
    # stdout carries JSON-RPC, so nothing a script prints may reach it.
    with contextlib.redirect_stdout(io.StringIO()):
        return function(*args)


def _materialize(arguments: dict[str, Any]) -> dict[str, Any]:
    materializer = _load_script("materialize_analysis")
    out_dir = _resolve(arguments.get("output_dir"), "output_dir")
    only = arguments.get("only")
    if "analysis" in arguments:
        data = arguments["analysis"]
        if not isinstance(data, dict):
            raise ValueError("analysis must be a JSON object")
    else:
        data = materializer.load_analysis(
            _resolve(arguments.get("analysis_path"), "analysis_path")
        )
    _run_quietly(materializer.materialise, data, out_dir, only)
    manifest = json.loads((out_dir / "manifest.json").read_text(encoding="utf-8"))
    files = sorted(entry["path"] for entry in manifest["files"].values())
    target = f"module '{only}'" if only else "selected modules"
    return _text_result(
        f"Generated {target} in {out_dir}. TraceGuard status: "
        f"{manifest['traceguard']['status']}. Review traceguard.md and review-index.md.",
        {
            "output_dir": str(out_dir),
            "module_files": files,
            "revision_target": only,
            "untouched_modules_verified": manifest["untouched_modules_verified"],
            "quality_warnings": manifest["quality_warnings"],
            "traceguard": manifest["traceguard"],
        },
    )


def _traceguard_audit(arguments: dict[str, Any]) -> dict[str, Any]:
    traceguard = _load_script("traceguard")
    data = traceguard._load(_resolve(arguments.get("analysis_path"), "analysis_path"))
    out_dir = _resolve(arguments.get("output_dir"), "output_dir")
    report = _run_quietly(traceguard.write_audit, data, out_dir)
    return _text_result(
        f"TraceGuard status: {report['status']}. Reports written to "
        f"{out_dir / 'traceguard.md'} and {out_dir / 'traceguard.json'}.",
        {"output_dir": str(out_dir), "status": report["status"], "summary": report["summary"]},
    )


def _traceguard_impact(arguments: dict[str, Any]) -> dict[str, Any]:
    traceguard = _load_script("traceguard")
    data = traceguard._load(_resolve(arguments.get("analysis_path"), "analysis_path"))
    preview = traceguard.preview_impact(
        data,
        str(arguments.get("element_id", "")),
        str(arguments.get("change", "")),
        str(arguments.get("action", "propagate")),
    )
    if arguments.get("output_path"):
        output_path = _resolve(arguments["output_path"], "output_path")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(preview, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        preview = {**preview, "written_to": str(output_path)}
    modules = ", ".join(preview["affected_modules"]) or "none"
    return _text_result(
        f"Change to {preview['element_id']} affects: {modules}. Ask the reviewer to "
        "choose propagate, local-override, or cancel before editing.",
        preview,
    )


def _prompt_definitions() -> list[dict[str, Any]]:
    return [
        {
            "name": name,
            "title": name.replace("-", " ").capitalize(),
            "description": description,
            "arguments": [
                {
                    "name": "request",
                    "description": "The scenario, notes, or change request to work on.",
                    "required": False,
                }
            ],
        }
        for name, description in SKILLS.items()
    ]


def _get_prompt(params: dict[str, Any]) -> dict[str, Any]:
    name = params.get("name")
    if name not in SKILLS:
        raise ValueError(f"Unknown prompt: {name}")
    request = str((params.get("arguments") or {}).get("request", "")).strip()
    text = (
        "Follow this Requirements Analysis Workbench workflow.\n\n"
        + _workflow_text(name)
        + "\nUser request:\n"
        + (request or "(Ask the user for their material and selection.)")
    )
    return {
        "description": SKILLS[name],
        "messages": [{"role": "user", "content": {"type": "text", "text": text}}],
    }


def _resource_list() -> list[dict[str, Any]]:
    resources = [
        {
            "uri": RESOURCE_URI,
            "name": "Requirements Analysis Workbench",
            "description": "Visual mode and output-module configuration.",
            "mimeType": "text/html;profile=mcp-app",
        }
    ]
    for path in _skill_files():
        relative = path.relative_to(SKILLS_ROOT).as_posix()
        resources.append(
            {
                "uri": SKILL_URI_PREFIX + relative,
                "name": relative,
                "description": "Requirements Analysis Workbench workflow guidance.",
                "mimeType": "text/markdown",
            }
        )
    return resources


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
                "capabilities": {"tools": {}, "resources": {}, "prompts": {}},
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
                    "Keep TraceGuard results visible and require named approval for abstained high-impact items. "
                    "If the host has not loaded the bundled skills, call get_workflow_instructions "
                    "(analyze-requirements, revise-requirements-module, or traceguard-audit) before "
                    "starting and generate files with materialize_analysis."
                ),
            },
        )

    if method in {"notifications/initialized", "notifications/cancelled"}:
        return None
    if method == "tools/list":
        return _result(request_id, {"tools": _tool_definitions()})
    if method == "ping":
        return _result(request_id, {})
    if method == "resources/list":
        return _result(request_id, {"resources": _resource_list()})
    if method == "prompts/list":
        return _result(request_id, {"prompts": _prompt_definitions()})
    if method == "prompts/get":
        try:
            return _result(request_id, _get_prompt(message.get("params", {})))
        except ValueError as exc:
            return _error(request_id, -32602, str(exc))
    if method == "resources/read":
        uri = message.get("params", {}).get("uri")
        if isinstance(uri, str) and uri.startswith(SKILL_URI_PREFIX):
            try:
                path = _skill_file(uri[len(SKILL_URI_PREFIX):])
            except ValueError:
                return _error(request_id, -32002, f"Unknown resource: {uri}")
            return _result(
                request_id,
                {
                    "contents": [
                        {
                            "uri": uri,
                            "mimeType": "text/markdown",
                            "text": path.read_text(encoding="utf-8"),
                        }
                    ]
                },
            )
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
            if name == "get_workflow_instructions":
                return _result(
                    request_id, _text_result(_workflow_text(str(arguments.get("skill"))))
                )
            if name == "read_workflow_reference":
                path = _skill_file(arguments.get("path"))
                return _result(request_id, _text_result(path.read_text(encoding="utf-8")))
            handler = TOOL_HANDLERS.get(name)
            if handler is None:
                return _error(request_id, -32601, f"Unknown tool: {name}")
        except ValueError as exc:
            return _error(request_id, -32602, str(exc))
        try:
            return _result(request_id, handler(arguments))
        except (ValueError, OSError) as exc:
            # Domain failures are tool results so the model can read and fix them.
            return _result(
                request_id,
                {"isError": True, "content": [{"type": "text", "text": f"ERROR: {exc}"}]},
            )

    if request_id is None:
        return None
    return _error(request_id, -32601, f"Unknown method: {method}")


TOOL_HANDLERS = {
    "materialize_analysis": _materialize,
    "traceguard_audit": _traceguard_audit,
    "traceguard_impact": _traceguard_impact,
}


def main() -> int:
    # MCP stdio is UTF-8. Hosts may launch Python under a legacy Windows code
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
