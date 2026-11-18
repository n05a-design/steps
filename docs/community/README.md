# Community and Public Presence

**Status:** Operating proposal and owner-action list, assessed 2026-11-18. These materials are drafts for review; they do not publish discussions, initialize a wiki, create a Project, or activate funding.

## Current GitHub state

| Surface | Observed state | Next action |
|---|---|---|
| Discussions | Enabled. Existing categories are `Announcements`, `General`, `Ideas`, `Polls`, `Q&A`, and `Show and tell`. | Reuse existing categories. An owner may add `Music Theory & Harmony`, `Development & Architecture`, and `Knowledge Base & Research` if they improve discovery. Do not create duplicates of `Ideas` or `Q&A`. |
| Wiki | Wiki support is enabled, but `n05a-design/steps.wiki` returned 404 during this assessment; no initialized wiki repository was found. | Owner initializes it. Until then, `docs/` remains the canonical source; do not claim that wiki sync is active. |
| Projects | Projects support is enabled, but no repository-linked GitHub Projects v2 board was returned by the repository query; `gh project list --owner n05a-design` returned none. | Owner creates one after approving fields, views, and automation scope. |
| Funding | No `.github/FUNDING.yml` or verified sponsor account/URL is present. | Do not publish a sponsor button or placeholder account. The owner must first establish and verify a supported funding destination. |

Prepared versionable assets:

- `.github/DISCUSSION_TEMPLATE/` contains English drafts for Questions, Ideas, Music Theory,
  Knowledge & Research, and Development. Category creation and live publication remain owner actions.
- [GitHub Project specification](GITHUB_PROJECT_SPEC.md) is a no-write configuration proposal.
- [Wiki publication manifest](WIKI_PUBLICATION_MANIFEST.md) remains `OWNER_ACTION_REQUIRED`.
- [Funding owner action](FUNDING_OWNER_ACTION.md) records the funding boundary without a placeholder account.

## Language and moderation

English is the default language for public navigation and project announcements. Community members may post in English or German. A German-language post does not need to be removed or machine-translated. When a bilingual summary is useful, label each language clearly and preserve source meaning.

Announcements and release claims must reference an exact merged commit or release. Draft text below contains placeholders and is not an announcement about a completed feature.

## Discussion-category proposal

| Existing category | Recommendation |
|---|---|
| Announcements | Reuse for owner-reviewed project and release notices. |
| General | Reuse for introductions and community topics. |
| Ideas | Reuse for feature brainstorming; implementation requests still belong in Issues. |
| Polls | Reuse only for clearly scoped, non-binding questions. |
| Q&A | Reuse for questions and support; point reproducible defects to Issues. |
| Show and tell | Reuse for projects and musical examples that contributors have rights to share. |
| Music Theory & Harmony | Optional new category; add only if category permissions and moderation are assigned. |
| Development & Architecture | Optional new category; otherwise use Issues/PRs for actionable work. |
| Knowledge Base & Research | Optional new category; do not use it to publish unreviewed sources or copyrighted excerpts. |

GitHub category creation and moderation settings are UI/API operations, not ordinary repository-file changes. The discussion-form syntax has been checked against GitHub's published schema. No discussion-form files are added because no new category or category-to-template mapping has been approved; the existing categories can use the reviewed post drafts below without repository-specific forms.

## Reviewable post drafts

### Welcome discussion — draft

> **Welcome to STEPS**
>
> STEPS is an open-source project for chord progressions, harmony, and music theory. The Python core and a desktop prototype are available in the repository; the project is not yet a complete installable product.
>
> English is the default language for project updates. German contributions are welcome. Please keep musical notation explicit (`INT` or `DE`) and share only material you have permission to publish.
>
> For reproducible defects or implementation requests, use the [issue tracker](https://github.com/n05a-design/steps/issues). For security issues, follow [SECURITY.md](../../SECURITY.md) rather than posting publicly.

### Community introduction — draft

> **Introduce yourself**
>
> - What do you compose, produce, teach, or study?
> - Which music-theory or workflow problem brought you to STEPS?
> - Which language do you prefer for discussion: English, German, or either?
> - Is there a musical example you can describe without sharing material you do not have rights to?

### Development update — draft

> **Development update — YYYY-MM-DD**
>
> - Verified merged work: `<PR/commit links>`
> - What users can do now: `<link to implementation status>`
> - Still in progress or blocked: `<issue links>`
> - Tests or manual checks: `<exact commands/results>`
> - Owner decisions needed: `<items or "None">`
>
> Do not describe a proposed design, open PR, planned issue, or passing unit test as a shipped product feature.

### Major feature announcement — draft

> **Feature: `<user-visible capability>`**
>
> - Availability and version: `<release/tag or "not released">`
> - User outcome: `<what can be done>`
> - Limitations: `<known boundaries>`
> - Documentation: `<link>`
> - Verification: `<tests and any manual acceptance>`
> - Related work: `<PR/issue links>`
>
> German summary (if reviewed): `<German text or "not yet reviewed">`

### Release discussion — draft

> **STEPS `<version>`**
>
> - Release tag and commit: `<immutable tag and SHA>`
> - Highlights: `<verified release-note entries>`
> - Install instructions: `<exact artifact/documentation link>`
> - Known issues: `<issue links>`
> - Language and platform coverage: `<verified support matrix>`
> - Security/licensing notes: `<reviewed release information>`
>
> German summary: `<reviewed translation or "not yet reviewed">`

### Community guidelines — draft

> Be kind and constructive. Critique ideas and evidence, not people. Make the musical context, theoretical perspective, and notation convention explicit. Preserve plausible alternative analyses. Do not post private information, copyrighted pages, unlicensed recordings, or credentials. Keep actionable bugs and feature requests in Issues, and report security concerns privately. English and German are welcome; English is the project-wide default for summaries.

## Documentation wiki publication

The canonical sources remain versioned under `docs/`, `knowledge/`, and the root project files. A future wiki must be a selected publication view of approved source documents, not a second independently edited theory base.

Required before enabling synchronization:

1. Owner initializes the Wiki and selects exact source pages/locales.
2. A PR-reviewed manifest lists each source and destination page; unreviewed research is excluded.
3. Synchronization runs only from a trusted post-merge context with least-privilege credentials. Fork/PR code must never receive wiki write credentials.
4. A dry-run produces a diff and refuses to overwrite a manually changed page without review.
5. Logs record source commit and publication result. Missing permission or missing wiki is an explicit failure, not a success-shaped no-op.

No synchronization workflow is active in this repository at the assessment baseline.

## Project dashboard proposal

After an owner creates a Project, suggested views are:

- **Development:** Backlog, Ready, In Progress, In Review, Blocked, Done.
- **Product roadmap:** milestones and dependencies; dates remain owner-managed.
- **Knowledge quality:** source, claim, domain-review, rights, and publication blockers.
- **Localization:** locale coverage, missing translations, placeholder errors, and review status.
- **Release readiness:** tests, docs, security, packaging, platform acceptance, and owner sign-off.

Do not overwrite manually curated field values from an automation. Use narrowly scoped GitHub App/project permissions; do not store tokens in the repository.

## Funding setup

Funding is intentionally unconfigured. The owner must choose a platform, complete its account verification and legal/tax review, decide how contributions are handled, and verify a public destination before adding `.github/FUNDING.yml`. No sample username, payment ID, or donation URL should be committed.

[GitHub and CI configuration](../../.github/GITHUB_UND_CI.md) · [Continuous repository maintenance](../governance/CONTINUOUS_MAINTENANCE.md) · [Product target](../product/V1.0.0_PRODUCT_CONTRACT.md)
