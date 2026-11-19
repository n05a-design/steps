# Music Theory Engine and Musical Distinctions

**Baseline commit:** `00f4d5b9079575260c9f26d6d0f3305ab15e241a`
**Audit date:** 2026-11-19
**Status:** IMPLEMENTED / TESTED for selected core behaviors; PARTIAL for full theory coverage and human review.
**Status key:** IMPLEMENTED = exists; TESTED = automated evidence; PARTIAL = incomplete; PLANNED = future; BLOCKED = decision or dependency; HISTORICAL = dated state; NOT_EVIDENCED = insufficient evidence.

## Core distinctions

1. **Pitch** is a sounding/register-specific height; **pitch class** is a 12-TET class (0–11); **spelling** is a letter plus accidental. Equal pitch class does not make spellings functionally identical: `F#` and `Gb` may sound alike but have different diatonic roles.
2. **Chord identity** is a harmonic recipe; **symbol** is textual notation; **voicing** is ordered notes in registers; **inversion** concerns the bass relative to the chord; **function** depends on context.
3. A progression is not its timed events, phrasing, or style context. Onset and duration are distinct.
4. A deterministic rule is not a corpus statistic or a creative heuristic.
5. Notation is not MIDI export or audio playback. Standard MIDI does not reliably preserve enharmonic spelling or Roman-numeral analysis.

## German and international notation

The notation setting is explicit: `DE` uses `H` for B natural and `B` for B-flat; `INT` uses `B` for B natural and `Bb` for B-flat. Ambiguous `B` input must not be interpreted without a known convention. UI language does not choose notation.

## Contextual interpretation

An event can support more than one theoretical reading. For example, `E7 → Am` can be `V7 → i` in A minor or `V7/vi → vi` in C major. A correct explanation exposes the key, framework/style assumptions, and alternatives where relevant. It must not present one interpretation as context-free fact.

## Implemented code and boundaries

Key modules include `src/steps/theory/pitch.py`, `interval.py`, `chord.py`, `triad.py`, `seventh.py`, `inversion.py`, `voicings.py`, and `src/steps/progression/engine.py`, `voice_leading.py`, and `recommender.py`. Tests include `tests/test_notation_contract.py`, `test_theory_core.py`, `test_golden_music_invariants.py`, `test_progression_engine.py`, and `test_voice_leading_styles.py`.

These are not proof that every music tradition or edge case is represented. Human music-theory review, exhaustive source validation, and user comprehension are NOT_EVIDENCED as universal acceptance. Explicit unresolved semantics appear in `docs/engineering/MUSIC_DOMAIN_AND_MIDI.md` and `docs/project/CONFLICTS_AND_GAPS.md`.

## References

- `docs/engineering/MUSIC_DOMAIN_AND_MIDI.md`
- `decisions/ADR-014-theorie-perspektiven-und-kontext.md`
- `decisions/ADR-015-kernvertraege-intervalle-voicing-notation.md`
- `knowledge/benchmark/PILOT_ABNAHME.md`
- [Glossary](16_GLOSSARY.md)
