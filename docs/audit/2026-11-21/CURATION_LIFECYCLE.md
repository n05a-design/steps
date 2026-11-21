# STEPS curation lifecycle audit

**Revision tested** `d227d7f238a166ac8efd6d30e8271affad7a51e5` from GitHub `main`.
**Scope** Migration selection, snapshot compatibility, restore readiness, and the
Git revision attached to the research-library release report. Tests used an
isolated checkout and temporary data. No musical data, acceptance decisions or
repository settings were changed during the audit.

Earlier changes are tracked in [#248](https://github.com/n05a-design/steps/pull/248),
[#250](https://github.com/n05a-design/steps/pull/250) and
[#258](https://github.com/n05a-design/steps/pull/258).

## Reproduced findings

| Area | Isolated change | Observed result |
| --- | --- | --- |
| Migration precedence | Swap the two existing `ACTIVE` controlled corrections for `REF-0015` in the migration CSV. Leave the data and fingerprints unchanged. | The reference check changes from exit 0 to exit 1. It selects the last active correction by row order. |
| Exact catalog corrections | In separate copies, change `PAT-001` from 115 to 116 BPM or replace the stated `P01` learning goal. Add a synthetic controlled correction with the exact new identity hash and regenerate the candidate fingerprints for that copy. | Each change still produces exit 1. The tempo and learning-goal checks ignore the matching correction while the hash comparison recognizes it. |
| Baseline compatibility | Change only `schema_version` from `1.3.0` to `99.0.0` in the identity baseline. | The reference check returns exit 0 without reporting the unknown version. |
| Snapshot readiness | Back up a version 2 test register containing `DONE_VERIFIED` with the four completion fields absent. Restore over an `OPEN` entry in the same target. | The inventory reports `VERIFIED` and restore succeeds. Full register validation then reports four missing completion fields. The inventory verifies the manifest and recoverable structure. |
| Snapshot identity | Store a backup outside its project directory, move the original project, and initialize another repository at that same absolute path with a different valid register. | Restore accepts the unchanged absolute path. The other register is replaced and its previous bytes are saved. |
| Release revision binding | Run the research-library preview from the STEPS checkout with `GIT_DIR` and `GIT_WORK_TREE` inherited from a separate synthetic repository. | The report analyzes the STEPS files but records the other repository's HEAD. Both previews report `BLOCKED`. The enforced run in the normal Git context reports the correct revision and returns exit 1. |

The relevant implementations are the
[reference verifier](../../../scripts/verify_reference_integrity.py),
[backup and restore helper](../../../.agents/skills/steps-knowledge-curation/scripts/backup_knowledge.py)
and [release verifier](../../../scripts/verify_musical_release.py).
The findings remain open for implementation.

## Verified controls

- The skill suite passed 82 tests. The repository suite passed 867 tests.
- A synthetic Windows version 2 backup was blocked by default on macOS. It was
  restored after the explicit other-register option was supplied.
- The clean research-library report identified missing independent reviews.
  Its preview returned exit 0 with status `BLOCKED`; enforced mode returned exit 1.
- The verified revision has a successful
  [Python and platform CI run](https://github.com/n05a-design/steps/actions/runs/44931188163).

Run the stock checks from the repository root. Use a disposable checkout and
temporary backup directory for the mutations described above.

```sh
python3 -B -m unittest discover -s .agents/skills/steps-knowledge-curation/tests -q
python3 -B -m unittest discover -s tests -p 'test_*.py' -q
python3 -B .agents/skills/steps-knowledge-curation/scripts/check_reference_ids.py --json
python3 -B scripts/verify_musical_release.py --area research-library --report-only
```

## Outstanding evidence

Bind release reports to their own repository context first. Resolve overlapping
active corrections explicitly and make the controlled correction policy
consistent across catalogs. Distinguish snapshot integrity, restore eligibility
and completion evidence in the reports. The
[open evidence register](../../../research/gaps/OPEN_GAPS.md) records the wider
review and governance scope.
