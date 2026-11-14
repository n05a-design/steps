"""Automated unit test suite for steps-knowledge-curation skill scripts covering 22 validation scenarios."""
from __future__ import annotations
import unittest
import tempfile
import os
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
        self.assertEqual(Path(dups[0]).resolve(), Path(f2).resolve())

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
        self.assertEqual(items[0]["origin"], "CANDIDATE_FROM_DOCUMENT")

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
        self.assertEqual(items[0]["origin"], "CANDIDATE_FROM_DOCUMENT")

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
        self.assertEqual(items[0]["category"], "DECISION_REQUIRED_DE")
        self.assertEqual(items[0]["origin"], "CANDIDATE_FROM_DOCUMENT")

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
* **Commit:** `0123456789abcdef0123456789abcdef01234567`
* **Prüfung:** `python -m unittest`
* **Abnahmebeleg:** Testprotokoll zur oben genannten Revision
* **Abnahmekriterien:** Die Suite besteht.
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

    def test_18_register_requires_one_status_per_task(self):
        content = """### OA-0001: No status
* **Beschreibung:** The string **Status:** `OPEN` is an example.
### OA-0002: Repeated status
* **Status:** `OPEN`
* **Status:** `IN_PROGRESS`
"""
        result = validate_register.validate_content(content)
        self.assertEqual(result["errors_count"], 2)
        self.assertIn("OA-0001", result["errors"][0])
        self.assertIn("OA-0002", result["errors"][1])

    # Scenario 19: Directory Boundary Check (within vs outside bounds)
    def test_19_directory_boundary_check(self):
        inside = os.path.join(self.dir_path, "inside.txt")
        with open(inside, "w", encoding="utf-8") as fp:
            fp.write("Inside file")
        res_in = check_source.check_file(inside, base_dir=self.dir_path)
        self.assertTrue(res_in["within_bounds"])
        
        # Test file outside bounds
        with tempfile.TemporaryDirectory() as other_dir:
            outside = Path(other_dir) / "outside.txt"
            outside.write_text("Outside file", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "outside the allowed directory"):
                check_source.check_file(outside, base_dir=self.dir_path)

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

    # Scenario 23: Backup and Recovery Lifecycle
    def test_23_backup_and_recovery(self):
        import backup_knowledge
        test_master = os.path.join(self.dir_path, "master_to_backup.md")
        with open(test_master, "w", encoding="utf-8") as fp:
            fp.write("# Backup Test Master\n### OA-0001: Task One\n* **Kategorie:** Test · **Status:** `OPEN`\n")
        b_dir = os.path.join(self.dir_path, "backups")
        
        # Test backup
        res = backup_knowledge.backup_master(test_master, b_dir)
        self.assertEqual(res["status"], "BACKUP_SUCCESS")
        self.assertTrue(os.path.exists(res["backup"]))
        
        # Test listing
        b_list = backup_knowledge.list_backups(b_dir)
        self.assertEqual(len(b_list), 1)
        self.assertEqual(b_list[0]["sha256"], res["sha256"])
        
        previous = "### OA-0001: Task One\n* **Status:** `IN_PROGRESS`\n"
        Path(test_master).write_text(previous, encoding="utf-8")
        self.assertNotEqual(backup_knowledge.compute_sha256(test_master), res["sha256"])
        
        # Test restore
        rest_res = backup_knowledge.restore_master(res["backup"], test_master)
        self.assertEqual(rest_res["status"], "RESTORE_SUCCESS")
        self.assertEqual(backup_knowledge.compute_sha256(test_master), res["sha256"])
        saved = rest_res["previous_backup"]
        self.assertEqual(Path(saved).read_text(encoding="utf-8"), previous)
        backup_knowledge.restore_master(saved, test_master)
        self.assertEqual(Path(test_master).read_text(encoding="utf-8"), previous)

    def test_24_verified_status_needs_evidence_in_its_own_task(self):
        content = """### OA-0001: No evidence
* **Status:** `DONE_VERIFIED`
```md
* **Commit:** `0123456789abcdef0123456789abcdef01234567`
```
### OA-0002: Evidence belongs to this task
* **Status:** `DONE_VERIFIED`
* **Commit:** `0123456789abcdef0123456789abcdef01234567`
* **Prüfung:** `python -m unittest`
* **Abnahmebeleg:** Testprotokoll
* **Abnahmekriterien:** Die Suite besteht.
"""
        result = validate_register.validate_content(content)
        self.assertEqual(result["errors_count"], 4)
        self.assertTrue(all("OA-0001" in error for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()
