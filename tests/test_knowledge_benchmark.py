"""Exercise the pilot benchmark, targeted negative cases, and coach grading."""

from __future__ import annotations

import subprocess
import unittest
from copy import deepcopy
from unittest.mock import patch

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
                 "fingerprint": benchmark.case_fingerprint(case), "model": "Synthetic model",
                 "skill_revision": "Synthetic revision", "run_evidence": "Synthetic run",
                 "source_evidence": "Synthetic locator and checked excerpt",
                 "criteria": dict.fromkeys(case["expected"], True), "sources_verified": True}
        for input_data, status in (
            ({}, "PENDING"), ({case["id"]: grade}, "PASS"),
            ({case["id"]: {**grade, "sources_verified": False}}, "FAIL"),
            ({case["id"]: {**grade, "criteria": {}}}, "FAIL"),
            ({case["id"]: {**grade, "fingerprint": "stale"}}, "PENDING"),
        ):
            result, = benchmark.run([case], self.examples, self.claims, input_data)
            self.assertEqual(result["status"], status)

    def test_corrected_catalog_and_learning_cases(self):
        contents = {"PROG-008", "PROG-016", "PROG-020", "PROG-027", "P12", "P16", "P19", "PAT-026"}
        cases = [case for case in self.cases if case["scope"] == "catalog" and case["content"] in contents]
        self.assertEqual({case["content"] for case in cases}, contents)
        for result in benchmark.run(cases, self.examples, self.claims, {}):
            with self.subTest(case=result["id"]):
                self.assertEqual(result["status"], "PASS", result["observed"])

    def test_p16_detects_wrong_notated_extension(self):
        case = next(case for case in self.cases if case["id"] == "KB-P16")
        document = benchmark.PIANO.read_text(encoding="utf-8")
        self.assertIn("D4 F#4 A4", document)
        mutated = document.replace("D4 F#4 A4", "D4 F4 A4")
        with patch.object(type(benchmark.PIANO), "read_text", return_value=mutated):
            result, = benchmark.run([case], self.examples, self.claims, {})
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["observed"]["upper_intervals"], [14, 17, 21])

    def test_minor_cadence_requires_whole_tone_and_chord_membership(self):
        case = next(c for c in self.cases if c["id"] == "KB-CLAIM-032-MINOR")
        result, = benchmark.run([case], self.examples, self.claims, {})
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["observed"], {"major": [-1, -1], "minor": [-1, -2]})
        mutated = deepcopy(case)
        mutated["input"]["minor"]["paths"][1][1] = "E4"
        result, = benchmark.run([mutated], self.examples, self.claims, {})
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["observed"]["error"], "note outside chord")

    def test_manual_evidence_is_bound_to_case_and_revision(self):
        case = next(case for case in self.cases if case["method"] == "manual")
        grade = {
            "fingerprint": benchmark.case_fingerprint(case),
            "git_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=benchmark.ROOT, text=True).strip(),
            "reviewer": "Synthetic reviewer", "evidence": "Synthetic session",
            "observations": "Synthetic notes", "criteria": dict.fromkeys(case["expected"], True),
        }
        for evidence, expected in (
            (None, "PENDING"), (grade, "PASS"), ({**grade, "fingerprint": "stale"}, "PENDING"),
            ({**grade, "git_sha": "0" * 40}, "PENDING"), ({**grade, "criteria": {}}, "FAIL"),
        ):
            result, = benchmark.run([case], self.examples, self.claims, {}, {case["id"]: evidence})
            self.assertEqual(result["status"], expected)
            self.assertEqual(bool(result["next_step"]), expected != "PASS")

    def test_coverage_counts_partition_and_coach_rubric_reaches_all_domains(self):
        self.assertEqual(
            {case["domain"] for case in self.cases if case["scope"] == "coach"},
            {f"M{i:02}" for i in range(1, 13)},
        )
        result = coverage.read_csv(coverage.MATRIX)
        count = {row["Bereich"]: int(row["Gesamt"]) for row in result}
        self.assertEqual(count["Pilot-Lernaussagen"], 8)
        self.assertEqual(count["Progressionspositionen"], 116)
        for row in result:
            def n(key):
                return int(row[key])
            self.assertEqual(n("Gesamt"), n("Formal_geprüft") + n("Inventar_only"))
            self.assertEqual(n("Gesamt"), n("Fachlich_untersucht") + n("Fachlich_offen"))
            self.assertEqual(n("Gesamt"), n("Fachlich_vollständig") + n("Fachlich_Stichprobe") + n("Fachlich_nicht_geprüft"))
