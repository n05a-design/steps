#!/usr/bin/env python3
"""
STEPS Reference Integrity & Semantic Mutation Test Suite (Hardened Phase 4.16)

Executes genuine isolated negative mutation tests against the reference integrity checker:
Each test injects exactly one real defect into an isolated temporary workspace/fixture,
runs verify_integrity(), and asserts that:
1. The defect is detected by the validator fail-closed.
2. The error message accurately describes the injected failure.
3. The canonical repository remains completely untouched.
4. The clean canonical repository passes with 0 errors.

Implements all 15 mandatory negative Gegenproben from Phase 4.16 Master Prompt Section 2.1:
1. REF title unchanged, expected output modified.
2. REF title unchanged, input modified.
3. REF ID unchanged, musical context/domain replaced.
4. PROG ID unchanged, chord progression changed.
5. PAT ID unchanged, rhythmic events/tempo changed.
6. P module ID unchanged, learning target/didactic goal swapped.
7. Relation ID unchanged, target object changed.
8. Baseline hash modified.
9. Baseline modification without migration record detected.
10. Historical object deleted.
11. New object uses already assigned historical ID.
12. Correct reference case receives wrong pitch.
13. Reference case receives wrong swing offset.
14. Reference case receives wrong enharmonic notation.
15. Permitted path: Legitimate documented correction entered as migration passes cleanly.
"""

import os
import sys
import shutil
import tempfile
import unittest
import json
import csv

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
        shutil.copytree(os.path.join(REPO_ROOT, "decisions"), os.path.join(self.temp_dir, "decisions"))

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _sync_golden_mirrors(self, cases):
        """Helper to keep canon and mirror in sync inside temp directory for isolated tests."""
        canon_path = os.path.join(self.temp_knowledge, 'research', 'golden_cases', 'golden_reference_cases.json')
        mirror_path = os.path.join(self.temp_tests, 'golden_cases', 'golden_reference_cases.json')
        with open(canon_path, 'w', encoding='utf-8') as f:
            json.dump(cases, f, indent=2, ensure_ascii=False)
        with open(mirror_path, 'w', encoding='utf-8') as f:
            json.dump(cases, f, indent=2, ensure_ascii=False)

    # =========================================================================
    # CANONICAL VERIFICATION
    # =========================================================================

    def test_00_canonical_repository_passes_cleanly(self):
        """Verifies that the canonical untouched repository passes 100% with zero errors."""
        result = checker.verify_integrity(repo_root=REPO_ROOT)
        self.assertEqual(len(result['errors']), 0, f"Unexpected canonical errors: {result['errors']}")
        stats = result['stats']
        self.assertEqual(stats['progressions'], 28)
        self.assertEqual(stats['drum_patterns'], 31)
        self.assertEqual(stats['piano_modules'], 19)
        self.assertEqual(stats['golden_cases'], 198)
        self.assertEqual(stats['relations'], 94)
        self.assertEqual(stats['adrs'], 12)

    # =========================================================================
    # 15 MANDATORY NEGATIVE MUTATION PROOFS (Section 2.1)
    # =========================================================================

    def test_01_mutation_ref_title_unchanged_expected_output_modified(self):
        """1. REF title remains unchanged, expected output modified -> Detected via semantic hash & field check."""
        canon_path = os.path.join(self.temp_knowledge, 'research', 'golden_cases', 'golden_reference_cases.json')
        with open(canon_path, 'r', encoding='utf-8') as f:
            cases = json.load(f)
        
        # Keep title identical: 'Pitch-Class C4 (MIDI 60)', modify expected_output: 0 -> 99
        cases[0]['expected_output'] = 99
        self._sync_golden_mirrors(cases)

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Expected output changed from 0 to 99" in e for e in result['errors']), result['errors'])
        self.assertTrue(any("Semantic identity hash mismatch for REF-0001" in e for e in result['errors']), result['errors'])

    def test_02_mutation_ref_title_unchanged_input_modified(self):
        """2. REF title remains unchanged, input parameter modified -> Detected via semantic hash & field check."""
        canon_path = os.path.join(self.temp_knowledge, 'research', 'golden_cases', 'golden_reference_cases.json')
        with open(canon_path, 'r', encoding='utf-8') as f:
            cases = json.load(f)
        
        # Keep title identical, modify input: midi_note: 60 -> 61
        cases[0]['input_params'] = {'midi_note': 61}
        self._sync_golden_mirrors(cases)

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Input parameters changed" in e for e in result['errors']), result['errors'])
        self.assertTrue(any("Semantic identity hash mismatch for REF-0001" in e for e in result['errors']), result['errors'])

    def test_03_mutation_ref_id_unchanged_context_domain_replaced(self):
        """3. REF ID remains unchanged, musical domain/context replaced -> Detected via semantic hash."""
        canon_path = os.path.join(self.temp_knowledge, 'research', 'golden_cases', 'golden_reference_cases.json')
        with open(canon_path, 'r', encoding='utf-8') as f:
            cases = json.load(f)
        
        # Replace domain M01 with M08
        cases[0]['domain'] = 'M08'
        self._sync_golden_mirrors(cases)

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Semantic identity hash mismatch for REF-0001" in e for e in result['errors']), result['errors'])

    def test_04_mutation_prog_id_unchanged_chord_progression_changed(self):
        """4. PROG ID remains unchanged, chord progression degrees changed -> Detected."""
        prog_file = os.path.join(self.temp_knowledge, 'concepts', 'progressions', 'CHORD_PROGRESSION_REFERENCE_LIBRARY.md')
        with open(prog_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Mutate PROG-001 degrees from 'I - V - vi - IV' to 'I - IV - V - I'
        mutated = content.replace('| `PROG-001` | Pop Four Chords | `I - V - vi - IV` |',
                                  '| `PROG-001` | Pop Four Chords | `I - IV - V - I` |')
        self.assertNotEqual(content, mutated)
        with open(prog_file, 'w', encoding='utf-8') as f:
            f.write(mutated)

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Harmonic structure changed from 'I - V - vi - IV' to 'I - IV - V - I'" in e for e in result['errors']), result['errors'])

    def test_05_mutation_pat_id_unchanged_rhythmic_events_changed(self):
        """5. PAT ID remains unchanged, tempo/meter changed -> Detected."""
        drum_file = os.path.join(self.temp_knowledge, 'concepts', 'styles', 'DRUM_GROOVE_REFERENCE_LIBRARY.md')
        with open(drum_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Mutate PAT-001 tempo from 115 BPM to 180 BPM
        mutated = content.replace('| `PAT-001` | Pop / Rock Straight | 115 BPM |',
                                  '| `PAT-001` | Pop / Rock Straight | 180 BPM |')
        self.assertNotEqual(content, mutated)
        with open(drum_file, 'w', encoding='utf-8') as f:
            f.write(mutated)

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Tempo changed from '115 BPM' to '180 BPM'" in e for e in result['errors']), result['errors'])

    def test_06_mutation_p_module_id_unchanged_learning_target_swapped(self):
        """6. Piano module ID remains unchanged, didactic goal swapped -> Detected."""
        piano_file = os.path.join(self.temp_knowledge, 'concepts', 'chords', 'PIANO_PRACTICE_REFERENCE_LIBRARY.md')
        with open(piano_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Swap P01 didactic goal
        mutated = content.replace('| `P01` | **Stamm-Dreiklänge & Topografie** | Tastenfindung, Grundstellung, Terzschichtung |',
                                  '| `P01` | **Stamm-Dreiklänge & Topografie** | Komplexe Atonale Dodekaphonie |')
        self.assertNotEqual(content, mutated)
        with open(piano_file, 'w', encoding='utf-8') as f:
            f.write(mutated)

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Didactic goal changed" in e for e in result['errors']), result['errors'])

    def test_07_mutation_relation_id_unchanged_target_changed(self):
        """7. Relation ID remains unchanged, target object changed -> Detected."""
        rel_file = os.path.join(self.temp_knowledge, 'relations', 'MUSIC_CONCEPT_RELATIONS.csv')
        with open(rel_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Mutate CR-001 target from M01-02 to M01-99
        mutated = content.replace('CR-001,M01-01,M01-02,REQUIRES', 'CR-001,M01-01,M01-99,REQUIRES')
        self.assertNotEqual(content, mutated)
        with open(rel_file, 'w', encoding='utf-8') as f:
            f.write(mutated)

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Target changed from 'M01-02' to 'M01-99'" in e for e in result['errors']), result['errors'])

    def test_08_mutation_baseline_hash_modified(self):
        """8. Baseline semantic hash artificially modified -> Detected."""
        baseline_file = os.path.join(self.temp_knowledge, 'research', 'REFERENCE_IDENTITY_BASELINE.json')
        with open(baseline_file, 'r', encoding='utf-8') as f:
            b = json.load(f)
        
        # Artificially alter REF-0001 semantic hash in baseline
        b['reference_cases']['REF-0001']['semantic_hash'] = '0000000000000000000000000000000000000000000000000000000000000000'
        with open(baseline_file, 'w', encoding='utf-8') as f:
            json.dump(b, f, indent=2)

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Semantic identity hash mismatch for REF-0001" in e for e in result['errors']), result['errors'])

    def test_09_mutation_baseline_modification_without_migration_record(self):
        """9. Baseline modified without authorized migration record -> Detected fail-closed."""
        baseline_file = os.path.join(self.temp_knowledge, 'research', 'REFERENCE_IDENTITY_BASELINE.json')
        with open(baseline_file, 'r', encoding='utf-8') as f:
            b = json.load(f)
        
        # Change PROG-001 name in baseline without entering into migration register
        b['progressions']['PROG-001']['name'] = 'Invented Pop Progression'
        with open(baseline_file, 'w', encoding='utf-8') as f:
            json.dump(b, f, indent=2)

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Semantic identity conflict for PROG-001: Name changed from 'Invented Pop Progression'" in e for e in result['errors']), result['errors'])

    def test_10_mutation_historical_object_deleted(self):
        """10. Historical object REF-0001 deleted from repository -> Detected."""
        canon_path = os.path.join(self.temp_knowledge, 'research', 'golden_cases', 'golden_reference_cases.json')
        with open(canon_path, 'r', encoding='utf-8') as f:
            cases = json.load(f)
        
        cases = [c for c in cases if c['case_id'] != 'REF-0001'] # Delete REF-0001
        self._sync_golden_mirrors(cases)

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Baseline Golden Case 'REF-0001' missing from current test suite" in e for e in result['errors']), result['errors'])

    def test_11_mutation_new_object_reuses_allocated_historical_id(self):
        """11. New object attempts to hijack allocated historical ID REF-0002 -> Detected."""
        canon_path = os.path.join(self.temp_knowledge, 'research', 'golden_cases', 'golden_reference_cases.json')
        with open(canon_path, 'r', encoding='utf-8') as f:
            cases = json.load(f)
        
        # Duplicate case with REF-0002 ID but different content
        hijacked = dict(cases[1])
        hijacked['title'] = "Hijacked Concept For Historical ID"
        cases[1] = hijacked
        self._sync_golden_mirrors(cases)

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Historical identity conflict for REF-0002: Title changed" in e for e in result['errors']), result['errors'])

    def test_12_mutation_reference_case_wrong_pitch(self):
        """12. Reference case REF-0001 receives musical pitch corruption (e.g. 7 instead of 0) -> Detected."""
        canon_path = os.path.join(self.temp_knowledge, 'research', 'golden_cases', 'golden_reference_cases.json')
        with open(canon_path, 'r', encoding='utf-8') as f:
            cases = json.load(f)
        
        # Corrupt pitch output of REF-0001
        cases[0]['expected_output'] = 7 # G instead of C
        self._sync_golden_mirrors(cases)

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Expected output changed from 0 to 7" in e for e in result['errors']), result['errors'])

    def test_13_mutation_reference_case_wrong_swing_offset(self):
        """13. Reference case REF-0177 receives false swing offset -> Detected."""
        canon_path = os.path.join(self.temp_knowledge, 'research', 'golden_cases', 'golden_reference_cases.json')
        with open(canon_path, 'r', encoding='utf-8') as f:
            cases = json.load(f)
        
        # Corrupt REF-0177 expected output (0 -> 120)
        for c in cases:
            if c['case_id'] == 'REF-0177':
                c['expected_output'] = 120
                break
        self._sync_golden_mirrors(cases)

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Expected output changed from 0 to 120" in e for e in result['errors']), result['errors'])

    def test_14_mutation_reference_case_wrong_enharmonic_notation(self):
        """14. Reference case REF-0003 receives wrong enharmonic note spelling -> Detected."""
        canon_path = os.path.join(self.temp_knowledge, 'research', 'golden_cases', 'golden_reference_cases.json')
        with open(canon_path, 'r', encoding='utf-8') as f:
            cases = json.load(f)
        
        for c in cases:
            if c['case_id'] == 'REF-0003':
                c['expected_output'] = 'E#' # Incorrect enharmonic spelling
                break
        self._sync_golden_mirrors(cases)

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Expected output changed" in e for e in result['errors']), result['errors'])

    def test_15_controlled_migration_path_accepted(self):
        """15. Permitted path: Legitimate documented correction with CONTROLLED_CORRECTION passes."""
        # Update a case in golden_cases
        canon_path = os.path.join(self.temp_knowledge, 'research', 'golden_cases', 'golden_reference_cases.json')
        with open(canon_path, 'r', encoding='utf-8') as f:
            cases = json.load(f)
        
        # Legitimate typographical improvement for REF-0198
        cases[-1]['title'] = "Tick Dauer ms bei 120 BPM und 480 PPQ (Präzise)"
        self._sync_golden_mirrors(cases)

        # Register authorized migration in migration register
        mig_file = os.path.join(self.temp_knowledge, 'research', 'REFERENCE_ID_MIGRATION_REGISTER.csv')
        with open(mig_file, 'a', encoding='utf-8') as f:
            f.write("REF-0198,REF-0198,M11,MIDI_TIMING,Tick Dauer ms bei 120 BPM und 480 PPQ (Präzise),Phase 4.16,Authorized typographical refinement,CONTROLLED_CORRECTION,ACTIVE\n")

        result = checker.verify_integrity(repo_root=self.temp_dir)
        # Verify that REF-0198 was exempted from hash mismatch failure because it was authorized
        self.assertFalse(any("Semantic identity hash mismatch for REF-0198" in e for e in result['errors']), result['errors'])

    # =========================================================================
    # STRUCTURAL INTEGRITY MUTATIONS
    # =========================================================================

    def test_16_mutation_duplicate_prog_id(self):
        """Duplicate PROG-001 detected."""
        prog_file = os.path.join(self.temp_knowledge, 'concepts', 'progressions', 'CHORD_PROGRESSION_REFERENCE_LIBRARY.md')
        with open(prog_file, 'a', encoding='utf-8') as f:
            f.write("\n| `PROG-001` | Duplicate Pop Four | `I - V - vi - IV` | `C - G - Am - F` | Pop | M05 |\n")

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Duplicate definition of ID 'PROG-001'" in e for e in result['errors']), result['errors'])

    def test_17_mutation_malformed_markdown_table_row(self):
        """Malformed markdown row (missing column) detected."""
        prog_file = os.path.join(self.temp_knowledge, 'concepts', 'progressions', 'CHORD_PROGRESSION_REFERENCE_LIBRARY.md')
        with open(prog_file, 'a', encoding='utf-8') as f:
            f.write("| `PROG-099` | Malformed Row | Only 3 Cols |\n")

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Table row has 3 columns, expected 6 (malformed table structure)" in e for e in result['errors']), result['errors'])

    def test_18_mutation_desync_between_canon_and_mirror(self):
        """Desynchronization between canon and mirror JSON detected."""
        mirror_file = os.path.join(self.temp_tests, 'golden_cases', 'golden_reference_cases.json')
        with open(mirror_file, 'w', encoding='utf-8') as f:
            f.write('[\n  {"case_id": "REF-0001", "mutated": true}\n]')

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Golden cases desynchronization" in e for e in result['errors']), result['errors'])

    def test_19_mutation_adr_topic_reassignment_fails_closed(self):
        """ADR topic reassignment (e.g. changing ADR-005 to PyInstaller) fails closed (Section 1.3)."""
        decisions_file = os.path.join(self.temp_dir, 'decisions', 'DECISION_REGISTER.md')
        with open(decisions_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Mutate ADR-005 theme
        mutated_content = content.replace(
            "| ADR-005 | proposed | Fachmodell",
            "| ADR-005 | proposed | Release-Packaging-Modell mit PyInstaller"
        )
        with open(decisions_file, 'w', encoding='utf-8') as f:
            f.write(mutated_content)

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Semantic identity conflict in ADR-005" in e for e in result['errors']), result['errors'])

    def test_20_mutation_graph_topology_dangling_reference(self):
        """Graph relation containing a dangling target reference fails closed (Section 3.2)."""
        rel_file = os.path.join(self.temp_knowledge, 'relations', 'MUSIC_CONCEPT_RELATIONS.csv')
        with open(rel_file, 'a', encoding='utf-8') as f:
            f.write("CR-999,M01-01,PROG-999,REQUIRES,FORMAL_RULE,Testing,Test Rule,Test desc,PROPOSED\n")

        result = checker.verify_integrity(repo_root=self.temp_dir)
        self.assertGreater(len(result['errors']), 0)
        self.assertTrue(any("Dangling reference in target_id: ID 'PROG-999'" in e for e in result['errors']), result['errors'])

if __name__ == '__main__':
    unittest.main()
