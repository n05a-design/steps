# Roadmap and Backlog

**Baseline commit:** `00f4d5b9079575260c9f26d6d0f3305ab15e241a`
**Audit date:** 2026-11-19
**Status:** PARTIAL — v0.1 direction is accepted; future milestones are proposed, not scheduled.
**Status key:** IMPLEMENTED = exists; TESTED = automated evidence; PARTIAL = incomplete; PLANNED = future; BLOCKED = decision or dependency; HISTORICAL = dated state; NOT_EVIDENCED = insufficient evidence.

## Direction and dependencies

1. Maintain the implemented chord/progression and project workflows.
2. Close user-facing and platform acceptance gaps, including localization review, accessibility, project recovery and release delivery.
3. Verify MIDI interoperability in independent applications, beyond automated parser/writer tests.
4. Extend source-bound learning content only with provenance, rights and human review.
5. Consider drums in app v2 under accepted [ADR-013](../../decisions/ADR-013-v01-umfang-akkorde-und-midi-export.md); avoid claiming an implementation from research models alone.

The historical and proposed dependency plan in `docs/roadmap/ROADMAP_AND_RESOURCE_PLAN.md` is not a schedule or owner-approved release plan. The 1.0 target in `docs/product/V1.0.0_PRODUCT_CONTRACT.md` is also a proposal.

## Current gates

| Work | Status | Completion evidence needed |
|---|---|---|
| 1.0 scope and support policy | BLOCKED | owner-approved ADR |
| Native UX/accessibility | PLANNED | recorded platform-specific review |
| MIDI interoperability | PARTIAL | versioned import checks in independent DAWs |
| Source knowledge expansion | PARTIAL | rights-cleared, reviewed, cited claims and test cases |
| Desktop installer/release process | NOT_EVIDENCED | reproducible artifacts, notices, install/upgrade acceptance |
| Drum editor | PLANNED | future scope decision and user workflow |

## Backlog maintenance

Consult existing issues/epics and canonical roadmaps before creating new work. Keep historical IDs and snapshots. Each proposal should identify owner, dependency, acceptance criteria, risk and exact evidence needed. Never convert “code exists” to “feature accepted” or close an issue without its criteria. See `docs/governance/CONTINUOUS_MAINTENANCE.md`.
