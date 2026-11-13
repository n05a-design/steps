"""
STEPS Music Theory Core: Comprehensive Chord Engine, Symbols & Voicings.

Adheres to:
- M04 (Akkorde, Erweiterungen, Alterationen, Drop-2, Shell Voicings, Rootless Voicings)
- Golden Reference Cases: REF-0012..0016, REF-0021, REF-0035, REF-0039, REF-0040,
  REF-0043, REF-0049, REF-0050, REF-0138..0147
- Mark Levine (1995): The Jazz Piano Book
"""

from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Literal, Optional, Tuple, List, Set, Dict

from .exceptions import ChordConstructionError, MusicTheoryError, VoiceLeadingError
from .pitch import NoteSpelling, PitchClass, DIATONIC_BASE_PC, _parse_note_name, _UNICODE_TO_ASCII


# Canonical dictionary of standard chord qualities:
# Each entry defines:
#   theoretical_intervals: complete set of scale degrees in semitones from root
#   default_voiced_intervals: standard performance voicing intervals (e.g. omitting 5th in #11)
#   category: 'TRIAD' | 'SEVENTH' | 'EXTENDED' | 'SUSPENDED' | 'ADD'
CHORD_TEMPLATES: Dict[str, Dict[str, any]] = {
    # Triads
    '': {
        'aliases': ['', 'maj', 'M'],
        'theoretical': (0, 4, 7),
        'voiced': (0, 4, 7),
        'category': 'TRIAD'
    },
    'm': {
        'aliases': ['m', 'min', '-'],
        'theoretical': (0, 3, 7),
        'voiced': (0, 3, 7),
        'category': 'TRIAD'
    },
    'dim': {
        'aliases': ['dim', 'o', '°'],
        'theoretical': (0, 3, 6),
        'voiced': (0, 3, 6),
        'category': 'TRIAD'
    },
    'aug': {
        'aliases': ['aug', '+'],
        'theoretical': (0, 4, 8),
        'voiced': (0, 4, 8),
        'category': 'TRIAD'
    },
    'sus4': {
        'aliases': ['sus4', 'sus'],
        'theoretical': (0, 5, 7),
        'voiced': (0, 5, 7),
        'category': 'SUSPENDED'
    },
    'sus2': {
        'aliases': ['sus2'],
        'theoretical': (0, 2, 7),
        'voiced': (0, 2, 7),
        'category': 'SUSPENDED'
    },
    'add9': {
        'aliases': ['add9', 'add2'],
        'theoretical': (0, 4, 7, 14),
        'voiced': (0, 2, 4, 7),
        'category': 'ADD'
    },
    'madd9': {
        'aliases': ['madd9', 'minadd9', '-add9'],
        'theoretical': (0, 3, 7, 14),
        'voiced': (0, 2, 3, 7),
        'category': 'ADD'
    },
    '6': {
        'aliases': ['6', 'maj6'],
        'theoretical': (0, 4, 7, 9),
        'voiced': (0, 4, 7, 9),
        'category': 'ADD'
    },
    'm6': {
        'aliases': ['m6', 'min6', '-6'],
        'theoretical': (0, 3, 7, 9),
        'voiced': (0, 3, 7, 9),
        'category': 'ADD'
    },
    
    # Seventh Chords
    '7': {
        'aliases': ['7', 'dom7'],
        'theoretical': (0, 4, 7, 10),
        'voiced': (0, 4, 7, 10),
        'category': 'SEVENTH'
    },
    'maj7': {
        'aliases': ['maj7', '^7', 'M7', 'Δ', 'Δ7'],
        'theoretical': (0, 4, 7, 11),
        'voiced': (0, 4, 7, 11),
        'category': 'SEVENTH'
    },
    'm7': {
        'aliases': ['m7', 'min7', '-7'],
        'theoretical': (0, 3, 7, 10),
        'voiced': (0, 3, 7, 10),
        'category': 'SEVENTH'
    },
    'm7b5': {
        'aliases': ['m7b5', '-7b5', 'ø', 'ø7', 'half-dim'],
        'theoretical': (0, 3, 6, 10),
        'voiced': (0, 3, 6, 10),
        'category': 'SEVENTH'
    },
    'dim7': {
        'aliases': ['dim7', 'o7', '°7'],
        'theoretical': (0, 3, 6, 9),
        'voiced': (0, 3, 6, 9),
        'category': 'SEVENTH'
    },
    'm(maj7)': {
        'aliases': ['m(maj7)', 'mmaj7', 'm^7', '-^7', 'minmaj7'],
        'theoretical': (0, 3, 7, 11),
        'voiced': (0, 3, 7, 11),
        'category': 'SEVENTH'
    },
    '7#5': {
        'aliases': ['7#5', '7aug', '7+'],
        'theoretical': (0, 4, 8, 10),
        'voiced': (0, 4, 8, 10),
        'category': 'SEVENTH'
    },
    'maj7#5': {
        'aliases': ['maj7#5', '^7#5', 'maj7+'],
        'theoretical': (0, 4, 8, 11),
        'voiced': (0, 4, 8, 11),
        'category': 'SEVENTH'
    },
    '7sus4': {
        'aliases': ['7sus4', '7sus'],
        'theoretical': (0, 5, 7, 10),
        'voiced': (0, 5, 7, 10),
        'category': 'SUSPENDED'
    },
    
    # Extended & Altered Chords
    '9': {
        'aliases': ['9', 'dom9'],
        'theoretical': (0, 4, 7, 10, 14),
        'voiced': (0, 4, 10, 14),  # Standard jazz voicing omits 5th
        'category': 'EXTENDED'
    },
    'maj9': {
        'aliases': ['maj9', '^9', 'M9', 'Δ9'],
        'theoretical': (0, 4, 7, 11, 14),
        'voiced': (0, 4, 11, 14),  # Omits 5th
        'category': 'EXTENDED'
    },
    'm9': {
        'aliases': ['m9', 'min9', '-9'],
        'theoretical': (0, 3, 7, 10, 14),
        'voiced': (0, 3, 10, 14),  # Omits 5th
        'category': 'EXTENDED'
    },
    '7b9': {
        'aliases': ['7b9', '7(b9)', 'dom7b9'],
        'theoretical': (0, 4, 7, 10, 13),
        'voiced': (0, 4, 10, 13),  # Root, 3, b7, b9
        'category': 'EXTENDED'
    },
    '7#9': {
        'aliases': ['7#9', '7(#9)', 'dom7#9', 'hendrix'],
        'theoretical': (0, 4, 7, 10, 15),
        'voiced': (0, 4, 10, 15),  # Root, 3, b7, #9
        'category': 'EXTENDED'
    },
    '7#11': {
        'aliases': ['7#11', '7(#11)', 'lydian_dom'],
        'theoretical': (0, 4, 7, 10, 18),  # 1, 3, 5, b7, #11
        'voiced': (0, 4, 6, 10),          # Standard voicing omits 5th to prevent tritone clash
        'category': 'EXTENDED'
    },
    '7b5': {
        'aliases': ['7b5', '7(b5)'],
        'theoretical': (0, 4, 6, 10),
        'voiced': (0, 4, 6, 10),
        'category': 'SEVENTH'
    },
    '7b13': {
        'aliases': ['7b13', '7(b13)'],
        'theoretical': (0, 4, 7, 10, 20),
        'voiced': (0, 4, 10, 20),
        'category': 'EXTENDED'
    },
    '13': {
        'aliases': ['13', 'dom13'],
        'theoretical': (0, 4, 7, 10, 14, 21),
        'voiced': (0, 4, 10, 14, 21),  # Root, 3, b7, 9, 13
        'category': 'EXTENDED'
    },
    'maj13': {
        'aliases': ['maj13', '^13', 'M13'],
        'theoretical': (0, 4, 7, 11, 14, 21),
        'voiced': (0, 4, 11, 14, 21),
        'category': 'EXTENDED'
    },
    'm11': {
        'aliases': ['m11', 'min11', '-11'],
        'theoretical': (0, 3, 7, 10, 14, 17),
        'voiced': (0, 3, 10, 14, 17),
        'category': 'EXTENDED'
    }
}


ALIAS_MAP = {
    alias: quality
    for quality, template in CHORD_TEMPLATES.items()
    for alias in (quality, *template['aliases'])
}
# Short M/m quality markers carry musical meaning in their case.
_FOLDED_ALIASES = {
    alias.lower(): quality
    for alias, quality in ALIAS_MAP.items()
    if not re.match(r"^[Mm](?:$|[0-9(]|maj|add)", alias, re.IGNORECASE)
}


def _resolve_quality(quality: str) -> str | None:
    return ALIAS_MAP.get(quality, _FOLDED_ALIASES.get(quality.lower()))


@dataclass(frozen=True)
class Voicing:
    """
    Concrete realization of a chord in specific octaves/voices.
    """
    notes: tuple[int, ...]
    voicing_type: Literal['CLOSE', 'DROP2', 'SHELL', 'ROOTLESS', 'OPEN', 'CUSTOM'] = 'CLOSE'
    bass_override: Optional[int] = None

    def __post_init__(self):
        if not isinstance(self.notes, (list, tuple)) or not self.notes:
            raise ChordConstructionError("A voicing must contain at least one note in a list or tuple.")
        if any(not isinstance(note, int) or isinstance(note, bool) or not 0 <= note <= 127 for note in self.notes):
            raise VoiceLeadingError("Voicing notes must be MIDI integers in 0..127.")
        if self.bass_override is not None and (
            type(self.bass_override) is not int or self.bass_override != min(self.notes)
        ):
            raise VoiceLeadingError("Bass override must be the lowest MIDI note as an integer.")
        object.__setattr__(self, "notes", tuple(self.notes))

    @property
    def midi_notes(self) -> list[int]:
        return list(sorted(self.notes))

    @property
    def bass_note(self) -> int:
        return self.bass_override if self.bass_override is not None else min(self.notes)

    @property
    def soprano_note(self) -> int:
        return max(self.notes)

    def transpose(self, semitones: int) -> Voicing:
        if type(semitones) is not int:
            raise VoiceLeadingError("Voicing transposition requires whole semitones.")
        transposed = tuple(n + semitones for n in self.notes)
        transposed_bass = (self.bass_override + semitones) if self.bass_override is not None else None
        return Voicing(notes=transposed, voicing_type=self.voicing_type, bass_override=transposed_bass)

    def invert(self, inversion: int) -> Voicing:
        """Rotate the lowest voices above the top, keeping their pitch classes.

        The rotation count wraps modulo voice count. This operation uses
        register order and does not infer a harmonic root. If the result
        cannot fit in MIDI 0..127, it raises VoiceLeadingError.
        """
        if type(inversion) is not int:
            raise VoiceLeadingError("Voicing rotation count must be an integer.")
        notes = self.midi_notes
        count = inversion % len(notes)
        if count == 0:
            return self
        rotated = notes[count:]
        for note in notes[:count]:
            octaves = (rotated[-1] - note) // 12 + 1
            rotated.append(note + 12 * octaves)
        return Voicing(tuple(rotated), self.voicing_type)


@dataclass(frozen=True)
class ChordDefinition:
    """
    Abstract musical chord definition preserving theoretical pitch-class set,
    orthographic root, optional slash-bass note, and voicing configurations.
    """
    root: NoteSpelling
    quality: str
    bass: Optional[NoteSpelling] = None

    def __post_init__(self):
        norm_q = _resolve_quality(self.quality)
        if norm_q is None:
            raise ChordConstructionError(f"Unsupported chord quality: '{self.quality}'")
        # Override with canonical quality name
        object.__setattr__(self, 'quality', norm_q)

    @property
    def template(self) -> Dict[str, any]:
        return CHORD_TEMPLATES[self.quality]

    @property
    def theoretical_intervals(self) -> tuple[int, ...]:
        """Complete theoretical scale degree intervals in semitones."""
        return self.template['theoretical']

    @property
    def default_voiced_intervals(self) -> tuple[int, ...]:
        """Default performance intervals (may omit natural 5th in altered chords)."""
        return self.template['voiced']

    @property
    def theoretical_pitch_classes(self) -> list[PitchClass]:
        """Full theoretical pitch classes."""
        r = int(self.root.pitch_class)
        return [PitchClass(r + semi) for semi in self.theoretical_intervals]

    @property
    def pitch_class_set(self) -> set[int]:
        """Set of unique integers in Z12 belonging to the theoretical chord."""
        return {int(pc) for pc in self.theoretical_pitch_classes}

    @property
    def voiced_pitch_classes(self) -> list[PitchClass]:
        """Pitch classes used in standard performance voicing."""
        r = int(self.root.pitch_class)
        return [PitchClass(r + semi) for semi in self.default_voiced_intervals]

    @property
    def category(self) -> str:
        return self.template['category']

    @property
    def is_triad(self) -> bool:
        return self.category == 'TRIAD'

    @property
    def is_seventh(self) -> bool:
        return self.category == 'SEVENTH'

    @property
    def is_extended(self) -> bool:
        return self.category == 'EXTENDED'

    @property
    def symbol(self) -> str:
        root_str = self.root.render('INT').removesuffix(str(self.root.octave))
        q_str = self.quality
        if q_str == 'm(maj7)':
            q_disp = 'm(maj7)'
        elif q_str == '7#11':
            q_disp = '7(#11)'
        elif q_str == '7b9':
            q_disp = '7(b9)'
        elif q_str == '7#9':
            q_disp = '7(#9)'
        elif q_str == '7b13':
            q_disp = '7(b13)'
        else:
            q_disp = q_str
            
        base_sym = f"{root_str}{q_disp}"
        if self.bass is not None:
            bass_str = self.bass.render('INT').removesuffix(str(self.bass.octave))
            return f"{base_sym}/{bass_str}"
        return base_sym

    def contains_pitch_class(self, pc: int | PitchClass) -> bool:
        return (int(pc) % 12) in self.pitch_class_set

    def to_voicing(
        self,
        bass_octave: int = 3,
        voicing_type: Literal['CLOSE', 'DROP2', 'SHELL', 'ROOTLESS'] = 'CLOSE'
    ) -> Voicing:
        """Realize a layout in MIDI range. ROOTLESS omits the root from the upper part.

        An explicit slash bass is retained even if it is the root.
        DROP2 requires a valid four-note selection and keeps the highest extension.
        """
        if not isinstance(bass_octave, int) or isinstance(bass_octave, bool) or not -1 <= bass_octave <= 9:
            raise VoiceLeadingError("Bass octave must be an integer in -1..9.")
        root_pc = int(self.root.pitch_class)
        root_note = 12 * (bass_octave + 1) + root_pc
        bass_pc = int(self.bass.pitch_class) if self.bass is not None else root_pc
        bass_note = 12 * (bass_octave + 1) + bass_pc
        intervals = self.default_voiced_intervals

        if voicing_type == 'DROP2':
            if len(intervals) < 4:
                raise VoiceLeadingError("Drop-2 requires a four-tone selection.")
            # Keep the defining third, seventh and highest written extension.
            selection = intervals[:3] + intervals[-1:] if len(intervals) > 4 else intervals
            pcs = sorted({(root_pc + semi) % 12 for semi in selection} | {bass_pc})
            if len(pcs) != 4:
                raise VoiceLeadingError("Drop-2 requires four chord tones including the explicit bass.")
            if self.bass is not None:
                # In a drop-2 voicing, the third note of the close stack becomes the bass.
                start = (pcs.index(bass_pc) - 2) % 4
                first = pcs[start]
            else:
                first = root_pc
            close = sorted((pc - first) % 12 for pc in pcs)
            notes = [root_note - root_pc + first + semi for semi in close]
            notes[2] -= 12
            if self.bass is not None:
                offset = bass_note - min(notes)
                notes = [note + offset for note in notes]
            return Voicing(tuple(sorted(notes)), 'DROP2')

        if voicing_type == 'ROOTLESS':
            pcs = {(root_pc + semi) % 12 for semi in intervals if semi % 12}
            if self.bass is None:
                return Voicing(tuple(sorted(12 * (bass_octave + 2) + pc for pc in pcs)), 'ROOTLESS')
            upper = [bass_note + ((pc - bass_pc) % 12) for pc in pcs - {bass_pc}]
            return Voicing(tuple(sorted([bass_note, *upper])), 'ROOTLESS')

        if voicing_type == 'SHELL':
            # The theoretical order separates triad tones from extensions such as add9.
            recipe = self.theoretical_intervals
            upper_interval = next((semi for semi in recipe if 9 <= semi <= 11), recipe[2])
            pcs = {(root_pc + semi) % 12 for semi in (recipe[1], upper_interval)}
            floor = max(59, bass_note)
            upper = [floor + 1 + ((pc - floor - 1) % 12) for pc in pcs - {bass_pc}]
            return Voicing(tuple(sorted([bass_note, *upper])), 'SHELL', bass_note)

        if voicing_type != 'CLOSE':
            raise VoiceLeadingError(f"Unknown voicing type: {voicing_type!r}.")
        upper = []
        for semi in intervals:
            note = root_note + semi
            if note % 12 == bass_pc:
                continue
            if note <= bass_note:
                note += 12 * ((bass_note - note) // 12 + 1)
            upper.append(note)
        return Voicing(tuple(sorted({bass_note, *upper})), 'CLOSE')


_ROOT_PATTERNS = {
    "INT": re.compile(r"^([A-Ga-g](?:bb|b|##|#|x|n)?)(.*)$"),
    "DE": re.compile(r"^([A-H](?:isis|is|eses|ses|es|s(?!us))?)(.*)$", re.IGNORECASE),
}


def _parse_chord_parts(root_and_quality: str, bass_name: str | None, convention: str) -> ChordDefinition:
    match = _ROOT_PATTERNS[convention].fullmatch(root_and_quality)
    if not match:
        raise ChordConstructionError(f"Cannot identify root in chord symbol: {root_and_quality!r}.")
    root_name, quality = match.groups()
    quality = quality.strip()
    if not re.fullmatch(r"(?:[^()]|\([^()]+\))*", quality):
        raise ChordConstructionError(f"Malformed parentheses in chord symbol: {root_and_quality!r}.")
    canonical = _resolve_quality(quality)
    if canonical is None:
        canonical = _resolve_quality(re.sub(r"[()]", "", quality))
    if canonical is None:
        raise ChordConstructionError(f"Unrecognized chord quality: {quality!r}.")
    try:
        root = _parse_note_name(root_name, convention, 4)
        bass = _parse_note_name(bass_name, convention, 3) if bass_name is not None else None
    except MusicTheoryError as exc:
        raise ChordConstructionError(str(exc)) from exc
    return ChordDefinition(root, canonical, bass)


def parse_chord(symbol: str, convention: Literal['INT', 'DE', 'AUTO'] = 'AUTO') -> ChordDefinition:
    """Parse a chord and optional slash bass under one notation convention."""
    if not isinstance(symbol, str) or not symbol.strip():
        raise ChordConstructionError("Chord symbol must be nonempty text.")
    if convention not in ("INT", "DE", "AUTO"):
        raise ChordConstructionError(f"Unknown notation convention: {convention!r}.")
    root_and_quality, slash, bass = symbol.strip().translate(_UNICODE_TO_ASCII).partition("/")
    parts = (root_and_quality.strip(), bass.strip() if slash else None)
    if convention != "AUTO":
        return _parse_chord_parts(*parts, convention)
    candidates = []
    for notation in ("INT", "DE"):
        try:
            candidates.append(_parse_chord_parts(*parts, notation))
        except ChordConstructionError:
            continue
    if not candidates:
        raise ChordConstructionError(f"Cannot parse chord in one notation convention: {symbol!r}.")
    if len(candidates) == 2 and candidates[0] != candidates[1]:
        raise ChordConstructionError(f"Ambiguous chord symbol {symbol!r}: select DE or INT.")
    return candidates[0]
