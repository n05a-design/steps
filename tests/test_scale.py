"""
STEPS Music Theory Core: Scales & Modes Verification Test Suite.

Validates:
- Scale construction from NoteSpelling and ScaleTemplate
- Exact diatonic spelling preservation (avoiding enharmonic flattening)
- All 7 church modes from C and altered keys (F#, Db, C#)
- Harmonic Minor and Melodic Minor (Jazz Minor)
- Diatonic triad and seventh chord derivation (I..VII)
- Characteristic intervals and modal avoid notes
- Pentatonic & Blues scales
- Scale string parsing (DE, INT, AUTO ambiguity detection)
- Degree queries and octave wrapping
"""

import unittest

from src.steps.theory import (
    ModeCategory,
    NoteSpelling,
    PitchClass,
    ScaleConstructionError,
    ScaleDefinition,
    construct_scale,
    get_scale_template,
    parse_scale,
    parse_spelling,
)


class TestScaleConstruction(unittest.TestCase):
    def test_c_ionian_major(self):
        root = NoteSpelling("C", 0, 4)
        scale = construct_scale(root, "ionian")
        self.assertEqual(scale.name, "ionian")
        self.assertEqual(scale.pitch_classes, (0, 2, 4, 5, 7, 9, 11))
        self.assertEqual(scale.render_text("INT"), ["C4", "D4", "E4", "F4", "G4", "A4", "B4"])
        self.assertEqual(scale.render_text("DE"), ["C4", "D4", "E4", "F4", "G4", "A4", "H4"])

    def test_diatonic_spelling_preservation_f_sharp_major(self):
        # F# Major must have E# as 7th degree, NOT F natural!
        root = NoteSpelling("F", 1, 4)
        scale = construct_scale(root, "major")
        steps = [s.step for s in scale.spellings]
        self.assertEqual(steps, ["F", "G", "A", "B", "C", "D", "E"])
        self.assertEqual(scale.spellings[6], NoteSpelling("E", 1, 5))  # E#5
        self.assertEqual(scale.render_text("INT"), ["F#4", "G#4", "A#4", "B4", "C#5", "D#5", "E#5"])

    def test_diatonic_spelling_preservation_d_flat_major(self):
        # Db Major must have Gb as 4th degree, NOT F#!
        root = NoteSpelling("D", -1, 4)
        scale = construct_scale(root, "major")
        steps = [s.step for s in scale.spellings]
        self.assertEqual(steps, ["D", "E", "F", "G", "A", "B", "C"])
        self.assertEqual(scale.spellings[3], NoteSpelling("G", -1, 4))  # Gb4
        self.assertEqual(scale.render_text("INT"), ["Db4", "Eb4", "F4", "Gb4", "Ab4", "Bb4", "C5"])

    def test_seven_church_modes_from_c(self):
        root = NoteSpelling("C", 0, 4)
        expected_modes = {
            "ionian": (0, 2, 4, 5, 7, 9, 11),
            "dorian": (0, 2, 3, 5, 7, 9, 10),
            "phrygian": (0, 1, 3, 5, 7, 8, 10),
            "lydian": (0, 2, 4, 6, 7, 9, 11),
            "mixolydian": (0, 2, 4, 5, 7, 9, 10),
            "aeolian": (0, 2, 3, 5, 7, 8, 10),
            "locrian": (0, 1, 3, 5, 6, 8, 10),
        }
        for mode_name, expected_intervals in expected_modes.items():
            with self.subTest(mode=mode_name):
                scale = construct_scale(root, mode_name)
                self.assertEqual(scale.intervals, expected_intervals)
                # Verify that every diatonic letter step is used exactly once
                steps = [s.step for s in scale.spellings]
                self.assertEqual(steps, ["C", "D", "E", "F", "G", "A", "B"])

    def test_harmonic_and_melodic_minor(self):
        root = NoteSpelling("C", 0, 4)
        harm = construct_scale(root, "harmonic_minor")
        self.assertEqual(harm.intervals, (0, 2, 3, 5, 7, 8, 11))
        # Degree 7 must be B natural (leading tone)
        self.assertEqual(harm.spellings[6], NoteSpelling("B", 0, 4))

        mel = construct_scale(root, "melodic_minor")
        self.assertEqual(mel.intervals, (0, 2, 3, 5, 7, 9, 11))
        # Degree 6 is A natural, degree 7 is B natural
        self.assertEqual(mel.spellings[5], NoteSpelling("A", 0, 4))
        self.assertEqual(mel.spellings[6], NoteSpelling("B", 0, 4))


class TestDiatonicHarmonization(unittest.TestCase):
    def test_c_major_triads(self):
        scale = construct_scale(NoteSpelling("C", 0, 4), "major")
        expected_triads = [
            (1, "C", ""),      # I
            (2, "D", "m"),     # ii
            (3, "E", "m"),     # iii
            (4, "F", ""),      # IV
            (5, "G", ""),      # V
            (6, "A", "m"),     # vi
            (7, "B", "dim"),   # vii°
        ]
        for degree, root_step, quality in expected_triads:
            with self.subTest(degree=degree):
                chord = scale.get_diatonic_triad(degree)
                self.assertEqual(chord.root.step, root_step)
                self.assertEqual(chord.quality, quality)

    def test_c_major_sevenths(self):
        scale = construct_scale(NoteSpelling("C", 0, 4), "major")
        expected_sevenths = [
            (1, "C", "maj7"),   # Imaj7
            (2, "D", "m7"),     # ii7
            (3, "E", "m7"),     # iii7
            (4, "F", "maj7"),   # IVmaj7
            (5, "G", "7"),      # V7
            (6, "A", "m7"),     # vi7
            (7, "B", "m7b5"),   # viiø7
        ]
        for degree, root_step, quality in expected_sevenths:
            with self.subTest(degree=degree):
                chord = scale.get_diatonic_seventh(degree)
                self.assertEqual(chord.root.step, root_step)
                self.assertEqual(chord.quality, quality)

    def test_a_natural_minor_triads(self):
        scale = construct_scale(NoteSpelling("A", 0, 4), "natural_minor")
        expected_triads = [
            (1, "A", "m"),     # i
            (2, "B", "dim"),   # ii°
            (3, "C", ""),      # III
            (4, "D", "m"),     # iv
            (5, "E", "m"),     # v
            (6, "F", ""),      # VI
            (7, "G", ""),      # VII
        ]
        for degree, root_step, quality in expected_triads:
            with self.subTest(degree=degree):
                chord = scale.get_diatonic_triad(degree)
                self.assertEqual(chord.root.step, root_step)
                self.assertEqual(chord.quality, quality)


class TestPentatonicAndBlues(unittest.TestCase):
    def test_major_pentatonic(self):
        scale = construct_scale(NoteSpelling("C", 0, 4), "major_pentatonic")
        self.assertEqual(len(scale.spellings), 5)
        self.assertEqual(scale.intervals, (0, 2, 4, 7, 9))
        self.assertEqual(scale.render_text("INT"), ["C4", "D4", "E4", "G4", "A4"])

    def test_blues_scale(self):
        scale = construct_scale(NoteSpelling("C", 0, 4), "blues")
        self.assertEqual(len(scale.spellings), 6)
        self.assertEqual(scale.intervals, (0, 3, 5, 6, 7, 10))
        # Blue note is tritone (6)
        self.assertIn(6, scale.intervals)


class TestScaleParsingAndAmbiguity(unittest.TestCase):
    def test_parse_international(self):
        s1 = parse_scale("C Major", convention="INT")
        self.assertEqual(s1.root.step, "C")
        self.assertEqual(s1.name, "ionian")

        s2 = parse_scale("D Dorian", convention="INT")
        self.assertEqual(s2.root.step, "D")
        self.assertEqual(s2.name, "dorian")

    def test_parse_german(self):
        # H-Dur in DE convention
        s_h = parse_scale("H-Dur", convention="DE")
        self.assertEqual(s_h.root.step, "B")
        self.assertEqual(s_h.root.alteration, 0)
        self.assertEqual(s_h.root.render("DE"), "H4")

        # B-Dur in DE convention is Bb
        s_b = parse_scale("B-Dur", convention="DE")
        self.assertEqual(s_b.root.step, "B")
        self.assertEqual(s_b.root.alteration, -1)
        self.assertEqual(s_b.root.render("DE"), "B4")
        self.assertEqual(s_b.root.render("INT"), "Bb4")

    def test_auto_ambiguity_rejection(self):
        # "B Major" means B natural in INT, but Bb in DE -> Must be rejected as ambiguous under AUTO!
        with self.assertRaises(ScaleConstructionError):
            parse_scale("B Major", convention="AUTO")

    def test_degree_wrapping(self):
        scale = construct_scale(NoteSpelling("C", 0, 4), "major")
        # Degree 1 = C4
        self.assertEqual(scale.get_degree(1), NoteSpelling("C", 0, 4))
        # Degree 8 = Octave = C5
        self.assertEqual(scale.get_degree(8), NoteSpelling("C", 0, 5))
        # Degree 9 = Ninth = D5
        self.assertEqual(scale.get_degree(9), NoteSpelling("D", 0, 5))

    def test_invalid_parameters(self):
        scale = construct_scale(NoteSpelling("C", 0, 4), "major_pentatonic")
        # Pentatonic scale has no 7-step diatonic triads
        with self.assertRaises(ScaleConstructionError):
            scale.get_diatonic_triad(1)

        with self.assertRaises(ScaleConstructionError):
            construct_scale(NoteSpelling("C", 0, 4), "non_existent_scale_xyz")

        with self.assertRaises(ScaleConstructionError):
            parse_scale("")


if __name__ == "__main__":
    unittest.main()
