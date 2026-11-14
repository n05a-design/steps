# STEPS – Integrierte Musikalische Fallstudien (Phase 4.8)

**Dokumenttyp:** COMPREHENSIVE MULTI-TRACK ARRANGEMENT CASE STUDIES  
**Wissensdomänen:** M01–M12 (Vollständige Integration von Harmonik, Rhythmik, Basslinie, Klaviervoicings und Metrik)  
**Standard:** 480 PPQ (Division = 480 Ticks/Viertel; 1 Takt 4/4 = 1920 Ticks). SPN-Tonhöhen (C4 = MIDI 60); deutsches H = int. B explizit.  
**Epistemischer Status:** `ILLUSTRATIVE_DESIGN` (eigenständige, didaktisch geschlossene Kompositionsmodelle für STEPS-Lernende und Algorithmen).  
**Korrekturbezug:** Behebt `ERR-025` (Strikte Einstufung von "Horizon Drift" als D-Aeolisch; Entfernung unpassender dorischer Referenzen).

---

## 1. Fallstudie 1: Neo-Soul / Jazz-Hop ("Midnight Solace")

### A. Musikalische Rahmenparameter
- **Taktart:** 4/4 | **Tempo:** 86 BPM (entspanntes, laid-back Neo-Soul Feeling).
- **Tonales Zentrum:** $C$-Dur mit modalem Entleihen (Modal Interchange) aus $C$-Aeolisch (paralleles Moll).
- **Akkordprogression (4 Takte):**
  $$\underbrace{Fm^7}_{\text{iv}^7} \;\longrightarrow\; \underbrace{B\flat^7}_{\flat\text{VII}^7} \;\longrightarrow\; \underbrace{C^{\text{maj}7}}_{\text{I}^{\text{maj}7}} \;\longrightarrow\; \underbrace{A\flat^{\text{maj}7}}_{\flat\text{VI}^{\text{maj}7}}$$
  *Harmonische Logik:*
  Die ersten drei Takte bilden die kanonische **Jazz-Backdoor-Kadenz (`PROG-017`)**. Anstelle der dominanten Diatonik ($G^7 \to C$) nähert sich die Progression der Tonika subdominantisch über die Moll-Subdominante $Fm^7$ und den chromatischen Backdoor-Dominantakkord $B\flat^7$. Die Auflösung in die Tonika $C^{\text{maj}7}$ wird durch die Halbton-Gleitbewegung der Guide Tones getragen ($A\flat \to G$, $D \to C$ bzw. $E$).
  In Takt 4 wird anstelle einer einfachen Tonika-Verlängerung der chromatische Borrowed Chord **$\flat\text{VI}^{\text{maj}7}$ ($A\flat^{\text{maj}7}$)** eingeschoben. Über den gemeinsamen Ton $C$ (Tonika-Grundton = Terz von $A\flat^{\text{maj}7}$) und die sanfte chromatische Rückführung ($A\flat \to F$) wird ein nahtloser 4-Takt-Loop geschlossen!

---

### B. Klavier-Arrangement (Drop-2 & Shell-Voicings)

| Takt | Akkord | Linke Hand (Fundament & Tenor) | Rechte Hand (Oberstimmen / Guide Tones) | Stimmführung ($L_1$-Distanz RH) |
|---|---|---|---|---|
| **1** | **$Fm^7$** | `F2` (41) $+$ `C3` (48) [Quinte] | `E\flat 4` (63) $+$ `A\flat 4` (68) [Quarte] | Ausgangslage |
| **2** | **$B\flat^7$** | `B\flat 2` (46) $+$ `F3` (53) [Quinte] | `D4` (62) $+$ `A\flat 4` (68) [Tritonus] | **1 Halbton** ($E\flat 4 \to D4$, $A\flat 4$ liegt!) |
| **3** | **$C^{\text{maj}7}$** | `C3` (48) $+$ `G3` (55) [Quinte] | `E4` (64) $+$ `B4` (dt. `H4`, 71) [Quinte] | 5 Halbtöne ($D4 \to E4$, $A\flat 4 \to B4$) |
| **4** | **$A\flat^{\text{maj}7}$** | `A\flat 2` (44) $+$ `E\flat 3` (51) [Quinte] | `G4` (67) $+$ `C5` (72) [Quarte] | 4 Halbtöne ($E4 \to G4$, $B4 \to C5$) |

*Didaktische Ergonomie:*
- Die linke Hand spielt stabile, offene Quinten im klanglich sauberen Bereich zwischen $A\flat 2$ und $G3$ (weit oberhalb der kritischen Tiefen-Intervall-Grenze / Low Interval Limit, LIL).
- Die rechte Hand vermeidet dichte Akkordblöcke und führt die Guide Tones (Terz und Septime) in ergonomischer Mittellage.
- *Voice-Leading-Qualität:* Der Übergang von Takt 1 zu Takt 2 erfordert lediglich die minimale Verschiebung eines einzelnen Fingers um einen Halbton ($E\flat 4 \to D4$), während der Ton $A\flat 4$ als Liegestimme gehalten wird.

---

### C. Basslinie (Electric Fingerstyle Bass)
Der E-Bass übernimmt die harmonische Verankerung und erzeugt durch chromatische Übergangsnoten (Passing Tones) eine fließende Kontrapunktik:
- **Takt 1 ($Fm^7$):**
  - Tick 0 (1): $F1$ (MIDI 29, Velocity 110, Grundton).
  - Tick 720 (2+): $F2$ (MIDI 41, Velocity 85, Oktav-Sprung).
  - Tick 1200 (3+): $A\flat 1$ (MIDI 32, Velocity 95, Mollterz).
  - Tick 1680 (4+): $A1$ (MIDI 33, Velocity 90, chromatische Durchgangsnote aufwärts nach $B\flat 1$).
- **Takt 2 ($B\flat^7$):**
  - Tick 0 (1): $B\flat 1$ (MIDI 34, Velocity 112, Grundton).
  - Tick 720 (2+): $F2$ (MIDI 41, Velocity 82, Quinte).
  - Tick 1440 (4): $B1$ (dt. $H1$, MIDI 35, Velocity 96, chromatische Annäherung von unten an $C2$).
- **Takt 3 ($C^{\text{maj}7}$):**
  - Tick 0 (1): $C2$ (MIDI 36, Velocity 115, Tonika-Ankunft).
  - Tick 720 (2+): $G1$ (MIDI 31, Velocity 80, fallende Quinte).
  - Tick 1200 (3+): $E2$ (MIDI 40, Velocity 88, Durterz).
  - Tick 1680 (4+): $E\flat 2$ (MIDI 39, Velocity 92, chromatisch abwärtsgleitend nach $D2$ bzw. antizipierend $A\flat 1$).
- **Takt 4 ($A\flat^{\text{maj}7}$):**
  - Tick 0 (1): $A\flat 1$ (MIDI 32, Velocity 110, Grundton).
  - Tick 720 (2+): $E\flat 2$ (MIDI 39, Velocity 85, Quinte).
  - Tick 1440 (4): $G1$ (MIDI 31, Velocity 88, große Septime).
  - Tick 1680 (4+): $G\flat 1$ (MIDI 30, Velocity 94, Leitton abwärts zur Zielnote $F1$ von Takt 1).

---

### D. Drum-Groove (Swung Funk/Soul `PAT-013` Variante)
- **Tempo:** 86 BPM | **Swing-Faktor:** MPC 58% auf den 16teln (zweites 16tel verzögert auf Tick 139 bei 480 PPQ).
- **Instrumentierung (General MIDI Kanal 10):**
  - Kick Drum: MIDI Note 36 (Acoustic Bass Drum)
  - Snare Drum: MIDI Note 38 (Acoustic Snare)
  - Side Stick: MIDI Note 37 (Cross-Stick)
  - Closed Hi-Hat: MIDI Note 42
  - Open Hi-Hat: MIDI Note 46
- **Rhythmisches Gerüst:**
  - Kick landet synchron mit dem Bass auf Zählzeit 1 (Tick 0) und auf der vorgezogenen Synkope 3+ (Tick 1200).
  - Snare schlägt den soliden Backbeat auf Zählzeit 2 (Tick 480) und Zählzeit 4 (Tick 1440).
  - Zwischen den Hauptschlägen füllen leise Ghost Notes (Velocity 28–42) auf Ticks 379 und 859 die Zwischenräume.
  - Das leicht geschleppte Hi-Hat-Muster (Laid-Back um +10 Ticks auf den Offbeats) erzeugt den typischen J-Dilla / Neo-Soul Groove.

---

## 2. Fallstudie 2: Liquid Drum & Bass 8-Bar Arrangement ("Horizon Drift")

### A. Musikalische Rahmenparameter
- **Taktart:** 4/4 | **Tempo:** 174 BPM.
- **Tonales Zentrum & Modale Klassifikation:**
  - **Rein $D$-Aeolisch (Natürliches Moll / Aeolian Mode).**
  - *Tonvorrat:* $\{D, E, F, G, A, B\flat, C\}$ (identisch mit dem Tonvorrat von $F$-Dur).
  - *Fachliche Abgrenzung (Korrektur ERR-025):*
    Diese Progression ist **kein D-Dorisch**. Dorisch verlangt zwingend die große Sexte $B\natural$ (dt. $H$). Im Akkordschema liegt jedoch mit $B\flat^{\text{maj}7}$ und $Gm^7$ ($G - B\flat - D - F$) durchgehend die kleine Sexte $B\flat$ vor. Das Stück bewegt sich somit in der reinen, wehmütig-schwebenden Aeolischen Klangsphäre.
- **Akkordprogression (4 Takte, im 8-Takt-Arrangement zweifach mit Klangvariation gespielt):**
  $$\underbrace{Dm^9}_{\text{i}^9} \;\longrightarrow\; \underbrace{B\flat^{\text{maj}7}}_{\flat\text{VI}^{\text{maj}7}} \;\longrightarrow\; \underbrace{Gm^7}_{\text{iv}^7} \;\longrightarrow\; \underbrace{C^{\text{add}9}}_{\flat\text{VII}^{\text{add}9}}$$
  *Harmonische Analyse:*
  1. $Dm^9$ ($\text{i}^9$): Tonika mit schwebender None $E5$.
  2. $B\flat^{\text{maj}7}$ ($\flat\text{VI}^{\text{maj}7}$): Weicher Subdominant-Gegenpol mit großer Septime $A4$.
  3. $Gm^7$ ($\text{iv}^7$): Echte Moll-Subdominante, stabilisiert den Mollcharakter.
  4. $C^{\text{add}9}$ ($\flat\text{VII}^{\text{add}9}$): Subtonika (Ganzton unter der Tonika); bringt durch die None $D5$ den Leitton zur Tonika $D$ als Akkordbestandteil mit, ohne scharfe Dominantspannung aufzubauen.

---

### B. Fender Rhodes / Piano-Akkorde (Syncopated Upbeat Stabs)
Im Liquid Drum & Bass werden Akkorde bei 174 BPM selten als schwere Ganztaktakkorde ausgehalten, da sie sonst den dichten Rhythmusfluss ersticken. Stattdessen werden federnde, synkopierte Offbeat-Stabs gespielt:

| Takt | Akkord | Anschlagzeitpunkte (Ticks bei 480 PPQ) | Voicing Rechte Hand | Klangliche Wirkung |
|---|---|---|---|---|
| **1** | **$Dm^9$** | Tick 240 (1+) & Tick 1200 (3+) | `F4` (65) – `A4` (69) – `C5` (72) – `E5` (76) | Reiner $F$-Dur-Dreiklang über Bass $D$ = satter $Dm^9$-Klang. |
| **2** | **$B\flat^{\text{maj}7}$** | Tick 240 (1+) & Tick 1200 (3+) | `F4` (65) – `A4` (69) – `D5` (74) | Transparenter Quart-Sext-Auszug; weiche Fläche. |
| **3** | **$Gm^7$** | Tick 240 (1+) & Tick 1200 (3+) | `F4` (65) – `B\flat 4` (70) – `D5` (74) | Nur 1 Ton ändert sich ($A4 \to B\flat 4$); minimale Stimmführungsbewegung. |
| **4** | **$C^{\text{add}9}$** | Tick 240 (1+) & **Tick 1080 (3e Antizipation!)** | `E4` (64) – `G4` (67) – `D5` (74) | Vorzeitige Synkope auf 3e erzeugt Vorwärtsdrang zur Wiederholung. |

*In Takten 5–8 (Variation):*
Die Rhodes-Stabs werden im Release verlängert (Stereo Ping-Pong Delay mit punktierten Achteln) und erhalten in Takt 8 ein aufsteigendes Arpeggio über die Töne $C5 - D5 - E5 - G5$.

---

### C. Reese Sub-Bass & Metrische Dualität (87 BPM Halftime Phrasierung)
Das Fundament beruht auf der **metrischen Dualität**:
Während das Schlagzeug mit 174 BPM rasante kinetische Mikro-Energie erzeugt, schwingt der Bass im beruhigenden Halftime-Puls von 87 BPM.

- **Klangsynthese:**
  - Dual Sawtooth Oszillatoren mit feinem Detuning ($\pm 8$ Cents) für die schwebende "Reese"-Textur.
  - Tiefpassfilter (24 dB/Okt.) moduliert mit langsamer LFO-Sinusschwingung (1/2 Note synchronisiert).
  - Separater reiner Sub-Sinus-Oszillator für das unerschütterliche Tiefton-Fundament (unter 60 Hz).
- **Bassnoten & Frequenzen:**
  - **Takt 1 ($Dm^9$):** $D1$ (MIDI 26, Frequenz $\approx 36{,}71\text{ Hz}$), Ganztaktnote mit leisem Legato-Portamento.
  - **Takt 2 ($B\flat^{\text{maj}7}$):** $B\flat 0$ (MIDI 22, Frequenz $\approx 29{,}14\text{ Hz}$), tiefes Sub-Bass-Wummern.
  - **Takt 3 ($Gm^7$):** $G1$ (MIDI 31, Frequenz $\approx 48{,}99\text{ Hz}$), warmer, drückender Grundton.
  - **Takt 4 ($C^{\text{add}9}$):** $C1$ (MIDI 24, Frequenz $\approx 32{,}70\text{ Hz}$), gleitet auf Zählzeit 4+ (Tick 1680) aufwärts über $C\sharp 1$ zurück nach $D1$.

---

### D. Schlagzeug-Spur (`PAT-018` Liquid Drum & Bass Break)
- **Tempo:** 174 BPM | **Micro-Timing:** Straight ($\rho = 1{,}0$) mit subtilem Humanize-Jitter ($\pm 3$ Ticks).
- **Event-Struktur bei 480 PPQ:**
  - **Kick 1:** Tick 0 (Zählzeit 1, Velocity 122).
  - **Snare 1:** Tick 480 (Zählzeit 2, Velocity 118, knackiger Center-Hit).
  - **Kick 2 (Two-Step Push):** Tick 1200 (Zählzeit 3+, Velocity 114) $\implies$ Der Raum auf Schlag 3 bleibt frei!
  - **Snare 2:** Tick 1440 (Zählzeit 4, Velocity 120).
  - **Ghost Snares:** Ticks 720 (Velocity 42), 1080 (Velocity 35), 1680 (Velocity 50).
  - **Ride Cymbal 1 (GM 51):** Durchgehende 8tel-Noten (Ticks 0, 240, 480, 720, 960, 1200, 1440, 1680) mit wechselnder Velocity (90 / 65) für den schimmernden Höhenteppich.

---

## 3. Didaktische Zusammenfassung & Cross-Domain Synthese

| Dimension | Fallstudie 1: Midnight Solace | Fallstudie 2: Horizon Drift |
|---|---|---|
| **Genre** | Neo-Soul / Jazz-Hop | Liquid Drum & Bass |
| **Tempo / Puls** | 86 BPM (entspanntes Laid-Back) | 174 BPM Drums vs. 87 BPM Halftime Bass |
| **Tonales System** | C-Dur mit Modal Interchange (C-Aeolisch) | Rein D-Aeolisch (Natürliches Moll) |
| **Akkord-Identität** | `PROG-017` Backdoor Kadenz $+$ $\flat\text{VI}^{\text{maj}7}$ | Aeolischer Moll-Zyklus ($i^9 - \flat VI^{\text{maj}7} - iv^7 - \flat VII^{\text{add}9}$) |
| **Groove-Identität** | `PAT-013` Swung Funk (58% MPC-Swing, Tick 139) | `PAT-018` Two-Step Liquid Break |
| **Klavier-Spieltechnik** | Shell-Voicings & Drop-2; linke Hand reine Quinten | Syncopated Offbeat Stabs (1+ & 3+); weite Oberstimmen |
| **Bass-Konzeption** | Bewegte Fingerstyle-Basslinie mit Chromatik | Breiter Reese-Subbass mit LFO-Filterung |
| **Didaktischer Kern** | Minimal Voice Leading ($L_1 = 1$); Akkorde atmen lassen | Metrische Schichtung; Transparenz trotz 174 BPM |
