# Automated GitHub checks

The workflows validate different properties of the exact revision under test.

| Workflow | Purpose |
|---|---|
| [Python tests](python-tests.yml) | Python 3.11–3.14, curation tests, API/Golden checks, pilot publication, knowledge coverage and technical music validation. |
| [Repository structure](structure-check.yml) | Directory structure, JSON, and selected tests for relevant path changes. |
| [Pilot evidence](pilot-evidence.yml) | Validates GitHub approval evidence using the base-commit verifier. |
| [Musical release acceptance](musical-release.yml) | Runs the technical and independent review gates for the selected release area on STEPS main. |
| [Secret scanner](secret-scan.yml) | Checks changes for accidentally committed credentials. |
| [Repository configuration](repository-config.yml) | Parses GitHub YAML, checks issue-form structure, and validates Dependabot/release configuration. |

[Local checks](../../tests/README.md) · [GitHub Actions](https://github.com/n05a-design/steps/actions)

Music validation runs in the PR test matrix. The default-branch schedule runs at 03:24 UTC and manual dispatch accepts a profile, seed or finite reference case. The run stores separate JSON evidence and performs stateful tests on the schedule. Sunday runs include curated mutation checks. Inspect the latest scheduled job with `python -B scripts/check_music_audit_freshness.py`. A missing, stale, failed or skipped scheduled job returns a nonzero exit status. The musical release workflow continues to require its independent evidence on STEPS main. [MVVE operating instructions](../../docs/audit/2026-11-27/MVVE_V2.md)

The pilot-evidence workflow uses the trusted base resolver
`scripts/resolve_pilot_review_revision.py`. If the pull-request merge ref has
disappeared, it accepts only a verified completed merge with the expected event
parents. API or identity errors fail closed; target code is not executed by the
resolver.

[GitHub and CI overview](../GITHUB_UND_CI.md)
