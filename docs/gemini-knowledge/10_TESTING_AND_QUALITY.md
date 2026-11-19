# Testing and Quality Evidence

**Baseline commit:** `00f4d5b9079575260c9f26d6d0f3305ab15e241a`
**Audit date:** 2026-11-19
**Status:** TESTED — repository reports 746 unittest tests passing; manual product and release gates remain PARTIAL or NOT_RUN.
**Status key:** IMPLEMENTED = exists; TESTED = automated evidence; PARTIAL = incomplete; PLANNED = future; BLOCKED = decision or dependency; HISTORICAL = dated state; NOT_EVIDENCED = insufficient evidence.

## Test evidence

The core suite was run for this audit: `python3 -B -m unittest discover -s tests -p 'test_*.py'` — **746 tests, PASS**. The pilot benchmark was also run: `python3 -B scripts/run_knowledge_benchmark.py --scope pilot` — **PASS 8, FAIL 0, PENDING 0**. The repository includes tests and CI for theory, notation, progression, storage, MIDI, localization, knowledge review, UI, packaging, security and structure. Do not generalize these results into all platforms or human acceptance.

## Reproducible local checks

```sh
python3 -B -m unittest discover -s tests -p 'test_*.py'
python3 -B -m unittest discover -s .agents/skills/steps-knowledge-curation/tests -v
python3 -B scripts/run_knowledge_benchmark.py --scope pilot
python3 -B scripts/check_gemini_knowledge_pack.py --check
```

More commands and intent are documented in `tests/README.md`. CI includes `.github/workflows/python-tests.yml`; relevant workflows run multiple Python versions and platform smoke checks. Exact job results for all CI matrices are NOT_RECORDED in this pack.

## Benchmark inventory

`knowledge/benchmark/cases.json` has 119 cases: 8 pilot, 25 catalog, 51 sample, 12 coach, 3 publication, 7 API and 13 backlog. The supplied pilot result is 8/0. Benchmark case counts describe test inventory, not human sign-off. The benchmark documentation notes that manually reviewed claims and some coach/sample assessments can remain pending.

## Separate quality dimensions

| Dimension | Evidence / status |
|---|---|
| Unit/integration behavior | TESTED, reported 746 passing |
| Pilot benchmark | TESTED, supplied 8 PASS / 0 FAIL |
| Other benchmark scope results | NOT_REPORTED here; inventory only |
| Translation review | PARTIAL / NOT_EVIDENCED as human acceptance |
| Music-theory expert review | PARTIAL; only explicitly approved content is approved |
| Independent DAW import | NOT_EVIDENCED in supplied evidence |
| Native accessibility and user research | NOT_RUN / NOT_EVIDENCED |
| Installer/signing/release acceptance | NOT_EVIDENCED |

## Rule

Never reinterpret a planned quality gate as a pass. Report exact command and exact outcome for tests actually run. Human review, research, rights decisions, native UI assessment and publication remain separate from automated tests. See `docs/quality/VERIFICATION_PLAN_V2.md` and `docs/quality/QUALITY_GATES.md`.
