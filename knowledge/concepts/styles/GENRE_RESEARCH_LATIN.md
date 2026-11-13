# STEPS – Lateinamerikanische Rhythmik & Bossa Nova Groove-Modelle (Phase 4.10)

**Dokumenttyp:** COMPREHENSIVE LATIN GENRE RESEARCH & GROOVE EXTENSION  
**Wissensdomänen:** M07 (Rhythmik/Metrum), M08 (Drums/Percussion), M09 (Genres), M10 (Klavierpraxis)  
**Kulturelle & Musikologische Evidenz:** Antonio Carlos Jobim, João Gilberto (*Chega de Saudade* 1958), Ed Thigpen (*The Rhythm Section*), Rebeca Mauleón (*The Salsa Guidebook*)  
**Standard:** 480 PPQ (Division = 480 Ticks/Viertel; 1 Takt 4/4 = 1920 Ticks), General MIDI Percussion Map (Kanal 10)  
**Status:** Forschungsmodelle. Die angegebenen Raster und Stufen sind nachrechenbar. Für Stil- und Werkzuschreibungen gelten die jeweils angegebenen Fundstellen.

---

## 1. M07 & M09: Die Clave als metrischer Gravitationsanker

Die Son-Clave ist das rhythmische Bezugsraster des folgenden afrokubanischen
Modells. Das Bossa-Nova-Beispiel in diesem Dokument ist ein eigenes
Begleitmodell.

### Die Son-Clave (3:2 und 2:3)

Die Son-Clave verteilt fünf Schläge auf zwei 4/4-Takte. Das folgende Raster
hat 16 Sechzehntelpositionen je Takt. In der 2:3-Richtung steht die 2er-Seite
zuerst.

- **3er-Takt (Tresillo-Hälfte):** Schläge auf **1**, **2+** (Tick 720) und **4** (Tick 1440).
- **2er-Takt:** Schläge auf **2** (Tick 480) und **3** (Tick 960).

```
3:2 Son Clave (480 PPQ, 2 Takte = 3840 Ticks):
Takt 1 (3er-Seite):  [X . . . . . X . . . . . X . . .] (Ticks 0, 720, 1440)
Takt 2 (2er-Seite):  [. . . . X . . . X . . . . . . .] 
  - Relativ zu Takt 2: Ticks 480, 960
  - Absolut auf Zeitachse: Ticks 2400 (1920+480), 2880 (1920+960)
```

### Bossa-Nova-Übungsmuster

Für dieses Cross-Stick-Modell bleibt die erste Hälfte des Son-Clave-Rasters
erhalten. In der zweiten Hälfte liegt der letzte Schlag eine Achtelnote später.

- **Takt 1 (3er-Seite):** Ticks 0 (Schlag 1), 720 (Schlag 2+), 1440 (Schlag 4).
- **Takt 2 (2er-Seite):**
  - Schlag 2: Tick 480 (relativ) / **Tick 2400** (absolut auf 2-Takt-Timeline: 1920 + 480)
  - Schlag 3+: Tick 1200 (relativ) / **Tick 3120** (absolut auf 2-Takt-Timeline: 1920 + 1200)!

---

## 2. M08 & M09: Drei neue kanonische Drum- & Percussion-Grooves (PAT-027 bis PAT-029)

### A. PAT-027: Bossa Nova Brush & Cross-Stick (128 BPM)
- **Tempo:** 128 BPM (als 4/4 oder 2/4 notiert) | **Metrum:** 4/4 Straight ($\rho = 1{,}0$) mit weichem humanized Micro-Drift ($\pm 4$ Ticks).
- **Instrumentierung (General MIDI Kanal 10):**
  - **Bass Drum (35/36):** Das brasilianische "Surdo"-Herzstück. Schlägt auf Zählzeit **1** (leise, Velocity 70) und Zählzeit **3** (betont, Velocity 105), jeweils vorbereitet durch einen leisen synkopierten Geisterschlag auf 2+ bzw. 4+ (punktierte Viertel-Figuren).
  - **Cross-Stick / Rimshot (37):** Spielt das zweitaktige **Bossa-Nova-Übungsmuster**:
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

### A. PROG-024 · Bossa-Nova-Übungsfolge mit Doppeldominante

- **Stufenfolge:** `I^maj7 - II^7 - ii^7 - V^7 - I^maj7`.
- **C-Dur:** Cmaj7 – D7 – Dm7 – G7 – Cmaj7. D7 hat die
  Akkordgestalt der Doppeldominante V7/V. Der nächste Akkord ist die
  zweite Stufe Dm7. Der Grundton D bleibt liegen, und F♯ sinkt zu F.
  V7/ii wäre hier A7.
- **F-Dur:** Fmaj7 – G7 – Gm7 – C7 – Fmaj7. Bei G7 → Gm7
  sinkt H zu B (internationale Schreibweise B → B♭).

Die Folge ist ein transponierbares Übungsschema. In Paulo Jobims Arrangement
von *Garota de Ipanema* steht in Takt 38–40 Gm7 – G♭7(9) – Fmaj7
(PDF-Seite 3). Das PDF nennt Paulo Jobim auf Seite 1. Der Katalogtext
zum Archivdatensatz beschreibt die Aufnahme mit Claus Ogerman.
[Partitur im Acervo Antônio Carlos Jobim](https://www.jobim.org/jobim/bitstream/handle/2010/10407/garota%20de%20ipanema.pdf)

---

### B. PROG-025 · Afro-Cuban Minor Ostinato Vamp

- **Stufenfolge:** `i - iv - V^7 - iv` als harmonische Schleife.
- **C-Moll:** Cm – Fm – G7 – Fm.
- **Klaviermodell:** Über der Akkordschleife kann ein synkopierter Montuno
  mit gebrochenen Oktaven und Terzen gespielt werden. Das Übungsmuster
  kann die 2:3 Son-Clave als rhythmischen Bezug verwenden.
