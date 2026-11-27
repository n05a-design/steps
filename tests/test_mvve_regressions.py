"""Independent reproductions of the keyboard and theory audit findings."""

import unittest

from src.steps.keyboard.chord_tones import label_voicing
from src.steps.keyboard.practice import EvaluationPolicy, Exercise, evaluate
from src.steps.keyboard.recognition import CandidateKind, recognize_chord
from src.steps.keyboard.voice_motion import compare_voicings
from src.steps.theory.chord import parse_chord
from src.steps.theory.exceptions import ScaleConstructionError
from src.steps.theory.pitch import parse_spelling
from src.steps.theory.scale import ScaleDefinition, construct_scale


class MusicalAuditRegressions(unittest.TestCase):
    def test_bass_role_and_classical_figure(self):
        cases = (
            ("C/E", (52, 60, 67), "MAJOR_THIRD", "6"),
            ("G7/D", (50, 53, 55, 59), "PERFECT_FIFTH", "4/3"),
            ("Cdim7/Bbb", (57, 60, 63, 66), "DIMINISHED_SEVENTH", "4/2"),
            ("C7b5/Gb", (54, 60, 64, 70), "DIMINISHED_FIFTH", "4/3"),
            ("C6/A", (57, 60, 64, 67), "SIXTH", None),
            ("C7#9/D#", (51, 60, 64, 67, 70), "SHARP_NINTH", None),
            ("C7#11/F#", (54, 60, 64, 67, 70), "SHARP_ELEVENTH", None),
            ("C7b13/Ab", (56, 60, 64, 67, 70), "FLAT_THIRTEENTH", None),
            ("C13/A", (57, 60, 64, 67, 70, 74), "THIRTEENTH", None),
            ("Cmaj13/A", (57, 60, 64, 67, 71, 74), "THIRTEENTH", None),
            ("C/F#", (54, 60, 64, 67), "SLASH_BASS", "slash"),
            ("C/Eb", (51, 60, 64, 67), "SLASH_BASS", "slash"),
            ("C/E", (51, 60, 64, 67), "NON_CHORD_TONE", "slash"),
        )
        for symbol, notes, role, figure in cases:
            with self.subTest(symbol=symbol, notes=notes):
                labelled = label_voicing(parse_chord(symbol, "INT"), notes)
                self.assertEqual(labelled.bass.role.value, role)
                self.assertEqual(labelled.inversion.figured_bass if labelled.inversion else None, figure)

    def test_recognition_uses_the_same_bass_role_as_the_symbol(self):
        result = recognize_chord([51, 60, 64, 67, 70], allow_incomplete=False)
        altered = next(c for c in result.candidates
                       if c.kind is CandidateKind.EXACT and c.chord.quality == "7#9"
                       and int(c.chord.root.pitch_class) == 0)
        self.assertEqual(altered.bass_role.value, "SHARP_NINTH")
        self.assertEqual(altered.figured_bass, "slash")

    def test_recognition_preserves_exact_candidates_under_doubling_and_translation(self):
        # A is lowest in both voicings. The C6 and Am7 readings remain distinct.
        base = [57, 60, 64, 67]
        for distance in range(12):
            permuted = [n + distance for n in (*reversed(base), 72)]
            result = recognize_chord(permuted, allow_incomplete=False)
            candidates = {(int(c.chord.root.pitch_class), c.chord.quality)
                          for c in result.candidates if c.kind is CandidateKind.EXACT}
            self.assertEqual(candidates, {(distance, "6"), ((9 + distance) % 12, "m7")})

    def test_exercise_rejects_invalid_scoring_and_review_values(self):
        base = dict(exercise_id="mvve.case", topic="triads", objective_key="objective",
                    prompt_key="prompt", difficulty=1, policy=EvaluationPolicy.PITCH_CLASSES_WITH_BASS,
                    expected_pitch_classes=(0, 4, 7), expected_bass_pitch_class=0)
        for wrong in (
            {"difficulty": True}, {"policy": "UNKNOWN"}, {"expected_pitch_classes": (0, 4, 12)},
            {"expected_bass_pitch_class": 2}, {"expected_bass_pitch_class": False},
            {"review_status": "UNKNOWN", "publishable": True},
            {"policy": EvaluationPolicy.EXACT_PITCHES, "expected_pitches": (128,)},
        ):
            with self.subTest(wrong=wrong), self.assertRaises(ValueError):
                Exercise(**(base | wrong))

    def test_empty_exact_exercise_reports_missing_register(self):
        exercise = Exercise("mvve.register", "notes", "objective", "prompt", 1,
                            EvaluationPolicy.EXACT_PITCHES, expected_pitches=(72, 67, 60))
        feedback = evaluate(exercise, [])
        self.assertEqual(feedback.verdict.value, "EMPTY")
        self.assertEqual(feedback.missing_pitches, (60, 67, 72))
        self.assertEqual(feedback.missing_pitch_classes, (0, 7))
        self.assertEqual(evaluate(exercise, [60, 67]).verdict.value, "PARTIAL")

    def test_shared_pitch_can_move_between_paired_voices(self):
        forward = compare_voicings([60, 64], [64, 67])
        backward = compare_voicings([64, 67], [60, 64])
        self.assertEqual(forward.held_pitches, (64,))
        self.assertEqual(forward.stationary_voices, ())
        self.assertEqual([m.semitones for m in forward.motions], [4, 3])
        self.assertEqual([m.semitones for m in backward.motions], [-4, -3])
        hold = compare_voicings([60, 64], [60, 67])
        self.assertEqual([m.start for m in hold.stationary_voices], [60])

    def test_scale_rejects_inconsistent_notes_and_degree_types(self):
        scale = construct_scale(parse_spelling("C4", "INT"), "ionian")
        spellings = scale.spellings
        for wrong in (
            (), spellings[::-1], spellings[:-1],
            (parse_spelling("B#3", "INT"), *spellings[1:]),
            (*spellings[:1], parse_spelling("C##4", "INT"), *spellings[2:]),
        ):
            with self.subTest(wrong=wrong), self.assertRaises(ScaleConstructionError):
                ScaleDefinition(scale.root, scale.template, wrong)
        for get_degree in (scale.get_degree, scale.get_diatonic_triad, scale.get_diatonic_seventh):
            for invalid in (True, 1.5, "1"):
                with self.subTest(api=get_degree.__name__, degree=invalid):
                    with self.assertRaises(ScaleConstructionError):
                        get_degree(invalid)
