"""Regression checks for musical layout, voice identity and interval limits."""

import unittest

from src.steps.progression import analyze_progression_voice_leading
from src.steps.progression.voice_leading import VoiceLeadingStyle, detect_parallel_fifths_octaves, detect_voice_crossing
from src.steps.theory import (
    CHORD_TEMPLATES, DiatonicInterval, Voicing, interval_between_spellings,
    make_drop2_voicing, parse_chord, parse_spelling,
)
from src.steps.theory.exceptions import InvalidIntervalError, MusicTheoryError


class TestVoicingContract(unittest.TestCase):
    def test_layouts_use_explicit_reductions(self):
        with self.assertRaises(MusicTheoryError):
            parse_chord("C").to_voicing(voicing_type="DROP2")
        self.assertEqual(set(n % 12 for n in parse_chord("C13").to_voicing(voicing_type="DROP2").notes), {0, 4, 9, 10})
        self.assertEqual(set(n % 12 for n in parse_chord("C6").to_voicing(voicing_type="SHELL").notes), {0, 4, 9})
        chord = parse_chord("C7")
        a = chord.to_voicing(3, "ROOTLESS")
        b = chord.to_voicing(4, "ROOTLESS")
        self.assertEqual(b.notes, tuple(n + 12 for n in a.notes))
        slash = parse_chord("C7/C").to_voicing(voicing_type="ROOTLESS")
        self.assertEqual([n % 12 for n in slash.notes].count(0), 1)
        self.assertEqual(slash.bass_note % 12, 0)
        self.assertEqual(make_drop2_voicing([62, 65, 69, 72]), [57, 62, 65, 72])

    def test_layouts_across_register_boundaries(self):
        roots = ("C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B")
        for root in roots:
            for quality in CHORD_TEMPLATES:
                chord = parse_chord(root + quality, "INT")
                voiced_pcs = {int(pc) for pc in chord.voiced_pitch_classes}
                for layout in ("CLOSE", "DROP2", "SHELL", "ROOTLESS"):
                    for octave in range(-1, 10):
                        with self.subTest(root=root, quality=quality, layout=layout, octave=octave):
                            try:
                                voicing = chord.to_voicing(octave, layout)
                            except MusicTheoryError:
                                if layout == "CLOSE":
                                    highest = 12 * (octave + 1) + chord.root.pitch_class + max(
                                        chord.default_voiced_intervals
                                    )
                                    self.assertGreater(highest, 127)
                                else:
                                    self.assertTrue(
                                        (layout == "DROP2" and len(voiced_pcs) < 4) or octave in (-1, 8, 9)
                                    )
                                continue
                            self.assertEqual(voicing.voicing_type, layout)
                            self.assertTrue(all(0 <= note <= 127 for note in voicing.notes))
                            self.assertEqual(list(voicing.notes), sorted(set(voicing.notes)))
                            pitch_classes = {note % 12 for note in voicing.notes}
                            self.assertLessEqual(pitch_classes, chord.pitch_class_set)
                            if layout == "ROOTLESS":
                                self.assertEqual(pitch_classes, voiced_pcs - {chord.root.pitch_class})
                            elif layout in ("CLOSE", "SHELL"):
                                self.assertEqual(voicing.bass_note % 12, chord.root.pitch_class)
                                if layout == "CLOSE":
                                    self.assertEqual(pitch_classes, voiced_pcs)
                            else:
                                self.assertEqual(len(voicing.notes), 4)

    def test_shell_and_slash_bass_keep_their_musical_roles(self):
        for symbol, layout, expected in (
            ("Cadd9/E", "SHELL", [52, 67]),
            ("F#7/E", "SHELL", [52, 70]),
            ("Ebmaj7/Bb", "DROP2", [58, 63, 67, 74]),
            ("C7/F#", "CLOSE", [54, 55, 58, 60, 64]),
            ("Dm9/F", "ROOTLESS", [53, 60, 64]),
        ):
            with self.subTest(symbol=symbol, layout=layout):
                self.assertEqual(parse_chord(symbol, "INT").to_voicing(3, layout).midi_notes, expected)

    def test_voicing_is_immutable_and_discrete_operations_reject_nonintegers(self):
        notes = [64, 60, 67]
        voicing = Voicing(notes)
        notes[0] = 200
        self.assertEqual(voicing.notes, (64, 60, 67))
        self.assertEqual(hash(voicing), hash(Voicing((64, 60, 67))))
        pitch = parse_spelling("C4", "INT")
        for value in (True, 1.0, "1", None):
            for operation in (
                voicing.transpose, voicing.invert, pitch.transpose_chromatic,
                lambda value: pitch.transpose_diatonic(value, 1),
                lambda value: pitch.transpose_diatonic(1, value),
            ):
                with self.subTest(value=value, operation=operation), self.assertRaises(MusicTheoryError):
                    operation(value)
        for value in (False, 0.0):
            with self.assertRaises(MusicTheoryError):
                Voicing((0, 4, 7), bass_override=value)

    def test_voice_identity_and_stable_result(self):
        a = Voicing((64, 60, 67))
        b = Voicing((60, 64, 67))
        empty = analyze_progression_voice_leading([])
        one = analyze_progression_voice_leading([a])
        two = analyze_progression_voice_leading([a, b])
        self.assertEqual(empty.keys(), one.keys())
        self.assertEqual(one.keys(), two.keys())
        self.assertEqual(one["voice_crossings_count"], 1)
        self.assertEqual(two["total_l1_distance"], 8)
        self.assertFalse(detect_voice_crossing([60, 60]))
        self.assertTrue(detect_parallel_fifths_octaves([48, 67], [53, 60]))
        self.assertFalse(detect_parallel_fifths_octaves([48, 67], [53, 60], VoiceLeadingStyle.JAZZ_POP))

    def test_interval_validation_and_enharmonic_direction(self):
        for args in ((1, "d"), (2, "dd"), (2.5, "M"), (2, "X"), (2, "M", True)):
            with self.assertRaises(InvalidIntervalError):
                DiatonicInterval(*args)
        with self.assertRaises(InvalidIntervalError):
            DiatonicInterval(8, "A").invert()
        a, b = (parse_spelling(s, "INT") for s in ("C4", "B#3"))
        self.assertEqual(interval_between_spellings(a, b), DiatonicInterval(2, "d", -1))
        self.assertEqual(interval_between_spellings(b, a), DiatonicInterval(2, "d"))
        self.assertEqual(interval_between_spellings(a, parse_spelling("Gbb4")), DiatonicInterval(5, "dd"))
