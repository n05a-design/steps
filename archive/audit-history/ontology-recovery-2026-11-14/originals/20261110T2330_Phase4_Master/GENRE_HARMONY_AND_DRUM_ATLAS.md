# STEPS – GENRE HARMONY & DRUM ATLAS: PILOT PROFILE (POP & HOUSE)
**Dokumenttyp:** GENRE SPECIFICATION REFERENCE  
**Wissensdomänen:** M08 (Drums), M09 (Genres), M06 (Progressionen), M07 (Rhythmik)

---

## 1. Pilot-Genre 1: Pop (Contemporary & Classic Pop)

### A. Musikalische Charakteristik
* **Tempo-Bereich:** 100 – 128 BPM (Balladen: 70–90 BPM; Dance-Pop: 120–128 BPM).
* **Harmonik:** Diatonische Dur- und Moll-Tonalität, hohe Hookline-Prägnanz, funktionale Entspannung, Vermeidung komplexer Alterationen.
* **Typischer Harmonischer Rhythmus:** 1 Akkord pro Takt (seltener 2 Akkorde pro Takt).

### B. Charakteristische Akkordprogressionen
1. **The Four Chords of Pop (Diatonische 4-Akkord-Schleife):**
   - Stufenfolge: `I - V - vi - IV`
   - In C-Dur: `C - G - Am - F`
   - Wirkung: Universell, triumphal, hochgradig vertraut.
   - Varianten:
     - `vi - IV - I - V` (Moll-Fokus / "Sad Pop", z. B. `Am - F - C - G`)
     - `I - vi - IV - V` (50s Doo-Wop-Progression, z. B. `C - Am - F - G`)
     - `I - IV - vi - V` (Moderner Pop-Aufbau, z. B. `C - F - Am - G`)

### C. Rhythmus- & Drum-Architektur
* **Taktart:** 4/4 Standard.
* **Metrische Rollenaufteilung:**
  - **Kick Drum (MIDI 36):** Betont Zählzeit 1 und oft die "3+" (Synkope vor Zählzeit 4) oder Zählzeiten 1 und 3.
  - **Snare / Clap (MIDI 38 / 39):** Klarer, druckvoller **Backbeat** exakt auf Zählzeit **2 und 4**.
  - **Closed Hi-Hat (MIDI 42):** Durchgehende 8tel-Noten (`1 + 2 + 3 + 4 +`), mit leichter Akzentuierung auf den Viertelschlägen.
* **Micro-Timing & Feel:** Straight (Swing-Ratio $\rho = 1{,}0$), tighte Quantisierung.

### D. Exemplarisches 2-Takt Pop-Pattern (Event-Tabelle)
*Raster: 16tel-Auflösung (1 Takt = 16 Schritte zu je 120 Ticks bei 480 PPQ).*

| Zählzeit | Tick (480 PPQ) | Instrument | MIDI Pitch | Velocity (0–127) | Funktion |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1.1.1** | 0 | Kick Drum | 36 | 120 | Downbeat / Taktbeginn |
| 1.1.1 | 0 | Closed Hi-Hat | 42 | 95 | Viertel-Akzent |
| 1.1.3 | 240 | Closed Hi-Hat | 42 | 75 | 8tel-Offbeat |
| **1.2.1** | 480 | Snare Drum | 38 | 115 | **Backbeat** |
| 1.2.1 | 480 | Closed Hi-Hat | 42 | 90 | Viertel-Akzent |
| 1.2.3 | 720 | Closed Hi-Hat | 42 | 75 | 8tel-Offbeat |
| **1.3.1** | 960 | Kick Drum | 36 | 110 | Halbtakt-Fundament |
| 1.3.1 | 960 | Closed Hi-Hat | 42 | 95 | Viertel-Akzent |
| 1.3.3 | 1200 | Closed Hi-Hat | 42 | 75 | 8tel-Offbeat |
| 1.3.4 | 1320 | Kick Drum | 36 | 100 | **Vorgezogene Synkope ("3+")** |
| **1.4.1** | 1440 | Snare Drum | 38 | 115 | **Backbeat** |
| 1.4.1 | 1440 | Closed Hi-Hat | 42 | 90 | Viertel-Akzent |
| 1.4.3 | 1680 | Closed Hi-Hat | 42 | 80 | Vorbereitung Takt 2 |

---

## 2. Pilot-Genre 2: House (Classic / Deep / Tech House)

### A. Musikalische Charakteristik
* **Tempo-Bereich:** 120 – 128 BPM (Standard 124–126 BPM).
* **Harmonik:** Modale Schleifen (Dorian, Aeolian, seltener Phrygian), ausgeprägte Nutzung von Moll-Sept- und Moll-Neunt-Akkorden (`m7`, `m9`), Quartenquinten-Akkordschichtungen, hypnotische Wiederholung statt klassischer Kadenzenauflösung.
* **Harmonischer Rhythmus:** 2- oder 4-taktige statische harmonische Schleifen.

### B. Charakteristische Akkordprogressionen
1. **Dorian / Soulful House Vibe:**
   - Stufenfolge: `i^7 - IV^7 - i^7 - iv^7` (oder `i^7 - $\flat VII^{\text{maj}7} - \flat VI^{\text{maj}7} - \flat VII^{\text{maj}7}`)
   - In A-Moll: `Am7 - D7 - Am7 - Dm7` (oder `Am7 - Gmaj7 - Fmaj7 - Gmaj7`)
   - Voicings: Rootless Voicings am Klavier/Rhodes (z. B. linke Hand Bass `A`, rechte Hand `C - E - G - B` für $Am^9$).

### C. Rhythmus- & Drum-Architektur
* **Das unumstößliche Gesetz: Four-on-the-Floor:**
  - **Kick Drum (MIDI 36):** Gleichmäßige, durchgehende Schläge auf **jedem einzelnen Viertel** (`1, 2, 3, 4`).
  - **Open Hi-Hat (MIDI 46):** Der typische House-Lift entsteht durch eine laute, offene Hi-Hat exakt auf den **Offbeats** (`1+, 2+, 3+, 4+` / Zählzeit 240, 720, 1200, 1680).
  - **Snare / Clap (MIDI 38 / 39):** Liegt exakt mit der Kick auf Zählzeit **2 und 4** (oft gelayert: tiefe Snare + breiter Stereo-Clap).
  - **Closed Hi-Hat / Shaker (MIDI 42):** Subtile 16tel-Muster dazwischen, oft mit leichtem MPC-Swing ($\rho \approx 1{,}15$ bis $1{,}25$).

### D. Exemplarisches 1-Takt House-Pattern (Verifiziert aus technischem SMF-Standard)
*Tempo: 124 BPM. Division: 480 PPQ.*

| Zählzeit | Tick | Instrument | MIDI Pitch | Velocity | Ästhetische Rolle |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1.1.1** | 0 | Kick Drum | 36 | 127 | Downbeat 1 |
| 1.1.2 | 120 | Closed Hat (Shaker) | 42 | 60 | Subtiler 16tel-Groove |
| **1.1.3** | 240 | **Open Hi-Hat** | 46 | 105 | **House-Offbeat ("Und")** |
| 1.1.4 | 360 | Closed Hat | 42 | 50 | Ghost-Tick |
| **1.2.1** | 480 | Kick Drum | 36 | 124 | Viertel 2 |
| 1.2.1 | 480 | **Clap / Snare** | 39 | 110 | **Backbeat-Layering** |
| 1.2.2 | 600 | Closed Hat | 42 | 65 | 16tel-Drive |
| **1.2.3** | 720 | **Open Hi-Hat** | 46 | 105 | **House-Offbeat ("Und")** |
| 1.2.4 | 840 | Closed Hat | 42 | 55 | Ghost-Tick |
| **1.3.1** | 960 | Kick Drum | 36 | 124 | Viertel 3 |
| 1.3.2 | 1080 | Closed Hat | 42 | 60 | 16tel-Drive |
| **1.3.3** | 1200 | **Open Hi-Hat** | 46 | 105 | **House-Offbeat ("Und")** |
| 1.3.4 | 1320 | Closed Hat | 42 | 50 | Ghost-Tick |
| **1.4.1** | 1440 | Kick Drum | 36 | 124 | Viertel 4 |
| 1.4.1 | 1440 | **Clap / Snare** | 39 | 110 | **Backbeat-Layering** |
| 1.4.2 | 1560 | Closed Hat | 42 | 65 | 16tel-Drive |
| **1.4.3** | 1680 | **Open Hi-Hat** | 46 | 110 | Offbeat vor dem nächsten Takt |
| 1.4.4 | 1800 | Closed Hat (Accent) | 42 | 75 | Takt-Abschluss-Impuls |
