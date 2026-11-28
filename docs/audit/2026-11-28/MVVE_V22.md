# MVVE V2.2 verification and integration

This checkpoint starts at `41acc91a11e56cb66291fbf2bb064654d44ab7b4`. The latest observed remote main was `8fe7163006d154638bdd5181963ccf70ce261868`. The V2 and V2.1 reports retain their original revision boundaries. The local V2.2 evidence index records the exact final revision, commands, SHA-256 digests, result counts and changed files. [V2 findings MVVE-001–016](../2026-11-27/MVVE_V2.md) · [V2.1 requirements A–K](MVVE_V21.md)

| V2.2 requirement | Evidence and limit |
| --- | --- |
| §3 Mutation resolution | `--replay-v21` regenerates the original 56 sites from their Git commit, relocates unchanged source lines, then runs the current witnesses. No skipped or unmappable site can pass. Structured exception outcomes preserve product, loader, import, infrastructure and timeout distinctions. The local per-site register retains all 22 historical non-detections. |
| §4 Windows regression | Real independent processes test active, exited and terminated owners and concurrent acquisition. Mocked native handles test denied access, invalid IDs, wait failure and cleanup with no signal. The zero-byte `.lock.guard` serializes writer metadata updates and intentionally persists. Owner tokens prevent stale or unowned release. PID reuse before timeout is conservatively treated as an active owner. The guard applies to callers of the explicit ProjectLock API. The current lease and simultaneous use by older builds remain compatibility limits. |
| §5 Shell | Hashes of Git blobs, checkout bytes, built wheel entries and installed resources were compared for every manifest file. The dedicated owner handoff records all remediation alternatives. [Shell owner handoff](MVVE_SHELL_OWNER_HANDOFF.md) |
| §6 MIDI | Generated valid streams cover 7-, 14-, 21- and 28-bit boundaries and mutate intact track framing. Added SysEx, strict validation of explicit End-of-Track, malformed data, FIFO note pairing and unsupported Format 2 and SMPTE distinctions. Missing End-of-Track remains accepted for existing callers. A FIFO stress fixture exercises 4,000 overlapping notes without quadratic head removal. File-wide memory limits remain unspecified. |
| §7 Musical results | The cadence C–D7–G is checked under an explicit key change, with undo, redo, persistence and re-imported multitrack MIDI bass/voicing. This is context selection. The generic project export also preserves explicit 3/4, its tempo map, a supplied melodic line and swung drum onsets in both MIDI formats. Automatic modulation, autonomous melody and arrangement generation have no new product implementation. Prior groove and corpus scope remains the V2.1 scope. |
| §8 Differential | music21 and Tonal remain pinned to the existing theory comparisons. Each exception is the exact tonic-relative addition or omission, with no additional difference accepted. Mido adds boundary delta, SysEx, End-of-Track and low/zero-velocity semantics. The local register retains the 24 root-specific rows. |
| §9 Knowledge and skills | The exact-revision benchmark and local unresolved-case register distinguish deterministic passes, missing sources/review and unavailable model responses. No approved content, answer keys or model responses are committed. |
| §10 Decisions and review | The separate ADR-019 decision brief and the German review packets preserve the hardware, source and independent approval boundaries. The additional review case covers an explicit tonal context change. [ADR-019 decision brief](MVVE_ADR019_DECISION_BRIEF.md) · [Review packets](MVVE_FACHABNAHME.md) |
| §§11–12 Integration and security | Workflow syntax and local equivalents are scoped by trigger. The separate curation suite exposed another Windows empty-environment value loss. Its register-path test now replaces a mocked mapping without rewriting the real process environment. The diff is reviewed against the observed remote commit. Private stdout, user paths, benchmark keys and evidence indices remain local. Repository-safe changes contain original code, synthetic fixtures and links to existing or primary sources. |
| §§13–16 Final verification, audit and handoff | The local evidence index binds both Windows variants, the full musical profile, release and benchmark reports to the final commit. The earlier V2 and V2.1 matrices remain the source for previously proved requirements. Open technical gaps and reviews retain their status. |

## Gate sequence

1. **Checkpoint push** requires the scoped Git diff, secret scan and local verification. A first push also requires explicit authorization. Schedule freshness has no role at this phase.
2. **Draft pull request** requires the checkpoint branch and explicit authorization. Describe the Shell hash failures as a known external blocker, and attach the allowed evidence.
3. **Merge readiness** requires actual feature and PR checks on the candidate revision, verified required check names, human code review and disposition of the known Windows blocker. The branch remains local.
4. **Post-merge verification** checks the actual main revision, then observes a calendar-triggered execution and freshness. GitHub schedules run on the default branch. A manual run and a feature-branch run have distinct evidence. [GitHub schedule behavior](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)
5. **Musical publication** uses the canonical acceptance workflow, remaining human approvals and platform evidence. The local technical checkpoint conveys no musical publication status. [Musical release acceptance](../../governance/MUSICAL_RELEASE_ACCEPTANCE.md)

## Reproduction

```text
python -B scripts/check_music_audit_mutations.py --replay-v21 --json-out mutations.json
python -B -m unittest discover -s tests -p "test_*.py" -v
python -B scripts/audit_randomized_music.py --profile full --workers 2 --timeout 120 --external-oracles --tonal-module PATH_TO_TONAL --json-out full.json
python -B scripts/run_knowledge_benchmark.py --scope all --json-out knowledge.json
python -B scripts/verify_musical_release.py --area all --json-out release.json
```

Use the same Python and dependencies for both Windows checkouts. The exact-byte comparison changes only materialization of the intact reference blobs. Use an evidence directory outside either checkout. The Git revision containing the V2.1 cohort must be available for the frozen mutation replay.

The `reviewed` and GitHub-review mutation witnesses use test-only citations and synthetic reviewer evidence. A product exception on a previously passing witness is evidence of detection, and a module-load regression is separately visible. Source path and stack frames distinguish unrelated infrastructure failures. The altered recognition rank for incomplete vs. standard candidates is semantically equivalent after stable partitioning. The altered suspended recipe can switch between legitimate enharmonic-context-free suspended roots and remains a policy observation. The altered fourth decimal of elapsed time is telemetry precision outside the published acceptance contract.
