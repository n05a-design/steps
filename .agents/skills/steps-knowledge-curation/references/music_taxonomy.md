# STEPS Music Knowledge Taxonomy Reference

This document defines the extensible taxonomy used by the `steps-knowledge-curation` skill to categorize music theory literature, concepts, and analytical frameworks.

## 1. Concepts and notation conventions
1. **Pitch vs. Pitch Class vs. Note Spelling**:
   - Sounding pitch includes octave and micro-tuning.
   - Pitch Class is an integer (0..11) in 12-TET.
   - Record notation convention explicitly. In `INT`, B denotes B natural. In `DE`, H denotes B natural and B denotes B-flat. In 12-TET, F-sharp and G-flat can share a pitch class while retaining different spellings and harmonic roles.
2. **Chord Identity vs. Chord Symbol vs. Voicing vs. Inversion**:
   - Chord Identity: Normalized harmonic recipe and quality.
   - Chord Symbol: Textual notation string (e.g., `Cmaj7`).
   - Voicing: Specific pitch arrangement across registers and instruments.
   - Inversion: Position determined by which chord member is in the bass. Record an explicit non-chord slash bass separately and document function in the tonal or stylistic context.
3. **Harmonic Progression vs. Rhythmic Events (`MusicTime`)**:
   - Harmonies are organized along a timeline measured in integer PPQ ticks.
   - Onset and duration are strictly separated.
4. **Theory Rules vs. Corpus Heuristics**:
   - Deterministic rule (e.g., voice leading constraints).
   - Empirical frequency (e.g., ChoCo/Billboard chord transition probabilities).
   - Creative heuristic (e.g., tritone substitution suggestions).
5. **Notation vs. MIDI Export vs. Audio Playback**:
   - Standard MIDI note events carry pitch numbers. Enharmonic spelling and harmonic analysis cannot be reconstructed from those events alone. SMF can carry descriptive metadata. Verify what the exporter writes and what the receiving application preserves. See the [MIDI Association SMF overview](https://midi.org/standard-midi-files).

## 2. Topic Categories
- `THEORY_HARMONY`: Diatonic harmony, chromatic harmony, modal interchange, jazz extensions.
- `THEORY_VOICING`: Close/open voicings, drop-2, drop-4, voice leading distance.
- `THEORY_RHYTHM`: Meter, pulse, micro-timing, groove templates, swing.
- `THEORY_NOTATION`: Sheet music conventions, lead sheet symbols, German vs. International naming.
- `SOFTWARE_MIDI`: Standard MIDI Files (Type 0, Type 1), PPQ, tempo map, control changes.
- `PRODUCTION_DAW`: Sequencer workflows, Ableton Live packs, sound design.
