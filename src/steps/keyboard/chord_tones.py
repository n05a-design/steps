"""Musical meaning for keyboard notes: chord-tone roles, spellings and voicing labels.

Everything here is derived from the existing core contracts:

* chord qualities and unreduced intervals from ``theory.chord.CHORD_TEMPLATES``
  (ADR-015: 9/11/13 keep their compound size),
* spelling by diatonic transposition from ``NoteSpelling.transpose_diatonic``,
* inversion state from ``theory.inversion.detect_chord_inversion``.

No chord, interval or spelling rule is redefined; this module only names the
role each template interval plays so a view can mark root, bass, third, etc.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Literal, Optional, Sequence

from ..theory.chord import ChordDefinition, Voicing
from ..theory.exceptions import ChordConstructionError, MusicTheoryError
from ..theory.inversion import ChordInversion, InversionAnalysis, detect_chord_inversion
from ..theory.pitch import NoteSpelling
from ..theory.scale import ScaleDefinition
from .model import sorted_unique_notes

Convention = Literal["INT", "DE"]


class ChordToneRole(str, Enum):
    """Function of a tone relative to the chord root (not to the key)."""

    ROOT = "ROOT"
    SECOND = "SECOND"
    MINOR_THIRD = "MINOR_THIRD"
    MAJOR_THIRD = "MAJOR_THIRD"
    FOURTH = "FOURTH"
    DIMINISHED_FIFTH = "DIMINISHED_FIFTH"
    PERFECT_FIFTH = "PERFECT_FIFTH"
    AUGMENTED_FIFTH = "AUGMENTED_FIFTH"
    SIXTH = "SIXTH"
    DIMINISHED_SEVENTH = "DIMINISHED_SEVENTH"
    MINOR_SEVENTH = "MINOR_SEVENTH"
    MAJOR_SEVENTH = "MAJOR_SEVENTH"
    FLAT_NINTH = "FLAT_NINTH"
    NINTH = "NINTH"
    SHARP_NINTH = "SHARP_NINTH"
    ELEVENTH = "ELEVENTH"
    SHARP_ELEVENTH = "SHARP_ELEVENTH"
    FLAT_THIRTEENTH = "FLAT_THIRTEENTH"
    THIRTEENTH = "THIRTEENTH"
    SLASH_BASS = "SLASH_BASS"  # written bass that is not a chord tone
    NON_CHORD_TONE = "NON_CHORD_TONE"  # sounding note outside chord and written bass

    @property
    def interval_label(self) -> str:
        """Compact degree label relative to the root (ASCII, notation neutral)."""
        return _ROLE_INFO[self][0]

    @property
    def diatonic_steps(self) -> int | None:
        """Letter-name distance from the root (0 = unison, 2 = third, ...)."""
        return _ROLE_INFO[self][1]

    @property
    def is_altered(self) -> bool:
        return self in _ALTERED_ROLES

    @property
    def family(self) -> str:
        """Coarse family used for display grouping: root/third/fifth/seventh/extension/other."""
        return _ROLE_INFO[self][2]


_ROLE_INFO: dict[ChordToneRole, tuple[str, int | None, str]] = {
    ChordToneRole.ROOT: ("1", 0, "root"),
    ChordToneRole.SECOND: ("2", 1, "suspension"),
    ChordToneRole.MINOR_THIRD: ("b3", 2, "third"),
    ChordToneRole.MAJOR_THIRD: ("3", 2, "third"),
    ChordToneRole.FOURTH: ("4", 3, "suspension"),
    ChordToneRole.DIMINISHED_FIFTH: ("b5", 4, "fifth"),
    ChordToneRole.PERFECT_FIFTH: ("5", 4, "fifth"),
    ChordToneRole.AUGMENTED_FIFTH: ("#5", 4, "fifth"),
    ChordToneRole.SIXTH: ("6", 5, "sixth"),
    ChordToneRole.DIMINISHED_SEVENTH: ("bb7", 6, "seventh"),
    ChordToneRole.MINOR_SEVENTH: ("b7", 6, "seventh"),
    ChordToneRole.MAJOR_SEVENTH: ("7", 6, "seventh"),
    ChordToneRole.FLAT_NINTH: ("b9", 1, "extension"),
    ChordToneRole.NINTH: ("9", 1, "extension"),
    ChordToneRole.SHARP_NINTH: ("#9", 1, "extension"),
    ChordToneRole.ELEVENTH: ("11", 3, "extension"),
    ChordToneRole.SHARP_ELEVENTH: ("#11", 3, "extension"),
    ChordToneRole.FLAT_THIRTEENTH: ("b13", 5, "extension"),
    ChordToneRole.THIRTEENTH: ("13", 5, "extension"),
    ChordToneRole.SLASH_BASS: ("/", None, "other"),
    ChordToneRole.NON_CHORD_TONE: ("x", None, "other"),
}

_ALTERED_ROLES = frozenset({
    ChordToneRole.DIMINISHED_FIFTH,
    ChordToneRole.AUGMENTED_FIFTH,
    ChordToneRole.FLAT_NINTH,
    ChordToneRole.SHARP_NINTH,
    ChordToneRole.SHARP_ELEVENTH,
    ChordToneRole.FLAT_THIRTEENTH,
})

# Unreduced template interval (semitones above the root) -> role.
_SEMITONE_ROLES: dict[int, ChordToneRole] = {
    0: ChordToneRole.ROOT,
    2: ChordToneRole.SECOND,
    3: ChordToneRole.MINOR_THIRD,
    4: ChordToneRole.MAJOR_THIRD,
    5: ChordToneRole.FOURTH,
    6: ChordToneRole.DIMINISHED_FIFTH,
    7: ChordToneRole.PERFECT_FIFTH,
    8: ChordToneRole.AUGMENTED_FIFTH,
    9: ChordToneRole.SIXTH,
    10: ChordToneRole.MINOR_SEVENTH,
    11: ChordToneRole.MAJOR_SEVENTH,
    13: ChordToneRole.FLAT_NINTH,
    14: ChordToneRole.NINTH,
    15: ChordToneRole.SHARP_NINTH,
    17: ChordToneRole.ELEVENTH,
    18: ChordToneRole.SHARP_ELEVENTH,
    20: ChordToneRole.FLAT_THIRTEENTH,
    21: ChordToneRole.THIRTEENTH,
}

# Quality-specific readings of an ambiguous semitone size.
_QUALITY_OVERRIDES: dict[tuple[str, int], ChordToneRole] = {
    ("dim7", 9): ChordToneRole.DIMINISHED_SEVENTH,
}


def is_seventh_quality(quality: str) -> bool:
    """True when the template contains a seventh (b7, 7 or the bb7 of dim7).

    Passed to ``detect_chord_inversion`` so that voicings without a fifth
    (shell, rootless, incomplete) still receive seventh-chord figures.
    """
    from ..theory.chord import CHORD_TEMPLATES

    intervals = CHORD_TEMPLATES[quality]["theoretical"]
    return quality == "dim7" or any(s % 12 in (10, 11) and s < 12 for s in intervals)


def role_for_interval(quality: str, semitones: int) -> ChordToneRole:
    """Role of one unreduced template interval inside a canonical chord quality."""
    override = _QUALITY_OVERRIDES.get((quality, semitones))
    if override is not None:
        return override
    try:
        return _SEMITONE_ROLES[semitones]
    except KeyError as exc:
        raise ChordConstructionError(
            f"No chord-tone role is defined for {semitones} semitones in quality {quality!r}."
        ) from exc


def inversion_for_bass(
    chord: ChordDefinition, notes: tuple[int, ...], role: ChordToneRole,
) -> InversionAnalysis | None:
    """Apply figures to the actual bass factor of the declared chord."""
    root_pc = int(chord.root.pitch_class)
    seventh = is_seventh_quality(chord.quality)
    if role.family in {"root", "third", "fifth", "seventh"}:
        return detect_chord_inversion(notes, root_pitch_class=root_pc, is_seventh=seventh)
    if role.family in {"sixth", "extension"}:
        return None
    bass_pc = notes[0] % 12
    distance = (bass_pc - root_pc) % 12
    suspended = role.family == "suspension"
    return InversionAnalysis(
        inversion=ChordInversion.ROOT_POSITION,
        figured_bass="slash",
        bass_factor="SUSPENSION" if suspended else "NON_CHORD_TONE",
        root_pc=root_pc,
        bass_pc=bass_pc,
        german_name=f"Vorhalt im Bass ({distance})" if suspended else f"Orgelpunkt / Fremdbass ({distance})",
        is_seventh_chord=seventh,
    )


@dataclass(frozen=True)
class ChordTone:
    """One theoretical chord tone with its role, pitch class and written spelling."""

    role: ChordToneRole
    semitones: int
    pitch_class: int
    spelling: Optional[NoteSpelling]  # None if the core cannot spell it (beyond double accidentals)

    def name(self, convention: Convention) -> str:
        if self.spelling is None:
            return "?"
        return strip_octave(self.spelling.render(convention))


def strip_octave(rendered: str) -> str:
    return rendered.rstrip("0123456789").removesuffix("-")


def spell_chord_tone(root: NoteSpelling, role: ChordToneRole, semitones: int) -> Optional[NoteSpelling]:
    """Spell ``semitones`` above ``root`` on the letter implied by ``role``."""
    steps = role.diatonic_steps
    if steps is None:
        return None
    try:
        return root.transpose_diatonic(step_delta=steps, semitone_delta=semitones % 12 if steps else 0)
    except MusicTheoryError:
        return None


def chord_tones(chord: ChordDefinition) -> tuple[ChordTone, ...]:
    """Theoretical tones of ``chord`` in template order, spelled from its root."""
    tones = []
    root_pc = int(chord.root.pitch_class)
    for semitones in chord.theoretical_intervals:
        role = role_for_interval(chord.quality, semitones)
        tones.append(ChordTone(role, semitones, (root_pc + semitones) % 12, spell_chord_tone(chord.root, role, semitones)))
    return tuple(tones)


def render_chord_symbol(chord: ChordDefinition, convention: Convention) -> str:
    """Chord symbol in INT or DE note names; quality text follows ``ChordDefinition.symbol``."""
    if convention == "INT":
        return chord.symbol
    international = chord.symbol
    root_int = strip_octave(chord.root.render("INT"))
    body, _, _ = international.partition("/")
    quality_text = body[len(root_int):]
    text = strip_octave(chord.root.render("DE")) + quality_text
    if chord.bass is not None:
        text += "/" + strip_octave(chord.bass.render("DE"))
    return text


def spell_at(spelling: NoteSpelling, midi: int) -> NoteSpelling:
    """Keep the letter and accidental of ``spelling`` but move it to sounding pitch ``midi``."""
    delta = midi - spelling.midi_number
    if delta % 12:
        raise MusicTheoryError(f"Spelling {spelling} has pitch class {spelling.pitch_class}, not {midi % 12}.")
    return NoteSpelling(spelling.step, spelling.alteration, spelling.octave + delta // 12)


@dataclass(frozen=True)
class VoicedNote:
    """One sounding note of a concrete voicing with its musical meaning."""

    midi: int
    role: ChordToneRole
    spelling: Optional[NoteSpelling]
    is_root: bool
    is_bass: bool

    def name(self, convention: Convention, with_octave: bool = True) -> str:
        if self.spelling is None:
            return "?"
        rendered = self.spelling.render(convention)
        return rendered if with_octave else strip_octave(rendered)


@dataclass(frozen=True)
class LabeledVoicing:
    """A concrete voicing (MIDI notes) labelled against its chord definition."""

    chord: ChordDefinition
    notes: tuple[VoicedNote, ...]
    inversion: Optional[InversionAnalysis]
    omitted_roles: tuple[ChordToneRole, ...]  # theoretical tones absent from this voicing
    foreign_notes: tuple[int, ...]  # sounding notes that are neither chord tone nor written bass

    @property
    def midi_notes(self) -> tuple[int, ...]:
        return tuple(note.midi for note in self.notes)

    @property
    def bass(self) -> VoicedNote:
        return self.notes[0]

    @property
    def root_midis(self) -> tuple[int, ...]:
        return tuple(note.midi for note in self.notes if note.is_root)


def label_voicing(chord: ChordDefinition, notes: Iterable[int] | Voicing) -> LabeledVoicing:
    """Attach role and contextual spelling to every MIDI note of a concrete voicing.

    Root and bass are kept apart: in C/E the root role belongs to every C, while
    the bass flag belongs only to the lowest sounding note (E).
    """
    midi_notes = sorted_unique_notes(notes.notes if isinstance(notes, Voicing) else notes)
    if not midi_notes:
        raise ChordConstructionError("A labelled voicing needs at least one note.")
    tones = {tone.pitch_class: tone for tone in chord_tones(chord)}
    bass_midi = midi_notes[0]
    labelled: list[VoicedNote] = []
    foreign: list[int] = []
    for midi in midi_notes:
        tone = tones.get(midi % 12)
        if tone is not None:
            role, spelling = tone.role, tone.spelling
        elif chord.bass is not None and midi % 12 == int(chord.bass.pitch_class):
            role, spelling = ChordToneRole.SLASH_BASS, chord.bass
        else:
            role, spelling = ChordToneRole.NON_CHORD_TONE, None
            foreign.append(midi)
        positioned = spell_at(spelling, midi) if spelling is not None else None
        labelled.append(VoicedNote(midi, role, positioned, role is ChordToneRole.ROOT, midi == bass_midi))
    present = {midi % 12 for midi in midi_notes}
    omitted = tuple(tone.role for tone in tones.values() if tone.pitch_class not in present)
    inversion = inversion_for_bass(chord, midi_notes, labelled[0].role)
    return LabeledVoicing(chord, tuple(labelled), inversion, omitted, tuple(foreign))


@dataclass(frozen=True)
class ScaleTone:
    degree: int  # 1-based scale degree
    pitch_class: int
    spelling: NoteSpelling


def scale_tones(scale: ScaleDefinition) -> tuple[ScaleTone, ...]:
    return tuple(
        ScaleTone(index + 1, int(spelling.pitch_class), spelling)
        for index, spelling in enumerate(scale.spellings)
    )


def spelling_for_midi(midi: int, contexts: Sequence[dict[int, NoteSpelling]]) -> Optional[NoteSpelling]:
    """First contextual spelling (by pitch class) that applies, moved to ``midi``."""
    for context in contexts:
        spelling = context.get(midi % 12)
        if spelling is not None:
            return spell_at(spelling, midi)
    return None


__all__ = [
    "ChordTone",
    "ChordToneRole",
    "LabeledVoicing",
    "ScaleTone",
    "VoicedNote",
    "chord_tones",
    "label_voicing",
    "render_chord_symbol",
    "role_for_interval",
    "scale_tones",
    "spell_at",
    "spell_chord_tone",
    "spelling_for_midi",
    "strip_octave",
]
