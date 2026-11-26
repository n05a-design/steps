"""Keyboard workbench: UI-free controller between ProgressionSession and a keyboard view.

The workbench *reads* the leading ``ProgressionSession`` (through a provider so
a replaced session is always picked up) and keeps only transient keyboard state:
selected event, preview voicing type and inversion rotation, scale overlay,
viewport, note input and practice progress. None of that is project data, so
nothing here can make the project dirty or add undo entries. The only path to a
project change is ``project_symbol_for`` which returns a chord symbol for the
caller to submit through the existing undoable controller commands.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Literal, Optional

from ..progression.session import ProgressionSession
from ..theory.chord import ChordDefinition, Voicing, parse_chord
from ..theory.exceptions import MusicTheoryError
from ..theory.inversion import InversionAnalysis
from ..theory.pitch import parse_spelling
from ..theory.scale import SCALE_TEMPLATES, ScaleDefinition, construct_scale
from .chord_tones import ChordTone, LabeledVoicing, chord_tones, label_voicing, render_chord_symbol, strip_octave
from .input import KeyboardInputState
from .model import KeyboardViewport
from .practice import EvaluationPolicy, Exercise, PracticeFeedback, evaluate, pilot_exercises
from .recognition import CandidateKind, ChordCandidate, RecognitionResult, recognize_chord
from .state import KeyboardLayers, KeyboardViewModel, build_view_model, practice_layers
from .voice_motion import VoicingComparison, compare_voicings

VoicingType = Literal["CLOSE", "DROP2", "SHELL", "ROOTLESS"]
VOICING_TYPES: tuple[VoicingType, ...] = ("CLOSE", "DROP2", "SHELL", "ROOTLESS")
KEY_SCALE = "__project_key__"


class KeyboardMode(str, Enum):
    PROGRESSION = "PROGRESSION"  # follow the selected progression event (read-only preview)
    FREE_INPUT = "FREE_INPUT"  # explore: click keys, see recognition
    PRACTICE = "PRACTICE"  # pilot exercises; never touches the project


@dataclass(frozen=True)
class ChordInfo:
    index: int
    symbol: str  # in the project notation convention, as stored
    chord: ChordDefinition
    tones: tuple[ChordTone, ...]
    voicing_type: VoicingType
    rotation: int
    voicing: Optional[LabeledVoicing]
    error: Optional[str]  # set when the requested voicing cannot be realised
    roman: Optional[str]
    key_root: str  # project key root without octave, project convention
    key_is_minor: bool

    @property
    def inversion(self) -> Optional[InversionAnalysis]:
        return self.voicing.inversion if self.voicing else None


@dataclass
class KeyboardWorkbench:
    session_provider: Callable[[], ProgressionSession]
    mode: KeyboardMode = KeyboardMode.PROGRESSION
    selected_index: Optional[int] = 0
    voicing_type: VoicingType = "CLOSE"
    rotation: int = 0
    show_chord: bool = True
    show_scale: bool = False
    scale_name: str = KEY_SCALE
    scale_root: Optional[str] = None  # written in project convention; None = project key root
    compare_previous: bool = False
    show_all_names: bool = False
    viewport: KeyboardViewport = field(default_factory=KeyboardViewport)
    auto_fit: bool = True
    input: KeyboardInputState = field(default_factory=KeyboardInputState)
    exercise_index: int = 0
    feedback: Optional[PracticeFeedback] = None
    show_practice_solution: bool = False
    exercises: tuple[Exercise, ...] = field(default_factory=pilot_exercises)

    # -- session access ------------------------------------------------------------
    @property
    def session(self) -> ProgressionSession:
        return self.session_provider()

    @property
    def convention(self) -> Literal["INT", "DE"]:
        return self.session.convention

    def sync(self) -> None:
        """Re-validate transient state after any project change (load, undo, remove...)."""
        count = len(self.session.chords)
        if count == 0:
            self.selected_index = None
        elif self.selected_index is None or not 0 <= self.selected_index < count:
            self.selected_index = min(max(self.selected_index or 0, 0), count - 1)

    # -- progression navigation ----------------------------------------------------
    def select(self, index: int) -> None:
        count = len(self.session.chords)
        if not 0 <= index < count:
            raise IndexError(f"Chord index {index} out of range")
        if index != self.selected_index:
            self.rotation = 0
        self.selected_index = index

    def step(self, delta: int) -> Optional[int]:
        self.sync()
        if self.selected_index is None:
            return None
        target = min(max(self.selected_index + delta, 0), len(self.session.chords) - 1)
        self.select(target)
        return target

    def set_voicing_type(self, voicing_type: VoicingType) -> None:
        if voicing_type not in VOICING_TYPES:
            raise ValueError(f"Unknown voicing type {voicing_type!r}")
        self.voicing_type = voicing_type
        self.rotation = 0

    def rotate(self, delta: int) -> None:
        self.rotation += delta

    # -- musical content ------------------------------------------------------------
    def key_scale(self) -> Optional[ScaleDefinition]:
        session = self.session
        try:
            root = parse_spelling(session.key_root, convention=session.convention)
            return construct_scale(root, "aeolian" if session.is_minor else "ionian")
        except MusicTheoryError:
            return None

    def overlay_scale(self) -> Optional[ScaleDefinition]:
        if self.scale_name == KEY_SCALE and self.scale_root is None:
            return self.key_scale()
        session = self.session
        try:
            root_text = self.scale_root if self.scale_root is not None else session.key_root
            root = parse_spelling(root_text, convention=session.convention)
            name = ("aeolian" if session.is_minor else "ionian") if self.scale_name == KEY_SCALE else self.scale_name
            return construct_scale(root, name)
        except MusicTheoryError:
            return None

    def chord_info(self, index: Optional[int] = None) -> Optional[ChordInfo]:
        self.sync()
        index = self.selected_index if index is None else index
        session = self.session
        if index is None or not 0 <= index < len(session.chords):
            return None
        symbol = session.chords[index]
        chord = parse_chord(symbol, convention=session.convention)
        error: Optional[str] = None
        labeled: Optional[LabeledVoicing] = None
        try:
            voicing = session.get_voicings(self.voicing_type)[index]
            if self.rotation:
                voicing = Voicing(voicing.notes, voicing.voicing_type).invert(self.rotation)
            labeled = label_voicing(chord, voicing)
        except (MusicTheoryError, ValueError, IndexError) as exc:
            error = str(exc)
        try:
            roman = session.harmonic_degree_at(index)
        except (MusicTheoryError, ValueError):
            roman = None
        try:
            key_root = strip_octave(
                parse_spelling(session.key_root, convention=session.convention).render(session.convention)
            )
        except MusicTheoryError:
            key_root = session.key_root
        return ChordInfo(index, symbol, chord, chord_tones(chord), self.voicing_type, self.rotation,
                         labeled, error, roman, key_root, session.is_minor)

    def comparison(self) -> Optional[VoicingComparison]:
        """Previous event's voicing compared with the current one (same voicing type)."""
        self.sync()
        index = self.selected_index
        if index is None or index == 0:
            return None
        try:
            voicings = self.session.get_voicings(self.voicing_type)
        except (MusicTheoryError, ValueError):
            return None
        current = voicings[index]
        if self.rotation:
            current = Voicing(current.notes).invert(self.rotation)
        return compare_voicings(voicings[index - 1].notes, current.notes)

    def recognition(self) -> RecognitionResult:
        return recognize_chord(self.input.active_notes, self.key_scale())

    def project_symbol_for(self, candidate: ChordCandidate) -> str:
        """Symbol in the project's convention, validated by the core parser."""
        symbol = render_chord_symbol(candidate.chord, self.convention)
        parse_chord(symbol, convention=self.convention)
        return symbol

    # -- practice --------------------------------------------------------------------
    @property
    def exercise(self) -> Exercise:
        return self.exercises[self.exercise_index % len(self.exercises)]

    def select_exercise(self, index: int) -> None:
        if not 0 <= index < len(self.exercises):
            raise IndexError(index)
        self.exercise_index = index
        self.feedback = None
        self.show_practice_solution = False
        self.input.clear_selected()
        self.input.release_all()

    def check_practice(self) -> PracticeFeedback:
        self.feedback = evaluate(self.exercise, self.input.active_notes)
        return self.feedback

    # -- view model ------------------------------------------------------------------
    def layers(self) -> KeyboardLayers:
        layers = KeyboardLayers(
            pressed=frozenset(self.input.sounding),
            selected=frozenset(self.input.selected),
        )
        if self.show_scale:
            scale = self.overlay_scale()
            if scale is not None:
                layers.scale_pitch_classes = {int(s.pitch_class): i + 1 for i, s in enumerate(scale.spellings)}
                layers.scale_spellings = {int(s.pitch_class): s for s in scale.spellings}
        if self.mode is KeyboardMode.PROGRESSION and self.show_chord:
            info = self.chord_info()
            if info is not None and info.voicing is not None:
                layers.chord_notes = {note.midi: note.role for note in info.voicing.notes}
                layers.chord_bass = info.voicing.bass.midi
                layers.spellings = {
                    note.midi: note.spelling for note in info.voicing.notes if note.spelling is not None
                }
            if self.compare_previous:
                comparison = self.comparison()
                if comparison is not None:
                    layers.comparison_notes = frozenset(comparison.start)
                    layers.comparison_held = frozenset(comparison.held_pitches)
        if self.mode is KeyboardMode.FREE_INPUT and self.input.active_notes:
            # Spell entered keys from the first complete reading. Only names are
            # taken over (no role badges), because the reading may be ambiguous.
            result = self.recognition()
            reading = next((c for c in result.candidates if c.kind is not CandidateKind.INCOMPLETE), None)
            if reading is not None:
                labelled = label_voicing(reading.chord, self.input.active_notes)
                layers.spellings = {n.midi: n.spelling for n in labelled.notes if n.spelling is not None}
        if self.mode is KeyboardMode.PRACTICE:
            exercise = self.exercise
            if self.feedback is not None or self.show_practice_solution:
                exact = exercise.policy is EvaluationPolicy.EXACT_PITCHES
                marks = practice_layers(exercise.reference_notes, self.input.active_notes, exact)
                layers.practice_correct = marks["correct"]
                layers.practice_wrong = marks["wrong"] if self.feedback is not None else frozenset()
                layers.practice_missing = marks["missing"] if self.show_practice_solution else frozenset()
        return layers

    def view_model(self) -> KeyboardViewModel:
        layers = self.layers()
        if self.auto_fit:
            self.viewport = self.viewport.fitted_to(
                [*layers.chord_notes, *layers.comparison_notes, *layers.practice_missing]
            )
        return build_view_model(self.viewport, layers, self.convention, show_all_names=self.show_all_names)


def available_scales() -> tuple[str, ...]:
    """Scale templates the core supports, in registry order."""
    return tuple(SCALE_TEMPLATES)


__all__ = [
    "KEY_SCALE",
    "VOICING_TYPES",
    "ChordInfo",
    "KeyboardMode",
    "KeyboardWorkbench",
    "available_scales",
]
