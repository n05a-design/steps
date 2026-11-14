# STEPS – Genre-Forschung: UK Garage & 2-Step Rhythmik (Phase 4.7)

**Dokumenttyp:** GENRE SPECIFICATION & RHYTHMIC ENGINE ANALYSIS  
**Wissensdomänen:** M07 (Rhythmik & Micro-Timing), M08 (Drums), M09 (Genres), M05/M06 (Harmonik & Bass)  
**Standard:** 480 PPQ (Division = 480 Ticks/Viertel; 1 Takt 4/4 = 1920 Ticks). General-MIDI Percussion Map (Kanal 10).  
**Epistemischer Status:** Analyse & Akustikregeln = `THEORY_SUPPORTED` / `EMPIRICALLY_SUPPORTED`; Patterns = `ILLUSTRATIVE_DESIGN`.

---

## 1. Die rhythmische Identität von 2-Step UK Garage

UK Garage (UKG) entstand Ende der 1990er-Jahre in London aus einer Fusion von US-Garage-House (Todd Edwards, Masters at Work), Drum & Bass und Dancehall.

### Die 3 Kernmerkmale des 2-Step:
1. **Der "zerbrochene" Kick-Puls (Das Auslassen von Schlag 2):**  
   Während normaler House starr auf allen vier Viertelschlägen pumpt (Four-on-the-Floor), entfernt 2-Step die Kick von Schlag 2, 3 und 4 und platziert stattdessen einen einzigen synkopierten Schlag auf der Zählzeit **3+** (bzw. kurz vor 4).
2. **Die 16tel-MPC-Swing-Quantisierung (55% bis 62%):**  
   Im Gegensatz zum ternären $\frac{12}{8}$-Jazz-Swing nutzt UK Garage einen geschwungenen **16tel-Shuffle** ($\rho_{16} \approx 1{,}25\text{ bis }1{,}40$). Jede zweite 16tel-Note wird um ca. 15–30 Ticks nach hinten verzögert.
3. **Der trockene Rimshot/Side-Stick:**  
   Anstelle einer breiten Pop-Snare dominiert ein ultrakompakter, hoch gestimmter Side-Stick (GM Note 37) oder Rimshot, oft gedoppelt mit einem zarten Finger-Snap oder Clap (GM Note 39).

---

## 2. Metrische Tabelle: Gerade vs. 58% Swung-Ticks (480 PPQ)

| 16tel-Position | Straight Tick | 58% Swung Tick ($\Delta \approx +24\text{ Ticks}$) | Musikalische Funktion |
|---|---|---|---|
| **1** | 0 | **0** | Starker Taktbeginn (Kick) |
| **1e** | 120 | **144** | Geschwungene Ghost-Hat / Shaker |
| **1+** | 240 | **240** | Offbeat Closed Hat |
| **1a** | 360 | **384** | Geschwungener Shuffle-Step |
| **2** | 480 | **480** | **Backbeat Side Stick / Clap (37/39)** |
| **2e** | 600 | **624** | Snare Ghost |
| **2+** | 720 | **720** | Offbeat Hat |
| **2a** | 840 | **864** | Shuffle-Step |
| **3** | 960 | **960** | *Kick schweigt komplett!* (Freier Raum) |
| **3e** | 1080 | **1104** | Ghost-Step |
| **3+** | 1200 | **1200** | **Synkopierte Kick (Der typische 2-Step Bounce!)** |
| **3a** | 1320 | **1344** | Push-Step vor dem Backbeat |
| **4** | 1440 | **480** | **Backbeat Side Stick / Clap (37/39)** |
| **4e** | 1560 | **1584** | Optionaler Skip-Kick |
| **4+** | 1680 | **1680** | Offbeat Open Hat (46) |
| **4a** | 1800 | **1824** | Letzter Swing-Schubs vor neuem Takt |

---

## 3. Bass- und Harmonie-Interaktion im UK Garage

### A. Der "Organ Bass" (Korg M1 Preset Organ 2)
- Kurzer, perkussiver, hölzerner Bass-Stab mit schnellem Decay.
- Spielt synkopierte Riffs auf den unbetonten 16tel-Schlägen, die sich exakt in die Lücken zwischen Kick und Snare verzahnen.

### B. Harmonik: Modalität & Jazz-Akkorde
- Typische Kadenzen: Moll-Loops mit Septimen und Nonen ($ii^9 - vi^7$ oder $i^7 - \flat VII^{\text{maj}7} - \flat VI^{\text{maj}7}$).
- Schnelle, staccatoartige Rhodes- oder Streicher-Stabs, die dem perkussiven Beat Glanz und Eleganz verleihen.

---

## 4. PAT-020: Authentic 2-Step UK Garage Groove (2 Takte, 134 BPM)

- **ID:** `PAT-020`
- **Tempo:** 134 BPM | **Metrum:** 4/4 | **Swing:** 58% ($\rho_{16} = 1{,}32$)
- **GM Map:** Kick (36), Side Stick (37), Hand Clap (39), Closed HH (42), Open HH (46).

### Exakte Tick-Tabelle (2 Takte, 480 PPQ):

**Takt 1:**
- **Tick 0 (1):** Kick (36, Vel 115)
- **Tick 144 (1e):** Closed HH (42, Vel 50) [Swung Ghost]
- **Tick 240 (1+):** Closed HH (42, Vel 80) [Offbeat]
- **Tick 384 (1a):** Closed HH (42, Vel 45) [Swung Ghost]
- **Tick 480 (2):** **Side Stick (37, Vel 110) + Clap (39, Vel 95)**
- **Tick 624 (2e):** Side Stick Ghost (37, Vel 35) [Micro-Roll]
- **Tick 720 (2+):** Closed HH (42, Vel 85)
- **Tick 864 (2a):** Closed HH (42, Vel 50)
- **Tick 960 (3):** Open HH (46, Vel 75) – *Kick & Snare schweigen vollkommen!*
- **Tick 1104 (3e):** Closed HH (42, Vel 45)
- **Tick 1200 (3+):** **Synkopierte Kick (36, Vel 115) [Der Bounce-Schlag!]**
- **Tick 1344 (3a):** Closed HH (42, Vel 55)
- **Tick 1440 (4):** **Side Stick (37, Vel 110) + Clap (39, Vel 95)**
- **Tick 1584 (4e):** Closed HH (42, Vel 45)
- **Tick 1680 (4+):** **Open HH (46, Vel 95) [Heller Akzent vor Taktgrenze]**
- **Tick 1824 (4a):** Closed HH (42, Vel 60)

**Takt 2:**
- Wie Takt 1, jedoch mit einem zusätzlichen **Skip-Kick** auf **Tick 1584 (4e)** (Kick 36, Vel 90), der den Groove kurz vor dem nächsten Takt anschiebt.
