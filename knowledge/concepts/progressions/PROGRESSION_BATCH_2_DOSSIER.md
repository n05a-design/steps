# STEPS – Fachdossier Progressions-Archetypen Gruppe 2 (PROG-002, PROG-004, PROG-005, PROG-012)

> Dieses Fachdossier vertieft die musikwissenschaftliche, harmonische und stufentheoretische Modellierung der zweiten Gruppe zentraler Progressions-Archetypen des [Kanonischen Progressions-Atlas](CHORD_PROGRESSION_REFERENCE_LIBRARY.md).

**Dokumenttyp:** HARMONIETHEORETISCHES VERTIEFUNGSDOSSIER  
**Wissensdomänen:** M04 (Akkordtheorie), M05 (Harmonielehre), M06 (Voice Leading), M09 (Genre-Atlas)  
**Notationsstandard:** SPN (C4 = MIDI 60); internationales B♭ entspricht deutschem B, internationales B entspricht deutschem H.

---

## 1. Übersicht der Gruppe 2

| ID | Name / Archetyp | Stufen (Standardtonart) | Akkordfolge | Harmonischer Motor & Familie | Primäre Fachquellen |
|---|---|---|---|---|---|
| `PROG-002` | Emotional Minor Loop | `vi - IV - I - V` (in C) / `i - bVI - bIII - bVII` (in Am) | `Am - F - C - G` | Axis Minor Rotation / Tonale Ambiguität | Tagg (2014), Richards (2017) |
| `PROG-004` | 50s Doo-Wop Loop | `I - vi - IV - V` (in C) | `C - Am - F - G` | Authentischer Turnaround-Loop (T-Tp-S-D) | Aldwell/Schachter (1989), Kostka/Payne (2013) |
| `PROG-005` | Andalusische Kadenz | `i - bVII - bVI - V` (in Am) | `Am - G - F - E` | Absteigendes Tetrachord / Phrygischer Halbschluss | Gauldin (2004) |
| `PROG-012` | Descending Circle of Fifths | `vi - ii - V - I` (in C) | `Am - Dm - G - C` | Diatonische Quintfallsequenz (*Basse fondamentale*) | Rameau (1722), Salzer (1952) |

---

## 2. Detaillierte Fachanalyse je Archetyp

### 2.1 PROG-002 – Emotional Minor Loop

* **Stufengang:**
  * In Dur-Interpretation (C-Dur): $\text{vi} - \text{IV} - \text{I} - \text{V}$ ($\text{Tp} - \text{S} - \text{T} - \text{D}$)
  * In Moll-Interpretation (a-Moll Naturmoll): $\text{i} - \flat\text{VI} - \flat\text{III} - \flat\text{VII}$ ($\text{t} - \text{sP} - \text{tP} - \text{dP}$)
* **Klanggestalt & Voicing (in C/Am):**
  * $\text{Am}$ (MIDI `[57, 60, 64]` / $A - C - E$)
  * $\text{F}$ (MIDI `[53, 57, 60, 65]` / $F - A - C$)
  * $\text{C}$ (MIDI `[48, 52, 55, 60]` / $C - E - G$)
  * $\text{G}$ (MIDI `[55, 59, 62]` / $G - H - D$)
* **Tonale Ambiguität (Richards 2017 / Tagg 2014):**
  * Die Folge ist eine zyklische Rotation der 4-Chord-Pop-Achse (`PROG-001`, Rotations-Offset 2).
  * Durch den Beginn auf $\text{Am}$ entsteht eine starke moll-orientierte Hörerwartung (Tagg 2014: *Melodic EDM / Emotional Ballad*).
  * Da auf $\text{G}$ ($\flat\text{VII}$ bzgl. Am) kein Leitton $G\sharp$ folgt, bleibt die Tonika C-Dur vs. a-Moll offen; melodische Phrasierung und hypermetrische Schwerpunktbildung bestimmen die wahrgenommene Tonika.
* **Stimmführungseigenschaften:**
  * Der Basston $C$ ist als Bindeton (Common Tone) über die ersten drei Akkorde ($\text{Am} \to \text{F} \to \text{C}$) stabilisierbar.
  * Der Schritt von $\text{G}$ zurück nach $\text{Am}$ vollzieht einen Ganztonschritt im Bass ($G \to A$) und Halbtonschritte in den Oberstimmen ($H \to C$).

---

### 2.2 PROG-004 – 50s Doo-Wop Loop

* **Stufengang (in C-Dur):**
  * $\text{I} - \text{vi} - \text{IV} - \text{V}$
  * Funktionale Syntax: Tonika $\to$ Tonikaparallele (Submediante) $\to$ Subdominante (Prädominante) $\to$ Dominante (Halbschluss)
* **Klanggestalt & Voicing (in C):**
  * $\text{C}$ (MIDI `[60, 64, 67]` / $C - E - G$)
  * $\text{Am}$ (MIDI `[57, 60, 64]` / $A - C - E$)
  * $\text{F}$ (MIDI `[53, 57, 60, 65]` / $F - A - C$)
  * $\text{G}$ (MIDI `[55, 59, 62]` / $G - H - D$)
* **Harmonischer Motor (Aldwell/Schachter 1989):**
  * **Tonika-Prolongation:** Die Bewegung $\text{I} \to \text{vi}$ ($C \to Am$) dehnt das Tonikafeld über die Terzverbindung terzabwärts aus.
  * **Prädominant-Vorbereitung:** $\text{IV}$ ($F$) etabliert die Vorbereitung auf die Dominante $\text{V}$ ($G$).
  * **Turnaround-Syntax:** Der Halbschluss auf $\text{V}$ drängt zur Auflösung zurück auf $\text{I}$ im Loop.
* **Didaktische und stilistische Bedeutung:**
  * Archetyp des 1950er Doo-Wop, frühen Rhythm & Blues und der Soul-Ballade.
  * Oft mit Triolen-Arpeggien (*12/8 Feel*) in Klavier und Gitarre realisiert.

---

### 2.3 PROG-005 – Andalusische Kadenz

* **Stufengang (in a-Moll):**
  * $\text{i} - \flat\text{VII} - \flat\text{VI} - \text{V}$
  * Modale Notation: $\text{Am} - \text{G} - \text{F} - \text{E}$
* **Klanggestalt & Voicing (in Am):**
  * $\text{Am}$ (MIDI `[57, 60, 64]` / $A - C - E$)
  * $\text{G}$ (MIDI `[55, 59, 62]` / $G - H - D$)
  * $\text{F}$ (MIDI `[53, 57, 60, 65]` / $F - A - C$)
  * $\text{E}$ (MIDI `[52, 56, 59, 64]` / $E - G\sharp - H$)
* **Das absteigende Tetrachord (Gauldin 2004):**
  * Der Bass vollzieht den klassischen Lamento-Bassgang $A \to G \to F \to E$ (Skalenstufen $1 \to \flat 7 \to \flat 6 \to 5$).
  * Schrittabfolge im Bass: Ganzton $\to$ Ganzton $\to$ Halbton ($2 - 2 - 1$ Halbtöne abwärts).
* **Der Phrygische Halbschluss & Chromatik:**
  * Die Bewegung $\flat\text{VI} \to \text{V}$ ($F \to E$) ist der kennzeichnende phrygische Halbtonschritt im Bass.
  * Während $\flat\text{VII}$ ($G$-Dur) das diatonische Naturmoll-Element darstellt, führt der Zielakkord $\text{E}$-Dur die harmonische Dur-Dominante mit dem chromatischen Leitton $G\sharp$ ein ($G \to G\sharp$ Chromatik).
  * Dies verknüpft traditionellen Flamenco (*Cadencia andaluza* im phrygischen Modus) mit klassischer barocker Lamento-Dramaturgie.

---

### 2.4 PROG-012 – Descending Circle of Fifths (Diatonische Quintfallsequenz)

* **Stufengang (in C-Dur):**
  * $\text{vi} - \text{ii} - \text{V} - \text{I}$
  * Stufenakkorde: $\text{Am} - \text{Dm} - \text{G} - \text{C}$
* **Klanggestalt & Voicing (in C):**
  * $\text{Am}$ (MIDI `[57, 60, 64]` / $A - C - E$)
  * $\text{Dm}$ (MIDI `[50, 53, 57, 62]` / $D - F - A$)
  * $\text{G}$ (MIDI `[55, 59, 62]` / $G - H - D$)
  * $\text{C}$ (MIDI `[48, 52, 55, 60]` / $C - E - G$)
* **Der harmonische Motor (Rameau 1722 / Salzer 1952):**
  * **Quintfallkette:** Jeder Akkordgrundton springt eine diatonische Quinte abwärts (bzw. eine Quarte aufwärts):
    $$A \xrightarrow{-7 / +5} D \xrightarrow{-7 / +5} G \xrightarrow{-7 / +5} C$$
  * Rameau begründete mit dieser Sequenz 1722 die Theorie der *Basse fondamentale*.
  * In der Schenkerianischen Analyse (Salzer 1952) fungiert die Kette als lineare Auskomponierung des Weges von der Tonikaparallele $\text{vi}$ über die Zwischenstufen $\text{ii}$ und $\text{V}$ zurück zur stabilen Tonika $\text{I}$.
* **Stimmführung & Erweiterungen:**
  * In vierstimmigen Sätzen führen alternierende Terzen und Septimen zu minimalen Stimmbewegungen (z. B. bei Septakkorden $\text{Am}^7 \to \text{Dm}^7 \to \text{G}^7 \to \text{C}^{\text{maj}7}$, wo jeweils die Septime zur Terz des Folgeakkords um einen Halb- oder Ganzton absinkt).

---

## 3. Implementierungsnachweis in STEPS

Die theoretischen Eigenschaften dieser Archetypen sind im STEPS-System verankert:

1. **Kanonische Registry:** Alle vier Archetypen sind unter `PROG-002`, `PROG-004`, `PROG-005` und `PROG-012` in `CANONICAL_PROGRESSIONS` (`src/steps/progression/engine.py`) hinterlegt.
2. **Theorie-Profile:** `ARCHETYPE_THEORY_METADATA` kapselt Familie, funktionale Syntax, tonale Ambiguitäten und Stimmführungsmerkmale.
3. **Muster-Erkennung (`detect_progression_archetypes`):** Erkennung beliebiger Akkordfolgen, automatisierte Identifikation von Rotationen (z. B. $\text{Am} - \text{F} - \text{C} - \text{G}$ als eigenständiges $\text{PROG-002}$ und Rotation von $\text{PROG-001}$) sowie transponierter Instanzen.
4. **Interaktive Vorschlags-Engine (`ProgressionSession`):**
   * Andalusische Kadenz ($\flat\text{VI} \to \text{V}$ in Moll).
   * 50s Doo-Wop Kadenz ($\text{vi} \to \text{IV} \to \text{V} \to \text{I}$).
   * Quintfall-Fortschreitungen.
5. **Verifikations-Suite:** Alle Tests in `tests/test_progression_batch2.py` und der Gesamt-Testsuite bestätigen die korrekte Funktion.
