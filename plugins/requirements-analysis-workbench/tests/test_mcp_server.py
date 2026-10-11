"""Protocol-level tests for the dependency-free MCP Apps server."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SERVER_PATH = PLUGIN_ROOT / "mcp" / "server.py"
DEMO_ANALYSIS = PLUGIN_ROOT / "assets" / "demo_analysis.json"

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


    def call_tool(self, name: str, arguments: dict) -> dict:
        return server.handle(
            {
                "jsonrpc": "2.0",
                "id": name,
                "method": "tools/call",
                "params": {"name": name, "arguments": arguments},
            }
        )

    def test_prompts_publish_every_skill_with_host_notes(self) -> None:
        listed = server.handle({"jsonrpc": "2.0", "id": 6, "method": "prompts/list"})
        names = [prompt["name"] for prompt in listed["result"]["prompts"]]
        self.assertEqual(
            ["analyze-requirements", "revise-requirements-module", "traceguard-audit"],
            names,
        )

        prompt = server.handle(
            {
                "jsonrpc": "2.0",
                "id": 7,
                "method": "prompts/get",
                "params": {
                    "name": "analyze-requirements",
                    "arguments": {"request": "A booking system for clinics."},
                },
            }
        )
        text = prompt["result"]["messages"][0]["content"]["text"]
        self.assertIn("open_workbench", text)
        self.assertIn(str(server.PLUGIN_ROOT), text)
        self.assertIn("A booking system for clinics.", text)

    def test_workflow_tools_return_skills_and_references(self) -> None:
        guide = self.call_tool("get_workflow_instructions", {"skill": "traceguard-audit"})
        self.assertIn("TraceGuard Audit", guide["result"]["content"][0]["text"])

        reference = self.call_tool(
            "read_workflow_reference",
            {"path": "analyze-requirements/references/output-contract.md"},
        )
        self.assertIn("Output contract", reference["result"]["content"][0]["text"])

        resources = server.handle({"jsonrpc": "2.0", "id": 8, "method": "resources/list"})
        uris = {item["uri"] for item in resources["result"]["resources"]}
        self.assertIn(server.RESOURCE_URI, uris)
        self.assertIn(
            "workbench://skills/analyze-requirements/references/knowledge-index.md", uris
        )

    def test_workflow_reference_rejects_paths_outside_skills(self) -> None:
        for path in (
            "../mcp/server.py",
            "../../README.md",
            "analyze-requirements/../../ui/workbench.html",
        ):
            with self.subTest(path=path):
                response = self.call_tool("read_workflow_reference", {"path": path})
                self.assertEqual(-32602, response["error"]["code"])

        response = server.handle(
            {
                "jsonrpc": "2.0",
                "id": 9,
                "method": "resources/read",
                "params": {"uri": "workbench://skills/../mcp/server.py"},
            }
        )
        self.assertEqual(-32002, response["error"]["code"])

    def test_materialize_audit_and_impact_tools_write_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "bundle"
            response = self.call_tool(
                "materialize_analysis",
                {"analysis_path": str(DEMO_ANALYSIS), "output_dir": str(output)},
            )
            structured = response["result"]["structuredContent"]
            self.assertEqual(str(output.resolve()), structured["output_dir"])
            self.assertIn("requirements.md", structured["module_files"])
            self.assertTrue((output / "manifest.json").is_file())
            server._serialize(response).encode("ascii")

            revised = json.loads((output / "analysis.json").read_text(encoding="utf-8"))
            revised["use_cases"][0]["goal"] += " Confirmation is visible."
            response = self.call_tool(
                "materialize_analysis",
                {"analysis": revised, "output_dir": str(output), "only": "use-cases"},
            )
            structured = response["result"]["structuredContent"]
            self.assertEqual("use-cases", structured["revision_target"])
            self.assertIn("requirements", structured["untouched_modules_verified"])

            audit = self.call_tool(
                "traceguard_audit",
                {
                    "analysis_path": str(output / "analysis.json"),
                    "output_dir": str(output),
                },
            )
            self.assertIn(
                audit["result"]["structuredContent"]["status"],
                {"pass", "review_required", "abstain"},
            )

            preview_path = output / "impact-preview.json"
            impact = self.call_tool(
                "traceguard_impact",
                {
                    "analysis_path": str(output / "analysis.json"),
                    "element_id": "FR-01",
                    "change": "Clarify the trigger.",
                    "output_path": str(preview_path),
                },
            )
            self.assertIn(
                "requirements", impact["result"]["structuredContent"]["affected_modules"]
            )
            self.assertTrue(preview_path.is_file())

    def test_invalid_analysis_is_reported_as_tool_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            response = self.call_tool(
                "materialize_analysis",
                {"analysis": {}, "output_dir": temporary_directory},
            )

        self.assertTrue(response["result"]["isError"])
        self.assertIn("ERROR:", response["result"]["content"][0]["text"])


if __name__ == "__main__":
    unittest.main()
