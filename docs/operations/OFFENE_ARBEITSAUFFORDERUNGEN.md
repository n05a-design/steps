# STEPS Open Work Register

**Authority:** This is the single active, versioned register for STEPS tasks and owner decisions.
**Effective date:** 2026-11-21.
**Source baseline:** GitHub `main` at `3a5db64b6131806c432b7b38dca60680c5a57d9b` (previous baseline `e2faf276adf6d65caf81fe28f38521a176e0c283`).
**Operating model:** One repository backlog, following Glide's single-plan model. GitHub issues provide linked discussion/evidence; this register is the active status authority.

## Migration boundary

The former external register was not configured or available during the audit. The dated [`OFFENE_ARBEITSAUFFORDERUNGEN_SNAPSHOT.md`](OFFENE_ARBEITSAUFFORDERUNGEN_SNAPSHOT.md) preserves 33 legacy IDs, but it does not establish their current status. Its three `DONE_VERIFIED` entries also lack the evidence fields required by the current validator. Do not silently import those statuses or infer completion; reconcile them under OA-0034.

New active IDs continue after the legacy range. Dated plans and audit reports remain historical evidence, not parallel active task lists.

## Active tasks

### OA-0034: Reconcile legacy task IDs with current evidence
- **Kategorie:** Register migration · **Status:** `BLOCKED` · **Ursprung:** EXPLICIT
- **Beschreibung:** Reconcile legacy OA-0001–OA-0033 from the dated snapshot against current code, GitHub issues, and human decisions. The prior external register was unavailable, so its possible updates cannot be recovered from this audit.
- **Quellen:** [Historical register snapshot](OFFENE_ARBEITSAUFFORDERUNGEN_SNAPSHOT.md); [open STEPS issues](https://github.com/n05a-design/steps/issues)
- **Blocker:** No source copy of the former external register; legacy statuses are stale and three historical `DONE_VERIFIED` entries lack required evidence.
- **Abnahmekriterien:** Every legacy ID is either mapped to a current register item/issue, verified with commit-level evidence, or explicitly retained as historical/superseded. Do not duplicate issue work or infer completion.

### OA-0035: Establish the versioned repository register as canonical
- **Kategorie:** Governance / Dokumentation · **Status:** `DONE_VERIFIED` · **Ursprung:** EXPLICIT
- **Beschreibung:** Implement the owner-directed Glide-style authority model: a single versioned STEPS task register in this repository, with the old external path contract removed from active tooling.
- **Quellen:** User decision on 2026-11-19; [register protocol](../../.agents/skills/steps-knowledge-curation/references/work_instructions_protocol.md)
- **Commit:** `5c3e829d53e8f2cfc609eddd0d3c597c862a9698`
- **Prüfung:** `python3 -B -m unittest discover -s .agents/skills/steps-knowledge-curation/tests/ -q` — 40 tests passed; `python3 .agents/skills/steps-knowledge-curation/scripts/validate_register.py` — 7 tasks, 0 errors.
- **Abnahmebeleg:** PR [#209](https://github.com/n05a-design/steps/pull/209) merged; `test_default_register_is_repository_canonical_and_ignores_legacy_env` passed; the dated snapshot is unchanged since the migration.
- **Abnahmekriterien:** Default helpers resolve this file independent of the working directory and ignore the legacy environment variable; skill and operations documentation identify it as the sole active authority; validation and recovery tests pass; dated snapshots remain unchanged.

### OA-0036: Complete repository truth and documentation sync
- **Kategorie:** Dokumentation / Governance · **Status:** `OPEN` · **Ursprung:** EXPLICIT
- **Beschreibung:** Finish the remaining repository-truth and documentation work without treating merged implementation or passing tests as owner acceptance.
- **Quellen:** [Issue #149](https://github.com/n05a-design/steps/issues/149); [implementation status](../IMPLEMENTATION.md); [roadmap](../roadmap/ROADMAP_AND_RESOURCE_PLAN.md)
- **Fortschritt 2026-11-21:** The roadmap, implementation status, 1.0 readiness matrix and project overview are synchronized to `3a5db64` (875 tests). A relative Markdown link check now runs in CI. GitHub epics and release labels are tracked under OA-0041.
- **Abnahmekriterien:** Current public claims and linked GitHub status agree with observed evidence; stale issue notes are either corrected or explicitly retained as history; required owner actions remain open until approved.

### OA-0037: Close knowledge-base provenance and review gaps
- **Kategorie:** Wissensbasis / Provenienz · **Status:** `OPEN` · **Ursprung:** EXPLICIT
- **Beschreibung:** Continue source, rights, graph, and domain review only with provenance-bound evidence. The benchmark rechecked on the desktop evolution branch reports 92 passed, 0 failed and 27 pending (15 manual evidence checks and 12 coach assessments).
- **Quellen:** [Issue #150](https://github.com/n05a-design/steps/issues/150); [open research gaps](../../research/gaps/OPEN_GAPS.md)
- **Abnahmekriterien:** Each published claim has an allowed source, locator, scope, and recorded review state; pending cases are not promoted to pass without evidence and required human review.

### OA-0038: Complete desktop MVP acceptance
- **Kategorie:** Produkt / Desktop · **Status:** `OPEN` · **Ursprung:** EXPLICIT
- **Beschreibung:** Continue the desktop workflow toward owner-approved MVP acceptance. The [native widget workflow](../../tests/native_ui/README.md) now covers the library, recommendations, style preview/application, MIDI options and save/reopen. The local macOS development bundle has a reproducible build recipe. Reproducible DAW fixtures and a manual import protocol exist (PR #240), and the local macOS bundle build is logged (PR #262). The 875-test pass at `main` `3a5db64` and ADR-017 export checks do not replace independent DAW, native accessibility, platform, installer, or user acceptance.
- **Quellen:** [Issue #151](https://github.com/n05a-design/steps/issues/151); [1.0 readiness contract](../product/V1.0.0_PRODUCT_CONTRACT.md); [handover audit](../handover/MASTER_UEBERGABE_2026-11-19.md)
- **Abnahmekriterien:** Required human and platform checks are recorded for the approved scope; DAW imports are verified independently; owner decisions and release boundaries remain explicit.

### OA-0039: Complete independent localization acceptance
- **Kategorie:** Lokalisierung / Accessibility · **Status:** `OPEN` · **Ursprung:** EXPLICIT
- **Beschreibung:** Complete independent English/German translation and native accessibility/platform review. The recommendation presentation is covered in all four UI-language and notation combinations. Independent translation and accessibility reviewers still need to assess the visible workflow.
- **Quellen:** [Issue #154](https://github.com/n05a-design/steps/issues/154); [internationalization contract](../engineering/INTERNATIONALIZATION.md)
- **Abnahmekriterien:** Translation review and supported-platform/accessibility acceptance are recorded separately from automated test status; UI language remains independent of `INT`/`DE` notation.

### OA-0040: Verify OneDrive cloud synchronization
- **Kategorie:** Projektablage / Owner action · **Status:** `OWNER_DECISION_REQUIRED` · **Ursprung:** EXPLICIT
- **Beschreibung:** Confirm through the OneDrive client or another authoritative sync indicator that the approved project workspace and pushed branch have completed cloud synchronization. A local path under OneDrive is placement evidence only.
- **Quellen:** [handover audit](../handover/MASTER_UEBERGABE_2026-11-19.md); current project worktree is under the configured OneDrive project tree.
- **Abnahmekriterien:** Record the verified sync result and any pending/conflict state without copying or deleting files to force synchronization.

### OA-0041: Align GitHub labels and epics with the repository state
- **Kategorie:** GitHub / Governance · **Status:** `DONE_UNVERIFIED` · **Ursprung:** EXPLICIT
- **Beschreibung:** Create the label taxonomy in [`.github/labels.yml`](../../.github/labels.yml), including the categories that [`release.yml`](../../.github/release.yml) expects, apply it to issue templates and open epics, and record the current state in issues #149, #150, #151 and #154.
- **Quellen:** User request on 2026-11-21; [GitHub and CI overview](../../.github/GITHUB_UND_CI.md); [roadmap §0](../roadmap/ROADMAP_AND_RESOURCE_PLAN.md#0-aktueller-stand-und-nächste-etappen-21112026)
- **Fortschritt 2026-11-21:** All 23 taxonomy labels were created or updated with `gh label create --force`; epics #149, #150, #151 and #154 carry epic/area/state labels and a dated status comment. Independent review of the label scheme and PR #266 is pending.
- **Abnahmekriterien:** Every label in the versioned taxonomy exists on GitHub; issue templates reference only existing labels; each open epic carries its area and epic labels and a dated status comment; no issue is closed without owner acceptance.

### OA-0042: Protect `main` with required checks and review
- **Kategorie:** GitHub / Owner action · **Status:** `OWNER_DECISION_REQUIRED` · **Ursprung:** EXPLICIT
- **Beschreibung:** On 2026-11-21 `main` had no classic branch protection, and the only active ruleset (`basic`) enabled Copilot code review. Pull requests, the CI status checks and code-owner approval are therefore not enforced merge gates.
- **Quellen:** `gh api repos/n05a-design/steps/rulesets`; [CODEOWNERS](../../.github/CODEOWNERS); [continuous maintenance](../governance/CONTINUOUS_MAINTENANCE.md)
- **Abnahmekriterien:** The owner records the chosen required checks, review and code-owner rules for `main`; the observed GitHub setting is cited with date and the agent contract's no-direct-merge rule is enforced by GitHub.
