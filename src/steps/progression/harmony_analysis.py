"""Spelling-aware harmonic labels for the session's displayed analysis."""

from ..theory.chord import ChordDefinition
from ..theory.pitch import DIATONIC_BASE_PC, DIATONIC_STEPS, NoteSpelling

_NUMERALS = ("I", "II", "III", "IV", "V", "VI", "VII")
_MAJOR = (0, 2, 4, 5, 7, 9, 11)
_MINOR = (0, 2, 3, 5, 7, 8, 10)
_SUFFIXES = {
    "m": "", "dim": "°", "dim7": "°7", "m7b5": "ø7", "aug": "+",
    "m(maj7)": "maj7", "m7": "7", "m9": "9", "m11": "11", "madd9": "add9",
    "6": "(add6)", "m6": "(add6)",
}


def _root_interval(root: NoteSpelling, tonic: NoteSpelling) -> tuple[int, int]:
    degree = (DIATONIC_STEPS.index(root.step) - DIATONIC_STEPS.index(tonic.step)) % 7
    natural = (DIATONIC_BASE_PC[root.step] - DIATONIC_BASE_PC[tonic.step]) % 12
    return degree, natural + root.alteration - tonic.alteration


def has_dominant_quality(chord: ChordDefinition) -> bool:
    """Recognize a major triad or a seventh chord with a major third and minor seventh."""
    return chord.quality == "" or {4, 10}.issubset(chord.theoretical_intervals)


def _degree_label(chord: ChordDefinition, key: NoteSpelling, minor: bool) -> str:
    degree, semitones = _root_interval(chord.root, key)
    reference = (_MINOR if minor else _MAJOR)[degree]
    if minor and degree == 6 and semitones == 11 and chord.quality in {"dim", "dim7", "m7b5"}:
        reference = 11  # Conventional leading-tone numeral in minor.
    alteration = semitones - reference
    accidental = "#" * max(0, alteration) + "b" * max(0, -alteration)
    numeral = _NUMERALS[degree]
    if 3 in chord.theoretical_intervals:
        numeral = numeral.lower()
    return accidental + numeral


def _bass_figure(chord: ChordDefinition, suffix: str, convention: str) -> str:
    bass = chord.bass
    if bass is None:
        return ""
    degree, semitones = _root_interval(bass, chord.root)
    semitones %= 12
    if degree == 0 and semitones == 0:
        return ""
    intervals = {tone % 12 for tone in chord.theoretical_intervals}
    if semitones in intervals:
        figures = {2: "6", 4: "64"} if chord.is_triad else {}
        if chord.is_seventh:
            figures = {2: "65", 4: "43", 6: "42"}
        figure = figures.get(degree)
        if figure:
            return f"({figure})" if suffix else figure
    return f"/{bass.render(convention).removesuffix(str(bass.octave))}"


def format_harmonic_degree(
    chord: ChordDefinition,
    key: NoteSpelling,
    is_minor: bool,
    convention: str,
    following: ChordDefinition | None = None,
) -> str:
    """Use written roots and chord structure; infer direct applied dominants from the next chord."""
    degree = _degree_label(chord, key, is_minor)
    suffix = _SUFFIXES.get(chord.quality, chord.quality)
    figure = _bass_figure(chord, suffix, convention)
    scale = {(int(key.pitch_class) + step) % 12 for step in (_MINOR if is_minor else _MAJOR)}
    if (
        following is not None
        and _root_interval(following.root, key) != (0, 0)
        and _root_interval(chord.root, following.root) == (4, 7)
        and has_dominant_quality(chord)
        and not figure.startswith("/")
        and not chord.pitch_class_set <= scale
        and 7 in following.theoretical_intervals
        and any(tone in following.theoretical_intervals for tone in (3, 4))
    ):
        return f"V{suffix}{figure}/{_degree_label(following, key, is_minor)}"
    return degree + suffix + figure
