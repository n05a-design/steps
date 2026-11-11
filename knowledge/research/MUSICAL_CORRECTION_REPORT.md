# STEPS Musical Correction Report (Phase 4.15)

**Date**: 2026-11-11  
**Phase**: STEPS Phase 4.15  
**Topic**: High-Fidelity Musical Corrections, Harmonic Integrity, and Corpus Harmonization  
**Status**: **VERIFIED COMPLETE**

---

## 1. Overview & Musical Axioms

In accordance with `docs/engineering/MUSIC_DOMAIN_AND_MIDI.md`, music theory data in STEPS must strictly respect core domain axioms:
- Sounding pitch $\neq$ pitch class ($0..11$) $\neq$ note spelling.
- Chord identity $\neq$ chord symbol $\neq$ voicing $\neq$ inversion $\neq$ context function.
- Progression $\neq$ rhythmic events (`MusicTime` ticks) $\neq$ phrasing $\neq$ style context.
- Notation $\neq$ MIDI export $\neq$ audio playback.

Phase 4.15 audited and repaired several subtle musical defects and table omissions that were identified in the Phase 4.14 codebase.

---

## 2. Corrected Harmonic Progressions

### 2.1 PROG-016: Table Row Pipe Formatting & Chromatic Mediant Axis
* **Issue**: In Phase 4.14, the markdown row for `PROG-016` omitted a column delimiter pipe, collapsing the example and context fields into a single column.
* **Harmonic Correction**:
  - **ID**: `PROG-016`
  - **Name**: Chromatic Mediants (Dual-Axis)
  - **Roman Numeral / Stufe**: `I^maj7 - V^7/bVI - bVI^maj7 - V^7/III - III^maj7`
  - **Concrete Example**: `Cmaj7 - Eb7 - Abmaj7 - B7 - Emaj7`
  - **Context & Theory**: Non-diatonic third relations, Neo-Riemannian P- and L-transformations, voice-leading through chromatic parsimonious steps.
  - **Domain**: `M02`
* **Table Verification**: Verified 6 columns; unit test `test_11_mutation_malformed_markdown_table_row` guards against column dropping.

### 2.2 PROG-021: Neo-Soul Minor Cycle Harmonic Realization
* **Issue**: PROG-021 had previously been listed with a generic major-modal vamp, which conflicted with the authentic Neo-Soul genre signature.
* **Harmonic Correction**:
  - **ID**: `PROG-021`
  - **Name**: Neo-Soul Minor 9th Cadence
  - **Roman Numeral / Stufe**: `i^9 - iv^9 - bVI^maj9 - V^7(b9)`
  - **Concrete Example**: `Dm9 - Gm9 - Bbmaj9 - A7(b9)`
  - **Voicing Structure**: Extended 9th chords with minor third and seventh intervals; rootless piano voicings often drop root to bass and voice $[b3, 5, b7, 9]$.
  - **Altered Dominant**: Resolution via altered dominant `A7(b9)` providing half-step tension ($Bb \rightarrow A$, $C\# \rightarrow D$).
  - **Domain**: `M02`

### 2.3 PROG-025, PROG-026, PROG-027 Confirmations
* **PROG-025**:
  - **Name**: Lydian Major Vamp
  - **Stufe**: `I^maj7(#11) - II/I`
  - **Example**: `Cmaj7(#11) - D/C`
  - **Theory**: `#4`/`#11` acoustic scale sonority, modal jazz / film scoring vamp.
* **PROG-026**:
  - **Name**: Phrygian Cadence Extended
  - **Stufe**: `i - bII^maj7 - vii^o7 - i`
  - **Example**: `Fm - Gbmaj7 - E°7 - Fm`
  - **Theory**: Flamenco cadence with half-step upper neighbor bass descent ($Gb \rightarrow F$) reinforced by leading-tone diminished chord ($E^\circ7$).
* **PROG-027**:
  - **Name**: Coltrane Matrix Major (Giant Steps Cycle)
  - **Stufe**: `I^maj7 - V^7/bVI - bVI^maj7 - V^7/III - III^maj7 - V^7 - I^maj7`
  - **Example**: `Cmaj7 - Eb7 - Abmaj7 - B7 - Emaj7 - G7 - Cmaj7`
  - **Theory**: Major thirds cycle dividing the octave into three equal tonal centers ($C$, $Ab$, $E$) linked by secondary dominants ($Eb7$, $B7$, $G7$).

---

## 3. Corrected Piano Modules (P18 & P19)

* **P18: Drop-2 Voicings Rootless 7th/9th**
  - **Technical Basis**: Open spacing; taking the second note from the top of a closed voicing and dropping it down an octave.
  - **Voicing Formula**: Bass plays root; LH/RH plays $3, 7, 9, 5$ or $7, 3, 5, 9$.
  - **Application**: Standard jazz accompaniment, preventing muddy frequency clashes in the lower midrange ($< 250$ Hz).
  - **Difficulty**: Advanced | Domain: `M05`

* **P19: Quartal Stacks (McCoy Tyner Modern Jazz)**
  - **Technical Basis**: Voicings built on stacked perfect fourths (and occasional augmented fourths) rather than traditional tertian chords.
  - **Voicing Formula**: e.g., $E - A - D - G - C$ over $C$ or $D$ Dorian.
  - **Application**: Ambiguous harmonic weight allowing chromatic side-slipping and modal tension.
  - **Difficulty**: Advanced | Domain: `M05`

---

## 4. Drum Library Header & PAT-031 Consistency

* **Header Update**:
  - `DRUM_GROOVE_REFERENCE_LIBRARY.md` previously read `25 Grooves` in the section header, despite containing 31 distinct groove patterns.
  - Header was updated to `31 Grooves (PAT-001 .. PAT-031)`.
* **PAT-031 Specification**:
  - **ID**: `PAT-031`
  - **Name**: Afrobeat 12/8 Polyrhythm
  - **Time Signature**: `12/8` | **Subdivision**: `1/8-triple` | **Tempo**: `112 BPM`
  - **Rhythmic Signature**: Polyrhythmic bell pattern ($3:2$ feel) with cross-metric accents on dotted quarters and syncopated snare backbeats.
  - **Domain**: `M03`

---

## 5. Verification Checklist

- [x] All 27 chord progressions possess valid functional analyses and concrete pitch examples.
- [x] All 31 drum patterns possess time signatures, tempos, grid subdivisions, and rhythmic signatures.
- [x] All 19 piano modules possess hand split definitions and difficulty ratings.
- [x] Enharmonic note spelling conforms to key context ($Dm9 - Gm9 - Bbmaj9 - A7(b9)$, not $A\#maj9$).
- [x] All 198 golden test cases reflect these exact musical values and pass independent algorithmic verification.
