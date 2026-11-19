# STEPS Glossary

**Baseline commit:** `00f4d5b9079575260c9f26d6d0f3305ab15e241a`
**Audit date:** 2026-11-19
**Status:** IMPLEMENTED — terminology index; definitions summarize repository contracts and do not replace domain review.
**Status key:** IMPLEMENTED = exists; TESTED = automated evidence; PARTIAL = incomplete; PLANNED = future; BLOCKED = decision or dependency; HISTORICAL = dated state; NOT_EVIDENCED = insufficient evidence.

| Term | Meaning in this pack |
|---|---|
| `DE` notation | German naming convention: `H` is B natural; `B` is B-flat |
| `INT` notation | International convention: `B` is B natural; `Bb` is B-flat |
| Chord identity | Harmonic recipe/quality distinct from the displayed chord symbol |
| Chord symbol | Textual shorthand such as `Cmaj7` |
| Enharmonic spelling | Distinct written note names that can map to the same pitch class in 12-TET |
| Function | Context-dependent harmonic role, not an immutable chord property |
| MIDI | Musical instrument digital interface data; SMF export is not audio playback |
| PPQ | Pulses per quarter note; unit for MIDI/timeline tick resolution |
| Pitch | Register-specific sounding note height |
| Pitch class | Pitch class modulo octave; for 12-TET, one of 0–11 |
| Project schema version | Version of serialized project structure, separate from app version |
| SMF | Standard MIDI File |
| Status label | Evidence state: IMPLEMENTED, TESTED, PARTIAL, PLANNED, BLOCKED, HISTORICAL, or NOT_EVIDENCED |
| Timeline event | An event with time position and duration; list order alone is not timing |
| UI language | Language of visible interface strings; independent from musical notation |
| Voicing | Specific notes in register/order for a chord; not the chord identity itself |
| V6.6/V6.7 | Historical knowledge-library revisions, not STEPS app versions |

For theory taxonomy, see `docs/engineering/MUSIC_DOMAIN_AND_MIDI.md`; for project concepts, see `knowledge/glossary/README.md`.
