# STEPS Safe Sync Plan

No merge, push, reset, clean, force-push, branch deletion, tag change, or release action was performed. This plan is read-only and requires separate authorization for integration.

## P0 — preserve and verify

1. Preserve all worktrees, stashes, reflogs, unreachable objects, OneDrive copies, and prunable metadata.
2. Do not prune or garbage-collect until every relevant inaccessible worktree is accounted for.
3. Retain current `origin/main` and the merged Gemini Knowledge Pack commit as evidence snapshots.
4. Keep rights/security review as a blocker for any copyrighted or private source material.

## P1 — reconcile implementation branches

1. Select each specialized STEPS branch/worktree by source business impact.
2. Compare the source tree by Git patch/Blob identity against `origin/main`, accounting for squash, rebase, and cherry-pick.
3. Mark files with `ALREADY_INTEGRATED`, `CONTENT_DIVERGED`, or `LOCAL_COMMIT_NOT_PUSHED` only after patch comparison.
4. Create isolated integration branches from `origin/main`.
5. Re-run 746 unit tests, 40 curation tests, pack checks, i18n gates, documentation gates, and pilot/all benchmark checks.

## P2 — owner-approved knowledge and documentation

1. Obtain individual human decisions for the 27 pending benchmark cases.
2. Resolve source/provenance, graph, and historical claim findings with evidence.
3. Update issue/roadmap state without implying release or manual approval.
4. Keep historical prompts and reports immutable as audit artifacts.

## P3 — packaging and live GitHub service settings

1. Reproduce and sign native installers only under owner-controlled credentials.
2. Create a real external DAW interoperability fixture and independent human protocol.
3. Verify live wiki, Discussions, Projects, Funding, branch rules, and release settings through owner access.
4. Create a new PR only for owner-authorized missing work, never merge directly to `main`.
