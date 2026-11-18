# STEPS Project Schema Migration

**Status:** Implemented compatibility contract for project loading.

Project files use `schema_version` separately from the STEPS application and package versions. The loader is intentionally conservative:

- A malformed schema version is rejected.
- A higher major version is rejected as unsupported.
- The 0.x compatibility migration is identified as `MIG-001 0.x-to-1.0.0`.
- 1.x project fields may be normalized only for documented defaults.
- Missing required project identity or title is rejected; a title is never invented.
- Existing `load_project()` callers keep the `Project` return type.
- `load_project_with_status()` adds `migrations`, `migrated`, backup recovery status, and backup path.

The current migration IDs are:

| ID | Compatibility change |
|---|---|
| `MIG-001` | Mark a 0.x project as migrated to the 1.0 project contract |
| `MIG-002` | Add a missing project ID |
| `MIG-003` | Add the current app version |
| `MIG-004` | Add the default `INT` notation convention |
| `MIG-005` | Normalize missing or invalid metadata to an object |
| `MIG-006` | Add missing PPQ, meter, tempo, and tempo-point defaults |
| `MIG-007` | Normalize missing or invalid tracks to an empty array |

Loading a migration does not overwrite the source file. A later save writes the normalized project in the current schema. Adding a new migration requires a new stable migration ID, tests, and a product-level compatibility note.
