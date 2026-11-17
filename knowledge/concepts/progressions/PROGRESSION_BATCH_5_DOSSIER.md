# STEPS – Fachdossier Progressions-Archetypen Gruppe 5 (PROG-008, PROG-017, PROG-018, PROG-020, PROG-027)

> Dieses Fachdossier vertieft die musikwissenschaftliche, harmonische und jazzanalytische Modellierung der fünften Gruppe zentraler Progressions-Archetypen des [Kanonischen Progressions-Atlas](CHORD_PROGRESSION_REFERENCE_LIBRARY.md).

**Dokumenttyp:** HARMONIETHEORETISCHES VERTIEFUNGSDOSSIER  
**Wissensdomänen:** M04 (Akkordtheorie), M05 (Harmonielehre), M06 (Voice Leading), M09 (Genre-Atlas)  
**Notationsstandard:** SPN (C4 = MIDI 60); deutsches H = int. B explizit.

---

## 1. Übersicht der Gruppe 5 (Blues, Jazz-Blues & Alterationen)

| ID | Name / Archetyp | Stufen (Standardtonart) | Akkordfolge | Harmonischer Motor & Familie | Primäre Fachquellen |
|---|---|---|---|---|---|
| `PROG-008` | 12-Bar Blues | `Idom7 - IVdom7 - Idom7 - V^7 - IVdom7 - Idom7` | `C7 - F7 - C7 - G7 - F7 - C7` | Blues-Funktion mit nicht-auflösenden Dominantseptakkorden | Rawlins/Bahha (2005), Open Music Theory |
| `PROG-017` | Classical Jazz Backdoor ii–V | `iv^7 - bVII^7 - I^maj7` | `Fm7 - Bb7 - Cmaj7` | Mollsubdominantischer Ganzton-Herantritt (*Lady Bird*) | Levine (1995), Terefenko (2014) |
| `PROG-018` | Substitute Backdoor ii–V | `ii^7 - bVII^7 - I^maj7` | `Dm7 - Bb7 - Cmaj7` | Diatonische Supertonika mit Backdoor-Dominantsubstitution | Rawlins/Bahha (2005) |
| `PROG-020` | Extended Tritone Sub (Altered) | `ii^9 - bII^7(#11) - I^maj9` | `Dm9 - Db7(#11) - Cmaj9` | Alterierte Tritonussubstitution mit $\sharp 11$-Tonikaantizipation | Levine (1995), Pease (2003) |
| `PROG-027` | Minor Jazz Blues Submediant Turnaround | `i^7 - iv^7 - i^7 - bVI^maj7 - V^7(#11) - i^7` | `Cm7 - Fm7 - Cm7 - Abmaj7 - G7(#11) - Cm7` | Submedianten-Turnaround im Minor Blues (*Birk's Works*) | Levine (1995), Terefenko (2014) |

---

## 2. Detaillierte Fachanalyse je Archetyp

### 2.1 PROG-008 – 12-Bar Blues (Kanonisches Harmonieschema)

* **Stufengang (in C-Dur):**
  * $\text{I}^{\text{dom}7} - \text{IV}^{\text{dom}7} - \text{I}^{\text{dom}7} - \text{V}^7 - \text{IV}^{\text{dom}7} - \text{I}^{\text{dom}7}$
  * Stufenakkorde: $\text{C}^7 - \text{F}^7 - \text{C}^7 - \text{G}^7 - \text{F}^7 - \text{C}^7$
* **Klanggestalt & Voicing (in C):**
  * $\text{C}^7$ (MIDI `[48, 52, 55, 58]` / $C - E - G - B\flat$)
  * $\text{F}^7$ (MIDI `[41, 45, 48, 51]` / $F - A - C - E\flat$)
  * $\text{G}^7$ (MIDI `[43, 47, 50, 53]` / $G - H - D - F$)
* **Harmonischer Motor (Rawlins/Bahha 2005 / Open Music Theory):**
  * **Nicht-dominante Septakkorde:** Im Blues fungieren Akkorde mit kleiner Septime ($\text{C}^7$, $\text{F}^7$) nicht als auflösungsbedürftige Zwischendominanten, sondern als primäre tonale Ruhepole und Klangfarben (Blues-Tonika und Blues-Subdominante).
  * **Blue Notes:** Die kleine Septime der Tonika ($B\flat$ in $\text{C}^7$) etabliert die charakteristische $\flat 7$-Färbung der Blues-Tonleiter direkt im Harmoniegerüst.
  * **Guide-Tone-Shifts:** Zwischen $\text{C}^7$ und $\text{F}^7$ findet eine Umkehrung der Terz-Septim-Rollen statt: Die Terz $E$ von $\text{C}^7$ fällt chromatisch zur Septime $E\flat$ von $\text{F}^7$, während die Septime $B\flat$ zum $A$ (Terz von $\text{F}^7$) absinkt.
  * **Plagale Blues-Kadenz $\text{V}^7 \to \text{IV}^7 \to \text{I}^7$:** Im Gegensatz zur klassischen Kadenz weicht der 12-Takter von der Dominante $\text{V}^7$ über die Subdominante $\text{IV}^7$ zurück in die Tonika $\text{I}^7$ aus.

---

### 2.2 PROG-017 – Classical Jazz Backdoor ii–V

* **Stufengang (in C-Dur):**
  * $\text{iv}^7 - \flat\text{VII}^7 - \text{I}^{\text{maj}7}$
  * Stufenakkorde: $\text{Fm}^7 - \text{B}\flat^7 - \text{C}^{\text{maj}7}$
* **Klanggestalt & Voicing (in C):**
  * $\text{Fm}^7$ (MIDI `[53, 56, 60, 63]` / $F - A\flat - C - E\flat$)
  * $\text{B}\flat^7$ (int. Bb = dt. B; MIDI `[46, 50, 53, 56]` / $B\flat - D - F - A\flat$)
  * $\text{C}^{\text{maj}7}$ (MIDI `[48, 52, 55, 59]` / $C - E - G - H$)
* **Harmonischer Motor (Levine 1995 / Terefenko 2014):**
  * **Moll-Subdominante als ii-V-Kopf:** $\text{Fm}^7$ ist die Moll-Subdominante ($\text{iv}^7$) aus dem parallelen Äolisch (Modal Interchange). Im Backdoor-Kontext bildet sie die lokale $\text{ii}^7$ zur Subtonika $\text{B}\flat^7$.
  * **Ganzton-Schluss:** Die Dominante $\flat\text{VII}^7$ nähert sich der Tonika $\text{I}$ von einem Ganzton darunter ($B\flat \to C$). Dies umgeht die Tritonusspannung zum Leitton ($H$) und erzeugt einen eleganten, weichen Klangschluss.
  * **Chromatischer Innenstimmenabstieg:** Der Ton $A\flat$ (Terz in $\text{Fm}^7$, Septime in $\text{B}\flat^7$) löst sich mit starkem melodischem Zug um einen Halbton abwärts in die Quinte $G$ der Tonika $\text{C}^{\text{maj}7}$ auf.
  * Prominente Verwendung: Tadd Damers *Lady Bird*, Charlie Parkers *Yardbird Suite*.

---

### 2.3 PROG-018 – Substitute Backdoor ii–V

* **Stufengang (in C-Dur):**
  * $\text{ii}^7 - \flat\text{VII}^7 - \text{I}^{\text{maj}7}$
  * Stufenakkorde: $\text{Dm}^7 - \text{B}\flat^7 - \text{C}^{\text{maj}7}$
* **Klanggestalt & Voicing (in C):**
  * $\text{Dm}^7$ (MIDI `[50, 53, 57, 60]` / $D - F - A - C$)
  * $\text{B}\flat^7$ (MIDI `[46, 50, 53, 56]` / $B\flat - D - F - A\flat$)
  * $\text{C}^{\text{maj}7}$ (MIDI `[48, 52, 55, 59]` / $C - E - G - H$)
* **Harmonischer Motor (Rawlins/Bahha 2005):**
  * **Hybride Verknüpfung:** Verbindet die rein diatonische zweite Stufe ($\text{Dm}^7$) mit der modalfremden Backdoor-Dominante ($\text{B}\flat^7$).
  * **Maximale Tontreue:** $\text{Dm}^7$ und $\text{B}\flat^7$ teilen sich die Töne $D$ und $F$. Lediglich $A$ inflektiert chromatisch zu $A\flat$, während $C$ zu $B\flat$ wird.
  * Dies ermöglicht eine geschmeidige Stimmführung im Cool Jazz und West Coast Bebop.

---

### 2.4 PROG-020 – Extended Tritone Sub (Altered / Lydian Dominant)

* **Stufengang (in C-Dur):**
  * $\text{ii}^9 - \flat\text{II}^{7(\sharp 11)} - \text{I}^{\text{maj}9}$
  * Stufenakkorde: $\text{Dm}^9 - \text{D}\flat^{7(\sharp 11)} - \text{C}^{\text{maj}9}$
* **Klanggestalt & Voicing (in C):**
  * $\text{Dm}^9$ (MIDI `[50, 53, 57, 60, 64]` / $D - F - A - C - E$)
  * $\text{D}\flat^{7(\sharp 11)}$ (MIDI `[49, 53, 55, 56, 59]` / $D\flat - F - G - A\flat - C\flat[H]$)
  * $\text{C}^{\text{maj}9}$ (MIDI `[48, 52, 55, 59, 62]` / $C - E - G - H - D$)
* **Harmonischer Motor (Pease 2003 / Levine 1995):**
  * **Lydisch Dominant ($\flat\text{II}^{7(\sharp 11)}$):** Die übermäßige Undezime ($\sharp 11$) über $D\flat$ ist $G$ ($49 + 6 = 55$).
  * **Tonic-Antizipation:** Das $G$ ist zugleich die Quinte der Zieltonika $C$. Dadurch fungiert die Alteration nicht als klangliche Reibung, sondern als harmonische Antizipation der Zieltonika!
  * **Paralleler Halbton-Bass:** Der Bass gleitet chromatisch abwärts: $D \xrightarrow{-1} D\flat \xrightarrow{-1} C$.
  * **Upper-Structure-Stimmführung:** Die None $E$ in $\text{Dm}^9$ steigt leittönig zur $\sharp 11$ ($G$) in $\text{D}\flat^{7(\sharp 11)}$ auf und führt zur None $D$ in $\text{C}^{\text{maj}9}$ zurück.

---

### 2.5 PROG-027 – Minor Jazz Blues Submediant Turnaround

* **Stufengang (in c-Moll):**
  * $\text{i}^7 - \text{iv}^7 - \text{i}^7 - \flat\text{VI}^{\text{maj}7} - \text{V}^{7(\sharp 11)} - \text{i}^7$
  * Stufenakkorde: $\text{Cm}^7 - \text{Fm}^7 - \text{Cm}^7 - \text{A}\flat^{\text{maj}7} - \text{G}^{7(\sharp 11)} - \text{Cm}^7$
* **Klanggestalt & Voicing (in Cm):**
  * $\text{Cm}^7$ (MIDI `[48, 51, 55, 58]` / $C - E\flat - G - B\flat$)
  * $\text{Fm}^7$ (MIDI `[53, 56, 60, 63]` / $F - A\flat - C - E\flat$)
  * $\text{A}\flat^{\text{maj}7}$ (MIDI `[44, 48, 51, 55]` / $A\flat - C - E\flat - G$)
  * $\text{G}^{7(\sharp 11)}$ (MIDI `[43, 47, 49, 53]` / $G - H - C\sharp/D\flat - F$)
* **Harmonischer Motor (Levine 1995 / Terefenko 2014):**
  * **Submedianten-Einschub:** Statt einer reinen $\text{ii}-\text{V}$-Folge nutzt der Minor Blues die Durseptakkord-Submediante $\flat\text{VI}^{\text{maj}7}$ ($A\flat^{\text{maj}7}$) als Sprungbrett zur Dominante.
  * **Halbtonabstieg zur Dominante:** Der Grundton sinkt um einen Halbton von $A\flat$ nach $G$.
  * **$\sharp 11$-Spannung im Dominantseptakkord:** $C\sharp/D\flat$ in $\text{G}^{7(\sharp 11)}$ verstärkt die Dissonanz, die sich im Grundton $C$ der Tonika $\text{Cm}^7$ auflöst.
  * Standardwerke: Dizzy Gillespies *Birk's Works*, Wayne Shorters *Footprints*.

---

## 3. Implementierungsnachweis in STEPS

1. **Theorie-Profile (`ARCHETYPE_THEORY_METADATA`):** Vollständig implementiert in `src/steps/progression/engine.py`.
2. **Mustererkennung (`detect_progression_archetypes`):** Exakte und rotierte Identifikation aller 5 Archetypen verifiziert.
3. **Session-Vorschlagsengine (`ProgressionSession.explore_next_chords`):**
   * Automatische Empfehlung von $\text{IV}^{\text{dom}7}$ und Blues-Rückkehr bei $\text{I}^{\text{dom}7}$.
   * Backdoor-Dominanten $\flat\text{VII}^7$ nach $\text{iv}^7$ und $\text{ii}^7$.
   * Alterierte $\flat\text{II}^{7(\sharp 11)}$-Auflösung in $\text{I}^{\text{maj}9}$.
   * Minor-Blues-Turnaround mit $\flat\text{VI}^{\text{maj}7}$ und $\text{V}^{7(\sharp 11)}$.
4. **Stimmführungseigenschaften:** L1-Distanz, Zirkuläre Distanz und Stimmkreuzungsfreiheit mathematisch in `tests/test_progression_batch5.py` nachgewiesen.
