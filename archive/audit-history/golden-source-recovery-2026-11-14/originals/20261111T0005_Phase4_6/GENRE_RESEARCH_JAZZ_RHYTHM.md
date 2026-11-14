# STEPS – Genre Research: Jazz Drumming, Swing & Micro-Timing (Phase 4.6)

**Domänen:** M07 (Rhythmik & Micro-Timing), M08 (Drums), M09 (Genres), M11 (MIDI-Quantisierung)  
**Standard:** 480 PPQ (Division = 480 Ticks/Viertel); General-MIDI Percussion Map (Kanal 10); SPN-Noten; H/B-Klarheit.  
**Epistemischer Status:** Mathematische Zeitfunktionen und empirische Studien = `THEORY_SUPPORTED` / `FORMAL_VERIFIED`; Pattern-Entwürfe = `ILLUSTRATIVE_REFERENCE`.

---

## 1. Empirische Grundlage: Die Studie von Friberg & Sundström (2002)

| Parameter | Details der Untersuchung |
|---|---|
| **Quelle** | Anders Friberg & Andreas Sundström: *„Swing Ratios and Ensemble Timing in Jazz Performance: Evidence for a Common Rhythmic Pattern“*, in: *Music Perception* (2002), Vol. 19, No. 3. (Gelesen via Forschungszusammenfassung / WEB-4.6-04). |
| **Gegenstand** | Analyse professioneller Jazz-Schlagzeuger am Ride-Becken über Tempobereiche von 100 bis 320 BPM. |
| **Kritik am "Triolen-Mythos"** | In der Schulmusik wird Swing oft als starre Triolenaufteilung gelehrt ($\rho = 2{,}0$, d. h. lange Note : kurze Note = 2 : 1). Die Studie beweist formal: **Swing-Ratio $\rho$ ist keine Konstante, sondern eine lineare Funktion des Tempos!** |
| **Ergebnis 1 (Verhältnis)** | Bei langsamen Tempos ($< 120$ BPM) erreicht $\rho$ extreme Werte von bis zu **$3{,}5 : 1$** (punktierte Rhythmen nahe 16tel-Offbeats). Mit steigendem Tempo fällt $\rho$ stetig ab und nähert sich bei sehr schnellem Bebop ($> 280$ BPM) dem Wert **$1{,}0 : 1$** (nahezu Straight 8ths!). |
| **Ergebnis 2 (Absolute Dauer)** | Die absolute Dauer der *kurzen* Achtelnote (der Upbeat) bleibt über mittlere bis schnelle Tempi bemerkenswert konstant bei ca. **$100\text{ ms}$** ($\pm 15\text{ ms}$). Dies deutet auf eine psychoakustische und motorische Mindestzeit für artikulierte Swing-Achtel hin. |

---

## 2. Mathematische Modellierung der dynamischen Swing-Ratio in STEPS

Die Swing-Ratio $\rho = \frac{\Delta t_{\text{down}}}{\Delta t_{\text{up}}}$ bestimmt die zeitliche Platzierung des Offbeats innerhalb einer Viertelnote ($T = 480\text{ Ticks}$):

$$\Delta t_{\text{down}} = 480 \cdot \frac{\rho}{\rho + 1}, \quad \Delta t_{\text{up}} = 480 \cdot \frac{1}{\rho + 1}$$

### Lineare Näherungsfunktion nach Friberg & Sundström:
Für Tempi $B \in [100, 300]\text{ BPM}$ lässt sich $\rho(B)$ pragmatisch approximieren:

$$\rho(B) \approx \max\left(1{,}0, \; 3{,}0 - 0{,}008 \cdot (B - 100)\right)$$

*Beispielwerte:*
- **100 BPM (Ballade):** $\rho \approx 3{,}0$ $\implies$ Downbeat = 360 Ticks, Upbeat = 120 Ticks (exakt punktierte Achtel + Sechzehntel!).
- **130 BPM (Medium Swing):** $\rho \approx 2{,}76$ (Triolen-Nähe $\rho \approx 2{,}0$ bei ca. 180–200 BPM).
- **200 BPM (Up-Tempo Swing):** $\rho \approx 2{,}2$ $\implies$ Downbeat = 330 Ticks, Upbeat = 150 Ticks.
- **280 BPM (Fast Bebop):** $\rho \approx 1{,}56$ $\implies$ Downbeat = 292 Ticks, Upbeat = 188 Ticks.

---

## 3. Die 4 Säulen des traditionellen Jazz-Drumming

1. **Ride Cymbal (GM Note 51) – "The Spang-a-Lang":**
   Das Herz des Jazz. Der Puls wird nicht auf der Hi-Hat, sondern mit einem definierten Holzstock auf dem Ride-Becken geschlagen:
   - Viertel auf 1 und 3.
   - Viertel + geswingter Skip-Stroke auf 2 und 4.
2. **Pedal Hi-Hat (GM Note 44) – "The Foot Chick":**
   Schlägt **unbeirrbar auf den Zählzeiten 2 und 4** mit dem linken Fuß zu. Trockener, scharfer Klang. (Korrektur ERR-010: Niemals GM 42 für das getretene Pedal verwenden!).
3. **Bass Drum (GM Note 35) – "Feathering":**
   Im traditionellen Swing/Bebop wird die Bassdrum auf allen 4 Vierteln extrem leise gespielt (Velocity 20–35), oft so unaufdringlich, dass man sie kaum hört, sondern nur als Druck im Raum spürt. Sie stützt den Walking Bass des Kontrabassisten.
4. **Snare Drum (GM Note 38) & Left Hand – "Comping":**
   Die linke Hand spielt unregelmäßige, synkopierte Phrasen, um mit Solisten oder Klavierakkorden zu dialogisieren.

---

## 4. PAT-012 v2 – Traditional Jazz Ride Swing (Korrektur & Verifikation)

- **ID:** `PAT-012`
- **Tempo:** 130 BPM | **Metrum:** 4/4
- **GM Map:** Ride Cymbal 1 (51), Pedal Hi-Hat (44), Acoustic Bass Drum (35), Acoustic Snare (38).

### Exakte Tick-Tabelle für Takt 1 (480 PPQ, $\rho = 2{,}0$ vereinfachte Triolen-Projektion):

| Tick | Instrument (GM Note) | Velocity | Musikalische Funktion |
|---|---|---|---|
| **0** | **Ride Cymbal (51)**, Kick (35) | 90, 30 | Schlag 1: Hauptpuls + leises Feathering |
| **480** | **Ride Cymbal (51)**, **Pedal Hi-Hat (44)**, Kick (35) | 95, 85, 30 | Schlag 2: Hauptpuls + **Hi-Hat Chick** + Feathering |
| **800** | **Ride Cymbal (51)** [Skip-Stroke] | 70 | Schlag 2+ (Triolen-Achtel: $480 + 320$) |
| **960** | **Ride Cymbal (51)**, Kick (35) | 90, 30 | Schlag 3: Hauptpuls + Feathering |
| **1440** | **Ride Cymbal (51)**, **Pedal Hi-Hat (44)**, Kick (35) | 95, 85, 30 | Schlag 4: Hauptpuls + **Hi-Hat Chick** + Feathering |
| **1760** | **Ride Cymbal (51)** [Skip-Stroke] | 75 | Schlag 4+ (Triolen-Achtel: $1440 + 320$) |

---

## 5. PAT-017 – Bebop Medium-Up Comping Groove (2 Takte, Neuaufnahme)

- **ID:** `PAT-017`
- **Tempo:** 180 BPM | **Metrum:** 4/4
- **Charakteristik:** Schneller Swing mit aktiver linker Hand (Snare-Comping) gegen den stetigen Ride-/Hi-Hat-Puls.

### Tick-Tabelle (2 Takte, 480 PPQ, Skip-Stroke auf Tick $+320$):

**Takt 1:**
- **0:** Ride (51, Vel 95), Kick Feathering (35, Vel 25)
- **480:** Ride (51, Vel 100), Pedal HH (44, Vel 90), Kick (35, Vel 25)
- **800:** Ride (51, Vel 75)
- **960:** Ride (51, Vel 95), Kick (35, Vel 25)
- **1280:** **Snare Comping (38, Vel 85) [Synkope auf 3+]**
- **1440:** Ride (51, Vel 100), Pedal HH (44, Vel 90), Kick (35, Vel 25)
- **1760:** Ride (51, Vel 75)

**Takt 2:**
- **0:** Ride (51, Vel 95), Kick (35, Vel 25)
- **320:** **Snare Ghost (38, Vel 45) [Antizipation vor Schlag 2]**
- **480:** Ride (51, Vel 100), Pedal HH (44, Vel 90), Kick (35, Vel 25)
- **800:** Ride (51, Vel 75)
- **960:** Ride (51, Vel 95), Kick (35, Vel 25)
- **1440:** Ride (51, Vel 100), Pedal HH (44, Vel 90), **Snare Accent (38, Vel 105) + Kick Bomb (35, Vel 110) [Akzent auf 4!]**
- **1760:** Ride (51, Vel 75)
