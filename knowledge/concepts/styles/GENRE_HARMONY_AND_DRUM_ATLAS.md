# STEPS – Genre Harmony & Drum Atlas: Erweiterte Genreprofile (OA-0023, M09)

**Dokumenttyp:** GENRE SPECIFICATION REFERENCE & EVENT MATRIX  
**Wissensdomänen:** M07 (Rhythmik), M08 (Drums), M09 (Genres), M06 (Progressionen), M11 (MIDI)  
**Standard:** 480 PPQ (Division = 480 Ticks / Viertelnote; 1 Takt 4/4 = 1920 Ticks, 2 Takte = 3840 Ticks), General-MIDI Percussion Map (Kanal 10).  
**Verknüpfte Identitäten:** PAT-001 bis PAT-031, PROG-001 bis PROG-028, P01 bis P19.

---

## Übersicht der Genreprofile

| Genre | Tempo | Metrum & Feel | Kick-Charakteristik | Snare / Backbeat | Hi-Hat / Perkussion | Harmonischer Fokus |
|---|---|---|---|---|---|---|
| **Pop** (Pilot 1) | 115 BPM | 4/4 Straight ($\rho = 1{,}0$) | 1 und 3 (Synkope 3+) | 2 und 4 (Snare 38) | Durchgehende 8tel | Diatonische 4-Chords |
| **House** (Pilot 2) | 124 BPM | 4/4 Straight ($\rho = 1{,}0$) | Four-on-the-Floor (1, 2, 3, 4) | 2 und 4 Clap (39) | Offbeat Open Hat (46) | Dorian / Aeolian Vamps |
| **Berlin Peak Techno** (OA-0023) | 132 BPM | 4/4 Straight ($\rho = 1{,}0$) | Wuchtige 909 auf 1, 2, 3, 4 | 2 und 4 Side Stick / Clap | Offbeat Hat + 3er-Rimshot | Minimal / Phrygian Drones |
| **Golden Era Boom-Bap** (OA-0023) | 90 BPM | 4/4 MPC-61% ($\rho \approx 1{,}56$) | 1 und 2e+ (Synkope vor 3) | 2 und 4 Laid-back (+26 Ticks) | Geschwungene 16tel mit Velocity-Drift | Gesampelte Jazz-Chords (ii-V-I) |
| **UK Garage 2-Step** (OA-0023) | 134 BPM | 4/4 MPC-58% ($\rho \approx 1{,}38$) | 1 und 3+ (Schlag 2 leer!) | 2 Side Stick, 4 Clap | Geschwungene Ghost-Hats & Shaker | Catchy Minor-9th & Sus4 |
| **Modern Halftime Trap** (OA-0023) | 140 BPM | 4/4 Halftime | Spärliche 808-Sub-Kicks | **Schlag 3** Hard Clap (39) | Rollende 32tel- / Triolen-Bursts | Phrygische / Äolische Loops |

---

## 1. Pilot-Genre 1: Pop (Contemporary & Classic Pop)

### A. Musikalische Charakteristik
* **Tempo-Bereich:** 100 – 128 BPM (Standard 115 BPM).
* **Harmonik:** Diatonische Dur- und Moll-Tonalität, hohe Hookline-Prägnanz, funktionale Entspannung.
* **Typischer Harmonischer Rhythmus:** 1 Akkord pro Takt.

### B. Charakteristische Akkordprogressionen
* **The Four Chords of Pop:** `I - V - vi - IV` (in C-Dur: `C - G - Am - F`, PROG-001).

### C. Rhythmus- & Drum-Architektur
* **Kick (MIDI 36):** Betont 1 und "3+" (Tick 1320).
* **Snare (MIDI 38):** Klarer Backbeat exakt auf 2 und 4.
* **Closed Hi-Hat (MIDI 42):** Durchgehende 8tel-Noten (`1 + 2 + 3 + 4 +`).

### D. 2-Takt Pop-Pattern (Event-Tabelle)
*Division: 480 PPQ. Takt 1: Ticks 0..1919; Takt 2: Ticks 1920..3839.*

| Takt.Zählzeit | Tick (480 PPQ) | Instrument | MIDI Pitch | Velocity | Funktion |
|---|---|---|---|---|---|
| **1.1.1** | 0 | Acoustic Kick | 36 | 120 | Downbeat Takt 1 |
| 1.1.1 | 0 | Closed Hi-Hat | 42 | 95 | Viertel-Akzent |
| 1.1.3 | 240 | Closed Hi-Hat | 42 | 75 | 8tel-Offbeat |
| **1.2.1** | 480 | Acoustic Snare | 38 | 115 | Backbeat 2 |
| 1.2.1 | 480 | Closed Hi-Hat | 42 | 90 | Viertel-Akzent |
| 1.2.3 | 720 | Closed Hi-Hat | 42 | 75 | 8tel-Offbeat |
| **1.3.1** | 960 | Acoustic Kick | 36 | 110 | Halbtakt-Fundament |
| 1.3.1 | 960 | Closed Hi-Hat | 42 | 95 | Viertel-Akzent |
| 1.3.3 | 1200 | Closed Hi-Hat | 42 | 75 | 8tel-Offbeat |
| 1.3.4 | 1320 | Acoustic Kick | 36 | 100 | Vorgezogene Synkope ("3+") |
| **1.4.1** | 1440 | Acoustic Snare | 38 | 115 | Backbeat 4 |
| 1.4.1 | 1440 | Closed Hi-Hat | 42 | 90 | Viertel-Akzent |
| 1.4.3 | 1680 | Closed Hi-Hat | 42 | 80 | Vorbereitung Takt 2 |
| **2.1.1** | 1920 | Acoustic Kick | 36 | 122 | Downbeat Takt 2 |
| 2.1.1 | 1920 | Closed Hi-Hat | 42 | 95 | Viertel-Akzent |
| 2.1.3 | 2160 | Closed Hi-Hat | 42 | 75 | 8tel-Offbeat |
| **2.2.1** | 2400 | Acoustic Snare | 38 | 115 | Backbeat 2 |
| 2.2.1 | 2400 | Closed Hi-Hat | 42 | 90 | Viertel-Akzent |
| 2.2.3 | 2640 | Closed Hi-Hat | 42 | 75 | 8tel-Offbeat |
| **2.3.1** | 2880 | Acoustic Kick | 36 | 112 | Halbtakt-Fundament |
| 2.3.1 | 2880 | Closed Hi-Hat | 42 | 95 | Viertel-Akzent |
| 2.3.3 | 3120 | Closed Hi-Hat | 42 | 75 | 8tel-Offbeat |
| 2.3.4 | 3240 | Acoustic Kick | 36 | 102 | Vorgezogene Synkope ("3+") |
| **2.4.1** | 3360 | Acoustic Snare | 38 | 118 | Backbeat 4 |
| 2.4.1 | 3360 | Closed Hi-Hat | 42 | 90 | Viertel-Akzent |
| 2.4.3 | 3600 | Closed Hi-Hat | 42 | 85 | Vorbereitung |

---

## 2. Pilot-Genre 2: House (Classic & Deep House)

### A. Musikalische Charakteristik
* **Tempo-Bereich:** 120 – 128 BPM (Standard 124 BPM).
* **Harmonik:** Modale Vamps (Dorian, Aeolian), Moll-Sept- und Moll-Neunt-Akkorde (`m7`, `m9`), Quarten-/Quintenspannungen.
* **Harmonischer Rhythmus:** 2- oder 4-taktige statische Schleifen.

### B. Charakteristische Akkordprogressionen
* **Dorian House Vibe:** `i^7 - IV^7 - i^7 - iv^7` (in A-Moll: `Am7 - D7 - Am7 - Dm7`, PROG-002).

### C. Rhythmus- & Drum-Architektur
* **Kick (MIDI 36):** Unumstößliches Four-on-the-Floor auf jedem Viertel (`1, 2, 3, 4`).
* **Open Hi-Hat (MIDI 46):** Markanter Offbeat auf den Achteln (`1+, 2+, 3+, 4+` / Ticks 240, 720, 1200, 1680).
* **Clap / Snare (MIDI 39 / 38):** Druckvoller Backbeat auf 2 und 4 (oft mit Kick gelayert).

### D. 2-Takt House-Pattern (Event-Tabelle)
*Division: 480 PPQ.*

| Takt.Zählzeit | Tick (480 PPQ) | Instrument | MIDI Pitch | Velocity | Funktion |
|---|---|---|---|---|---|
| **1.1.1** | 0 | Electric Kick | 36 | 127 | Downbeat 1 |
| 1.1.2 | 120 | Closed Hat (Shaker) | 42 | 60 | 16tel-Groove |
| **1.1.3** | 240 | Open Hi-Hat | 46 | 105 | **House-Offbeat ("Und")** |
| 1.1.4 | 360 | Closed Hat | 42 | 50 | Ghost-Tick |
| **1.2.1** | 480 | Electric Kick | 36 | 124 | Viertel 2 |
| 1.2.1 | 480 | Hand Clap | 39 | 110 | **Backbeat 2** |
| 1.2.2 | 600 | Closed Hat | 42 | 65 | 16tel-Drive |
| **1.2.3** | 720 | Open Hi-Hat | 46 | 105 | **House-Offbeat ("Und")** |
| 1.2.4 | 840 | Closed Hat | 42 | 55 | Ghost-Tick |
| **1.3.1** | 960 | Electric Kick | 36 | 124 | Viertel 3 |
| 1.3.2 | 1080 | Closed Hat | 42 | 60 | 16tel-Drive |
| **1.3.3** | 1200 | Open Hi-Hat | 46 | 105 | **House-Offbeat ("Und")** |
| 1.3.4 | 1320 | Closed Hat | 42 | 50 | Ghost-Tick |
| **1.4.1** | 1440 | Electric Kick | 36 | 124 | Viertel 4 |
| 1.4.1 | 1440 | Hand Clap | 39 | 110 | **Backbeat 4** |
| 1.4.2 | 1560 | Closed Hat | 42 | 65 | 16tel-Drive |
| **1.4.3** | 1680 | Open Hi-Hat | 46 | 110 | Offbeat vor Takt 2 |
| 1.4.4 | 1800 | Closed Hat | 42 | 75 | Takt-Abschluss |
| **2.1.1** | 1920 | Electric Kick | 36 | 127 | Downbeat Takt 2 |
| 2.1.3 | 2160 | Open Hi-Hat | 46 | 105 | House-Offbeat |
| **2.2.1** | 2400 | Electric Kick | 36 | 124 | Viertel 2 |
| 2.2.1 | 2400 | Hand Clap | 39 | 112 | Backbeat 2 |
| 2.2.3 | 2640 | Open Hi-Hat | 46 | 105 | House-Offbeat |
| **2.3.1** | 2880 | Electric Kick | 36 | 124 | Viertel 3 |
| 2.3.3 | 3120 | Open Hi-Hat | 46 | 105 | House-Offbeat |
| **2.4.1** | 3360 | Electric Kick | 36 | 124 | Viertel 4 |
| 2.4.1 | 3360 | Hand Clap | 39 | 112 | Backbeat 4 |
| 2.4.3 | 3600 | Open Hi-Hat | 46 | 110 | Offbeat vor Loop |

---

## 3. Genre 3: Berlin Peak Techno (PAT-005, PAT-025)

### A. Musikalische Charakteristik
* **Tempo-Bereich:** 130 – 136 BPM (Referenztempo: 132 BPM).
* **Harmonik:** Strikt modal, oft monochromatisch zentriert auf Moll-Grundton ($i$); Tritonus-Spannungsakkorde ($i \leftrightarrow \flat V$), Phrygischer Halbtonschritt ($\flat II \leftrightarrow i$), hypnotische Synthesizer-Filter-Drones.
* **Metrum & Micro-Timing:** 4/4 unnachgiebig straight ($\rho = 1{,}0$), hochpräzise Maschinenquantisierung, metallisch-industrielle Textur.

### B. Charakteristische Harmonik & Bass-Progressionen
* **Dark Peak Drone:** $i - i - \flat II - i$ (in D-Moll: `Dm - Dm - Eb - Dm`, PROG-005).
* **Synth Stabs:** Schnelle staccato Terz-lose Quartenvoicings (z. B. `D - G - C`) über tiefem Bass-Rumble.

### C. Rhythmus- & Drum-Architektur
* **Kick Drum (MIDI 36):** Dominante, bassgewaltige 909-Kick auf allen Viertelschlägen (`1, 2, 3, 4`) mit langem Decay und Sub-Rumble auf 40–50 Hz.
* **Open Hi-Hat (MIDI 46):** Schneidende 909 Open Hat auf den 8tel-Offbeats (`1+, 2+, 3+, 4+`).
* **Side Stick / Percussion (MIDI 37):** Polyrhythmische 3-gegen-4 Akzente (z. B. alle 3 Sechzehntel = 360 Ticks), die dem Four-on-the-Floor Puls kinetische Vorwärtsenergie verleihen.
* **Clap (MIDI 39):** Trocken gegateter Clap auf 2 und 4.

### D. 2-Takt Berlin Peak Techno Pattern (Event-Tabelle)
*Division: 480 PPQ (PAT-025).*

| Takt.Zählzeit | Tick (480 PPQ) | Instrument | MIDI Pitch | Velocity | Ästhetische Rolle |
|---|---|---|---|---|---|
| **1.1.1** | 0 | 909 Bass Drum | 36 | 127 | Wuchtiger Downbeat |
| 1.1.1 | 0 | Closed Hi-Hat | 42 | 80 | Taktanker |
| 1.1.2 | 120 | Closed Hi-Hat | 42 | 60 | 16tel Drive |
| **1.1.3** | 240 | Open Hi-Hat | 46 | 115 | **Metallischer Offbeat ("Und")** |
| 1.1.4 | 360 | Side Stick | 37 | 95 | **3er-Polyrhythmik Impuls 1** |
| **1.2.1** | 480 | 909 Bass Drum | 36 | 125 | Viertel 2 |
| 1.2.1 | 480 | Hand Clap | 39 | 110 | Backbeat 2 |
| 1.2.2 | 600 | Closed Hi-Hat | 42 | 65 | 16tel Drive |
| **1.2.3** | 720 | Open Hi-Hat | 46 | 115 | **Offbeat ("Und")** |
| 1.2.3 | 720 | Side Stick | 37 | 100 | **3er-Polyrhythmik Impuls 2** |
| **1.3.1** | 960 | 909 Bass Drum | 36 | 125 | Viertel 3 |
| 1.3.2 | 1080 | Side Stick | 37 | 105 | **3er-Polyrhythmik Impuls 3** |
| **1.3.3** | 1200 | Open Hi-Hat | 46 | 115 | **Offbeat ("Und")** |
| 1.3.4 | 1320 | Closed Hi-Hat | 42 | 70 | Drive |
| **1.4.1** | 1440 | 909 Bass Drum | 36 | 125 | Viertel 4 |
| 1.4.1 | 1440 | Hand Clap | 39 | 110 | Backbeat 4 |
| 1.4.1 | 1440 | Side Stick | 37 | 110 | **3er-Polyrhythmik Impuls 4** |
| **1.4.3** | 1680 | Open Hi-Hat | 46 | 120 | Taktübergangs-Offbeat |
| 1.4.4 | 1800 | Side Stick | 37 | 112 | **3er-Polyrhythmik Impuls 5** |
| **2.1.1** | 1920 | 909 Bass Drum | 36 | 127 | Downbeat Takt 2 |
| **2.1.3** | 2160 | Open Hi-Hat | 46 | 115 | Offbeat |
| 2.1.4 | 2280 | Side Stick | 37 | 95 | Polyrhythmik Fortsetzung |
| **2.2.1** | 2400 | 909 Bass Drum | 36 | 125 | Viertel 2 |
| 2.2.1 | 2400 | Hand Clap | 39 | 112 | Backbeat 2 |
| **2.2.3** | 2640 | Open Hi-Hat | 46 | 115 | Offbeat |
| 2.2.3 | 2640 | Side Stick | 37 | 100 | Polyrhythmik |
| **2.3.1** | 2880 | 909 Bass Drum | 36 | 125 | Viertel 3 |
| 2.3.2 | 3000 | Side Stick | 37 | 105 | Polyrhythmik |
| **2.3.3** | 3120 | Open Hi-Hat | 46 | 115 | Offbeat |
| **2.4.1** | 3360 | 909 Bass Drum | 36 | 125 | Viertel 4 |
| 2.4.1 | 3360 | Hand Clap | 39 | 112 | Backbeat 4 |
| 2.4.1 | 3360 | Side Stick | 37 | 110 | Polyrhythmik |
| 2.3.4 | 3240 | 909 Bass Drum (Ghost) | 36 | 90 | **Ghost-Kick Synkope vor Taktende** |
| **2.4.3** | 3600 | Open Hi-Hat | 46 | 120 | Offbeat vor Loop |

---

## 4. Genre 4: Golden Era Boom-Bap Hip-Hop (PAT-003, PAT-024)

### A. Musikalische Charakteristik
* **Tempo-Bereich:** 86 – 94 BPM (Standard 90 BPM).
* **Harmonik:** Typischerweise von Jazz-, Soul- oder Funk-Vinyl gesampelte Akkordketten: $ii^7 - V^7 - I^{\text{maj}7}$, $i^7 - iv^7$, Moll-Akkorde mit Nonen und Undezimen ($m^9, m^{11}$); warmer, gesättigter Rhodes- und Bass-Sound.
* **Metrum & Micro-Timing:** 4/4 mit ausgeprägtem MPC-3000-Swing **61%** ($\rho \approx 1{,}56$).
* **Laid-Back Backbeat:** Die Snare auf Zählzeit 2 und 4 wird gezielt um **+26 Ticks** (ca. 36 ms bei 90 BPM; ERR-034) nach hinten verzögert, wodurch der charakteristische „schleppende“ Head-Nod-Groove entsteht.

### B. Charakteristische Akkordprogressionen
* **Jazz Minor Turnaround:** $i^7 - \flat VI^{\text{maj}7} - ii^{\varnothing 7} - V^{7(\text{alt})}$ (in C-Moll: `Cm7 - Abmaj7 - Dm7b5 - G7alt`, PROG-003).

### C. Rhythmus- & Drum-Architektur
* **Kick Drum (MIDI 36):** Erster Schlag fett auf 1; zweiter Schlag synkopiert auf der geschwungenen Sechzehntel vor der 3 ("2e+"), die 3 selbst bleibt oft frei.
* **Acoustic Snare (MIDI 38):** Satter Rim/Crack auf 2 und 4 mit Laid-Back-Versatz (+26 Ticks) und subtilen Ghost-Notes (Velocity 30–50).
* **Closed Hi-Hat (MIDI 42):** Kontinuierliche 16tel-Kette mit MPC-61%-Offset auf allen geraden 16tel-Teilungen (Ticks: unverschoben 0, 240; verschoben auf Tick 146 statt 120, 386 statt 360) und dynamischem Velocity-Verlauf.

### D. 2-Takt Boom-Bap Pattern (Event-Tabelle)
*Division: 480 PPQ (PAT-024).*

| Takt.Zählzeit | Tick (480 PPQ) | Instrument | MIDI Pitch | Velocity | Ästhetische Rolle |
|---|---|---|---|---|---|
| **1.1.1** | 0 | Acoustic Kick | 36 | 118 | Schwerer Downbeat |
| 1.1.1 | 0 | Closed Hi-Hat | 42 | 90 | Betonte 16tel |
| 1.1.2 | 146 | Closed Hi-Hat | 42 | 68 | **MPC-61% Swing-Tick (+26 Ticks)** |
| 1.1.3 | 240 | Closed Hi-Hat | 42 | 82 | Gerade 8tel |
| 1.1.4 | 386 | Closed Hi-Hat | 42 | 62 | **MPC-61% Swing-Tick** |
| 1.2.1 | 480 | Closed Hi-Hat | 42 | 88 | Zählzeit 2 |
| **1.2.1+** | 506 | Acoustic Snare | 38 | 116 | **Laid-Back Backbeat (+26 Ticks / 36 ms)** |
| 1.2.2 | 626 | Closed Hi-Hat | 42 | 65 | Swing-Tick |
| **1.2.3** | 720 | Acoustic Kick | 36 | 112 | **Synkopen-Kick ("2+")** |
| 1.2.3 | 720 | Closed Hi-Hat | 42 | 80 | Gerade 8tel |
| 1.2.4 | 866 | Closed Hi-Hat | 42 | 70 | Swing-Tick vor 3 |
| 1.3.1 | 960 | Closed Hi-Hat | 42 | 85 | Schlag 3 (Kick ausgespart) |
| 1.3.2 | 1106 | Closed Hi-Hat | 42 | 65 | Swing-Tick |
| 1.3.3 | 1200 | Closed Hi-Hat | 42 | 80 | Gerade 8tel |
| 1.3.4 | 1346 | Acoustic Snare (Ghost) | 38 | 45 | **Ghost Snare Note** |
| 1.3.4 | 1346 | Closed Hi-Hat | 42 | 68 | Swing-Tick |
| 1.4.1 | 1440 | Closed Hi-Hat | 42 | 90 | Zählzeit 4 |
| **1.4.1+** | 1466 | Acoustic Snare | 38 | 118 | **Laid-Back Backbeat (+26 Ticks)** |
| 1.4.2 | 1586 | Closed Hi-Hat | 42 | 62 | Swing-Tick |
| 1.4.3 | 1680 | Closed Hi-Hat | 42 | 82 | Vorbereitung Takt 2 |
| 1.4.4 | 1826 | Closed Hi-Hat | 42 | 72 | Letzter Swing-Impuls |
| **2.1.1** | 1920 | Acoustic Kick | 36 | 120 | Downbeat Takt 2 |
| 2.1.1 | 1920 | Closed Hi-Hat | 42 | 92 | Betonte 16tel |
| 2.1.2 | 2066 | Closed Hi-Hat | 42 | 68 | MPC-61% Swing-Tick |
| 2.1.3 | 2160 | Closed Hi-Hat | 42 | 82 | Gerade 8tel |
| 2.1.4 | 2306 | Closed Hi-Hat | 42 | 62 | Swing-Tick |
| 2.2.1 | 2400 | Closed Hi-Hat | 42 | 88 | Zählzeit 2 |
| **2.2.1+** | 2426 | Acoustic Snare | 38 | 116 | **Laid-Back Backbeat (+26 Ticks)** |
| 2.2.3 | 2640 | Acoustic Kick | 36 | 110 | Synkopen-Kick |
| 2.3.3 | 3120 | Acoustic Kick | 36 | 105 | Zusätzlicher Push auf "3+" |
| **2.4.1+** | 3386 | Acoustic Snare | 38 | 120 | **Laid-Back Backbeat (+26 Ticks)** |

---

## 5. Genre 5: UK Garage 2-Step (PAT-004, PAT-020, PAT-023, PAT-026)

### A. Musikalische Charakteristik
* **Tempo-Bereich:** 130 – 136 BPM (Standard 134 BPM).
* **Harmonik:** Urban Soul- und R&B-Harmonik, üppige $m^9$-, $\text{add}^9$- und $\text{sus}^4$-Akkorde, parallele Verschiebungen, Vocoder-Chops, drückender Reese- oder Sine-Sub-Bass.
* **Metrum & Micro-Timing:** 4/4 mit markantem MPC-Swing **58%** (Tick 139) bis **64%** (Tick 154) bei 480 PPQ.
* **Das 2-Step-Prinzip:** Der Kick-Schlag auf Zählzeit **2 wird strikt weggelassen**; stattdessen springt der Groove über synkopierte Kicks auf 1 und "3+" (Tick 1200/1320), was dem Beat den charakteristischen federnden Vorwärtsdrang verleiht.

### B. Charakteristische Akkordprogressionen
* **London Underground 2-Step:** $i^9 - \flat VII^{\text{sus}4} - \flat VI^{\text{maj}7} - \flat VII$ (in F-Moll: `Fm9 - Eb(sus4) - Dbmaj7 - Eb`, PROG-004).

### C. Rhythmus- & Drum-Architektur
* **Kick Drum (MIDI 36):** Trocken und punchig; exakt auf 1 und vorgezogen auf "3+" (Ticks 0, 1200 / 1339); Schlag 2 und 3 sind kickfrei!
* **Side Stick / Rimshot (MIDI 37):** Extrem trockener, perkussiver Rimshot auf Zählzeit **2**.
* **Hand Clap (MIDI 39):** Stereo-breiter Clap auf Zählzeit **4**.
* **Ghost Hi-Hats / Shaker (MIDI 42 / 70):** Dichte, verspielte 16tel-Ketten mit dynamischem Velocity-Verlauf und 58% Swing.

### D. 2-Takt UK Garage 2-Step Pattern (Event-Tabelle)
*Division: 480 PPQ (PAT-020 / PAT-023).*

| Takt.Zählzeit | Tick (480 PPQ) | Instrument | MIDI Pitch | Velocity | Ästhetische Rolle |
|---|---|---|---|---|---|
| **1.1.1** | 0 | Punchy Kick | 36 | 125 | Downbeat 1 |
| 1.1.1 | 0 | Closed Hi-Hat | 42 | 95 | Taktstart |
| 1.1.2 | 139 | Closed Hi-Hat | 42 | 60 | **58% MPC-Swing-Hat** |
| 1.1.3 | 240 | Closed Hi-Hat | 42 | 80 | Gerade 8tel |
| 1.1.4 | 379 | Shaker | 70 | 55 | Ghost Shuffle |
| **1.2.1** | 480 | Side Stick | 37 | 115 | **Backbeat 2 (Kick bleibt frei!)** |
| 1.2.2 | 619 | Closed Hi-Hat | 42 | 65 | Swing-Hat |
| 1.2.3 | 720 | Closed Hi-Hat | 42 | 85 | Offbeat |
| 1.2.4 | 859 | Shaker | 70 | 60 | Ghost Shuffle |
| 1.3.1 | 960 | Closed Hi-Hat | 42 | 75 | Schlag 3 (Keine Kick!) |
| 1.3.2 | 1099 | Closed Hi-Hat | 42 | 70 | Swing-Hat |
| **1.3.3** | 1200 | Punchy Kick | 36 | 120 | **2-Step Synkopen-Kick ("3+")** |
| 1.3.3 | 1200 | Open Hi-Hat | 46 | 100 | Akzent-Hat |
| 1.3.4 | 1339 | Closed Hi-Hat | 42 | 65 | Swing-Hat |
| **1.4.1** | 1440 | Hand Clap | 39 | 118 | **Backbeat 4** |
| 1.4.2 | 1579 | Closed Hi-Hat | 42 | 60 | Swing-Hat |
| 1.4.3 | 1680 | Closed Hi-Hat | 42 | 80 | Vorbereitung Takt 2 |
| 1.4.4 | 1819 | Shaker | 70 | 70 | Shuffle Überleitung |
| **2.1.1** | 1920 | Punchy Kick | 36 | 125 | Downbeat Takt 2 |
| 2.1.2 | 2059 | Closed Hi-Hat | 42 | 62 | 58% Swing |
| **2.2.1** | 2400 | Side Stick | 37 | 115 | Backbeat 2 |
| **2.3.3** | 3120 | Punchy Kick | 36 | 122 | **2-Step Synkopen-Kick ("3+")** |
| 2.3.3 | 3120 | Open Hi-Hat | 46 | 105 | Offbeat Accent |
| **2.4.1** | 3360 | Hand Clap | 39 | 118 | Backbeat 4 |
| 2.4.4 | 3739 | Punchy Kick (Ghost) | 36 | 95 | **Doppelkick-Antizipation vor Takt 1** |

---

## 6. Genre 6: Modern Halftime Trap (PAT-006)

### A. Musikalische Charakteristik
* **Tempo-Bereich:** 136 – 148 BPM (Standard 140 BPM).
* **Harmonik:** Düstere Moll- und Phrygische Tonalität ($i - \flat VI$ oder $i - \flat II$), sparse Melodielinien (Glocken, verhallte Pianos, Flöten-Samples), extrem lange, tief gestimmte 808-Subbässe mit Tonhöhenbeugungen (Pitch-Slides).
* **Metrum & Halftime-Feel:** Notiert im 4/4-Takt bei 140 BPM, fühlt sich das Tempo durch die Platzierung des Backbeats wie **70 BPM Halftime** an.

### B. Charakteristische Akkordprogressionen
* **Phrygian Dark Trap:** $i - \flat II - i - \flat VII$ (in C-Moll: `Cm - Db - Cm - Bbm`, PROG-006).

### C. Rhythmus- & Drum-Architektur
* **808 Sub-Bass Kick (MIDI 36):** Sehr tiefe Sinus-Kick mit langem Sustain; sitzt auf Zählzeit 1 und unregelmäßigen Offbeats, korrespondiert direkt mit der melodischen Bassline.
* **Trap Clap / Snare (MIDI 39 / 40):** Der entscheidende Halftime-Effekt: **Der primäre Backbeat liegt ausschließlich auf Zählzeit 3 (Tick 960)**! Schlag 2 und 4 bleiben frei von Snares.
* **Hi-Hat Rolls (MIDI 42):** Hochdynamische Closed Hi-Hat-Figuren; wechseln zwischen geraden 16teln, rollenden 32teln (Ticks 60), 64tel-Rampen und Triolen-Bursts mit massiven Velocity-Kurven (Crescendo von 30 auf 110).

### D. 2-Takt Trap Halftime Pattern (Event-Tabelle)
*Division: 480 PPQ (PAT-006).*

| Takt.Zählzeit | Tick (480 PPQ) | Instrument | MIDI Pitch | Velocity | Ästhetische Rolle |
|---|---|---|---|---|---|
| **1.1.1** | 0 | 808 Sub Kick | 36 | 127 | Gewaltiger Downbeat 1 |
| 1.1.1 | 0 | Closed Hi-Hat | 42 | 90 | Taktbeginn |
| 1.1.2 | 120 | Closed Hi-Hat | 42 | 70 | 16tel |
| 1.1.3 | 240 | Closed Hi-Hat | 42 | 85 | 8tel |
| 1.1.4 | 360 | Closed Hi-Hat | 42 | 70 | 16tel |
| 1.2.1 | 480 | Closed Hi-Hat | 42 | 90 | Viertel 2 (Keine Snare!) |
| 1.2.2 | 600 | Closed Hi-Hat | 42 | 75 | 16tel |
| 1.2.3 | 720 | 808 Sub Kick | 36 | 115 | **Synkopen-Basskick ("2+")** |
| 1.2.3 | 720 | Closed Hi-Hat | 42 | 80 | 8tel |
| 1.2.4 | 840 | Closed Hi-Hat | 42 | 70 | Vorbereitung Schlag 3 |
| **1.3.1** | 960 | Hard Trap Clap | 39 | 125 | **HALFTIME BACKBEAT (Zählzeit 3!)** |
| 1.3.1 | 960 | Closed Hi-Hat | 42 | 95 | Viertel 3 |
| 1.3.2 | 1080 | Closed Hi-Hat | 42 | 70 | 16tel |
| 1.3.3 | 1200 | Closed Hi-Hat | 42 | 85 | 8tel |
| **1.3.4** | 1320 | Closed Hi-Hat | 42 | 40 | **Start 32tel Roll (Crescendo)** |
| 1.3.4+ | 1380 | Closed Hi-Hat | 42 | 65 | Roll Impuls 2 |
| **1.4.1** | 1440 | Closed Hi-Hat | 42 | 90 | Roll Peak |
| 1.4.1 | 1440 | 808 Sub Kick | 36 | 110 | Synkopen-Kick auf 4 |
| 1.4.2 | 1560 | Closed Hi-Hat | 42 | 75 | 16tel |
| 1.4.3 | 1680 | Closed Hi-Hat | 42 | 85 | 8tel |
| **1.4.4** | 1800 | Closed Hi-Hat | 42 | 50 | **Triolen-Burst vor Takt 2** |
| 1.4.4+ | 1840 | Closed Hi-Hat | 42 | 75 | Triolen-Burst |
| 1.4.4++ | 1880 | Closed Hi-Hat | 42 | 100 | Triolen-Burst Peak |
| **2.1.1** | 1920 | 808 Sub Kick | 36 | 127 | Downbeat Takt 2 |
| 2.1.1 | 1920 | Closed Hi-Hat | 42 | 95 | 16tel |
| 2.2.3 | 2640 | 808 Sub Kick | 36 | 115 | Synkopen-Kick |
| **2.3.1** | 2880 | Hard Trap Clap | 39 | 127 | **HALFTIME BACKBEAT (Zählzeit 3!)** |
| 2.3.3 | 3120 | Closed Hi-Hat | 42 | 85 | 8tel |
| **2.4.1** | 3360 | Closed Hi-Hat | 42 | 45 | **Fast 64tel Roll Break** |
| 2.4.1+ | 3390 | Closed Hi-Hat | 42 | 70 | 64tel Roll |
| 2.4.1++ | 3420 | Closed Hi-Hat | 42 | 95 | 64tel Roll |
| 2.4.1+++ | 3450 | Closed Hi-Hat | 42 | 110 | 64tel Roll Peak |
| 2.4.3 | 3600 | 808 Sub Kick | 36 | 120 | **Schwerer Offbeat Kick vor neuem Loop** |

---

## 7. Referenz-Mappings & Integritäts-Nachweis

| Genre | PAT-ID | PROG-ID | Piano Modul | Swing Engine Ratio ($\rho$) | Micro-Timing Regel |
|---|---|---|---|---|---|
| Pop | `PAT-001` | `PROG-001` | `P01` | $\rho = 1{,}0$ (Straight) | Rigid Grid |
| House | `PAT-002` | `PROG-002` | `P05` | $\rho = 1{,}0$ (Straight) | Four-on-the-Floor Offbeat |
| Techno | `PAT-005` / `PAT-025` | `PROG-005` | `P08` | $\rho = 1{,}0$ (Straight) | Polyrhythmic 3-against-4 Side Stick |
| Boom-Bap | `PAT-003` / `PAT-024` | `PROG-003` | `P12` | $\rho = 1{,}56$ (MPC-61%) | Laid-Back Snare +26 Ticks (36 ms) |
| UK Garage | `PAT-004` / `PAT-020` | `PROG-004` | `P05` | $\rho = 1{,}38$ (MPC-58%) | 2-Step (Beat 2 Kick Omission) |
| Trap | `PAT-006` | `PROG-006` | `P01` | $\rho = 1{,}0$ (Halftime) | Halftime Backbeat auf Schlag 3 |
