# STEPS – Genre-Forschung: Drum & Bass & Breakbeat-Architektur (Phase 4.7)

**Dokumenttyp:** GENRE SPECIFICATION & RHYTHMIC ENGINE ANALYSIS  
**Wissensdomänen:** M07 (Rhythmik), M08 (Drums & Percussion), M09 (Genres), M05/M06 (Harmonik & Bass)  
**Standard:** 480 PPQ (1 Viertel = 480 Ticks; 1 Takt 4/4 = 1920 Ticks, 16tel = 120 Ticks). General-MIDI Percussion Map (Kanal 10).  
**Epistemischer Status:** Struktur- und Akustikanalyse = `THEORY_SUPPORTED` / `EMPIRICALLY_SUPPORTED`; Groove-Patterns = `ILLUSTRATIVE_DESIGN` (eigenständige didaktische Kompositionen, keine geschützten Sample-Rips).

---

## 1. Die Anatomie von Drum & Bass bei 174 BPM

### Das Tempo-Zentrum (174 BPM):
Während früher Jungle (1992–1994) bei 155–165 BPM operierte, hat sich im modernen Drum & Bass seit den 2000er-Jahren **174 BPM** als weltweites Schwerkraftzentrum etabliert.
- Bei $174\text{ BPM}$ dauert ein 16tel-Schritt exakt:
  $$t_{16} = \frac{60.000}{174 \cdot 4} \approx 86{,}2\text{ ms}$$
- **Psychoakustischer Grund:** 86 Millisekunden sind schnell genug, um Adrenalin und motorischen Bewegungsdrang auszulösen, aber langsam genug, um komplexe 16tel-Ghost-Notes, synkopierte Bassdrum-Verschiebungen und Modulationen des Sub-Basses ohne Verwaschen zu artikulieren.

---

## 2. Metrische Dualität (Das Zwei-Geschwindigkeiten-Phänomen)

Das faszinierendste Merkmal von Drum & Bass ist die **metrische Dualität**:
1. **Die obere/schnelle Schicht (174 BPM):**  
   Schlagzeug, perkussive Rolls und Ride-Cymbals rasen in rasanten 16teln vorwärts.
2. **Die untere/langsame Schicht (87 BPM Halftime):**  
   Der Sub-Bass, melodische Pads und Vocal-Chops bewegen sich im entspannten Halftime-Tempo eines Hip-Hop- oder Reggae-Tracks (87 BPM).
- **Wirkung:** Der Körper des Hörers wiegt sich im ruhigen 87-BPM-Schwerpunkt, während der Geist der kinetischen Energie des 174-BPM-Rhythmus folgt.

---

## 3. Der "Two-Step"-Grundrhythmus & Ghost Notes

### Das Standard-Skelett:
- **Zählzeit 1 (Tick 0):** Wuchtige Kick (GM Note 36).
- **Zählzeit 2 (Tick 480):** Peitschende, helle Snare (GM Note 38 oder 40), oft mit Rimshot oder kurzem Clap gelayert.
- **Zählzeit 3+ (Tick 1200):** **Die synkopierte Kick!** Der entscheidende Vorwärts-Drang entsteht dadurch, dass die zweite Kick nicht auf 3 schlägt, sondern um ein Achtel verzögert auf die Zählzeit 3+ (Tick 1200) fällt!
- **Zählzeit 4 (Tick 1440):** Zweite Backbeat-Snare.

### Die Rolle der Ghost Notes:
Ohne Ghost Notes klingt ein Two-Step steif und leblos. Leise Snare-Ghost-Notes (Velocity 25–45) auf unbetonten 16tel-Positionen (z. B. Ticks 360, 600, 1080, 1320) simulieren die rollenden Wirbel klassischer Funk-Schlagzeuger.

---

## 4. Der Reese-Bass (Fundament & Interaktion)

- **Ursprung:** Entwickelt von Kevin Saunderson (unter dem Alias *Reese*) 1988 im Track *Just Want Another Chance*.
- **Synthese-Axiom:** Zwei leicht gegeneinander verstimmte Sägezahn-Wellenformen (Detune $\pm 5\text{ bis }15\text{ Cents}$) erzeugen kontinuierliche Phasenauslöschungen und Schwebungen.
- **Frequenz-Split:**
  - **Sub-Bereich ($< 90\text{ Hz}$):** Reiner, monofoner Sinus-Subbass, phasenstarr zur Bassdrum.
  - **Mittenbereich ($150\text{ Hz bis }3\text{ kHz}$):** Verzerrter, mit Chorus und LFO-Filtern animierter Sägezahn-Sound.

---

## 5. Neue kanonische Patterns

### PAT-018: Liquid D&B Rolling Break (2 Takte, 174 BPM)
Fließender, melodischer Drum & Bass (Stil: Calibre, High Contrast, LTJ Bukem).
- **Charakter:** Warme, akustisch angelehnte Snare mit zarten Ghost Notes und schimmerndem Ride-Becken.

#### Tick-Tabelle (Takt 1 & 2 bei 480 PPQ):
*Takt 1:*
- **Tick 0 (1):** Kick (36, Vel 115), Ride (51, Vel 80)
- **Tick 120 (1e):** Ride (51, Vel 50)
- **Tick 240 (1+):** Closed HH (42, Vel 70), Ride (51, Vel 75)
- **Tick 360 (1a):** Snare Ghost (38, Vel 30)
- **Tick 480 (2):** **Main Snare (38, Vel 118)**, Ride (51, Vel 85)
- **Tick 600 (2e):** Snare Ghost (38, Vel 35)
- **Tick 720 (2+):** Closed HH (42, Vel 70), Ride (51, Vel 75)
- **Tick 840 (2a):** Closed HH (42, Vel 50)
- **Tick 960 (3):** Ride (51, Vel 75) – *Kick schweigt!*
- **Tick 1080 (3e):** Snare Ghost (38, Vel 30)
- **Tick 1200 (3+):** **Synkopierte Kick (36, Vel 110)**, Open HH (46, Vel 85)
- **Tick 1320 (3a):** Snare Ghost (38, Vel 40)
- **Tick 1440 (4):** **Main Snare (38, Vel 120)**, Ride (51, Vel 85)
- **Tick 1560 (4e):** Closed HH (42, Vel 50)
- **Tick 1680 (4+):** Closed HH (42, Vel 70), Ride (51, Vel 75)
- **Tick 1800 (4a):** Snare Ghost (38, Vel 35)

*Takt 2 Variation:*
- Wie Takt 1, jedoch auf **Tick 1080 (3e)** eine zusätzliche antizipierende Kick (36, Vel 95), wodurch ein treibender Doppelkick-Roll ($1080 \to 1200$) entsteht!

---

### PAT-019: Neurofunk Two-Step (2 Takte, 174 BPM)
Harter, hochpräziser, elektronischer Drum & Bass (Stil: Noisia, Black Sun Empire).
- **Charakter:** Knochentrockene, kurze 808-Kick, scharfer Snare-Transienten-Schlag (Note 40, Electric Snare), metallisch gegatete Closed Hats, keine weichen Ride-Becken.

#### Tick-Tabelle (Auszug Takt 1):
- **Tick 0:** Kick (36, Vel 127), Closed Hat (42, Vel 90)
- **Tick 240:** Closed Hat (42, Vel 80)
- **Tick 480:** **Electric Snare (40, Vel 127)**, Closed Hat (42, Vel 90)
- **Tick 720:** Closed Hat (42, Vel 75)
- **Tick 960:** Closed Hat (42, Vel 85)
- **Tick 1200:** **Kick (36, Vel 122)**, Closed Hat (42, Vel 95)
- **Tick 1440:** **Electric Snare (40, Vel 127)**, Closed Hat (42, Vel 90)
- **Tick 1680:** Closed Hat (42, Vel 80)
