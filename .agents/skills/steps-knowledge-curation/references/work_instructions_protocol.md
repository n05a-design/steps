# Open Work Instructions Protocol

## 1. Single Canonical Authority
All open tasks, required decisions, and engineering action items in STEPS must be registered in:
`%LOCALAPPDATA%\StepsKnowledge\OFFENE_ARBEITSAUFFORDERUNGEN.md`

There must be NO competing active task lists.

## 2. Identification Guidelines
Work instructions can be:
- **EXPLICIT**: Directly requested by the user, an ADR, an issue, or a `TODO:` comment.
- **INFERRED**: Derived from an unfulfilled architectural requirement, an engineering gap, or an unresolved conflict in documentation.

## 3. Lifecycle States
- `OPEN`: Task is defined and pending execution.
- `IN_PROGRESS`: Actively being worked on in an isolated branch.
- `BLOCKED`: Precondition not met.
- `OWNER_DECISION_REQUIRED`: Requires explicit decision from the Project Owner (e.g. ADRs, copyright choices).
- `DONE_VERIFIED`: Task completed and verified by tests and commit evidence.
- `SUPERSEDED`: Replaced by a more comprehensive task.
