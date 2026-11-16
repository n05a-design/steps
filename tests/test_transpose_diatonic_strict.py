"""Diatonische Transposition: Stufenzahl bestimmt Buchstabe und Oktave, ohne stille Umdeutung."""

import unittest

from src.steps.theory.exceptions import InvalidAlterationError
from src.steps.theory.pitch import DIATONIC_STEPS, NoteSpelling, parse_spelling


def diatonic_index(spelling):
    return spelling.octave * 7 + DIATONIC_STEPS.index(spelling.step)


class TransposeDiatonicStrictTest(unittest.TestCase):
    def test_inconsistent_step_and_semitone_deltas_raise(self):
        c4 = parse_spelling("C4", "INT")
        # Zuvor still umgedeutet: (0, 11) -> Cb5, (0, -11) -> C#3, (1, 13) -> Db5.
        for step_delta, semitone_delta in ((0, 11), (0, -11), (1, 13), (-1, -13), (4, 12), (6, 4)):
            with self.subTest(step_delta=step_delta, semitone_delta=semitone_delta):
                with self.assertRaises(InvalidAlterationError):
                    c4.transpose_diatonic(step_delta, semitone_delta)

    def test_enharmonic_edges_across_octave_boundary(self):
        cases = (
            ("B#3", 1, 1, "C#4", 61),   # übermäßige Prime -> kleine Sekunde über die Oktavgrenze
            ("Cb4", -1, -1, "Bb3", 58),
            ("B3", 1, 1, "C4", 60),
            ("C4", -1, -1, "B3", 59),
            ("Cb4", 0, 0, "Cb4", 59),
            ("C4", 8, 13, "Db5", 73),   # kleine None
            ("C4", 6, 9, "Bbb4", 69),   # verminderte Septime
            ("C4", 7, 11, "Cb5", 71),   # verminderte Oktave, ausdrücklich als Oktave angefragt
        )
        for start, step_delta, semitone_delta, expected, midi in cases:
            with self.subTest(start=start, step_delta=step_delta, semitone_delta=semitone_delta):
                result = parse_spelling(start, "INT").transpose_diatonic(step_delta, semitone_delta)
                self.assertEqual(result.render("INT"), expected)
                self.assertEqual(result.midi_number, midi)

    def test_result_keeps_requested_step_count_for_all_spellings(self):
        checked = 0
        for step in DIATONIC_STEPS:
            for alteration in (-2, -1, 0, 1, 2):
                start = NoteSpelling(step=step, alteration=alteration, octave=4)
                for step_delta in range(-14, 15):
                    for semitone_delta in range(-26, 27):
                        try:
                            result = start.transpose_diatonic(step_delta, semitone_delta)
                        except InvalidAlterationError:
                            continue
                        checked += 1
                        self.assertEqual(diatonic_index(result), diatonic_index(start) + step_delta)
                        self.assertEqual(result.midi_number, start.midi_number + semitone_delta)
                        self.assertIn(result.alteration, (-2, -1, 0, 1, 2))
        self.assertGreater(checked, 1000)


if __name__ == "__main__":
    unittest.main()
