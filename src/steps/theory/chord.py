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

from .exceptions import ChordConstructionError, MusicTheoryError
from .pitch import NoteSpelling, PitchClass, parse_spelling, DIATONIC_BASE_PC


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
        'theoretical': (0, 2, 4, 7),
        'voiced': (0, 2, 4, 7),
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
        'aliases': ['7#11', '7(#11)', 'lydian_dom', '7(b5)'],
        'theoretical': (0, 4, 6, 7, 10),  # Full scale set: 1, 3, #11(6), 5(7), b7(10)
        'voiced': (0, 4, 6, 10),          # Standard voicing omits 5th to prevent tritone clash
        'category': 'EXTENDED'
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


def _build_alias_map() -> Dict[str, str]:
    mapping = {}
    for canon_name, data in CHORD_TEMPLATES.items():
        mapping[canon_name.lower()] = canon_name
        for alias in data['aliases']:
            mapping[alias.lower()] = canon_name
    return mapping

ALIAS_MAP = _build_alias_map()


@dataclass(frozen=True)
class Voicing:
    """
    Concrete realization of a chord in specific octaves/voices.
    """
    notes: tuple[int, ...]
    voicing_type: Literal['CLOSE', 'DROP2', 'SHELL', 'ROOTLESS', 'OPEN', 'CUSTOM'] = 'CLOSE'
    bass_override: Optional[int] = None

    def __post_init__(self):
        if not self.notes:
            raise ChordConstructionError("A voicing must contain at least one note.")

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
        transposed = tuple(n + semitones for n in self.notes)
        transposed_bass = (self.bass_override + semitones) if self.bass_override is not None else None
        return Voicing(notes=transposed, voicing_type=self.voicing_type, bass_override=transposed_bass)

    def invert(self, inversion: int) -> Voicing:
        sorted_notes = list(sorted(self.notes))
        n = len(sorted_notes)
        inv = inversion % n
        if inv == 0:
            return self
        rotated = sorted_notes[inv:] + [pitch + 12 for pitch in sorted_notes[:inv]]
        return Voicing(notes=tuple(sorted(rotated)), voicing_type=self.voicing_type)


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
        norm_q = ALIAS_MAP.get(self.quality.lower())
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
        root_str = self.root.render('INT')[:-1]  # omit octave number
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
            bass_str = self.bass.render('INT')[:-1]
            return f"{base_sym}/{bass_str}"
        return base_sym

    def contains_pitch_class(self, pc: int | PitchClass) -> bool:
        return (int(pc) % 12) in self.pitch_class_set

    def to_voicing(
        self,
        bass_octave: int = 3,
        voicing_type: Literal['CLOSE', 'DROP2', 'SHELL', 'ROOTLESS'] = 'CLOSE'
    ) -> Voicing:
        """
        Synthesizes a concrete Voicing in MIDI notes based on requested style.
        """
        root_pc = int(self.root.pitch_class)
        bass_note = (bass_octave + 1) * 12 + (int(self.bass.pitch_class) if self.bass else root_pc)
        
        if voicing_type == 'SHELL':
            # LH: Bass root note
            # RH: 3rd and 7th in octave 4
            intervals = self.default_voiced_intervals
            # 3rd is interval 1, 7th is interval 3 (or 2 if 3-note)
            third_semi = intervals[1]
            seventh_semi = intervals[-1] if len(intervals) >= 4 else intervals[2]
            rh_3rd = 60 + ((root_pc + third_semi) % 12)
            rh_7th = 60 + ((root_pc + seventh_semi) % 12)
            notes = tuple(sorted([bass_note, rh_3rd, rh_7th]))
            return Voicing(notes=notes, voicing_type='SHELL', bass_override=bass_note)
            
        elif voicing_type == 'ROOTLESS':
            # Typically 3rd, 5th, 7th, 9th (Levine Rootless A/B)
            intervals = self.default_voiced_intervals
            upper_notes = []
            for semi in intervals:
                if semi % 12 != 0:  # skip root
                    pc = (root_pc + semi) % 12
                    upper_notes.append(60 + pc)
            return Voicing(notes=tuple(sorted(upper_notes)), voicing_type='ROOTLESS')
            
        elif voicing_type == 'DROP2':
            # Construct 4-note close voicing around octave 4, then drop 2nd from top
            intervals = self.default_voiced_intervals[:4]
            close_notes = sorted([60 + ((root_pc + semi) % 12) for semi in intervals])
            if len(close_notes) == 4:
                # drop 2nd from top (index 2) down 12 semitones
                v0, v1, v2, v3 = close_notes
                notes = tuple(sorted([v0, v1, v2 - 12, v3]))
                return Voicing(notes=notes, voicing_type='DROP2')
            else:
                return Voicing(notes=tuple(close_notes), voicing_type='CLOSE')
                
        else:  # CLOSE
            intervals = self.default_voiced_intervals
            notes = [bass_note]
            for semi in intervals:
                if semi != 0:
                    note_val = bass_note + semi
                    notes.append(note_val)
            return Voicing(notes=tuple(sorted(notes)), voicing_type='CLOSE')


def parse_chord(symbol: str, convention: Literal['INT', 'DE', 'AUTO'] = 'AUTO') -> ChordDefinition:
    """
    Parses a lead-sheet chord symbol into a ChordDefinition.
    
    Examples:
      - 'C', 'Dm', 'G7', 'Cmaj7', 'Bm7b5', 'Bdim7', 'C7#11', 'C7(#11)', 'Dm9', 'G7(b9)', 'C/E', 'G/B'
      - German: 'H7', 'Hm7', 'Bmaj7' (where B is Bb), 'Fis7', 'Esmaj7'
    """
    cleaned = symbol.strip()
    if not cleaned:
        raise ChordConstructionError("Cannot parse empty chord symbol.")
        
    # Check for slash bass: e.g. "C/E" or "Dm7/G"
    bass_spelling: Optional[NoteSpelling] = None
    if '/' in cleaned:
        parts = cleaned.split('/', 1)
        chord_part = parts[0].strip()
        bass_part = parts[1].strip()
        cleaned = chord_part
        # parse bass note
        # append default octave 3 for bass note
        bass_spelling = parse_spelling(bass_part + '3', convention=convention)

    # Heuristic: Match root note letter + optional accidentals
    # International roots: C, D, E, F, G, A, B with #, b, ##, bb
    # German roots: H, B, Cis, Des, Es, As, Fis, etc.
    
    # 1. Try German prefix if starts with H or is explicitly DE or German pattern
    root_spelling: Optional[NoteSpelling] = None
    remaining: str = ''
    
    # Check if string starts with standard sus keyword - if so, it's not German accidental
    is_sus = bool(re.match(r"^[A-Ga-g]sus", cleaned, re.IGNORECASE))
    
    # German detection
    is_german = False
    if not is_sus:
        if convention == 'DE':
            is_german = True
        elif convention == 'AUTO':
            if cleaned.startswith(('H', 'h')):
                is_german = True
            elif re.match(r"^[A-Ga-g](isis|is|eses|es)[a-z0-9]", cleaned, re.IGNORECASE):
                is_german = True
            elif re.match(r"^[EAea](s|ses)[a-z0-9]", cleaned, re.IGNORECASE):
                is_german = True
                
    if is_german:
        m_de = re.match(r"^([A-Ha-h](?:isis|is|eses|ses|es|s)?)(.*)$", cleaned)
        if m_de:
            root_candidate = m_de.group(1)
            try:
                root_spelling = parse_spelling(root_candidate + '4', convention='DE')
                remaining = m_de.group(2)
            except Exception:
                root_spelling = None

    # 2. International prefix match
    if root_spelling is None:
        m_int = re.match(r"^([A-Ga-g])(bb|b|##|#|x)?(.*)$", cleaned)
        if not m_int:
            raise ChordConstructionError(f"Cannot identify root note in chord symbol: '{symbol}'")
        step = m_int.group(1).upper()
        acc = m_int.group(2) or ''
        remaining = m_int.group(3)
        root_spelling = parse_spelling(f"{step}{acc}4", convention='INT')

    # Normalize remaining quality string
    quality_raw = remaining.strip()
    # Remove enclosing parentheses from tensions if any: e.g. 7(b9) -> 7b9, 7(#11) -> 7#11
    quality_cleaned = re.sub(r"[()]", "", quality_raw)
    
    # Direct lookup or alias lookup
    canon_q = ALIAS_MAP.get(quality_cleaned.lower())
    if canon_q is None:
        # Try without lowercase or look for longest prefix
        raise ChordConstructionError(
            f"Unrecognized chord quality/extension '{quality_raw}' in symbol '{symbol}'."
        )
        
    return ChordDefinition(root=root_spelling, quality=canon_q, bass=bass_spelling)
