"""Structural tests for the selectively loaded analysis knowledge base."""

from __future__ import annotations

import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = PLUGIN_ROOT / "skills" / "analyze-requirements"


class KnowledgeRoutingTests(unittest.TestCase):
    def test_entrypoint_routes_through_knowledge_index(self) -> None:
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("references/knowledge-index.md", skill_text)
        self.assertIn("never as evidence", skill_text)

    def test_index_links_to_existing_focused_references(self) -> None:
        index_path = SKILL_ROOT / "references" / "knowledge-index.md"
        index_text = index_path.read_text(encoding="utf-8")
        expected = [
            "problem-framing-and-domain-models.md",
            "requirement-quality-and-traceability.md",
            "stakeholders-and-behavioural-models.md",
            "delivery-planning-and-handoff.md",
        ]

        for filename in expected:
            with self.subTest(filename=filename):
                self.assertIn(filename, index_text)
                self.assertTrue(
                    (index_path.parent / "knowledge" / filename).is_file()
                )


if __name__ == "__main__":
    unittest.main()
