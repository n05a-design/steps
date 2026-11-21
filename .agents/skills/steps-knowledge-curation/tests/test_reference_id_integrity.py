"""Reference gate tests using real data and isolated one-defect mutations."""

import csv
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SKILL = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL / "scripts"
ROOT = SKILL.parents[2]
sys.path.insert(0, str(SCRIPTS))

from check_reference_ids import validate_reference_ids


BASELINE = Path("knowledge/research/REFERENCE_IDENTITY_BASELINE.json")
MIRROR = Path("tests/golden_cases/golden_reference_cases.json")
GOLDEN = Path("knowledge/research/golden_cases/golden_reference_cases.json")
PROGRESSIONS = Path("knowledge/concepts/progressions/CHORD_PROGRESSION_REFERENCE_LIBRARY.md")
GRAPH = Path("knowledge/relations/GRAPH_AUDIT_MATRIX_v3.csv")
REVIEW = Path("knowledge/relations/GRAPH_HUMAN_REVIEW_v3.csv")
ADR = Path("decisions/DECISION_REGISTER.md")
FINGERPRINTS = Path("knowledge/research/CURATION_EVIDENCE_FINGERPRINTS.json")
CHECK_INPUTS = (
    FINGERPRINTS,
    BASELINE, MIRROR, GOLDEN, PROGRESSIONS, GRAPH, REVIEW, ADR,
    Path("knowledge/concepts/styles/DRUM_GROOVE_REFERENCE_LIBRARY.md"),
    Path("knowledge/concepts/chords/PIANO_PRACTICE_REFERENCE_LIBRARY.md"),
    Path("knowledge/relations/MUSIC_CONCEPT_RELATIONS.csv"),
    Path("knowledge/research/MUSIC_DOMAIN_READINESS_MATRIX.csv"),
    Path("knowledge/research/HISTORICAL_REFERENCE_ID_MATRIX.csv"),
    Path("knowledge/research/REFERENCE_ID_MIGRATION_REGISTER.csv"),
)


class TestReferenceIdIntegrityTool(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.fixture = Path(folder.name)
        for path in CHECK_INPUTS:
            target = self.fixture / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, target)

    def assert_rejected(self, message):
        report = validate_reference_ids(self.fixture)
        self.assertFalse(report.success)
        self.assertTrue(any(message in error for error in report.errors), report.errors)

    def test_real_repo_integrity(self):
        report = validate_reference_ids(ROOT)
        self.assertTrue(report.success, report.errors)
        self.assertEqual(report.identities_checked, 390)
        self.assertFalse(report.warnings)

    def test_detection_of_missing_adr(self):
        path = self.fixture / ADR
        original = path.read_text(encoding="utf-8")
        path.write_text("\n".join(line for line in original.splitlines() if not line.startswith("| ADR-001 |")), encoding="utf-8")
        self.assert_rejected("Missing canonical ADR 'ADR-001'")

    def test_detection_of_invalid_ref_id_format(self):
        self._write_golden_pair([{"case_id": "REF-1"}])
        self.assert_rejected("Invalid REF ID format")

    def test_detection_of_mirror_out_of_sync(self):
        (self.fixture / MIRROR).write_text("[]", encoding="utf-8")
        self.assert_rejected("Golden cases desynchronization")

    def test_missing_mirror_is_fatal(self):
        (self.fixture / MIRROR).unlink()
        self.assert_rejected("test mirror missing")

    def test_missing_and_empty_baselines_are_fatal(self):
        baseline = self.fixture / BASELINE
        baseline.unlink()
        self.assert_rejected("Identity baseline missing")
        baseline.write_text("{}", encoding="utf-8")
        self.assert_rejected("Invalid identity baseline summary")

    def test_deleting_identity_from_baseline_is_fatal(self):
        baseline = self.fixture / BASELINE
        content = json.loads(baseline.read_text(encoding="utf-8"))
        del content["progressions"]["PROG-001"]
        content["summary"]["progressions"] -= 1
        baseline.write_text(json.dumps(content), encoding="utf-8")
        self.assert_rejected("Invalid identity baseline section 'progressions'")

    def _write_golden_pair(self, content):
        for path in (GOLDEN, MIRROR):
            (self.fixture / path).write_text(json.dumps(content), encoding="utf-8")

    def test_wrong_pitch_fails_even_when_both_copies_match(self):
        content = json.loads((self.fixture / GOLDEN).read_text(encoding="utf-8"))
        self.assertEqual(content[0]["expected_output"], 0)
        content[0]["expected_output"] = 7
        self._write_golden_pair(content)
        self.assert_rejected("Expected output changed from 0 to 7")

    def test_invalid_golden_shape_is_reported(self):
        self._write_golden_pair({"case_id": "REF-0001"})
        self.assert_rejected("Root must be a JSON array")

    def test_duplicate_progression_is_fatal(self):
        path = self.fixture / PROGRESSIONS
        content = path.read_text(encoding="utf-8")
        row = next(line for line in content.splitlines() if line.startswith("| `PROG-001`"))
        path.write_text(content + "\n" + row + "\n", encoding="utf-8")
        self.assert_rejected("Duplicate definition of ID 'PROG-001'")

    def test_audit_matrix_must_match_reviewed_endpoints(self):
        self._change_graph_field(GRAPH, "target_id", "PROG-999")
        self.assert_rejected("differs from the recorded v3 review")

    def test_missing_v3_review_is_fatal(self):
        (self.fixture / REVIEW).unlink()
        self.assert_rejected("GRAPH_HUMAN_REVIEW_v3.csv")

    def test_matching_review_and_matrix_must_bind_to_the_original_edge(self):
        for path in (GRAPH, REVIEW):
            self._change_graph_field(path, "original_row_sha256", "0" * 64)
        self.assert_rejected("does not match the original relation hash")

    def test_matching_graph_copies_cannot_introduce_unknown_catalog_endpoint(self):
        self._change_graph_field(GRAPH, "target_id", "PROG-999")
        self._change_graph_field(REVIEW, "target_id", "PROG-999")
        self.assert_rejected("dangling PROG reference")

    def _change_graph_field(self, path, field, value):
        path = self.fixture / path
        with path.open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))
        rows[0][field] = value
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)

    def test_musical_catalog_content_changes_are_detected(self):
        for path, before, after, ident in (
            (Path("knowledge/concepts/styles/DRUM_GROOVE_REFERENCE_LIBRARY.md"), "1 und 3 (Synkope auf 3e+)", "nur Zählzeit 4", "PAT-001"),
            (PROGRESSIONS, "Pop, Rock, Singer-Songwriter", "ausschließlich Barock", "PROG-001"),
        ):
            with self.subTest(ident=ident):
                target = self.fixture / path
                original = target.read_text(encoding="utf-8")
                self.assertIn(before, original)
                target.write_text(original.replace(before, after, 1), encoding="utf-8")
                self.assert_rejected(f"{path.as_posix()} [{ident}]")
                target.write_text(original, encoding="utf-8")

    def test_golden_classification_and_source_are_protected(self):
        for field, value in (("test_class", "SPECIFICATION_EXAMPLE"), ("source_citation", "")):
            with self.subTest(field=field):
                content = json.loads((ROOT / GOLDEN).read_text(encoding="utf-8"))
                content[0][field] = value
                self._write_golden_pair(content)
                self.assert_rejected(f"{GOLDEN.as_posix()} [REF-0001]")

    def test_graph_scope_and_source_locator_are_protected(self):
        for path, field, value in ((GRAPH, "source_locator", ""), (REVIEW, "scope", "All styles")):
            with self.subTest(field=field):
                self._change_graph_field(path, field, value)
                self.assert_rejected(f"{path.as_posix()} [CR-001]")
                shutil.copyfile(ROOT / path, self.fixture / path)

    def test_duplicate_domain_is_rejected(self):
        path = self.fixture / "knowledge/research/MUSIC_DOMAIN_READINESS_MATRIX.csv"
        content = path.read_text(encoding="utf-8")
        path.write_text(content + content.splitlines()[1] + "\n", encoding="utf-8")
        self.assert_rejected("Duplicate ID 'M01'")

    def test_empty_historical_inventory_is_rejected(self):
        path = self.fixture / "knowledge/research/HISTORICAL_REFERENCE_ID_MATRIX.csv"
        path.write_text(path.read_text(encoding="utf-8").splitlines()[0] + "\n", encoding="utf-8")
        self.assert_rejected("HISTORICAL_REFERENCE_ID_MATRIX.csv [REF-0001]")

    def test_missing_evidence_manifest_is_rejected(self):
        (self.fixture / FINGERPRINTS).unlink()
        self.assert_rejected(FINGERPRINTS.name)

    def test_missing_baseline_field_returns_structured_failure(self):
        baseline = self.fixture / BASELINE
        content = json.loads(baseline.read_text(encoding="utf-8"))
        del content["progressions"]["PROG-001"]["harmonic_structure"]
        baseline.write_text(json.dumps(content), encoding="utf-8")
        result = subprocess.run(
            [sys.executable, "-B", str(SCRIPTS / "check_reference_ids.py"),
             "--repo-root", str(self.fixture), "--json"], capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("Invalid identity baseline record: PROG-001", json.loads(result.stdout)["errors"])

    def test_cli_reports_missing_baseline_as_failure(self):
        (self.fixture / BASELINE).unlink()
        result = subprocess.run(
            [sys.executable, "-B", str(SCRIPTS / "check_reference_ids.py"), "--repo-root", str(self.fixture)],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("Identity baseline missing", result.stdout)
        self.assertNotIn("100%", result.stdout)
