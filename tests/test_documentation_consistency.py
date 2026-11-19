"""Tests for immutable documentation snapshot and version consistency."""

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TestDocumentationConsistency(unittest.TestCase):
    def test_release_consistency_check_passes_without_creating_artifacts(self):
        result = subprocess.run(
            [sys.executable, "-B", "scripts/check_release_consistency.py", "--check"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("RELEASE CONSISTENCY PASS", result.stdout)

    def test_checker_accepts_current_checkout_and_version_axes(self):
        result = subprocess.run(
            [
                sys.executable,
                "-B",
                "scripts/check_documentation_consistency.py",
                "--check",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("DOCUMENTATION CONSISTENCY PASS", result.stdout)

    def test_status_policy_documents_snapshot_not_head_semantics(self):
        policy = (
            ROOT / "docs/governance/DOCUMENTATION_STATUS_POLICY.md"
        ).read_text(encoding="utf-8")
        self.assertIn("immutable evidence snapshot", policy)
        self.assertIn("not an assertion that every later merge", policy)
        self.assertIn("does not require a historical snapshot", policy)
