# STEPS – Musiktheoretische Grundlagen & Vertiefung: Skalensystematik, Akkordtheorie & Stimmführung (Phase 4.9)

**Dokumenttyp:** COMPREHENSIVE MUSIC THEORY SPECIFICATION & SYSTEMATIC EXTENSION  
**Wissensdomänen:** M01 (Grundlagen), M02 (Notation), M03 (Skalen/Modi), M04 (Akkordtheorie), M05 (Harmonielehre), M06 (Voice Leading)  
**Evidenzquellen:** `Scales with 4 smart tools.txt`, `harmony as a student.txt`, `How to use chord files.txt`, Aldwell & Schachter, Hindemith, Schoenberg  
**Status:** `FORMAL_VERIFIED` · `THEORY_SUPPORTED`

---

## 1. M03: Das geschlossene mathematische System der 28 Heptatonik-Skalen (Prehn-Modell)

In der Musiktheorie und Algorithmik von STEPS wird das 7-Ton-Skalensystem (Heptatonik) mathematisch geschlossen formalisiert.
Unter den folgenden 5 Invarianten:
1. **Oktavrahmen:** Jede Skala spannt exakt eine reine Oktave (12 Halbtöne) auf.
2. **Schrittweiten-Restriktion:** Zulässig sind ausschließlich Halbtonschritte ($H = 1$), Ganztonschritte ($W = 2$) und übermäßige Sekundschritte bzw. Terzschritte ($W+H = 3$).
3. **Keine benachbarten Halbtonschritte:** $H$ darf niemals direkt neben $H$ stehen ($1-1$ verboten).
4. **Keine benachbarten 3-Halbton-Schritte:** $3$ darf niemals direkt neben $3$ stehen.
5. **Keine Nachbarschaft von 2 und 3:** Ausgeschlossen zur Wahrung der modalen Stabilität.

Unter diesen Bedingungen existieren **exakt 4 disjunkte Skalenfamilien à 7 Modi = 28 Skalen**:

```
[FAMILIE 1: Major Modes / Kirchentonarten] (Intervallschritte: 2-2-1-2-2-2-1)
  ├── 1. Ionisch (Dur): 1 - 2 - 3 - 4 - 5 - 6 - 7
  ├── 2. Dorisch: 1 - 2 - b3 - 4 - 5 - 6 - b7 (Moll mit großer Sexte 6)
  ├── 3. Phrygisch: 1 - b2 - b3 - 4 - 5 - b6 - b7 (Moll mit kleiner Sekunde b2)
  ├── 4. Lydisch: 1 - 2 - 3 - #4 - 5 - 6 - 7 (Dur mit übermäßiger Quarte #4)
  ├── 5. Mixolydisch: 1 - 2 - 3 - 4 - 5 - 6 - b7 (Dur mit kleiner Septime b7)
  ├── 6. Aeolisch (Natürliches Moll): 1 - 2 - b3 - 4 - 5 - b6 - b7
  └── 7. Lokrisch: 1 - b2 - b3 - 4 - b5 - b6 - b7 (Verminderte Quinte b5)

[FAMILIE 2: Melodic Minor Modes] (Aufsteigend: 2-1-2-2-2-2-1)
  ├── 1. Melodisch Moll: 1 - 2 - b3 - 4 - 5 - 6 - 7 (Moll mit gr. 6 und gr. 7)
  ├── 2. Dorisch b2 (Phrygisch #6): 1 - b2 - b3 - 4 - 5 - 6 - b7
  ├── 3. Lydisch Augmented (#5): 1 - 2 - 3 - #4 - #5 - 6 - 7 (Übermäßige Dur-Skala)
  ├── 4. Lydisch Dominant (Mixolydisch #4): 1 - 2 - 3 - #4 - 5 - 6 - b7
  ├── 5. Mixolydisch b6 (Hindu / Melodic Major): 1 - 2 - 3 - 4 - 5 - b6 - b7
  ├── 6. Lokrisch #2 (Halbvermindert): 1 - 2 - b3 - 4 - b5 - b6 - b7
  └── 7. Alterierte Skala (Superlokrisch / Diminished Whole-Tone): 1 - b2 - b3 - b4 - b5 - b6 - b7

[FAMILIE 3: Harmonic Minor Modes] (Harmonisch Moll: 2-1-2-2-1-3-1)
  ├── 1. Harmonisch Moll: 1 - 2 - b3 - 4 - 5 - b6 - 7 (Hiatus-Schritt b6 -> 7)
  ├── 2. Lokrisch ♮6: 1 - b2 - b3 - 4 - b5 - 6 - b7
  ├── 3. Ionisch #5: 1 - 2 - 3 - 4 - #5 - 6 - 7
  ├── 4. Dorisch #4 (Ukrainisch Dorisch): 1 - 2 - b3 - #4 - 5 - 6 - b7
  ├── 5. Phrygisch Dominant (Spanisch Phrygisch): 1 - b2 - 3 - 4 - 5 - b6 - b7
  ├── 6. Lydisch #2: 1 - #2 - 3 - #4 - 5 - 6 - 7
  └── 7. Alteriert bb7 (Ultralokrisch): 1 - b2 - b3 - b4 - b5 - b6 - bb7

[FAMILIE 4: Harmonic Major Modes] (Harmonisch Dur: 2-2-1-2-1-3-1)
  ├── 1. Harmonisch Dur: 1 - 2 - 3 - 4 - 5 - b6 - 7 (Dur mit kleiner Sexte b6)
  ├── 2. Dorisch b5: 1 - 2 - b3 - 4 - b5 - 6 - b7
  ├── 3. Phrygisch b4: 1 - b2 - b3 - b4 - 5 - b6 - b7
  ├── 4. Lydisch b3 (Lydian Diminished): 1 - 2 - b3 - #4 - 5 - 6 - 7
  ├── 5. Mixolydisch b2: 1 - b2 - 3 - 4 - 5 - 6 - b7
  ├── 6. Lydisch Augmented #2: 1 - #2 - 3 - #4 - #5 - 6 - 7
  └── 7. Lokrisch bb7: 1 - b2 - b3 - 4 - b5 - b6 - bb7
```

---

## 2. M04: Trennung der Schichten: Akkordidentität vs. Voicing vs. Handverteilung

Zur Vermeidung klassischer KI- und Software-Fehler (wie in ERR-006, ERR-013, ERR-025 und ERR-026 dokumentiert) definiert STEPS eine 5-Schichten-Harmonie-Architektur:

| Schicht | Datenelement | Beschreibung & Invarianz | Beispiel C-Dur |
|---|---|---|---|
| **Ebene 1** | `PITCH_CLASS_SET` | Reine ungeordnete Menge modulo 12. Invariant gegen Umkehrung, Transposition über Oktaven und Verdopplungen. | $\{0, 4, 7\}$ |
| **Ebene 2** | `CHORD_IDENTITY` | Harmonische Identität mit Grundton, Tongeschlecht und Zusätzen. | $C\text{-Dur (Triad)}$ |
| **Ebene 3** | `HARMONIC_INVERSION` | Welcher Akkordton liegt im physikalisch tiefsten Bass? ($5/3$ Grundstellung, $6/3$ Terzbass, $6/4$ Quintbass). | $C/E$ ($6/3$-Sextakkord) |
| **Ebene 4** | `ABSOLUTE_VOICING` | Die exakten MIDI-Noten aller erklingenden Stimmen. | `[E2 (40), G3 (55), C4 (60), E4 (64)]` |
| **Ebene 5** | `HAND_ALLOCATION` | Pianistische Zuweisung auf linke und rechte Hand. | LH: `E2 (40)`; RH: `[G3, C4, E4]` |

> [!IMPORTANT]
> **LEHRSATZ FÜR STEPS-ALGORITHMEN:**  
> Eine rechte Hand, die auf dem Klavier `[E4, G4, C5]` greift, spielt **keine "erste Umkehrung des C-Dur-Akkords"**, wenn die linke Hand im Bass zeitgleich ein tiefes `C2` spielt!  
> Die Umkehrung eines Akkords ist **ausschließlich durch den tiefsten Gesamtklingelton (den akustischen Bass)** definiert! Das Gebilde der rechten Hand ist lediglich ein *Sopran-Voicing in weiter oder enger Terzlage*.

---

## 3. M05 & M06: Erweiterung des Progressions-Katalogs um PROG-021 bis PROG-023

Auf Basis der in Phase 4.9 untersuchten Korpora (PPR Boom-Bap, Sub Focus Liquid D&B, Eleanor Rigby Reharmonisation) werden die folgenden drei neuen kanonischen Archetypen verankert:

### A. PROG-021: Neo-Soul Rootless Minor Cycle
- **Stufenfolge:** `i^9 - iv^9 - bVI^maj9 - V^7(b9)`
- **Beispiel in D-Moll (PPR Boom Bap Lesson 1.1):**
  $$Dm^9 \;\longrightarrow\; Gm^9 \;\longrightarrow\; B\flat^{\text{maj}9} \;\longrightarrow\; A^{7(\flat 9)}$$
- **Stimmführung & Rootless Voicing:**
  - Bass spielt stoisch die Grundtöne: $D2 \to G2 \to B\flat 1 \to A1$.
  - Klavier/Keys spielen 4-stimmige Rootless Voicings (Terz, Quinte, Septime, None):
    - Über $D$: `[F3, A3, C4, E4]` (Klingt alleine als $F^{\text{maj}7}$, mit Bass = $Dm^9$!)
    - Über $G$: `[B\flat 3, D4, F4, A4]` (Klingt alleine als $B\flat^{\text{maj}7}$, mit Bass = $Gm^9$!)
    - Über $B\flat$: `[D3, F3, A3, C4]` (Klingt alleine als $Dm^7$, mit Bass = $B\flat^{\text{maj}9}$!)
    - Über $A$: `[C\sharp 4, E4, G4, B\flat 4]` (Klingt alleine als $C\sharp^{\text{dim}7}$, mit Bass = $A^{7(\flat 9)}$!)
- **Charakter:** Höchste klangliche Wärme; der Standard-Zyklus des modernen Neo-Soul, Lo-Fi Hip-Hop und Contemporary R&B.

---

### B. PROG-022: Picardy Third Minor Cadence (Tierce de Picardie)
- **Stufenfolge:** `i - iv - bVII - I` (bzw. `i - iv - V^7 - I`)
- **Beispiel in E-Moll / E-Dur (Eleanor Rigby Level 4):**
  $$Em \;\longrightarrow\; Am \;\longrightarrow\; D \;\longrightarrow\; \mathbf{E\text{-Dur}}$$
- **Harmonisches Prinzip:** Ein Abschnitt in Moll löst sich im letzten Takt überraschend nicht in die Moll-Tonika auf, sondern strahlt durch die Hinzunahme der großen Terz ($G\sharp$ statt $G\natural$) in hellem, festlichem Dur auf.
- **Historische Verwurzelung:** Barockmusik (J. S. Bach), Renaissance-Polyphonie, Romantik und britischer Art-Rock.

---

### C. PROG-023: Liquid D&B Sub-Pulse Cadence (Sub Focus Style)
- **Stufenfolge:** `i - bVI - iv - bVII`
- **Beispiel in E-Moll (174 BPM Two-Step Break):**
  $$Em^7 \;\longrightarrow\; C^{\text{maj}7} \;\longrightarrow\; Am^7 \;\longrightarrow\; D^{\text{add}9}$$
- **Metrische Eigenschaft:**
  Der Reese- oder 808-Subbass moduliert in 8tel-Pulsen auf Grundtönen ($E1 \to C1 \to A0 \to D1$), während die Synthesizer-Pads luftige Septimen und Nonen aushalten.
