"""
STEPS Progression Core: Contrapuntal Motion Classification & Voice-Leading Analysis (OA-0021).

Validates:
- Relative contrapuntal motion classification (CONTRARY, OBLIQUE, PARALLEL, SIMILAR, STATIC)
- Adherence to Fux (1725), Aldwell & Schachter (1989), and CLM-0051
- Pairwise contrapuntal analysis across multi-voice chords
- Integration with analyze_progression_voice_leading
"""

import unittest

from src.steps.progression.voice_leading import (
    ContrapuntalMotion,
    classify_voice_motion,
    analyze_contrapuntal_motions,
    VoiceLeadingStyle
)
from src.steps.progression.engine import (
    analyze_progression_voice_leading,
    get_progression,
    generate_progression_voicings
)
from src.steps.theory.chord import Voicing
from src.steps.theory.exceptions import VoiceLeadingError


class TestContrapuntalMotionClassification(unittest.TestCase):
    """Verifies pairwise voice motion classification against Fux & Aldwell/Schachter rules."""

    def test_contrary_motion(self):
        # Voice 1 ascends, Voice 2 descends
        self.assertEqual(classify_voice_motion(60, 64, 48, 45), ContrapuntalMotion.CONTRARY)
        # Voice 1 descends, Voice 2 ascends
        self.assertEqual(classify_voice_motion(67, 65, 36, 41), ContrapuntalMotion.CONTRARY)

    def test_oblique_motion(self):
        # Voice 1 stationary, Voice 2 moves
        self.assertEqual(classify_voice_motion(60, 60, 48, 52), ContrapuntalMotion.OBLIQUE)
        # Voice 1 moves, Voice 2 stationary
        self.assertEqual(classify_voice_motion(64, 62, 48, 48), ContrapuntalMotion.OBLIQUE)

    def test_parallel_motion(self):
        # Both ascend by +2 semitones
        self.assertEqual(classify_voice_motion(60, 62, 48, 50), ContrapuntalMotion.PARALLEL)
        # Both descend by -5 semitones (parallel fourths/fifths)
        self.assertEqual(classify_voice_motion(67, 62, 55, 50), ContrapuntalMotion.PARALLEL)

    def test_similar_motion(self):
        # Both ascend by different intervals (+4 and +2)
        self.assertEqual(classify_voice_motion(60, 64, 48, 50), ContrapuntalMotion.SIMILAR)
        # Both descend by different intervals (-2 and -4)
        self.assertEqual(classify_voice_motion(67, 65, 55, 51), ContrapuntalMotion.SIMILAR)

    def test_static_motion(self):
        # Neither voice moves
        self.assertEqual(classify_voice_motion(60, 60, 48, 48), ContrapuntalMotion.STATIC)

    def test_invalid_input_validation(self):
        with self.assertRaises(VoiceLeadingError):
            classify_voice_motion(-1, 60, 48, 50)
        with self.assertRaises(VoiceLeadingError):
            classify_voice_motion(60, 128, 48, 50)
        with self.assertRaises(VoiceLeadingError):
            classify_voice_motion(60, True, 48, 50)  # type: ignore[arg-type]


class TestAnalyzeContrapuntalMotions(unittest.TestCase):
    """Verifies multi-voice contrapuntal motion analysis between consecutive voicings."""

    def test_four_part_satb_transition(self):
        # C major root position: C3 (48), G3 (55), C4 (60), E4 (64)
        voicing_a = [48, 55, 60, 64]
        # A minor root position: A2 (45), A3 (57), C4 (60), E4 (64)
        # Bass: 48 -> 45 (-3)
        # Tenor: 55 -> 57 (+2)
        # Alto: 60 -> 60 (0)
        # Soprano: 64 -> 64 (0)
        voicing_b = [45, 57, 60, 64]

        result = analyze_contrapuntal_motions(voicing_a, voicing_b)

        # 4 voices -> 4 * 3 // 2 = 6 pairs
        self.assertEqual(result['total_voice_pairs'], 6)
        # Pairwise motions
        pw = result['pairwise_motions']
        # Bass (0) and Tenor (1): Bass down (-3), Tenor up (+2) -> CONTRARY
        self.assertEqual(pw[(0, 1)], ContrapuntalMotion.CONTRARY.value)
        # Bass (0) and Alto (2): Bass down (-3), Alto stationary (0) -> OBLIQUE
        self.assertEqual(pw[(0, 2)], ContrapuntalMotion.OBLIQUE.value)
        # Alto (2) and Soprano (3): both stationary (0) -> STATIC
        self.assertEqual(pw[(2, 3)], ContrapuntalMotion.STATIC.value)

        # Outer voice motion: Bass (0) vs Soprano (3) -> OBLIQUE (Bass moves, Soprano static)
        self.assertEqual(result['outer_voice_motion'], ContrapuntalMotion.OBLIQUE.value)
        self.assertGreater(result['motion_counts']['CONTRARY'], 0)

    def test_mismatched_voice_count_error(self):
        with self.assertRaises(VoiceLeadingError):
            analyze_contrapuntal_motions([48, 60, 64], [48, 60])

    def test_single_voice_error(self):
        with self.assertRaises(VoiceLeadingError):
            analyze_contrapuntal_motions([60], [62])


class TestProgressionVoiceLeadingIntegration(unittest.TestCase):
    """Verifies integration of contrapuntal motion with analyze_progression_voice_leading."""

    def test_canonical_progression_motion_distribution(self):
        prog = get_progression('PROG-003')  # Jazz ii-V-I
        voicings = generate_progression_voicings(prog.chord_definitions)
        analysis = analyze_progression_voice_leading(voicings, style=VoiceLeadingStyle.JAZZ_POP)

        self.assertIn('motion_distribution', analysis)
        self.assertIn('outer_voice_motions', analysis)
        self.assertEqual(len(analysis['outer_voice_motions']), analysis['transition_count'])
        for m_type in ContrapuntalMotion:
            self.assertIn(m_type.value, analysis['motion_distribution'])


if __name__ == '__main__':
    unittest.main()
