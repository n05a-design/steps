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

    def test_piano_exercises_detect_wrong_notated_notes(self):
        document = benchmark.PIANO.read_text(encoding="utf-8")
        for ident, before, after in (
            ("P05", "B3 F4", "Bb3 F4"),
            ("P06", "Eb4 G4 D5", "E4 G4 D5"),
            ("P08", "A3 D4", "A4 D4"),
        ):
            with self.subTest(module=ident):
                case = next(case for case in self.cases if case["id"] == f"KB-{ident}-NOTEN")
                result, = benchmark.run([case], self.examples, self.claims, {})
                self.assertEqual(result["status"], "PASS", result["observed"])
                self.assertIn(before, document)
                with patch.object(type(benchmark.PIANO), "read_text", return_value=document.replace(before, after)):
                    altered, = benchmark.run([case], self.examples, self.claims, {})
                self.assertEqual(altered["status"], "FAIL")

    def test_catalog_coverage_reports_pass_fail_and_pending_independently_of_order(self):
        pending = {"status": "PENDING", "next_step": "Hörprobe."}
        passed = {"status": "PASS", "next_step": ""}
        failed = {"status": "FAIL", "next_step": "Noten prüfen."}
        self.assertEqual(coverage.catalog_evidence([]), ("OFFEN", "", ""))
        for checks, status, detail in (
            ([pending], "PENDING", "1 PENDING."),
            ([pending, passed], "PASS", "1 PASS. 1 PENDING."),
            ([passed, pending, failed], "FAIL", "1 PASS. 1 FAIL. 1 PENDING."),
        ):
            with self.subTest(status=status):
                self.assertEqual(coverage.catalog_evidence(checks)[:2], (status, detail))
                self.assertEqual(coverage.catalog_evidence(checks[::-1])[:2], (status, detail))
        self.assertEqual(coverage.catalog_evidence([passed, pending, failed])[2], "Hörprobe. Noten prüfen.")

    def test_progression_positions_keep_positional_and_whole_progression_checks(self):
        by_case = {
            "KB-PROG-001-02": {"status": "PASS", "next_step": ""},
            "PROG-001-HARMONY": {"status": "FAIL", "next_step": "Akkordfolge prüfen."},
        }
        both = coverage.position_checks(by_case, "PROG-001", 2)
        self.assertEqual(both, [by_case["KB-PROG-001-02"], by_case["PROG-001-HARMONY"]])
        self.assertEqual(coverage.catalog_evidence(both), ("FAIL", "1 PASS. 1 FAIL.", "Akkordfolge prüfen."))
        self.assertEqual(coverage.position_checks(by_case, "PROG-001", 3), [by_case["PROG-001-HARMONY"]])
        self.assertEqual(coverage.catalog_evidence(coverage.position_checks(by_case, "PROG-002", 1))[0], "OFFEN")

    def test_pat031_checks_notated_boundaries_and_keeps_hearing_pending(self):
        cases = [case for case in self.cases if case["content"] == "PAT-031"]
        results = benchmark.run(cases, self.examples, self.claims, {})
        self.assertEqual({r["id"]: r["status"] for r in results}, {
            "KB-PAT-031-RASTER": "PASS", "KB-M08-METER": "PENDING",
        })
        document = benchmark.DRUMS.read_text(encoding="utf-8")
        for before, after in (
            ("0, 1440 und 2880", "0, 1200 und 2880"),
            ("punktierte Viertel = 120 BPM", "Viertel = 120 BPM"),
            ("1200, 1680, 2160", "1200, 1440, 2160"),
        ):
            with self.subTest(changed=before):
                self.assertIn(before, document)
                with patch.object(type(benchmark.DRUMS), "read_text", return_value=document.replace(before, after)):
                    results = benchmark.run(cases, self.examples, self.claims, {})
                self.assertEqual(coverage.catalog_evidence(results)[0], "FAIL")

    def test_p18_detects_changed_resolution_in_written_voicing(self):
        case = next(case for case in self.cases if case["id"] == "KB-P18-VOICINGS")
        result, = benchmark.run([case], self.examples, self.claims, {})
        self.assertEqual(result["status"], "PASS", result["observed"])
        document = benchmark.PIANO.read_text(encoding="utf-8")
        self.assertIn("G3 B3 E4", document)
        mutated = document.replace("G3 B3 E4", "G3 B3 Eb4")
        with patch.object(type(benchmark.PIANO), "read_text", return_value=mutated):
            result, = benchmark.run([case], self.examples, self.claims, {})
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["observed"]["resolution"], [-1, -1, 1])

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

    def test_format_node_evidence_requires_unique_id_and_source_locator(self):
        entry = {
            "node_id": "MUSICXML_PITCH",
            "definition": "Geschriebene Tonhöhe",
            "source_url": "https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/pitch/",
            "locator": "Content",
        }
        self.assertEqual(
            coverage.format_node_evidence([entry]),
            {entry["node_id"]: f"{entry['source_url']} (Content)"},
        )
        for rows in ([entry, entry], [{**entry, "locator": ""}], [{**entry, "source_url": "http://example.com"}]):
            with self.subTest(rows=rows), self.assertRaisesRegex(ValueError, entry["node_id"]):
                coverage.format_node_evidence(rows)

    def test_graph_samples_detect_changed_edges_and_musical_inputs(self):
        graph_cases = [c for c in self.cases if c["method"] == "graph_sample"]
        self.assertEqual(len(graph_cases), 4)
        for case in graph_cases:
            with self.subTest(case=case["id"]):
                result, = benchmark.run([case], self.examples, self.claims, {})
                self.assertEqual(result["status"], "PASS", result["observed"])
                changed = deepcopy(case)
                changed["input"]["edge"][1] = "UNRELATED_NODE"
                result, = benchmark.run([changed], self.examples, self.claims, {})
                self.assertEqual(result["status"], "FAIL")
        mode = deepcopy(graph_cases[0])
        mode["input"]["degree"] = 6
        result, = benchmark.run([mode], self.examples, self.claims, {})
        self.assertEqual(result["status"], "FAIL")
        drop = deepcopy(next(c for c in graph_cases if c["input"]["check"] == "drop2"))
        drop["input"]["close"][2] += 12
        result, = benchmark.run([drop], self.examples, self.claims, {})
        self.assertEqual(result["status"], "FAIL")

    def test_graph_counterexample_keeps_the_underlying_claim_red(self):
        checks = [{"status": "PASS", "next_step": "Graphzuordnung klären."}]
        self.assertEqual(coverage.graph_evidence(checks, {"assessment": "COUNTEREXAMPLE"})[0], "FAIL")
        self.assertEqual(coverage.graph_evidence(checks, {"assessment": "SOURCE_SUPPORTED_SAMPLE"})[0], "PASS")

    def test_relation_evidence_rejects_unknown_duplicate_and_unbounded_records(self):
        row = {"relation_id": "CDR-005", "source_url": "https://example.com/source", "locator": "Page 1",
               "claim_id": "CLAIM-022", "assessment": "SOURCE_SUPPORTED_SAMPLE", "scope": "One rotation",
               "limitation": "No human approval"}
        coverage.relation_evidence([row], {"CDR-005"}, {"CLAIM-022"})
        for records in ([row, row], [{**row, "relation_id": "UNKNOWN"}], [{**row, "limitation": ""}],
                        [{**row, "claim_id": "MISSING"}], [{**row, "assessment": "APPROVED"}]):
            with self.subTest(records=records), self.assertRaises(ValueError):
                coverage.relation_evidence(records, {"CDR-005"}, {"CLAIM-022"})
