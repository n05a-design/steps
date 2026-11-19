# Source and Evidence Register

**Baseline commit:** `00f4d5b9079575260c9f26d6d0f3305ab15e241a`
**Audit date:** 2026-11-19
**Status:** PARTIAL — repository source paths are mapped; this is not a complete per-claim citation or rights register.
**Status key:** IMPLEMENTED = exists; TESTED = automated evidence; PARTIAL = incomplete; PLANNED = future; BLOCKED = decision or dependency; HISTORICAL = dated state; NOT_EVIDENCED = insufficient evidence.

## Evidence matrix

| Claim group | Primary evidence paths | What it supports | Does not establish |
|---|---|---|---|
| Product state | `README.md`, `docs/IMPLEMENTATION.md` | Current product/code claims and named limitations | User satisfaction or release acceptance |
| Product decisions | `decisions/DECISION_REGISTER.md`, `decisions/ADR-013-v01-umfang-akkorde-und-midi-export.md` | Accepted scope and decision record | That every decision is fully implemented |
| Architecture | `docs/architecture/ARCHITECTURE_OVERVIEW.md`, `src/steps/`, `app/` | Code organization and documented data flow | Production-grade platform support |
| Music model | `docs/engineering/MUSIC_DOMAIN_AND_MIDI.md`, `src/steps/theory/`, `tests/test_notation_contract.py` | Music distinctions and implemented tested contracts | Universal theory consensus |
| Data and storage | `docs/engineering/DATA_STORAGE_AND_PORTABILITY.md`, `src/steps/storage/`, `schemas/` | Storage approach, schemas, compatibility boundaries | Every migration/recovery case |
| Internationalization | `docs/engineering/INTERNATIONALIZATION.md`, `app/i18n.py`, `app/locales/` | Locale implementation and requirements | Human translation approval |
| Quality | `tests/README.md`, `.github/workflows/python-tests.yml` | Test commands and configured CI | Successful result on every runner in this audit |
| Knowledge | `knowledge/benchmark/cases.json`, `knowledge/benchmark/PILOT_ABNAHME.md`, `knowledge/sources/` | Benchmark cases and reviewed pilot statements | Whole library approved or rights-cleared |
| Licensing/security | `LICENSE`, `SECURITY.md`, `docs/governance/RIGHTS_SECURITY_AND_RELEASE.md` | Policy and repository-level license | Rights to each third-party file |
| Design | `design/`, `app/assets/brand/`, `decisions/ADR-004-lizenz-und-marke.md` | Present design files and brand policy | Trademark clearance or full accessibility |
| History/archive | `archive/INDEX.md`, `docs/project/PROJECT_OVERVIEW.md` | Dated history and archive routes | Current product features |

## Evidence types

Use **code** for implementation, **test** for automated behavior, **decision** for accepted owner direction, **human review** for expertise/translation/rights, and **release** for published artifacts. A document claim alone is not implementation proof. Benchmark inventory and pass counts must be linked to the exact benchmark data and run.

## Provenance and open questions

This pack's claims are bounded by baseline `00f4d5b9079575260c9f26d6d0f3305ab15e241a`. It does not record SHA-256 for each repository file or claim-specific external source locator; that work remains PARTIAL. The curated source registry is distinct from historical books, corpora, scraped pages and archives. For new factual claims, add source IDs/locators using the existing knowledge curation process, preserve rights status, and ask for domain review where necessary.
