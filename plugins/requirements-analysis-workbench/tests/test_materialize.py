"""Regression tests for the Requirements Workbench materialiser."""

from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PLUGIN_ROOT / "scripts" / "materialize_analysis.py"
DEMO_ANALYSIS = PLUGIN_ROOT / "assets" / "demo_analysis.json"

spec = importlib.util.spec_from_file_location("materialize_analysis", SCRIPT_PATH)
assert spec and spec.loader
materialize_analysis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(materialize_analysis)


class MaterialiseAnalysisTests(unittest.TestCase):
    def load_demo(self) -> dict:
        with DEMO_ANALYSIS.open("r", encoding="utf-8") as stream:
            return json.load(stream)

    def test_all_selected_modules_are_generated(self) -> None:
        data = self.load_demo()
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory)
            materialize_analysis.materialise(data, output, only=None)

            for module, filename in materialize_analysis.MODULE_FILES.items():
                self.assertIn(module, data["selected_modules"])
                self.assertTrue((output / filename).is_file(), filename)

            self.assertTrue((output / "review-index.md").is_file())
            self.assertTrue((output / "traceability.csv").is_file())
            self.assertTrue((output / "traceguard.json").is_file())
            self.assertTrue((output / "traceguard.md").is_file())
            self.assertNotIn("<script", (output / "wireframe.html").read_text().lower())

    def test_targeted_revision_preserves_other_module_hashes(self) -> None:
        original = self.load_demo()
        revised = copy.deepcopy(original)
        revised["use_cases"][0]["goal"] += " Confirmation is visible."

        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory)
            materialize_analysis.materialise(original, output, only=None)
            before = materialize_analysis.existing_module_hashes(
                output, original["selected_modules"]
            )

            materialize_analysis.materialise(revised, output, only="use-cases")
            after = materialize_analysis.existing_module_hashes(
                output, original["selected_modules"]
            )

            self.assertNotEqual(before["use-cases"], after["use-cases"])
            for module in original["selected_modules"]:
                if module != "use-cases":
                    self.assertEqual(before[module], after[module], module)

    def test_unknown_module_is_rejected(self) -> None:
        data = self.load_demo()
        data["selected_modules"] = ["context", "unknown-module"]
        with self.assertRaisesRegex(materialize_analysis.AnalysisError, "Unknown module"):
            materialize_analysis.validate_analysis(data)

    def test_configured_minimum_rejects_too_few_requirements(self) -> None:
        data = self.load_demo()
        data["requirements"] = data["requirements"][:10]
        with self.assertRaisesRegex(materialize_analysis.AnalysisError, "at least 11"):
            materialize_analysis.validate_analysis(data)

    def test_minimum_count_is_optional_for_general_users(self) -> None:
        data = self.load_demo()
        data["project"].pop("minimum_requirements")
        data["selected_modules"] = ["requirements"]
        data["requirements"] = data["requirements"][:3]
        materialize_analysis.validate_analysis(data)

    def test_requirement_categories_and_binding_language_are_checked(self) -> None:
        data = self.load_demo()
        data["requirements"][0]["category"] = "technical"
        with self.assertRaisesRegex(materialize_analysis.AnalysisError, "invalid category"):
            materialize_analysis.validate_analysis(data)

        data = self.load_demo()
        data["requirements"][0]["statement"] = "Users can submit a request."
        with self.assertRaisesRegex(materialize_analysis.AnalysisError, "must/shall"):
            materialize_analysis.validate_analysis(data)

    def test_dangling_trace_ids_are_rejected(self) -> None:
        data = self.load_demo()
        data["wireframe"]["screens"][0]["components"][0]["trace_ids"] = ["REQ-404"]
        with self.assertRaisesRegex(materialize_analysis.AnalysisError, "unknown trace ID"):
            materialize_analysis.validate_analysis(data)

    def test_native_wireframe_input_type_is_supported(self) -> None:
        rendered = materialize_analysis.render_component(
            {"kind": "input", "label": "Needed by", "input_type": "date"}
        )
        self.assertIn('type="date"', rendered)
        self.assertNotIn("textarea", rendered)

    def test_traceguard_resolves_exact_source_spans(self) -> None:
        data = self.load_demo()
        with tempfile.TemporaryDirectory() as temporary_directory:
            report = materialize_analysis.write_audit(
                data, Path(temporary_directory)
            )

            self.assertGreater(report["summary"]["exact_source_spans"], 0)
            self.assertFalse(
                any(
                    item["check_id"] == "TG-EVIDENCE-QUOTE"
                    for item in report["findings"]
                )
            )

    def test_traceguard_flags_cross_artefact_actor_drift(self) -> None:
        data = self.load_demo()
        data["use_cases"][0]["primary_actor"] = "Unmodelled Actor"
        with tempfile.TemporaryDirectory() as temporary_directory:
            report = materialize_analysis.write_audit(
                data, Path(temporary_directory)
            )

            self.assertTrue(
                any(
                    item["check_id"] == "TG-ACTOR-CONTEXT"
                    for item in report["findings"]
                )
            )

    def test_traceguard_requires_named_approval_for_high_impact_items(self) -> None:
        data = self.load_demo()
        with tempfile.TemporaryDirectory() as temporary_directory:
            report = materialize_analysis.write_audit(
                data, Path(temporary_directory)
            )

            self.assertEqual("abstain", report["status"])
            self.assertGreater(report["summary"]["abstain"], 0)

    def test_targeted_revision_writes_rollback_snapshot(self) -> None:
        original = self.load_demo()
        revised = copy.deepcopy(original)
        revised["use_cases"][0]["goal"] += " A rollback test change."

        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory)
            materialize_analysis.materialise(original, output, only=None)
            materialize_analysis.materialise(revised, output, only="use-cases")
            manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))

            rollback = manifest["traceguard"]["rollback_snapshot"]
            self.assertIsNotNone(rollback)
            self.assertTrue((output / rollback).is_file())


if __name__ == "__main__":
    unittest.main()
