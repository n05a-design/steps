"""
Unit tests for the automated reference ID integrity checker tool (OA-0031, M01-M12).
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add skill scripts directory to sys.path
SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from check_reference_ids import ReferenceIdChecker, validate_reference_ids


class TestReferenceIdIntegrityTool(unittest.TestCase):
    """Verifies reference ID validation, failure detection, and reporting."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.repo_root = Path(__file__).resolve().parents[4]

    def test_real_repo_integrity(self) -> None:
        if not (self.repo_root / "decisions" / "DECISION_REGISTER.md").is_file():
            self.skipTest("Sparse checkout detected: decisions/ not present in environment")
        report = validate_reference_ids(self.repo_root)
        self.assertTrue(report.success, f"Reference check failed with errors: {report.errors}")
        self.assertEqual(len(report.errors), 0)
        self.assertEqual(report.stats.get("adrs"), 17)
        self.assertEqual(report.stats.get("progressions"), 28)
        self.assertEqual(report.stats.get("drum_patterns"), 31)
        self.assertEqual(report.stats.get("piano_modules"), 19)
        self.assertEqual(report.stats.get("golden_cases"), 198)
        self.assertEqual(report.stats.get("relations"), 97)
        self.assertEqual(report.identities_checked, 390)

    def test_detection_of_missing_adr(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            dec_dir = tmp_root / "decisions"
            dec_dir.mkdir(parents=True)
            # Write DECISION_REGISTER without ADR-001
            (dec_dir / "DECISION_REGISTER.md").write_text("| ADR-002 |\n| ADR-003 |\n", encoding="utf-8")

            checker = ReferenceIdChecker(tmp_root)
            report = checker.run_check()
            self.assertFalse(report.success)
            self.assertTrue(any("Missing expected ADRs" in err for err in report.errors))

    def test_detection_of_invalid_ref_id_format(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            # Create minimal structure
            golden_dir = tmp_root / "knowledge" / "research" / "golden_cases"
            golden_dir.mkdir(parents=True)
            # Write invalid REF id format (REF-1 instead of REF-0001)
            cases = [{"case_id": "REF-1"}]
            (golden_dir / "golden_reference_cases.json").write_text(json.dumps(cases), encoding="utf-8")

            checker = ReferenceIdChecker(tmp_root)
            report = checker.run_check()
            self.assertFalse(report.success)
            self.assertTrue(any("Invalid REF ID format" in err for err in report.errors))

    def test_detection_of_mirror_out_of_sync(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            canon_dir = tmp_root / "knowledge" / "research" / "golden_cases"
            canon_dir.mkdir(parents=True)
            mirror_dir = tmp_root / "tests" / "golden_cases"
            mirror_dir.mkdir(parents=True)

            (canon_dir / "golden_reference_cases.json").write_text(json.dumps([{"case_id": "REF-0001"}]), encoding="utf-8")
            # Mirror has different content
            (mirror_dir / "golden_reference_cases.json").write_text(json.dumps([{"case_id": "REF-0002"}]), encoding="utf-8")

            checker = ReferenceIdChecker(tmp_root)
            report = checker.run_check()
            self.assertFalse(report.success)
            self.assertTrue(any("out of sync" in err for err in report.errors))


if __name__ == "__main__":
    unittest.main()
