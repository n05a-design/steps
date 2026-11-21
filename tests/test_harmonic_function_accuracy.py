"""Music audit regressions for session labels and explorer preconditions."""

import unittest

from src.steps.progression.session import ProgressionSession


class TestHarmonicFunctionAccuracy(unittest.TestCase):
    def test_degrees_show_quality_spelling_bass_and_local_resolution(self):
        chords = [
            "Cmaj7", "E7", "Am", "C/E", "Ddim", "Db", "F#", "Gb",
            "Dm7", "G7/F", "C", "C/F#", "Cmaj9/E",
        ]
        session = ProgressionSession(initial_chords=chords)
        analysis = session.analyze_progression()
        self.assertEqual(
            [item.roman_numeral for item in analysis],
            ["Imaj7", "V7/vi", "vi", "I6", "ii°", "bII", "#IV", "bV",
             "ii7", "V7(42)", "I", "I/F#", "Imaj9/E"],
        )

        self.assertEqual(
            [session.harmonic_degree_at(i) for i in range(len(chords))],
            [item.roman_numeral for item in analysis],
        )

    def test_chord_pairs_keep_regular_labels_without_applied_dominant_evidence(self):
        for chords, expected in (
            (["C", "F", "G", "C"], ["I", "IV", "V", "I"]),
            (["E7", "F", "Am"], ["V7", "VI", "i"]),
            (["G", "C", "Bm7b5"], ["VII", "III", "iiø7"]),
        ):
            key = "C" if chords[0] == "C" else "A"
            with self.subTest(chords=chords):
                analysis = ProgressionSession(
                    initial_chords=chords, key_root=key, is_minor=key == "A",
                ).analyze_progression()
                self.assertEqual([item.roman_numeral for item in analysis], expected)

    def test_degrees_preserve_german_b_h_and_keep_foreign_bass_explicit(self):
        session = ProgressionSession(
            initial_chords=["H7/Dis", "Em", "B", "C/Fis"], key_root="C", convention="DE",
        )
        labels = [item.roman_numeral for item in session.analyze_progression()]
        self.assertEqual(labels, ["V7(65)/iii", "iii", "bVII", "I/Fis"])

    def test_minor_quality_and_extensions_gate_style_explanations(self):
        for chord, minor, forbidden_framework in (
            ("Gm", True, "Minor Jazz Blues Submediant Turnaround"),
            ("Gm", True, "Jazz ii–V–I"),
            ("F", True, "Minor Jazz Blues Submediant Turnaround"),
            ("Ab", True, "Minor Jazz Blues Submediant Turnaround"),
            ("Dbmaj7", False, "Extended Tritone Sub (Altered)"),
            ("Bb", False, "Backdoor Progression"),
            ("A7", False, "Doo-Wop Turnaround"),
        ):
            with self.subTest(chord=chord, minor=minor):
                options = ProgressionSession(
                    initial_chords=[chord], key_root="C", is_minor=minor,
                ).explore_next_chords(0)
                self.assertNotIn(forbidden_framework, [r.framework for r in options])

    def test_fifth_and_slash_bass_are_not_confused_with_voice_motion_or_cadence(self):
        for chord, target, interval in (("Gm", "C", "Quintfall"), ("C/G", "Dm", "Ganzton")):
            with self.subTest(chord=chord):
                options = ProgressionSession(
                    initial_chords=[chord], key_root="C",
                ).explore_next_chords(0)
                matching = [r for r in options if r.candidate_symbol == target]
                self.assertTrue(matching)
                self.assertTrue(all(r.relation_type == "ROOT_MOTION" for r in matching))
                self.assertTrue(all(interval in r.explanation for r in matching))
                self.assertTrue(all("Bass" not in r.explanation for r in matching))

    def test_explorer_models_real_dominant_targets_and_jazz_pairs(self):
        for notation, key, minor, chords in (
            ("INT", "C", False, ("Dm7", "G7", "Cmaj7")),
            ("INT", "C", True, ("Dm7b5", "G7", "Cm7")),
            ("DE", "H", False, ("Cism7", "Fis7", "Hmaj7")),
            ("DE", "B", True, ("Cm7b5", "F7", "Bm7")),
        ):
            with self.subTest(chords=chords):
                session = ProgressionSession(
                    initial_chords=list(chords), key_root=key, is_minor=minor, convention=notation,
                )
                for index, target in enumerate(chords[1:]):
                    self.assertTrue(any(
                        item.candidate_symbol == target and item.source_id == "omt-ii-v-i"
                        for item in session.explore_next_chords(index)
                    ))
        for key, chord, target, minor in (("A", "E", "Am", True), ("C", "E7", "Am", False)):
            with self.subTest(key=key, chord=chord):
                options = ProgressionSession(
                    initial_chords=[chord], key_root=key, is_minor=minor,
                ).explore_next_chords(0)
                self.assertTrue(any(
                    item.candidate_symbol == target and item.relation_type == "RESOLVES_TO"
                    for item in options
                ))

    def test_double_dominant_description_targets_dominant(self):
        options = ProgressionSession(initial_chords=["C"], key_root="C").explore_next_chords(0)
        double_dominant = next(item for item in options if "Doppeldominante" in item.explanation)
        self.assertEqual(double_dominant.candidate_symbol, "D7")
        self.assertIn("Stufe V", double_dominant.explanation)
