"""STEPS progression and harmonic transformation models."""
from __future__ import annotations

from .voice_leading import (
    ContrapuntalMotion,
    VoiceLeadingStyle,
    absolute_semitone_distance,
    analyze_contrapuntal_motions,
    circular_pc_distance,
    classify_voice_motion,
    detect_voice_crossing,
    detect_voice_overlap,
    detect_parallel_fifths_octaves,
    guide_tone_resolution,
    optimize_smooth_voice_leading
)
from .engine import (
    CanonicalProgression,
    CANONICAL_PROGRESSIONS,
    ARCHETYPE_THEORY_METADATA,
    get_progression,
    list_progressions,
    resolve_roman_degree,
    generate_progression_voicings,
    analyze_progression_voice_leading,
    detect_progression_archetypes
)
from .session import (
    ProgressionSession,
    ChordRecommendation,
    DegreeAnalysis
)

__all__ = [
    'ContrapuntalMotion',
    'VoiceLeadingStyle',
    'absolute_semitone_distance',
    'analyze_contrapuntal_motions',
    'circular_pc_distance',
    'classify_voice_motion',
    'detect_voice_crossing',
    'detect_voice_overlap',
    'detect_parallel_fifths_octaves',
    'guide_tone_resolution',
    'optimize_smooth_voice_leading',
    'CanonicalProgression',
    'CANONICAL_PROGRESSIONS',
    'ARCHETYPE_THEORY_METADATA',
    'get_progression',
    'list_progressions',
    'resolve_roman_degree',
    'generate_progression_voicings',
    'analyze_progression_voice_leading',
    'detect_progression_archetypes',
    'ProgressionSession',
    'ChordRecommendation',
    'DegreeAnalysis'
]

