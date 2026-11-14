# STEPS – Lateinamerikanische Rhythmik & Bossa Nova Groove-Modelle (Phase 4.10)

**Dokumenttyp:** COMPREHENSIVE LATIN GENRE RESEARCH & GROOVE EXTENSION  
**Wissensdomänen:** M07 (Rhythmik/Metrum), M08 (Drums/Percussion), M09 (Genres), M10 (Klavierpraxis)  
**Kulturelle & Musikologische Evidenz:** Antonio Carlos Jobim, João Gilberto (*Chega de Saudade* 1958), Ed Thigpen (*The Rhythm Section*), Rebeca Mauleón (*The Salsa Guidebook*)  
**Standard:** 480 PPQ (Division = 480 Ticks/Viertel; 1 Takt 4/4 = 1920 Ticks), General MIDI Percussion Map (Kanal 10)  
**Status:** `EMPIRICALLY_SUPPORTED` · `FORMAL_VERIFIED`

---

## 1. M07 & M09: Die Clave als metrischer Gravitationsanker

In der afro-kubanischen und brasilianischen Musiktheorie ist der Rhythmus nicht durch einen statischen europäischen Backbeat (Schlag 2 und 4) definiert, sondern durch eine asymmetrische, zweitaktige rhythmische Leitachse: die **Clave**.

### Die Son Clave (3:2 vs. 2:3 Richtung):
Die Son Clave besteht aus 5 Schlägen verteilt auf 2 Takte (8 Achtelnoten je Takt = 16 Achtelnoten Gesamtlänge):
- **3er-Takt (Tresillo-Hälfte):** Schläge auf **1**, **2+** (Tick 720) und **4** (Tick 1440).
- **2er-Takt:** Schläge auf **2** (Tick 480) und **3** (Tick 960).

```
3:2 Son Clave (480 PPQ):
Takt 1 (3er-Seite):  [X . . . . . X . . . . . X . . .] (Ticks 0, 720, 1440)
Takt 2 (2er-Seite):  [. . . . X . . . X . . . . . . .] (Ticks 480, 960)
```

### Der Bossa Nova Clave-Puls (Brasilianische Modifikation):
In Rio de Janeiro modifizierten Musiker wie João Gilberto und Vinicius de Moraes die Clave: Der letzte Schlag der 2er-Seite wird um ein Sechzehntel/Achtel nach hinten verzögert, wodurch das charakteristische sanft-schwebende brasilianische Lebensgefühl entsteht:
- **Takt 1 (3er-Seite):** Ticks 0 (1), 720 (2+), 1440 (4).
- **Takt 2 (2er-Seite):** Ticks 480 (2) und **1200 (3+)**!

---

## 2. M08 & M09: Drei neue kanonische Drum- & Percussion-Grooves (PAT-027 bis PAT-029)

### A. PAT-027: Bossa Nova Authentic Brush & Cross-Stick (128 BPM)
- **Tempo:** 128 BPM (als 4/4 oder 2/4 notiert) | **Metrum:** 4/4 Straight ($\rho = 1{,}0$) mit weichem humanized Micro-Drift ($\pm 4$ Ticks).
- **Instrumentierung (General MIDI Kanal 10):**
  - **Bass Drum (35/36):** Das brasilianische "Surdo"-Herzstück. Schlägt auf Zählzeit **1** (leise, Velocity 70) und Zählzeit **3** (betont, Velocity 105), jeweils vorbereitet durch einen leisen synkopierten Geisterschlag auf 2+ bzw. 4+ (punktierte Viertel-Figuren).
  - **Cross-Stick / Rimshot (37):** Spielt stoisch das 2-taktige brasilianische **Bossa-Nova-Clave-Muster**:
    - Takt 1: Ticks 0 (1), 720 (2+), 1440 (4).
    - Takt 2: Ticks 480 (2), 1200 (3+).
  - **Closed Hi-Hat / Shaker (42):** Durchgehende, sanfte Sechzehntelketten mit feiner Akzentuierung der Aufschläge, die das Schwingen von Sand in einem brasilianischen *Ganzá* nachbilden.

---

### B. PAT-028: Afro-Cuban Cha-Cha-Chá (116 BPM)
- **Tempo:** 116 BPM | **Metrum:** 4/4.
- **Instrumentierung:**
  - **Cowbell / Campana (56):** Fester Puls auf den Viertelschlägen 1, 2, 3, 4.
  - **Congas (62 Mute High, 63 Open High, 64 Low Conga):**
    - Schläge 1, 2 und 3 werden durch gedämpfte Hand- und Fersen-Techniken vorbereitet.
    - Auf Zählzeit **4 und 4+** (Ticks 1440 und 1680) schlagen zwei offene, warme Töne auf der High Conga (der namensgebende "Cha-Cha"-Schritt!).
  - **Guiro (73/74):** Langer Zug auf 1, zwei kurze Striche auf 2 und 2+.

---

### C. PAT-029: Samba Batucada Sectional (105 BPM 2/2 bzw. 210 BPM 4/4)
- **Tempo:** 105 BPM (Alla Breve) | **Metrum:** 2/2.
- **Charakteristik:**
  - Explosives Zusammenspiel von Surdo (tiefes Fundament), Caixa (Snare-Ghost-Rolls), Tamborim (synkopierte 16tel-Akzente) und Agogô-Glocken (zweitönige Melodiefiguren).

---

## 3. M05 & M06: Zwei neue kanonische Progressions-Archetypen (PROG-024 & PROG-025)

### A. PROG-024: Bossa Nova Girl-from-Ipanema Descent
- **Stufenfolge:** `I^maj7 - II^7 - ii^7 - V^7 - I^maj7`
- **Beispiel in F-Dur (Jobim-Standard):**
  $$F^{\text{maj}7} \;\longrightarrow\; G^7 \;\longrightarrow\; Gm^7 \;\longrightarrow\; C^7 \;\longrightarrow\; F^{\text{maj}7}$$
- **Harmonisches Phänomen:**
  Die Stufe $II^7$ ($G^7$) ist eine unaufgelöste Doppeldominante ($V^7/V$), die überraschend nicht direkt nach $C^7$ stürzt, sondern sanft in die Moll-Subdominante $Gm^7$ hineingleitet!
- **Voice Leading am Klavier:**
  Der Ton $B\natural$ (Terz von $G^7$) gleitet chromatisch um einen Halbton nach unten zum Ton $B\flat$ (Mollterz von $Gm^7$).

---

### B. PROG-025: Afro-Cuban Montuno Cadence
- **Stufenfolge:** `i - iv - V^7 - iv` (bzw. `I - IV - V - IV`)
- **Beispiel in C-Moll:**
  $$Cm \;\longrightarrow\; Fm \;\longrightarrow\; G^7 \;\longrightarrow\; Fm$$
- **Synkopierter Piano-Montuno:**
  Das Klavier spielt keine starren Akkorde, sondern synkopierte, perkussive Oktav- und Terzenbrechungen exakt synchron mit der 2:3 Son Clave.
