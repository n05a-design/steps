"""STEPS keyboard domain: 88-key model, musical overlays, recognition and practice.

Pure and UI-free (no tkinter, no glide_shell, no app). The music theory core in
``src.steps.theory`` stays authoritative; this package adds the keyboard view of
it. See ``docs/architecture/KEYBOARD_ARCHITECTURE.md`` and ADR-018.
"""

from __future__ import annotations

from .chord_tones import (
    ChordTone,
    ChordToneRole,
    LabeledVoicing,
    VoicedNote,
    chord_tones,
    label_voicing,
    render_chord_symbol,
)
from .input import InputSource, KeyboardInputState
from .model import (
    PIANO_HIGHEST_MIDI,
    PIANO_KEY_COUNT,
    PIANO_LOWEST_MIDI,
    KeyboardViewport,
    PianoKey,
    is_black_key,
    is_on_piano,
    piano_key,
    piano_keys,
)
from .practice import EvaluationPolicy, Exercise, PracticeFeedback, Verdict, evaluate, pilot_exercises
from .recognition import (
    CandidateKind,
    ChordCandidate,
    Reason,
    RecognitionResult,
    RecognitionStatus,
    recognize_chord,
)
from .state import FILL_PRIORITY, KeyboardLayers, KeyboardViewModel, KeyState, KeyVisual, build_view_model
from .voice_motion import Direction, MotionKind, VoiceMotion, VoicingComparison, compare_voicings
from .workbench import KEY_SCALE, VOICING_TYPES, ChordInfo, KeyboardMode, KeyboardWorkbench, available_scales

__all__ = [
    "CandidateKind",
    "ChordCandidate",
    "ChordInfo",
    "ChordTone",
    "ChordToneRole",
    "Direction",
    "EvaluationPolicy",
    "Exercise",
    "FILL_PRIORITY",
    "InputSource",
    "KEY_SCALE",
    "KeyState",
    "KeyVisual",
    "KeyboardInputState",
    "KeyboardLayers",
    "KeyboardMode",
    "KeyboardViewModel",
    "KeyboardViewport",
    "KeyboardWorkbench",
    "LabeledVoicing",
    "MotionKind",
    "PIANO_HIGHEST_MIDI",
    "PIANO_KEY_COUNT",
    "PIANO_LOWEST_MIDI",
    "PianoKey",
    "PracticeFeedback",
    "Reason",
    "RecognitionResult",
    "RecognitionStatus",
    "VOICING_TYPES",
    "Verdict",
    "VoiceMotion",
    "VoicedNote",
    "VoicingComparison",
    "available_scales",
    "build_view_model",
    "chord_tones",
    "compare_voicings",
    "evaluate",
    "is_black_key",
    "is_on_piano",
    "label_voicing",
    "pilot_exercises",
    "piano_key",
    "piano_keys",
    "recognize_chord",
    "render_chord_symbol",
]
