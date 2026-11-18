# GitHub Projects v2 Integration Specification

**Status:** Owner-action specification. No GitHub Project currently exists.

## Required owner decision

The owner must create or select a Projects v2 board. Repository files must not create or
claim a Project through write-side automation.

## Recommended fields

- Workstream: Repository Truth, Desktop, Localization, GitHub Operations, Knowledge, Packaging
- Priority: P0/P1/P2
- Status: Backlog, Ready, In Progress, In Review, Blocked, Done
- Evidence state: PLANNED, IMPLEMENTED, TESTED, REVIEWED, RELEASED, BLOCKED
- Base SHA
- Release gate
- Owner decision

## Recommended views

1. **Development:** status and priority.
2. **Roadmap:** target state and dependencies.
3. **Knowledge Quality:** source/rights/domain-review blockers.
4. **Localization:** locale coverage and human-review status.
5. **Release Readiness:** tests, docs, security, packaging, platform, and owner sign-off.

## Automation boundaries

- Never overwrite manually curated owner/field values.
- Use read-only repository automation until permissions and field IDs are approved.
- Do not infer PR merge or release success from a board state.
- Issue-to-Project mapping remains a separate, owner-authorized operation.
