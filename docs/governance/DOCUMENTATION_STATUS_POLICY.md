# Documentation Status and Baseline Policy

**Status:** Active repository maintenance policy.

The repository separates historical evidence snapshots from active implementation status.

## Snapshot semantics

- A full 40-character Git SHA in an active status document is an immutable evidence snapshot.
- A snapshot proves the state described for that commit only. It does not claim that every later merge changed or preserved the feature.
- This is not an assertion that every later merge requires a documentation update.
- A later merge must not require a documentation-only PR solely because the repository HEAD moved.
- A status document changes only when code, product claims, test evidence, or a canonical status rule changes.
- Historical documents remain historically dated and are not rewritten as current truth.

## Validation

Run:

```sh
python -B scripts/check_documentation_consistency.py --check
```

The check:

- validates that referenced snapshot commits exist;
- keeps historical snapshots separate from later/current implementation status;
- does not require a historical snapshot to be an ancestor of the checked HEAD;
- validates package/development version axes;
- rejects selected README statements that contradict implemented i18n capability.

- This is a consistency gate, not an assertion that a snapshot is the latest merge.
