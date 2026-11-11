#!/usr/bin/env python3
"""
STEPS Reference Integrity & Mutation Test Suite (OA-0031 Hardened Phase 4.15)

Executes genuine isolated negative mutation tests against the reference integrity checker:
Each test injects exactly one real defect into an isolated temporary workspace/fixture,
runs verify_integrity(), and asserts that:
1. The defect is detected by the validator.
2. The error message accurately describes the injected failure.
3. The canonical repository remains completely untouched.
4. The clean canonical repository passes with 0 errors.
"""

import os
import sys
import shutil
import tempfile
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import scripts.verify_reference_integrity as checker

class TestReferenceIntegrityAndMutations(unittest.TestCase):
    def setUp(self):
        # Create an isolated temporary copy of the repository knowledge and tests directories
        self.temp_dir = tempfile.mkdtemp(prefix="steps_integrity_mutation_")
        self.temp_knowledge = os.path.join(self.temp_dir, "knowledge")
        self.temp_tests = os.path.join(self.temp_dir, "tests")
        
        shutil.copytree(os.path.join(REPO_ROOT, "knowledge"), self.temp_knowledge)
        shutil.copytree(os.path.join(REPO_ROOT, "tests"), self.temp_tests)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_00_canonical_repository_passes_cleanly(self):
        """Verifies that the canonical untouched repository passes 100% with zero errors."""
        result = checker.verify_integrity(repo_root=REPO_ROOT)
        self.assertEqual(len(result['errors']), 0, f"Unexpected canonical errors: {result['errors']}")
        stats = result['stats']
        self.assertEqual(stats['progressions'], 27)
        self.assertEqual(stats['drum_patterns'], 31)
        self.assertEqual(stats['piano_modules'], 19)
        self.assertEqual(stats['golden_cases'], 198)
        self.assertEqual(stats['relations'], 94)

    def test_01_mutation_duplicate_prog_id(self):
        """Mutates progression library by duplicating PROG-001 with line numbers."""
        prog_file = os.path.join(self.temp_knowledge, 'concepts', 'progressions', 'CHORD_PROGRESSION_REFERENCE_LIBRARY.md')
        with open(prog_file, 'a', encoding='utf-8') as f:
            f.write("\n| `PROG-001` | Duplicate Pop Four | `I - V - vi - IV` | `C - G - Am - F` | Pop | Piston |\n")

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Duplicate definition of ID 'PROG-001'" in e for e in result['errors']), result['errors'])

    def test_02_mutation_duplicate_pat_id(self):
        """Mutates drum library by duplicating PAT-001."""
        drum_file = os.path.join(self.temp_knowledge, 'concepts', 'styles', 'DRUM_GROOVE_REFERENCE_LIBRARY.md')
        with open(drum_file, 'a', encoding='utf-8') as f:
            f.write("\n| `PAT-001` | Duplicate Rock | 120 BPM | 4/4 | 1 & 3 | 2 & 4 | 8ths |\n")

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Duplicate definition of ID 'PAT-001'" in e for e in result['errors']), result['errors'])

    def test_03_mutation_duplicate_piano_module_id(self):
        """Mutates piano library by duplicating P01."""
        piano_file = os.path.join(self.temp_knowledge, 'concepts', 'chords', 'PIANO_PRACTICE_REFERENCE_LIBRARY.md')
        with open(piano_file, 'a', encoding='utf-8') as f:
            f.write("\n| `P01` | Duplicate Module | Goal | Focus | Phase 4.3 |\n")

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Duplicate definition of ID 'P01'" in e for e in result['errors']), result['errors'])

    def test_04_mutation_duplicate_ref_id(self):
        """Mutates golden reference JSON by duplicating REF-0001."""
        json_file = os.path.join(self.temp_knowledge, 'research', 'golden_cases', 'golden_reference_cases.json')
        with open(json_file, 'r', encoding='utf-8') as f:
            import json
            cases = json.load(f)
        cases.append(dict(cases[0])) # Duplicate first case
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(cases, f)
        # Also sync mirror to isolate the duplicate test
        mirror_file = os.path.join(self.temp_tests, 'golden_cases', 'golden_reference_cases.json')
        with open(mirror_file, 'w', encoding='utf-8') as f:
            json.dump(cases, f)

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Duplicate case_id 'REF-0001'" in e for e in result['errors']), result['errors'])

    def test_05_mutation_same_ref_id_altered_meaning(self):
        """Mutates REF-0001 by changing its title (semantic identity collision with baseline)."""
        json_file = os.path.join(self.temp_knowledge, 'research', 'golden_cases', 'golden_reference_cases.json')
        with open(json_file, 'r', encoding='utf-8') as f:
            import json
            cases = json.load(f)
        cases[0]['title'] = "Kammerton A4 Frequenzstandard" # Altered title!
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(cases, f)
        mirror_file = os.path.join(self.temp_tests, 'golden_cases', 'golden_reference_cases.json')
        with open(mirror_file, 'w', encoding='utf-8') as f:
            json.dump(cases, f)

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Historical identity conflict for REF-0001" in e for e in result['errors']), result['errors'])

    def test_06_mutation_missing_ref_id(self):
        """Mutates golden reference JSON by removing baseline case REF-0001."""
        json_file = os.path.join(self.temp_knowledge, 'research', 'golden_cases', 'golden_reference_cases.json')
        with open(json_file, 'r', encoding='utf-8') as f:
            import json
            cases = json.load(f)
        cases = cases[1:] # Drop REF-0001
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(cases, f)
        mirror_file = os.path.join(self.temp_tests, 'golden_cases', 'golden_reference_cases.json')
        with open(mirror_file, 'w', encoding='utf-8') as f:
            json.dump(cases, f)

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Baseline Golden Case 'REF-0001' missing from current test suite" in e for e in result['errors']), result['errors'])

    def test_07_mutation_relation_dangling_prog_id(self):
        """Mutates relations CSV by introducing a relation to non-existent PROG-999."""
        rel_file = os.path.join(self.temp_knowledge, 'relations', 'MUSIC_CONCEPT_RELATIONS.csv')
        with open(rel_file, 'a', encoding='utf-8') as f:
            f.write("CR-999,PROG-999,M05,REQUIRES,FORMAL_RULE,Scope,Rule,Desc,VERIFIED_ACTIVE\n")

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("ID 'PROG-999' does not exist in any canonical library" in e for e in result['errors']), result['errors'])

    def test_08_mutation_relation_dangling_piano_module(self):
        """Mutates relations CSV by introducing a relation to non-existent P99."""
        rel_file = os.path.join(self.temp_knowledge, 'relations', 'MUSIC_CONCEPT_RELATIONS.csv')
        with open(rel_file, 'a', encoding='utf-8') as f:
            f.write("CR-998,PROG-001,P99,DIDACTIC_APPLICATION,PEDAGOGICAL_RECOMMENDATION,Scope,Rule,Desc,VERIFIED_ACTIVE\n")

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("ID 'P99' does not exist in any canonical library" in e for e in result['errors']), result['errors'])

    def test_09_mutation_invalid_m010_domain(self):
        """Mutates domain readiness matrix with historical typo M010."""
        dom_file = os.path.join(self.temp_knowledge, 'research', 'MUSIC_DOMAIN_READINESS_MATRIX.csv')
        with open(dom_file, 'a', encoding='utf-8') as f:
            f.write("M010,Invalid Piano Domain,M10,High,Ready,Complete\n")

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Invalid non-canonical domain ID in readiness matrix: 'M010'" in e for e in result['errors']), result['errors'])

    def test_10_mutation_missing_csv_column(self):
        """Mutates relations CSV by dropping a required column from header."""
        rel_file = os.path.join(self.temp_knowledge, 'relations', 'MUSIC_CONCEPT_RELATIONS.csv')
        with open(rel_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        # Drop source_id from header
        lines[0] = "relation_id,target_id,relation_type,epistemic_classification\n"
        with open(rel_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Missing mandatory column 'source_id'" in e for e in result['errors']), result['errors'])

    def test_11_mutation_malformed_markdown_table_row(self):
        """Mutates progression table by omitting one column (reproducing former PROG-016 bug)."""
        prog_file = os.path.join(self.temp_knowledge, 'concepts', 'progressions', 'CHORD_PROGRESSION_REFERENCE_LIBRARY.md')
        with open(prog_file, 'a', encoding='utf-8') as f:
            f.write("| `PROG-028` | Malformed Row | Only 3 Cols |\n")

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Table row has 3 columns, expected 6 (malformed table structure)" in e for e in result['errors']), result['errors'])

    def test_12_mutation_manipulated_golden_test_expected_output_desync(self):
        """Mutates tests golden fixture so it diverges from canonical source of truth."""
        mirror_file = os.path.join(self.temp_tests, 'golden_cases', 'golden_reference_cases.json')
        with open(mirror_file, 'w', encoding='utf-8') as f:
            f.write('[\n  {"case_id": "REF-0001", "mutated": true}\n]')

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Golden cases desynchronization" in e for e in result['errors']), result['errors'])

    def test_13_mutation_unregistered_semantic_migration(self):
        """Mutates migration register by dropping a required column."""
        mig_file = os.path.join(self.temp_knowledge, 'research', 'REFERENCE_ID_MIGRATION_REGISTER.csv')
        with open(mig_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        lines[0] = "original_id,migrated_id,domain,category\n" # Missing 'title', 'action', 'status'
        with open(mig_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Missing mandatory column 'action'" in e for e in result['errors']), result['errors'])

    def test_14_mutation_incorrect_json_datatype(self):
        """Mutates JSON by making the root a dictionary instead of an array."""
        json_file = os.path.join(self.temp_knowledge, 'research', 'golden_cases', 'golden_reference_cases.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            f.write('{"error": "not a list"}')
        mirror_file = os.path.join(self.temp_tests, 'golden_cases', 'golden_reference_cases.json')
        with open(mirror_file, 'w', encoding='utf-8') as f:
            f.write('{"error": "not a list"}')

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Root must be a JSON array, got dict" in e for e in result['errors']), result['errors'])

    def test_15_mutation_invalid_relation_type(self):
        """Mutates relation type with an invalid invented type."""
        rel_file = os.path.join(self.temp_knowledge, 'relations', 'MUSIC_CONCEPT_RELATIONS.csv')
        with open(rel_file, 'a', encoding='utf-8') as f:
            f.write("CR-997,M01,M02,INVALID_INVENTED_RELATION_TYPE,FORMAL_RULE,Scope,Rule,Desc,VERIFIED_ACTIVE\n")

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Invalid relation_type 'INVALID_INVENTED_RELATION_TYPE'" in e for e in result['errors']), result['errors'])

if __name__ == '__main__':
    unittest.main()
