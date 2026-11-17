"""
STEPS Music Theory Core: Scales, Modes & Diatonic Harmonization.

Adheres to:
- M03 (Skalen & Modi), M04 (Harmonielehre, Stufentheorie)
- ADR-005 (Explicit DE/INT notation convention separation)
- Pure, UI-independent music domain core
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Literal, Optional, Tuple

from .chord import ChordDefinition, parse_chord
from .exceptions import (
    ChordConstructionError,
    MusicTheoryError,
    ScaleConstructionError,
)
from .pitch import (
    DIATONIC_BASE_PC,
    DIATONIC_STEPS,
    NoteSpelling,
    PitchClass,
    parse_spelling,
)


class ModeCategory(str, Enum):
    DIATONIC_MAJOR = "DIATONIC_MAJOR"
    DIATONIC_MINOR = "DIATONIC_MINOR"
    MELODIC_MINOR = "MELODIC_MINOR"
    HARMONIC_MINOR = "HARMONIC_MINOR"
    PENTATONIC = "PENTATONIC"
    BLUES = "BLUES"
    SYMMETRIC = "SYMMETRIC"


@dataclass(frozen=True)
class ScaleTemplate:
    """Canonical definition of a scale structure."""
    name: str
    aliases: tuple[str, ...]
    intervals: tuple[int, ...]  # Semitones from root (e.g. 0, 2, 4, 5, 7, 9, 11)
    category: ModeCategory
    characteristic_intervals: tuple[int, ...]  # Identifying intervals
    avoid_notes: tuple[int, ...]  # Semitones of avoid notes in modal jazz / counterpoint
    triad_qualities: tuple[str, ...]  # Diatonic triads I..VII (if 7-tone)
    seventh_qualities: tuple[str, ...]  # Diatonic 7ths I..VII (if 7-tone)


# Comprehensive registry of standard scales and church modes
SCALE_TEMPLATES: Dict[str, ScaleTemplate] = {
    # Diatonic Church Modes (Major basis)
    "ionian": ScaleTemplate(
        name="ionian",
        aliases=("ionian", "major", "dur", "major_scale", "dur_skala"),
        intervals=(0, 2, 4, 5, 7, 9, 11),
        category=ModeCategory.DIATONIC_MAJOR,
        characteristic_intervals=(4, 11),  # Major 3rd and Major 7th
        avoid_notes=(5,),  # Perfect 4th over major triad is avoid note in classical/jazz
        triad_qualities=("", "m", "m", "", "", "m", "dim"),
        seventh_qualities=("maj7", "m7", "m7", "maj7", "7", "m7", "m7b5")
    ),
    "dorian": ScaleTemplate(
        name="dorian",
        aliases=("dorian", "dorisch"),
        intervals=(0, 2, 3, 5, 7, 9, 10),
        category=ModeCategory.DIATONIC_MINOR,
        characteristic_intervals=(3, 9),  # Minor 3rd with Major 6th
        avoid_notes=(),  # Dorian has no strict avoid note; 6th is characteristic
        triad_qualities=("m", "m", "", "", "m", "dim", ""),
        seventh_qualities=("m7", "m7", "maj7", "7", "m7", "m7b5", "maj7")
    ),
    "phrygian": ScaleTemplate(
        name="phrygian",
        aliases=("phrygian", "phrygisch"),
        intervals=(0, 1, 3, 5, 7, 8, 10),
        category=ModeCategory.DIATONIC_MINOR,
        characteristic_intervals=(1, 3),  # Minor 2nd with Minor 3rd
        avoid_notes=(1, 8),  # Minor 2nd and Minor 6th
        triad_qualities=("m", "", "", "m", "dim", "", "m"),
        seventh_qualities=("m7", "maj7", "7", "m7", "m7b5", "maj7", "m7")
    ),
    "lydian": ScaleTemplate(
        name="lydian",
        aliases=("lydian", "lydisch"),
        intervals=(0, 2, 4, 6, 7, 9, 11),
        category=ModeCategory.DIATONIC_MAJOR,
        characteristic_intervals=(4, 6),  # Major 3rd with Augmented 4th (#4)
        avoid_notes=(),  # Lydian has no avoid note (#4 is consonant colour)
        triad_qualities=("", "", "m", "dim", "", "m", "m"),
        seventh_qualities=("maj7", "7", "m7", "m7b5", "maj7", "m7", "m7")
    ),
    "mixolydian": ScaleTemplate(
        name="mixolydian",
        aliases=("mixolydian", "mixolydisch", "dominant_scale"),
        intervals=(0, 2, 4, 5, 7, 9, 10),
        category=ModeCategory.DIATONIC_MAJOR,
        characteristic_intervals=(4, 10),  # Major 3rd with Minor 7th (b7)
        avoid_notes=(5,),  # 4th is avoid note against major 3rd
        triad_qualities=("", "m", "dim", "", "m", "m", ""),
        seventh_qualities=("7", "m7", "m7b5", "maj7", "m7", "m7", "maj7")
    ),
    "aeolian": ScaleTemplate(
        name="aeolian",
        aliases=("aeolian", "aeolisch", "natural_minor", "reines_moll", "natürliches_moll", "minor", "moll"),
        intervals=(0, 2, 3, 5, 7, 8, 10),
        category=ModeCategory.DIATONIC_MINOR,
        characteristic_intervals=(3, 8),  # Minor 3rd with Minor 6th
        avoid_notes=(8,),  # Minor 6th creates b9 clash with 5th
        triad_qualities=("m", "dim", "", "m", "m", "", ""),
        seventh_qualities=("m7", "m7b5", "maj7", "m7", "m7", "maj7", "7")
    ),
    "locrian": ScaleTemplate(
        name="locrian",
        aliases=("locrian", "lokrisch"),
        intervals=(0, 1, 3, 5, 6, 8, 10),
        category=ModeCategory.DIATONIC_MINOR,
        characteristic_intervals=(1, 6),  # Minor 2nd with Diminished 5th (b5)
        avoid_notes=(1,),  # Minor 2nd
        triad_qualities=("dim", "", "m", "m", "", "", "m"),
        seventh_qualities=("m7b5", "maj7", "m7", "m7", "maj7", "7", "m7")
    ),

    # Minor Scale Variations
    "harmonic_minor": ScaleTemplate(
        name="harmonic_minor",
        aliases=("harmonic_minor", "harmonisches_moll"),
        intervals=(0, 2, 3, 5, 7, 8, 11),
        category=ModeCategory.HARMONIC_MINOR,
        characteristic_intervals=(3, 8, 11),  # Minor 3rd, Minor 6th, Major 7th (leading tone)
        avoid_notes=(8,),
        triad_qualities=("m", "dim", "aug", "m", "", "", "dim"),
        seventh_qualities=("m(maj7)", "m7b5", "maj7#5", "m7", "7", "maj7", "dim7")
    ),
    "melodic_minor": ScaleTemplate(
        name="melodic_minor",
        aliases=("melodic_minor", "melodisches_moll", "jazz_minor"),
        intervals=(0, 2, 3, 5, 7, 9, 11),
        category=ModeCategory.MELODIC_MINOR,
        characteristic_intervals=(3, 9, 11),  # Minor 3rd with Major 6th and Major 7th
        avoid_notes=(),
        triad_qualities=("m", "m", "aug", "", "", "dim", "dim"),
        seventh_qualities=("m(maj7)", "m7", "maj7#5", "7", "7", "m7b5", "m7b5")
    ),

    # Pentatonic & Blues
    "major_pentatonic": ScaleTemplate(
        name="major_pentatonic",
        aliases=("major_pentatonic", "dur_pentatonik", "pentatonic_major"),
        intervals=(0, 2, 4, 7, 9),
        category=ModeCategory.PENTATONIC,
        characteristic_intervals=(4, 9),
        avoid_notes=(),
        triad_qualities=(),
        seventh_qualities=()
    ),
    "minor_pentatonic": ScaleTemplate(
        name="minor_pentatonic",
        aliases=("minor_pentatonic", "moll_pentatonik", "pentatonic_minor"),
        intervals=(0, 3, 5, 7, 10),
        category=ModeCategory.PENTATONIC,
        characteristic_intervals=(3, 10),
        avoid_notes=(),
        triad_qualities=(),
        seventh_qualities=()
    ),
    "blues": ScaleTemplate(
        name="blues",
        aliases=("blues", "blues_scale", "blues_skala"),
        intervals=(0, 3, 5, 6, 7, 10),
        category=ModeCategory.BLUES,
        characteristic_intervals=(3, 6, 10),  # Blue note: dim 5th / tritone (6)
        avoid_notes=(),
        triad_qualities=(),
        seventh_qualities=()
    ),

    # Symmetrical Scales
    "whole_tone": ScaleTemplate(
        name="whole_tone",
        aliases=("whole_tone", "ganzton", "ganztonleiter"),
        intervals=(0, 2, 4, 6, 8, 10),
        category=ModeCategory.SYMMETRIC,
        characteristic_intervals=(2, 4, 6, 8, 10),
        avoid_notes=(),
        triad_qualities=(),
        seventh_qualities=()
    ),
    "diminished_half_whole": ScaleTemplate(
        name="diminished_half_whole",
        aliases=("diminished_half_whole", "halfton_ganzton", "half_whole_diminished"),
        intervals=(0, 1, 3, 4, 6, 7, 9, 10),
        category=ModeCategory.SYMMETRIC,
        characteristic_intervals=(1, 3, 6, 9),
        avoid_notes=(),
        triad_qualities=(),
        seventh_qualities=()
    ),
    "diminished_whole_half": ScaleTemplate(
        name="diminished_whole_half",
        aliases=("diminished_whole_half", "ganzton_halfton", "whole_half_diminished"),
        intervals=(0, 2, 3, 5, 6, 8, 9, 11),
        category=ModeCategory.SYMMETRIC,
        characteristic_intervals=(2, 3, 6, 9, 11),
        avoid_notes=(),
        triad_qualities=(),
        seventh_qualities=()
    )
}

# Lookup alias map
_ALIAS_TO_TEMPLATE: Dict[str, ScaleTemplate] = {}
for _tmpl in SCALE_TEMPLATES.values():
    for _alias in _tmpl.aliases:
        _ALIAS_TO_TEMPLATE[_alias.lower().replace("-", "_").replace(" ", "_")] = _tmpl


def get_scale_template(name_or_alias: str) -> Optional[ScaleTemplate]:
    """Resolves scale template by canonical name or alias."""
    key = name_or_alias.strip().lower().replace("-", "_").replace(" ", "_")
    return _ALIAS_TO_TEMPLATE.get(key)


@dataclass(frozen=True)
class ScaleDefinition:
    """
    Concrete realization of a musical scale from a given root spelling.
    
    Preserves exact diatonic orthography (e.g. C# -> D# -> E# -> F# -> G# -> A# -> B#)
    without enharmonic pitch-class flattening.
    """
    root: NoteSpelling
    template: ScaleTemplate
    spellings: tuple[NoteSpelling, ...]

    def __post_init__(self):
        if not isinstance(self.root, NoteSpelling):
            raise ScaleConstructionError(f"Root must be NoteSpelling, got {type(self.root)}")
        if not isinstance(self.template, ScaleTemplate):
            raise ScaleConstructionError(f"Template must be ScaleTemplate, got {type(self.template)}")

    @property
    def name(self) -> str:
        return self.template.name

    @property
    def intervals(self) -> tuple[int, ...]:
        return self.template.intervals

    @property
    def pitch_classes(self) -> tuple[PitchClass, ...]:
        return tuple(s.pitch_class for s in self.spellings)

    @property
    def midi_notes(self) -> tuple[int, ...]:
        return tuple(s.midi_number for s in self.spellings)

    def get_degree(self, degree: int) -> NoteSpelling:
        """
        Returns the NoteSpelling for the requested scale degree (1-indexed).
        Handles degrees above octave (e.g. 8 = octave, 9 = ninth).
        """
        if not isinstance(degree, int) or degree < 1:
            raise ScaleConstructionError(f"Scale degree must be an integer >= 1, got {degree}")
        
        n = len(self.spellings)
        idx = (degree - 1) % n
        octave_shift = (degree - 1) // n
        base = self.spellings[idx]
        if octave_shift == 0:
            return base
        return NoteSpelling(step=base.step, alteration=base.alteration, octave=base.octave + octave_shift)

    def get_diatonic_triad(self, degree: int) -> ChordDefinition:
        """
        Derives the diatonic triad on the given scale degree (1..7 for heptatonic scales).
        """
        if len(self.spellings) != 7 or not self.template.triad_qualities:
            raise ScaleConstructionError(f"Diatonic triads only defined for 7-tone scales, not {self.name}")
        if not 1 <= degree <= 7:
            raise ScaleConstructionError(f"Degree must be 1..7, got {degree}")
        
        root_spelling = self.get_degree(degree)
        quality = self.template.triad_qualities[degree - 1]
        return ChordDefinition(root=root_spelling, quality=quality)

    def get_diatonic_seventh(self, degree: int) -> ChordDefinition:
        """
        Derives the diatonic seventh chord on the given scale degree (1..7 for heptatonic scales).
        """
        if len(self.spellings) != 7 or not self.template.seventh_qualities:
            raise ScaleConstructionError(f"Diatonic seventh chords only defined for 7-tone scales, not {self.name}")
        if not 1 <= degree <= 7:
            raise ScaleConstructionError(f"Degree must be 1..7, got {degree}")
        
        root_spelling = self.get_degree(degree)
        quality = self.template.seventh_qualities[degree - 1]
        return ChordDefinition(root=root_spelling, quality=quality)

    def render_text(self, convention: Literal['INT', 'DE'] = 'INT', unicode_accidental: bool = False) -> list[str]:
        """Renders notes of the scale in either International or German notation."""
        return [s.render(convention=convention, unicode_accidental=unicode_accidental) for s in self.spellings]


def construct_scale(root: NoteSpelling, template_or_name: ScaleTemplate | str) -> ScaleDefinition:
    """
    Constructs a concrete ScaleDefinition from a root spelling and scale template.
    
    For 7-tone scales, guarantees pure diatonic step progression:
    degree i has step DIATONIC_STEPS[(root_idx + i - 1) % 7].
    """
    if isinstance(template_or_name, str):
        tmpl = get_scale_template(template_or_name)
        if tmpl is None:
            raise ScaleConstructionError(f"Unknown scale or mode: {template_or_name!r}")
    elif isinstance(template_or_name, ScaleTemplate):
        tmpl = template_or_name
    else:
        raise ScaleConstructionError("Expected ScaleTemplate or scale name string.")

    spellings: list[NoteSpelling] = []
    
    # Check if heptatonic (7 steps)
    if len(tmpl.intervals) == 7:
        # Strict diatonic step progression: each letter step used exactly once
        for i, semitones in enumerate(tmpl.intervals):
            spelling = root.transpose_diatonic(step_delta=i, semitone_delta=semitones)
            spellings.append(spelling)
    else:
        # Non-heptatonic scales (pentatonic, blues, symmetric): chromatic transposition with clean accidentals
        for semitones in tmpl.intervals:
            spelling = root.transpose_chromatic(semitones)
            spellings.append(spelling)

    return ScaleDefinition(root=root, template=tmpl, spellings=tuple(spellings))


_SCALE_PATTERNS = {
    "INT": re.compile(r"^([A-Ga-g](?:bb|b|##|#|x|n)?)\s*(?:-|\s+)\s*(.+)$"),
    "DE": re.compile(r"^([A-H](?:isis|is|eses|ses|es|s)?)\s*(?:-|\s+)\s*(.+)$", re.IGNORECASE),
}


def parse_scale(text: str, convention: Literal['INT', 'DE', 'AUTO'] = 'AUTO') -> ScaleDefinition:
    """
    Parses a scale specification such as:
      - 'C Major', 'C Dur', 'C-Dur'
      - 'A Natural Minor', 'A Moll', 'A Aeolian'
      - 'F# Dorian', 'Bb Mixolydian'
      - 'H Dur', 'H-Moll' (German convention)
      - 'Eb Harmonic Minor'
    
    Respects explicit DE/INT notation conventions and detects ambiguities.
    """
    if not isinstance(text, str) or not text.strip():
        raise ScaleConstructionError("Scale name must be non-empty text.")
    clean = text.strip()

    if convention not in ("INT", "DE", "AUTO"):
        raise ScaleConstructionError(f"Unknown convention: {convention!r}")

    def _try_parse(conv: Literal['INT', 'DE']) -> Optional[ScaleDefinition]:
        # Handle formats like "C-Dur" or "C Dur" or "C Major"
        m = _SCALE_PATTERNS[conv].match(clean)
        if not m:
            # Try splitting by space
            parts = clean.split(maxsplit=1)
            if len(parts) == 2:
                root_str, scale_str = parts
            else:
                return None
        else:
            root_str, scale_str = m.groups()

        tmpl = get_scale_template(scale_str)
        if tmpl is None:
            return None

        try:
            root = parse_spelling(root_str, convention=conv)
        except MusicTheoryError:
            return None

        return construct_scale(root, tmpl)

    if convention != "AUTO":
        result = _try_parse(convention)
        if result is None:
            raise ScaleConstructionError(f"Cannot parse scale {clean!r} under {convention} convention.")
        return result

    # AUTO convention: evaluate INT and DE
    candidates = []
    for conv in ("INT", "DE"):
        res = _try_parse(conv)  # type: ignore
        if res is not None:
            candidates.append((conv, res))

    if not candidates:
        raise ScaleConstructionError(f"Cannot parse scale {clean!r} in any recognized notation.")

    if len(candidates) == 2:
        # Check if they result in different notes (e.g. "B Major" in INT is B natural, in DE B flat)
        c1, s1 = candidates[0]
        c2, s2 = candidates[1]
        if s1.root.pitch_class != s2.root.pitch_class:
            raise ScaleConstructionError(
                f"Ambiguous scale symbol {clean!r}: represents different roots in INT and DE. Specify convention explicitly."
            )
        return s1

    return candidates[0][1]
