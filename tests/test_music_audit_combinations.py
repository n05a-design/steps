"""Independent combinatorial witnesses for recognition and harmonic results."""

from itertools import product
from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from src.steps.keyboard.recognition import CandidateKind, recognize_chord
from src.steps.keyboard.practice import evaluate, pilot_exercises
from src.steps.midi import SMFParser
from src.steps.progression import ProgressionSession
from src.steps.theory.chord import parse_chord
from src.steps.theory.exceptions import ChordConstructionError


class MusicalCombinationAudit(unittest.TestCase):
    def test_recognition_omissions_with_bass_register_and_policy(self):
        # The exact reference recipes and permitted omitted fifths are independent
        # of the production chord dictionary. Check a candidate without requiring
        # the surrounding pitch set to have a single harmonic interpretation.
        recipes = (
            ("7", (0, 4, 7, 10), CandidateKind.INCOMPLETE),
            ("maj7", (0, 4, 7, 11), CandidateKind.INCOMPLETE),
            ("9", (0, 4, 7, 10, 2), CandidateKind.STANDARD_VOICING),
            ("7#9", (0, 4, 7, 10, 3), CandidateKind.STANDARD_VOICING),
            ("7#11", (0, 4, 7, 10, 6), CandidateKind.STANDARD_VOICING),
        )
        for (quality, factors, fifth_omission), root, incomplete in product(recipes, range(12), (False, True)):
            for omitted in (None, *factors):
                played = {(root + factor) % 12 for factor in factors if factor != omitted}
                for bass, lower_octave in product(sorted(played), (36, 48)):
                    notes = [72 + pc for pc in sorted(played - {bass}, reverse=True)] + [lower_octave + bass]
                    result = recognize_chord(notes, allow_incomplete=incomplete)
                    candidate = next((c for c in result.candidates
                                      if int(c.chord.root.pitch_class) == root and c.chord.quality == quality), None)
                    with self.subTest(quality=quality, root=root, omitted=omitted, bass=bass,
                                      lower_octave=lower_octave, incomplete=incomplete):
                        expected = (CandidateKind.EXACT if omitted is None else fifth_omission
                                    if omitted == 7 and (incomplete or fifth_omission is CandidateKind.STANDARD_VOICING)
                                    else None)
                        self.assertEqual(candidate.kind if candidate else None, expected)
                        if candidate:
                            self.assertEqual(int((candidate.chord.bass or candidate.chord.root).pitch_class), bass)
                            self.assertEqual([role.value for role in candidate.missing_roles],
                                             [] if omitted is None else ["PERFECT_FIFTH"])

    def test_altered_standard_voicing_keeps_its_named_tension(self):
        for suffix, factors in (("7#9", {0, 3, 4, 10}), ("7#11", {0, 4, 6, 10})):
            for root, pitch in (("C", 0), ("Db", 1), ("F#", 6), ("Bb", 10)):
                with self.subTest(root=root, quality=suffix):
                    voicing = parse_chord(root + suffix, "INT").to_voicing()
                    self.assertEqual({note % 12 for note in voicing.notes}, {(pitch + factor) % 12 for factor in factors})

    def test_practice_register_bass_and_publication_boundary(self):
        exercises = {case.exercise_id: case for case in pilot_exercises()}
        find_c = exercises["pilot.find_c4"]
        self.assertEqual(find_c.difficulty, 1)
        self.assertEqual(evaluate(find_c, (60,)).verdict.value, "CORRECT")
        self.assertEqual(evaluate(find_c, (72,)).verdict.value, "PARTIAL")
        with self.assertRaises(ValueError):
            replace(find_c, publishable=True)
        inversion = exercises["pilot.c_major_first_inversion"]
        self.assertEqual(evaluate(inversion, (52, 60, 67)).verdict.value, "CORRECT")
        self.assertEqual(evaluate(inversion, (48, 52, 55)).verdict.value, "PARTIAL")

    def test_notation_and_slash_grammar(self):
        pairs = (("Bb", "B", 10), ("B", "H", 11), ("Eb", "Es", 3), ("F#", "Fis", 6))
        for root, bass, suffix, notation in product(pairs, pairs, ("", "m7", "7#11"), ("INT", "DE")):
            index = int(notation == "DE")
            with self.subTest(root=root, bass=bass, suffix=suffix, notation=notation):
                symbol = f" {root[index]}{suffix} / {bass[index]} "
                chord = parse_chord(symbol, notation)
                self.assertEqual((int(chord.root.pitch_class), chord.quality, int(chord.bass.pitch_class)),
                                 (root[2], suffix, bass[2]))
                for invalid in (symbol + "/", symbol + "?", "/" + symbol):
                    with self.assertRaises(ChordConstructionError):
                        parse_chord(invalid, notation)

    def test_transposed_applied_and_borrowed_progression_reaches_export(self):
        symbols = ["D7/F#", "G7", "C", "Fm", "Ab", "Bb", "E7", "Am"]
        bass = (6, 7, 0, 5, 8, 10, 4, 9)
        labels = ("V7(65)/V", "V7", "I", "iv", "bVI", "bVII", "V7/vi", "vi")
        for interval in (0, 1, 6, 11):
            with self.subTest(transposition=interval), TemporaryDirectory() as folder:
                session = ProgressionSession(symbols, key_root="C", convention="INT")
                for index in range(len(symbols)):
                    session.set_chord_event_timing(index, index * 480, 480)
                session.transpose(interval)
                self.assertEqual(tuple(session.harmonic_degree_at(i) for i in range(len(symbols))), labels)
                midi = session.export_midi_file(Path(folder) / "progression.mid")
                events = SMFParser.parse(midi.read_bytes()).all_notes
                self.assertEqual([(n.start_tick, n.pitch, n.duration_ticks) for n in events if n.channel == 1],
                                 [(i * 480, 36 + (pitch + interval) % 12, 470) for i, pitch in enumerate(bass)])

    def test_cadence_recontextualization_undo_redo_save_and_multitrack_export(self):
        # C is a subdominant in G. D7 then G closes that explicitly selected
        # context. The same last chord is a dominant when analyzed in C.
        chords = ["C", "D7", "G"]
        session = ProgressionSession(chords, key_root="C", convention="INT")
        for index, start in enumerate((0, 480, 1200)):
            session.set_chord_event_timing(index, start, 360)
        self.assertEqual(session.harmonic_degree_at(2), "V")
        session.set_key("G")
        self.assertEqual(tuple(session.harmonic_degree_at(i) for i in range(3)), ("IV", "V7", "I"))
        session.undo()
        self.assertEqual((session.key_root, session.harmonic_degree_at(2)), ("C", "V"))
        session.redo()
        self.assertEqual((session.key_root, session.harmonic_degree_at(2)), ("G", "I"))
        with TemporaryDirectory() as folder:
            folder = Path(folder)
            project = session.save_to_file(folder / "cadence.steps")
            restored = ProgressionSession(["Am"], key_root="A", convention="INT")
            restored.load_from_file(project)
            self.assertEqual((restored.key_root, restored.chords), ("G", chords))
            parsed = SMFParser.parse(restored.export_midi_file(folder / "cadence.mid").read_bytes())
        self.assertGreaterEqual(parsed.num_tracks, 3)
        self.assertEqual([(n.start_tick, n.pitch, n.duration_ticks) for n in parsed.all_notes if n.channel == 1],
                         [(0, 36, 350), (480, 38, 350), (1200, 43, 350)])
        for start, expected in ((0, {0, 4, 7}), (480, {0, 2, 6, 9}), (1200, {2, 7, 11})):
            self.assertEqual({n.pitch % 12 for n in parsed.all_notes if n.channel == 0 and n.start_tick == start},
                             expected)
