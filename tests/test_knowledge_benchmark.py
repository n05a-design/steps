"""Exercise the pilot benchmark, targeted negative cases, and coach grading."""

from __future__ import annotations

from collections import Counter
import unittest

from scripts import audit_knowledge_coverage as coverage
from scripts import run_knowledge_benchmark as benchmark
from src.steps.progression import reviewed


class KnowledgeBenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = benchmark.load_cases()
        cls.examples, cls.claims = reviewed._candidates()

    def test_current_pilots_pass_independent_reference_cases(self):
        pilot = [case for case in self.cases if case["scope"] == "pilot" and case["mandatory"]]
        self.assertEqual({case["id"] for case in pilot}, self.claims.keys())
        self.assertEqual(len(pilot), 8)
        for result in benchmark.run(pilot, self.examples, self.claims, {}):
            with self.subTest(claim=result["id"]):
                self.assertEqual(result["status"], "PASS", result["observed"])

    def test_benchmark_rejects_wrong_expected_pitch_classes(self):
        case = next(case for case in self.cases if case["id"] == "PROG-001-HARMONY")
        altered = {**case, "expected": {**case["expected"], "pitch_classes": [[0, 3, 7]]}}
        result, = benchmark.run([altered], self.examples, self.claims, {})
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["observed"]["resolved"][0], [0, 4, 7])

    def test_coach_rubric_requires_response_all_criteria_and_sources(self):
        case = next(case for case in self.cases if case["scope"] == "coach")
        grade = {"reviewer": "Synthetic fixture", "response": "Synthetic response",
                 "source_evidence": "Synthetic locator and checked excerpt",
                 "criteria": dict.fromkeys(case["expected"], True), "sources_verified": True}
        for input_data, status in (
            ({}, "PENDING"), ({case["id"]: grade}, "PASS"),
            ({case["id"]: {**grade, "sources_verified": False}}, "FAIL"),
            ({case["id"]: {**grade, "criteria": {}}}, "FAIL"),
        ):
            result, = benchmark.run([case], self.examples, self.claims, input_data)
            self.assertEqual(result["status"], status)

    def test_coverage_counts_partition_and_benchmark_reaches_all_domains(self):
        self.assertEqual({case["domain"] for case in self.cases}, {f"M{i:02}" for i in range(1, 13)})
        result = coverage.summarize(coverage.audit())
        count = Counter({row["Bereich"]: row["Gesamt"] for row in result})
        self.assertEqual(count["Pilot-Lernaussagen"], 8)
        self.assertEqual(count["Progressionspositionen"], 116)
        for row in result:
            self.assertEqual(row["Gesamt"], row["Formal_geprüft"] + row["Inventar_only"])
            self.assertEqual(row["Gesamt"], row["Fachlich_untersucht"] + row["Fachlich_offen"])
