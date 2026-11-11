import unittest
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import scripts.verify_reference_integrity as checker

class TestReferenceIntegrity(unittest.TestCase):
    def test_canonical_reference_integrity_passes(self):
        """Verifies that the actual repository knowledge base passes 100% without errors."""
        result = checker.verify_integrity()
        self.assertEqual(len(result['errors']), 0, f"Integrity errors found: {result['errors']}")
        stats = result['stats']
        self.assertGreaterEqual(stats['progressions'], 27)
        self.assertGreaterEqual(stats['drum_patterns'], 29)
        self.assertGreaterEqual(stats['piano_modules'], 19)
        self.assertEqual(stats['golden_cases'], 100)

    def test_detects_dangling_reference_in_relations(self):
        """Verifies that referencing a non-existent PROG or P module ID triggers an error."""
        prog_ids, _ = checker.extract_progression_ids(checker.PROG_LIB_PATH)
        self.assertNotIn("PROG-999", prog_ids)

    def test_canonical_domain_validation(self):
        """Verifies that canonical domains are strictly M01 to M12."""
        self.assertEqual(len(checker.CANONICAL_DOMAINS), 12)
        self.assertIn("M10", checker.CANONICAL_DOMAINS)
        self.assertNotIn("M010", checker.CANONICAL_DOMAINS)

    def test_epistemic_classification_vocab(self):
        """Verifies valid epistemic classifications taxonomy."""
        expected = {
            'FORMAL_RULE',
            'HISTORICAL_CONVENTION',
            'GENRE_TENDENCY',
            'PEDAGOGICAL_RECOMMENDATION',
            'SOFTWARE_DESIGN_RULE',
            'ILLUSTRATIVE_RELATION'
        }
        self.assertEqual(checker.VALID_EPISTEMIC_CLASSES, expected)

if __name__ == '__main__':
    unittest.main()
