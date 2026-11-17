"""STEPS core music theory concepts and notation models."""
from __future__ import annotations

from .exceptions import (
    MusicTheoryError,
    InvalidPitchClassError,
    InvalidDiatonicStepError,
    InvalidAlterationError,
    PitchRangeError,
    InvalidIntervalError,
    ChordConstructionError,
    VoiceLeadingError,
    ProgressionParsingError,
    ScaleConstructionError
)
from .pitch import (
    PitchClass,
    NoteSpelling,
    midi_to_pitch_class,
    midi_to_frequency,
    frequency_to_midi,
    parse_spelling
)
from .interval import (
    ChromaticInterval,
    DiatonicInterval,
    semitones_between,
    directed_semitones,
    invert_semitones_modulo12,
    transpose_spelling,
    interval_between_spellings
)
from .triad import (
    TriadQuality,
    construct_triad,
    invert_triad_voicing,
    get_triad_pitch_class_set
)
from .seventh import (
    SeventhQuality,
    construct_seventh,
    invert_seventh_voicing,
    make_drop2_voicing,
    make_shell_voicing
)
from .chord import (
    ChordDefinition,
    Voicing,
    parse_chord,
    CHORD_TEMPLATES
)
from .scale import (
    ModeCategory,
    ScaleTemplate,
    ScaleDefinition,
    SCALE_TEMPLATES,
    get_scale_template,
    construct_scale,
    parse_scale
)
from .inversion import (
    ChordInversion,
    FiguredBassSymbol,
    InversionAnalysis,
    detect_chord_inversion,
    detect_hand_voicing
)
from .voicings import (
    GuideToneResolution,
    ProgressionShellVoicings,
    ShellVoicing,
    extract_guide_tone_pcs,
    generate_shell_voicings,
)
from .beginner_voicing import (
    BeginnerTriadInversion,
    PedagogicalReduction,
    BeginnerChordVoicing,
    BeginnerVoiceLeadingTransition,
    BeginnerProgressionVoicings,
    reduce_chord_for_beginners,
    generate_beginner_inversions,
    determine_beginner_fingering,
    generate_beginner_voicings,
)

__all__ = [
    'MusicTheoryError',
    'InvalidPitchClassError',
    'InvalidDiatonicStepError',
    'InvalidAlterationError',
    'PitchRangeError',
    'InvalidIntervalError',
    'ChordConstructionError',
    'VoiceLeadingError',
    'ProgressionParsingError',
    'ScaleConstructionError',
    'PitchClass',
    'NoteSpelling',
    'midi_to_pitch_class',
    'midi_to_frequency',
    'frequency_to_midi',
    'parse_spelling',
    'ChromaticInterval',
    'DiatonicInterval',
    'semitones_between',
    'directed_semitones',
    'invert_semitones_modulo12',
    'transpose_spelling',
    'interval_between_spellings',
    'TriadQuality',
    'construct_triad',
    'invert_triad_voicing',
    'get_triad_pitch_class_set',
    'SeventhQuality',
    'construct_seventh',
    'invert_seventh_voicing',
    'make_drop2_voicing',
    'make_shell_voicing',
    'ChordDefinition',
    'Voicing',
    'parse_chord',
    'CHORD_TEMPLATES',
    'ModeCategory',
    'ScaleTemplate',
    'ScaleDefinition',
    'SCALE_TEMPLATES',
    'get_scale_template',
    'construct_scale',
    'parse_scale',
    'ChordInversion',
    'FiguredBassSymbol',
    'InversionAnalysis',
    'detect_chord_inversion',
    'detect_hand_voicing',
    'GuideToneResolution',
    'ProgressionShellVoicings',
    'ShellVoicing',
    'extract_guide_tone_pcs',
    'generate_shell_voicings',
    'BeginnerTriadInversion',
    'PedagogicalReduction',
    'BeginnerChordVoicing',
    'BeginnerVoiceLeadingTransition',
    'BeginnerProgressionVoicings',
    'reduce_chord_for_beginners',
    'generate_beginner_inversions',
    'determine_beginner_fingering',
    'generate_beginner_voicings'
]

