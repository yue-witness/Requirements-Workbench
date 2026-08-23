"""Protocol-level tests for the dependency-free MCP Apps server."""

from __future__ import annotations

import importlib.util
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
        self.assertIn("@mentions this plugin", tools["open_workbench"]["description"])

        initialize = server.handle(
            {"jsonrpc": "2.0", "id": 11, "method": "initialize", "params": {}}
        )
        self.assertIn(
            "open the workbench before analysis by default",
            initialize["result"]["instructions"],
        )

    def test_ui_resource_contains_modes_and_six_module_checkboxes(self) -> None:
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
        self.assertEqual(6, html.count('type="checkbox" name="modules"'))

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
