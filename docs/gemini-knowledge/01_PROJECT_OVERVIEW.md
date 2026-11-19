# STEPS Project Overview

**Baseline commit:** `00f4d5b9079575260c9f26d6d0f3305ab15e241a`
**Audit date:** 2026-11-19
**Status:** IMPLEMENTED — a Python music-theory core, desktop prototype, project-storage services, and MIDI export exist; product acceptance remains PARTIAL.
**Status key:** IMPLEMENTED = exists; TESTED = automated evidence; PARTIAL = incomplete; PLANNED = future; BLOCKED = decision or dependency; HISTORICAL = dated state; NOT_EVIDENCED = insufficient evidence.

## Project in one paragraph

STEPS is an open-source music-theory project focused on creating chord progressions, exploring harmonic context, and exporting Standard MIDI Files. At this snapshot, it includes Python APIs in `src/steps/`, an application/CLI in `app/`, reviewed learning examples under `knowledge/`, schemas, tests, and design assets. It is not evidenced as a complete, installer-backed, platform-accepted desktop product.

## Version boundaries

| Identifier | Meaning | Evidence status |
|---|---|---|
| `v0.1.0` | Only release tag reported at this snapshot | IMPLEMENTED release/tag; not proof of current release readiness |
| `0.2.0-dev` / `0.2.0.dev0` | Development version in `VERSION` and `pyproject.toml` | IMPLEMENTED metadata; not a published release |
| `schema_version` | Project-file format version, separate from app version | IMPLEMENTED in `src/steps/storage/project_io.py` |
| V6.6/V6.7 | Historical research-library generations | HISTORICAL; never treat as app version or product test evidence |

## Product and research boundaries

The accepted [ADR-013](../../decisions/ADR-013-v01-umfang-akkorde-und-midi-export.md) defines v0.1 around chord work and MIDI file export, with drum editing deferred to app v2. The broader research archive, corpora and source files are not equivalent to approved product learning content. The proposed 1.0 scope in `docs/product/V1.0.0_PRODUCT_CONTRACT.md` is not an approved release commitment.

## What this overview does not assert

It does not claim user-study validation, full platform or accessibility acceptance, independent DAW interoperability, complete rights clearance, or a signed installer. Consult [feature inventory](05_FEATURE_INVENTORY.md), [risks](12_KNOWN_ISSUES_AND_RISKS.md), and [final audit](21_FINAL_AUDIT_REPORT.md).

## Source evidence

- [Root README](../../README.md) — project description, current capabilities, known limits.
- [Implementation status](../IMPLEMENTATION.md) — code-level behavior and constraints.
- [Project overview](../project/PROJECT_OVERVIEW.md) — broader historical context with dated status boundaries.
- [1.0 readiness proposal](../product/V1.0.0_PRODUCT_CONTRACT.md) — target and gap matrix, explicitly not approved.
