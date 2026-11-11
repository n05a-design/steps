# 07 – Technischer Änderungsverlauf (CHANGES_AND_IMPLEMENTATIONS)

**Projekt:** STEPS – System zur Theorie-gestützten Erkundung von Progressionen und Skalen  
**Dokumenttyp:** Rekonstruktion aller technischen Code- und Strukturänderungen  

---

## 1. Systematische Änderungsmatrix (CHG-001 bis CHG-025)

| Änderungs-ID | Commit-SHA | Betroffene Komponenten | Zweck & Technische Umsetzung | Test / Nachweis |
|---|---|---|---|---|
| `CHG-001` | `078bc59` | `src/steps/`, `pyproject.toml` | Scaffolding des reinen Python-Pakets STEPS (Task T-04) | `check_structure.py` |
| `CHG-002` | `190228a` | `main` | Merge von PR #4 (Package Scaffold T-04) | CI Build Grün |
| `CHG-003` | `1dbe1ce` | `.agents/skills/steps-knowledge-curation/` | Initiale Implementierung des Wissens-Kuratierungs-Skills | Skill Schema |
| `CHG-004` | `513fa9c` | `.agents/skills/...` | Härtung der Validierungsskripte, 18-Szenarien-Testsuite | 18 Unittests |
| `CHG-005` | `af6c0bc` | `.agents/skills/...` | Härtung gegen Pfadgrenzenverletzungen und Symlink-Traversal | 23 Unittests |
| `CHG-006` | `1e52af7` | `.agents/skills/...` | Hinzufügen von `backup_knowledge.py` und 25 Unittests | 25 Unittests |
| `CHG-007` | `aa8fba1` | `.github/workflows/structure-check.yml` | Einbindung von Unittest-Ausführung in CI Workflow | CI Ausführung |
| `CHG-008` | `dbd319a` | `main` | Merge von PR #5 (Knowledge Curation Skill) | CI Build Grün |
| `CHG-009` | `e2826fe` | `main` | Merge von PR #6 (CI Path Normalization) | CI Build Grün |
| `CHG-010` | `031ddc1` | `.agents/.../tests/` | Anpassung von Test 24 an dynamische Aufgabenerweiterung ($\ge 21$) | 25 Unittests |
| `CHG-011` | `a4b87f6` | `knowledge/` | Verifizierter Research-Checkpoint Phase 4.13 | Git Checkpoint |
| `CHG-012` | `88c506a` | `knowledge/` | Erweiterung des Unified Concept Graphs und Referenzbibliotheken | Graph Validierung |
| `CHG-013` | `d7d7f1e` | `tests/test_golden_reference_cases.py` | Reparatur von Referenz-IDs, Behebung von Scheinerfolgen | Golden Tests |
| `CHG-014` | `7cc8705` | `knowledge/research/canonical/` | Arretierung von 198 Referenzidentitäten mit SHA-256 Hashes | Hash-Verifikation |
| `CHG-015` | `c25b667` | `scripts/pre-commit-secret-check.py` | Robuste Pfadnormalisierung mit `chr(92)` statt Backslash-Literal | Test Suite Secret Scanner |
| `CHG-016` | `c4313ba` | `tests/`, `scripts/` | Fail-Closed Secret Scanner mit historischer Baseline-Quarantäne | 15 Security Tests |
| `CHG-017` | `422ec96` | `knowledge/architecture/`, `knowledge/research/` | Wiederherstellung von ADR-001..012, Bewahrung von PROG-021 | ADR Tabellen |
| `CHG-018` | `918d0a7` | Gesamtes Repo | Master-Audit: 3947 Dateien, 37 Fehler bereinigt, BOM entfernt | Revisionspaket |
| `CHG-019` | `bb14fce` | `src/steps/theory/`, `src/steps/progression/` | Phase 4.18 Master-Integration, Initialer Theoriekern, 89 Tests | 89 Unittests |
| `CHG-020` | `fe66637` | `src/steps/theory/exceptions.py` | Hierarchie domänenspezifischer Fehlerklassen | `test_theory_core.py` |
| `CHG-021` | `fe66637` | `src/steps/theory/pitch.py` | Deutsche Notenbezeichnungen, Enharmonik-Prädikate, Transpositionen | `test_theory_core.py` |
| `CHG-022` | `fe66637` | `src/steps/theory/interval.py` | Zusammengesetzte Intervalle (None, Undezime, Tredezime), Transposition | `test_theory_core.py` |
| `CHG-023` | `fe66637` | `src/steps/theory/chord.py` | Umfassender Leadsheet-Parser, Lydian Dominant Formel vs. Voicing | `test_theory_core.py` |
| `CHG-024` | `fe66637` | `src/steps/progression/engine.py` | 28 kanonische Progressionen, Stufenauflöser, Voicing-Sequenzer | `test_progression_engine.py` |
| `CHG-025` | `fe66637` | `.github/workflows/python-tests.yml` | Remote GitHub Actions CI Workflow für Python 3.11 und 3.12 | Remote CI |
