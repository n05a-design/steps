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
        contents = {"PROG-008", "PROG-016", "PROG-020", "PROG-027", "P12", "P16", "P19", "PAT-026", "PAT-027", "PAT-028", "PAT-029"}
        cases = [case for case in self.cases if case["scope"] == "catalog" and case["content"] in contents]
        self.assertEqual({case["content"] for case in cases}, contents)
        for result in benchmark.run(cases, self.examples, self.claims, {}):
            with self.subTest(case=result["id"]):
                self.assertEqual(result["status"], "PASS", result["observed"])

    def test_latin_timing_detects_changed_catalog_raster(self):
        document = benchmark.LATIN.read_text(encoding="utf-8")
        original_read = type(benchmark.LATIN).read_text
        for pattern, original, altered in (
            ("PAT-027", "| 2 | 4, 10 |", "| 2 | 4, 9 |"),
            ("PAT-028", "| 1 | 12, 14 |", "| 1 | 12, 16 |"),
            ("PAT-029", "105 Halbe | 480", "105 Viertel | 480"),
        ):
            case = next(case for case in self.cases if case["id"] == f"KB-{pattern}-RASTER")
            self.assertEqual(document.count(original), 1)
            mutated = document.replace(original, altered)

            def read(path, *args, **kwargs):
                return mutated if path == benchmark.LATIN else original_read(path, *args, **kwargs)

            with self.subTest(pattern=pattern), patch.object(type(benchmark.LATIN), "read_text", read):
                result, = benchmark.run([case], self.examples, self.claims, {})
                self.assertEqual(result["status"], "FAIL")

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

    def test_sample_cases_consume_inputs_and_check_observed_citation_fields(self):
        cases = {case["id"]: case for case in self.cases}
        for ident, field, value in (
            ("KB-M02-ENHARMONIC", "notes", ["Cis4", "D4"]),
            ("KB-M07-CLAVE", "sixteenth_positions", [[0, 3, 6], [4, 8]]),
        ):
            case = deepcopy(cases[ident])
            case["input"][field] = value
            result, = benchmark.run([case], self.examples, self.claims, {})
            self.assertEqual(result["status"], "FAIL", result["observed"])

        case = deepcopy(cases["KB-M07-SWING-SOURCE"])
        case["expected"]["volume_issue"] = "19(4)"
        result, = benchmark.run([case], self.examples, self.claims, {})
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["observed"]["actual"]["volume_issue"], "19(3)")

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

    def test_assessment_templates_keep_unrated_cases_pending(self):
        for method in ("manual", "coach"):
            case = next(case for case in self.cases if case["method"] == method)
            template = benchmark.assessment_template([case], method, "a" * 40)
            entry = template[case["id"]]
            self.assertEqual(entry["fingerprint"], benchmark.case_fingerprint(case))
            self.assertEqual(entry["criteria"], dict.fromkeys(case["expected"], None))
            args = ({}, template) if method == "manual" else (template, {})
            result, = benchmark.run([case], self.examples, self.claims, *args)
            self.assertEqual(result["status"], "PENDING")

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
