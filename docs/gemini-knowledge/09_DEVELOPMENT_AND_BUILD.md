# Development and Build

**Baseline commit:** `00f4d5b9079575260c9f26d6d0f3305ab15e241a`
**Audit date:** 2026-11-19
**Status:** IMPLEMENTED — Python package metadata and development workflows exist; desktop distribution is PARTIAL / NOT_EVIDENCED.
**Status key:** IMPLEMENTED = exists; TESTED = automated evidence; PARTIAL = incomplete; PLANNED = future; BLOCKED = decision or dependency; HISTORICAL = dated state; NOT_EVIDENCED = insufficient evidence.

## Environment and entry points

The project declares Python `>=3.11` in `pyproject.toml`. Development identifier is `0.2.0-dev` (`0.2.0.dev0` in package metadata). Run from the repository root:

```sh
python3 -m app.main --headless
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
```

The GUI entry point is `python3 -m app.main` and requires Tk plus a graphical environment. See `README.md`, `CONTRIBUTING.md`, `tests/README.md`, and `.github/workflows/python-tests.yml`.

## Build and artifact boundaries

`pyproject.toml` configures a Python package/entry point. `tests/test_package_artifacts.py` builds and inspects a wheel. This is not evidence of a complete signed desktop installer, notarization, or acceptance on supported end-user systems.

## CI

`.github/workflows/python-tests.yml` runs Python test matrices and checks generated docs, localization inventories, package artifacts, knowledge benchmarks and coverage audits. Workflow outcomes are commit- and runner-specific; this pack's audit did not independently verify every matrix runner.

## Safe development rules

Keep application integration in `app/`, domain behavior in `src/steps/`, and reviewed facts in `knowledge/`. Preserve the existing schema, locale, source and security gates. Do not install dependencies unless a changed manifest or missing dependency requires it. Do not confuse `v0.1.0`, development metadata, schema version, or V6.6/V6.7 research archives.

## Not included in this audit

Native installation, signing, fresh-machine packaging and artifact reproducibility were NOT_RUN as manual release gates. Consult `docs/IMPLEMENTATION.md`, `docs/quality/QUALITY_GATES.md`, and [testing and quality](10_TESTING_AND_QUALITY.md).
