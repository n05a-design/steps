# STEPS – Fachdossier Progressions-Archetypen Gruppe 3 (PROG-007, PROG-010, PROG-011, PROG-013, PROG-014)

> Dieses Fachdossier vertieft die musikwissenschaftliche, harmonische und stufentheoretische Modellierung der dritten Gruppe zentraler Progressions-Archetypen des [Kanonischen Progressions-Atlas](CHORD_PROGRESSION_REFERENCE_LIBRARY.md).

**Dokumenttyp:** HARMONIETHEORETISCHES VERTIEFUNGSDOSSIER  
**Wissensdomänen:** M04 (Akkordtheorie), M05 (Harmonielehre), M06 (Voice Leading), M09 (Genre-Atlas)  
**Notationsstandard:** SPN (C4 = MIDI 60); deutsches H = int. B explizit.

---

## 1. Übersicht der Gruppe 3

| ID | Name / Archetyp | Stufen (Standardtonart) | Akkordfolge | Harmonischer Motor & Familie | Primäre Fachquellen |
|---|---|---|---|---|---|
| `PROG-007` | Dorian Groove Vamp | `i^7 - IV^7` (in Dm) | `Dm7 - G7` | Modaler Vamp / Dorische Sexte | Pease (2003) |
| `PROG-010` | Secondary Dominant Lift | `I - V^7/vi - vi - IV` (in C) | `C - E7 - Am - F` | Zwischendominante mit Leittonanhebung | Kostka/Payne (2013) |
| `PROG-011` | Modal Interchange Aeolian | `I - bVI - bVII - I` (in C) | `C - Ab - Bb - C` | Doppelter Subtonik-Schritt (Mario Cadence / Epic Pop) | Mulholland (2013) |
| `PROG-013` | Tritone Substitution Cadence | `ii^7 - bII^7 - I^maj7` (in C) | `Dm7 - Db7 - Cmaj7` | Tritonussubstitution der Dominante / Chromatischer Bass | Levine (1995) |
| `PROG-014` | Backdoor Resolution (IV) | `IV - bVII^7 - I` (in C) | `F - Bb7 - C` | Subdominantische Backdoor-Kadenz | Terefenko (2014) |

---

## 2. Detaillierte Fachanalyse je Archetyp

### 2.1 PROG-007 – Dorian Groove Vamp

* **Stufengang (in d-Moll / D-Dorisch):**
  * $\text{i}^7 - \text{IV}^7$
  * Funktionale Syntax: Tonika-Mollseptakkord $\to$ Dur-Subdominante mit kleiner Septime
* **Klanggestalt & Voicing (in Dm):**
  * $\text{Dm}^7$ (MIDI `[50, 53, 57, 60]` / $D - F - A - C$)
  * $\text{G}^7$ (MIDI `[43, 53, 59, 62]` / $G - F - H - D$)
* **Modale Harmonik (Pease 2003):**
  * Kennzeichnend für den dorischen Modus ist die **große Sexte** über dem Grundton ($H$ bzw. int. $B$ in D-Dorisch).
  * Der Akkord $\text{G}^7$ liefert genau diesen charakteristischen Ton als seine große Terz ($H$).
  * Durch das Pendeln zwischen $\text{Dm}^7$ und $\text{G}^7$ ohne Auflösung nach C-Dur bleibt die Tonalität modal auf D zentriert (Klassiker in Funk, Fusion und Modal Jazz wie *So What* oder *Oye Como Va*).

---

### 2.2 PROG-010 – Secondary Dominant Lift

* **Stufengang (in C-Dur):**
  * $\text{I} - \text{V}^7/\text{vi} - \text{vi} - \text{IV}$
  * Funktionale Syntax: Tonika $\to$ Zwischendominante zur Submediante $\to$ Submediante $\to$ Subdominante
* **Klanggestalt & Voicing (in C):**
  * $\text{C}$ (MIDI `[48, 52, 55, 60]` / $C - E - G$)
  * $\text{E}^7$ (MIDI `[52, 56, 59, 62]` / $E - G\sharp - H - D$)
  * $\text{Am}$ (MIDI `[57, 60, 64]` / $A - C - E$)
  * $\text{F}$ (MIDI `[53, 57, 60, 65]` / $F - A - C$)
* **Harmonischer Motor (Kostka/Payne 2013):**
  * $\text{E}^7$ fungiert als angewandte Dominante ($\text{V}^7/\text{vi}$), deren große Terz $G\sharp$ den chromatischen Leitton zur Zieltonika $\text{Am}$ bildet ($G \to G\sharp \to A$).
  * Der anschließende Wechsel von $\text{Am}$ nach $\text{F}$ führt die Bewegung über eine Terzverbindung terzabwärts in die Subdominante weiter.

---

### 2.3 PROG-011 – Modal Interchange Aeolian

* **Stufengang (in C-Dur):**
  * $\text{I} - \flat\text{VI} - \flat\text{VII} - \text{I}$
  * Stufenakkorde: $\text{C} - \text{A}\flat - \text{B}\flat - \text{C}$
* **Klanggestalt & Voicing (in C):**
  * $\text{C}$ (MIDI `[48, 52, 55, 60]` / $C - E - G$)
  * $\text{A}\flat$ (MIDI `[56, 60, 63]` / $A\flat - C - E\flat$)
  * $\text{B}\flat$ (MIDI `[58, 62, 65]` / $B\flat - D - F$)
  * $\text{C}$ (MIDI `[60, 64, 67]` / $C - E - G$)
* **Harmonischer Motor (Mulholland 2013):**
  * **Modal Interchange (Moll-Entlehnung):** $\text{A}\flat$ ($\flat\text{VI}$) und $\text{B}\flat$ ($\flat\text{VII}$) entstammen dem parallelen c-Moll (äolisch).
  * **Stufenweiser Ganztonanstieg im Bass:** $A\flat \xrightarrow{+2} B\flat \xrightarrow{+2} C$.
  * Bekannt als *Mario Cadence* oder heroische Rock-/Filmmusikkadenz durch den kraftvollen, nicht-diatonischen Ganzton-Antritt zurück zur Tonika.

---

### 2.4 PROG-013 – Tritone Substitution Cadence

* **Stufengang (in C-Dur):**
  * $\text{ii}^7 - \flat\text{II}^7 - \text{I}^{\text{maj}7}$
  * Jazzkadenz mit Substitution: $\text{Dm}^7 - \text{D}\flat^7 - \text{C}^{\text{maj}7}$
* **Klanggestalt & Voicing (in C):**
  * $\text{Dm}^7$ (MIDI `[50, 53, 57, 60]` / $D - F - A - C$)
  * $\text{D}\flat^7$ (MIDI `[49, 53, 56, 59]` / $D\flat - F - A\flat - C\flat$)
  * $\text{C}^{\text{maj}7}$ (MIDI `[48, 52, 55, 59]` / $C - E - G - H$)
* **Tritonussubstitution (Levine 1995):**
  * Der Dominantseptakkord $\text{G}^7$ ($G - H - D - F$) und sein Tritonus-Partner $\text{D}\flat^7$ ($D\flat - F - A\flat - C\flat$) teilen denselben aktiven Tritonus zwischen 3. und 7. Stufe:
    $$\{H, F\} \equiv \{C\flat, F\}$$
  * Durch den Austausch von $\text{G}^7$ gegen $\text{D}\flat^7$ entsteht im Bass ein lückenloser chromatischer Abstieg:
    $$D \xrightarrow{-1} D\flat \xrightarrow{-1} C$$
  * Gleichzeitig lösen sich alle Dissonanzen halbtonweise nach innen in die Terz und Quinte von $\text{C}^{\text{maj}7}$ auf ($D\flat \to C$, $F \to E$, $A\flat \to G$, $C\flat/H \to H$).

---

### 2.5 PROG-014 – Backdoor Resolution (IV)

* **Stufengang (in C-Dur):**
  * $\text{IV} - \flat\text{VII}^7 - \text{I}$
  * Akkorde: $\text{F} - \text{B}\flat^7 - \text{C}$
* **Klanggestalt & Voicing (in C):**
  * $\text{F}$ (MIDI `[53, 57, 60]` / $F - A - C$)
  * $\text{B}\flat^7$ (MIDI `[58, 62, 65, 68]` / $B\flat - D - F - A\flat$)
  * $\text{C}$ (MIDI `[60, 64, 67]` / $C - E - G$)
* **Harmonischer Motor (Terefenko 2014):**
  * Anstelle der regulären Dominante $\text{V}^7$ ($\text{G}^7$) löst sich die Subtonika $\flat\text{VII}^7$ ($\text{B}\flat^7$) von „hinten“ (*Backdoor*) in die Tonika auf.
  * Der Akkord $\text{B}\flat^7$ fungiert funktionell als Vertreter der Mollsubdominante $\text{Fm}^6$ ($\{F, A\flat, C, D\}$ entspricht $\text{B}\flat^9$ ohne Grundton).
  * Die Innenstimme $A\flat$ sinkt chromatisch um einen Halbton zur Quinte $G$ der Tonika ab, während der Bass von $B\flat$ nach $C$ springt.

---

## 3. Implementierungsnachweis in STEPS

1. **Theorie-Profile (`ARCHETYPE_THEORY_METADATA`):** Alle fünf Profile sind vollständig in `src/steps/progression/engine.py` integriert.
2. **Muster-Erkennung (`detect_progression_archetypes`):** Erkennung beliebiger Akkordfolgen, automatisierte Identifikation von Transpositionen und exakten Matches.
3. **Session-Vorschlagsengine (`ProgressionSession.explore_next_chords`):**
   * Tritonussubstitution auf $\text{ii}$ ($\text{Dm} \to \text{D}\flat^7$).
   * Backdoor-Auflösung auf $\flat\text{VII}^7$ ($\text{B}\flat^7 \to \text{C}$).
   * Zwischendominanten-Lift auf $\text{I}$ ($\text{C} \to \text{E}^7$).
4. **Verifikations-Suite:** Alle Tests in `tests/test_progression_batch3.py` validieren diese Invarianten.
