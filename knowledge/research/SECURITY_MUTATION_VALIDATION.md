# STEPS – Security Mutation & Fail-Closed Guardrail Validation (Phase 4.17)

**Datum:** 2026-11-11  
**Status:** ALL 15 NEGATIVE MUTATION TESTS PASSED (Gate 5 Passed)  
**Testsuite:** `tests/test_secret_scanner.py`  
**Referenzdokument:** Phase 4.17 Master Prompt, Teil IV (Abschnitt 4.4)  

---

## 1. Übersicht & Zielsetzung

Ein Secret-Scanner erfüllt seinen Zweck nur dann verlässlich, wenn künstlich injizierte Angriffsvektoren und Sabotagemuster reproduzierbar abgefangen werden.

In `tests/test_secret_scanner.py` wurden alle 15 in Abschnitt 4.4 des Master Prompts geforderten negativen und positiven Kontrollmutationen implementiert:

---

## 2. Detaillierte Matrix der 15 Sicherheits-Mutationstests

| Test-Methode | Geprüfter Angriffsvektor / Mutation | Erwartetes Verhalten | Gemessenes Ergebnis | Status |
|---|---|---|---|:---:|
| `test_01_exact_baseline_entry_allowed` | Quarantänisierter Eintrag mit exaktem Pfad, Zeile und Hash | Befreiung (`QUARANTINED_HISTORICAL_BASELINE`) | Quarantänisiert | **PASS** |
| `test_02_new_secret_at_historical_position_blocked` | Neues Secret auf historischer Baseline-Zeile (DEF-4.16-04) | Abbruch (`TAMPERED_SECRET_ON_BASELINE_LINE`) | Blockiert | **PASS** |
| `test_03_new_secret_in_known_archive_file_blocked` | Altes Secret in bekannte Archivdatei auf neue Zeile kopiert | Abbruch (`UNREGISTERED_SECRET_LEAK`) | Blockiert | **PASS** |
| `test_04_new_secret_in_new_file_type_detected` | Secret in neuem Dateityp (`.sh`, `.ps1`, `.yaml`) | Erkennung und Abbruch | Erkannt & blockiert | **PASS** |
| `test_05_new_secret_in_agent_skill_file_blocked` | Secret in `.agents/skills/...` (DEF-4.16-05) | Vollständige Durchsuchung von `.agents/` | Blockiert | **PASS** |
| `test_06_modified_historical_hash_blocked` | Künstlich veränderter `secret_sha256` in Baseline | Hash-Mismatch löst Alarm aus | Blockiert | **PASS** |
| `test_07_corrupted_json_baseline_fails_closed` | Beschädigte JSON-Syntax in der Baseline-Datei | Fail-Closed (`JSONDecodeError` / Exit 1) | Fail-Closed | **PASS** |
| `test_08_missing_baseline_file_fails_closed` | Fehlende `historical_secret_baseline.json` | Fail-Closed (`FileNotFoundError` / Exit 1) | Fail-Closed | **PASS** |
| `test_09_invalid_or_noncanonical_file_path_blocked` | Secret in bisher ungetracktem Quellcode-Pfad | Erkennung als unregistriertes Leak | Blockiert | **PASS** |
| `test_10_manipulated_line_number_blocked` | Manipulierte Zeilennummer bei echtem Token | Keine Baseline-Befreiung | Blockiert | **PASS** |
| `test_11_multiple_matches_in_one_line_handled` | Mehrere Secrets auf einer einzigen Zeile | Isolierte Erkennung jedes Treffers | Erkannt | **PASS** |
| `test_12_unreadable_file_fails_closed` | E/A- oder Berechtigungsfehler beim Dateilesen | Fail-Closed (kein stiller Bypass) | Fail-Closed | **PASS** |
| `test_13_unexpected_binary_file_handled_safely` | Unerwartete Binärzeichenketten / UTF-8 Replacement | Sicherer Scan ohne Absturz | Bestätigt | **PASS** |
| `test_14_unauthorized_baseline_modification_blocked` | Unautorisierte Modifikation der Baseline | Sofortiger Alarm bei Drift | Blockiert | **PASS** |
| `test_15_clean_file_produces_zero_false_positives` | Regulärer Code / Dokumentation | Exakt 0 Fehlalarme | 0 Fehlalarme | **PASS** |

---

## 3. Scanner-Abdeckung & Ergänzende Werkzeuge

Der integrierte Python-Regex-Scanner (`scripts/pre-commit-secret-check.py` und `.github/workflows/secret-scan.yml`) deckt die unmittelbaren Risiken im CI-Zyklus zuverlässig ab:
1. **Scoping:** Überwacht `.py`, `.js`, `.sh`, `.ps1`, `.md`, `.json`, `.yaml`, `.yml`, `.csv`, `.html`, `.download`.
2. **Pre-Commit Guard:** Verhindert das lokale Staging von unmaskierten Geheimnissen vor dem Git-Commit.
3. **Ergänzende Empfehlung:** Für historische Deep-Scans über alle vergangenen Git-Commits vor einer Open-Source-Veröffentlichung wird die Ausführung von `gitleaks detect --source=. -v` oder `trufflehog git file://.` empfohlen.
