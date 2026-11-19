# Product Strategy and Scope

**Baseline commit:** `00f4d5b9079575260c9f26d6d0f3305ab15e241a`
**Audit date:** 2026-11-19
**Status:** PARTIAL — v0.1 scope is accepted; 1.0 remains a proposed, unapproved product hypothesis.
**Status key:** IMPLEMENTED = exists; TESTED = automated evidence; PARTIAL = incomplete; PLANNED = future; BLOCKED = decision or dependency; HISTORICAL = dated state; NOT_EVIDENCED = insufficient evidence.

## Accepted direction

[ADR-013](../../decisions/ADR-013-v01-umfang-akkorde-und-midi-export.md) records the v0.1 slice: enter, transpose and analyze chords, then export Standard MIDI; the primary audience is producers who want to learn while producing. Drum editing is deferred to v2 of the app. Existing rhythm research and timeline preparation do not override that decision. [ADR-007](../../decisions/ADR-007-audio-nur-dateiexport-v01.md) keeps v0.1 to file export rather than in-app playback.

## Proposed 1.0 outcome

The not-yet-approved target is a local-first progression workspace where a producer can edit and transpose chords, inspect contextual and qualified theory explanations, preserve notation, save/reopen work, and export MIDI. User success, accessibility, and market differentiation are NOT_EVIDENCED by repository tests. The 1.0 contract is in `docs/product/V1.0.0_PRODUCT_CONTRACT.md`.

## Product evidence matrix

| Statement | Status | Boundary |
|---|---|---|
| Chord editing and analysis are a product direction | IMPLEMENTED / TESTED in code pathways | See `app/ui/`, `src/steps/progression/`, and `tests/`; not usability acceptance |
| MIDI file export is in v0.1 scope | IMPLEMENTED / TESTED | Not live audio and not independent DAW sign-off |
| Drums are in v0.1 | BLOCKED / contradicted by accepted ADR-013 | Drum editing deferred to app v2 |
| Producers learn while composing | PLANNED as product positioning | User outcome not measured |
| Product-market fit or learning effectiveness | NOT_EVIDENCED | Requires human research |
| 1.0 schedule and release scope | BLOCKED | No accepted 1.0 ADR or scheduled release found |

## Decision discipline

Treat competitive advantage and learning outcomes as hypotheses. Do not silently change accepted scope. Revisions require an owner decision recorded as an ADR, with testable acceptance criteria. Separate feature implementation from product validation, and both from publication/release. See [roadmap](11_ROADMAP_AND_BACKLOG.md) and [history](15_HISTORY_AND_DECISIONS.md).

## Sources

- `decisions/ADR-013-v01-umfang-akkorde-und-midi-export.md`
- `decisions/ADR-007-audio-nur-dateiexport-v01.md`
- `docs/product/PRODUCT_STRATEGY_AND_MVP.md`
- `docs/product/V1.0.0_PRODUCT_CONTRACT.md`
- `docs/product/LEARNING_AND_EXPERIENCE.md`
