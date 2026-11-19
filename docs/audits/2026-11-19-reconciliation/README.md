# STEPS Reconciliation Audit - 2026-11-19

This directory contains the public, rights-cleared reconciliation evidence
created for the STEPS repository audit on 2026-11-19.

## Executive reports

- [Executive status](STEPS_EXECUTIVE_STATUS.md)
- [Local inventory](STEPS_LOCAL_INVENTORY.md)
- [Local/remote reconciliation](STEPS_LOCAL_REMOTE_RECONCILIATION.md)
- [Requirements completeness audit](STEPS_REQUIREMENTS_COMPLETENESS_AUDIT.md)
- [Safe synchronization plan](STEPS_SAFE_SYNC_PLAN.md)
- [Verification results](STEPS_VERIFICATION_RESULTS.md)
- [Expert decisions from 27 pending benchmark cases](EXPERT_DECISIONS_2026-11-19.md)

## Machine-readable evidence

- `01-local-git-inventory.txt`: local worktree, branch, ref, reflog and object inventory
- `02-git-root-candidates.txt`: discovered STEPS repository roots
- `03-remotes.txt`: configured remote inventory
- `04-all-refs.tsv`: tabular branch and ref inventory
- `05-merged-to-main.txt`: local refs and commits identified in `main`
- `06-not-merged-to-main.txt`: refs not identified in `main`
- `07-active-status.txt`: active worktree status
- `08-benchmark-all.txt` and `benchmark-all.{json,md}`: full benchmark output
- `09-active-git-file-inventory.tsv`: SHA-256 inventory of active worktree files
- `10-github-pr-inventory.json`: GitHub pull-request inventory
- `11-github-issue-inventory.json`: GitHub issue inventory
- `12-github-release-inventory.txt`: GitHub release inventory
- `13-github-main-actions.json`: main-branch Actions and workflow inventory
- `14-prompt-source-hashes.txt`: hashes of prompt source attachments, without prompt contents
- `15-all-branches.txt`: structured branch/worktree inventory
- `pilot.txt` and `pilot.json`: pilot benchmark evidence

## Scope and limitations

These reports are evidence snapshots for the recorded baseline and commands.
They do not claim that later commits, unreviewed external sources, human
acceptance, platform certifications, or GitHub owner-only settings have been
verified.

The reports contain no raw prompt attachments, private credentials, or
copyrighted source texts. Machine-specific paths are retained as audit
provenance and should not be interpreted as required repository paths.
