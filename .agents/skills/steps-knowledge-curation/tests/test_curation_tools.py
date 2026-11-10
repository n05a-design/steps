"""Automated test suite for steps-knowledge-curation skill scripts."""
import unittest
import tempfile
import os
from pathlib import Path

# Adjust path to import scripts
SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
import sys
sys.path.insert(0, str(SCRIPTS_DIR))

import check_source
import detect_duplicates
import extract_instructions
import validate_register

class TestCurationTools(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_file = os.path.join(self.test_dir.name, "test_file.txt")
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("Line 1\nTODO: Implement secondary dominant parser\nLine 3\n")

    def tearDown(self):
        self.test_dir.cleanup()

    def test_check_source(self):
        res = check_source.check_file(self.test_file)
        self.assertEqual(res["extension"], ".txt")
        self.assertTrue(len(res["sha256"]) == 64)
        self.assertTrue(res["size_bytes"] > 0)

    def test_detect_duplicates(self):
        # Create an exact duplicate
        dup_file = os.path.join(self.test_dir.name, "dup_file.txt")
        with open(dup_file, "w", encoding="utf-8") as f:
            f.write("Line 1\nTODO: Implement secondary dominant parser\nLine 3\n")
        dups = detect_duplicates.is_duplicate(self.test_file, self.test_dir.name)
        self.assertEqual(len(dups), 1)
        self.assertEqual(os.path.abspath(dups[0]), os.path.abspath(dup_file))

    def test_extract_instructions(self):
        items = extract_instructions.extract_from_file(self.test_file)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["line"], 2)
        self.assertIn("secondary dominant", items[0]["match"])

    def test_validate_register(self):
        canonical_p = os.path.expandvars(r"%LOCALAPPDATA%\StepsKnowledge\OFFENE_ARBEITSAUFFORDERUNGEN.md")
        if os.path.exists(canonical_p):
            res = validate_register.validate_master_file(canonical_p)
            self.assertEqual(res["errors_count"], 0)
            self.assertTrue(res["total_tasks_found"] >= 10)

if __name__ == "__main__":
    unittest.main()
