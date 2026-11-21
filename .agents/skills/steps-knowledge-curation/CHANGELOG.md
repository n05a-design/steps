# Changelog – steps-knowledge-curation Skill

## Unreleased

- Track row-wise evidence fingerprints for catalog, Golden, graph, historical
  and readiness records. Include the check in research-library release acceptance.
- Reject Markdown-formatted task IDs and require a reason for
  `NOT_APPLICABLE`. Report malformed baseline fields as structured failures.
- Separate the canonical register and reference checks in CI.

- Use the repository identity verifier, require the Golden mirror and validate
  v3 graph bindings against the original relation rows and recorded reviews.
- Check task heading syntax and resolve declared completion commits for the
  canonical register. Apply task syntax checks during restore.
- Report an incomplete duplicate scan as an error. Source checks without an
  intake directory return `None` for `within_bounds`. Task extraction from
  unsupported formats or corrupt text now fails explicitly.
- Run live repository checks on each curation CI platform.

## [1.0.0] - 2026-11-10 (Phase 3 Master V2)
### Added
- Initial verified release of the `steps-knowledge-curation` skill.
- Runbook `SKILL.md` with progressive disclosure to `references/`.
- Executable scripts for source checking, duplicate detection, instruction extraction, and register validation.
- Standard templates for source entries, work instructions, and conflict documentation.
- Comprehensive automated test suite in `tests/test_curation_tools.py`.
- Strict alignment with P0-1 copyright safeguards and the 5 music theory axioms.
