# STEPS Gemini Knowledge Pack — Index

**Baseline commit:** `00f4d5b9079575260c9f26d6d0f3305ab15e241a`
**Audit date:** 2026-11-19
**Status:** IMPLEMENTED — documentation package for a fixed repository snapshot; not product or release approval.
**Status key:** IMPLEMENTED = exists; TESTED = automated evidence; PARTIAL = incomplete; PLANNED = future; BLOCKED = decision or dependency; HISTORICAL = dated state; NOT_EVIDENCED = insufficient evidence.

## Purpose and scope

This English-first pack is a standalone orientation and source map for Gemini sessions working on STEPS. It describes repository evidence at the baseline above. It supplements, but does not replace, canonical contracts, source files, tests, accepted ADRs, or human music/legal review. The pack does not imply that planned work has shipped.

Read [Gemini instructions](19_GEMINI_INSTRUCTIONS.md), then this index and the topic most relevant to the task. [Gemini usage guide](18_GEMINI_USAGE_GUIDE.md) and [update/change map](20_UPDATE_AND_CHANGE_MAP.md) explain safe maintenance. [Final audit](21_FINAL_AUDIT_REPORT.md) records known verification boundaries.

## Status vocabulary

- **IMPLEMENTED** — behavior or artifact exists in the baseline checkout.
- **TESTED** — the exact behavior has an identified automated test or recorded run; this does not imply human acceptance.
- **PARTIAL** — some implementation or evidence exists, with material gaps.
- **PLANNED** — described as future work or proposal, not delivered.
- **BLOCKED** — cannot proceed without a decision, dependency, permission, or evidence.
- **HISTORICAL** — true only of a dated earlier project state; not current product status.
- **NOT_EVIDENCED** — the reviewed baseline does not provide sufficient evidence. This is not proof of absence.

Apply statuses to each claim, not to an entire project indiscriminately. Report implementation, tests, manual acceptance, publication, and release separately.

## Documents

| File | Subject |
|---|---|
| [01 Project overview](01_PROJECT_OVERVIEW.md) | Identity, scope, maturity, version boundaries |
| [02 Product strategy](02_PRODUCT_STRATEGY.md) | Accepted v0.1 direction and proposed 1.0 hypothesis |
| [03 System architecture](03_SYSTEM_ARCHITECTURE.md) | Runtime boundaries and data flow |
| [04 Music theory engine](04_MUSIC_THEORY_ENGINE.md) | Theory model, notation, interpretation limits |
| [05 Feature inventory](05_FEATURE_INVENTORY.md) | Implemented/tested/partial/planned feature matrix |
| [06 Data models and interfaces](06_DATA_MODELS_AND_INTERFACES.md) | Project data, timeline, APIs, schemas |
| [07 User experience](07_USER_EXPERIENCE.md) | Desktop interactions and acceptance gaps |
| [08 Internationalization](08_INTERNATIONALIZATION.md) | English/German UI and notation independence |
| [09 Development and build](09_DEVELOPMENT_AND_BUILD.md) | Python setup, package and build limits |
| [10 Testing and quality](10_TESTING_AND_QUALITY.md) | Test inventory, commands, manual gates |
| [11 Roadmap and backlog](11_ROADMAP_AND_BACKLOG.md) | Dependency-based future work |
| [12 Known issues and risks](12_KNOWN_ISSUES_AND_RISKS.md) | Open evidence, product, platform and source risks |
| [13 Design and branding](13_DESIGN_AND_BRANDING.md) | Visual assets, tokens, provenance |
| [14 Security, license and governance](14_SECURITY_LICENSE_GOVERNANCE.md) | License scope, data handling, review authority |
| [15 History and decisions](15_HISTORY_AND_DECISIONS.md) | Release history and accepted decisions |
| [16 Glossary](16_GLOSSARY.md) | Project and music terminology |
| [17 Source evidence register](17_SOURCE_EVIDENCE_REGISTER.md) | Claim-to-repository evidence map |
| [18 Gemini usage guide](18_GEMINI_USAGE_GUIDE.md) | Grounded, bounded use of this pack |
| [19 Gemini instructions](19_GEMINI_INSTRUCTIONS.md) | Operational rules for Gemini |
| [20 Update and change map](20_UPDATE_AND_CHANGE_MAP.md) | Upkeep and affected-file mapping |
| [21 Final audit report](21_FINAL_AUDIT_REPORT.md) | Snapshot, tests, benchmarks, NOT_RUN items |
| [German summary](ZUSAMMENFASSUNG_DE.md) | German overview; separate from English canonical pack |

## Authority and change boundary

Repository-wide authority remains `AGENTS.md`; technical, product, and governance detail is owned by the relevant `docs/engineering/`, `docs/product/`, and `docs/governance/` documents. Accepted decisions live in `decisions/`. The source of implementation truth is code and tests, not this pack. Preserve German historical originals; do not overwrite or silently translate them.

Primary entry points: [root README](../../README.md), [implementation status](../IMPLEMENTATION.md), [continuous maintenance contract](../governance/CONTINUOUS_MAINTENANCE.md), [source tree](../../src/steps/), and [test instructions](../../tests/README.md).
