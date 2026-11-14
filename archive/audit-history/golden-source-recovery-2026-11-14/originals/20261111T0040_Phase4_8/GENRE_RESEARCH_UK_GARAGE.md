# STEPS – Genre-Forschung: UK Garage & 2-Step Rhythmik (Phase 4.8)

**Dokumenttyp:** GENRE SPECIFICATION & RHYTHMIC ENGINE ANALYSIS  
**Wissensdomänen:** M07 (Rhythmik & Micro-Timing), M08 (Drums), M09 (Genres), M05/M06 (Harmonik & Bass)  
**Standard:** 480 PPQ (Division = 480 Ticks/Viertel; 1 Takt 4/4 = 1920 Ticks, 16tel = 120 Ticks). General-MIDI Percussion Map (Kanal 10).  
**Epistemischer Status:** Analyse & Akustikregeln = `THEORY_SUPPORTED` / `EMPIRICALLY_SUPPORTED`; Patterns = `ILLUSTRATIVE_DESIGN`.

---

## 1. Exakte mathematische Swing-Tabelle für UK Garage (480 PPQ)

*Korrektur ERR-024:* Zur Vermeidung von Definitionsvermischungen trennt STEPS strikt zwischen Swing-Prozentsatz, Tick-Position und resultierender mathematischer Ratio.

| Swing % ($P$) | Dauer 1. 16tel | Position 2. 16tel | Offset ($\Delta$) | Swing-Ratio ($\rho = \frac{t_1}{t_2}$) | Typischer Einsatzbereich |
|---|---|---|---|---|---|
| **50 %** | 120 Ticks | **Tick 120** | $0$ Ticks | **$1{,}00 : 1$** | Straight House / Techno |
| **55 %** | 132 Ticks | **Tick 132** | $+12$ Ticks | **$1{,}22 : 1$** | Milder Garage-House-Shuffle |
| **58 %** | 139,2 Ticks | **Tick 139** | **$+19$ Ticks** | **$1{,}38 : 1$** | **Authentischer 2-Step Standard (Sweet Spot)** |
| **60 %** | 144 Ticks | **Tick 144** | **$+24$ Ticks** | **$1{,}50 : 1$** | **Harter MPC-Swing / Spät-90er Garage** |
| **62 %** | 148,8 Ticks | **Tick 149** | $+29$ Ticks | **$1{,}63 : 1$** | Extremer Broken-Beat Shuffle |

---

## 2. 4-Taktige Variations-Architektur im 2-Step

Ein authentischer UKG-Groove darf niemals nur als starrer 1-Takt-Loop laufen.  
Er folgt einer **4-Takt-Spannungskurve**:
1. **Takt 1 (Foundation):** Standard 2-Step-Bounce. Kick auf 1 und 3+; Side-Stick auf 2 und 4.
2. **Takt 2 (Subtle Push):** Zusätzlicher Skip-Kick auf **4e** (Tick 1579 bei 58% Swing), der den nächsten Takt anstößt.
3. **Takt 3 (Air & Space):** Offene Hi-Hat auf Zählzeit 2+ wird akzentuiert; Kick auf 3+ wird minimal leiser gespielt (Vel 90).
4. **Takt 4 (Turnaround Fill):** Kick auf 3+ fällt weg! Stattdessen spielen Side-Stick und gegateter Tom-Roll einen synkopierten 16tel-Wirbel auf Zählzeit 3e+, 4, 4+ zur Taktüberleitung.

---

## 3. Neues kanonisches Pattern

### PAT-023: 4-Bar UKG Vocal-Chop Shuffle (134 BPM, 58% MPC Swing)
- **ID:** `PAT-023`
- **Tempo:** 134 BPM | **Metrum:** 4/4 | **Swing:** 58% ($P = 0{,}58 \implies \text{Offset } +19\text{ Ticks}$, 2. 16tel auf Tick 139).
- **Instrumente:** Kick (36), Side Stick (37), Hand Clap (39), Closed Hat (42), Open Hat (46), Shaker (70).

#### Tick-Tabelle Takt 1 (58% Swung-Grid):
- **Tick 0 (1):** Kick (36, Vel 115)
- **Tick 139 (1e):** Shaker (70, Vel 55) [Swung 16th]
- **Tick 240 (1+):** Closed Hat (42, Vel 85) [Offbeat 8th]
- **Tick 379 (1a):** Closed Hat Ghost (42, Vel 45) [Swung 16th]
- **Tick 480 (2):** **Side Stick (37, Vel 115) + Clap (39, Vel 90)**
- **Tick 619 (2e):** Side Stick Ghost (37, Vel 40)
- **Tick 720 (2+):** Closed Hat (42, Vel 85)
- **Tick 859 (2a):** Shaker (70, Vel 50)
- **Tick 960 (3):** Open Hat (46, Vel 80) – *Kick schweigt!*
- **Tick 1099 (3e):** Closed Hat (42, Vel 45)
- **Tick 1200 (3+):** **Synkopierte Kick (36, Vel 120) [Der 2-Step Bounce!]**
- **Tick 1339 (3a):** Shaker (70, Vel 55)
- **Tick 1440 (4):** **Side Stick (37, Vel 115) + Clap (39, Vel 90)**
- **Tick 1680 (4+):** **Open Hat (46, Vel 95) [Akzent vor Taktwechsel]**
- **Tick 1819 (4a):** Closed Hat (42, Vel 60)
