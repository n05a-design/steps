"""STEPS progression and harmonic transformation models."""
from __future__ import annotations

from .voice_leading import (
    VoiceLeadingStyle,
    absolute_semitone_distance,
    circular_pc_distance,
    detect_voice_crossing,
    detect_voice_overlap,
    detect_parallel_fifths_octaves,
    guide_tone_resolution,
    optimize_smooth_voice_leading
)
from .engine import (
    CanonicalProgression,
    CANONICAL_PROGRESSIONS,
    get_progression,
    list_progressions,
    resolve_roman_degree,
    generate_progression_voicings,
    analyze_progression_voice_leading
)

__all__ = [
    'VoiceLeadingStyle',
    'absolute_semitone_distance',
    'circular_pc_distance',
    'detect_voice_crossing',
    'detect_voice_overlap',
    'detect_parallel_fifths_octaves',
    'guide_tone_resolution',
    'optimize_smooth_voice_leading',
    'CanonicalProgression',
    'CANONICAL_PROGRESSIONS',
    'get_progression',
    'list_progressions',
    'resolve_roman_degree',
    'generate_progression_voicings',
    'analyze_progression_voice_leading'
]

