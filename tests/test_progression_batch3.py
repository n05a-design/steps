"""
STEPS Progression Core: Batch 3 Verification Suite (PROG-007, PROG-010, PROG-011, PROG-013, PROG-014).

Validates:
- Theory metadata profiles for modal, secondary dominant, and tritone archetypes
- Archetype pattern detection for PROG-007, PROG-010, PROG-011, PROG-013, PROG-014
- Tritone substitution and backdoor resolution recommendations
- Secondary dominant lift (V7/vi) recommendations
"""

import unittest

from src.steps.progression.engine import (
    ARCHETYPE_THEORY_METADATA,
    CanonicalProgression,
    get_progression,
    detect_progression_archetypes
)
from src.steps.progression.session import ProgressionSession


class TestBatch3TheoryMetadata(unittest.TestCase):
    """Verifies theory profile metadata for Batch 3 archetypes."""

    def test_prog_007_profile(self):
        p7 = get_progression('PROG-007')
        self.assertEqual(p7.archetype_family, 'MODAL_DORIAN_VAMP')
        profile = p7.theory_profile
        self.assertEqual(profile['functional_syntax'], 'i7 - IV7 (t7 - S7[dur])')
        amb = profile['tonal_ambiguity']
        self.assertEqual(amb['modal_center'], 'Dm')
        self.assertIn('Pease (2003)', amb['citations'])

    def test_prog_010_profile(self):
        p10 = get_progression('PROG-010')
        self.assertEqual(p10.archetype_family, 'SECONDARY_DOMINANT_PROLONGATION')
        profile = p10.theory_profile
        amb = profile['tonal_ambiguity']
        self.assertEqual(amb['applied_target'], 'Am (vi)')
        self.assertIn('Kostka/Payne (2013)', amb['citations'])

    def test_prog_011_profile(self):
        p11 = get_progression('PROG-011')
        self.assertEqual(p11.archetype_family, 'MODAL_INTERCHANGE_AEOLIAN')
        profile = p11.theory_profile
        amb = profile['tonal_ambiguity']
        self.assertEqual(amb['borrowed_mode'], 'C Minor / C Aeolian')
        self.assertIn('Mulholland (2013)', amb['citations'])

    def test_prog_013_profile(self):
        p13 = get_progression('PROG-013')
        self.assertEqual(p13.archetype_family, 'TRITONE_SUBSTITUTION_CADENCE')
        profile = p13.theory_profile
        amb = profile['tonal_ambiguity']
        self.assertEqual(amb['substitute_for'], 'G7 (V7)')
        self.assertEqual(amb['common_tritone'], ['F', 'B/Cb'])
        self.assertIn('Levine (1995)', amb['citations'])

    def test_prog_014_profile(self):
        p14 = get_progression('PROG-014')
        self.assertEqual(p14.archetype_family, 'BACKDOOR_RESOLUTION')
        profile = p14.theory_profile
        amb = profile['tonal_ambiguity']
        self.assertEqual(amb['backdoor_dominant'], 'Bb7')
        self.assertIn('Terefenko (2014)', amb['citations'])


class TestBatch3ArchetypeDetection(unittest.TestCase):
    """Verifies recognition of Batch 3 archetypes."""

    def test_detect_prog_007_dorian_vamp(self):
        # Dm7 - G7: exactly PROG-007
        matches = detect_progression_archetypes(['Dm7', 'G7'])
        self.assertGreater(len(matches), 0)
        self.assertEqual(matches[0]['prog_id'], 'PROG-007')
        self.assertEqual(matches[0]['score'], 1.0)
        self.assertTrue(matches[0]['is_exact_match'])

    def test_detect_prog_010_secondary_dominant_lift(self):
        # C - E7 - Am - F: exactly PROG-010
        matches = detect_progression_archetypes(['C', 'E7', 'Am', 'F'])
        self.assertGreater(len(matches), 0)
        self.assertEqual(matches[0]['prog_id'], 'PROG-010')
        self.assertEqual(matches[0]['score'], 1.0)

    def test_detect_prog_011_modal_interchange(self):
        # C - Ab - Bb - C: exactly PROG-011
        matches = detect_progression_archetypes(['C', 'Ab', 'Bb', 'C'])
        self.assertGreater(len(matches), 0)
        self.assertEqual(matches[0]['prog_id'], 'PROG-011')
        self.assertEqual(matches[0]['score'], 1.0)

    def test_detect_prog_013_tritone_sub(self):
        # Dm7 - Db7 - Cmaj7: exactly PROG-013
        matches = detect_progression_archetypes(['Dm7', 'Db7', 'Cmaj7'])
        self.assertGreater(len(matches), 0)
        self.assertEqual(matches[0]['prog_id'], 'PROG-013')
        self.assertEqual(matches[0]['score'], 1.0)

    def test_detect_prog_014_backdoor(self):
        # F - Bb7 - C: exactly PROG-014
        matches = detect_progression_archetypes(['F', 'Bb7', 'C'])
        self.assertGreater(len(matches), 0)
        self.assertEqual(matches[0]['prog_id'], 'PROG-014')
        self.assertEqual(matches[0]['score'], 1.0)


class TestBatch3SessionRecommendations(unittest.TestCase):
    """Verifies recommendations for tritone sub, backdoor, and secondary dominants."""

    def test_session_tritone_substitution_recommendation(self):
        # In C major session, chord at index 0 is Dm (ii)
        session = ProgressionSession(initial_chords=['Dm'], key_root='C', is_minor=False)
        recs = session.explore_next_chords(0)
        tritone_rec = next((r for r in recs if 'Tritonussubstitution' in r.explanation), None)
        self.assertIsNotNone(tritone_rec)
        self.assertEqual(tritone_rec.candidate_symbol, 'Db7')
        self.assertEqual(tritone_rec.relation_type, 'SUBSTITUTES_FOR')

    def test_session_backdoor_recommendation(self):
        # In C major session, chord at index 0 is Bb7 (bVII)
        session = ProgressionSession(initial_chords=['Bb7'], key_root='C', is_minor=False)
        recs = session.explore_next_chords(0)
        backdoor_rec = next((r for r in recs if 'Backdoor-Auflösung' in r.explanation), None)
        self.assertIsNotNone(backdoor_rec)
        self.assertEqual(backdoor_rec.candidate_symbol, 'C')
        self.assertEqual(backdoor_rec.relation_type, 'RESOLVES_TO')

    def test_session_secondary_dominant_recommendation(self):
        # In C major session, chord at index 0 is C (I)
        session = ProgressionSession(initial_chords=['C'], key_root='C', is_minor=False)
        recs = session.explore_next_chords(0)
        sec_rec = next((r for r in recs if 'V7/vi' in r.explanation), None)
        self.assertIsNotNone(sec_rec)
        self.assertEqual(sec_rec.candidate_symbol, 'E7')
        self.assertEqual(sec_rec.relation_type, 'DOMINANT_OF')


if __name__ == '__main__':
    unittest.main()
