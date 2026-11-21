"""
STEPS Progression Core: Batch 6 Verification Suite (PROG-021..PROG-026, PROG-028 & Atlas Completion).

Validates:
- Complete coverage of all 28 archetypes (PROG-001 through PROG-028) in ARCHETYPE_THEORY_METADATA
- Theory metadata profiles for Neo-Soul, Picardy Third, Liquid D&B, Bossa Nova, Afro-Cuban, Chromatic Bassline, and Soul Cycle
- Archetype pattern detection for PROG-021, PROG-022, PROG-023, PROG-024, PROG-025, PROG-026, PROG-028
- Session recommendations for Bossa Nova applied dominant, Picardy Third, and Afro-Cuban rebound
- Voice leading smoothness analysis for extended and contrapuntal structures
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


class TestBatch6TheoryMetadata(unittest.TestCase):
    """Verifies theory profile metadata for Batch 6 archetypes and 100% atlas coverage."""

    def test_complete_28_archetypes_coverage(self):
        """Verifies that all 28 canonical archetypes (PROG-001..PROG-028) are present."""
        expected_ids = [f'PROG-{i:03d}' for i in range(1, 29)]
        for prog_id in expected_ids:
            self.assertIn(prog_id, ARCHETYPE_THEORY_METADATA, f"{prog_id} missing from ARCHETYPE_THEORY_METADATA")
            profile = ARCHETYPE_THEORY_METADATA[prog_id]
            self.assertIn('family', profile)
            self.assertIn('functional_syntax', profile)
            self.assertIn('harmonic_drive', profile)
            self.assertIn('voice_leading_features', profile)

    def test_prog_021_profile(self):
        p21 = get_progression('PROG-021')
        self.assertEqual(p21.archetype_family, 'NEO_SOUL_ROOTLESS_CYCLE')
        self.assertIn('Mulholland (2013)', p21.theory_profile['tonal_ambiguity']['citations'])

    def test_prog_022_profile(self):
        p22 = get_progression('PROG-022')
        self.assertEqual(p22.archetype_family, 'PICARDY_THIRD_RESOLUTION')
        self.assertIn('Aldwell/Schachter (1989)', p22.theory_profile['tonal_ambiguity']['citations'])

    def test_prog_023_profile(self):
        p23 = get_progression('PROG-023')
        self.assertEqual(p23.archetype_family, 'MODAL_SUBPULSE_CADENCE')
        self.assertIn('Butterfield (2010)', p23.theory_profile['tonal_ambiguity']['citations'])

    def test_prog_024_profile(self):
        p24 = get_progression('PROG-024')
        self.assertEqual(p24.archetype_family, 'BOSSA_NOVA_APPLIED_DOMINANT')
        self.assertIn('Mauleón (1993)', p24.theory_profile['tonal_ambiguity']['citations'])

    def test_prog_025_profile(self):
        p25 = get_progression('PROG-025')
        self.assertEqual(p25.archetype_family, 'AFRO_CUBAN_OSTINATO_VAMP')
        self.assertIn('Peñalosa (2009)', p25.theory_profile['tonal_ambiguity']['citations'])

    def test_prog_026_profile(self):
        p26 = get_progression('PROG-026')
        self.assertEqual(p26.archetype_family, 'CHROMATIC_BASS_SECONDARY_DOMINANT')
        self.assertIn('Kostka (2013)', p26.theory_profile['tonal_ambiguity']['citations'])

    def test_prog_028_profile(self):
        p28 = get_progression('PROG-028')
        self.assertEqual(p28.archetype_family, 'SOUL_CIRCLE_OF_FIFTHS')
        self.assertIn('Mulholland (2013)', p28.theory_profile['tonal_ambiguity']['citations'])


class TestBatch6ArchetypeDetection(unittest.TestCase):
    """Verifies pattern recognition of Batch 6 archetypes."""

    def test_detect_prog_021_neo_soul(self):
        chords = ['Dm9', 'Gm9', 'Bbmaj9', 'A7(b9)']
        matches = detect_progression_archetypes(chords)
        self.assertGreater(len(matches), 0)
        self.assertEqual(matches[0]['prog_id'], 'PROG-021')
        self.assertEqual(matches[0]['score'], 1.0)

    def test_detect_prog_022_picardy_third(self):
        chords = ['Dm', 'Gm', 'C', 'D']
        matches = detect_progression_archetypes(chords)
        self.assertGreater(len(matches), 0)
        self.assertEqual(matches[0]['prog_id'], 'PROG-022')
        self.assertEqual(matches[0]['score'], 1.0)

    def test_detect_prog_023_liquid_dnb(self):
        chords = ['Fm7', 'Dbmaj7', 'Eb', 'Fm']
        matches = detect_progression_archetypes(chords)
        self.assertGreater(len(matches), 0)
        self.assertEqual(matches[0]['prog_id'], 'PROG-023')
        self.assertEqual(matches[0]['score'], 1.0)

    def test_detect_prog_024_bossa_nova(self):
        chords = ['Cmaj7', 'D7', 'Dm7', 'G7', 'Cmaj7']
        matches = detect_progression_archetypes(chords)
        self.assertGreater(len(matches), 0)
        self.assertEqual(matches[0]['prog_id'], 'PROG-024')
        self.assertEqual(matches[0]['score'], 1.0)

    def test_detect_prog_025_afro_cuban(self):
        chords = ['Cm', 'Fm', 'G7', 'Fm']
        matches = detect_progression_archetypes(chords)
        self.assertGreater(len(matches), 0)
        self.assertEqual(matches[0]['prog_id'], 'PROG-025')
        self.assertEqual(matches[0]['score'], 1.0)

    def test_detect_prog_026_chromatic_bassline(self):
        chords = ['G', 'A7/C#', 'Am/C', 'G/B', 'D7/A', 'G']
        matches = detect_progression_archetypes(chords)
        self.assertGreater(len(matches), 0)
        self.assertEqual(matches[0]['prog_id'], 'PROG-026')
        self.assertEqual(matches[0]['score'], 1.0)

    def test_detect_prog_028_soul_circle(self):
        chords = ['Em9', 'Am9', 'D9', 'Gmaj9']
        matches = detect_progression_archetypes(chords)
        self.assertGreater(len(matches), 0)
        self.assertEqual(matches[0]['prog_id'], 'PROG-028')
        self.assertEqual(matches[0]['score'], 1.0)


class TestBatch6SessionRecommendations(unittest.TestCase):
    """Verifies session recommendations for Bossa Nova, Picardy Third, and Afro-Cuban."""

    def test_double_dominant_recommendation_with_tonicization_reference(self):
        session = ProgressionSession(initial_chords=['Cmaj7'], key_root='C', is_minor=False)
        recs = session.explore_next_chords(0)
        double_dominant = next(r for r in recs if 'Doppeldominante' in r.explanation)
        self.assertEqual(double_dominant.candidate_symbol, 'D7')
        self.assertEqual(double_dominant.source_id, 'omt-tonicization')
        self.assertEqual(double_dominant.evidence_kind, 'LITERATURE_REFERENCE')

    def test_bossa_nova_terz_descent_recommendation(self):
        session = ProgressionSession(initial_chords=['D7'], key_root='C', is_minor=False)
        recs = session.explore_next_chords(0)
        terz_rec = next((r for r in recs if 'Bossa Nova Stimmführung' in r.explanation), None)
        self.assertIsNotNone(terz_rec)
        self.assertEqual(terz_rec.candidate_symbol, 'Dm7')

    def test_picardy_third_recommendation(self):
        session = ProgressionSession(initial_chords=['C'], key_root='D', is_minor=True)
        recs = session.explore_next_chords(0)
        picardy_rec = next((r for r in recs if 'Picardy Third' in r.explanation), None)
        self.assertIsNotNone(picardy_rec)
        self.assertEqual(picardy_rec.candidate_symbol, 'D')

    def test_afro_cuban_rebound_recommendation(self):
        session = ProgressionSession(initial_chords=['G7'], key_root='C', is_minor=True)
        recs = session.explore_next_chords(0)
        rebound_rec = next((r for r in recs if 'Afro-Cuban Montuno Vamp' in r.explanation), None)
        self.assertIsNotNone(rebound_rec)
        self.assertEqual(rebound_rec.candidate_symbol, 'Fm')


class TestBatch6VoiceLeadingAnalysis(unittest.TestCase):
    """Verifies voice leading metrics on Batch 6 progressions."""

    def test_voice_leading_metrics_exist(self):
        for prog_id in ['PROG-021', 'PROG-022', 'PROG-023', 'PROG-024', 'PROG-025', 'PROG-026', 'PROG-028']:
            prog = get_progression(prog_id)
            voicings = generate_progression_voicings(prog.chord_definitions)
            analysis = analyze_progression_voice_leading(voicings)
            self.assertIn('total_l1_distance', analysis)
            self.assertIn('average_l1_step', analysis)
            self.assertIn('voice_crossings_count', analysis)
            self.assertGreaterEqual(analysis['total_l1_distance'], 0)


if __name__ == '__main__':
    unittest.main()
