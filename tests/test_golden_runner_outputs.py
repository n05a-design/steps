"""Prüft, dass der Golden-Runner versionierte Berichte nur auf ausdrücklichen Wunsch überschreibt."""

import contextlib
import hashlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "knowledge" / "research" / "run_golden_test_suite.py"
BASELINE_FILES = [
    "REAL_GOLDEN_TEST_EXECUTION_REPORT.md",
    "GOLDEN_TEST_EXECUTION_REPORT.md",
    "FINAL_REFERENCE_CASE_VALIDATION.csv",
    "MUSICAL_REFERENCE_VALIDATION.csv",
    "GOLDEN_TEST_CLASSIFICATION_AUDIT.csv",
]


def load_runner():
    spec = importlib.util.spec_from_file_location("run_golden_test_suite", RUNNER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digests():
    base = ROOT / "knowledge" / "research"
    return {name: hashlib.sha256((base / name).read_bytes()).hexdigest() for name in BASELINE_FILES}


class GoldenRunnerOutputTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runner = load_runner()

    def run_quiet(self, **kwargs):
        with contextlib.redirect_stdout(io.StringIO()):
            return self.runner.run_suite(**kwargs)

    def test_default_run_leaves_versioned_reports_untouched(self):
        before = digests()
        self.assertEqual(self.run_quiet(), 0)
        self.assertEqual(digests(), before)

    def test_output_dir_receives_exports_without_touching_baseline(self):
        before = digests()
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(self.run_quiet(output_dir=tmp), 0)
            written = sorted(p.name for p in Path(tmp).iterdir())
        self.assertEqual(written, sorted(BASELINE_FILES))
        self.assertEqual(digests(), before)


if __name__ == "__main__":
    unittest.main()
