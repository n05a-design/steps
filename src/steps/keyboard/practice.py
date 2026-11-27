"""Practice engine foundation: exercise contract, per-type scoring and a pilot set.

Exercises only *read* played notes; they never touch a ``ProgressionSession``.
Each exercise states which musical facts it checks (``EvaluationPolicy``): a
chord-building task accepts any octave, a voicing task requires exact pitches.

Review status: the pilot exercises below are AI-drafted and **not** reviewed by
an independent music theorist. They are marked ``AI_DRAFT_UNREVIEWED`` and
``publishable=False``; the app must label them as such. Expected notes are
derived from the core chord definitions, not hard-coded here, except for the
explicit single pitches of note and interval tasks.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Literal, Optional

from ..theory.chord import parse_chord
from .model import sorted_unique_notes

ReviewStatus = Literal["AI_DRAFT_UNREVIEWED", "HUMAN_REVIEWED", "OWNER_APPROVED"]


class EvaluationPolicy(str, Enum):
    EXACT_PITCHES = "EXACT_PITCHES"  # same MIDI notes, nothing else (note / interval / voicing tasks)
    PITCH_CLASSES = "PITCH_CLASSES"  # any octave and doubling, all tones present, no foreign tone
    PITCH_CLASSES_WITH_BASS = "PITCH_CLASSES_WITH_BASS"  # as above plus required lowest pitch class


class Verdict(str, Enum):
    EMPTY = "EMPTY"
    CORRECT = "CORRECT"
    PARTIAL = "PARTIAL"  # some expected material present, but missing, extra or wrong bass
    INCORRECT = "INCORRECT"  # nothing expected present


@dataclass(frozen=True)
class Exercise:
    exercise_id: str
    topic: str  # e.g. "notes", "triads", "inversions", "sevenths", "intervals"
    objective_key: str  # localization key of the learning objective
    prompt_key: str  # localization key of the task text
    difficulty: int  # 1 (entry) .. 5
    policy: EvaluationPolicy
    expected_pitches: tuple[int, ...] = ()  # EXACT_PITCHES
    expected_pitch_classes: tuple[int, ...] = ()  # PITCH_CLASSES*
    expected_bass_pitch_class: Optional[int] = None
    chord_symbol: Optional[str] = None  # INT symbol the expectation was derived from
    hint_keys: tuple[str, ...] = ()
    knowledge_refs: tuple[str, ...] = ()  # knowledge module ids, e.g. "M04"
    review_status: ReviewStatus = "AI_DRAFT_UNREVIEWED"
    publishable: bool = False
    version: int = 1

    def __post_init__(self) -> None:
        if type(self.difficulty) is not int or not 1 <= self.difficulty <= 5:
            raise ValueError("Difficulty must be 1..5.")
        if not isinstance(self.policy, EvaluationPolicy):
            raise ValueError("Unknown evaluation policy.")
        if any(type(note) is not int or not 0 <= note <= 127 for note in self.expected_pitches):
            raise ValueError("Expected pitches must be MIDI integers in 0..127.")
        if any(type(pc) is not int or not 0 <= pc < 12 for pc in self.expected_pitch_classes):
            raise ValueError("Expected pitch classes must be integers in 0..11.")
        if self.policy is EvaluationPolicy.EXACT_PITCHES and not self.expected_pitches:
            raise ValueError("EXACT_PITCHES exercises need expected_pitches.")
        if self.policy is not EvaluationPolicy.EXACT_PITCHES and not self.expected_pitch_classes:
            raise ValueError("Pitch-class exercises need expected_pitch_classes.")
        if self.policy is EvaluationPolicy.PITCH_CLASSES_WITH_BASS and self.expected_bass_pitch_class is None:
            raise ValueError("Bass exercises need expected_bass_pitch_class.")
        if self.expected_bass_pitch_class is not None and (
            type(self.expected_bass_pitch_class) is not int
            or self.expected_bass_pitch_class not in self.expected_pitch_classes
        ):
            raise ValueError("The expected bass must be one of the expected pitch classes.")
        if self.review_status not in ("AI_DRAFT_UNREVIEWED", "HUMAN_REVIEWED", "OWNER_APPROVED"):
            raise ValueError("Unknown exercise review status.")
        if type(self.publishable) is not bool:
            raise ValueError("Publishable must be a boolean.")
        if self.publishable and self.review_status == "AI_DRAFT_UNREVIEWED":
            raise ValueError("Unreviewed exercises cannot be publishable.")

    @property
    def reference_notes(self) -> tuple[int, ...]:
        """A concrete solution for display hints (exact pitches, else pitch classes near C4)."""
        if self.expected_pitches:
            return self.expected_pitches
        notes = [60 + pc for pc in self.expected_pitch_classes]
        if self.expected_bass_pitch_class is not None:
            bass = 48 + self.expected_bass_pitch_class
            notes = [bass] + [n if n > bass else n + 12 for n in notes if n % 12 != self.expected_bass_pitch_class]
        return sorted_unique_notes(notes)


@dataclass(frozen=True)
class PracticeFeedback:
    exercise_id: str
    verdict: Verdict
    played: tuple[int, ...]
    correct_pitch_classes: tuple[int, ...]
    missing_pitch_classes: tuple[int, ...]
    extra_pitch_classes: tuple[int, ...]
    correct_pitches: tuple[int, ...] = ()  # EXACT_PITCHES only
    missing_pitches: tuple[int, ...] = ()
    extra_pitches: tuple[int, ...] = ()
    bass_correct: Optional[bool] = None
    message_key: str = ""

    @property
    def is_correct(self) -> bool:
        return self.verdict is Verdict.CORRECT


def evaluate(exercise: Exercise, played: Iterable[int]) -> PracticeFeedback:
    notes = sorted_unique_notes(played)
    played_pcs = {n % 12 for n in notes}
    if not notes:
        missing_pitches = (tuple(sorted(set(exercise.expected_pitches)))
                           if exercise.policy is EvaluationPolicy.EXACT_PITCHES else ())
        expected_pcs = {n % 12 for n in missing_pitches} if missing_pitches else set(exercise.expected_pitch_classes)
        return PracticeFeedback(exercise.exercise_id, Verdict.EMPTY, (), (), tuple(sorted(expected_pcs)), (),
                                missing_pitches=missing_pitches,
                                message_key="practice.feedback.empty")

    if exercise.policy is EvaluationPolicy.EXACT_PITCHES:
        expected = set(exercise.expected_pitches)
        got = set(notes)
        correct, missing, extra = sorted(expected & got), sorted(expected - got), sorted(got - expected)
        expected_pcs = {n % 12 for n in expected}
        if not missing and not extra:
            verdict, key = Verdict.CORRECT, "practice.feedback.correct"
        elif correct:
            verdict, key = Verdict.PARTIAL, "practice.feedback.partial_pitches"
        elif played_pcs & expected_pcs:
            verdict, key = Verdict.PARTIAL, "practice.feedback.wrong_octave"
        else:
            verdict, key = Verdict.INCORRECT, "practice.feedback.incorrect"
        return PracticeFeedback(
            exercise.exercise_id, verdict, notes,
            tuple(sorted(played_pcs & expected_pcs)), tuple(sorted(expected_pcs - played_pcs)),
            tuple(sorted(played_pcs - expected_pcs)),
            tuple(correct), tuple(missing), tuple(extra), message_key=key,
        )

    expected_pcs = set(exercise.expected_pitch_classes)
    correct = sorted(expected_pcs & played_pcs)
    missing = sorted(expected_pcs - played_pcs)
    extra = sorted(played_pcs - expected_pcs)
    bass_ok: Optional[bool] = None
    if exercise.policy is EvaluationPolicy.PITCH_CLASSES_WITH_BASS:
        bass_ok = notes[0] % 12 == exercise.expected_bass_pitch_class
    if not missing and not extra and bass_ok in (None, True):
        verdict, key = Verdict.CORRECT, "practice.feedback.correct"
    elif not missing and not extra:
        verdict, key = Verdict.PARTIAL, "practice.feedback.wrong_bass"
    elif correct:
        verdict, key = Verdict.PARTIAL, "practice.feedback.partial_tones"
    else:
        verdict, key = Verdict.INCORRECT, "practice.feedback.incorrect"
    return PracticeFeedback(exercise.exercise_id, verdict, notes, tuple(correct), tuple(missing),
                            tuple(extra), bass_correct=bass_ok, message_key=key)


def _chord_pcs(symbol: str) -> tuple[int, ...]:
    chord = parse_chord(symbol, convention="INT")
    return tuple(sorted(chord.pitch_class_set))


def _bass_pc(symbol: str) -> int:
    chord = parse_chord(symbol, convention="INT")
    return int((chord.bass or chord.root).pitch_class)


def pilot_exercises() -> tuple[Exercise, ...]:
    """Six entry exercises. AI draft, not human-reviewed, not publishable."""
    return (
        Exercise(
            "pilot.find_c4", "notes", "practice.objective.find_note", "practice.task.find_c4", 1,
            EvaluationPolicy.EXACT_PITCHES, expected_pitches=(60,),
            hint_keys=("practice.hint.middle_c",), knowledge_refs=("M01", "M02"),
        ),
        Exercise(
            "pilot.c_major_triad", "triads", "practice.objective.build_triad", "practice.task.c_major", 1,
            EvaluationPolicy.PITCH_CLASSES, expected_pitch_classes=_chord_pcs("C"), chord_symbol="C",
            hint_keys=("practice.hint.major_triad",), knowledge_refs=("M04",),
        ),
        Exercise(
            "pilot.a_minor_triad", "triads", "practice.objective.build_triad", "practice.task.a_minor", 1,
            EvaluationPolicy.PITCH_CLASSES, expected_pitch_classes=_chord_pcs("Am"), chord_symbol="Am",
            hint_keys=("practice.hint.minor_triad",), knowledge_refs=("M04",),
        ),
        Exercise(
            "pilot.c_major_first_inversion", "inversions", "practice.objective.inversion",
            "practice.task.c_first_inversion", 2, EvaluationPolicy.PITCH_CLASSES_WITH_BASS,
            expected_pitch_classes=_chord_pcs("C/E"), expected_bass_pitch_class=_bass_pc("C/E"),
            chord_symbol="C/E", hint_keys=("practice.hint.first_inversion",), knowledge_refs=("M04",),
        ),
        Exercise(
            "pilot.g7", "sevenths", "practice.objective.seventh", "practice.task.g7", 2,
            EvaluationPolicy.PITCH_CLASSES, expected_pitch_classes=_chord_pcs("G7"), chord_symbol="G7",
            hint_keys=("practice.hint.dominant_seventh",), knowledge_refs=("M04",),
        ),
        Exercise(
            "pilot.major_third_above_c4", "intervals", "practice.objective.interval",
            "practice.task.major_third_c4", 1, EvaluationPolicy.EXACT_PITCHES, expected_pitches=(60, 64),
            hint_keys=("practice.hint.major_third",), knowledge_refs=("M02",),
        ),
    )


__all__ = [
    "EvaluationPolicy",
    "Exercise",
    "PracticeFeedback",
    "Verdict",
    "evaluate",
    "pilot_exercises",
]
