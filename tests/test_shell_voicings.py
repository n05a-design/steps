"""
Tests for the STEPS Shell-Voicing & Guide-Tone Engine (OA-0030, M04/M10, Modul P05).

Verifies:
- Guide-tone extraction (3rd & 7th) across chord qualities.
- Authentic two-handed realization of ii–V–I (PROG-003) adhering to Modul P05.
- Zero-jump voice leading with 1-semitone guide-tone downward resolutions (7 -> 3).
- Layout alternation ('7_3' <-> '3_7').
- German vs. international notation conventions (DE H vs. INT B).
- Support for Backdoor cadences (PROG-017), Pop loops (PROG-001), and CanonicalProgression objects.
"""

from __future__ import annotations

import unittest

from src.steps.progression.engine import get_progression
from src.steps.theory import (
    ChordConstructionError,
    ChordDefinition,
    GuideToneResolution,
    ProgressionParsingError,
    ProgressionShellVoicings,
    ShellVoicing,
    extract_guide_tone_pcs,
    generate_shell_voicings,
    parse_chord,
)


class TestShellVoicings(unittest.TestCase):
    def test_extract_guide_tone_pcs(self) -> None:
        """Verify 3rd and 7th pitch class extraction for standard jazz/pop chords."""
        # Dm7: Root D (2) -> 3rd F (5), 7th C (0)
        c_dm7 = parse_chord("Dm7")
        self.assertEqual(extract_guide_tone_pcs(c_dm7), (5, 0))

        # G7: Root G (7) -> 3rd B (11), 7th F (5)
        c_g7 = parse_chord("G7")
        self.assertEqual(extract_guide_tone_pcs(c_g7), (11, 5))

        # Cmaj7: Root C (0) -> 3rd E (4), 7th B (11)
        c_cmaj7 = parse_chord("Cmaj7")
        self.assertEqual(extract_guide_tone_pcs(c_cmaj7), (4, 11))

        # Fm7: Root F (5) -> 3rd Ab (8), 7th Eb (3)
        c_fm7 = parse_chord("Fm7")
        self.assertEqual(extract_guide_tone_pcs(c_fm7), (8, 3))

        # Bb7: Root Bb (10) -> 3rd D (2), 7th Ab (8)
        c_bb7 = parse_chord("Bb7")
        self.assertEqual(extract_guide_tone_pcs(c_bb7), (2, 8))

    def test_prog_003_p05_exact_alignment_layout_7_3(self) -> None:
        """
        Verify textbook realization of Modul P05 in PIANO_PRACTICE_REFERENCE_LIBRARY.md:
        - Dm7: LH D3 (50) | RH C4 (60) + F4 (65) [layout 7_3]
        - G7: LH G2 (43) | RH B3 (59) + F4 (65) [layout 3_7]
        - Cmaj7: LH C3 (48) | RH B3 (59) + E4 (64) [layout 7_3]
        """
        result = generate_shell_voicings(
            "Dm7 - G7 - Cmaj7",
            starting_layout="7_3",
            bass_octave=3,
            rh_octave=4,
            convention="INT",
        )

        self.assertEqual(len(result.voicings), 3)
        self.assertEqual(result.starting_layout, "7_3")
        self.assertEqual(result.total_l1_distance, 2)
        self.assertEqual(result.average_l1_distance, 1.0)

        # 1. Dm7
        v_dm7 = result.voicings[0]
        self.assertEqual(v_dm7.chord_symbol, "Dm7")
        self.assertEqual(v_dm7.bass_note, 50)  # D3
        self.assertEqual(v_dm7.lh_spelling, "D3")
        self.assertEqual(v_dm7.guide_tones, (60, 65))  # C4, F4
        self.assertEqual(v_dm7.rh_spellings, ("C4", "F4"))
        self.assertEqual(v_dm7.layout, "7_3")
        self.assertEqual(v_dm7.rh_span, 5)  # Perfect fourth
        self.assertTrue(v_dm7.is_seventh_below_third)

        # 2. G7
        v_g7 = result.voicings[1]
        self.assertEqual(v_g7.chord_symbol, "G7")
        self.assertEqual(v_g7.bass_note, 43)  # G2
        self.assertEqual(v_g7.lh_spelling, "G2")
        self.assertEqual(v_g7.guide_tones, (59, 65))  # B3, F4
        self.assertEqual(v_g7.rh_spellings, ("B3", "F4"))
        self.assertEqual(v_g7.layout, "3_7")
        self.assertEqual(v_g7.rh_span, 6)  # Tritone
        self.assertFalse(v_g7.is_seventh_below_third)

        # 3. Cmaj7
        v_cmaj7 = result.voicings[2]
        self.assertEqual(v_cmaj7.chord_symbol, "Cmaj7")
        self.assertEqual(v_cmaj7.bass_note, 48)  # C3
        self.assertEqual(v_cmaj7.lh_spelling, "C3")
        self.assertEqual(v_cmaj7.guide_tones, (59, 64))  # B3, E4
        self.assertEqual(v_cmaj7.rh_spellings, ("B3", "E4"))
        self.assertEqual(v_cmaj7.layout, "7_3")
        self.assertEqual(v_cmaj7.rh_span, 5)  # Perfect fourth
        self.assertTrue(v_cmaj7.is_seventh_below_third)

        # Resolutions
        self.assertEqual(len(result.resolutions), 2)

        # Transition 1: Dm7 -> G7
        res1 = result.resolutions[0]
        self.assertEqual(res1.from_chord, "Dm7")
        self.assertEqual(res1.to_chord, "G7")
        self.assertEqual(res1.retained_note, 65)  # F4 held
        self.assertEqual(res1.moving_note_from, 60)  # C4
        self.assertEqual(res1.moving_note_to, 59)  # B3
        self.assertEqual(res1.motion_semitones, -1)  # Half step down!
        self.assertEqual(res1.resolution_type, "HALF_STEP_DOWN")
        self.assertEqual(res1.total_l1_distance, 1)

        # Transition 2: G7 -> Cmaj7
        res2 = result.resolutions[1]
        self.assertEqual(res2.from_chord, "G7")
        self.assertEqual(res2.to_chord, "Cmaj7")
        self.assertEqual(res2.retained_note, 59)  # B3 held
        self.assertEqual(res2.moving_note_from, 65)  # F4
        self.assertEqual(res2.moving_note_to, 64)  # E4
        self.assertEqual(res2.motion_semitones, -1)  # Half step down!
        self.assertEqual(res2.resolution_type, "HALF_STEP_DOWN")
        self.assertEqual(res2.total_l1_distance, 1)

    def test_prog_003_layout_3_7_alternative(self) -> None:
        """
        Verify alternative starting layout 3_7:
        - Dm7: RH F4 (65) + C5 (72) [layout 3_7]
        - G7: RH F4 (65) + B4 (71) [layout 7_3] (C5 -> B4, F4 held)
        - Cmaj7: RH E4 (64) + B4 (71) [layout 3_7] (F4 -> E4, B4 held)
        """
        result = generate_shell_voicings(
            "Dm7 - G7 - Cmaj7",
            starting_layout="3_7",
            bass_octave=3,
            rh_octave=4,
            convention="INT",
        )

        self.assertEqual(result.starting_layout, "3_7")
        self.assertEqual(result.total_l1_distance, 2)
        self.assertEqual(result.average_l1_distance, 1.0)

        self.assertEqual(result.voicings[0].guide_tones, (65, 72))  # F4, C5
        self.assertEqual(result.voicings[0].layout, "3_7")

        self.assertEqual(result.voicings[1].guide_tones, (65, 71))  # F4, B4
        self.assertEqual(result.voicings[1].layout, "7_3")

        self.assertEqual(result.voicings[2].guide_tones, (64, 71))  # E4, B4
        self.assertEqual(result.voicings[2].layout, "3_7")

    def test_german_convention_spelling(self) -> None:
        """Verify that convention='DE' renders B as H in SPN."""
        result = generate_shell_voicings(
            "Dm7 - G7 - Cmaj7",
            starting_layout="7_3",
            bass_octave=3,
            convention="DE",
        )
        self.assertEqual(result.voicings[1].rh_spellings, ("H3", "F4"))
        self.assertEqual(result.voicings[2].rh_spellings, ("H3", "E4"))

    def test_prog_017_backdoor_cadence(self) -> None:
        """Verify smooth guide tone voice leading on the Backdoor cadence (PROG-017)."""
        result = generate_shell_voicings("Fm7 - Bb7 - Cmaj7", starting_layout="7_3")
        self.assertEqual(len(result.voicings), 3)

        # Fm7 -> Bb7 retains Ab4 (68) and moves Eb4 (63) down to D4 (62)
        res1 = result.resolutions[0]
        self.assertEqual(res1.from_chord, "Fm7")
        self.assertEqual(res1.to_chord, "Bb7")
        self.assertEqual(res1.motion_semitones, -1)
        self.assertEqual(res1.resolution_type, "HALF_STEP_DOWN")
        self.assertEqual(res1.total_l1_distance, 1)

    def test_canonical_progression_input(self) -> None:
        """Verify passing a CanonicalProgression object directly."""
        prog = get_progression("PROG-003")
        result = generate_shell_voicings(prog)
        self.assertEqual(len(result.voicings), 3)
        self.assertEqual(result.voicings[0].chord_symbol, "Dm7")
        self.assertEqual(result.voicings[1].chord_symbol, "G7")
        self.assertEqual(result.voicings[2].chord_symbol, "Cmaj7")

    def test_auto_layout_selection(self) -> None:
        """Verify AUTO chooses the layout with minimal L1 distance."""
        result = generate_shell_voicings("Dm7 - G7 - Cmaj7", starting_layout="AUTO")
        self.assertIn(result.starting_layout, ("7_3", "3_7"))
        self.assertEqual(result.total_l1_distance, 2)

    def test_serialization_to_dict(self) -> None:
        """Verify ShellVoicing.to_dict format."""
        result = generate_shell_voicings("Dm7 - G7 - Cmaj7")
        d = result.voicings[0].to_dict()
        self.assertIn("chord_symbol", d)
        self.assertIn("bass_note", d)
        self.assertIn("lh_spelling", d)
        self.assertIn("guide_tones", d)
        self.assertIn("rh_spellings", d)
        self.assertIn("layout", d)
        self.assertIn("rh_span", d)

    def test_pop_four_chords_progression(self) -> None:
        """Verify shell voicing generation on Pop Four Chords (C - G - Am - F)."""
        result = generate_shell_voicings("C - G - Am - F")
        self.assertEqual(len(result.voicings), 4)
        self.assertLessEqual(result.average_l1_distance, 5.0)
        for v in result.voicings:
            self.assertGreater(v.rh_span, 0)
            self.assertGreater(v.guide_tones[0], v.bass_note)

    def test_empty_and_invalid_inputs(self) -> None:
        """Verify graceful handling of empty lists and invalid chords."""
        empty_res = generate_shell_voicings([])
        self.assertEqual(len(empty_res.voicings), 0)
        self.assertEqual(empty_res.total_l1_distance, 0)

        with self.assertRaises(Exception):
            generate_shell_voicings("INVALID_CHORD_XYZ")


if __name__ == "__main__":
    unittest.main()
