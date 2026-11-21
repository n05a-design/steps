# Open Work Instructions Protocol

## 1. Single Canonical Authority
All active STEPS tasks and required owner decisions belong in the versioned repository file `docs/operations/OFFENE_ARBEITSAUFFORDERUNGEN.md`. The helper resolves it relative to its own location, independent of the current working directory; do not configure an external register path.

This follows the Glide project's single-backlog model. GitHub issues are linked evidence/discussion for register entries, not a second authority for task status. Dated snapshots and plans are historical context, not active task lists. There must be no competing active register.

The former external register was not available in the 2026-11-19 audit. The dated snapshot retains legacy OA-0001–OA-0033, but its statuses are not silently promoted to current truth. Reconcile those IDs against current evidence in a tracked task; preserve unresolved cases as blocked.

## 2. Identification Guidelines
Work instructions can be:
- **EXPLICIT**: Directly requested by the user, an ADR, an issue, or a trusted project `TODO:` comment whose authority was reviewed.
- **INFERRED**: Derived from an unfulfilled architectural requirement, an engineering gap, or an unresolved conflict in documentation.

The extractor reports document text as `CANDIDATE_FROM_DOCUMENT`. A reviewer assigns the origin of a register entry after checking the source.

## 3. Lifecycle States
- `OPEN`: Task is defined and pending execution.
- `IN_PROGRESS`: Actively being worked on in an isolated branch.
- `BLOCKED`: Precondition not met.
- `OWNER_DECISION_REQUIRED`: Requires explicit decision from the Project Owner (e.g. ADRs, copyright choices).
- `DONE_UNVERIFIED`: Implementation complete with evidence or review still pending.
- `DONE_VERIFIED`: Record the full commit SHA under **Commit**, the executed check under **Prüfung**, its review or test evidence under **Abnahmebeleg**, and the criterion under **Abnahmekriterien**.
- `SUPERSEDED`: Replaced by a more comprehensive task.
- `NOT_APPLICABLE`: The task does not apply to the current scope. Record exactly one non-placeholder reason in the **Begründung** field.
