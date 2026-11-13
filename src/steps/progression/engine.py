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
from typing import TYPE_CHECKING, Literal, Dict, Any

from ..theory.exceptions import ProgressionParsingError, VoiceLeadingError
from ..theory.pitch import NoteSpelling, parse_spelling
from ..theory.chord import ChordDefinition, Voicing, parse_chord
from .voice_leading import (
    VoiceLeadingStyle,
    absolute_semitone_distance,
    circular_pc_distance,
    detect_voice_crossing,
    detect_parallel_fifths_octaves,
    optimize_smooth_voice_leading
)


if TYPE_CHECKING:
    from .reviewed import ApprovedClaim


# The general catalog preserves compatibility independently of pilot publication.
_HISTORICAL_PROGRESSION_DEFINITIONS: list[dict[str, str]] = [
    {
        'id': 'PROG-001',
        'name': 'Pop Four Chords',
        'roman': 'I - V - vi - IV',
        'default_key': 'C',
        'chords': 'C - G - Am - F',
        'context': 'Pop-Loop mit angenommener Tonika C',
        'sources': 'omt-roman-numerals',
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
        'context': 'Jazzkadenz in C-Dur',
        'sources': 'omt-ii-v-i',
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
        'roman': 'Idom7 - IVdom7 - Idom7 - V^7 - IVdom7 - Idom7',
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
        'context': 'Mollsubdominante im Dur-Kontext',
        'sources': 'omt-roman-numerals, omt-chromatic-subdominants',
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
        'roman': 'I^maj7 - V^7/bVI - bVI^maj7 - V^7/bIV - bIV^maj7',
        'default_key': 'B',
        'chords': 'Bmaj7 - D7 - Gmaj7 - Bb7 - Ebmaj7',
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
        'roman': 'i - i^(maj7) - i^7 - im6',
        'default_key': 'Am',
        'chords': 'Am - Am(maj7) - Am7 - Am6',
        'context': 'Bossa Nova, Spy Film, Ballade',
        'sources': 'Levine (1995)'
    },
    {
        'id': 'PROG-020',
        'name': 'Extended Tritone Sub (Altered)',
        'roman': 'ii^9 - bII^7(#11) - I^maj9',
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
        'context': 'Bossa Nova practice schema',
        'sources': 'Historical reference: Mauleón (1993)'
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
        'roman': 'I - V7(6/5)/V - ii6 - I6 - V7(4/3) - I',
        'default_key': 'G',
        'chords': 'G - A7/C# - Am/C - G/B - D7/A - G',
        'context': 'Barock, Klassik, Latin Jazz',
        'sources': 'Kostka (2013), Aldwell (1989)'
    },
    {
        'id': 'PROG-027',
        'name': 'Minor Jazz Blues Submediant Turnaround',
        'roman': 'i^7 - iv^7 - i^7 - bVI^maj7 - V^7(#11) - i^7',
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


@dataclass(frozen=True)
class ReviewedProgression:
    """A checked progression and the associated original learning text."""

    progression: CanonicalProgression
    lesson: str
    source_ids: tuple[str, ...]
    reviewed_on: str
    claims: tuple[ApprovedClaim, ...]
    catalog_version: str


def list_reviewed_progressions() -> tuple[ReviewedProgression, ...]:
    """Return the published pilot catalog after validating all claim approvals."""
    from .reviewed import load_reviewed_catalog

    return load_reviewed_catalog()


def get_reviewed_progression(prog_id: str) -> ReviewedProgression:
    """Resolve a published pilot example by ID."""
    for example in list_reviewed_progressions():
        if example.progression.prog_id == prog_id.upper():
            return example
    raise ProgressionParsingError(f"No reviewed progression for {prog_id!r}.")


CANONICAL_PROGRESSION_DEFINITIONS = _HISTORICAL_PROGRESSION_DEFINITIONS


def _build_registry() -> Dict[str, CanonicalProgression]:
    reg = {}
    for d in _HISTORICAL_PROGRESSION_DEFINITIONS:
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
    return dict(sorted(reg.items()))


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


_MAJOR_DEGREES = (0, 2, 4, 5, 7, 9, 11)
_MINOR_DEGREES = (0, 2, 3, 5, 7, 8, 10)
_DEGREE_INDEX = {name: i for i, name in enumerate(("I", "II", "III", "IV", "V", "VI", "VII"))}
_FIGURES = {"53": (0, False), "6": (1, False), "63": (1, False), "64": (2, False),
            "65": (1, True), "43": (2, True), "42": (3, True), "2": (3, True)}
_EXPLICIT_QUALITIES = {
    "maj7", "maj9", "maj13", "m", "m6", "m7", "m7b5", "m9", "m11",
    "dim", "dim7", "aug", "add9", "sus2", "sus4", "7sus4", "7b9",
    "7#9", "7#11", "7b13", "7#5", "maj7#5", "13", "mmaj7",
}


def _degree_quality(suffix: str, minor_triad: bool, major_seventh: bool) -> str:
    if suffix == "maj7" and minor_triad:
        return "m(maj7)"
    if suffix == "7b5" and not minor_triad:
        return "7b5"
    if suffix in {"dom7", "dom9"}:
        return suffix.removeprefix("dom")
    if suffix in _EXPLICIT_QUALITIES:
        return "m(maj7)" if suffix == "mmaj7" else suffix
    diminished = {"o": "dim", "ob5": "dim", "b5": "dim", "o7": "dim7",
                  "ø": "m7b5", "ø7": "m7b5", "7b5": "m7b5"}
    if suffix in diminished:
        return diminished[suffix]
    if suffix == "":
        return "m" if minor_triad else ""
    if suffix == "7":
        return "m7" if minor_triad else "maj7" if major_seventh else "7"
    if suffix == "9":
        return "m9" if minor_triad else "maj9" if major_seventh else "9"
    if suffix == "11" and minor_triad:
        return "m11"
    raise ProgressionParsingError(f"Unsupported Roman numeral quality: {suffix!r}.")


def resolve_roman_degree(
    degree_str: str,
    key_root: str | NoteSpelling = 'C',
    is_minor_key: bool = False,
    *,
    convention: Literal['INT', 'DE', 'AUTO'] = 'AUTO',
) -> ChordDefinition:
    """Resolve a degree in major or minor, with optional applied function and figures.

    A bare V is a triad. V7 and ii7 use the numeral's case and function.
    Figures 6, 6/4, 6/5, 4/3 and 4/2 select the bass. Use m6 for an
    added-sixth minor chord. Explicit accidentals are relative to major.
    """
    key = parse_spelling(key_root.strip() + '4', convention=convention) if isinstance(key_root, str) else key_root
    cleaned = degree_str.strip().translate(str.maketrans({"♭": "b", "♯": "#", "°": "o", "º": "o"}))
    # Parentheses keep figured-bass slashes separate from applied functions.
    cleaned = re.sub(r'(?<=[IViv7^])([654])/([5432])(?=$|/)', r'(\1/\2)', cleaned)
    match = re.fullmatch(r'(bb|##|b|#)?([ivIV]+)((?:[^/()\s]|\([^()\s]+\))*)(?:/(.+))?', cleaned)
    if not match:
        raise ProgressionParsingError(f"Cannot parse Roman numeral: {degree_str!r}.")

    accidental, numeral, suffix, applied = match.groups()
    index = _DEGREE_INDEX.get(numeral.upper())
    if index is None or not (numeral.isupper() or numeral.islower()):
        raise ProgressionParsingError(f"Unknown Roman numeral: {numeral!r}.")
    # Also accept the catalog's V7/V(6/5) spelling for V7(6/5)/V.
    if applied:
        suffix_figure = re.fullmatch(r'([^()]+)(\((?:6/?5|4/?3|4/?2|2)\))', applied)
        if suffix_figure and not re.search(r'\d\)$', suffix):
            applied, figure_text = suffix_figure.groups()
            suffix += figure_text
        if accidental or numeral not in {"V", "vii"}:
            raise ProgressionParsingError(f"Unsupported applied function: {degree_str!r}.")
        key = resolve_roman_degree(applied, key, is_minor_key).root

    suffix = suffix.removeprefix("^")
    figure_match = re.search(r'\((5/?3|6(?:/?[345])?|4/?[23]|2)\)$', suffix)
    if not figure_match:
        figure_match = re.fullmatch(r'(?:o|ø|dim)(65|43|42|64|63|6|2)', suffix)
    figure = figure_match[1].replace("/", "") if figure_match else suffix
    inversion = 0
    if figure in _FIGURES:
        inversion, seventh = _FIGURES[figure]
        suffix = suffix[:figure_match.start(1)].removesuffix("(") if figure_match else ""
        if seventh and suffix in {"", "o", "ø"}:
            suffix += "7"
        elif seventh and suffix == "dim":
            suffix = "dim7"
    if not re.fullmatch(r'[^()]*?(?:\([^()]+\))?', suffix):
        raise ProgressionParsingError(f"Invalid Roman numeral quality: {suffix!r}.")
    suffix = suffix.replace("(", "").replace(")", "")
    if applied and numeral == "vii" and suffix not in {"o", "o7", "dim", "dim7", "ø", "ø7", "m7b5", "b5", "7b5"}:
        raise ProgressionParsingError("Applied leading-tone chords require a diminished quality.")

    minor_scale = is_minor_key and not applied
    leading_tone = numeral == "vii" and suffix in {"o", "o7", "dim", "dim7", "ø", "ø7", "m7b5", "b5", "7b5"}
    if accidental:
        semitones = _MAJOR_DEGREES[index] + (len(accidental) if accidental[0] == "#" else -len(accidental))
    else:
        semitones = (_MINOR_DEGREES if minor_scale and not leading_tone else _MAJOR_DEGREES)[index]
    root = key.transpose_diatonic(index, semitones)
    major_seventh = not accidental and not applied and (
        (minor_scale and numeral in {"III", "VI"}) or (not minor_scale and numeral in {"I", "IV"})
    )
    quality = _degree_quality(suffix, numeral.islower(), major_seventh)
    chord = ChordDefinition(root, quality)
    if not inversion:
        return chord
    if inversion >= len(chord.theoretical_intervals):
        raise ProgressionParsingError(f"Inversion exceeds chord size: {degree_str!r}.")
    bass = root.transpose_diatonic(2 * inversion, chord.theoretical_intervals[inversion])
    return ChordDefinition(root, quality, bass)


def generate_progression_voicings(
    chords: list[ChordDefinition] | CanonicalProgression,
    style: VoiceLeadingStyle = VoiceLeadingStyle.JAZZ_POP,
    initial_voicing_type: Literal['CLOSE', 'DROP2', 'SHELL', 'ROOTLESS'] = 'CLOSE',
    bass_octave: int = 3
) -> list[Voicing]:
    """Voice all chords with a consistent number of voices and explicit basses.

    The first chord uses the requested layout. Transitions optimize movement
    over each chord's selected pitch classes and may change the layout.
    """
    chord_list = chords.chord_definitions if isinstance(chords, CanonicalProgression) else chords
    if not chord_list:
        return []

    layouts = [chord.to_voicing(bass_octave, initial_voicing_type) for chord in chord_list]
    voice_count = max(len(layout.notes) for layout in layouts)
    initial_notes = layouts[0].midi_notes
    for _ in range(voice_count - len(initial_notes)):
        # Double a pitch already present while keeping the bass and ascending order.
        doubled = min(note + 12 * ((initial_notes[-1] - note) // 12 + 1) for note in initial_notes)
        if doubled > 127:
            raise VoiceLeadingError("Cannot complete the initial voicing in MIDI range.")
        initial_notes.append(doubled)

    initial_type = layouts[0].voicing_type if len(initial_notes) == len(layouts[0].notes) else 'CUSTOM'
    voicings = [Voicing(tuple(initial_notes), initial_type)]
    for chord, layout in zip(chord_list[1:], layouts[1:]):
        bass = chord.bass
        if bass is None and initial_voicing_type in {'CLOSE', 'SHELL'}:
            bass = chord.root
        next_notes = optimize_smooth_voice_leading(
            source_voicing=voicings[-1].midi_notes,
            target_pcs={note % 12 for note in layout.notes},
            bass_pc=int(bass.pitch_class) if bass is not None else None,
            style=style,
        )
        voicings.append(Voicing(tuple(next_notes), 'CUSTOM'))
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
