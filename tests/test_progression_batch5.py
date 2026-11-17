"""
STEPS Progression Core: Batch 5 Verification Suite (PROG-008, PROG-017, PROG-018, PROG-020, PROG-027).

Validates:
- Theory metadata profiles for Blues, Backdoor ii-V, Altered Tritone Sub, and Minor Blues Turnaround
- Archetype pattern detection for PROG-008, PROG-017, PROG-018, PROG-020, PROG-027
- Session chord recommendations for Backdoor, Blues, and Altered Sub
- Voice leading smoothness analysis for extended and altered jazz structures
"""

import unittest

from src.steps.progression.engine import (
    ARCHETYPE_THEORY_METADATA,
    CanonicalProgression,
    get_progression,
    detect_progression_archetypes,
    generate_progression_voicings,
    analyze_progression_voice_leading,
)
from src.steps.progression.session import ProgressionSession


class TestBatch5TheoryMetadata(unittest.TestCase):
    """Verifies theory profile metadata for Batch 5 archetypes."""

    def test_prog_008_profile(self):
        p8 = get_progression('PROG-008')
        self.assertEqual(p8.archetype_family, 'BLUES_12_BAR')
        profile = p8.theory_profile
        self.assertEqual(profile['functional_syntax'], 'Idom7 - IVdom7 - Idom7 - V7 - IVdom7 - Idom7')
        self.assertIn('Rawlins/Bahha (2005)', profile['tonal_ambiguity']['citations'])

    def test_prog_017_profile(self):
        p17 = get_progression('PROG-017')
        self.assertEqual(p17.archetype_family, 'CLASSICAL_JAZZ_BACKDOOR_II_V')
        profile = p17.theory_profile
        self.assertEqual(profile['functional_syntax'], 'iv7 - bVII7 - Imaj7 (s7 - Subtonik7 - Tmaj7)')
        self.assertIn('Levine (1995)', profile['tonal_ambiguity']['citations'])
        self.assertIn('Terefenko (2014)', profile['tonal_ambiguity']['citations'])

    def test_prog_018_profile(self):
        p18 = get_progression('PROG-018')
        self.assertEqual(p18.archetype_family, 'SUBSTITUTE_BACKDOOR_II_V')
        profile = p18.theory_profile
        self.assertEqual(profile['functional_syntax'], 'ii7 - bVII7 - Imaj7 (Sp7 - Subtonik7 - Tmaj7)')
        self.assertIn('Rawlins/Bahha (2005)', profile['tonal_ambiguity']['citations'])

    def test_prog_020_profile(self):
        p20 = get_progression('PROG-020')
        self.assertEqual(p20.archetype_family, 'EXTENDED_TRITONE_SUB_ALTERED')
        profile = p20.theory_profile
        amb = profile['tonal_ambiguity']
        self.assertEqual(amb['tonic'], 'C')
        self.assertIn('Levine (1995)', amb['citations'])
        self.assertIn('Pease (2003)', amb['citations'])

    def test_prog_027_profile(self):
        p27 = get_progression('PROG-027')
        self.assertEqual(p27.archetype_family, 'MINOR_JAZZ_BLUES_SUBMEDIANT_TURNAROUND')
        profile = p27.theory_profile
        amb = profile['tonal_ambiguity']
        self.assertEqual(amb['tonic'], 'Cm')
        self.assertIn("Birk's Works", amb['standards'])
        self.assertIn('Levine (1995)', amb['citations'])


class TestBatch5ArchetypeDetection(unittest.TestCase):
    """Verifies pattern recognition of Batch 5 archetypes."""

    def test_detect_prog_008_blues(self):
        chords = ['C7', 'F7', 'C7', 'G7', 'F7', 'C7']
        matches = detect_progression_archetypes(chords)
        self.assertGreater(len(matches), 0)
        self.assertEqual(matches[0]['prog_id'], 'PROG-008')
        self.assertEqual(matches[0]['score'], 1.0)
        self.assertTrue(matches[0]['is_exact_match'])

    def test_detect_prog_017_classical_backdoor(self):
        chords = ['Fm7', 'Bb7', 'Cmaj7']
        matches = detect_progression_archetypes(chords)
        self.assertGreater(len(matches), 0)
        self.assertEqual(matches[0]['prog_id'], 'PROG-017')
        self.assertEqual(matches[0]['score'], 1.0)

    def test_detect_prog_018_substitute_backdoor(self):
        chords = ['Dm7', 'Bb7', 'Cmaj7']
        matches = detect_progression_archetypes(chords)
        self.assertGreater(len(matches), 0)
        self.assertEqual(matches[0]['prog_id'], 'PROG-018')
        self.assertEqual(matches[0]['score'], 1.0)

    def test_detect_prog_020_extended_tritone_sub(self):
        chords = ['Dm9', 'Db7(#11)', 'Cmaj9']
        matches = detect_progression_archetypes(chords)
        self.assertGreater(len(matches), 0)
        self.assertEqual(matches[0]['prog_id'], 'PROG-020')
        self.assertEqual(matches[0]['score'], 1.0)

    def test_detect_prog_027_minor_jazz_blues(self):
        chords = ['Cm7', 'Fm7', 'Cm7', 'Abmaj7', 'G7(#11)', 'Cm7']
        matches = detect_progression_archetypes(chords)
        self.assertGreater(len(matches), 0)
        self.assertEqual(matches[0]['prog_id'], 'PROG-027')
        self.assertEqual(matches[0]['score'], 1.0)

    def test_detect_prog_017_transposition_to_f(self):
        # In F major: Bbm7 - Eb7 - Fmaj7
        chords = ['Bbm7', 'Eb7', 'Fmaj7']
        matches = detect_progression_archetypes(chords)
        self.assertGreater(len(matches), 0)
        top_match = next((m for m in matches if m['prog_id'] == 'PROG-017'), None)
        self.assertIsNotNone(top_match)
        self.assertEqual(top_match['transposition_semitones'], 5)


class TestBatch5SessionRecommendations(unittest.TestCase):
    """Verifies session recommendations for Backdoor, Blues, and Altered Sub."""

    def test_blues_tonic_to_subdominant(self):
        session = ProgressionSession(initial_chords=['C7'], key_root='C', is_minor=False)
        recs = session.explore_next_chords(0)
        blues_rec = next((r for r in recs if '12-Bar Blues' in r.framework and r.candidate_symbol == 'F7'), None)
        self.assertIsNotNone(blues_rec)
        self.assertEqual(blues_rec.relation_type, 'RESOLVES_TO')

    def test_classical_backdoor_iv_to_bvii(self):
        session = ProgressionSession(initial_chords=['Fm7'], key_root='C', is_minor=False)
        recs = session.explore_next_chords(0)
        backdoor_rec = next((r for r in recs if 'Classical Jazz Backdoor' in r.framework), None)
        self.assertIsNotNone(backdoor_rec)
        self.assertEqual(backdoor_rec.candidate_symbol, 'Bb7')

    def test_substitute_backdoor_ii_to_bvii(self):
        session = ProgressionSession(initial_chords=['Dm7'], key_root='C', is_minor=False)
        recs = session.explore_next_chords(0)
        sub_rec = next((r for r in recs if 'Substitute Backdoor' in r.framework), None)
        self.assertIsNotNone(sub_rec)
        self.assertEqual(sub_rec.candidate_symbol, 'Bb7')

    def test_extended_tritone_sub_resolution(self):
        session = ProgressionSession(initial_chords=['Db7(#11)'], key_root='C', is_minor=False)
        recs = session.explore_next_chords(0)
        tritone_rec = next((r for r in recs if 'Extended Tritone Sub' in r.framework), None)
        self.assertIsNotNone(tritone_rec)
        self.assertEqual(tritone_rec.candidate_symbol, 'Cmaj9')

    def test_minor_blues_turnaround_resolutions(self):
        # 1. From subdominant Fm7 -> Abmaj7
        session1 = ProgressionSession(initial_chords=['Fm7'], key_root='C', is_minor=True)
        recs1 = session1.explore_next_chords(0)
        mb_rec1 = next((r for r in recs1 if 'Minor Jazz Blues' in r.framework and r.candidate_symbol == 'Abmaj7'), None)
        self.assertIsNotNone(mb_rec1)

        # 2. From Abmaj7 -> G7(#11)
        session2 = ProgressionSession(initial_chords=['Abmaj7'], key_root='C', is_minor=True)
        recs2 = session2.explore_next_chords(0)
        mb_rec2 = next((r for r in recs2 if 'Minor Jazz Blues' in r.framework and '7(#11)' in r.candidate_symbol), None)
        self.assertIsNotNone(mb_rec2)


class TestBatch5VoiceLeadingAnalysis(unittest.TestCase):
    """Verifies voice leading metrics on Batch 5 progressions."""

    def test_voice_leading_metrics_exist(self):
        for prog_id in ['PROG-008', 'PROG-017', 'PROG-018', 'PROG-020', 'PROG-027']:
            prog = get_progression(prog_id)
            voicings = generate_progression_voicings(prog.chord_definitions)
            analysis = analyze_progression_voice_leading(voicings)
            self.assertIn('total_l1_distance', analysis)
            self.assertIn('average_l1_step', analysis)
            self.assertIn('voice_crossings_count', analysis)
            self.assertGreaterEqual(analysis['total_l1_distance'], 0)


if __name__ == '__main__':
    unittest.main()
