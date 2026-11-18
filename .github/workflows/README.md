# Automated GitHub checks

The workflows validate different properties of the exact revision under test.

| Workflow | Purpose |
|---|---|
| [Python tests](python-tests.yml) | Python 3.11–3.14, curation tests, API/Golden checks, pilot publication, and knowledge coverage. |
| [Repository structure](structure-check.yml) | Directory structure, JSON, and selected tests for relevant path changes. |
| [Pilot evidence](pilot-evidence.yml) | Validates GitHub approval evidence using the base-commit verifier. |
| [Secret scanner](secret-scan.yml) | Checks changes for accidentally committed credentials. |
| [Repository configuration](repository-config.yml) | Parses GitHub YAML, checks issue-form structure, and validates Dependabot/release configuration. |

[Local checks](../../tests/README.md) · [GitHub Actions](https://github.com/n05a-design/steps/actions)

The pilot-evidence workflow uses the trusted base resolver
`scripts/resolve_pilot_review_revision.py`. If the pull-request merge ref has
disappeared, it accepts only a verified completed merge with the expected event
parents. API or identity errors fail closed; target code is not executed by the
resolver.

[GitHub and CI overview](../GITHUB_UND_CI.md)
