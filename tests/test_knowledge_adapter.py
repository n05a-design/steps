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
from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock

from scripts.evaluate_knowledge_adapter import evaluate, run
from src.steps.knowledge import KnowledgeAdapter
from src.steps.progression import get_progression, reviewed

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

    def test_unreviewed_interpretations_have_no_evidence(self):
        for query in ("Bdim7", "diminished", "bVII", "modal interchange", "dimension"):
            with self.subTest(query=query):
                result = self.adapter.query(query, convention="INT")
                self.assertEqual(result.status, "NO_EVIDENCE")
                self.assertFalse(result.found)
                self.assertFalse(result.claims or result.sources or result.alternatives)

    def test_exact_query_preserves_all_validated_citations(self):
        expected = {
            (reference.source_id, reference.locator)
            for approved in reviewed.load_reviewed_catalog()[0].claims[1:]
            for reference in approved.claim.citations
        }
        result = self.adapter.query("Axis")
        self.assertEqual({(source.source_id, source.locator) for source in result.sources}, expected)
        self.assertEqual([claim.claim_id for claim in result.claims],
                         ["PROG-001-HARMONY", "PROG-001-TONAL-CENTER"])
        self.assertTrue(all(claim.verified and claim.citations for claim in result.claims))
        self.assertEqual(self.adapter.query("doo-wop").status, "NO_EVIDENCE")
        self.assertEqual(self.adapter.query("IV-I").status, "NO_EVIDENCE")

        concepts = json.loads(EVAL_CASES_PATH.with_name("index.json").read_text(encoding="utf-8"))["concepts"]
        for name, entry in concepts.items():
            with self.subTest(concept=name):
                lookup = self.adapter.query(name)
                if entry["publication_status"] == "reviewed_pilot":
                    self.assertEqual([claim.claim_id for claim in lookup.claims], entry["claims"])
                    self.assertEqual({src.source_id for src in lookup.sources}, set(entry["sources"]))
                else:
                    self.assertEqual(lookup.status, "NO_EVIDENCE")
        doo_wop = concepts["doo-wop"]
        self.assertEqual(doo_wop["claims"], [])
        self.assertEqual(get_progression(doo_wop["prog_id"]).roman_numerals, "I - vi - IV - V")

    def test_notation_projection_preserves_reviewed_notes_and_sources(self):
        for concept, international, german in (
            ("PROG-003-VOICE-II-V", "zu B im", "zu H im"),
            ("PROG-009-VOICE-LEADING", "Ab in", "As in"),
        ):
            result_int = self.adapter.query(concept, "INT")
            result_de = self.adapter.query(concept, "DE")
            self.assertIn(international, result_int.claims[0].summary)
            self.assertIn(german, result_de.claims[0].summary)
            self.assertEqual(result_int.sources, result_de.sources)
            self.assertEqual(self.adapter.get_claim(concept), result_de.claims[0])
        self.assertEqual(self.adapter.query("B").status, "AMBIGUOUS_REJECTION")
        self.assertEqual(self.adapter.query("B", "DE").status, "GROUNDED")

    def test_disallowed_claim_data_cannot_reach_query_or_claim_lookup(self):
        catalog = json.loads(reviewed.CATALOG.read_text(encoding="utf-8"))
        registry = json.loads(reviewed.REGISTRY.read_text(encoding="utf-8"))
        with TemporaryDirectory() as directory:
            path = Path(directory) / "candidate.json"
            path.write_text(json.dumps(catalog), encoding="utf-8")
            self.assertTrue(KnowledgeAdapter(reviewed_progressions=path).query("ii-V-I").found)
            catalog["examples"][1]["claims"][0]["text"] = "Eine ungeprüfte Änderung am Lerntext."
            path.write_text(json.dumps(catalog), encoding="utf-8")
            with self.assertLogs("src.steps.knowledge.adapter", level="WARNING"):
                altered = KnowledgeAdapter(reviewed_progressions=path)
            self.assertIsNone(altered.get_claim("PROG-003-HARMONY"))
            self.assertEqual(altered.query("ii-V-I").status, "NO_EVIDENCE")
            path.write_text("{", encoding="utf-8")
            with self.assertLogs("src.steps.knowledge.adapter", level="WARNING"):
                invalid = KnowledgeAdapter(reviewed_progressions=path)
            self.assertEqual(invalid.query("ii-V-I").status, "NO_EVIDENCE")

            source = next(row for row in registry["sources"] if row["id"] == "omt-ii-v-i")
            for rights in (None, "review_required"):
                with self.subTest(rights=rights):
                    if rights is None:
                        source.pop("rights_status", None)
                    else:
                        source["rights_status"] = rights
                    path.write_text(json.dumps(registry), encoding="utf-8")
                    with self.assertLogs("src.steps.knowledge.adapter", level="WARNING"):
                        unapproved = KnowledgeAdapter(product_registry=path)
                    result = unapproved.query("ii-V-I")
                    self.assertEqual(result.status, "NO_EVIDENCE")
                    self.assertFalse(result.claims or result.sources)

    def test_no_evidence_for_unverified_concepts(self):
        for query in ("", "  ", "jazz", "Jazz-Achtelnoten bei Swing", "PROG-003 und unbekannte Skalen",
                      "Quantum Brainwave Harmonics in PROG-024"):
            with self.subTest(query=query):
                result = self.adapter.query(query)
                self.assertFalse(result.found)
                self.assertEqual(result.status, "NO_EVIDENCE")
                self.assertIn("kein geprüfter Primärbeleg", result.explanation)

    def test_restricted_local_boundary(self):
        res = self.adapter.query("Z-Library Volltext kopieren")
        self.assertFalse(res.found)
        self.assertEqual(res.status, "RESTRICTED_LOCAL")
        self.assertIn("Klasse E", res.explanation)

    def test_twenty_five_eval_cases_matrix(self):
        for case in run():
            with self.subTest(case=case["id"]):
                self.assertTrue(case["runtime_pass"], case)

    def test_correct_status_without_the_approved_citation_fails_evaluation(self):
        case = self.eval_data["cases"][0]
        result = self.adapter.query(case["prompt"])
        without_sources = replace(result, sources=())
        self.assertFalse(evaluate([case], Mock(query=Mock(return_value=without_sources)))[0]["runtime_pass"])

    def test_false_explanation_and_unverified_alternatives_fail_evaluation(self):
        grounded = self.eval_data["cases"][0]
        unavailable = self.eval_data["cases"][2]
        for case, mutation in (
            (grounded, {"explanation": "Deutsches B und internationales B sind derselbe Ton."}),
            (grounded, {"alternatives": ("Unbelegte Deutung",)}),
            (unavailable, {"alternatives": ("Unbelegte Deutung",)}),
            (unavailable, {"explanation": "Unbelegte musikalische Aussage."}),
        ):
            with self.subTest(case=case["id"], mutation=mutation):
                result = replace(self.adapter.query(case["prompt"]), **mutation)
                self.assertFalse(evaluate([case], Mock(query=Mock(return_value=result)))[0]["runtime_pass"])

    def test_explicit_english_notation_questions_use_reviewed_comparison(self):
        for notation in ("German", "international"):
            with self.subTest(notation=notation):
                result = self.adapter.query(f"What note is B in {notation} notation?")
                self.assertEqual([claim.claim_id for claim in result.claims], [reviewed.NOTATION])
                self.assertEqual([source.source_id for source in result.sources], ["yale-key-names"])
        self.assertEqual(self.adapter.query("What note is B in music?").status, "NO_EVIDENCE")


if __name__ == "__main__":
    unittest.main()
