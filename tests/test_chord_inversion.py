"""
STEPS Theory Core: Chord Inversion & Figured Bass Verification Suite (OA-0025).

Validates:
- Precise bass-driven chord inversion detection (Aldwell & Schachter 1989, Kap. 4–5)
- Figured bass symbols (5/3, 6, 6/4, 7, 6/5, 4/3, 4/2)
- Resolution of ERR-006 (Correct distinction between root deduction and bass factor)
- Golden Cases: REF-0031 ([57, 60, 64] -> Grundstellung 5/3) and REF-0032
- Distinction between hand-voicing configuration and overall acoustic inversion
"""

import unittest

from src.steps.theory.inversion import (
    ChordInversion,
    FiguredBassSymbol,
    detect_chord_inversion,
    detect_hand_voicing,
    InversionAnalysis
)
from src.steps.theory.chord import Voicing
from src.steps.theory.exceptions import ChordConstructionError, VoiceLeadingError


class TestTriadInversion(unittest.TestCase):
    """Verifies inversion detection for major, minor, diminished, and augmented triads."""

    def test_ref_0031_a_minor_root_position(self):
        # A3 (57), C4 (60), E4 (64)
        result = detect_chord_inversion([57, 60, 64])
        self.assertEqual(result.inversion, ChordInversion.ROOT_POSITION)
        self.assertEqual(result.figured_bass, "5/3")
        self.assertEqual(result.bass_factor, "ROOT")
        self.assertEqual(result.root_pc, 9)  # A
        self.assertEqual(result.bass_pc, 9)  # A
        self.assertEqual(result.german_name, "Grundstellung (5/3)")
        self.assertFalse(result.is_seventh_chord)

    def test_ref_0032_a_minor_first_inversion(self):
        # C4 (60), E4 (64), A4 (69)
        result = detect_chord_inversion([60, 64, 69])
        self.assertEqual(result.inversion, ChordInversion.FIRST_INVERSION)
        self.assertEqual(result.figured_bass, "6")
        self.assertEqual(result.bass_factor, "THIRD")
        self.assertEqual(result.root_pc, 9)  # A
        self.assertEqual(result.bass_pc, 0)  # C
        self.assertEqual(result.german_name, "1. Umkehrung (Sextakkord 6)")

    def test_err_006_fix_f_major_over_a(self):
        # A3 (57), C4 (60), F4 (65) -> F major in 1st inversion (NOT Am(b6))
        result = detect_chord_inversion([57, 60, 65])
        self.assertEqual(result.inversion, ChordInversion.FIRST_INVERSION)
        self.assertEqual(result.figured_bass, "6")
        self.assertEqual(result.bass_factor, "THIRD")
        self.assertEqual(result.root_pc, 5)  # F
        self.assertEqual(result.bass_pc, 9)  # A (major 3rd of F)
        self.assertEqual(result.german_name, "1. Umkehrung (Sextakkord 6)")

    def test_triad_second_inversion(self):
        # E4 (64), A4 (69), C5 (72) -> Am in 2nd inversion (Quartsextakkord)
        result = detect_chord_inversion([64, 69, 72])
        self.assertEqual(result.inversion, ChordInversion.SECOND_INVERSION)
        self.assertEqual(result.figured_bass, "6/4")
        self.assertEqual(result.bass_factor, "FIFTH")
        self.assertEqual(result.root_pc, 9)  # A
        self.assertEqual(result.bass_pc, 4)  # E
        self.assertEqual(result.german_name, "2. Umkehrung (Quartsextakkord 6/4)")


class TestSeventhChordInversion(unittest.TestCase):
    """Verifies inversion detection for four-tone seventh chords."""

    def test_seventh_root_position(self):
        # C3 (48), E3 (52), G3 (55), Bb3 (58) -> C7 root position
        result = detect_chord_inversion([48, 52, 55, 58])
        self.assertEqual(result.inversion, ChordInversion.ROOT_POSITION)
        self.assertEqual(result.figured_bass, "7")
        self.assertEqual(result.bass_factor, "ROOT")
        self.assertEqual(result.german_name, "Grundstellung (7)")
        self.assertTrue(result.is_seventh_chord)

    def test_seventh_first_inversion(self):
        # E3 (52), G3 (55), Bb3 (58), C4 (60) -> C7 1st inversion (Quintsextakkord 6/5)
        result = detect_chord_inversion([52, 55, 58, 60])
        self.assertEqual(result.inversion, ChordInversion.FIRST_INVERSION)
        self.assertEqual(result.figured_bass, "6/5")
        self.assertEqual(result.bass_factor, "THIRD")
        self.assertEqual(result.german_name, "1. Umkehrung (Quintsextakkord 6/5)")

    def test_seventh_second_inversion(self):
        # G3 (55), Bb3 (58), C4 (60), E4 (64) -> C7 2nd inversion (Terzquartakkord 4/3)
        result = detect_chord_inversion([55, 58, 60, 64])
        self.assertEqual(result.inversion, ChordInversion.SECOND_INVERSION)
        self.assertEqual(result.figured_bass, "4/3")
        self.assertEqual(result.bass_factor, "FIFTH")
        self.assertEqual(result.german_name, "2. Umkehrung (Terzquartakkord 4/3)")

    def test_seventh_third_inversion(self):
        # Bb3 (58), C4 (60), E4 (64), G4 (67) -> C7 3rd inversion (Sekundakkord 4/2)
        result = detect_chord_inversion([58, 60, 64, 67])
        self.assertEqual(result.inversion, ChordInversion.THIRD_INVERSION)
        self.assertEqual(result.figured_bass, "4/2")
        self.assertEqual(result.bass_factor, "SEVENTH")
        self.assertEqual(result.german_name, "3. Umkehrung (Sekundakkord 4/2)")


class TestHandVoicingVsOverallInversion(unittest.TestCase):
    """Verifies distinction between hand-voicing configuration and overall acoustic inversion."""

    def test_pedal_bass_root_with_inverted_right_hand(self):
        # Left Hand: C2 (36)
        # Right Hand: E4 (64), G4 (67), C5 (72) -> 1st inversion C major in the hand
        analysis = detect_hand_voicing(
            hand_notes=[64, 67, 72],
            separate_bass_note=36,
            root_pitch_class=0  # C
        )
        self.assertTrue(analysis["is_hand_inverted"])
        self.assertEqual(analysis["hand_analysis"].inversion, ChordInversion.FIRST_INVERSION)
        self.assertEqual(analysis["hand_figured_bass"], "6")

        self.assertFalse(analysis["is_overall_inverted"])
        self.assertEqual(analysis["overall_analysis"].inversion, ChordInversion.ROOT_POSITION)
        self.assertEqual(analysis["overall_figured_bass"], "5/3")


class TestInversionInputValidation(unittest.TestCase):
    """Verifies error handling and data constraints."""

    def test_empty_chord_error(self):
        with self.assertRaises(ChordConstructionError):
            detect_chord_inversion([])

    def test_invalid_midi_note_error(self):
        with self.assertRaises(VoiceLeadingError):
            detect_chord_inversion([60, 64, 130])

    def test_explicit_triad_with_sixth_in_bass_is_not_a_third_inversion(self):
        result = detect_chord_inversion([45, 60, 64, 67], root_pitch_class=0, is_seventh=False)
        self.assertEqual((result.bass_factor, result.figured_bass), ("NON_CHORD_TONE", "slash"))
        self.assertFalse(result.is_seventh_chord)

    def test_suspension_in_the_bass_keeps_slash_notation_and_chord_membership(self):
        for notes, root in (([48, 55, 62, 65], 7), ([50, 60, 67], 0)):
            with self.subTest(notes=notes):
                result = detect_chord_inversion(notes, root_pitch_class=root)
                self.assertEqual((result.bass_factor, result.figured_bass), ("SUSPENSION", "slash"))

    def test_voicing_instance_compatibility(self):
        voicing = Voicing((57, 60, 64), 'CLOSE')
        result = detect_chord_inversion(voicing)
        self.assertEqual(result.inversion, ChordInversion.ROOT_POSITION)
        self.assertEqual(result.figured_bass, "5/3")


if __name__ == '__main__':
    unittest.main()
