# Update Mechanism and Change Map

**Baseline commit:** `00f4d5b9079575260c9f26d6d0f3305ab15e241a`
**Audit date:** 2026-11-19
**Status:** IMPLEMENTED — pack checker and CI gate are provided; periodic content review remains required.
**Status key:** IMPLEMENTED = exists; TESTED = automated evidence; PARTIAL = incomplete; PLANNED = future; BLOCKED = decision or dependency; HISTORICAL = dated state; NOT_EVIDENCED = insufficient evidence.

## Update process

1. Record the new baseline SHA, audit date, branch and clean/dirty status.
2. Inspect code, tests, accepted ADRs, release tags, knowledge cases, design and governance; prefer direct repository evidence.
3. Update affected pack pages and evidence register. Preserve unchanged German historical sources.
4. Recalculate reported test and benchmark inventory/results from actual commands or documented evidence.
5. Run `python -B scripts/check_gemini_knowledge_pack.py --check`, relevant tests and link review.
6. Review the diff for unexpected deletion, app-code change, unsupported claims, rights exposure and mismatched version axes.
7. Record manual/owner/legal/music/translation checks as NOT_RUN or NOT_EVIDENCED when not performed.

The script pins the baseline commit and date in the pack metadata, checks mandatory files, relative Markdown links, placeholder markers, and all full commit SHAs in the pack for consistency. Update the script's expected SHA/date and every document's evidence together when intentionally rebasing this pack.

## Change map

| Repository change | Update these pack files |
|---|---|
| Product scope / accepted ADR | `02_PRODUCT_STRATEGY.md`, `05_FEATURE_INVENTORY.md`, `11_ROADMAP_AND_BACKLOG.md`, `15_HISTORY_AND_DECISIONS.md`, `17_SOURCE_EVIDENCE_REGISTER.md` |
| Architecture or data model | `03_SYSTEM_ARCHITECTURE.md`, `06_DATA_MODELS_AND_INTERFACES.md`, and affected feature/roadmap pages |
| Theory, notation, source claims | `04_MUSIC_THEORY_ENGINE.md`, `16_GLOSSARY.md`, `17_SOURCE_EVIDENCE_REGISTER.md`, plus rights/review status |
| UI or i18n | `05_FEATURE_INVENTORY.md`, `07_USER_EXPERIENCE.md`, `08_INTERNATIONALIZATION.md` |
| Build, tests, CI | `09_DEVELOPMENT_AND_BUILD.md`, `10_TESTING_AND_QUALITY.md`, `21_FINAL_AUDIT_REPORT.md` |
| Rights/security/brand | `12_KNOWN_ISSUES_AND_RISKS.md`, `13_DESIGN_AND_BRANDING.md`, `14_SECURITY_LICENSE_GOVERNANCE.md` |
| New release or history | `01_PROJECT_OVERVIEW.md`, `02_PRODUCT_STRATEGY.md`, `15_HISTORY_AND_DECISIONS.md`, audit report |
| Pack structure or Gemini workflow | `00_KNOWLEDGE_INDEX.md`, `18_GEMINI_USAGE_GUIDE.md`, `19_GEMINI_INSTRUCTIONS.md`, checker and this map |

## CI

`.github/workflows/python-tests.yml` runs the pack check in the main unit-test job. It validates documentation mechanics only, not the truth of every statement, legal rights, music theory, translations or release readiness.

## Governance references

See `docs/governance/CONTINUOUS_MAINTENANCE.md` and `docs/governance/DOCUMENTATION_STATUS_POLICY.md`.
