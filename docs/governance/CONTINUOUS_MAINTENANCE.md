# Continuous Repository Maintenance Contract

**Status:** Repository operating guidance. The canonical agent authority remains the root [`AGENTS.md`](../../AGENTS.md); this document explains its repeatable review and evidence steps.

## 1. Required cross-domain review for every change

For each pull request, assess the domains below. Update only affected sources of truth; record `Not applicable` in the PR when a domain is not affected.

| Domain | Review question | Evidence or update |
|---|---|---|
| Product behavior | Did the actual user-visible capability or its limits change? | Update `docs/IMPLEMENTATION.md`, user docs, and affected roadmap/issue status. |
| UI/CLI language | Did a user-facing string, error, help entry, accessibility label, or public message change? | Add/update all required `en`/`de` catalog entries and run catalog parity checks once the i18n system exists. |
| Music knowledge | Did a claim, concept, interpretation, example, or source status change? | Preserve source IDs, locators, scope, rights, and independent domain-review state; use the knowledge curation workflow. |
| Architecture/API/schema | Did an import, public function, project format, enum, setting, or compatibility contract change? | Update the canonical engineering contract, generated reference, schema/migration tests, and ADR where a decision is required. |
| Documentation | Did instructions, screenshots, setup, supported platforms, or status change? | Update the relevant canonical document and its language/status metadata; do not create a competing register. |
| Issue/roadmap | Is the tracked objective, dependency, or completion state now inaccurate? | Reference the existing issue/epic and report evidence; do not close work merely because code exists. |
| Release | Is this user-facing or release-note-worthy? | Add a changelog entry or mark `Not applicable`; do not claim a release before a tag and artifact exist. |
| Security/licensing | Are dependencies, external content, assets, permissions, or data flows affected? | Review provenance/license and least-privilege implications; keep unresolved legal or owner decisions open. |
| Wiki/community | Is approved public content changed or a GitHub-only action required? | Identify the canonical source and required owner action. A merged PR is not proof of wiki/discussion/project configuration. |

## 2. Pull request and merge lifecycle

1. Link the PR to an existing issue or explain why no issue is needed. Use a non-closing reference when the work does not complete the entire issue.
2. Keep implementation, automated test results, human/domain review, publication, and release status separate.
3. Before merge, verify the diff, changed-file list, relative links and generated artifacts; report every relevant test command and result, plus `NOT_RUN` checks.
4. Merge requires the repository's configured human approval and status checks. Agents do not merge to `main`, bypass checks, or claim that repository settings are enabled without observing them.
5. After merge, the repository owner or an explicitly authorized integration may update issue/project status and publish the wiki. Do not run write-side actions from untrusted pull-request code.

## 3. Documentation and localization lifecycle

- `AGENTS.md` is the canonical agent contract; `docs/engineering/`, `docs/product/`, and `docs/governance/` own their respective technical, product, and operational details.
- New public documentation is authored in English by default. A German counterpart must link to the same concepts and be labeled with its translation/review status.
- Do not translate archived source documents, original quotations, or legally sensitive statements in place.
- Catalog changes require valid JSON, key parity, placeholder parity, no empty required values, and an updated language coverage report once the runtime catalogs are introduced.
- A UI translation review does not certify a music-theory claim. A domain review does not certify translation quality.

## 4. Knowledge and publication lifecycle

- Treat files under `research/` as source-bound research unless their review and publication state explicitly says otherwise.
- Preserve exact source identity, hashes, rights classification, claim locators, and historic review artifacts.
- Publish only reviewed, rights-cleared content through the existing knowledge adapter. Do not create a second active claim or work-instruction register.
- A generated report is evidence for its exact commit and command, not a standing assertion that later commits have passed.

## 5. GitHub-only operations and owner actions

Repository files can prepare a process but cannot by themselves create or authorize GitHub settings. Project boards, discussion categories, the separate Wiki repository, sponsor accounts, branch protection/rulesets, required reviewers, secret scopes, and repository-wide security toggles require the relevant owner/admin permissions.

For any such operation, record:

- the exact GitHub object or setting to create/change;
- the required permission or credential scope, without storing credentials;
- a dry-run or reviewable diff where supported;
- the observed result after an authorized action.

If permission or configuration is missing, mark the operation `OWNER_ACTION_REQUIRED`. Do not report a configuration file as an activated GitHub feature.

## 6. Release maintenance

Before any release, validate the code/package version, `VERSION`, changelog, schema compatibility, English/German catalogs, user documentation, knowledge publication status, CI, packaging, notices, and platform-specific acceptance. Create release candidates separately from publication. Human approval is required before immutable version tags or public artifacts are released.

Run the [musical acceptance gates](MUSICAL_RELEASE_ACCEPTANCE.md) for every area included in the release. Open mandatory cases block approval of their assigned area.

The proposed product-specific gates are listed in [STEPS 1.0.0 Product Target and Readiness](../product/V1.0.0_PRODUCT_CONTRACT.md).
