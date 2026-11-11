"""
STEPS Progression Core: Progression Engine, Canonical Archetypes & Voice-Leading Sequencer.

Adheres to:
- M05 (Harmonielehre), M06 (Voice Leading), M09 (Genre-Atlas)
- Canonical Progression Library: PROG-001 through PROG-028
- Golden Reference Cases: REF-0019, REF-0021, REF-0023..0026, REF-0065, REF-0095..0097
- Strict Preservation of PROG-021 and PROG-028
"""

from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Literal, Optional, List, Dict, Any, Tuple

from ..theory.exceptions import ProgressionParsingError, ChordConstructionError
from ..theory.pitch import NoteSpelling, PitchClass, parse_spelling, DIATONIC_BASE_PC
from ..theory.chord import ChordDefinition, Voicing, parse_chord
from .voice_leading import (
    VoiceLeadingStyle,
    absolute_semitone_distance,
    circular_pc_distance,
    detect_voice_crossing,
    detect_parallel_fifths_octaves,
    optimize_smooth_voice_leading
)


# Canonical registry data for all 28 progressions from CHORD_PROGRESSION_REFERENCE_LIBRARY.md
CANONICAL_PROGRESSION_DEFINITIONS: list[dict[str, str]] = [
    {
        'id': 'PROG-001',
        'name': 'Pop Four Chords',
        'roman': 'I - V - vi - IV',
        'default_key': 'C',
        'chords': 'C - G - Am - F',
        'context': 'Pop, Rock, Singer-Songwriter',
        'sources': 'Piston (1987), Kostka (2013)'
    },
    {
        'id': 'PROG-002',
        'name': 'Emotional Minor Loop',
        'roman': 'vi - IV - I - V',
        'default_key': 'C',
        'chords': 'Am - F - C - G',
        'context': 'Pop-Balladen, Melodic EDM',
        'sources': 'Tagg (2014)'
    },
    {
        'id': 'PROG-003',
        'name': 'Jazz Two-Five-One',
        'roman': 'ii^7 - V^7 - I^maj7',
        'default_key': 'C',
        'chords': 'Dm7 - G7 - Cmaj7',
        'context': 'Jazz, Bebop, Neo-Soul',
        'sources': 'Levine (1995), Nettles (1997)'
    },
    {
        'id': 'PROG-004',
        'name': '50s Doo-Wop Loop',
        'roman': 'I - vi - IV - V',
        'default_key': 'C',
        'chords': 'C - Am - F - G',
        'context': 'Doo-Wop, R&B, 50s Pop',
        'sources': 'Aldwell/Schachter (1989)'
    },
    {
        'id': 'PROG-005',
        'name': 'Andalusische Kadenz',
        'roman': 'i - bVII - bVI - V',
        'default_key': 'Am',
        'chords': 'Am - G - F - E',
        'context': 'Flamenco, Rock, Latin',
        'sources': 'Gauldin (2004)'
    },
    {
        'id': 'PROG-006',
        'name': 'Pachelbel-Sequenz',
        'roman': 'I - V - vi - iii - IV - I - IV - V',
        'default_key': 'D',
        'chords': 'D - A - Bm - F#m - G - D - G - A',
        'context': 'Barock, Klassik, Hochzeitsmusik',
        'sources': 'Fux (1725), Rameau (1722)'
    },
    {
        'id': 'PROG-007',
        'name': 'Dorian Groove Vamp',
        'roman': 'i^7 - IV^7',
        'default_key': 'Dm',
        'chords': 'Dm7 - G7',
        'context': 'Funk, Fusion, Modaler Jazz',
        'sources': 'Pease (2003)'
    },
    {
        'id': 'PROG-008',
        'name': '12-Bar Blues',
        'roman': 'I^7 - IV^7 - I^7 - V^7 - IV^7 - I^7',
        'default_key': 'C',
        'chords': 'C7 - F7 - C7 - G7 - F7 - C7',
        'context': "Traditional Blues, Rock'n'Roll",
        'sources': 'Rawlins/Bahha (2005)'
    },
    {
        'id': 'PROG-009',
        'name': 'Minor Plagal Romance',
        'roman': 'I - IV - iv - I',
        'default_key': 'C',
        'chords': 'C - F - Fm - C',
        'context': 'Romantik, Filmkomposition',
        'sources': 'de la Motte (1976)'
    },
    {
        'id': 'PROG-010',
        'name': 'Secondary Dominant Lift',
        'roman': 'I - V^7/vi - vi - IV',
        'default_key': 'C',
        'chords': 'C - E7 - Am - F',
        'context': 'Gospel, Pop, Soul',
        'sources': 'Kostka/Payne (2013)'
    },
    {
        'id': 'PROG-011',
        'name': 'Modal Interchange Aeolian',
        'roman': 'I - bVI - bVII - I',
        'default_key': 'C',
        'chords': 'C - Ab - Bb - C',
        'context': 'Epic Pop, Rock, Filmmusik',
        'sources': 'Mulholland (2013)'
    },
    {
        'id': 'PROG-012',
        'name': 'Descending Circle of Fifths',
        'roman': 'vi - ii - V - I',
        'default_key': 'C',
        'chords': 'Am - Dm - G - C',
        'context': 'Barock, Jazz, Chanson',
        'sources': 'Rameau (1722), Salzer (1952)'
    },
    {
        'id': 'PROG-013',
        'name': 'Tritone Substitution Cadence',
        'roman': 'ii^7 - bII^7 - I^maj7',
        'default_key': 'C',
        'chords': 'Dm7 - Db7 - Cmaj7',
        'context': 'Modern Jazz, Bebop',
        'sources': 'Levine (1995)'
    },
    {
        'id': 'PROG-014',
        'name': 'Backdoor Resolution (IV)',
        'roman': 'IV - bVII^7 - I',
        'default_key': 'C',
        'chords': 'F - Bb7 - C',
        'context': 'R&B, Pop, Soul',
        'sources': 'Terefenko (2014)'
    },
    {
        'id': 'PROG-015',
        'name': 'Royal Road (Ōdō shinkō)',
        'roman': 'IV^maj7 - V^7 - iii^7 - vi',
        'default_key': 'C',
        'chords': 'Fmaj7 - G7 - Em7 - Am',
        'context': 'J-Pop, Anime, Fusion',
        'sources': 'Jaffe (1996)'
    },
    {
        'id': 'PROG-016',
        'name': 'Coltrane Changes (3-Tonic Cycle)',
        'roman': 'I^maj7 - V^7/bVI - bVI^maj7 - V^7/III - III^maj7',
        'default_key': 'B',
        'chords': 'B - D7 - G - Bb7 - Eb',
        'context': 'Modern Jazz Matrix (Großterzteilung in Z12)',
        'sources': 'Cohn (2012), Tymoczko (2011)'
    },
    {
        'id': 'PROG-017',
        'name': 'Classical Jazz Backdoor ii–V',
        'roman': 'iv^7 - bVII^7 - I^maj7',
        'default_key': 'C',
        'chords': 'Fm7 - Bb7 - Cmaj7',
        'context': 'Jazz-Standards (Lady Bird, Yardbird)',
        'sources': 'Levine (1995), Terefenko (2014)'
    },
    {
        'id': 'PROG-018',
        'name': 'Substitute Backdoor ii–V',
        'roman': 'ii^7 - bVII^7 - I^maj7',
        'default_key': 'C',
        'chords': 'Dm7 - Bb7 - Cmaj7',
        'context': 'Cool Jazz, West Coast',
        'sources': 'Rawlins/Bahha (2005)'
    },
    {
        'id': 'PROG-019',
        'name': 'Minor Line Cliché',
        'roman': 'i - i^(maj7) - i^7 - i^6',
        'default_key': 'Am',
        'chords': 'Am - Am(maj7) - Am7 - Am6',
        'context': 'Bossa Nova, Spy Film, Ballade',
        'sources': 'Levine (1995)'
    },
    {
        'id': 'PROG-020',
        'name': 'Extended Tritone Sub (Altered)',
        'roman': 'ii^9 - bII^7(alt) - I^maj9',
        'default_key': 'C',
        'chords': 'Dm9 - Db7(#11) - Cmaj9',
        'context': 'Contemporary Jazz',
        'sources': 'Levine (1995), Pease (2003)'
    },
    {
        'id': 'PROG-021',
        'name': 'Neo-Soul Rootless Minor Cycle',
        'roman': 'i^9 - iv^9 - bVI^maj9 - V^7(b9)',
        'default_key': 'Dm',
        'chords': 'Dm9 - Gm9 - Bbmaj9 - A7(b9)',
        'context': 'Neo-Soul, R&B, Lo-Fi',
        'sources': 'Mulholland (2013)'
    },
    {
        'id': 'PROG-022',
        'name': 'Picardy Third Resolution',
        'roman': 'i - iv - bVII - I',
        'default_key': 'Dm',
        'chords': 'Dm - Gm - C - D',
        'context': 'Barock, Renaissance, Folk',
        'sources': 'Aldwell/Schachter (1989)'
    },
    {
        'id': 'PROG-023',
        'name': 'Liquid D&B Sub-Pulse Cadence',
        'roman': 'i^7 - bVI^maj7 - bVII - i',
        'default_key': 'Fm',
        'chords': 'Fm7 - Dbmaj7 - Eb - Fm',
        'context': 'Drum & Bass, UK Bass',
        'sources': 'Butterfield (2010)'
    },
    {
        'id': 'PROG-024',
        'name': 'Bossa Nova Applied Dominant',
        'roman': 'I^maj7 - V^7/V - ii^7 - V^7 - I^maj7',
        'default_key': 'C',
        'chords': 'Cmaj7 - D7 - Dm7 - G7 - Cmaj7',
        'context': 'Bossa Nova (Girl from Ipanema)',
        'sources': 'Mauleón (1993), Jobim (1962)'
    },
    {
        'id': 'PROG-025',
        'name': 'Afro-Cuban Minor Ostinato Vamp',
        'roman': 'i - iv - V^7 - iv',
        'default_key': 'Cm',
        'chords': 'Cm - Fm - G7 - Fm',
        'context': 'Salsa, Afro-Cuban, Mambo (Montuno)',
        'sources': 'Mauleón (1993), Peñalosa (2009)'
    },
    {
        'id': 'PROG-026',
        'name': 'Secondary Dominant Chromatic Bassline',
        'roman': 'I - V^7/V(6/5) - ii^6 - [I^6] - V^7 - I',
        'default_key': 'G',
        'chords': 'G - A7/C# - Am/C - G/B - D7/A - G',
        'context': 'Barock, Klassik, Latin Jazz',
        'sources': 'Kostka (2013), Aldwell (1989)'
    },
    {
        'id': 'PROG-027',
        'name': 'Minor Jazz Blues Submediant Turnaround',
        'roman': 'i^7 - iv^7 - i^7 - bVI^maj7 - V^7(alt) - i^7',
        'default_key': 'Cm',
        'chords': 'Cm7 - Fm7 - Cm7 - Abmaj7 - G7(#11) - Cm7',
        'context': "Minor Blues (Birk's Works, Footprints)",
        'sources': 'Levine (1995), Terefenko (2014)'
    },
    {
        'id': 'PROG-028',
        'name': 'Circle of Fifths Soul Cycle',
        'roman': 'i^9 - iv^9 - bVII^9 - III^maj9',
        'default_key': 'Em',
        'chords': 'Em9 - Am9 - D9 - Gmaj9',
        'context': 'Neo-Soul, Jazz-Funk, Contemporary R&B',
        'sources': 'Mulholland (2013), Levine (1995)'
    }
]


@dataclass(frozen=True)
class CanonicalProgression:
    """
    Represents a canonical progression archetype with both harmonic analysis
    and concrete realization.
    """
    prog_id: str
    name: str
    roman_numerals: str
    default_key: str
    chords_str: str
    context: str
    sources: str

    @property
    def chord_definitions(self) -> list[ChordDefinition]:
        chord_symbols = [c.strip() for c in self.chords_str.split('-')]
        return [parse_chord(s) for s in chord_symbols if s]

    def transpose(self, semitones: int) -> list[ChordDefinition]:
        """Transposes all chords in the progression by a chromatic semitone offset."""
        result = []
        for chord in self.chord_definitions:
            new_root = chord.root.transpose_chromatic(semitones)
            new_bass = chord.bass.transpose_chromatic(semitones) if chord.bass else None
            result.append(ChordDefinition(root=new_root, quality=chord.quality, bass=new_bass))
        return result


def _build_registry() -> Dict[str, CanonicalProgression]:
    reg = {}
    for d in CANONICAL_PROGRESSION_DEFINITIONS:
        p = CanonicalProgression(
            prog_id=d['id'],
            name=d['name'],
            roman_numerals=d['roman'],
            default_key=d['default_key'],
            chords_str=d['chords'],
            context=d['context'],
            sources=d['sources']
        )
        reg[d['id']] = p
    return reg


CANONICAL_PROGRESSIONS: Dict[str, CanonicalProgression] = _build_registry()


def get_progression(prog_id: str) -> CanonicalProgression:
    """Retrieves a canonical progression by ID (e.g. 'PROG-001' .. 'PROG-028')."""
    p = CANONICAL_PROGRESSIONS.get(prog_id.upper())
    if p is None:
        raise ProgressionParsingError(f"Progression '{prog_id}' not found in canonical library.")
    return p


def list_progressions() -> list[CanonicalProgression]:
    """Returns all 28 canonical progressions in order."""
    return [CANONICAL_PROGRESSIONS[f"PROG-{i:03d}"] for i in range(1, 29)]


def resolve_roman_degree(
    degree_str: str,
    key_root: str | NoteSpelling = 'C',
    is_minor_key: bool = False
) -> ChordDefinition:
    """
    Parses a Roman numeral scale degree in a given key into a ChordDefinition.
    
    Supports:
      - Major: I, ii, iii, IV, V, vi, vii° / viib5
      - Minor: i, ii°, bIII, iv, v, V, bVI, bVII, vii°
      - Extensions: ^7, 7, maj7, ^9, 9, m9, 7(b9), 7(#11)
      - Secondary dominants: V7/vi, V7/V, V7/ii
      - Alterations/Substitutions: bII7 (tritone sub), iv (minor plagal)
    """
    if isinstance(key_root, str):
        key_spelling = parse_spelling(key_root + '4')
    else:
        key_spelling = key_root
        
    cleaned = degree_str.strip()
    if not cleaned:
        raise ProgressionParsingError("Empty Roman numeral degree.")

    # 1. Secondary Dominant check: e.g. V7/V, V7/vi, V^7/bVI
    if '/' in cleaned:
        dom_part, target_part = cleaned.split('/', 1)
        target_chord = resolve_roman_degree(target_part, key_spelling, is_minor_key)
        # The secondary dominant has root a Perfect 5th above the target chord's root
        dom_root = target_chord.root.transpose_diatonic(step_delta=4, semitone_delta=7)
        dom_quality = re.sub(r"^[vViI]+(?:\^)?", "", dom_part).replace('(', '').replace(')', '')
        q = dom_quality if dom_quality else '7'
        return ChordDefinition(root=dom_root, quality=q)

    # 2. Extract leading accidental (e.g. 'b', '#')
    acc_match = re.match(r"^([b#]+)?([ivIV]+)(.*)$", cleaned)
    if not ac_match if (ac_match := re.match(r"^([b#]+)?([ivIV]+)(.*)$", cleaned)) else False:
        pass
        
    m = re.match(r"^([b#]+)?([ivIV]+)(.*)$", cleaned)
    if not m:
        raise ProgressionParsingError(f"Cannot parse Roman numeral: '{degree_str}'")
        
    acc = m.group(1) or ''
    roman = m.group(2)
    ext = m.group(3) or ''
    
    # Scale degree offset in major scale (diatonic)
    roman_upper = roman.upper()
    degree_map = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7}
    if roman_upper not in degree_map:
        raise ProgressionParsingError(f"Unknown Roman numeral degree: '{roman}'")
    deg_num = degree_map[roman_upper]
    
    # Scale degree calculation:
    # Standard music theory convention (Kostka, Levine):
    # When an explicit accidental prefix is present ('b' or '#', e.g. 'bVI', 'bVII', 'bIII', 'bII', '#IV'),
    # the accidental applies relative to the major scale degree root.
    major_diatonic_semis = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
    minor_diatonic_semis = {1: 0, 2: 2, 3: 3, 4: 5, 5: 7, 6: 8, 7: 10}
    
    if acc:
        base_semi = major_diatonic_semis[deg_num]
        shift = 0
        if acc == 'b':
            shift = -1
        elif acc == 'bb':
            shift = -2
        elif acc == '#':
            shift = 1
        target_semi = base_semi + shift
    else:
        target_semi = minor_diatonic_semis[deg_num] if is_minor_key else major_diatonic_semis[deg_num]
        
    target_step_delta = deg_num - 1
    chord_root = key_spelling.transpose_diatonic(step_delta=target_step_delta, semitone_delta=target_semi)
    
    # Clean extensions
    ext_clean = ext.replace('^', '').replace('(', '').replace(')', '').strip()
    is_lower = roman.islower()
    
    # Default quality based on case and degree
    if is_lower:
        # Minor-type default
        if 'b5' in ext_clean or '°' in ext_clean or 'dim' in ext_clean:
            default_q = 'm7b5' if '7' in ext_clean else 'dim'
        elif '9' in ext_clean:
            default_q = 'm9'
        elif '7' in ext_clean:
            default_q = 'm(maj7)' if 'maj' in ext_clean else 'm7'
        elif '6' in ext_clean:
            default_q = 'm6'
        else:
            default_q = 'm'
    else:
        # Major/Dominant-type default
        if deg_num == 5:
            # V degree is dominant by default
            if 'b9' in ext_clean:
                default_q = '7b9'
            elif '9' in ext_clean:
                default_q = '9'
            elif '13' in ext_clean:
                default_q = '13'
            else:
                default_q = '7'
        else:
            if 'maj9' in ext_clean or '9' in ext_clean and 'maj' in ext_clean:
                default_q = 'maj9'
            elif 'maj7' in ext_clean or '7' in ext_clean:
                default_q = 'maj7' if deg_num in (1, 4) else '7'
            elif 'add9' in ext_clean:
                default_q = 'add9'
            elif 'sus4' in ext_clean:
                default_q = 'sus4'
            else:
                default_q = ''
                
    # If explicit extension specified, map it
    if ext_clean in ('7', 'maj7', 'm7', 'm7b5', 'dim7', '9', 'maj9', 'm9', '7b9', '7#11', '7#9', '13', 'maj13'):
        final_q = ext_clean
    else:
        final_q = default_q
        
    return ChordDefinition(root=chord_root, quality=final_q)


def generate_progression_voicings(
    chords: list[ChordDefinition] | CanonicalProgression,
    style: VoiceLeadingStyle = VoiceLeadingStyle.JAZZ_POP,
    initial_voicing_type: Literal['CLOSE', 'DROP2', 'SHELL', 'ROOTLESS'] = 'CLOSE',
    bass_octave: int = 3
) -> list[Voicing]:
    """
    Synthesizes a smoothly voice-led sequence of Voicings for the given progression.
    Uses optimize_smooth_voice_leading to find the minimal-distance transitions.
    """
    chord_list = chords.chord_definitions if isinstance(chords, CanonicalProgression) else chords
    if not chord_list:
        return []

    voicings: list[Voicing] = []
    
    # 1. Generate initial voicing
    first_chord = chord_list[0]
    initial_voicing = first_chord.to_voicing(bass_octave=bass_octave, voicing_type=initial_voicing_type)
    voicings.append(initial_voicing)
    
    # 2. Iteratively voice-lead each subsequent chord
    for chord in chord_list[1:]:
        prev_notes = voicings[-1].midi_notes
        target_pcs = chord.voiced_pitch_classes
        bass_pc = int(chord.bass.pitch_class) if chord.bass else int(chord.root.pitch_class)
        
        # Optimize voice leading from previous voicing
        next_notes = optimize_smooth_voice_leading(
            source_voicing=prev_notes,
            target_pcs=target_pcs,
            bass_pc=bass_pc,
            style=style
        )
        voicings.append(Voicing(notes=tuple(next_notes), voicing_type=initial_voicing_type))
        
    return voicings


def analyze_progression_voice_leading(
    voicings: list[Voicing],
    style: VoiceLeadingStyle = VoiceLeadingStyle.JAZZ_POP
) -> Dict[str, Any]:
    """
    Analyzes voice-leading smoothness, distances, crossings, and parallel violations across a progression.
    """
    if len(voicings) < 2:
        return {
            'total_l1_distance': 0,
            'circular_pc_distance': 0,
            'transition_count': 0,
            'average_l1_step': 0.0,
            'voice_crossings_count': sum(1 for v in voicings if detect_voice_crossing(v.midi_notes)),
            'parallel_violations': []
        }

    total_l1 = 0
    total_circ = 0
    violations = []
    crossings = 0
    max_single_voice_jump = 0

    for i in range(len(voicings) - 1):
        v_a = voicings[i].midi_notes
        v_b = voicings[i + 1].midi_notes
        
        if detect_voice_crossing(v_a):
            crossings += 1
            
        dist_l1 = absolute_semitone_distance(v_a, v_b)
        dist_circ = circular_pc_distance(v_a, v_b)
        total_l1 += dist_l1
        total_circ += dist_circ
        
        for a, b in zip(v_a, v_b):
            max_single_voice_jump = max(max_single_voice_jump, abs(b - a))
            
        viols = detect_parallel_fifths_octaves(v_a, v_b, style=style)
        violations.extend(viols)

    # Check last voicing for crossing
    if detect_voice_crossing(voicings[-1].midi_notes):
        crossings += 1

    transitions = len(voicings) - 1
    n_voices = len(voicings[0].midi_notes)
    avg_step = total_l1 / (transitions * n_voices) if transitions > 0 and n_voices > 0 else 0.0

    return {
        'total_l1_distance': total_l1,
        'total_circular_distance': total_circ,
        'transition_count': transitions,
        'average_l1_step_per_voice': round(avg_step, 2),
        'max_single_voice_jump': max_single_voice_jump,
        'voice_crossings_count': crossings,
        'parallel_violations': violations
    }
