"""End-to-end integration test for steps-knowledge-curation skill pipeline.

Tests full execution lifecycle against an isolated temporary directory:
1. Intake new document -> check_source.py (metadata & SHA-256)
2. Duplicate detection -> detect_duplicates.py
3. Semantic claim & instruction extraction -> extract_instructions.py
4. Master register updating (isolated test register)
5. Validation of updated register -> validate_register.py
"""
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

class TestE2ECurationPipeline(unittest.TestCase):
    def setUp(self):
        self.test_env = tempfile.TemporaryDirectory()
        self.env_dir = self.test_env.name
        self.docs_dir = os.path.join(self.env_dir, "docs")
        self.registers_dir = os.path.join(self.env_dir, "registers")
        os.makedirs(self.docs_dir, exist_ok=True)
        os.makedirs(self.registers_dir, exist_ok=True)
        
        # Seed baseline isolated master file
        self.master_file = os.path.join(self.registers_dir, "OFFENE_ARBEITSAUFFORDERUNGEN.md")
        with open(self.master_file, "w", encoding="utf-8") as f:
            f.write("""# Test Master Tasks
### OA-0001: Initial Setup
* **Kategorie:** Test · **Status:** `DONE_UNVERIFIED`
""")

    def tearDown(self):
        self.test_env.cleanup()

    def test_e2e_pipeline_lifecycle(self):
        # Step 1: Create a new incoming research file with instructions
        sample_doc = os.path.join(self.docs_dir, "harmonic_geometry_research.md")
        with open(sample_doc, "w", encoding="utf-8") as f:
            f.write("""# Harmonic Geometry Research
Tymoczko voice-leading distance must be implemented for chromatic mediants.
TODO: Add chord distance tests for C to E major.
Eine Entscheidung ist noch zu treffen regarding microtonal support.
""")
        
        # Step 2: Source intake check
        check_res = check_source.check_file(sample_doc, self.docs_dir)
        self.assertEqual(check_res["extension"], ".md")
        self.assertEqual(len(check_res["sha256"]), 64)
        self.assertGreater(check_res["size_bytes"], 0)

        # Step 3: Duplicate detection check (verify not duplicate initially)
        dups = detect_duplicates.is_duplicate(sample_doc, self.docs_dir)
        self.assertEqual(len(dups), 0)

        # Step 4: Instruction & Claim extraction
        extracted = extract_instructions.extract_from_file(sample_doc, self.docs_dir)
        self.assertEqual(len(extracted), 3)
        self.assertEqual({item["origin"] for item in extracted}, {"CANDIDATE_FROM_DOCUMENT"})
        categories = {item["category"] for item in extracted}
        self.assertIn("NORMATIVE_MUST_EN", categories)
        self.assertIn("EXPLICIT_TODO", categories)
        self.assertIn("DECISION_REQUIRED_DE", categories)

        # Step 5: Append new extracted task to isolated master file
        with open(self.master_file, "a", encoding="utf-8") as f:
            f.write("""
### OA-0002: Implement Tymoczko Voice-Leading Distance
* **Kategorie:** Musiktheorie / Algorithmen · **Status:** `OPEN` · **Ursprung:** INFERRED
* **Beschreibung:** Tymoczko voice-leading distance must be implemented for chromatic mediants.
* **Quellen:** harmonic_geometry_research.md:2
""")

        # Step 6: Validate updated master file
        val_res = validate_register.validate_master_file(self.master_file)
        self.assertEqual(val_res["total_tasks_found"], 2)
        self.assertEqual(val_res["unique_ids"], 2)
        self.assertEqual(val_res["errors_count"], 0)

if __name__ == "__main__":
    unittest.main()
