"""Protocol-level tests for the dependency-free MCP Apps server."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SERVER_PATH = PLUGIN_ROOT / "mcp" / "server.py"

spec = importlib.util.spec_from_file_location("workbench_mcp_server", SERVER_PATH)
assert spec and spec.loader
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)


class WorkbenchMcpServerTests(unittest.TestCase):
    def test_tool_list_exposes_visual_and_structured_tools(self) -> None:
        response = server.handle({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
        tools = {item["name"]: item for item in response["result"]["tools"]}

        self.assertIn("open_workbench", tools)
        self.assertIn("save_workbench_selection", tools)
        self.assertEqual(
            server.RESOURCE_URI,
            tools["open_workbench"]["_meta"]["ui"]["resourceUri"],
        )
        self.assertIn(
            "wait for an explicit save_workbench_selection result",
            tools["open_workbench"]["description"],
        )

        initialize = server.handle(
            {"jsonrpc": "2.0", "id": 11, "method": "initialize", "params": {}}
        )
        self.assertIn(
            "open the workbench before analysis by default",
            initialize["result"]["instructions"],
        )
        self.assertIn("hard stop", initialize["result"]["instructions"])

    def test_ui_resource_contains_modes_and_eleven_module_checkboxes(self) -> None:
        response = server.handle(
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "resources/read",
                "params": {"uri": server.RESOURCE_URI},
            }
        )
        html = response["result"]["contents"][0]["text"]

        self.assertIn('value="guided"', html)
        self.assertIn('value="standard"', html)
        self.assertIn('value="professional"', html)
        self.assertEqual(11, html.count('type="checkbox" name="modules"'))
        for module in (
            "problem-vision-scope",
            "domain-model",
            "feasibility",
            "data-io",
            "lifecycle-roadmap",
        ):
            self.assertIn(f'value="{module}"', html)
        self.assertIn('"ui/initialize"', html)
        self.assertIn('"ui/notifications/initialized"', html)
        self.assertIn('"ui/notifications/size-changed"', html)
        self.assertIn('"tools/call"', html)

    def test_stdio_serialization_is_ascii_safe_and_round_trips_unicode(self) -> None:
        response = {
            "jsonrpc": "2.0",
            "id": "unicode-probe",
            "result": {"text": "选择已确认…"},
        }

        serialized = server._serialize(response)
        serialized.encode("ascii")

        self.assertEqual(response, json.loads(serialized))

    def test_ui_resource_response_is_ascii_safe(self) -> None:
        response = server.handle(
            {
                "jsonrpc": "2.0",
                "id": "resource-probe",
                "method": "resources/read",
                "params": {"uri": server.RESOURCE_URI},
            }
        )

        server._serialize(response).encode("ascii")

    def test_open_workbench_waits_without_confirming_defaults(self) -> None:
        response = server.handle(
            {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {"name": "open_workbench", "arguments": {}},
            }
        )
        result = response["result"]

        self.assertEqual(
            "awaiting_user_selection", result["structuredContent"]["state"]
        )
        self.assertFalse(result["structuredContent"]["confirmed"])
        self.assertIsNone(result["structuredContent"]["selection"])
        self.assertIn("WORKFLOW_BLOCKED", result["content"][0]["text"])

    def test_saved_selection_is_explicitly_confirmed(self) -> None:
        response = server.handle(
            {
                "jsonrpc": "2.0",
                "id": 5,
                "method": "tools/call",
                "params": {
                    "name": "save_workbench_selection",
                    "arguments": {
                        "mode": "professional",
                        "modules": ["requirements", "context"],
                    },
                },
            }
        )
        structured = response["result"]["structuredContent"]

        self.assertEqual("selection_confirmed", structured["state"])
        self.assertTrue(structured["confirmed"])
        self.assertEqual(
            ["requirements", "context"], structured["selection"]["modules"]
        )

    def test_selection_rejects_empty_modules(self) -> None:
        response = server.handle(
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "save_workbench_selection",
                    "arguments": {"mode": "guided", "modules": []},
                },
            }
        )

        self.assertEqual(-32602, response["error"]["code"])


if __name__ == "__main__":
    unittest.main()
