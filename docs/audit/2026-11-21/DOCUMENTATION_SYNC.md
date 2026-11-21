# Documentation and GitHub synchronization, 21 November 2026

**Scope:** active documentation, roadmap, task register and GitHub objects of `n05a-design/steps`.
**Checked revision:** `main` at `3a5db64b6131806c432b7b38dca60680c5a57d9b` (PR #265), clean worktree.
**Status:** automated and read-only evidence. No owner, domain, translation, platform or release approval is implied.

## Commands and results

| Check | Command | Result |
| --- | --- | --- |
| Test suite | `python3 -B -m unittest discover -s tests -p "test_*.py"` | 875 tests, OK (macOS, Python 3.14) |
| Documentation status | `python3 -B scripts/check_documentation_consistency.py --check` | PASS |
| Release and versions | `python3 -B scripts/check_release_consistency.py --check` | PASS; `0.2.0-dev`, published tag `v0.1.0` |
| Reference integrity | `python3 -B scripts/verify_reference_integrity.py` | PASS |
| Gemini knowledge pack | `python3 -B scripts/check_gemini_knowledge_pack.py --check` | PASS; pack baseline dated 2026-11-19 |
| GitHub configuration | `python3 -B scripts/validate_github_config.py` | PASS |
| Knowledge benchmark | `python3 -B scripts/run_knowledge_benchmark.py --scope all` | 92 PASS, 0 FAIL, 27 PENDING |
| Musical release gate | `python3 -B scripts/verify_musical_release.py --report-only` | READY: `theory-core`, `midi-export`; BLOCKED: six areas pending independent review |
| Task register | `python3 .agents/skills/steps-knowledge-curation/scripts/validate_register.py` | 9 tasks, 0 errors after this change |
| Relative Markdown links (new) | `python3 -B scripts/check_markdown_links.py --check` | PASS, 394 active files |

## Findings and changes

| Finding | Change |
| --- | --- |
| Roadmap, implementation status, 1.0 readiness matrix, project overview and task register named `e2faf27` / PR #220 / 791 tests as the current state. PRs #222–#265 were only in the changelog and body text. | Dated status notes added for `3a5db64`; roadmap §0 summarizes PRs #222–#265 by area and adds stages E1–E6 toward 1.0. Historical snapshots stay unchanged. |
| The 1.0 readiness matrix still described `README.md` as German-first and did not mention the DAW fixtures (#240), the musical release gate (#247) or the macOS bundle build (#262). | Affected rows updated with their evidence and remaining limits. |
| No automated check for relative links in active documentation. | `scripts/check_markdown_links.py`, tests and a CI step added. One dated audit link to a PDF removed in `9a316c6` is kept as a named historical exception. |
| `release.yml` expects labels that did not exist on GitHub; eight issue templates had no labels; open epics had none. | Versioned taxonomy in `.github/labels.yml`; templates labelled; test ensures templates and release notes only use versioned labels. Creating labels on GitHub is tracked as OA-0041. |
| `main` has no branch protection; the only active ruleset enables Copilot code review. CODEOWNERS is therefore not an enforced gate. | Recorded as owner action OA-0042 and in roadmap §0.3. |
| GitHub Project board not readable with the available token (`read:project` missing); Wiki enabled but not initialized. | Kept as owner actions in roadmap §0.3. |

## Not run

- Native accessibility, DAW import, translation and user acceptance: require people and external applications.
- CI on Windows and Ubuntu for this branch: runs on the pull request.
- External link reachability and heading anchors: outside the link check.
