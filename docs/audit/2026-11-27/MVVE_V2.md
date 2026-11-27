# MVVE V2 implementation and verification

- **Evidence dates** 27–28 November 2026
- **Baseline** STEPS main at `8fe7163`, package 0.8.0.dev0. [PR #271](https://github.com/n05a-design/steps/pull/271)
- **Working branch** `feat/steps-mvve-v2`
- **Overall status** Partial implementation. Technical checks, independent musical acceptance, and publication each have their own evidence.

The Windows primary checkout was clean at `cd455e3`. A fetch confirmed `origin/main` at the audit baseline, and a separate worktree started at that revision. The checked local Keyboard worktree at `bab2343` was clean and the GitHub open PR list was empty at intake. Historical macOS worktree registrations were outside this Windows environment. The four baseline push runs succeeded. [Python](https://github.com/n05a-design/steps/actions/runs/45900185242), [pilot evidence](https://github.com/n05a-design/steps/actions/runs/45900185220), [structure](https://github.com/n05a-design/steps/actions/runs/45900185228), [secret scanning](https://github.com/n05a-design/steps/actions/runs/45900185320)

## Intake and baseline

The six expected files were present as loose files. The folder also contained a pasted analysis request and an archived unfinished prompt. The master V2 and its six-file evidence set governed the implementation. SHA-256 values matched before and after the audit.

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `README_START.md` | 875 | `dd04f414947fb4c83b35243d9757562a66ff5f4bfdd9d6657fc93cecd52d230f` |
| `STEPS_Master_Implementierungsauftrag_MVVE_V2.md` | 70365 | `803c401925d75a829b7287efe6ab8d29ae003abc7b76f3092085d3a91685cc67` |
| `STEPS_MVVE_Tiefenaudit_2026-11-27.md` | 31914 | `773a7da363a039810be5926475c485207d955bc4c2317c5483172500daddd9f1` |
| `STEPS_music_audit_prepared.py` | 14378 | `764accbf6279d5f68f6521013f4e2784a2aa775957fb0df7631317e95f2793c4` |
| `build_mvve_reference_candidate.py` | 6773 | `229be4f5cee194d0082dbdaf840bef7d414769cbbb0a3bccf8ef9281b2414a09` |
| `STEPS_MVVE_Reference_Candidates.json` | 1053634 | `2c5553be73e1b01c3be8bd7506611352c60a76a4748922faf1d4c184a98af540` |
| `Pasted text(20261127-145615).txt` | 12732 | `2a192df4a0a8a4012c1cf6825d3cf0d41fada483ba338603465cf68809255f64` |
| `Archiv/unfertiger Prompt.txt` | 125771 | `2a2b754f3d71c79c2576138b232adbb4e421e9cc5b4c0dfa8c2a2ee5f713d4f9` |

The rebuilt JSON uses CRLF on Windows. Its parsed content and its bytes after line-ending normalization equal the original. The compact in-repository formulas were cross-checked against all 2,064 candidate records across their tested fields. There are 72 chord records with explicit convention review markers. Musical expertise is still required for the profile choices. The candidate bundle, external corpora and proprietary assets stayed outside the worktree.

| Windows CPython 3.14 baseline command | Actual result |
| --- | --- |
| Starter `--self-test`, normal and optimized | Exit 0 for the original in both modes. |
| Starter `--repo . --profile smoke` | 1,446 pass, 10 fail, 1,456 total. Exit 1. |
| Starter `--repo . --profile full` | 25,097 pass, 10 fail, 25,107 total. Exit 1. Recognition tested 11 qualities over 24,577 inputs. |
| Starter with missing checkout | Exit 1 and no JSON artifact. |
| Starter copy with Dur changed to Moll | Normal exit 1. Optimized exit 0, false PASS. |
| Existing randomized audit `--trials 128` | 1,024 pass, exit 0. |
| Existing release verifier `--report-only` | Report written, exit 0. Mandatory reviews blocked several areas. |
| Existing knowledge pilot and publication benchmarks | Respectively 8 and 3 pass. Exit 0 for both. |
| Windows repository-wide unittest discovery | Already showed unrelated failures before the MVVE changes. The initial full process did not produce a successful summary. |

The targeted Windows unittest run reported 249 tests, 248 passed and one platform skip for POSIX mode and symlink behavior. Windows repository-wide discovery still reproduced the baseline failures in Glide Shell integrity, wheel packaging, Git fixtures and restricted-local source summaries. A separate full discovery also ended with a Windows interrupt in the structure test. Those results provide neither a green repository-wide baseline nor a green local full suite.

## Findings and regression evidence

The original Starter case IDs and the MVVE IDs stay stable. The baseline reports are local evidence. Candidate and source profile reviews retain their own approval path.

| Finding | Technical disposition | Current evidence and open contract |
| --- | --- | --- |
| MVVE-001 | Verified fixed | The old randomized assertion used its own modulo formula. [Product interval regression](../../../tests/test_theory_properties.py) invokes three APIs over all 16,384 ordered MIDI pairs. The complement mutation is detected. |
| MVVE-002 | Verified fixed for declared chord and recognition routes | Starter BASS-003…009 failed. [Chord-tone labelling](../../../src/steps/keyboard/chord_tones.py) and [recognition](../../../src/steps/keyboard/recognition.py) share the role-based figure check. 4,464 declared quality/root/bass combinations and focused wrong-bass regressions pass. |
| MVVE-003 | Reproduced, approval pending | Starter LIVE-001…003 expose collapsed channels, global sustain and global reset. Single-source behavior has intermediate-state tests. A separate draft trace models endpoint identity and disconnect. [Open decision](../../../research/gaps/OPEN_GAPS.md) |
| MVVE-004 | Verified fixed for exact recognition | Existing shared-template consistency remains useful. The independent formula index checks the entire exact candidate list, including empty/negative inputs and symmetric readings. Metamorphic doubling and transposition also verify ambiguity. |
| MVVE-005 | Verified fixed for bounded audit failures | A controlled generator exception fails its case, preserves earlier work and allows another area to finish. Setup, generation, product, oracle self-test and timeout failures have explicit outcomes. [Harness tests](../../../tests/test_music_audit_harness.py) |
| MVVE-006 | Implemented and locally verified | Keyboard, recognition, keyboard practice and musical integration all ran technically in release preview. Each remains blocked by independent review. [Release criteria](../../governance/MUSICAL_RELEASE_ACCEPTANCE.md) |
| MVVE-007 | Reproduced by live port inspection and recorded traces | CC120/123 share one event, and CC121 is outside the current port contract. Draft distinct actions are exercised independently. Production support requires ADR-019. [Current port](../../../src/steps/ports/live.py) · [MIDI Association](https://midi.org/summary-of-midi-1-0-messages) |
| MVVE-008 | Verified fixed for the disclosed constructor and feedback cases | Invalid policy, difficulty, MIDI/pitch classes, bass and review enum are rejected. The exact-pitch empty reply reports missing notes in their registers. [Regression](../../../tests/test_mvve_regressions.py) |
| MVVE-009 | Verified fixed for the disclosed construction and degree cases | Ordered intervals, written root and seven-note letter order enforced. The constructor retains specified root spelling for nonheptatonic scales. [Regression](../../../tests/test_mvve_regressions.py) |
| MVVE-010 | Classification confirmed | Recognition provides literal candidate sets and context flags. Harmonic function remains a session/analysis concern. The headless integration test covers recognition adoption followed by tonal analysis. [Session integration](../../../tests/test_keyboard_engine.py) |
| MVVE-011 | Verified distinction | `held_pitches` reports a common MIDI pitch. `stationary_voices` reports unchanged register pairs. Opposite movements and common pitches moving between voices have direct tests. [Regression](../../../tests/test_mvve_regressions.py) |
| MVVE-012 | Profile recorded, expert review required | The named extensions and omission conventions are test scope. The compound-role arrays and the six review-marked qualities are defined in the [reference profile](../../../scripts/music_audit_references.py). |
| MVVE-013 | Verified fixed in canonical audit | The historical optimized bypass was reproduced on a copy. The new explicit checks detect the same mutation under `-O`. |
| MVVE-014 | Verified for checkout/setup and bounded case failures | Import and checkout mismatches have explicit error paths, JSON is atomic, and replay rejects a changed payload hash. A process kill can still interrupt reporting. |
| MVVE-015 | Partial | 31 qualities, 15 scales, actual harmonization calls, all portable pitches and enharmonics, single-source MIDI intermediate states and CC64 thresholds are checked. Exhaustive exact recognition has a measured bound. Rhythm, context/ranking, omissions and multi-device coverage remain narrower. |
| MVVE-016 | Configured, GitHub execution pending | The PR matrix runs technical validation. The branch adds scheduled/manual validation, report artifacts and a read-only freshness check. The local freshness result is `NOT_RUN`. The GitHub rules lookup returned Copilot review, with no observed required status check for this new work. |
| SMF header truncation | Reproduced and fixed | A 14-byte header declaring 10 header payload bytes and zero tracks formerly passed. The parser now checks the declared header extent independently of track count. A synthetic multi-track fixture checks every strict byte prefix, segment timing, meter events and same-note overlaps. [Parser](../../../src/steps/midi/smf_parser.py) · [Regression](../../../tests/test_mvve_regressions.py) |

## Coverage and requirement matrix

| Work package and rules | API, domain and case evidence | Status and remaining scope |
| --- | --- | --- |
| WP01, intake and baseline | Artifact inventory, direct GitHub checks, historic runtime execution | VERIFIED for the listed baseline operations. See the Windows repository-wide limitation above. |
| WP02, MVVE-001/004/005/013/014 | `invert_semitones_modulo12`, `recognize_chord`, `run`, self-test, generator/timeout/replay tests | VERIFIED within the stated cases. Independent references stay technically scoped. |
| WP03, profiles and error lifecycle | Stable case IDs, SHA-256 payloads, versioned sources, atomic JSON, per-area results and portable replay | PARTIAL. A persistent cross-run error database, general shrinking and hard per-case process deadlines remain open. Hypothesis shrinks supported state traces. |
| WP04, MVVE-002/003/007–012 | `label_voicing`, `Exercise`, `ScaleDefinition`, `compare_voicings`, `KeyboardInputState` | VERIFIED for the fixed contracts. EXTERNAL_REVIEW_REQUIRED for extended-profile decisions, hardware and multiple sources. |
| WP05, enumeration and mutation | 128 MIDI notes and their supported spellings, all 88 piano keys, 16,384 interval pairs, 2,064 chord/scale/harmonization records, 4,464 declared bass cases, 24,577 exact-recognition inputs, 16 isolated curated mutations and bounded SMF prefix checks | PARTIAL. Native Windows lacks the fork/WSL environment for mutmut. Branch coverage, general mutation score, configurable weighted combinations, long sequence/minimization coverage and coverage-guided parser fuzzing remain open. |
| WP06, external verification | music21 and Tonal basic-chord pitch classes, Mido SMF metadata and events on original and rewritten synthetic files | PARTIAL. 84/84 music21, 84/84 Tonal, 16/16 Mido. No corpus licensing or extended profile equivalence follows from these comparisons. [28-project register](MVVE_EXTERNAL_REFERENCES.md) |
| WP07, continuous and release | Local smoke, PR and full; scheduled and pull-request configuration; technical checks in all new release areas | PARTIAL. No GitHub run on this local branch. OWNER_ACTION_REQUIRED for publication and required-check enforcement. |
| WP08, canonical keyboard/session integration | Production APIs for key entry, recognition, explicit controller adoption, harmonic degree, preview, undo/redo, save/load and SMF export | PARTIAL. The combined headless chain and existing failures/recovery cases pass. Richer context, alternative voice pairing, performance and wider generated compositions need further coverage. |
| WP09, Knowledge/Skill/Practice/MIDI | Existing runtime benchmark, supervised pilot, deterministic query assertions, independent SMF checks | PARTIAL. Full benchmark 92 pass, 0 fail, 27 pending. A/B/C/D model runs and holdout results are NOT_RUN. The six keyboard exercises remain drafts. DAW, hardware, extended composition and arrangement remain separately scoped. |
| WP10, maintenance and handoff | This report, open gaps, roadmap, keyboard architecture, release guide and command references | PARTIAL. Reassess remaining requirements and acceptance statuses before calling the full master order complete. |

Source-bound graphs and corpus audits retain their existing owners in the Python workflow and knowledge scripts. The relevant existing checks include `audit_graph_corpus.py`, `audit_gmd_coverage.py`, `audit_pattern_syncopation.py`, `verify_reference_integrity.py`, `render_reviewed_progressions.py`, `render_api_reference.py` and `check_documentation_consistency.py`. Their results should stay tied to their own scope and revision.

## Operating the checks

Run commands at the worktree root. Use `py -3.14` in Windows PowerShell and `python3` on macOS with a supported Python. These examples were checked on Windows. `<evidence-dir>` denotes a writable directory outside the worktree.

```text
python3 -B -O scripts/audit_randomized_music.py --self-test
python3 -B scripts/audit_randomized_music.py --list-areas
python3 -B scripts/audit_randomized_music.py --profile smoke --json-out <evidence-dir>/smoke.json
python3 -B scripts/audit_randomized_music.py --profile pr --workers 2 --timeout 120
python3 -B scripts/audit_randomized_music.py --profile full --seed 20261121 --json-out <evidence-dir>/full.json
python3 -B scripts/audit_randomized_music.py --case RECOG-fff-11 --json-out <evidence-dir>/case.json
python3 -B scripts/audit_randomized_music.py --replay <evidence-dir>/replay.json
python3 -B scripts/check_music_audit_mutations.py --json-out <evidence-dir>/mutations.json
python3 -B scripts/check_music_audit_freshness.py --json-out <evidence-dir>/freshness.json
python3 -B scripts/verify_musical_release.py --area all --report-only --json-out <evidence-dir>/release.json
```

The default command still runs the eight random areas. Smoke and PR combine all fixed references with recognition anchors and 512 or 1,024 additional seeded draws, respectively. Full, nightly and release enumerate the 24,577 recognition inputs. The scheduled run uses the UTC date as its seed. On the Windows audit checkout, smoke passed 9,440 observations, PR 9,923 and full 32,257, with zero case failures, errors or timeouts. The measured full run was around eight seconds. `--trials` and `--cases` change the randomized count per area. The cooperative time budget applies to the serial run or to each area task in parallel mode. The runner checks deadlines between cases. GitHub also applies a job timeout to the scheduled run.

To replay, save the failure's `replay` object as a JSON file. Inputs and expected outcomes are hashed. Product replay works with recorded random trials and finite reference cases. Setup and generation errors may have no concrete input. The CLI returns 0 on technical pass, 1 on an observation mismatch, 2 for invalid parameters or unknown case, and 3 for execution, oracle, setup or time-budget errors. The release verifier has its own contract. Its report mode allows inspection even when a release area is blocked.

For independent comparisons use an isolated environment with `music21==10.5.2` and `mido==1.3.3`. Install `tonal@6.16.0` separately with lifecycle scripts disabled and pass its local module directory. The Python version snapshot and npm lockfile are kept with the local evidence. The shared comparison checks seven basic chord qualities across 12 tonic spellings and the two supported SMF formats. It compares pitch classes and event traces under stated normalizations. It does not vote on the meaning of extended symbols. [music21 harmony](https://music21.org/music21docs/moduleReference/moduleHarmony.html) · [Mido](https://mido.readthedocs.io/en/latest/changes.html) · [Tonal](https://github.com/tonaljs/tonal)

```text
python -B scripts/audit_randomized_music.py --area pitch --external-oracles --tonal-module <tonal-install>/node_modules/tonal
python -B -m unittest tests.test_music_audit_stateful -v
```

The scheduled workflow installs hash-pinned Hypothesis wheels in a disposable venv. Windows CPython 3.14 x64 can use the same [stateful test pins](../../../scripts/music-audit-stateful-requirements.txt). The local Hypothesis run passed both stateful tests and the deterministic single-source examples. The temporary mutation snapshots used only authored implementation and Python test sources. The Windows host has no WSL installation and mutmut requires fork. [mutmut requirements](https://mutmut.readthedocs.io/en/latest/#requirements)

## Next approval and verification boundaries

- ADR-018 and ADR-019 remain proposed. ADR-007 and ADR-017 define the accepted export scope and its DAW evidence requirements. The current input remains single-source. The draft multi-source trace recommends a source/device/channel/note identity, endpoint-scoped sustain, separate channel-mode events and global panic. Native acceptance will require real device traces.
- Existing keyboard rendering consumes the same neutral workbench/state contracts documented in the [keyboard architecture](../../architecture/KEYBOARD_ARCHITECTURE.md). Preview and explicit controller commands retain their separate roles.
- To assess publishability, reviewers must use the exact clean STEPS revision and authentic independent evidence. Technical readiness of `theory-core` or `midi-export` does not certify DAW import or a combined product release. The local release preview recorded two READY and ten BLOCKED areas.
