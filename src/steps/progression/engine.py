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

from ..theory.exceptions import MusicTheoryError, ProgressionParsingError, VoiceLeadingError
from ..theory.pitch import DIATONIC_STEPS, NoteSpelling, parse_spelling
from ..theory.chord import CHORD_TEMPLATES, ChordDefinition, Voicing, parse_chord
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


ARCHETYPE_THEORY_METADATA: dict[str, dict[str, Any]] = {
    'PROG-001': {
        'family': 'AXIS_FOUR_CHORD',
        'functional_syntax': 'I - V - vi - IV (T - D - Tp - S)',
        'harmonic_drive': 'Cyclic pop schema / singer-songwriter loop',
        'tonal_ambiguity': {
            'dual_center': True,
            'primary_center': 'C',
            'relative_center': 'Am',
            'major_reading': 'I - V - vi - IV',
            'minor_reading': 'III - VII - i - VI',
            'citations': ['Open Music Theory', 'Richards (2017)'],
        },
        'voice_leading_features': [
            'Common-tone C retained between C, Am and F',
            'Stepwise motion between IV and V',
        ],
    },
    'PROG-002': {
        'family': 'AXIS_PROGRESSION_MINOR_ROTATION',
        'functional_syntax': 'vi - IV - I - V (Tp - S - T - D) / i - VI - III - VII (t - sP - tP - dP)',
        'harmonic_drive': 'Emotional minor loop initiating on relative minor tonic',
        'tonal_ambiguity': {
            'dual_center': True,
            'primary_center': 'Am',
            'relative_center': 'C',
            'major_reading': 'vi - IV - I - V',
            'minor_reading': 'i - bVI - bIII - bVII (natural minor) or i - VI - III - VII',
            'citations': ['Tagg (2014)', 'Richards (2017)'],
            'ambiguity_notes': 'Beginning on Am creates strong minor gravitational pull; absence of leading tone G# leaves tonal center open to melodic resolution.',
        },
        'voice_leading_features': [
            'Descending bass line A -> F -> C -> G',
            'Common-tone C anchors the first three chords (Am, F, C)',
            'Smooth voice-leading step G -> A on loop turnaround',
        ],
    },
    'PROG-003': {
        'family': 'JAZZ_CADENCE',
        'functional_syntax': 'ii7 - V7 - Imaj7 (Sp7 - D7 - Tmaj7)',
        'harmonic_drive': 'Circle-of-fifths authentic full cadence in major',
        'tonal_ambiguity': {
            'dual_center': False,
            'primary_center': 'C',
            'cadence_type': 'Authentic Cadence',
            'citations': ['Levine (1995)', 'Open Music Theory'],
        },
        'voice_leading_features': [
            '7th of ii7 (C) resolves downward by half step to 3rd of V7 (B)',
            '7th of V7 (F) resolves downward by half step to 3rd of Imaj7 (E)',
            'Guide-tone counterpoint (3rd & 7th exchange)',
        ],
    },
    'PROG-004': {
        'family': 'DOO_WOP_AUTHENTIC_LOOP',
        'functional_syntax': 'I - vi - IV - V (T - Tp - S - D)',
        'harmonic_drive': 'Classic 50s Doo-Wop harmonic loop with submediant tonic prolongation and authentic turnaround',
        'tonal_ambiguity': {
            'dual_center': False,
            'primary_center': 'C',
            'cadence_type': 'Turnaround loop ending on dominant V',
            'citations': ['Aldwell/Schachter (1989)', 'Kostka/Payne (2013)'],
        },
        'voice_leading_features': [
            'Tonic prolongation via descending third C -> A',
            'Predominant preparation via F (IV) moving to dominant G (V)',
            'Stepwise bass motion F -> G -> C on cadence resolution',
        ],
    },
    'PROG-005': {
        'family': 'ANDALUSIAN_CADENCE_PHRYGIAN',
        'functional_syntax': 'i - bVII - bVI - V (t - dP - sP - D[dur])',
        'harmonic_drive': 'Descending minor tetrachord (lamento bass) terminating in Phrygian half-cadence',
        'tonal_ambiguity': {
            'modal_context': 'A Minor / A Phrygian Dominant',
            'primary_center': 'Am',
            'tetrachord_motion': 'A -> G -> F -> E (descending natural scale degrees 1 - b7 - b6 - 5)',
            'harmonic_tension': 'Dominant E major introduces chromatic leading-tone G# against modal subtonic G in bVII',
            'citations': ['Gauldin (2004)'],
        },
        'voice_leading_features': [
            'Lamento bass descent: stepwise down 2 - 2 - 1 semitones (A -> G -> F -> E)',
            'Characteristic Phrygian half-step resolution from F (bVI) to E (V)',
            'Chromatic inflection from G natural (in G) to G# leading tone (in E)',
        ],
    },
    'PROG-006': {
        'family': 'PACHELBEL_ROMANESCA_SEQUENCE',
        'functional_syntax': 'I - V - vi - iii - IV - I - IV - V (T - D - Tp - Dp - S - T - S - D)',
        'harmonic_drive': 'Diatonic descending sequence with alternating falling fourths and rising steps',
        'tonal_ambiguity': {
            'tonic': 'D',
            'sequence_type': 'Descending 4th / Romanesca variant',
            'citations': ['Fux (1725)', 'Rameau (1722)'],
        },
        'voice_leading_features': [
            'Stepwise descending soprano line over alternating root movements',
            'Authentic cadential turnaround IV - V - I on return',
        ],
    },
    'PROG-007': {
        'family': 'MODAL_DORIAN_VAMP',
        'functional_syntax': 'i7 - IV7 (t7 - S7[dur])',
        'harmonic_drive': 'Modal vamp highlighting characteristic Dorian major 6th',
        'tonal_ambiguity': {
            'modal_center': 'Dm',
            'characteristic_pitch': 'B (major 6th in D)',
            'citations': ['Pease (2003)'],
        },
        'voice_leading_features': [
            'Root oscillation D -> G',
            'Common tone D preserved between Dm7 and G7',
            'Guide-tone counterpoint: F (minor 3rd of Dm7) serves as 7th of G7, while B (major 3rd of G7) represents Dorian 6th',
        ],
    },
    'PROG-008': {
        'family': 'BLUES_12_BAR',
        'functional_syntax': 'Idom7 - IVdom7 - Idom7 - V7 - IVdom7 - Idom7',
        'harmonic_drive': 'Blues-functional dominant 7th chords on tonic, subdominant, and dominant with plagal/blues turnaround',
        'tonal_ambiguity': {
            'tonic': 'C',
            'blues_scale_coloring': 'b7 (Bb) over major tonic triad',
            'citations': ['Rawlins/Bahha (2005)', 'Open Music Theory (Blues Harmony)'],
        },
        'voice_leading_features': [
            'Dominant seventh chords functioning non-dominantly (blues tonic C7, subdominant F7)',
            'Guide tone shifts between 3rd and b7 (E/Bb in C7 -> Eb/A in F7)',
            'Plagal return V7 -> IV7 -> I7 characteristic of classic 12-bar blues',
        ],
    },
    'PROG-010': {
        'family': 'SECONDARY_DOMINANT_PROLONGATION',
        'functional_syntax': 'I - V7/vi - vi - IV (T - (D7)->Tp - Tp - S)',
        'harmonic_drive': 'Chromatic lift via secondary dominant E7 targeting relative minor Am',
        'tonal_ambiguity': {
            'tonic': 'C',
            'applied_target': 'Am (vi)',
            'citations': ['Kostka/Payne (2013)'],
        },
        'voice_leading_features': [
            'Chromatic voice step G -> G# in E7 resolving to A in Am',
            'Subdominant continuation to F (IV) via smooth step motion',
        ],
    },
    'PROG-011': {
        'family': 'MODAL_INTERCHANGE_AEOLIAN',
        'functional_syntax': 'I - bVI - bVII - I (T - sP - dP - T)',
        'harmonic_drive': 'Epic rock and film cadence borrowing bVI and bVII from parallel minor (Mario Cadence)',
        'tonal_ambiguity': {
            'tonic': 'C',
            'borrowed_mode': 'C Minor / C Aeolian',
            'citations': ['Mulholland (2013)'],
        },
        'voice_leading_features': [
            'Stepwise rising bass Ab -> Bb -> C',
            'Chromatic third-relation root movement C -> Ab',
        ],
    },
    'PROG-012': {
        'family': 'FALLING_FIFTHS_SEQUENCE',
        'functional_syntax': 'vi - ii - V - I (Tp - Sp - D - T)',
        'harmonic_drive': 'Complete diatonic circle-of-fifths sequence (basse fondamentale)',
        'tonal_ambiguity': {
            'dual_center': False,
            'primary_center': 'C',
            'cycle_type': 'Descending Fifths / Quintfall',
            'citations': ['Rameau (1722)', 'Salzer (1952)'],
        },
        'voice_leading_features': [
            'Consistent diatonic fifth-motion: root intervals of -5 semitones (or +7)',
            'Stepwise descending voice lines in alternating 3rds and 7ths',
            'Submediant vi prepares ii - V - I turnaround through uninterrupted quintal chain',
        ],
    },
    'PROG-013': {
        'family': 'TRITONE_SUBSTITUTION_CADENCE',
        'functional_syntax': 'ii7 - bII7 - Imaj7 (Sp7 - SubD7 - Tmaj7)',
        'harmonic_drive': 'Tritone substitution replacing dominant V7 (G7) with bII7 (Db7)',
        'tonal_ambiguity': {
            'tonic': 'C',
            'substitute_for': 'G7 (V7)',
            'common_tritone': ['F', 'B/Cb'],
            'citations': ['Levine (1995)'],
        },
        'voice_leading_features': [
            'Chromatic descending bass D -> Db -> C',
            'Tritone retention: F and B/Cb active in both G7 and Db7',
            'Half-step inward resolutions: Db -> C, F -> E, Ab -> G, Cb -> B',
        ],
    },
    'PROG-014': {
        'family': 'BACKDOOR_RESOLUTION',
        'functional_syntax': 'IV - bVII7 - I (S - Subtonik7 - T)',
        'harmonic_drive': 'Backdoor progression resolving subdominant minor/subtonic into major tonic',
        'tonal_ambiguity': {
            'tonic': 'C',
            'backdoor_dominant': 'Bb7',
            'citations': ['Terefenko (2014)'],
        },
        'voice_leading_features': [
            'Whole-step bass rise Bb -> C',
            'Inner voice chromatic descent: Ab (in Bb7) resolves down to G (in C)',
        ],
    },
    'PROG-015': {
        'family': 'ROYAL_ROAD_ODO_SHINKO',
        'functional_syntax': 'IVmaj7 - V7 - iii7 - vi (Smaj7 - D7 - Dp7 - Tp)',
        'harmonic_drive': 'Subdominant onset with deceptive-mediant falling-fifth resolution (J-Pop / Anime / Fusion)',
        'tonal_ambiguity': {
            'tonic': 'C',
            'cadence_type': 'Deceptive resolution to iii7 continuing as falling fifth to vi',
            'citations': ['Jaffe (1996)'],
        },
        'voice_leading_features': [
            'Parallel seventh voicings in smooth step motion',
            'Stepwise guide-tone descent F -> E -> D -> C across the loop',
            'Falling fifth motion iii7 -> vi (Em7 -> Am)',
        ],
    },
    'PROG-016': {
        'family': 'COLTRANE_CHANGES_THREE_TONIC',
        'functional_syntax': 'Imaj7 - V7/bVI - bVImaj7 - V7/bIV - bIVmaj7',
        'harmonic_drive': 'Symmetrical division of the octave into 3 equal major thirds in Z12 (Giant Steps Matrix)',
        'tonal_ambiguity': {
            'primary_key': 'B',
            'tonic_centers': ['B', 'G', 'Eb'],
            'symmetry_interval': 4,
            'citations': ['Cohn (2012)', 'Tymoczko (2011)', 'McClimon (2016)'],
        },
        'voice_leading_features': [
            'Hexatonic / Augmented triad symmetry {B, G, Eb}',
            'Interspersed secondary dominants (D7 -> Gmaj7, Bb7 -> Ebmaj7)',
            'Chromatic voice leading between major seventh and dominant seventh qualities',
        ],
    },
    'PROG-017': {
        'family': 'CLASSICAL_JAZZ_BACKDOOR_II_V',
        'functional_syntax': 'iv7 - bVII7 - Imaj7 (s7 - Subtonik7 - Tmaj7)',
        'harmonic_drive': 'Minor subdominant two-five cadence resolving from whole step below tonic (Lady Bird turnaround)',
        'tonal_ambiguity': {
            'tonic': 'C',
            'backdoor_cadence': 'Fm7 - Bb7 -> Cmaj7',
            'citations': ['Levine (1995)', 'Terefenko (2014)'],
        },
        'voice_leading_features': [
            'Minor subdominant iv7 (Fm7) preserves Aeolian modal interchange coloring (Ab)',
            'Smooth chromatic voice descent: Ab (in Fm7/Bb7) resolves down a half-step to G (in Cmaj7)',
            'Backdoor whole-step bass approach Bb -> C avoids dominant tritone tension',
        ],
    },
    'PROG-018': {
        'family': 'SUBSTITUTE_BACKDOOR_II_V',
        'functional_syntax': 'ii7 - bVII7 - Imaj7 (Sp7 - Subtonik7 - Tmaj7)',
        'harmonic_drive': 'Diatonic supertonic minor 7th paired with backdoor dominant bVII7 substituting for V7',
        'tonal_ambiguity': {
            'tonic': 'C',
            'hybrid_substitute': 'Dm7 (diatonic ii) combined with Bb7 (modal bVII7)',
            'citations': ['Rawlins/Bahha (2005)'],
        },
        'voice_leading_features': [
            'Common-tone retention: D and F shared between Dm7 and Bb7',
            'Chromatic inner-voice motion: A (in Dm7) moves to Ab (in Bb7) before resolving to G (in Cmaj7)',
            'Upward whole-step bass resolution Bb -> C into tonic major',
        ],
    },
    'PROG-019': {
        'family': 'MINOR_LINE_CLICHE',
        'functional_syntax': 'i - i(maj7) - i7 - im6 (t - t[maj7] - t7 - t6)',
        'harmonic_drive': 'Chromatic inner-voice descent 8 -> 7 -> b7 -> 6 over static tonic pedal',
        'tonal_ambiguity': {
            'tonic': 'Am',
            'cliche_voice': 'A -> G# -> G -> F# (semitone descent)',
            'citations': ['Levine (1995)'],
        },
        'voice_leading_features': [
            'Static root anchor A',
            'Single chromatic voice line descending 1 semitone per step',
            'Outer voices remain stable while inner chromatic motion generates harmonic tension',
        ],
    },
    'PROG-020': {
        'family': 'EXTENDED_TRITONE_SUB_ALTERED',
        'functional_syntax': 'ii9 - bII7(#11) - Imaj9 (Sp9 - SubD7[#11] - Tmaj9)',
        'harmonic_drive': 'Altered tritone substitution utilizing Lydian Dominant bII7(#11) with common-tone tonic anticipation',
        'tonal_ambiguity': {
            'tonic': 'C',
            'scale_degree_enharmonic': '#11 of Db7 is G natural, matching the fifth of C tonic',
            'citations': ['Levine (1995)', 'Pease (2003)'],
        },
        'voice_leading_features': [
            'Stepwise extended upper-structure voice leading: 9th to #11 to 9th (E -> G -> D)',
            'Common-tone tonic anticipation: G natural (#11 of Db7) held into Cmaj9 (5th)',
            'Half-step chromatic bass descent D -> Db -> C',
        ],
    },
    'PROG-027': {
        'family': 'MINOR_JAZZ_BLUES_SUBMEDIANT_TURNAROUND',
        'functional_syntax': 'i7 - iv7 - i7 - bVImaj7 - V7(#11) - i7',
        'harmonic_drive': 'Minor jazz blues turnaround incorporating bVImaj7 submediant and altered dominant V7(#11)',
        'tonal_ambiguity': {
            'tonic': 'Cm',
            'standards': ["Birk's Works", "Footprints"],
            'citations': ['Levine (1995)', 'Terefenko (2014)'],
        },
        'voice_leading_features': [
            'Submediant bVImaj7 (Abmaj7) prepares dominant V7(#11) (G7(#11)) by downward half-step bass motion',
            'Sharp eleven (#11 = C#/Db) in dominant resolves into root/third of tonic minor',
            'Minor blues scale flexibility over minor seventh and altered dominant qualities',
        ],
    },
}


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
        chord_symbols = re.split(r"\s+-\s+", self.chords_str.strip())
        return [parse_chord(symbol, "INT") for symbol in chord_symbols if symbol]

    @property
    def theory_profile(self) -> dict[str, Any]:
        """Deep musicological and structural profile of the archetype."""
        return ARCHETYPE_THEORY_METADATA.get(self.prog_id, {
            'family': 'CANONICAL_ARCHETYPE',
            'functional_syntax': self.roman_numerals,
            'harmonic_drive': self.context,
            'citations': [self.sources],
        })

    @property
    def archetype_family(self) -> str:
        """Categorical harmonic family identifier."""
        return self.theory_profile.get('family', 'CANONICAL_ARCHETYPE')

    def transpose(self, semitones: int) -> list[ChordDefinition]:
        """Transpose the entire progression using a single diatonic interval."""
        if isinstance(semitones, bool) or not isinstance(semitones, int):
            raise ProgressionParsingError("Transposition requires an integer number of semitones.")
        chords = self.chord_definitions
        if not chords or semitones == 0:
            return chords

        # Treat the key as a spelling anchor. The common diatonic shift
        # preserves relative letter distances, including slash basses.
        key_name = self.default_key.removesuffix("m")
        key = parse_spelling(key_name, "INT")
        preferred = key.transpose_chromatic(semitones)
        raw_shift = (
            7 * (preferred.octave - key.octave)
            + DIATONIC_STEPS.index(preferred.step) - DIATONIC_STEPS.index(key.step)
        )
        last_error = None
        for delta in (0, -1, 1, -2, 2, -3, 3):
            shift = raw_shift + delta
            try:
                key.transpose_diatonic(shift, semitones)
                return [
                    ChordDefinition(
                        chord.root.transpose_diatonic(shift, semitones), chord.quality,
                        chord.bass.transpose_diatonic(shift, semitones) if chord.bass else None,
                    )
                    for chord in chords
                ]
            except MusicTheoryError as exc:
                last_error = exc
        raise ProgressionParsingError(
            f"{self.prog_id}: no consistent spelling for transposition by {semitones} semitones."
        ) from last_error


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
    "dim", "dim7", "aug", "add9", "madd9", "sus2", "sus4", "7sus4", "7b9",
    "7#9", "7#11", "7b13", "7#5", "maj7#5", "13", "mmaj7",
}


def _degree_quality(suffix: str, minor_triad: bool, major_seventh: bool) -> str:
    if suffix == "add9" and minor_triad:
        return "madd9"
    if suffix == "maj7" and minor_triad:
        return "m(maj7)"
    if suffix == "7b5" and not minor_triad:
        return "7b5"
    if suffix == "+":
        return "aug"
    if suffix == "b5" and not minor_triad:
        raise ProgressionParsingError("A major numeral with b5 requires a supported major-third template.")
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
    minor_accidentals: Literal['major_reference', 'natural_minor'] = 'major_reference',
) -> ChordDefinition:
    """Resolve a degree in major or minor, with optional applied function and figures.

    A bare V is a triad. V7 and ii7 use the numeral's case and function.
    A bare vii denotes a minor chord. Write vii° to request a diminished triad.
    Figures 6, 6/4, 6/5, 4/3 and 4/2 select the bass. Figures 6/5,
    4/3 and 4/2 require a seventh. Use m6 for an added-sixth minor chord. Explicit minor-key accidentals use major_reference
    for legacy inputs or natural_minor when selected explicitly.
    """
    if minor_accidentals not in ("major_reference", "natural_minor"):
        raise ProgressionParsingError(f"Unknown minor accidental convention: {minor_accidentals!r}.")
    if not isinstance(degree_str, str):
        raise ProgressionParsingError("Roman numeral must be text.")
    if convention not in ("INT", "DE", "AUTO"):
        raise ProgressionParsingError(f"Unknown notation convention: {convention!r}.")
    if isinstance(key_root, str):
        try:
            key = parse_spelling(key_root, convention=convention)
        except MusicTheoryError as exc:
            raise ProgressionParsingError(str(exc)) from exc
    elif isinstance(key_root, NoteSpelling):
        key = key_root
    else:
        raise ProgressionParsingError("Key root must be a note name or NoteSpelling.")
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
        key = resolve_roman_degree(
            applied, key, is_minor_key, minor_accidentals=minor_accidentals,
        ).root

    suffix = suffix.removeprefix("^")
    figure_match = re.search(r'\((5/?3|6(?:/?[345])?|4/?[23]|2)\)$', suffix)
    if not figure_match:
        figure_match = re.fullmatch(r'(?:o|ø|dim)(65|43|42|64|63|6|2)', suffix)
    figure = figure_match[1].replace("/", "") if figure_match else suffix
    inversion = 0
    seventh = False
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
        scale = _MINOR_DEGREES if minor_scale and minor_accidentals == "natural_minor" else _MAJOR_DEGREES
        semitones = scale[index] + (len(accidental) if accidental[0] == "#" else -len(accidental))
    else:
        semitones = (_MINOR_DEGREES if minor_scale and not leading_tone else _MAJOR_DEGREES)[index]
    major_seventh = not accidental and not applied and (
        (minor_scale and numeral in {"III", "VI"}) or (not minor_scale and numeral in {"I", "IV"})
    )
    quality = _degree_quality(suffix, numeral.islower(), major_seventh)
    try:
        root = key.transpose_diatonic(index, semitones)
        chord = ChordDefinition(root, quality)
        intervals = chord.theoretical_intervals
        required_third = 3 if numeral.islower() else 4
        # An altered ninth does not determine the triad's quality.
        if CHORD_TEMPLATES[quality]["category"] != "SUSPENDED" and required_third not in intervals:
            raise ProgressionParsingError(f"Roman numeral case conflicts with chord quality: {degree_str!r}.")
        if not inversion:
            return chord
        seventh_intervals = (9,) if quality == "dim7" else (10, 11)
        if seventh and not any(tone in intervals for tone in seventh_intervals):
            raise ProgressionParsingError(f"Figure requires a seventh: {degree_str!r}.")
        tones = {1: (3, 4), 2: (6, 7, 8), 3: (9, 10, 11)}[inversion]
        if inversion == 3:
            tones = seventh_intervals
        pitch = next((tone for tone in tones if tone in intervals), None)
        if pitch is None:
            raise ProgressionParsingError(f"Figure refers to a missing chord tone: {degree_str!r}.")
        bass = root.transpose_diatonic(2 * inversion, pitch)
        return ChordDefinition(root, quality, bass)
    except ProgressionParsingError:
        raise
    except MusicTheoryError as exc:
        raise ProgressionParsingError(f"Cannot resolve {degree_str!r}: {exc}") from exc


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
    """Analyze transitions using the supplied voice order in each voicing."""
    transitions = max(0, len(voicings) - 1)
    total_l1 = 0
    total_circ = 0
    max_jump = 0
    violations = []
    for before, after in zip(voicings, voicings[1:]):
        left, right = list(before.notes), list(after.notes)
        total_l1 += absolute_semitone_distance(left, right)
        total_circ += circular_pc_distance(left, right)
        max_jump = max(max_jump, *(abs(b - a) for a, b in zip(left, right)))
        violations.extend(detect_parallel_fifths_octaves(left, right, style=style))
    comparisons = transitions * len(voicings[0].notes) if transitions else 0
    average = round(total_l1 / comparisons, 2) if comparisons else 0.0
    return {
        "total_l1_distance": total_l1,
        "total_circular_distance": total_circ,
        "transition_count": transitions,
        "average_l1_step_per_voice": average,
        "max_single_voice_jump": max_jump,
        "voice_crossings_count": sum(detect_voice_crossing(list(voicing.notes)) for voicing in voicings),
        "parallel_violations": violations,
        # Keep the historic short-input keys readable during migration.
        "circular_pc_distance": total_circ,
        "average_l1_step": average,
    }


def detect_progression_archetypes(
    chords: list[str] | list[ChordDefinition] | CanonicalProgression,
    key_root: str | NoteSpelling = "C",
    is_minor_key: bool = False,
    allow_rotations: bool = True,
    convention: Literal['INT', 'DE', 'AUTO'] = 'AUTO'
) -> list[dict[str, Any]]:
    """
    Intelligently identifies which canonical progression archetypes match a given chord sequence.
    Detects exact matches, cyclic rotations (e.g. Pop 4-Chord rotations), and transpositions.
    """
    if isinstance(chords, CanonicalProgression):
        chord_list = chords.chord_definitions
    elif isinstance(chords, list):
        if not chords:
            return []
        if isinstance(chords[0], str):
            conv = 'INT' if convention == 'AUTO' else convention
            chord_list = [parse_chord(s, convention=conv) for s in chords]  # type: ignore[arg-type]
        else:
            chord_list = chords  # type: ignore[assignment]
    else:
        raise ProgressionParsingError("Chords must be a list of chord strings or ChordDefinitions.")

    if not chord_list:
        return []

    input_roots = [int(c.root.pitch_class) for c in chord_list]
    input_qualities = [c.quality for c in chord_list]
    n = len(chord_list)

    input_rel_roots = [(r - input_roots[0]) % 12 for r in input_roots]

    matches: list[dict[str, Any]] = []

    for prog in CANONICAL_PROGRESSIONS.values():
        p_chords = prog.chord_definitions
        if len(p_chords) != n:
            continue

        p_roots = [int(c.root.pitch_class) for c in p_chords]
        p_qualities = [c.quality for c in p_chords]

        rotations_to_check = range(n) if allow_rotations else (0,)

        for rot in rotations_to_check:
            rot_roots = p_roots[rot:] + p_roots[:rot]
            rot_qualities = p_qualities[rot:] + p_qualities[:rot]

            # Quality check
            if input_qualities != rot_qualities:
                continue

            # Interval pattern check
            rot_rel_roots = [(r - rot_roots[0]) % 12 for r in rot_roots]
            if input_rel_roots != rot_rel_roots:
                continue

            # Check if in exact key or transposed
            is_exact_key = (input_roots == rot_roots)
            transposition_semitones = (input_roots[0] - rot_roots[0]) % 12

            # Scoring
            if rot == 0 and is_exact_key:
                score = 1.0
            elif rot == 0:
                score = 0.95
            elif is_exact_key:
                score = 0.90
            else:
                score = 0.85

            matches.append({
                'prog_id': prog.prog_id,
                'name': prog.name,
                'score': score,
                'rotation_offset': rot,
                'is_exact_match': (rot == 0 and is_exact_key),
                'is_exact_key': is_exact_key,
                'transposition_semitones': transposition_semitones,
                'roman_numerals': prog.roman_numerals,
                'default_key': prog.default_key,
                'context': prog.context,
                'family': prog.archetype_family,
                'theory_profile': prog.theory_profile,
            })

    # Sort matches by score descending, then by prog_id
    matches.sort(key=lambda m: (-m['score'], m['prog_id']))
    return matches
