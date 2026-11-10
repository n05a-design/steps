"""Automated unit test suite for steps-knowledge-curation skill scripts covering 22 validation scenarios."""
from __future__ import annotations
import unittest
import tempfile
import os
import shutil
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
import sys
sys.path.insert(0, str(SCRIPTS_DIR))

import check_source
import detect_duplicates
import extract_instructions
import validate_register

class TestCurationToolsScenarios(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.dir_path = self.test_dir.name

    def tearDown(self):
        self.test_dir.cleanup()

    # Scenario 1: New Source Intake (valid hashing & metadata)
    def test_01_new_source_intake(self):
        f = os.path.join(self.dir_path, "new_source.md")
        with open(f, "w", encoding="utf-8") as fp:
            fp.write("# New Music Theory Document\nContent")
        res = check_source.check_file(f)
        self.assertEqual(res["extension"], ".md")
        self.assertEqual(len(res["sha256"]), 64)
        self.assertTrue(res["size_bytes"] > 0)
        self.assertTrue(res["within_bounds"])

    # Scenario 2: Modified Source Detection (hash changes)
    def test_02_modified_source_detection(self):
        f = os.path.join(self.dir_path, "doc.txt")
        with open(f, "w", encoding="utf-8") as fp:
            fp.write("Version 1")
        hash1 = check_source.check_file(f)["sha256"]
        with open(f, "w", encoding="utf-8") as fp:
            fp.write("Version 2 (Modified)")
        hash2 = check_source.check_file(f)["sha256"]
        self.assertNotEqual(hash1, hash2)

    # Scenario 3: Exact Duplicate Identification (detect_duplicates)
    def test_03_exact_duplicate_identification(self):
        f1 = os.path.join(self.dir_path, "orig.txt")
        f2 = os.path.join(self.dir_path, "copy.txt")
        content = "Exact duplicate bytes"
        with open(f1, "w", encoding="utf-8") as fp:
            fp.write(content)
        with open(f2, "w", encoding="utf-8") as fp:
            fp.write(content)
        dups = detect_duplicates.is_duplicate(f1, self.dir_path)
        self.assertEqual(len(dups), 1)
        self.assertEqual(os.path.normpath(dups[0]), os.path.normpath(f2))

    # Scenario 4: Non-Duplicate Source (distinct content)
    def test_04_non_duplicate_source(self):
        f1 = os.path.join(self.dir_path, "file1.txt")
        f2 = os.path.join(self.dir_path, "file2.txt")
        with open(f1, "w", encoding="utf-8") as fp:
            fp.write("Content A")
        with open(f2, "w", encoding="utf-8") as fp:
            fp.write("Content B")
        dups = detect_duplicates.is_duplicate(f1, self.dir_path)
        self.assertEqual(len(dups), 0)

    # Scenario 5: File Rename Tracking (same hash, different path)
    def test_05_file_rename_tracking(self):
        f1 = os.path.join(self.dir_path, "old_name.txt")
        f2 = os.path.join(self.dir_path, "new_name.txt")
        with open(f1, "w", encoding="utf-8") as fp:
            fp.write("Persistent music content")
        h1 = check_source.check_file(f1)["sha256"]
        os.rename(f1, f2)
        h2 = check_source.check_file(f2)["sha256"]
        self.assertEqual(h1, h2)

    # Scenario 6: Deleted Source Verification
    def test_06_deleted_source_verification(self):
        f = os.path.join(self.dir_path, "to_delete.txt")
        with open(f, "w", encoding="utf-8") as fp:
            fp.write("temporary")
        os.remove(f)
        with self.assertRaises(FileNotFoundError):
            check_source.check_file(f)

    # Scenario 7: Explicit TODO Marker Extraction
    def test_07_explicit_todo_extraction(self):
        f = os.path.join(self.dir_path, "todo.txt")
        with open(f, "w", encoding="utf-8") as fp:
            fp.write("TODO: Build Roman numeral tokenizer\n")
        items = extract_instructions.extract_from_file(f)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["category"], "EXPLICIT_TODO")
        self.assertEqual(items[0]["origin"], "EXPLICIT")

    # Scenario 8: Explicit FIXME Marker Extraction
    def test_08_explicit_fixme_extraction(self):
        f = os.path.join(self.dir_path, "fixme.txt")
        with open(f, "w", encoding="utf-8") as fp:
            fp.write("FIXME: Repair enharmonic spelling for D# vs Eb\n")
        items = extract_instructions.extract_from_file(f)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["category"], "EXPLICIT_FIXME")

    # Scenario 9: Inferred German Normative Instruction (muss ... werden)
    def test_09_inferred_german_must(self):
        f = os.path.join(self.dir_path, "norm_de.txt")
        with open(f, "w", encoding="utf-8") as fp:
            fp.write("Die Stimmführung muss noch implementiert werden.\n")
        items = extract_instructions.extract_from_file(f)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["category"], "NORMATIVE_MUST_DE")
        self.assertEqual(items[0]["origin"], "INFERRED")

    # Scenario 10: Inferred English Normative Instruction (must be implemented)
    def test_10_inferred_english_must(self):
        f = os.path.join(self.dir_path, "norm_en.txt")
        with open(f, "w", encoding="utf-8") as fp:
            fp.write("Voice leading distance must be verified by automated tests.\n")
        items = extract_instructions.extract_from_file(f)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["category"], "NORMATIVE_MUST_EN")

    # Scenario 11: Inferred German Open Status (bleibt offen)
    def test_11_inferred_german_open_status(self):
        f = os.path.join(self.dir_path, "open_de.txt")
        with open(f, "w", encoding="utf-8") as fp:
            fp.write("Die Frage nach VST3-Hosting bleibt vorerst offen.\n")
        items = extract_instructions.extract_from_file(f)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["category"], "OPEN_STATUS_DE")

    # Scenario 12: Owner Decision Required Flag (Entscheidung ist noch zu treffen)
    def test_12_owner_decision_required_extraction(self):
        f = os.path.join(self.dir_path, "decision.txt")
        with open(f, "w", encoding="utf-8") as fp:
            fp.write("Eine Owner-Entscheidung ist erforderlich für ADR-002.\n")
        items = extract_instructions.extract_from_file(f)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["origin"], "OWNER_DECISION_REQUIRED")

    # Scenario 13: Deferred / Postponed Feature Extraction
    def test_13_deferred_feature_extraction(self):
        f = os.path.join(self.dir_path, "deferred.txt")
        with open(f, "w", encoding="utf-8") as fp:
            fp.write("Drums und Groove-Pattern wurden vertagt auf Version 0.2.\n")
        items = extract_instructions.extract_from_file(f)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["category"], "GAP_DEFERRED")

    # Scenario 14: Valid Master Register File Passes Validation
    def test_14_valid_master_register(self):
        m = os.path.join(self.dir_path, "master.md")
        with open(m, "w", encoding="utf-8") as fp:
            fp.write("""
### OA-0001: Task One
* **Kategorie:** Test · **Status:** `OPEN`
### OA-0002: Task Two
* **Kategorie:** Test · **Status:** `DONE_VERIFIED`
""")
        res = validate_register.validate_master_file(m)
        self.assertEqual(res["total_tasks_found"], 2)
        self.assertEqual(res["errors_count"], 0)

    # Scenario 15: Duplicate Task ID in Master File Is Detected as Error
    def test_15_duplicate_task_id_detected(self):
        m = os.path.join(self.dir_path, "dup_master.md")
        with open(m, "w", encoding="utf-8") as fp:
            fp.write("""
### OA-0001: Task One
* **Kategorie:** Test · **Status:** `OPEN`
### OA-0001: Task One Again
* **Kategorie:** Test · **Status:** `OPEN`
""")
        res = validate_register.validate_master_file(m)
        self.assertEqual(res["errors_count"], 1)
        self.assertIn("Duplicate OA-ID found: OA-0001", res["errors"][0])

    # Scenario 16: Invalid Status Value in Master File Is Caught
    def test_16_invalid_status_caught(self):
        m = os.path.join(self.dir_path, "invalid_status.md")
        with open(m, "w", encoding="utf-8") as fp:
            fp.write("""
### OA-0001: Task One
* **Kategorie:** Test · **Status:** `UNKNOWN_BOGUS_STATUS`
""")
        res = validate_register.validate_master_file(m)
        self.assertEqual(res["errors_count"], 1)
        self.assertIn("Invalid status value: UNKNOWN_BOGUS_STATUS", res["errors"][0])

    # Scenario 17: Empty / Unreadable File Handling
    def test_17_empty_file_handling(self):
        empty = os.path.join(self.dir_path, "empty.txt")
        with open(empty, "w", encoding="utf-8") as fp:
            pass
        res = check_source.check_file(empty)
        self.assertEqual(res["size_bytes"], 0)
        items = extract_instructions.extract_from_file(empty)
        self.assertEqual(len(items), 0)

    # Scenario 18: Canonical Production Master File Validation
    def test_18_canonical_master_production_file(self):
        canonical_p = os.path.expandvars(r"%LOCALAPPDATA%\StepsKnowledge\OFFENE_ARBEITSAUFFORDERUNGEN.md")
        if os.path.exists(canonical_p):
            res = validate_register.validate_master_file(canonical_p)
            self.assertEqual(res["errors_count"], 0)
            self.assertGreaterEqual(res["total_tasks_found"], 19)

    # Scenario 19: Directory Boundary Check (within vs outside bounds)
    def test_19_directory_boundary_check(self):
        inside = os.path.join(self.dir_path, "inside.txt")
        with open(inside, "w", encoding="utf-8") as fp:
            fp.write("Inside file")
        res_in = check_source.check_file(inside, base_dir=self.dir_path)
        self.assertTrue(res_in["within_bounds"])
        
        # Test file outside bounds
        other_dir = tempfile.TemporaryDirectory()
        outside = os.path.join(other_dir.name, "outside.txt")
        with open(outside, "w", encoding="utf-8") as fp:
            fp.write("Outside file")
        res_out = check_source.check_file(outside, base_dir=self.dir_path)
        self.assertFalse(res_out["within_bounds"])
        other_dir.cleanup()

    # Scenario 20: Non-File / Directory Rejection
    def test_20_non_file_rejection(self):
        sub = os.path.join(self.dir_path, "subdir")
        os.makedirs(sub, exist_ok=True)
        with self.assertRaises(ValueError):
            check_source.check_file(sub)

    # Scenario 21: Non-Directory Search Path Rejection
    def test_21_non_dir_search_rejection(self):
        f = os.path.join(self.dir_path, "file.txt")
        with open(f, "w", encoding="utf-8") as fp:
            fp.write("content")
        with self.assertRaises(NotADirectoryError):
            detect_duplicates.is_duplicate(f, f)

    # Scenario 22: Binary File Hashing & Extraction Resilience
    def test_22_binary_file_resilience(self):
        bin_f = os.path.join(self.dir_path, "data.bin")
        with open(bin_f, "wb") as fp:
            fp.write(b"\x00\xff\xfe\x00\x01\x02\x03\x7f")
        res = check_source.check_file(bin_f)
        self.assertEqual(res["size_bytes"], 8)
        self.assertEqual(len(res["sha256"]), 64)
        items = extract_instructions.extract_from_file(bin_f)
        self.assertEqual(len(items), 0)

if __name__ == "__main__":
    unittest.main()
