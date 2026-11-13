"""Regression cases for the shared INT/DE notation contract."""

import unittest

from src.steps.progression import get_progression, list_progressions, resolve_roman_degree
from src.steps.theory import NoteSpelling, PitchClass, midi_to_frequency, parse_chord, parse_spelling
from src.steps.theory.exceptions import ChordConstructionError, MusicTheoryError, ProgressionParsingError


class TestNotationContract(unittest.TestCase):
    def test_b_requires_context(self):
        self.assertEqual(parse_spelling("B4", "DE").midi_number, 70)
        self.assertEqual(parse_spelling("B4", "INT").midi_number, 71)
        for token in ("B4", "b", "b-1"):
            with self.subTest(token=token), self.assertRaisesRegex(MusicTheoryError, "Ambiguous"):
                parse_spelling(token)
        with self.assertRaisesRegex(ProgressionParsingError, "Ambiguous"):
            resolve_roman_degree("I", "B")

    def test_chord_and_bass_share_a_convention(self):
        for symbol, canonical, bass in (
            ("Esmaj7/B", "Ebmaj7/Bb", 10),
            ("Hm7/B", "Bm7/Bb", 10),
            ("Bmaj7/H", "Bbmaj7/B", 11),
            ("Es", "Eb", None),
            ("Fis", "F#", None),
            ("Esus4", "Esus4", None),
            ("Asus2", "Asus2", None),
            ("B♭maj7", "Bbmaj7", None),
        ):
            with self.subTest(symbol=symbol):
                chord = parse_chord(symbol)
                self.assertEqual(chord.symbol, canonical)
                self.assertEqual(chord.bass.pitch_class if chord.bass else None, bass)
        for symbol in ("Bm7", "G/B", "Esmaj7/Bb", "C/E5", "CMmaj7", "CMMAJ7", None):
            with self.subTest(symbol=symbol), self.assertRaises(ChordConstructionError):
                parse_chord(symbol)
        self.assertEqual(parse_chord("Cmmaj7").quality, "m(maj7)")

    def test_roundtrip_and_invalid_aliases(self):
        for step in "CDEFGAB":
            for alteration in range(-2, 3):
                spelling = NoteSpelling(step, alteration, 4)
                for notation in ("INT", "DE"):
                    for unicode in (False, True):
                        written = spelling.render(notation, unicode_accidental=unicode)
                        self.assertEqual(parse_spelling(written, notation), spelling)
        for note in ("Bis4", "Bes4", "Hses4", "Ees4", "Aes4", "Cn4"):
            with self.subTest(note=note), self.assertRaises(MusicTheoryError):
                parse_spelling(note, "DE")
        self.assertEqual(NoteSpelling("C").render(unicode_accidental=True), "C4")

    def test_discrete_pitch_values_and_midi_boundaries(self):
        for call in (
            lambda: PitchClass(True),
            lambda: NoteSpelling("C", True),
            lambda: NoteSpelling("C", 1.0),
            lambda: NoteSpelling("C", 0, 4.5),
            lambda: parse_spelling(None),
            lambda: parse_spelling("C4", "FR"),
            lambda: NoteSpelling("C").render("FR"),
            lambda: midi_to_frequency(True),
            lambda: parse_spelling("C10").midi_number,
        ):
            with self.assertRaises(MusicTheoryError):
                call()
        self.assertEqual(parse_spelling("C-1").midi_number, 0)
        self.assertEqual(parse_spelling("G9").midi_number, 127)
        self.assertGreater(midi_to_frequency(69.5), 440)

    def test_roman_case_and_figure_roles(self):
        for token in ("iadd9", "ii13", "IVm", "Vb5", "V7sus4(65)"):
            with self.subTest(token=token), self.assertRaises(ProgressionParsingError):
                resolve_roman_degree(token)
        self.assertEqual(resolve_roman_degree("Iadd9(6)").symbol, "Cadd9/E")
        self.assertEqual(resolve_roman_degree("V7#11(42)").symbol, "G7(#11)/F")
        self.assertEqual(resolve_roman_degree("I+").symbol, "Caug")
        self.assertEqual(resolve_roman_degree("#vi°", "C", True, minor_accidentals="natural_minor").symbol, "Adim")
        self.assertEqual(resolve_roman_degree("bVI", "C", True).symbol, "Ab")

    def test_seventh_figures_reject_chords_without_sevenths(self):
        for degree in ("Iadd9(6/5)", "Iadd9(43)", "Iadd9(42)", "im6(65)"):
            with self.subTest(degree=degree), self.assertRaisesRegex(ProgressionParsingError, "requires a seventh"):
                resolve_roman_degree(degree, "C", convention="INT")
        for degree, expected in (
            ("Iadd9(6)", "Cadd9/E"),
            ("V7(43)", "G7/D"),
            ("V9(43)", "G9/D"),
            ("vii°7(42)", "Bdim7/Ab"),
        ):
            with self.subTest(degree=degree):
                self.assertEqual(resolve_roman_degree(degree, "C", convention="INT").symbol, expected)

    def test_transposition_preserves_the_catalog_spelling(self):
        letters = "CDEFGAB"
        for prog in list_progressions():
            original = prog.chord_definitions
            for offset in range(12):
                with self.subTest(progression=prog.prog_id, offset=offset):
                    shifted = prog.transpose(offset)
                    letter_shifts = set()
                    for old, new in zip(original, shifted, strict=True):
                        self.assertEqual(new.quality, old.quality)
                        pairs = [(old.root, new.root)]
                        if old.bass:
                            self.assertIsNotNone(new.bass)
                            pairs.append((old.bass, new.bass))
                        for before, after in pairs:
                            self.assertEqual(after.midi_number - before.midi_number, offset)
                            letter_shifts.add((letters.index(after.step) - letters.index(before.step)) % 7)
                    self.assertEqual(len(letter_shifts), 1)
        self.assertEqual([c.symbol for c in get_progression("PROG-001").transpose(8)], ["Ab", "Eb", "Fm", "Db"])
