# STEPS – Security Baseline Mutation Tests & Verification (Phase 4.16)

**Datum:** 2026-11-11  
**Status:** ALL 12 TESTS PASSING  
**Testsuite:** `tests/test_secret_scanner.py`  
**Referenzdokument:** Phase 4.16 Master Prompt, Teil V  

---

## 1. Übersicht der 12 Sicherheits-Mutationstests

Zur Validierung der Härtung von `.github/workflows/secret-scan.yml` und `scripts/pre-commit-secret-check.py` wurden in `tests/test_secret_scanner.py` 12 isolierte Testfälle implementiert:

| Test-Methode | Geprüftes Verhalten | Erwartetes Ergebnis | Gemessenes Ergebnis | Status |
|---|---|---|---|:---:|
| `test_01_exact_baseline_entry_allowed` | Quarantänisierter Eintrag mit exaktem Pfad, Zeile und SHA-256 | Erlaubt (`QUARANTINED_HISTORICAL_BASELINE`) | Erlaubt | **PASS** |
| `test_02_modified_secret_on_exempt_line_blocked` | Neues Secret auf historischer Zeile (DEF-4.16-04) | Blockiert (`TAMPERED_SECRET_ON_BASELINE_LINE`) | Blockiert | **PASS** |
| `test_03_old_secret_moved_to_new_line_blocked` | Altes Secret auf andere Zeilennummer verschoben | Blockiert (`UNREGISTERED_SECRET_LEAK`) | Blockiert | **PASS** |
| `test_04_old_secret_moved_to_new_file_blocked` | Altes Secret in neue Datei kopiert | Blockiert (`UNREGISTERED_SECRET_LEAK`) | Blockiert | **PASS** |
| `test_05_missing_baseline_file_fails_closed` | Baseline-Datei existiert nicht | Fail-Closed (`FileNotFoundError` / Exit 1) | Fail-Closed | **PASS** |
| `test_06_corrupted_json_baseline_fails_closed` | Baseline-Datei enthält korruptes JSON | Fail-Closed (`JSONDecodeError` / Exit 1) | Fail-Closed | **PASS** |
| `test_07_tampered_baseline_hash_blocked` | Baseline-Hash stimmt nicht mit dem Secret überein | Blockiert (`TAMPERED_SECRET_ON_BASELINE_LINE`) | Blockiert | **PASS** |
| `test_08_new_secret_in_agents_directory_blocked` | Secret im Verzeichnis `.agents/` abgelegt (DEF-4.16-05) | Blockiert (wird gescannt, nicht ignoriert) | Blockiert | **PASS** |
| `test_09_real_leak_pattern_google_api_key_detected` | Erkennungsgenauigkeit für Google Cloud API Key | Regex matcht zuverlässig | Bestätigt | **PASS** |
| `test_10_real_leak_pattern_aws_key_detected` | Erkennungsgenauigkeit für AWS Access Key ID | Regex matcht zuverlässig | Bestätigt | **PASS** |
| `test_11_clean_file_without_secrets_allowed` | Regulärer Code / Dokumentation | Keine False Positives (0 Leaks) | 0 Leaks | **PASS** |
| `test_12_line_hash_integrity_verification` | Integrität des `line_sha256`-Feldes in der Baseline | 64-Zeichen Hex-Hash vorhanden | Vorhanden | **PASS** |

---

## 2. Testausführung

```text
test_01_exact_baseline_entry_allowed (tests.test_secret_scanner.TestSecretScannerSecuritySuite) ... ok
test_02_modified_secret_on_exempt_line_blocked (tests.test_secret_scanner.TestSecretScannerSecuritySuite) ... ok
test_03_old_secret_moved_to_new_line_blocked (tests.test_secret_scanner.TestSecretScannerSecuritySuite) ... ok
test_04_old_secret_moved_to_new_file_blocked (tests.test_secret_scanner.TestSecretScannerSecuritySuite) ... ok
test_05_missing_baseline_file_fails_closed (tests.test_secret_scanner.TestSecretScannerSecuritySuite) ... ok
test_06_corrupted_json_baseline_fails_closed (tests.test_secret_scanner.TestSecretScannerSecuritySuite) ... ok
test_07_tampered_baseline_hash_blocked (tests.test_secret_scanner.TestSecretScannerSecuritySuite) ... ok
test_08_new_secret_in_agents_directory_blocked (tests.test_secret_scanner.TestSecretScannerSecuritySuite) ... ok
test_09_real_leak_pattern_google_api_key_detected (tests.test_secret_scanner.TestSecretScannerSecuritySuite) ... ok
test_10_real_leak_pattern_aws_key_detected (tests.test_secret_scanner.TestSecretScannerSecuritySuite) ... ok
test_11_clean_file_without_secrets_allowed (tests.test_secret_scanner.TestSecretScannerSecuritySuite) ... ok
test_12_line_hash_integrity_verification (tests.test_secret_scanner.TestSecretScannerSecuritySuite) ... ok

----------------------------------------------------------------------
Ran 12 tests in 0.006s

OK
```
