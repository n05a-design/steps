# STEPS – MUSICAL KNOWLEDGE ONTOLOGY (M01–M12)
**Version:** 1.0 (Phase 4 Master Architecture)  
**Status:** CANONICAL DOMAIN ONTOLOGY  
**Erhaltungszustand:** Dauerhaft erweiterbar; hierarchisch verknüpft über Concept-IDs.

---

## 1. Übersicht der 12 Kerndomänen

Die musikalische Ontologie von STEPS gliedert die Gesamtheit der Musiktheorie, Rhythmik, Instrumentalpädagogik und Softwarearchitektur in 12 strikt voneinander abgegrenzte, aber relational verbundene Fachbereiche:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        STEPS MUSIK-ONTOLOGIE                           │
├────────────────────┬────────────────────┬──────────────────────────────┤
│ THEORETISCHE BASIS │ HARMONISCHE STRUKTUR│ ZEIT & GROOVE                │
│ M01 Grundlagen     │ M04 Akkordtheorie  │ M07 Rhythmik & Metrum        │
│ M02 Notation       │ M05 Harmonielehre  │ M08 Drums & Percussion       │
│ M03 Intervalle/Tonl│ M06 Progressionen  │ M09 Genres & Stile           │
├────────────────────┼────────────────────┼──────────────────────────────┤
│ PRAXIS & SYSTEME   │                    │                              │
│ M10 Klavierpraxis  │ M11 Datenmodelle   │ M12 Komposition & Didaktik   │
└────────────────────┴────────────────────┴──────────────────────────────┘
```

---

## 2. Detaillierte Spezifikation der Domänen

### M01 – Grundlagen der Musik
* **Geltungsbereich:** Akustische, physikalische und wahrnehmungsbezogene Fundamente von Tonhöhe, Schall und Stimmung.
* **Kernkonzepte:**
  - `M01-01`: Schallwelle, Periode, Schwingungsfrequenz ($f$ in Hz).
  - `M01-02`: Kammerton $A_4 = 440\text{ Hz}$ (Standard ISO 16) und historische Stimmtonhöhen ($432\text{ Hz}, 415\text{ Hz}$).
  - `M01-03`: Oktave als Frequenzverdopplung ($2:1$-Intervall, 1200 Cents).
  - `M01-04`: 12-stufige gleichstufige Temperatur (12-TET / Equal Temperament, Halbtonfaktor $\sqrt[12]{2} \approx 1{,}059463$).
  - `M01-05`: Stimmungssysteme im Vergleich (Reine Stimmung / Just Intonation, Pythagoreische Stimmung, Mitteltönige Stimmungen).
  - `M01-06`: Tonhöhe (Pitch) vs. Tonklasse (Pitch-Class $\mathbb{Z}_{12} = \{0, 1, \dots, 11\}$).
* **Epistemischer Status:** `FORMAL_VERIFIED` (mathematisch-physikalisch bewiesen).

### M02 – Musiknotation
* **Geltungsbereich:** Repräsentation musikalischer Symbole, Vorzeichen, Enharmonik und Sprachkonventionen.
* **Kernkonzepte:**
  - `M02-01`: Notenliniensystem (5 Linien, 4 Zwischenräume) und Hilfslinien.
  - `M02-02`: Schlüssel (G-Schlüssel / Violinschlüssel, F-Schlüssel / Bassschlüssel, C-Schlüssel / Alt-/Tenorschlüssel).
  - `M02-03`: Noten- und Pausenwerte (Ganze, Halbe, Viertel, Achtel, Sechzehntel, Zweiunddreißigstel, Punktierung).
  - `M02-04`: Vorzeichen (Kreuz $\sharp$, Be $\flat$, Auflösungszeichen $\natural$, Doppelkreuz $\sharp\sharp$, Doppel-Be $\flat\flat$).
  - `M02-05`: Enharmonische Äquivalenz ($C\sharp \equiv D\flat$ in 12-TET akustisch äquivalent, aber syntaktisch distinkt).
  - `M02-06`: Nationale Notationskonventionen: Deutsches System ($H$ = Stammton, $B$ = erniedrigt) vs. Internationales System ($B$ = Stammton, $B\flat$ = erniedrigt).
  - `M02-07`: Tonartvorzeichnung (Quintenzirkel, Vorzeichenreihenfolge Fis-Cis-Gis-Dis-Ais-Eis bzw. B-Es-As-Des-Ges-Ces).
  - `M02-08`: Taktarten (Einfache Takte 2/4, 3/4, 4/4; Zusammengesetzte Takte 6/8, 9/8, 12/8; Ungerade Takte 5/4, 7/8).
  - `M02-09`: Artikulation (Staccato, Legato, Tenuto, Akzent, Marcato) und Dynamik ($pp$ bis $ff$).
* **Epistemischer Status:** `THEORY_SUPPORTED` / `STYLE_DEPENDENT`.

### M03 – Intervalle und Tonleitern
* **Geltungsbereich:** Lineare Tonabstände, Heptatonik, Pentatonik und synthetische Skalen.
* **Kernkonzepte:**
  - `M03-01`: Diatonische Intervalle und Qualitäten (Reine Intervalle 1, 4, 5, 8; Große/Kleine Intervalle 2, 3, 6, 7; Übermäßige/Verminderte Intervalle).
  - `M03-02`: Dur-Tonleiter (Ionian, Intervallmuster: Ganz-Ganz-Halb-Ganz-Ganz-Ganz-Halb / 2-2-1-2-2-2-1).
  - `M03-03`: Natürliche Moll-Tonleiter (Aeolian, Intervallmuster: Ganz-Halb-Ganz-Ganz-Halb-Ganz-Ganz / 2-1-2-2-1-2-2).
  - `M03-04`: Harmonisch Moll (erhöhte 7. Stufe / Leitton, übermäßige Sekunde zwischen 6 und 7).
  - `M03-05`: Melodisch Moll (aufwärts erhöhte 6. und 7. Stufe; abwärts natürlich Moll im traditionellen Satz).
  - `M03-06`: Kirchentonarten (Modi: Dorian, Phrygian, Lydian, Mixolydian, Aeolian, Locrian, Ionian).
  - `M03-07`: Pentatonik (Dur-Pentatonik: 1, 2, 3, 5, 6; Moll-Pentatonik: 1, $\flat 3$, 4, 5, $\flat 7$).
  - `M03-08`: Blues-Skalen (Moll-Pentatonik + Blue Note $\flat 5$; Dur-Blues-Skala + $\flat 3$).
  - `M03-09`: Symmetrische Skalen (Ganztonleiter / Whole-Tone, Halbton-Ganzton / Ganzton-Halbton verminderte Skalen / Octatonic).
* **Epistemischer Status:** `FORMAL_VERIFIED` / `THEORY_SUPPORTED`.

### M04 – Akkordtheorie
* **Geltungsbereich:** Vertikale Tonkombinationen, Terzschichtung, Akkordstrukturen und Erweiterungen.
* **Kernkonzepte:**
  - `M04-01`: Dreiklänge (Dur / Major [0, 4, 7], Moll / Minor [0, 3, 7], Vermindert / Diminished [0, 3, 6], Übermäßig / Augmented [0, 4, 8]).
  - `M04-02`: Akkordumkehrungen (Grundstellung 5/3, 1. Umkehrung Sextakkord 6, 2. Umkehrung Quartsextakkord 6/4).
  - `M04-03`: Vierklänge / Septakkorde (Maj7 [0, 4, 7, 11], Dominant-7 [0, 4, 7, 10], m7 [0, 3, 7, 10], m7b5 / halbvermindert [0, 3, 6, 10], dim7 / vollvermindert [0, 3, 6, 9]).
  - `M04-04`: Umkehrungen der Septakkorde (Grundstellung 7, Quintsextakkord 6/5, Terzquartakkord 4/3, Sekundakkord 2).
  - `M04-05`: Erweiterte Akkorde (Tension Notes: 9, 11, 13; None, Undezime, Tredezime).
  - `M04-06`: Alterierte Akkorde ($\flat 9, \sharp 9, \sharp 11, \flat 13$ über Dominantseptakkorden).
  - `M04-07`: Suspendierte Akkorde (`sus4` [0, 5, 7], `sus2` [0, 2, 7]) und Hinzufügungsakkorde (`add9`, `add2`, `add11`).
  - `M04-08`: Slash-Chords (Inversionsanzeige wie $C/E$ vs. Pedalbass wie $F/C$ vs. Hybrid-/Akkordfremder Bass wie $D\flat/C$).
  - `M04-09`: Polychords (Zwei unabhängige Dreiklänge übereinander, Notation $\frac{D}{C}$).
  - `M04-10`: Voicings (Close Voicing, Drop-2, Drop-3, Shell Voicings, Rootless Voicings, Quartenharmonik).
* **Epistemischer Status:** `THEORY_SUPPORTED`.

### M05 – Harmonielehre
* **Geltungsbereich:** Funktionale und stufenbezogene Beziehungen im tonalen und modalen Raum.
* **Kernkonzepte:**
  - `M05-01`: Stufentheorie (Römische Zahlen I, ii, iii, IV, V, vi, vii°).
  - `M05-02`: Funktionstheorie nach Riemann (Tonika T/t, Subdominante S/s, Dominante D/d, Parallelen Tp/tP, Gegenklänge Tg/tG).
  - `M05-03`: Kadenzen (Ganzkadenz authentisch $V \to I$, Plagalkadenz $IV \to I$, Halbkadenz $I \to V$, Trugschluss $V \to vi$).
  - `M05-04`: Sekundärdominanten (Zwischendominanten, z. B. $V^7/V$, $V^7/ii$).
  - `M05-05`: Modal Interchange / Borrowed Chords (Akkordanleihen aus parallelem Moll, z. B. $\flat VI, \flat VII, iv$ in Dur).
  - `M05-06`: Tritonsubstitution (Ersetzung von $V^7$ durch $\flat II^7$ mit identischem Tritonus zwischen 3 und $\flat 7$).
  - `M05-07`: Modulation (Diatonische Umdeutung, chromatische Modulation, enharmonische Verwechslung des verminderten Septakkords).
  - `M05-08`: Modale Harmonik (Vermeidung von Leittonkadenzen, Pendelharmonik, tonale Zentrierung ohne Dominantfunktion).
* **Epistemischer Status:** `THEORY_SUPPORTED`.

### M06 – Chord Progressions & Voice Leading
* **Geltungsbereich:** Horizontale Verkettung von Akkorden, harmonischer Fluss und Stimmführungsmetriken.
* **Kernkonzepte:**
  - `M06-01`: Standard-Progressionen (Doo-Wop $I - vi - IV - V$, Pop Four Chords $I - V - vi - IV$, Jazz Two-Five-One $ii^7 - V^7 - I^{\text{maj}7}$, Andalusische Kadenz $i - \flat VII - \flat VI - V$).
  - `M06-02`: Harmonischer Rhythmus (Akkordwechsel pro Takt, Phrasenlängen, Vorwegnahme / Antizipation).
  - `M06-03`: Kontrapunktische Stimmführungsregeln (Verbot paralleler Quinten und Oktaven im klassischen Satz).
  - `M06-04`: Paritäts- und Distanzmetriken (Tymoczko Voice-Leading Distance, $L_1$- und $L_2$-Normen auf dem Tonhöhen-Torus).
  - `M06-05`: Reharmonisierungstechniken (Passierende verminderte Akkorde, Coltrane-Changes, modale Färbung, Basslinien-Harmonisierung).
  - `M06-06`: Melodische Bindung (Guide Tones: Terz und Septime leiten die Stimmführung).
* **Epistemischer Status:** `FORMAL_VERIFIED` (Metriken) / `STYLE_DEPENDENT` (Stilregeln).

### M07 – Rhythmik und Metrum
* **Geltungsbereich:** Organisation von Zeit, Akzentuierung, Pulshierarchie und mikroskopischen Zeitstrukturen.
* **Kernkonzepte:**
  - `M07-01`: Puls (Tactus, BPM), Zählzeiten und Metrum (Metrische Hierarchie: Schwere vs. Leichte Zählzeiten).
  - `M07-02`: Rhythmisches Raster (Grid, Quantisierung in Ticks pro Viertelnote / PPQ, z. B. 480 oder 960 PPQ).
  - `M07-03`: Binäre vs. ternäre Unterteilung (Straight 1/8 vs. Triolen / Shuffle / Swung 1/8).
  - `M07-04`: Swing-Verhältnis (Swing Ratio $\rho = t_{\text{long}} / t_{\text{short}}$, z. B. $1{,}0$ straight, $2{,}0$ Triolenswing, $1{,}4$ Hardbop-Swing).
  - `M07-05`: Synkope (Akzentverschiebung auf unbetonte Zählzeiten oder Zählzeit-Zwischenräume).
  - `M07-06`: Polyrhythmik (Überlagerung unterschiedlicher regelmäßiger Teilungen, z. B. 3 gegen 2, 4 gegen 3).
  - `M07-07`: Polymetrik (Gleichzeitiges Ablaufen unterschiedlicher Taktarten, z. B. 3/4 über 4/4).
  - `M07-08`: Mikro-Timing (Push/Pull, Laid-back, Drunken Drumming, Dilla-Feel, Humanisierungsvarianzen in Millisekunden).
* **Epistemischer Status:** `FORMAL_VERIFIED` / `EMPIRICAL`.

### M08 – Drums und Percussion
* **Geltungsbereich:** Schlagzeuginstrumente, General MIDI Drum Mapping, Groove-Patterns und dynamische Gestaltung.
* **Kernkonzepte:**
  - `M08-01`: Standard Drum Kit Elemente (Bass Drum / Kick, Snare Drum, Side Stick / Rimshot, Hi-Hat closed/open/pedal, Toms, Crash Cymbal, Ride Cymbal).
  - `M08-02`: General MIDI (GM) Standard Drum Map (Kanal 10, Kick=35/36, Snare=38/40, Closed HH=42, Pedal HH=44, Open HH=46, Ride=51, Crash=49).
  - `M08-03`: Grundlegende Rhythmusrollen: Kick als Fundament/Puls; Snare als Backbeat (Zählzeiten 2 und 4 im 4/4-Takt); Hi-Hat als Zeitteiler/Subdivisions-Motor.
  - `M08-04`: Ghost Notes (Leise Snare- oder Kick-Schläge bei Velocity 20–50 zur Verdichtung des Grooves).
  - `M08-05`: Velocity-Kurven und dynamische Schichtung (Akzentuierung z. B. Downbeat 110–127, Offbeat 70–90, Füllnoten 35–60).
  - `M08-06`: Drum Fills und Übergänge (Melodische Tom-Läufe, Snare-Wirbel, Crash-Becken auf Zählzeit 1 des Folgeabschnitts).
  - `M08-07`: Mehrtaktige Architektur (2-Takt-, 4-Takt- und 8-Takt-Schleifen mit variierenden Turnarounds).
* **Epistemischer Status:** `THEORY_SUPPORTED` / `EMPIRICAL`.

### M09 – Genres und Stile
* **Geltungsbereich:** Spezifische historische und zeitgenössische Musikstile, Formkonventionen und Klangästhetiken.
* **Kernkonzepte:**
  - `M09-01`: Pop (Kompakte 3-4 Akkordfolgen, klarer Backbeat, Verse-Chorus-Pop-Form, 100–128 BPM).
  - `M09-02`: House (Four-on-the-Floor Kick auf 1, 2, 3, 4; Offbeat Open Hi-Hat auf den "Und"-Zählzeiten; Moll-Septakkord-Schleifen; 120–128 BPM).
  - `M09-03`: Techno (Monolithische Kick auf allen Vierteln, metallische Closed/Open Hats, modale Repetition, funktionale Dissonanz, 128–140 BPM).
  - `M09-04`: Hip-Hop / Boom Bap (Geschwungene 16tel, Laid-back Snare auf 2 und 4, Jazz-Sample-Harmonik, 85–95 BPM).
  - `M09-05`: Trap (Schnelle rollende 16tel/32tel Hi-Hats mit Triolen-Bursts, tiefe gestimmte 808-Sub-Bässe, Snare/Clap auf Zählzeit 3 bei Halftime, 130–160 BPM).
  - `M09-06`: UK Garage / 2-Step (Synkopierte Kicks unter Vermeidung der Zählzeit 2, gesprungene Snare/Rimshot, Shuffle-Hi-Hats, 130–138 BPM).
  - `M09-07`: Blues (12-taktiges Formschema $I^7 - IV^7 - I^7 - V^7 - IV^7 - I^7$, Dominantseptakkorde auf allen Stufen, Shuffle-Feel, Blue Notes).
  - `M09-08`: Jazz (Erweiterte Harmonik $ii - V - I$, Substitutionen, Walking Bass, Ride-Cymbal Spang-a-Lang Pattern, Comping).
  - `M09-09`: Funk & R&B (Betonung des "One" / Zählzeit 1, perkussive Gitarren- und Clavinet-Voicings, synkopierte Ghost-Note-Snares).
* **Epistemischer Status:** `STYLE_DEPENDENT`.

### M10 – Klavierpraxis und Spieltechnik
* **Geltungsbereich:** Ergonomie der Klaviatur, Griffmuster, zweihändige Koordination und didaktische Reduktion.
* **Kernkonzepte:**
  - `M10-01`: Topografie der Klaviatur (Weißtasten C-D-E-F-G-A-B; Schwarztasten in 2er- und 3er-Gruppen; Orientierung am $C_4$ / Middle C).
  - `M10-02`: Standard-Fingersätze (1=Daumen bis 5=Kleiner Finger; Daumenuntersatz bei Tonleitern).
  - `M10-03`: Grundgriffe für Dreiklänge (Rechte Hand Grundstellung: 1-3-5; 1. Umkehrung: 1-2-5; 2. Umkehrung: 1-3-5).
  - `M10-04`: Zweihändige Arbeitsteilung (Linke Hand: Bassfundament, Oktaven, Grundton+Quinte; Rechte Hand: Dreiklang, Voicing, Melodie).
  - `M10-05`: Klavier-Begleitmuster (Blockakkorde, Gebrochene Akkorde / Arpeggios, Alberti-Bässe, Pop-Balladen-Pattern 1-5-8-9, Stride-Piano).
  - `M10-06`: Voice-Leading am Klavier (Gemeinsame Töne liegenlassen, andere Stimmen schrittweise bewegen).
  - `M10-07`: Gehörbildung am Instrument (Intervallerkennung, Dur vs. Moll Unterscheidung, Kadenzhören).
* **Epistemischer Status:** `PEDAGOGICAL_SIMPLIFICATION` / `THEORY_SUPPORTED`.

### M11 – Musiksoftware und Datenmodelle
* **Geltungsbereich:** Formate, Protokolle, Softwarearchitektur, Invarianten und Schnittstellen.
* **Kernkonzepte:**
  - `M11-01`: MIDI 1.0 Protokoll (Baudrate 31250, Statusbytes, Datenbytes 0–127, Kanalmeldungen 1–16).
  - `M11-02`: Standard MIDI File (SMF Format 0: 1 Track; Format 1: Multi-Track; Header-Chunk `MThd`, Track-Chunk `MTrk`, Delta-Times in Ticks).
  - `M11-03`: Zeitmodelle (Metrische Zeit / Pulses per Quarter Note PPQ vs. Absolute Zeit / Sekunden und Samples).
  - `M11-04`: STEPS PitchClass- und NoteSpelling-Datenmodell (`diatonic_step: 0..6`, `alteration: -2..+2`, `octave: int`, `midi_number: 0..127`).
  - `M11-05`: MusicXML (Strukturierte XML-Repräsentation von Notation, Schlüsseln, Stimmen, Balken und Vortragsbezeichnungen).
  - `M11-06`: Verlustfreie Konvertierung vs. Informationsverlust (MIDI kennt keine Notennamen: $C\sharp_4$ und $D\flat_4$ sind beide Pitch 61).
* **Epistemischer Status:** `FORMAL_VERIFIED` (Standards).

### M12 – Komposition, Arrangement und Didaktik
* **Geltungsbereich:** Formale Gestaltung musikalischer Verläufe, Spannungsbögen und didaktische Vermittlung.
* **Kernkonzepte:**
  - `M12-01`: Musikalische Bausteine (Motiv, Phrase, Thema, Periode, Satz).
  - `M12-02`: Formtypen (Liedform AABA, Strophenform Verse-Chorus-Bridge, Rondo, Sonatenhauptsatzform, 12-Takt-Bluesform).
  - `M12-03`: Spannungs- und Energiekurven (Tension & Release durch harmonische Reibung, rhythmische Dichte, Dynamik).
  - `M12-04`: Didaktischer Stufenaufbau (Stufe 1: Einzelne Töne & Klaviatur -> Stufe 2: Dur/Moll-Dreiklänge -> Stufe 3: Einfache 2-4 Akkordfolgen -> Stufe 4: Rhythmus & Groove -> Stufe 5: Vierklänge & Reharmonisierung).
  - `M12-05`: Fehlerkultur für Anfänger (Angst vor falschen Tönen abbauen; jeder Halbtonschritt ist nur einen Schritt von einem Konsonanzton entfernt).
* **Epistemischer Status:** `PEDAGOGICAL_SIMPLIFICATION`.
