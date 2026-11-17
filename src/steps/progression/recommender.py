"""
STEPS Cross-Domain Recommendation Engine (Harmonik <-> Drums <-> Piano <-> Bass).

Adheres to:
- OA-0032 (Cross-domain relation and recommendation module)
- M05 (Harmonielehre), M07 (Rhythmik), M08 (Drums), M09 (Genres), M10 (Klavierpraxis)
- ADR-005 (Notation conventions)
- Knowledge base: knowledge/relations/MUSIC_CONCEPT_RELATIONS.csv
- References: INTEGRATED_MUSICAL_CASE_STUDIES.md, DRUM_GROOVE_REFERENCE_LIBRARY.md,
  PIANO_PRACTICE_REFERENCE_LIBRARY.md, CHORD_PROGRESSION_REFERENCE_LIBRARY.md
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from .engine import CANONICAL_PROGRESSIONS, ARCHETYPE_THEORY_METADATA


@dataclass(frozen=True)
class CrossDomainRelation:
    """A cross-domain relationship between musical concepts from MUSIC_CONCEPT_RELATIONS.csv."""
    relation_id: str
    source_id: str
    target_id: str
    relation_type: str
    epistemic_classification: str
    domain_scope: str
    formal_rule_or_strength: str
    description: str
    validation_status: str


@dataclass(frozen=True)
class RecommendationItem:
    """A single recommended target item (drum pattern, piano module, progression, etc.)."""
    target_id: str
    target_name: str
    domain: str  # "DRUM", "PIANO", "PROGRESSION", "THEORY", "BASS"
    relation_type: str
    strength: str
    confidence: float
    description: str
    source_relation_id: Optional[str] = None


@dataclass(frozen=True)
class BasslineModel:
    """Genre-typical bassline model and performance practice for a chord progression."""
    name: str
    style_category: str
    description: str
    time_signature: Tuple[int, int]
    tempo_range: Tuple[int, int]
    pattern_description: str


@dataclass(frozen=True)
class CrossDomainRecommendation:
    """Validated cross-domain recommendation vector for a chord progression."""
    prog_id: str
    prog_name: str
    genre_scope: str
    drum_grooves: List[RecommendationItem]
    piano_voicings: List[RecommendationItem]
    bassline_model: BasslineModel
    explicit_relations: List[CrossDomainRelation]
    overall_compatibility: str = "HIGH"


# Canonical Drum Patterns catalogue (PAT-001 .. PAT-031) from DRUM_GROOVE_REFERENCE_LIBRARY.md
CANONICAL_DRUM_PATTERNS: Dict[str, Dict[str, Any]] = {
    "PAT-001": {"name": "Pop / Rock Straight", "tempo": 115, "feel": "4/4 Straight"},
    "PAT-002": {"name": "Classic House", "tempo": 124, "feel": "4/4 Straight Four-on-the-Floor"},
    "PAT-003": {"name": "Boom-Bap Hip-Hop", "tempo": 90, "feel": "4/4 Swung"},
    "PAT-004": {"name": "UK Garage 2-Step", "tempo": 134, "feel": "4/4 Swung"},
    "PAT-005": {"name": "Berlin Peak Techno", "tempo": 132, "feel": "4/4 Straight Four-on-the-Floor"},
    "PAT-006": {"name": "Trap Halftime", "tempo": 140, "feel": "4/4 Halftime"},
    "PAT-007": {"name": "Funk 'The One'", "tempo": 105, "feel": "4/4 16th Funk"},
    "PAT-008": {"name": "Drum & Bass (Amen)", "tempo": 174, "feel": "4/4 Fast Breakbeat"},
    "PAT-009": {"name": "Motown / Soul Stomp", "tempo": 120, "feel": "4/4 Straight Stomp"},
    "PAT-010": {"name": "Reggae One Drop", "tempo": 75, "feel": "4/4 Halftime Laid-back"},
    "PAT-011": {"name": "Afrobeat Sketch", "tempo": 118, "feel": "4/4 Polyrhythmic"},
    "PAT-012": {"name": "Jazz Traditional Ride", "tempo": 130, "feel": "4/4 Swung Spang-a-lang"},
    "PAT-013": {"name": "Funk 16th Linear Ghost", "tempo": 100, "feel": "4/4 16th Straight Ghost"},
    "PAT-014": {"name": "Soul Ballad 12/8", "tempo": 60, "feel": "12/8 Triplet Feel"},
    "PAT-015": {"name": "Reggae Steppers", "tempo": 78, "feel": "4/4 Four-on-the-Floor"},
    "PAT-016": {"name": "Reggae Rockers", "tempo": 82, "feel": "4/4 Syncopated Rockers"},
    "PAT-017": {"name": "Bebop Up-Tempo Comping", "tempo": 180, "feel": "4/4 Fast Swing"},
    "PAT-018": {"name": "Liquid D&B Rolling Break", "tempo": 174, "feel": "4/4 Fast Two-Step"},
    "PAT-019": {"name": "Neurofunk Two-Step", "tempo": 174, "feel": "4/4 Gated Electronic"},
    "PAT-020": {"name": "Authentic UKG 2-Step", "tempo": 134, "feel": "4/4 58% MPC-Swing"},
    "PAT-021": {"name": "Jungle Amen Chopped", "tempo": 168, "feel": "4/4 High-Syncopation Break"},
    "PAT-022": {"name": "Jump-Up Minimal Bouncer", "tempo": 175, "feel": "4/4 Stripped Minimal"},
    "PAT-023": {"name": "UK Garage 4-Bar Shuffle", "tempo": 134, "feel": "4/4 58% Swing"},
    "PAT-024": {"name": "Boom-Bap Golden Era", "tempo": 90, "feel": "4/4 61% MPC 3000 Swung"},
    "PAT-025": {"name": "Berlin 909 Peak Techno", "tempo": 130, "feel": "4/4 Straight Four-on-the-Floor"},
    "PAT-026": {"name": "UK Garage 2-Step Heavy", "tempo": 132, "feel": "4/4 64% Swing Heavy"},
    "PAT-027": {"name": "Bossa Nova Authentic Brush", "tempo": 128, "feel": "4/4 Two-Bar Cross-Stick"},
    "PAT-028": {"name": "Afro-Cuban Cha-Cha-Chá", "tempo": 116, "feel": "4/4 Campana & Conga"},
    "PAT-029": {"name": "Samba Batucada Sectional", "tempo": 105, "feel": "2/2 Alla Breve"},
    "PAT-030": {"name": "Phrygian Neo-Soul Halftime Shuffle", "tempo": 84, "feel": "4/4 57% Halftime Shuffle"},
    "PAT-031": {"name": "Afro-Cuban 6/8 Bembé Fusion", "tempo": 120, "feel": "6/8 Polyrhythm (3:2)"},
}

# Canonical Piano Modules catalogue (P01 .. P19) from PIANO_PRACTICE_REFERENCE_LIBRARY.md
CANONICAL_PIANO_MODULES: Dict[str, Dict[str, str]] = {
    "P01": {"title": "Stamm-Dreiklänge & Topografie", "competence": "Tastenfindung, Grundstellung, Terzschichtung", "core_principle": "Dreiklänge als Schneemänner (Weiß-Weiß-Weiß)"},
    "P02": {"title": "Akkordumkehrungen & Minimal Movement", "competence": "Geschmeidiges Verbinden ohne Hand-Sprünge", "core_principle": "L1-Distanzminimierung (1. & 2. Umkehrung)"},
    "P03": {"title": "Zweihändige Begleitmuster (Pop Groove)", "competence": "Rhythmisches Fundament der linken Hand", "core_principle": "Linke Hand Bass/Puls, rechte Hand Akkord-Offbeats"},
    "P04": {"title": "Vierklänge & Septakkorde", "competence": "Jazz- & Pop-Klangfarben verstehen", "core_principle": "Maj7, Dom7, m7 (Erweiterung um die Septime)"},
    "P05": {"title": "Zweihändige Shell-Voicings", "competence": "Klobige Griffe vermeiden; Jazz-Transparenz", "core_principle": "LH spielt Bass; RH spielt nur 3 & 7 (Guide Tones)"},
    "P06": {"title": "Sus- und Add-Akkorde", "competence": "Moderne Pop-Balladen-Sounds erzeugen", "core_principle": "Sus4 (Quarte ersetzt Terz) & Add9 (None hinzu)"},
    "P07": {"title": "Zweihändige rollende Arpeggien", "competence": "Fließende Balladenbegleitung (Coldplay-Style)", "core_principle": "LH Quint-Fundament; RH durchgehende 8tel-Welle"},
    "P08": {"title": "Drop-2 Voicings", "competence": "Raumfüllender, transparenter Profi-Klang", "core_principle": "Stimme 2 von oben fällt eine Oktave nach unten"},
    "P09": {"title": "Rhythmische Akkordbegleitung", "competence": "Vom steifen Akkord zum groovenden Begleiter", "core_principle": "Charleston-Rhythmus (1 & 2+) und Staccato-Offbeat-Stabs"},
    "P10": {"title": "Akkorde nach Gehör & Funktion verstehen", "competence": "Songs ohne Noten intuitiv am Gehör erfassen", "core_principle": "Heimat (I), Reise (IV/ii), Magnet (V); Bass-First Decoder"},
    "P11": {"title": "Akkordumkehrungen nach Gehör & Funktion", "competence": "Den Inversion Code knacken; Stufenbässe", "core_principle": "Grundstellung (5/3) vs. Sextakkord (6/3) vs. Quartsextakkord (6/4)"},
    "P12": {"title": "Zweihändige Rootless Voicings", "competence": "Den weichen Neo-Soul & Lo-Fi Sound spielen", "core_principle": "LH spielt Grundton; RH spielt grundtonlose 3-5-7-9 oder 7-9-3-5 Oberstruktur"},
    "P13": {"title": "Reharmonisation in der Praxis", "competence": "Monotone Melodien spannend umfärben", "core_principle": "Diatonische Substitution, Modal Interchange, Picardische Terz & Sus4"},
    "P14": {"title": "Bossa Nova & Latin Piano Begleitung", "competence": "Sanft wiegende Rhythmen spielen", "core_principle": "LH Surdo-Pendel (1 & 3 Grundton, 2 & 4 Quinte); RH Bossa Clave Comping"},
    "P15": {"title": "Stimmführung & Chromatische Medianten", "competence": "Geschmeidige Modulationen ohne Tonartbrüche", "core_principle": "Minimale L1-Distanzverschiebung bei Großterz-Modulationen"},
    "P16": {"title": "Upper Structure Triads über Dominanten", "competence": "Komplexe Jazz-Spannungen mühelos greifen", "core_principle": "RH Dur-Dreiklang über LH Shell-Gerüst (z. B. D über C7 für 9/#11/13)"},
    "P17": {"title": "Zeitgenössisches Syncopated Comping", "competence": "Moderne R&B- und Gospel-Pushes spielen", "core_principle": "16tel-Vorwegnahmen und synkopierte Push-Akkorde über 2- und 4-Bar-Loops"},
    "P18": {"title": "Backdoor Guide-Tone Voicings", "competence": "Reibungslose Auflösung über bVII7 zur Tonika", "core_principle": "Stimmführung iv7 -> bVII7 -> Imaj7; Septime Ab->G (Halbton), Terz D->E (Ganzton)"},
    "P19": {"title": "Chromatische Bassführung für Sekundärdominanten", "competence": "Fließende Basslinien in Kadenzen spielen", "core_principle": "I -> V7(6/5)/V -> ii6 -> I6 -> V7(4/3) -> I chromatisch-diatonischer Bassabstieg"},
}

# Canonical Genre Bassline Models
CANONICAL_BASSLINE_MODELS: Dict[str, BasslineModel] = {
    "PROG-001": BasslineModel(
        name="Root-Fifth Driving Pop Rock Bass",
        style_category="Pop / Rock / Singer-Songwriter",
        description="Driving 8th-note pulse anchored on chord roots on downbeats with rhythmic octave leaps.",
        time_signature=(4, 4),
        tempo_range=(100, 125),
        pattern_description="Root on beat 1 and 3; octave bounce on 2+ and 4; smooth scalar transition to next root."
    ),
    "PROG-002": BasslineModel(
        name="Halftime Reese Sub-Bass / 808 Foundation",
        style_category="Emotional Pop / Melodic EDM / Liquid D&B",
        description="Sustained sub-bass sine/saw foundation operating at halftime speed with smooth legato slides.",
        time_signature=(4, 4),
        tempo_range=(85, 174),
        pattern_description="Sustained roots on beat 1 lasting 2 to 4 beats; subtle filter modulation and glide between degrees."
    ),
    "PROG-003": BasslineModel(
        name="Acoustic Upright Walking Bass",
        style_category="Jazz / Bebop / Standards",
        description="Four-to-the-bar swinging quarter note line outlining chord arpeggios and chromatic lead-ins.",
        time_signature=(4, 4),
        tempo_range=(110, 160),
        pattern_description="Beat 1: Root; Beat 2: 3rd or 5th; Beat 3: Chord tone or diatonic passing note; Beat 4: Chromatic approach note."
    ),
    "PROG-004": BasslineModel(
        name="Doo-Wop Root-Fifth Bouncing Bass",
        style_category="50s Doo-Wop / Early Rock'n'Roll",
        description="Bouncing quarter or dotted-eighth bass alternating between root and lower/upper fifth.",
        time_signature=(4, 4),
        tempo_range=(95, 120),
        pattern_description="Beat 1: Root; Beat 2: 5th; Beat 3: Root; Beat 4: 5th or chromatic approach."
    ),
    "PROG-005": BasslineModel(
        name="Phrygian Ground Bass with Flamenco Syncopation",
        style_category="Flamenco / Latin Rock",
        description="Heavy downbeat root declaration descending stepwise through the Andalusian tetrachord.",
        time_signature=(4, 4),
        tempo_range=(85, 115),
        pattern_description="Strong accents on beat 1 and 3; descending roots Am -> G -> F -> E with 16th ornamental snaps."
    ),
    "PROG-006": BasslineModel(
        name="Basso Continuo Stepwise Cadential Bass",
        style_category="Baroque / Classical / Traditional Ballad",
        description="Classical figured bass line alternating descending fourth leaps with ascending stepwise voice-leading.",
        time_signature=(4, 4),
        tempo_range=(65, 85),
        pattern_description="Downbeat root declarations D -> A -> Bm -> F#m -> G -> D -> G -> A in continuous steady motion."
    ),
    "PROG-007": BasslineModel(
        name="Funk Thumb-Slap & Fingerstyle Vamp Bass",
        style_category="Funk / Soul / Acid Jazz",
        description="Dynamic slap/pop or fingerstyle groove locking tightly to the kick drum with ghost notes.",
        time_signature=(4, 4),
        tempo_range=(95, 115),
        pattern_description="Explosive root accent on 'The One'; syncopated 16th octave pops on 2e+ and 4; minor 7th slides."
    ),
    "PROG-008": BasslineModel(
        name="Boogie-Woogie / Blues Shuffle Walking Bass",
        style_category="Traditional Blues / Rock'n'Roll",
        description="Arpeggiated blues walking bass following the 1-3-5-6-b7 contour over swung eighth notes.",
        time_signature=(4, 4),
        tempo_range=(100, 140),
        pattern_description="Continuous swung 8ths: Root -> 3rd -> 5th -> 6th -> b7th -> 6th -> 5th -> 3rd for each bar."
    ),
    "PROG-009": BasslineModel(
        name="Lyrical Romantic Ballad Bass",
        style_category="Romantic / Film Score / Pop Ballad",
        description="Warm, melodic electric or orchestral bass supporting the major-to-minor plagal transformation.",
        time_signature=(4, 4),
        tempo_range=(60, 85),
        pattern_description="Root declaration on beat 1; upper scalar passing tone on beat 3; expressive chromatic descent into iv."
    ),
    "PROG-010": BasslineModel(
        name="Gospel / Soul Stepwise Secondary Dominant Bass",
        style_category="Gospel / Soul / Pop",
        description="Ascending and descending scalar bass leading purposefully into secondary dominant targets.",
        time_signature=(4, 4),
        tempo_range=(80, 115),
        pattern_description="Root on 1; chromatic leading tone G# leading into Am on beat 1 of measure 3."
    ),
    "PROG-011": BasslineModel(
        name="Cinematic Modal Rock Power Bass",
        style_category="Epic Pop / Rock / Film Music",
        description="Driving, powerful root-eighth lines accenting the borrowed bVI and bVII modal interchange degrees.",
        time_signature=(4, 4),
        tempo_range=(90, 130),
        pattern_description="Relentless 8th-note root drive emphasizing C -> Ab -> Bb -> C with heavy low-end compression."
    ),
    "PROG-012": BasslineModel(
        name="Descending Fifths Cycle Walking Bass",
        style_category="Baroque / Classic Jazz / Swing",
        description="Classic walking line executing circle of fifths root cycles with counter-directional voice leading.",
        time_signature=(4, 4),
        tempo_range=(115, 150),
        pattern_description="Four quarter notes per bar: Root -> 3rd -> 5th -> Chromatic approach to next fifth."
    ),
    "PROG-013": BasslineModel(
        name="Bebop Chromatic Tritone Slide Bass",
        style_category="Modern Jazz / Bebop",
        description="Acoustic walking bass emphasizing the half-step tritone substitution bass drop.",
        time_signature=(4, 4),
        tempo_range=(120, 170),
        pattern_description="Beat 1: D2 (ii); Beat 3: Db2 (bII tritone sub); Beat 1 (next bar): C2 (I) resolving smoothly."
    ),
    "PROG-014": BasslineModel(
        name="Soul / R&B Backdoor Syncopated Bass",
        style_category="R&B / Motown / Neo-Soul",
        description="Grooving electric bass line connecting the subdominant IV to the backdoor dominant bVII.",
        time_signature=(4, 4),
        tempo_range=(80, 105),
        pattern_description="Syncopated roots with 16th anticipations on beat 2+ and 4+; minor 3rd slides into bVII."
    ),
    "PROG-015": BasslineModel(
        name="J-Pop / Anime Melodic Driving Bass",
        style_category="J-Pop / Japanese Fusion / Anime",
        description="High-energy, melodic bassline featuring syncopated octave leaps and scalar connectives.",
        time_signature=(4, 4),
        tempo_range=(115, 140),
        pattern_description="Active 8th-note figures: F -> G -> Em -> Am with ornamental 16th scalar fills on beat 4."
    ),
    "PROG-016": BasslineModel(
        name="Coltrane Matrix High-Velocity Walking Bass",
        style_category="Modern Jazz Matrix / Three-Tonic Cycle",
        description="High-tempo acoustic walking bass navigating the major thirds tonal centres (B -> G -> Eb).",
        time_signature=(4, 4),
        tempo_range=(180, 240),
        pattern_description="Precise two-feel in exposition transitioning to rapid four-beat walk defining major-third shifts."
    ),
    "PROG-017": BasslineModel(
        name="Electric Fingerstyle Bass with Chromatic Passing Tones",
        style_category="Neo-Soul / Jazz-Hop / Standards",
        description="Warm electric fingerstyle bass with chromatic approaches, octave jumps, and laid-back timing.",
        time_signature=(4, 4),
        tempo_range=(75, 95),
        pattern_description="Bar 1 (Fm7): F1 (1), F2 (2+), Ab1 (3+), A1 (4+); Bar 2 (Bb7): Bb1 (1), F2 (2+), B1 chromatic slide into C2."
    ),
    "PROG-018": BasslineModel(
        name="Cool Jazz West Coast Walking Bass",
        style_category="Cool Jazz / West Coast Jazz",
        description="Spacious, understated acoustic bass line emphasizing open intervals and smooth voice leading.",
        time_signature=(4, 4),
        tempo_range=(100, 130),
        pattern_description="Gentle quarter-note pulse: D2 -> Bb1 -> C2 with melodic scalar bridge tones."
    ),
    "PROG-019": BasslineModel(
        name="Minor Line Cliché Stationary Pedal Bass",
        style_category="Bossa Nova / Ballade / Film Noir",
        description="Sustained tonic pedal bass grounding the harmony while inner voices descend chromatically.",
        time_signature=(4, 4),
        tempo_range=(70, 120),
        pattern_description="Tonic pedal A1 held firmly or pulsating in half notes while upper voices execute A -> G# -> G -> F#."
    ),
    "PROG-020": BasslineModel(
        name="Contemporary Jazz Altered Tritone Bass",
        style_category="Contemporary Jazz / Fusion",
        description="Modern acoustic or 5-string bass exploring low register alterations and chromatic approach gestures.",
        time_signature=(4, 4),
        tempo_range=(110, 150),
        pattern_description="Dm9 root -> Db7(#11) low chromatic slide -> Cmaj9 release with wide interval drops."
    ),
    "PROG-021": BasslineModel(
        name="Laid-Back Neo-Soul / Boom-Bap Sub-Bass",
        style_category="Neo-Soul / Boom-Bap / Lo-Fi",
        description="Heavy deep sub-bass or electric bass with delayed pocket feel and subtle pitch slides.",
        time_signature=(4, 4),
        tempo_range=(80, 95),
        pattern_description="Laid-back root hits on 1 and 2e+; silent downbeat variations; slide into bVImaj9."
    ),
    "PROG-022": BasslineModel(
        name="Modal-to-Picardy Cadential Ground Bass",
        style_category="Renaissance / Baroque / Folk",
        description="Stepwise descending minor bass resolving with strength and resonance on the major tonic root.",
        time_signature=(4, 4),
        tempo_range=(65, 90),
        pattern_description="D -> G -> C -> D with deep resonant decay on the final Picardy third resolution."
    ),
    "PROG-023": BasslineModel(
        name="Halftime Reese Sub-Bass LFO Sweep",
        style_category="Liquid Drum & Bass / UK Bass",
        description="Heavy 87 BPM halftime Reese saw/sub bass operating beneath 174 BPM breakbeats with LFO filtering.",
        time_signature=(4, 4),
        tempo_range=(85, 175),
        pattern_description="F1 Ganztaktnote -> Db0 deep rumble -> Eb1 -> F1 with subtle portamento glides."
    ),
    "PROG-024": BasslineModel(
        name="Bossa Nova Surdo-Pendel Acoustic Bass",
        style_category="Bossa Nova / Brazilian Jazz",
        description="Acoustic bass emulating the Brazilian Surdo drum with downbeat roots and syncopated fifths.",
        time_signature=(4, 4),
        tempo_range=(115, 135),
        pattern_description="Beat 1: Root (soft downbeat); Beat 2+: Fifth (syncopated pull); Beat 3: Root; Beat 4+: Passing tone."
    ),
    "PROG-025": BasslineModel(
        name="Afro-Cuban Anticipated Tumbao Bass",
        style_category="Afro-Cuban / Salsa / Mambo",
        description="Classic Latin bass playing syncopated anticipations on beat 2+ and beat 4, avoiding the downbeat.",
        time_signature=(4, 4),
        tempo_range=(105, 125),
        pattern_description="Downbeat on 1 is silent; bass triggers on beat 2+ and beat 4 (tied over the barline to beat 1)."
    ),
    "PROG-026": BasslineModel(
        name="Descending Chromatic Bass Walk for Secondary Dominants",
        style_category="Baroque / Classical / Latin Jazz",
        description="Continuous stepwise bass line descending from tonic through double dominant 1st inversion.",
        time_signature=(4, 4),
        tempo_range=(80, 110),
        pattern_description="G2 (I) -> C#3 (V7(6/5)/V) -> C3 (ii6) -> B2 (I6) -> A2 (V7(4/3)) -> G2 (I); C#-C-B-A-G step motion."
    ),
    "PROG-027": BasslineModel(
        name="Minor Blues Walking Bass with Submediant Turnaround",
        style_category="Minor Jazz Blues / Hard Bop",
        description="Steady walking bass line navigating the minor tonic, subdominant, and bVImaj7 to V7(#11) turnaround.",
        time_signature=(4, 4),
        tempo_range=(110, 150),
        pattern_description="Continuous quarter-note walk emphasizing the minor 3rd and outlining the Abmaj7 -> G7(#11) turnaround."
    ),
    "PROG-028": BasslineModel(
        name="Neo-Soul Halftime Shuffle Sub-Bass",
        style_category="Neo-Soul / Contemporary R&B / Jazz-Funk",
        description="Deep, pocket-oriented electric or synth bass with syncopated ghost notes and laid-back micro-timing.",
        time_signature=(4, 4),
        tempo_range=(75, 95),
        pattern_description="Hard downbeat root on 1; syncopated sub-kick push on 3+; chromatic slides connecting Em9 to Am9."
    ),
}


class CrossDomainRecommender:
    """
    Cross-domain recommendation and relationship engine connecting:
    - Chord Progressions (PROG-xxx)
    - Drum Patterns (PAT-xxx)
    - Piano Voicing Modules (Pxx)
    - Bassline Models & General Music Theory Domains (M01-M12)
    """

    def __init__(self, relations_path: Optional[str | Path] = None) -> None:
        self.relations_path = self._resolve_path(relations_path)
        self.relations: List[CrossDomainRelation] = []
        self._by_source: Dict[str, List[CrossDomainRelation]] = {}
        self._by_target: Dict[str, List[CrossDomainRelation]] = {}
        self._by_id: Dict[str, CrossDomainRelation] = {}
        self._load_relations()

    @staticmethod
    def _resolve_path(path: Optional[str | Path]) -> Path:
        if path is not None:
            return Path(path).resolve()
        # Look in repo hierarchy: knowledge/relations/MUSIC_CONCEPT_RELATIONS.csv
        current = Path(__file__).resolve()
        # Repo root is 3 levels up: progression -> steps -> src -> repo
        repo_root = current.parents[3]
        candidate = repo_root / "knowledge" / "relations" / "MUSIC_CONCEPT_RELATIONS.csv"
        if candidate.exists():
            return candidate
        # Fallback to local working directory
        cwd_candidate = Path("knowledge/relations/MUSIC_CONCEPT_RELATIONS.csv").resolve()
        return cwd_candidate

    def _load_relations(self) -> None:
        if not self.relations_path.exists():
            return
        with open(self.relations_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rel = CrossDomainRelation(
                    relation_id=row.get("relation_id", "").strip(),
                    source_id=row.get("source_id", "").strip(),
                    target_id=row.get("target_id", "").strip(),
                    relation_type=row.get("relation_type", "").strip(),
                    epistemic_classification=row.get("epistemic_classification", "").strip(),
                    domain_scope=row.get("domain_scope", "").strip(),
                    formal_rule_or_strength=row.get("formal_rule_or_strength", "").strip(),
                    description=row.get("description", "").strip(),
                    validation_status=row.get("validation_status", "").strip(),
                )
                self.relations.append(rel)
                self._by_id[rel.relation_id] = rel
                self._by_source.setdefault(rel.source_id, []).append(rel)
                self._by_target.setdefault(rel.target_id, []).append(rel)

    def get_relations_for_entity(self, entity_id: str) -> List[CrossDomainRelation]:
        """Return all explicit relations from MUSIC_CONCEPT_RELATIONS.csv involving entity_id."""
        results: List[CrossDomainRelation] = []
        seen = set()
        for rel in self._by_source.get(entity_id, []):
            if rel.relation_id not in seen:
                results.append(rel)
                seen.add(rel.relation_id)
        for rel in self._by_target.get(entity_id, []):
            if rel.relation_id not in seen:
                results.append(rel)
                seen.add(rel.relation_id)
        return results

    def recommend_for_progression(self, prog_id: str) -> CrossDomainRecommendation:
        """
        Produce a validated cross-domain recommendation vector for any canonical PROG ID.
        Combines explicit verified relations from CSV with genre-idiomatic pairings.
        """
        if prog_id not in CANONICAL_PROGRESSIONS:
            raise KeyError(f"Unknown canonical progression ID: '{prog_id}'. Expected PROG-001..PROG-028.")

        prog = CANONICAL_PROGRESSIONS[prog_id]
        meta = ARCHETYPE_THEORY_METADATA.get(prog_id, {})
        genre_scope = meta.get("harmonic_drive", prog.context)

        explicit_rels = self.get_relations_for_entity(prog_id)
        drum_items: List[RecommendationItem] = []
        piano_items: List[RecommendationItem] = []
        seen_targets: Set[str] = set()

        # 1. Harvest explicit relations from CSV (forward or reverse)
        for rel in explicit_rels:
            # Determine target counterpart
            other_id = rel.target_id if rel.source_id == prog_id else rel.source_id
            if other_id.startswith("PAT-") and other_id not in seen_targets:
                pat_info = CANONICAL_DRUM_PATTERNS.get(other_id, {"name": "Drum Pattern", "feel": ""})
                drum_items.append(
                    RecommendationItem(
                        target_id=other_id,
                        target_name=pat_info["name"],
                        domain="DRUM",
                        relation_type=rel.relation_type,
                        strength=rel.formal_rule_or_strength,
                        confidence=1.0,
                        description=rel.description,
                        source_relation_id=rel.relation_id,
                    )
                )
                seen_targets.add(other_id)
            elif other_id.startswith("P") and other_id not in seen_targets and not other_id.startswith("PROG"):
                piano_info = CANONICAL_PIANO_MODULES.get(other_id, {"title": "Piano Module", "competence": ""})
                piano_items.append(
                    RecommendationItem(
                        target_id=other_id,
                        target_name=piano_info["title"],
                        domain="PIANO",
                        relation_type=rel.relation_type,
                        strength=rel.formal_rule_or_strength,
                        confidence=1.0,
                        description=rel.description,
                        source_relation_id=rel.relation_id,
                    )
                )
                seen_targets.add(other_id)

        # 2. Add curated primary & secondary pairings for 100% coverage across all 28 archetypes
        self._supplement_progression_recommendations(prog_id, drum_items, piano_items, seen_targets)

        # 3. Retrieve genre-idiomatic bassline model
        bassline = CANONICAL_BASSLINE_MODELS.get(
            prog_id,
            BasslineModel(
                name="Tonal Root-Walking Bass",
                style_category="General Harmony",
                description="Standard diatonic bassline providing harmonic foundation and smooth transitions.",
                time_signature=(4, 4),
                tempo_range=(90, 120),
                pattern_description="Root notes on strong beats with scalar connectives.",
            )
        )

        return CrossDomainRecommendation(
            prog_id=prog_id,
            prog_name=prog.name,
            genre_scope=genre_scope,
            drum_grooves=drum_items,
            piano_voicings=piano_items,
            bassline_model=bassline,
            explicit_relations=explicit_rels,
            overall_compatibility="HIGH",
        )

    def recommend_for_drum_pattern(self, pat_id: str) -> List[RecommendationItem]:
        """Recommend matching chord progressions and piano modules for a given drum pattern."""
        if pat_id not in CANONICAL_DRUM_PATTERNS:
            raise KeyError(f"Unknown canonical drum pattern ID: '{pat_id}'. Expected PAT-001..PAT-031.")

        results: List[RecommendationItem] = []
        seen = set()

        # Check explicit relations from CSV
        for rel in self.get_relations_for_entity(pat_id):
            other_id = rel.target_id if rel.source_id == pat_id else rel.source_id
            if other_id.startswith("PROG-") and other_id not in seen:
                prog = CANONICAL_PROGRESSIONS.get(other_id)
                name = prog.name if prog else "Progression"
                results.append(
                    RecommendationItem(
                        target_id=other_id,
                        target_name=name,
                        domain="PROGRESSION",
                        relation_type=rel.relation_type,
                        strength=rel.formal_rule_or_strength,
                        confidence=1.0,
                        description=rel.description,
                        source_relation_id=rel.relation_id,
                    )
                )
                seen.add(other_id)
            elif other_id.startswith("P") and not other_id.startswith("PROG-") and other_id not in seen:
                p_info = CANONICAL_PIANO_MODULES.get(other_id, {"title": "Piano Module"})
                results.append(
                    RecommendationItem(
                        target_id=other_id,
                        target_name=p_info["title"],
                        domain="PIANO",
                        relation_type=rel.relation_type,
                        strength=rel.formal_rule_or_strength,
                        confidence=1.0,
                        description=rel.description,
                        source_relation_id=rel.relation_id,
                    )
                )
                seen.add(other_id)

        # Supplement with known stylistic pairings if not explicitly in CSV
        for prog_id in CANONICAL_PROGRESSIONS:
            if prog_id not in seen:
                rec = self.recommend_for_progression(prog_id)
                for d in rec.drum_grooves:
                    if d.target_id == pat_id and prog_id not in seen:
                        results.append(
                            RecommendationItem(
                                target_id=prog_id,
                                target_name=rec.prog_name,
                                domain="PROGRESSION",
                                relation_type="STYLISTIC_AFFINITY",
                                strength="HIGH",
                                confidence=0.85,
                                description=f"Stylistic match with {rec.genre_scope}",
                                source_relation_id=d.source_relation_id,
                            )
                        )
                        seen.add(prog_id)

        return results

    def recommend_for_piano_module(self, piano_id: str) -> List[RecommendationItem]:
        """Recommend matching chord progressions and drum patterns for a given piano module."""
        if piano_id not in CANONICAL_PIANO_MODULES:
            raise KeyError(f"Unknown canonical piano module ID: '{piano_id}'. Expected P01..P19.")

        results: List[RecommendationItem] = []
        seen = set()

        # Check explicit relations from CSV
        for rel in self.get_relations_for_entity(piano_id):
            other_id = rel.target_id if rel.source_id == piano_id else rel.source_id
            if other_id.startswith("PROG-") and other_id not in seen:
                prog = CANONICAL_PROGRESSIONS.get(other_id)
                name = prog.name if prog else "Progression"
                results.append(
                    RecommendationItem(
                        target_id=other_id,
                        target_name=name,
                        domain="PROGRESSION",
                        relation_type=rel.relation_type,
                        strength=rel.formal_rule_or_strength,
                        confidence=1.0,
                        description=rel.description,
                        source_relation_id=rel.relation_id,
                    )
                )
                seen.add(other_id)
            elif other_id.startswith("PAT-") and other_id not in seen:
                pat_info = CANONICAL_DRUM_PATTERNS.get(other_id, {"name": "Drum Pattern"})
                results.append(
                    RecommendationItem(
                        target_id=other_id,
                        target_name=pat_info["name"],
                        domain="DRUM",
                        relation_type=rel.relation_type,
                        strength=rel.formal_rule_or_strength,
                        confidence=1.0,
                        description=rel.description,
                        source_relation_id=rel.relation_id,
                    )
                )
                seen.add(other_id)

        # Supplement with known stylistic pairings
        for prog_id in CANONICAL_PROGRESSIONS:
            if prog_id not in seen:
                rec = self.recommend_for_progression(prog_id)
                for p in rec.piano_voicings:
                    if p.target_id == piano_id and prog_id not in seen:
                        results.append(
                            RecommendationItem(
                                target_id=prog_id,
                                target_name=rec.prog_name,
                                domain="PROGRESSION",
                                relation_type="DIDACTIC_AFFINITY",
                                strength="HIGH",
                                confidence=0.85,
                                description=f"Harmonic application in {rec.genre_scope}",
                                source_relation_id=p.source_relation_id,
                            )
                        )
                        seen.add(prog_id)

        return results

    def _supplement_progression_recommendations(
        self,
        prog_id: str,
        drum_items: List[RecommendationItem],
        piano_items: List[RecommendationItem],
        seen_targets: Set[str],
    ) -> None:
        """Supplement explicit CSV relations with genre-idiomatic mappings for complete 28-archetype coverage."""
        supplemental_map: Dict[str, Dict[str, List[Tuple[str, str, str, float, str]]]] = {
            "PROG-001": {
                "drums": [("PAT-001", "Pop / Rock Straight", "COMMONLY_PAIRED_WITH", 1.0, "Pop 4-chord driving rhythm")],
                "piano": [("P07", "Zweihändige rollende Arpeggien", "TAUGHT_VIA", 1.0, "Ballad accompaniment"),
                          ("P03", "Zweihändige Begleitmuster (Pop Groove)", "DIDACTIC_APPLICATION", 0.9, "Pop groove pattern")],
            },
            "PROG-002": {
                "drums": [("PAT-018", "Liquid D&B Rolling Break", "COMMONLY_PAIRED_WITH", 1.0, "Liquid D&B breakbeat"),
                          ("PAT-001", "Pop / Rock Straight", "STYLISTICALLY_COMPATIBLE", 0.9, "Straight pop ballad feel")],
                "piano": [("P07", "Zweihändige rollende Arpeggien", "DIDACTIC_APPLICATION", 0.9, "Arpeggio wave texture"),
                          ("P02", "Akkordumkehrungen & Minimal Movement", "VOICED_BY", 0.85, "Minimal voice leading")],
            },
            "PROG-003": {
                "drums": [("PAT-012", "Jazz Traditional Ride", "COMMONLY_PAIRED_WITH", 1.0, "Traditional jazz swing ride"),
                          ("PAT-017", "Bebop Up-Tempo Comping", "STYLISTICALLY_COMPATIBLE", 0.9, "Fast bebop comping")],
                "piano": [("P05", "Zweihändige Shell-Voicings", "VOICED_BY", 1.0, "Shell voicings 3 & 7 guide tones"),
                          ("P08", "Drop-2 Voicings", "VOICED_BY", 1.0, "Four-voice drop-2 jazz chords")],
            },
            "PROG-004": {
                "drums": [("PAT-009", "Motown / Soul Stomp", "COMMONLY_PAIRED_WITH", 0.95, "Four-on-the-snare stomp"),
                          ("PAT-001", "Pop / Rock Straight", "STYLISTICALLY_COMPATIBLE", 0.9, "Doo-Wop backbeat")],
                "piano": [("P03", "Zweihändige Begleitmuster (Pop Groove)", "DIDACTIC_APPLICATION", 0.9, "Two-handed 50s accompaniment"),
                          ("P01", "Stamm-Dreiklänge & Topografie", "TAUGHT_VIA", 0.85, "Root-position triads")],
            },
            "PROG-005": {
                "drums": [("PAT-027", "Bossa Nova Authentic Brush", "STYLISTICALLY_COMPATIBLE", 0.85, "Acoustic brush groove"),
                          ("PAT-003", "Boom-Bap Hip-Hop", "STYLISTICALLY_COMPATIBLE", 0.85, "Flamenco hip-hop crossover")],
                "piano": [("P02", "Akkordumkehrungen & Minimal Movement", "VOICED_BY", 0.9, "Stepwise voice leading"),
                          ("P08", "Drop-2 Voicings", "VOICED_BY", 0.85, "Harmonic minor drop-2 voicings")],
            },
            "PROG-006": {
                "drums": [("PAT-001", "Pop / Rock Straight", "COMMONLY_PAIRED_WITH", 0.85, "Slow ballad pop beat")],
                "piano": [("P07", "Zweihändige rollende Arpeggien", "DIDACTIC_APPLICATION", 0.95, "Baroque arpeggiated texture"),
                          ("P02", "Akkordumkehrungen & Minimal Movement", "VOICED_BY", 0.9, "Smooth step voice leading")],
            },
            "PROG-007": {
                "drums": [("PAT-007", "Funk 'The One'", "COMMONLY_PAIRED_WITH", 1.0, "Funk 16th syncopation"),
                          ("PAT-020", "Authentic UKG 2-Step", "COMMONLY_PAIRED_WITH", 1.0, "UK Garage 2-step syncopation")],
                "piano": [("P09", "Rhythmische Akkordbegleitung", "COMPATIBLE_WITH", 0.95, "Charleston rhythm & offbeat stabs"),
                          ("P05", "Zweihändige Shell-Voicings", "VOICED_BY", 0.9, "Dorian guide tones")],
            },
            "PROG-008": {
                "drums": [("PAT-012", "Jazz Traditional Ride", "COMMONLY_PAIRED_WITH", 0.95, "Blues swing ride"),
                          ("PAT-001", "Pop / Rock Straight", "STYLISTICALLY_COMPATIBLE", 0.85, "Straight 8th blues rock")],
                "piano": [("P05", "Zweihändige Shell-Voicings", "VOICED_BY", 0.95, "Blues guide tones 3 & b7"),
                          ("P09", "Rhythmische Akkordbegleitung", "DIDACTIC_APPLICATION", 0.9, "Swung blues comping")],
            },
            "PROG-009": {
                "drums": [("PAT-014", "Soul Ballad 12/8", "COMMONLY_PAIRED_WITH", 0.9, "Lyrical 12/8 triplet ballad"),
                          ("PAT-001", "Pop / Rock Straight", "STYLISTICALLY_COMPATIBLE", 0.85, "Straight romantic ballad")],
                "piano": [("P07", "Zweihändige rollende Arpeggien", "DIDACTIC_APPLICATION", 0.9, "Flowing ballad arpeggios"),
                          ("P13", "Reharmonisation in der Praxis", "DIDACTIC_APPLICATION", 0.9, "Minor plagal modal interchange")],
            },
            "PROG-010": {
                "drums": [("PAT-009", "Motown / Soul Stomp", "COMMONLY_PAIRED_WITH", 0.9, "Soul stomp drive"),
                          ("PAT-001", "Pop / Rock Straight", "STYLISTICALLY_COMPATIBLE", 0.85, "Pop rock backbeat")],
                "piano": [("P04", "Vierklänge & Septakkorde", "VOICED_BY", 0.9, "Secondary dominant 7th chords"),
                          ("P19", "Chromatische Bassführung für Sekundärdominanten", "DIDACTIC_APPLICATION", 0.85, "Leading tone bass motion")],
            },
            "PROG-011": {
                "drums": [("PAT-001", "Pop / Rock Straight", "COMMONLY_PAIRED_WITH", 0.9, "Driving rock straight groove"),
                          ("PAT-005", "Berlin Peak Techno", "STYLISTICALLY_COMPATIBLE", 0.8, "Four-on-the-floor epic drive")],
                "piano": [("P06", "Sus- und Add-Akkorde", "DIDACTIC_APPLICATION", 0.9, "Modern modal epic voicing"),
                          ("P13", "Reharmonisation in der Praxis", "DIDACTIC_APPLICATION", 0.9, "Aeolian modal interchange")],
            },
            "PROG-012": {
                "drums": [("PAT-012", "Jazz Traditional Ride", "COMMONLY_PAIRED_WITH", 0.95, "Standard jazz swing"),
                          ("PAT-003", "Boom-Bap Hip-Hop", "STYLISTICALLY_COMPATIBLE", 0.85, "Sampled circle of 5ths groove")],
                "piano": [("P05", "Zweihändige Shell-Voicings", "VOICED_BY", 0.95, "Continuous guide-tone resolution"),
                          ("P08", "Drop-2 Voicings", "VOICED_BY", 0.9, "Smooth descending drop-2 cycle")],
            },
            "PROG-013": {
                "drums": [("PAT-012", "Jazz Traditional Ride", "COMMONLY_PAIRED_WITH", 0.95, "Medium swing ride"),
                          ("PAT-017", "Bebop Up-Tempo Comping", "STYLISTICALLY_COMPATIBLE", 0.9, "Up-tempo bebop comping")],
                "piano": [("P05", "Zweihändige Shell-Voicings", "VOICED_BY", 0.95, "Tritone substitution guide tones"),
                          ("P16", "Upper Structure Triads über Dominanten", "DIDACTIC_APPLICATION", 0.9, "Altered dominant upper structures")],
            },
            "PROG-014": {
                "drums": [("PAT-013", "Funk 16th Linear Ghost", "COMMONLY_PAIRED_WITH", 0.95, "Linear funk backbeat"),
                          ("PAT-007", "Funk 'The One'", "STYLISTICALLY_COMPATIBLE", 0.9, "Soul funk groove")],
                "piano": [("P08", "Drop-2 Voicings", "VOICED_BY", 0.9, "Backdoor drop-2 voicings"),
                          ("P18", "Backdoor Guide-Tone Voicings", "DIDACTIC_APPLICATION", 0.95, "Guide-tone resolution bVII7 -> I")],
            },
            "PROG-015": {
                "drums": [("PAT-001", "Pop / Rock Straight", "COMMONLY_PAIRED_WITH", 0.9, "J-Pop driving straight groove"),
                          ("PAT-003", "Boom-Bap Hip-Hop", "STYLISTICALLY_COMPATIBLE", 0.85, "Anime lo-fi hip-hop")],
                "piano": [("P04", "Vierklänge & Septakkorde", "VOICED_BY", 0.9, "Major 7th and minor 7th grips"),
                          ("P08", "Drop-2 Voicings", "VOICED_BY", 0.85, "Lush anime soundtrack voicings")],
            },
            "PROG-016": {
                "drums": [("PAT-017", "Bebop Up-Tempo Comping", "COMMONLY_PAIRED_WITH", 0.95, "High-tempo Coltrane swing"),
                          ("PAT-012", "Jazz Traditional Ride", "STYLISTICALLY_COMPATIBLE", 0.9, "Fast ride cymbal drive")],
                "piano": [("P08", "Drop-2 Voicings", "VOICED_BY", 0.9, "Giant Steps drop-2 grips"),
                          ("P16", "Upper Structure Triads über Dominanten", "DIDACTIC_APPLICATION", 0.9, "Secondary dominant tensions")],
            },
            "PROG-017": {
                "drums": [("PAT-013", "Funk 16th Linear Ghost", "COMMONLY_PAIRED_WITH", 1.0, "Neo-Soul linear ghost notes"),
                          ("PAT-012", "Jazz Traditional Ride", "STYLISTICALLY_COMPATIBLE", 0.9, "Traditional jazz backdoor swing")],
                "piano": [("P08", "Drop-2 Voicings", "VOICED_BY", 1.0, "Drop-2 open position voicings"),
                          ("P18", "Backdoor Guide-Tone Voicings", "DIDACTIC_APPLICATION", 0.95, "Authentic backdoor guide tones")],
            },
            "PROG-018": {
                "drums": [("PAT-013", "Funk 16th Linear Ghost", "COMMONLY_PAIRED_WITH", 0.9, "Cool jazz linear groove"),
                          ("PAT-012", "Jazz Traditional Ride", "STYLISTICALLY_COMPATIBLE", 0.9, "West Coast swing")],
                "piano": [("P08", "Drop-2 Voicings", "VOICED_BY", 0.9, "Substitute backdoor drop-2"),
                          ("P18", "Backdoor Guide-Tone Voicings", "DIDACTIC_APPLICATION", 0.9, "Guide tone resolving to major 7th")],
            },
            "PROG-019": {
                "drums": [("PAT-027", "Bossa Nova Authentic Brush", "COMMONLY_PAIRED_WITH", 0.95, "Bossa nova cross-stick brush"),
                          ("PAT-012", "Jazz Traditional Ride", "STYLISTICALLY_COMPATIBLE", 0.85, "Slow ballad swing")],
                "piano": [("P02", "Akkordumkehrungen & Minimal Movement", "VOICED_BY", 0.95, "Chromatic inner-line descent"),
                          ("P08", "Drop-2 Voicings", "VOICED_BY", 0.85, "Drop-2 line cliché voicings")],
            },
            "PROG-020": {
                "drums": [("PAT-012", "Jazz Traditional Ride", "COMMONLY_PAIRED_WITH", 0.9, "Modern jazz swing"),
                          ("PAT-017", "Bebop Up-Tempo Comping", "STYLISTICALLY_COMPATIBLE", 0.9, "Contemporary bebop comping")],
                "piano": [("P16", "Upper Structure Triads über Dominanten", "DIDACTIC_APPLICATION", 0.95, "Altered dominant tensions (#11, b9)"),
                          ("P08", "Drop-2 Voicings", "VOICED_BY", 0.9, "Contemporary drop-2 voicings")],
            },
            "PROG-021": {
                "drums": [("PAT-024", "Boom-Bap Golden Era", "STYLISTICALLY_COMPATIBLE", 1.0, "Boom-Bap swung MPC groove"),
                          ("PAT-030", "Phrygian Neo-Soul Halftime Shuffle", "STYLISTICALLY_COMPATIBLE", 0.9, "Laid-back halftime shuffle")],
                "piano": [("P12", "Zweihändige Rootless Voicings", "DIDACTIC_APPLICATION", 1.0, "Rootless 9th and 11th voicings"),
                          ("P17", "Zeitgenössisches Syncopated Comping", "DIDACTIC_APPLICATION", 0.9, "R&B syncopated pushes")],
            },
            "PROG-022": {
                "drums": [("PAT-001", "Pop / Rock Straight", "STYLISTICALLY_COMPATIBLE", 0.85, "Straight historical cadential beat"),
                          ("PAT-012", "Jazz Traditional Ride", "STYLISTICALLY_COMPATIBLE", 0.85, "Folk jazz swing")],
                "piano": [("P13", "Reharmonisation in der Praxis", "DIDACTIC_APPLICATION", 1.0, "Picardy third resolution"),
                          ("P02", "Akkordumkehrungen & Minimal Movement", "VOICED_BY", 0.9, "Smooth modal voice leading")],
            },
            "PROG-023": {
                "drums": [("PAT-018", "Liquid D&B Rolling Break", "STYLISTICALLY_COMPATIBLE", 1.0, "174 BPM two-step breakbeat"),
                          ("PAT-008", "Drum & Bass (Amen)", "STYLISTICALLY_COMPATIBLE", 0.9, "Classic Amen breakbeat")],
                "piano": [("P09", "Rhythmische Akkordbegleitung", "DIDACTIC_APPLICATION", 0.95, "Syncopated offbeat stabs"),
                          ("P12", "Zweihändige Rootless Voicings", "VOICED_BY", 0.9, "Liquid D&B rootless pad voicings")],
            },
            "PROG-024": {
                "drums": [("PAT-027", "Bossa Nova Authentic Brush", "STYLISTICALLY_COMPATIBLE", 1.0, "Authentic Bossa brush groove"),
                          ("PAT-029", "Samba Batucada Sectional", "STYLISTICALLY_COMPATIBLE", 0.85, "Brazilian samba feel")],
                "piano": [("P14", "Bossa Nova & Latin Piano Begleitung", "DIDACTIC_APPLICATION", 1.0, "LH Surdo / RH Bossa Clave"),
                          ("P05", "Zweihändige Shell-Voicings", "VOICED_BY", 0.9, "Jazz-samba shell voicings")],
            },
            "PROG-025": {
                "drums": [("PAT-028", "Afro-Cuban Cha-Cha-Chá", "STYLISTICALLY_COMPATIBLE", 1.0, "Cha-Cha Conga Tumbao"),
                          ("PAT-031", "Afro-Cuban 6/8 Bembé Fusion", "COMMONLY_PAIRED_WITH", 1.0, "6/8 Bembé polyrhythmic clave")],
                "piano": [("P14", "Bossa Nova & Latin Piano Begleitung", "DIDACTIC_APPLICATION", 0.95, "Montuno Guajeo syncopated arpeggios"),
                          ("P09", "Rhythmische Akkordbegleitung", "COMPATIBLE_WITH", 0.9, "Latin syncopated stabs")],
            },
            "PROG-026": {
                "drums": [("PAT-012", "Jazz Traditional Ride", "STYLISTICALLY_COMPATIBLE", 0.9, "Traditional jazz brush swing"),
                          ("PAT-027", "Bossa Nova Authentic Brush", "STYLISTICALLY_COMPATIBLE", 0.85, "Acoustic brush groove")],
                "piano": [("P19", "Chromatische Bassführung für Sekundärdominanten", "DIDACTIC_APPLICATION", 1.0, "V7(6/5)/V chromatic descent"),
                          ("P11", "Akkordumkehrungen nach Gehör & Funktion", "DIDACTIC_APPLICATION", 0.95, "First-inversion 6/5 decoding")],
            },
            "PROG-027": {
                "drums": [("PAT-012", "Jazz Traditional Ride", "COMMONLY_PAIRED_WITH", 0.95, "Minor jazz blues ride swing"),
                          ("PAT-017", "Bebop Up-Tempo Comping", "STYLISTICALLY_COMPATIBLE", 0.9, "Fast bebop minor comping")],
                "piano": [("P05", "Zweihändige Shell-Voicings", "VOICED_BY", 0.95, "Minor blues guide tones"),
                          ("P16", "Upper Structure Triads über Dominanten", "DIDACTIC_APPLICATION", 0.9, "Altered V7(#11) turnaround voicings")],
            },
            "PROG-028": {
                "drums": [("PAT-030", "Phrygian Neo-Soul Halftime Shuffle", "COMMONLY_PAIRED_WITH", 1.0, "Phrygian neo-soul halftime shuffle"),
                          ("PAT-013", "Funk 16th Linear Ghost", "STYLISTICALLY_COMPATIBLE", 0.9, "Linear funk ghost notes")],
                "piano": [("P12", "Zweihändige Rootless Voicings", "VOICED_BY", 1.0, "Two-handed rootless stacking"),
                          ("P08", "Drop-2 Voicings", "VOICED_BY", 0.9, "Soul cycle drop-2 voicings")],
            },
        }

        config = supplemental_map.get(prog_id)
        if not config:
            return

        for pat_id, name, rel_type, conf, desc in config.get("drums", []):
            if pat_id not in seen_targets:
                drum_items.append(
                    RecommendationItem(
                        target_id=pat_id,
                        target_name=name,
                        domain="DRUM",
                        relation_type=rel_type,
                        strength="STRONG" if conf >= 0.95 else "HIGH",
                        confidence=conf,
                        description=desc,
                        source_relation_id=None,
                    )
                )
                seen_targets.add(pat_id)

        for p_id, name, rel_type, conf, desc in config.get("piano", []):
            if p_id not in seen_targets:
                piano_items.append(
                    RecommendationItem(
                        target_id=p_id,
                        target_name=name,
                        domain="PIANO",
                        relation_type=rel_type,
                        strength="STRONG" if conf >= 0.95 else "HIGH",
                        confidence=conf,
                        description=desc,
                        source_relation_id=None,
                    )
                )
                seen_targets.add(p_id)


# Module singleton instance
_GLOBAL_RECOMMENDER: Optional[CrossDomainRecommender] = None


def get_recommender(relations_path: Optional[str | Path] = None) -> CrossDomainRecommender:
    """Obtain or instantiate the global CrossDomainRecommender singleton."""
    global _GLOBAL_RECOMMENDER
    if _GLOBAL_RECOMMENDER is None or relations_path is not None:
        _GLOBAL_RECOMMENDER = CrossDomainRecommender(relations_path)
    return _GLOBAL_RECOMMENDER


def recommend_for_progression(
    prog_id: str, relations_path: Optional[str | Path] = None
) -> CrossDomainRecommendation:
    """
    Produce a validated cross-domain recommendation vector for any canonical PROG ID.
    Validates drums (PAT-xxx), piano voicings (Pxx), and genre-specific bassline model.
    """
    return get_recommender(relations_path).recommend_for_progression(prog_id)


def recommend_for_drum_pattern(
    pat_id: str, relations_path: Optional[str | Path] = None
) -> List[RecommendationItem]:
    """Recommend matching chord progressions and piano modules for a given drum pattern ID."""
    return get_recommender(relations_path).recommend_for_drum_pattern(pat_id)


def recommend_for_piano_module(
    piano_id: str, relations_path: Optional[str | Path] = None
) -> List[RecommendationItem]:
    """Recommend matching chord progressions and drum patterns for a given piano module ID."""
    return get_recommender(relations_path).recommend_for_piano_module(piano_id)


def get_concept_relations(
    entity_id: str, relations_path: Optional[str | Path] = None
) -> List[CrossDomainRelation]:
    """Retrieve all explicit relations involving entity_id from MUSIC_CONCEPT_RELATIONS.csv."""
    return get_recommender(relations_path).get_relations_for_entity(entity_id)
