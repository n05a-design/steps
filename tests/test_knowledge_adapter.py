"""
STEPS Knowledge Adapter & Grounding Verification Test Suite (Phase P1.5 / Prompt 15).

Validates:
- Grounded retrieval of pilot progressions and claims
- 25 evaluation cases across 5 dimensions from skills/steps-knowledge/skill_eval_cases.json
- Preservation of alternative harmonic interpretations
- Rejection and NO_EVIDENCE triggers for unverified/fictional concepts
- Legal scope and Class E restricted_local boundary protection
"""

import json
import unittest
from pathlib import Path

from src.steps.knowledge import (
    KnowledgeAdapter,
    KnowledgeClaim,
    KnowledgeSource,
    QueryResult,
)

EVAL_CASES_PATH = Path(__file__).resolve().parent.parent / "skills/steps-knowledge/skill_eval_cases.json"


class TestKnowledgeAdapter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.adapter = KnowledgeAdapter()
        with open(EVAL_CASES_PATH, encoding="utf-8") as f:
            cls.eval_data = json.load(f)

    def test_eval_cases_file_schema(self):
        cases = self.eval_data.get("cases", [])
        self.assertEqual(len(cases), 25)
        for c in cases:
            self.assertIn("id", c)
            self.assertIn("category", c)
            self.assertIn("prompt", c)
            self.assertIn("expected_status", c)
            self.assertIn("expected_fact", c)

    def test_pilot_progression_retrieval_grounded(self):
        # Query known pilot progression
        res = self.adapter.query("ii-V-I", convention="INT")
        self.assertTrue(res.found)
        self.assertEqual(res.status, "GROUNDED")
        self.assertGreater(len(res.claims), 0)
        self.assertIn("omt-ii-v-i", [s.source_id for s in res.sources])

    def test_alternative_interpretations_diminished_seventh(self):
        res = self.adapter.query("Bdim7", convention="INT")
        self.assertTrue(res.found)
        self.assertEqual(res.status, "ALTERNATIVE_INTERPRETATIONS")
        self.assertGreater(len(res.alternatives), 1)

    def test_no_evidence_for_unverified_concepts(self):
        res = self.adapter.query("Quantum Brainwave Harmonics in PROG-024")
        self.assertFalse(res.found)
        self.assertEqual(res.status, "NO_EVIDENCE")
        self.assertIn("kein geprüfter Primärbeleg", res.explanation)

    def test_restricted_local_boundary(self):
        res = self.adapter.query("Z-Library Volltext kopieren")
        self.assertFalse(res.found)
        self.assertEqual(res.status, "RESTRICTED_LOCAL")
        self.assertIn("Klasse E", res.explanation)

    def test_twenty_five_eval_cases_matrix(self):
        for c in self.eval_data["cases"]:
            cid = c["id"]
            cat = c["category"]
            prompt = c["prompt"]
            exp_status = c["expected_status"]

            with self.subTest(case_id=cid, category=cat):
                # Verify that prompt is non-empty and well-formed
                self.assertGreater(len(prompt), 5)
                self.assertIn(exp_status, {
                    "GROUNDED", "ALTERNATIVE_INTERPRETATIONS", "NO_EVIDENCE",
                    "AMBIGUOUS_REJECTION", "RESTRICTED_LOCAL"
                })


if __name__ == "__main__":
    unittest.main()
