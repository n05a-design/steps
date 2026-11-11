# STEPS Security Scanner Validation & Hardening Report (Phase 4.15)

**Date**: 2026-11-11  
**Phase**: STEPS Phase 4.15  
**Topic**: Secret Scanner Architecture, CI Failure Remediation, Bounded Test Fixtures, and Fail-Closed Guardrails  
**Status**: **VERIFIED COMPLETE**

---

## 1. Executive Summary & Incident Forensics

On commit `d7d7f1e1df0ba78c828e2671cd695ddb88c5ce2e` (Branch `fix/steps-phase4-14-knowledge-integrity`), GitHub Actions executed two CI workflows:
1. `structure`: Check-run ID `130398345023` -> **SUCCESS**
2. `scan-secrets`: Check-run ID `130398345273` -> **FAILURE**

### Root Cause Analysis:
The secret scan workflow in Phase 4.14 walked the entire repository without accounting for pre-existing historical third-party web downloads located in `research/STEPS_Bibliothek/` (archived Ableton blog articles committed in commit `a14c3f3`). These third-party HTML/JS files contain third-party embedded Google Maps API keys and AWS bucket keys. Because no quarantined baseline existed in the scanner, CI correctly triggered fail-closed and rejected the build.

Furthermore, on Windows platforms, path normalization discrepancies (`replace('\\', '/').lstrip('./')`) led to mismatched keys when querying baseline dictionaries.

---

## 2. Hardened Architecture & Quarantined Baseline

To resolve the CI failure without deleting historical research assets (strictly forbidden by Rule 2: Preservation-First), Phase 4.15 implemented a dual-layer security architecture:

### 2.1 Quarantined Historical Baseline (`scripts/historical_secret_baseline.json`)
- **Entries**: 33 verified historical third-party leaks.
- **Scope**: Exclusively third-party static assets in `research/STEPS_Bibliothek/` under active tracking in open work instructions:
  - `OA-0001`: Historical Ableton blog asset cleanup / redaction plan.
  - `OA-0033`: Historical third-party secret remediation and quarantine.
- **Fail-Closed Locking**: The baseline is locked to specific `(normalized_file_path, line_number, pattern_description)`. Any new file, modified line, or new secret in an existing file is immediately flagged as a new leak.

### 2.2 Strict Bounded Test Fixture Allowlist
Earlier proposals suggested blanket keyword exemptions (e.g. ignoring lines with comments `# SYNTHETIC_TEST` or skipping all files in `tests/`). Such exemptions represent severe security vulnerabilities, as a developer could inadvertently commit a real token inside a test file or bypass scanning with a comment.

**Hardened Policy**:
1. Blanket directory or comment-based bypasses are **strictly prohibited**.
2. Only exact, pre-authorized synthetic tokens are permitted:
   - `AIzaSy` + `FakeSyntheticTestKeyForCI00000000`
   - `AKIA` + `IOSFODNN7EXAMPLE`
   - `ghp_` + `FakeSyntheticGitHubTokenForCI1234567`
3. These tokens are only permitted within designated fixture paths:
   - `tests/test_secret_scanner.py`
   - `tests/fixtures/synthetic_secrets.json`
4. Any real token, unknown token, or authorized token in any non-fixture file is immediately blocked.

This behavior is verified by unit test `test_scan_diff_content_blocks_unauthorized_secret_even_in_test_fixtures`:
```python
def test_scan_diff_content_blocks_unauthorized_secret_even_in_test_fixtures(self):
    unauthorized_key = "AIzaSy" + "RealUnapprovedSecretKey000000000"
    diff_text = f"+REAL_KEY = '{unauthorized_key}'\n"
    leaks = scanner.scan_diff_content("tests/test_secret_scanner.py", diff_text)
    self.assertEqual(len(leaks), 1)
```

---

## 3. Tooling Implementation

### 3.1 Pre-Commit Hook (`scripts/pre-commit-secret-check.py`)
- Scans `git diff --cached` before commit creation.
- Normalizes Windows and POSIX path separators.
- Applies strict masking: secrets are never logged in plain text (`AIzaSy...XXXX` or `***REDACTED***`).
- Exits with status `1` upon detecting any unauthorized pattern.

### 3.2 CI Workflow (`.github/workflows/secret-scan.yml`)
- Executes on push and pull request to all branches.
- Loads `scripts/historical_secret_baseline.json`.
- Traverses all repository text files (`.py`, `.html`, `.js`, `.json`, `.md`, `.yml`, `.csv`, `.sh`, `.ps1`).
- Produces GitHub Action error annotations for any new leak.
- Exits with status `1` on read errors or new leaks.

---

## 4. Empirical Verification Results

Running the scanner against the complete repository tree:
```text
Loaded 33 quarantined baseline items
Result: 33 quarantined, 0 new leaks, 0 read errors.
SUCCESS: Zero unmasked secrets detected across all repository files.
```

Unit Test Results (`tests/test_secret_scanner.py`):
```text
test_negative_clean_lines ... ok
test_scan_diff_content_blocks_unauthorized_secret_even_in_test_fixtures ... ok
test_scan_diff_content_detects_secret_without_keyword_bypass ... ok
test_scan_diff_content_permits_authorized_synthetic_mock_secret ... ok
test_secret_masking ... ok
test_synthetic_positive_matches ... ok

Ran 6 tests in 0.003s - OK
```
