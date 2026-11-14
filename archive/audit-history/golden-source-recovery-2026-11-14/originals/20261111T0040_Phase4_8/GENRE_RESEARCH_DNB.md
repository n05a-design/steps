# STEPS – Genre-Forschung: Drum & Bass & Breakbeat-Architektur (Phase 4.8)

**Dokumenttyp:** GENRE SPECIFICATION & SUBGENRE BREAKBEAT ATLAS  
**Wissensdomänen:** M07 (Rhythmik), M08 (Drums & Percussion), M09 (Genres), M05/M06 (Harmonik & Bass)  
**Standard:** 480 PPQ (Division = 480 Ticks/Viertel; 1 Takt 4/4 = 1920 Ticks, 16tel = 120 Ticks). General-MIDI Percussion Map (Kanal 10).  
**Epistemischer Status:** Analyse & Akustikregeln = `THEORY_SUPPORTED` / `EMPIRICALLY_SUPPORTED`; Patterns = `ILLUSTRATIVE_DESIGN`.

---

## 1. Die Subgenre-Matrix des modernen Drum & Bass

| Subgenre | Typisches Tempo | Rhythmisches Skelett | Snare- & Percussion-Charakter | Bass-Interaktion | Wichtige Referenzen |
|---|---|---|---|---|---|
| **Liquid Funk** | 172–175 BPM | Two-Step mit rollenden 16tel-Ghost-Notes (`PAT-018`) | Organische Holz-Snare, schimmerndes Ride-Becken (GM 51), Shaker | Melodische Reese-Bässe, Sinus-Sub mit langen Release-Zeiten | Calibre, High Contrast, LTJ Bukem |
| **Neurofunk** | 174–176 BPM | Strikt quantisierter, harter Two-Step (`PAT-019`) | Knochentrockene Electric Snare (GM 40), metallisch gegatete Hats | Hochmodulierte, verzerrte Sawtooth-Wavetables mit Bandsättigung | Noisia, Black Sun Empire, Mefjus |
| **Jungle / Drumfunk** | 168–174 BPM | Zerschnittener, unruhiger Amen-Breakbeat (`PAT-021`) | Dynamische Snare-Wirbel, Crash-Synkopen, wechselnde Tonhöhen | Monofone, tiefe 808-Sub-Bass-Slides, Reagiert auf Break-Lücken | Goldie, Photek, Paradox, Dillinja |
| **Jump-Up** | 174–176 BPM | Minimalistisches Kick-Snare-Fundament (`PAT-022`) | Laute, durchsetzungsfähige Backbeat-Snare auf 2 und 4 ohne dichte Fills | Aggressive, hochgepitchte Synthesizer-Stabs ("Frogs/Screeches") | DJ Hazard, Hedex, Serum |

---

## 2. Metrische Schichten: Two-Step vs. Halftime-Wahrnehmung

Ein fundamentaler Fehler beim Programmieren von DnB besteht darin, die 174 BPM als reine Hektik zu begreifen.  
Die rhythmische Hierarchie gliedert sich in **drei metrische Ebenen**:
1. **Mikro-Ebene (174 BPM 16tel-Raster, $\approx 86\text{ ms}$):**  
   Hi-Hats, Shaker, Ghost-Snares und Ride-Cymbals. Diese Ebene erzeugt den kinetischen Vorwärts-Roll.
2. **Meso-Ebene (174 BPM Viertel-Raster, $\approx 345\text{ ms}$):**  
   Die Kicks (Schlag 1 und 3+) und Snares (Schlag 2 und 4). Sie bilden das rhythmische Gerüst für das Tanzen.
3. **Makro-Ebene (87 BPM Halftime-Ebene, $\approx 690\text{ ms}$ / Halbtakt):**  
   Der Sub-Bass, Akkord-Pads und Gesangslinien. Harmonische Wechsel finden fast ausschließlich in der Makro-Ebene (alle 2 oder 4 Takte) statt!

---

## 3. Neue kanonische Patterns

### PAT-021: Jungle / Amen Chopped Breakbeat (2 Takte, 174 BPM)
Inspiriert von der Zerschneidung des legendären *Amen Break* (The Winstons, 1969).
- **Charakter:** Synkopierte Kicks, dynamische Snare-Doppelschläge auf den 16tel-Offbeats, rollende Ride-Beckenschläge.

#### Tick-Tabelle (Auszug Takt 1, 480 PPQ):
- **Tick 0 (1):** Kick (36, Vel 120), Ride (51, Vel 85)
- **Tick 120 (1e):** Snare Ghost (38, Vel 40)
- **Tick 240 (1+):** Ride (51, Vel 75)
- **Tick 360 (1a):** Kick (36, Vel 100) [Vorgezogener Synkopen-Schlag!]
- **Tick 480 (2):** **Main Snare (38, Vel 125)**, Ride (51, Vel 85)
- **Tick 600 (2e):** Ride (51, Vel 70)
- **Tick 720 (2+):** **Snare Syncopation (38, Vel 110)** [Der klassische Amen-Doppelakzent!]
- **Tick 840 (2a):** Snare Ghost (38, Vel 45)
- **Tick 960 (3):** Ride (51, Vel 80)
- **Tick 1080 (3e):** Snare Ghost (38, Vel 40)
- **Tick 1200 (3+):** **Kick (36, Vel 115)**, Crash (49, Vel 95)
- **Tick 1320 (3a):** Snare Ghost (38, Vel 50)
- **Tick 1440 (4):** **Main Snare (38, Vel 125)**, Ride (51, Vel 85)
- **Tick 1680 (4+):** Ride (51, Vel 75)
- **Tick 1800 (4a):** Kick (36, Vel 95) [Push vor Taktgrenze]

---

### PAT-022: Jump-Up Minimal Bouncer (2 Takte, 174 BPM)
- **Charakter:** Strikt aufgeräumter Beat, der maximale akustische Energie für subsonische Basswellen freihält.
- **Takt 1 & 2:** Kick stoisch auf Tick 0 und Tick 1200 (3+). Snare exakt auf Tick 480 (2) und Tick 1440 (4). Closed Hats (Note 42) auf allen geraden Achteln (Tick 0, 240, 480, 720, 960, 1200, 1440, 1680).
