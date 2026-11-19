# History and Accepted Decisions

**Baseline commit:** `00f4d5b9079575260c9f26d6d0f3305ab15e241a`
**Audit date:** 2026-11-19
**Status:** IMPLEMENTED — decision records and release history exist; older records remain HISTORICAL where dated.
**Status key:** IMPLEMENTED = exists; TESTED = automated evidence; PARTIAL = incomplete; PLANNED = future; BLOCKED = decision or dependency; HISTORICAL = dated state; NOT_EVIDENCED = insufficient evidence.

## Snapshot history

The immutable repository baseline for this pack is `00f4d5b9079575260c9f26d6d0f3305ab15e241a`, identified as merge PR #186. The only supplied release/tag is `v0.1.0`. Prior docs may cite older baselines; preserve those as historical evidence rather than rewriting the past.

## Accepted decisions relevant to current work

| ADR | Decision | Status/limit |
|---|---|---|
| ADR-001 | One application root with two work areas | Accepted; see `decisions/ADR-001-ein-fenster-zwei-bereiche.md` |
| ADR-003 | Reuse only shell/infrastructure, with provenance | Accepted; not authorization to copy arbitrary Glide code |
| ADR-004 | MPL-2.0 code; own knowledge-data license policy; third-party status preserved | Accepted; not per-file rights clearance |
| ADR-006 | JSON project format with integer `schema_version` | Accepted; not a promise that every migration case is accepted |
| ADR-007 | v0.1 file export only, no in-app audio playback | Accepted |
| ADR-013 | v0.1 chords + MIDI export; drums in app v2; producers learn while producing | Accepted |
| ADR-014 | Preserve perspectives and contextual interpretation | Accepted conceptual direction |
| ADR-015/016 | Core interval/voicing/notation contracts and altered-dominant semantics | Accepted decisions; implementation status must be checked separately |
| ADR-017 | MIDI export settings for v0.1 | Accepted specification; acceptance evidence is separate |

The full register is `decisions/DECISION_REGISTER.md`. Decision acceptance does not mean all downstream code, tests, product, or human review is complete.

## Historical preservation

Maintain old German originals and archive snapshots. Do not replace them with English summaries or silently change old status claims. New documentation should link dated historical material and state its own snapshot. V6.6/V6.7 are research archive versions, not app releases. See `archive/INDEX.md`, `docs/project/PROJECT_OVERVIEW.md`, and `docs/governance/DOCUMENTATION_STATUS_POLICY.md`.
