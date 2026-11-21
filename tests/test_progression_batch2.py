"""
STEPS Progression Core: Batch 2 Verification Suite (PROG-002, PROG-004, PROG-005, PROG-012).

Validates:
- Deep musicological profiles in ARCHETYPE_THEORY_METADATA
- Pattern detection and rotation analysis via detect_progression_archetypes()
- Andalusian Cadence (PROG-005) descending tetrachord & Phrygian half-cadence
- 50s Doo-Wop Loop (PROG-004) submediant prolongation & authentic turnaround
- Emotional Minor Loop (PROG-002) dual-center ambiguity & Axis rotation
- Descending Circle of Fifths (PROG-012) quintal root motion (Rameau / Salzer)
- Interactive session recommendations in ProgressionSession
"""

import unittest

from src.steps.progression.engine import (
    ARCHETYPE_THEORY_METADATA,
    CanonicalProgression,
    get_progression,
    list_progressions,
    detect_progression_archetypes,
    generate_progression_voicings,
    analyze_progression_voice_leading
)
from src.steps.progression.session import ProgressionSession
from src.steps.progression.voice_leading import VoiceLeadingStyle


class TestBatch2TheoryMetadata(unittest.TestCase):
    """Verifies theory profile metadata for archetypes PROG-001..PROG-005 and PROG-012."""

    def test_prog_002_profile(self):
        p2 = get_progression('PROG-002')
        self.assertEqual(p2.archetype_family, 'AXIS_PROGRESSION_MINOR_ROTATION')
        profile = p2.theory_profile
        self.assertIn('tonal_ambiguity', profile)
        amb = profile['tonal_ambiguity']
        self.assertTrue(amb['dual_center'])
        self.assertEqual(amb['primary_center'], 'Am')
        self.assertEqual(amb['relative_center'], 'C')
        self.assertIn('Tagg (2014)', amb['citations'])
        self.assertIn('Richards (2017)', amb['citations'])

    def test_prog_004_profile(self):
        p4 = get_progression('PROG-004')
        self.assertEqual(p4.archetype_family, 'DOO_WOP_AUTHENTIC_LOOP')
        profile = p4.theory_profile
        self.assertEqual(profile['functional_syntax'], 'I - vi - IV - V (T - Tp - S - D)')
        amb = profile['tonal_ambiguity']
        self.assertEqual(amb['primary_center'], 'C')
        self.assertIn('Aldwell/Schachter (1989)', amb['citations'])

    def test_prog_005_profile(self):
        p5 = get_progression('PROG-005')
        self.assertEqual(p5.archetype_family, 'ANDALUSIAN_CADENCE_PHRYGIAN')
        profile = p5.theory_profile
        self.assertEqual(profile['functional_syntax'], 'i - bVII - bVI - V (t - dP - sP - D[dur])')
        amb = profile['tonal_ambiguity']
        self.assertEqual(amb['modal_context'], 'A Minor / A Phrygian Dominant')
        self.assertEqual(amb['tetrachord_motion'], 'A -> G -> F -> E (descending natural scale degrees 1 - b7 - b6 - 5)')
        self.assertIn('Gauldin (2004)', amb['citations'])

    def test_prog_012_profile(self):
        p12 = get_progression('PROG-012')
        self.assertEqual(p12.archetype_family, 'FALLING_FIFTHS_SEQUENCE')
        profile = p12.theory_profile
        self.assertEqual(profile['functional_syntax'], 'vi - ii - V - I (Tp - Sp - D - T)')
        amb = profile['tonal_ambiguity']
        self.assertEqual(amb['cycle_type'], 'Descending Fifths / Quintfall')
        self.assertIn('Rameau (1722)', amb['citations'])
        self.assertIn('Salzer (1952)', amb['citations'])


class TestArchetypeDetection(unittest.TestCase):
    """Verifies intelligent recognition of exact archetypes and cyclic rotations."""

    def test_detect_prog_002_exact_and_axis_rotation(self):
        # Am - F - C - G: exactly PROG-002, also rotation offset 2 of PROG-001
        matches = detect_progression_archetypes(['Am', 'F', 'C', 'G'], allow_rotations=True)
        self.assertGreaterEqual(len(matches), 2)

        # First match must be PROG-002 exact match (score 1.0)
        top = matches[0]
        self.assertEqual(top['prog_id'], 'PROG-002')
        self.assertEqual(top['score'], 1.0)
        self.assertTrue(top['is_exact_match'])
        self.assertEqual(top['rotation_offset'], 0)

        # Must also identify as rotation of PROG-001 (score 0.90)
        prog1_match = next((m for m in matches if m['prog_id'] == 'PROG-001'), None)
        self.assertIsNotNone(prog1_match)
        self.assertEqual(prog1_match['rotation_offset'], 2)
        self.assertEqual(prog1_match['score'], 0.90)

    def test_detect_prog_004_doo_wop(self):
        # C - Am - F - G: exactly PROG-004
        matches = detect_progression_archetypes(['C', 'Am', 'F', 'G'])
        self.assertGreater(len(matches), 0)
        top = matches[0]
        self.assertEqual(top['prog_id'], 'PROG-004')
        self.assertEqual(top['score'], 1.0)
        self.assertTrue(top['is_exact_match'])

    def test_detect_prog_005_andalusian(self):
        # Am - G - F - E: exactly PROG-005
        matches = detect_progression_archetypes(['Am', 'G', 'F', 'E'])
        self.assertGreater(len(matches), 0)
        top = matches[0]
        self.assertEqual(top['prog_id'], 'PROG-005')
        self.assertEqual(top['score'], 1.0)
        self.assertTrue(top['is_exact_match'])
        self.assertEqual(top['family'], 'ANDALUSIAN_CADENCE_PHRYGIAN')

    def test_detect_prog_012_quintfall(self):
        # Am - Dm - G - C: exactly PROG-012
        matches = detect_progression_archetypes(['Am', 'Dm', 'G', 'C'])
        self.assertGreater(len(matches), 0)
        top = matches[0]
        self.assertEqual(top['prog_id'], 'PROG-012')
        self.assertEqual(top['score'], 1.0)
        self.assertTrue(top['is_exact_match'])

    def test_detect_transposed_archetype(self):
        # Transpose PROG-005 (Am - G - F - E) to Dm (Dm - C - Bb - A)
        matches = detect_progression_archetypes(['Dm', 'C', 'Bb', 'A'])
        top = matches[0]
        self.assertEqual(top['prog_id'], 'PROG-005')
        self.assertEqual(top['score'], 0.95)
        self.assertFalse(top['is_exact_key'])
        self.assertEqual(top['transposition_semitones'], 5)


class TestSessionArchetypeIntegration(unittest.TestCase):
    """Verifies ProgressionSession archetype identification and harmonic recommendations."""

    def test_session_identify_archetypes(self):
        session = ProgressionSession(initial_chords=['Am', 'F', 'C', 'G'])
        archetypes = session.identify_archetypes()
        self.assertGreater(len(archetypes), 0)
        self.assertEqual(archetypes[0]['prog_id'], 'PROG-002')

    def test_session_andalusian_phrygian_recommendation(self):
        # In A minor session, chord at index 0 is F (bVI)
        session = ProgressionSession(initial_chords=['F'], key_root='A', is_minor=True)
        recs = session.explore_next_chords(0)
        andalusian_rec = next((r for r in recs if 'Andalusische Kadenz' in r.explanation), None)
        self.assertIsNotNone(andalusian_rec)
        self.assertEqual(andalusian_rec.candidate_symbol, 'E')
        self.assertEqual(andalusian_rec.relation_type, 'RESOLVES_TO')

    def test_session_doo_wop_turnaround_recommendation(self):
        # In C major session, chord at index 0 is Am (vi)
        session = ProgressionSession(initial_chords=['Am'], key_root='C', is_minor=False)
        recs = session.explore_next_chords(0)
        doo_wop_rec = next((r for r in recs if '50s Doo-Wop' in r.explanation), None)
        self.assertIsNotNone(doo_wop_rec)
        self.assertEqual(doo_wop_rec.candidate_symbol, 'F')

    def test_session_dominant_tonic_resolution_recommendation(self):
        # In C major session, chord at index 0 is G (V)
        session = ProgressionSession(initial_chords=['G'], key_root='C', is_minor=False)
        recs = session.explore_next_chords(0)
        tonic_rec = next((r for r in recs if 'Mögliche Dominantauflösung' in r.explanation), None)
        self.assertIsNotNone(tonic_rec)
        self.assertEqual(tonic_rec.candidate_symbol, 'C')
        self.assertEqual(tonic_rec.relation_type, 'RESOLVES_TO')


if __name__ == '__main__':
    unittest.main()
