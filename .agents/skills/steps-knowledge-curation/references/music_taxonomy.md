# STEPS Music Knowledge Taxonomy Reference

This document defines the extensible taxonomy used by the `steps-knowledge-curation` skill to categorize music theory literature, concepts, and analytical frameworks.

## 1. Axioms of the STEPS Music Theory Engine
1. **Pitch vs. Pitch Class vs. Note Spelling**:
   - Sounding pitch includes octave and micro-tuning.
   - Pitch Class is an integer (0..11) in 12-TET.
   - Note Spelling is a diatonic letter (`C` through `B`) plus accidental (`bb`, `b`, natural, `#`, `##`).
2. **Chord Identity vs. Chord Symbol vs. Voicing vs. Inversion**:
   - Chord Identity: Normalized harmonic recipe and quality.
   - Chord Symbol: Textual notation string (e.g., `Cmaj7`).
   - Voicing: Specific pitch arrangement across registers and instruments.
   - Inversion: Bass pitch class relative to chord root (Root, 1st, 2nd, 3rd inversion).
3. **Harmonic Progression vs. Rhythmic Events (`MusicTime`)**:
   - Harmonies are organized along a timeline measured in integer PPQ ticks.
   - Onset and duration are strictly separated.
4. **Theory Rules vs. Corpus Heuristics**:
   - Deterministic rule (e.g., voice leading constraints).
   - Empirical frequency (e.g., ChoCo/Billboard chord transition probabilities).
   - Creative heuristic (e.g., tritone substitution suggestions).
5. **Notation vs. MIDI Export vs. Audio Playback**:
   - MIDI SMF export results in unavoidable information loss (enharmonic spelling and functional Roman numerals are stripped by the standard SMF format).

## 2. Topic Categories
- `THEORY_HARMONY`: Diatonic harmony, chromatic harmony, modal interchange, jazz extensions.
- `THEORY_VOICING`: Close/open voicings, drop-2, drop-4, voice leading distance.
- `THEORY_RHYTHM`: Meter, pulse, micro-timing, groove templates, swing.
- `THEORY_NOTATION`: Sheet music conventions, lead sheet symbols, German vs. International naming.
- `SOFTWARE_MIDI`: Standard MIDI Files (Type 0, Type 1), PPQ, tempo map, control changes.
- `PRODUCTION_DAW`: Sequencer workflows, Ableton Live packs, sound design.
