# Open Work Instructions Protocol

## 1. Single Canonical Authority
All open tasks, required decisions, and engineering action items in STEPS belong in the canonical register. Set `STEPS_KNOWLEDGE_REGISTER` to its absolute path. Windows falls back to `%LOCALAPPDATA%\StepsKnowledge\OFFENE_ARBEITSAUFFORDERUNGEN.md`.

There must be NO competing active task lists.

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
- `NOT_APPLICABLE`: The task does not apply to the current scope. Record the reason.
