"""
STEPS Progression Core: Batch 4 Verification Suite (PROG-006, PROG-015, PROG-016, PROG-019).

Validates:
- Theory metadata profiles for Pachelbel, Royal Road, Coltrane Changes, and Line Cliché
- Archetype pattern detection for PROG-006, PROG-015, PROG-016, PROG-019
- Royal Road (iii -> vi) and Minor Line Cliché (i -> i(maj7) -> i7 -> im6) recommendations
"""

import unittest

from src.steps.progression.engine import (
    ARCHETYPE_THEORY_METADATA,
    CanonicalProgression,
    get_progression,
    detect_progression_archetypes
)
from src.steps.progression.session import ProgressionSession


class TestBatch4TheoryMetadata(unittest.TestCase):
    """Verifies theory profile metadata for Batch 4 archetypes."""

    def test_prog_006_profile(self):
        p6 = get_progression('PROG-006')
        self.assertEqual(p6.archetype_family, 'PACHELBEL_ROMANESCA_SEQUENCE')
        profile = p6.theory_profile
        self.assertIn('Fux (1725)', profile['tonal_ambiguity']['citations'])
        self.assertIn('Rameau (1722)', profile['tonal_ambiguity']['citations'])

    def test_prog_015_profile(self):
        p15 = get_progression('PROG-015')
        self.assertEqual(p15.archetype_family, 'ROYAL_ROAD_ODO_SHINKO')
        profile = p15.theory_profile
        self.assertEqual(profile['functional_syntax'], 'IVmaj7 - V7 - iii7 - vi (Smaj7 - D7 - Dp7 - Tp)')
        self.assertIn('Jaffe (1996)', profile['tonal_ambiguity']['citations'])

    def test_prog_016_profile(self):
        p16 = get_progression('PROG-016')
        self.assertEqual(p16.archetype_family, 'COLTRANE_CHANGES_THREE_TONIC')
        profile = p16.theory_profile
        amb = profile['tonal_ambiguity']
        self.assertEqual(amb['primary_key'], 'B')
        self.assertEqual(amb['tonic_centers'], ['B', 'G', 'Eb'])
        self.assertEqual(amb['symmetry_interval'], 4)
        self.assertIn('Cohn (2012)', amb['citations'])
        self.assertIn('Tymoczko (2011)', amb['citations'])

    def test_prog_019_profile(self):
        p19 = get_progression('PROG-019')
        self.assertEqual(p19.archetype_family, 'MINOR_LINE_CLICHE')
        profile = p19.theory_profile
        amb = profile['tonal_ambiguity']
        self.assertEqual(amb['tonic'], 'Am')
        self.assertEqual(amb['cliche_voice'], 'A -> G# -> G -> F# (semitone descent)')
        self.assertIn('Levine (1995)', amb['citations'])


class TestBatch4ArchetypeDetection(unittest.TestCase):
    """Verifies pattern recognition of Batch 4 archetypes."""

    def test_detect_prog_006_pachelbel(self):
        # D - A - Bm - F#m - G - D - G - A: exactly PROG-006
        chords = ['D', 'A', 'Bm', 'F#m', 'G', 'D', 'G', 'A']
        matches = detect_progression_archetypes(chords)
        self.assertGreater(len(matches), 0)
        self.assertEqual(matches[0]['prog_id'], 'PROG-006')
        self.assertEqual(matches[0]['score'], 1.0)
        self.assertTrue(matches[0]['is_exact_match'])

    def test_detect_prog_015_royal_road(self):
        # Fmaj7 - G7 - Em7 - Am: exactly PROG-015
        chords = ['Fmaj7', 'G7', 'Em7', 'Am']
        matches = detect_progression_archetypes(chords)
        self.assertGreater(len(matches), 0)
        self.assertEqual(matches[0]['prog_id'], 'PROG-015')
        self.assertEqual(matches[0]['score'], 1.0)

    def test_detect_prog_016_coltrane_changes(self):
        # Bmaj7 - D7 - Gmaj7 - Bb7 - Ebmaj7: exactly PROG-016
        chords = ['Bmaj7', 'D7', 'Gmaj7', 'Bb7', 'Ebmaj7']
        matches = detect_progression_archetypes(chords)
        self.assertGreater(len(matches), 0)
        self.assertEqual(matches[0]['prog_id'], 'PROG-016')
        self.assertEqual(matches[0]['score'], 1.0)

    def test_detect_prog_019_minor_line_cliche(self):
        # Am - Am(maj7) - Am7 - Am6: exactly PROG-019
        chords = ['Am', 'Am(maj7)', 'Am7', 'Am6']
        matches = detect_progression_archetypes(chords)
        self.assertGreater(len(matches), 0)
        self.assertEqual(matches[0]['prog_id'], 'PROG-019')
        self.assertEqual(matches[0]['score'], 1.0)


class TestBatch4SessionRecommendations(unittest.TestCase):
    """Verifies session recommendations for Royal Road and Line Cliché."""

    def test_royal_road_mediant_resolution(self):
        # In C major session, chord at index 0 is Em (iii)
        session = ProgressionSession(initial_chords=['Em'], key_root='C', is_minor=False)
        recs = session.explore_next_chords(0)
        rr_rec = next((r for r in recs if 'Royal Road' in r.explanation), None)
        self.assertIsNotNone(rr_rec)
        self.assertEqual(rr_rec.candidate_symbol, 'Am')
        self.assertEqual(rr_rec.relation_type, 'RESOLVES_TO')

    def test_minor_line_cliche_step_progression(self):
        # In Am minor session, test step 1: Am -> Am(maj7)
        session1 = ProgressionSession(initial_chords=['Am'], key_root='A', is_minor=True)
        recs1 = session1.explore_next_chords(0)
        cliche1 = next((r for r in recs1 if '8 -> 7' in r.explanation), None)
        self.assertIsNotNone(cliche1)
        self.assertEqual(cliche1.candidate_symbol, 'Am(maj7)')

        # Test step 2: Am(maj7) -> Am7
        session2 = ProgressionSession(initial_chords=['Am(maj7)'], key_root='A', is_minor=True)
        recs2 = session2.explore_next_chords(0)
        cliche2 = next((r for r in recs2 if '7 -> b7' in r.explanation), None)
        self.assertIsNotNone(cliche2)
        self.assertEqual(cliche2.candidate_symbol, 'Am7')

        # Test step 3: Am7 -> Am6
        session3 = ProgressionSession(initial_chords=['Am7'], key_root='A', is_minor=True)
        recs3 = session3.explore_next_chords(0)
        cliche3 = next((r for r in recs3 if 'b7 -> 6' in r.explanation), None)
        self.assertIsNotNone(cliche3)
        self.assertEqual(cliche3.candidate_symbol, 'Am6')


if __name__ == '__main__':
    unittest.main()
