# Musical release acceptance

Each musical release area has an executable gate for its deterministic behavior and a separate review for its source-dependent claims. A mandatory case that is missing, rejected or tied to another revision blocks its assigned release area.

| Area | Technical evidence | Independent musical evidence |
| --- | --- | --- |
| `theory-core` | Pitch, spelling, chord, degree and API contracts, including desktop transposition | Deterministic contracts |
| `desktop-voicing` | Beginner bass and reduction probes, voice-leading regression tests | Style, playable range and the required P02 playing check |
| `keyboard` | Key identity, voicing roles, bass and scale integrity | Contextual note names and voicing figures |
| `recognition` | Exhaustive exact recognition over 24,577 sounding set and bass combinations, plus recognition regressions | Ambiguous, standard and incomplete readings |
| `keyboard-practice` | Scoring policies, malformed exercise rejection and pilot regressions | Exercise-by-exercise review of valid answers and feedback |
| `musical-integration` | Workbench/session contracts and project persistence | Recognition adoption, preview isolation, recovery and exported output |
| `midi-export` | SMF tests, truncation and multi-tempo fixtures, timing and 192 exported CLOSE/Drop-2 and slash-bass cases | DAW acceptance is tracked separately |
| `recommendations` | Harmony and graph tests, Explorer probes for supported double accidentals | Alternative readings, stylistic scope and confidence labels |
| `learning-pilot` | Pilot calculation, publication tests and authentic GitHub pilot approvals | Teaching material, sources and the mandatory listening exercise |
| `knowledge-adapter` | Actual evaluation prompts, notation, relevance and unapproved-source checks | Correctness, citations and uncertainty in the actual responses |
| `harmony-coach` | Versioned prompts and required criteria across all twelve domains | Reviewed responses and source evidence for the actual model and Skill revision |
| `research-library` | Catalog and corpus checks, historical reference identities, and curation evidence fingerprints | Provenance, stylistic claims and outstanding historical cases |

The existing [knowledge benchmark](../../knowledge/benchmark/README.md) retains its case IDs and criteria. Release gates classify every benchmark case. This checks the declared cases for the selected area. Product-wide releases require `all` along with the other repository release gates.

## Run and enforce the gate

```sh
python -B scripts/verify_musical_release.py --report-only
python -B scripts/verify_musical_release.py --area desktop-voicing
```

The enforced command exits with status 1 when any selected area is blocked. It requires a clean tracked checkout. `--report-only` lets maintainers inspect all blockers during development. The JSON report records the revision, whether it was a preview, and the reasons for each decision. The verifier reads the revision and
tracked state from its own checkout and ignores inherited Git context overrides.

Use the [Musical release acceptance workflow](../../.github/workflows/musical-release.yml) on STEPS `main`. A release workflow can call it and require its success before preparing or publishing selected assets. For combined products, use `area: all`. The workflow itself has read-only permissions and stores a report. Existing manual GitHub releases and tag creation stay under repository owner control. Enforcing this workflow for those channels also requires configuring the publication workflow and repository permissions.

## Generated musical questions

```sh
python -B scripts/audit_randomized_music.py --seed 20261121 --trials 128 --json-out /tmp/steps-music-audit.json
```

The Python CI suite runs 128 generated questions per area with a fixed seed.
The theory release gate also executes the six theory probes. Repeat a
failure using its seed and area. The JSON report records the exact inputs,
expected and observed results, Python version and checked revision. For an
additional sample, choose a different seed. The [audit notes](../audit/2026-11-21/RANDOMIZED_MUSIC.md)
describe the independent formulas, covered input families and review limits.

## Record independent musical evidence

1. Open the exact revision to be released and generate a checklist with `python -B scripts/verify_musical_release.py --area AREA --template`. Use the corresponding [benchmark prompts and rubrics](../../knowledge/benchmark/cases.json).
2. An authorized specialist who did not author the reviewed material checks the actual musical output. Record each criterion, observations, an evidence permalink, and at least one source with an exact locator and the statement it supports. For a Coach case, include the actual answer, model, Skill revision and run evidence. A reviewer may record a failed criterion to make the reason for withholding release explicit.
3. Post the completed JSON alone in a fenced `steps-musical-review` block as a comment on the STEPS pull request for the revision. Set `independent` to `true` only after confirming independence. Supply the comment permalink to `--review-comment` or enter the per-area permalinks separated by spaces in the workflow. Use a new comment for a corrected assessment.
4. The gate verifies the comment through GitHub, checks the existing pilot reviewer allowlist, compares the reviewer with the PR author and checks the exact PR head or completed merge revision. It rejects edited comments, missing criteria and evidence from a different revision. Changes to the reviewed revision require new evidence. The specialist remains responsible for the musical judgment and for declaring any involvement beyond PR authorship.

Source URLs and locators make a review traceable. They do not assert redistribution rights or prove that the reviewer’s musical judgment is correct. [Rights, security and release](RIGHTS_SECURITY_AND_RELEASE.md)
