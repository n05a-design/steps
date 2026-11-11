# STEPS Semantic Identity Lock Architecture Report (Phase 4.16)

**Date**: 2026-11-11  
**Phase**: STEPS Phase 4.16  
**Topic**: Full Semantic Identity Locking, Deterministic Hashing, Field Classification, and Migration Governance  
**Status**: **100% IMPLEMENTED & VERIFIED**

---

## 1. Executive Summary & Defect Remediation

In Phase 4.15, an initial `verify_identity_lock()` function was introduced in `scripts/verify_reference_integrity.py`. However, an independent technical audit revealed that for Golden Reference Cases, it merely compared the textual `title`, ignoring `input_params`, `expected_output`, musical domain, and the pre-computed `semantic_hash` field. Furthermore, an overly broad condition in the migration check allowed historical and migrated cases to bypass hash verification entirely.

Phase 4.16 completely remediated these defects:
1. **Full Identity Locking**: Every entity across the repository's 6 knowledge categories is validated against its full structural definition.
2. **Deterministic Canonical Hashing**: Canonical serialization ensures that changes to any identity-defining field alter the entity's SHA-256 hash.
3. **Live Recomputation & Verification**: `verify_reference_integrity.py` recomputes the canonical hash directly from active Markdown tables, CSVs, and JSON files and strictly asserts equality with the baseline.
4. **Controlled Migration Authority**: Only explicit records with `action == 'CONTROLLED_CORRECTION'` in `REFERENCE_ID_MIGRATION_REGISTER.csv` can authorize a legitimate correction. All other mutations fail-closed.

---

## 2. Field Classification Taxonomy

To ensure music knowledge can be legitimately refined without permitting silent semantic corruption, fields are classified into five distinct tiers:

| Tier | Classification | Description | Mutability Rule |
|---|---|---|---|
| **Tier 1** | `IDENTITY_DEFINING` | Core musical properties: Entity ID, mathematical formula, input parameters, expected result, pitch classes, tempo, meter. | **Strictly Immutable**. Any change mutates the `semantic_hash` and halts CI unless authorized via `CONTROLLED_CORRECTION`. |
| **Tier 2** | `NORMATIVE_CONTENT` | Taxonomic classification: Knowledge Domain (`M01`..`M12`), Test Class, Relation Type, Epistemic status. | **Strictly Governed**. Must match canonical schemas and baseline definitions. |
| **Tier 3** | `CORRECTABLE_ERROR` | Historical typographical errors or imprecise wording. | **Migration Required**. Requires bidirectional mapping, audit justification, and explicit sign-off in `REFERENCE_ID_MIGRATION_REGISTER.csv`. |
| **Tier 4** | `DESCRIPTIVE_METADATA` | Contextual notes, commentary, pedagogical suggestions, stylistic tags. | **Evolutive**. May be enhanced across research phases provided identity fields remain untouched. |
| **Tier 5** | `PROVENANCE` | Historical origin: First attestation phase, source citation, evidence path, validation status. | **Preservation-First**. Must trace back to verified commit or research artifact. |

---

## 3. Canonical Hash Formulas by Entity Type

Each entity's `semantic_hash` is computed deterministically as `SHA256(JSON(sort_keys=True, ensure_ascii=False))`:

### 3.1 Chord Progressions (`PROG-001` .. `PROG-027`)
```python
canonical_dict = {
    'id': pid.strip(),
    'name': name.strip().lower(),
    'domain': domain.strip(),
    'harmonic_structure': degrees.strip('`* '),
    'standard_example': example.strip('`* ')
}
```

### 3.2 Drum Patterns (`PAT-001` .. `PAT-031`)
```python
canonical_dict = {
    'id': did.strip(),
    'name': name.strip().lower(),
    'domain': 'M08',
    'tempo': tempo.strip(),
    'meter_and_feel': meter_feel.strip()
}
```

### 3.3 Piano Practice Modules (`P01` .. `P19`)
```python
canonical_dict = {
    'id': pid.strip(),
    'title': title.strip().lower(),
    'domain': 'M10',
    'didactic_goal': goal.strip(),
    'musical_focus': focus.strip()
}
```

### 3.4 Concept Relations (`CR-001` .. `CR-094`)
```python
canonical_dict = {
    'id': rid.strip(),
    'source_id': src.strip(),
    'target_id': tgt.strip(),
    'relation_type': rel_type.strip(),
    'domain_scope': domain_scope.strip()
}
```

### 3.5 Golden Reference Cases (`REF-0001` .. `REF-0198`)
```python
canonical_dict = {
    'id': cid.strip(),
    'title': title.strip().lower(),
    'domain': domain.strip(),
    'input_params': json.dumps(input_params, sort_keys=True, ensure_ascii=False),
    'expected_output': json.dumps(expected_output, sort_keys=True, ensure_ascii=False)
}
```

---

## 4. Controlled Migration Governance Procedure

When a music theory finding requires an authentic correction (e.g., repairing an incorrect enharmonic spelling or updating a tuning ratio):

1. **Rule of Non-Reuse**: New independent musical concepts must **never** overwrite or hijack an existing ID. They receive a new, unallocated ID.
2. **Documented Migration Entry**: The correction must be registered in `knowledge/research/REFERENCE_ID_MIGRATION_REGISTER.csv`:
   - `original_id`: The ID being corrected.
   - `migrated_id`: Same ID (for in-place correction) or new ID (for reassignments).
   - `migration_reason`: Comprehensive musicological justification citing authoritative sources.
   - `action`: `CONTROLLED_CORRECTION`.
   - `status`: `ACTIVE`.
3. **Audit Trail**: The correction is documented in `knowledge/research/MUSICAL_CORRECTION_REPORT.md` and included in the phase session deliverables.

---

## 5. Verification Matrix Summary

Running `tests/test_reference_integrity.py` executes 19 isolated tests:
- 1 Canonical baseline check (27 PROG, 31 PAT, 19 P, 94 CR, 198 REF verified 100%).
- 15 Mandatory negative mutation tests (verifying fail-closed detection of modified outputs, corrupted inputs, swapped contexts, deleted objects, and hijacked IDs).
- 3 Structural table, CSV, and mirror synchronization tests.

All 19 tests pass in 3.2 seconds.
