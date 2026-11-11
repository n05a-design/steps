# 09 – Fehlerregister, Risiken & Widersprüche (ISSUES_RISKS_AND_CONTRADICTIONS)

**Projekt:** STEPS – System zur Theorie-gestützten Erkundung von Progressionen und Skalen  
**Dokumenttyp:** Register aller identifizierten, behobenen und noch offenen Fehler und Risiken  

---

## 1. Register behobener Fehler (ERR-001 bis ERR-037 & Technische Issues)

| Problem-ID | Komponente | Beschreibung | Ursache | Behoben in | Status |
|---|---|---|---|---|:---:|
| `ERR-001` bis `ERR-037` | `knowledge/` | 37 musikalische Fachfehler in Skalen, Intervallen und Akkorden | Ursprüngliche fehlerhafte Recherche | Commit `918d0a7` | **BEHOBEN** |
| `ISSUE-BOM` | `knowledge/research/*.csv` | `KeyError: 'error_id'` bei `csv.DictReader` | Windows/Excel UTF-8 Byte Order Mark (`\xef\xbb\xbf`) | Commit `918d0a7` | **BEHOBEN** |
| `ISSUE-CSUS4` | `src/steps/theory/chord.py` | `Csus4` fälschlich als deutsches `C-flat us4` geparst | RegEx-Kollision bei deutschem Vorzeichen `'s'` (Es, As) | Commit `fe66637` | **BEHOBEN** |
| `ISSUE-BVI-MIN` | `src/steps/progression/engine.py` | `bVI` in d-Moll ergab Bbb statt Bb | Doppelte Vorzeichenanwendung bei Moll-Skalenstufe 6 | Commit `fe66637` | **BEHOBEN** |
| `ISSUE-SEC-SCAN` | `scripts/pre-commit-secret-check.py` | Syntax-Warnung bei Windows-Backslash in String | Unescaped Backslash im Pfadnormalisierer | Commit `c25b667` | **BEHOBEN** |
| `ISSUE-TEST24` | `.agents/.../tests/` | Test 24 schlug fehl bei Hinzufügen von Task 21 | Fester Schwellenwert `== 20` statt `>= 21` | Commit `031ddc1` | **BEHOBEN** |
| `ISSUE-ADR-DESYNC` | `knowledge/architecture/` | ADR-001 bis ADR-012 fehlten in einer Branch-Version | Unvollständige Zwischenreconciliation | Commit `422ec96` | **BEHOBEN** |
| `ISSUE-LYDIAN-DOM` | `src/steps/theory/seventh.py` | Unklarheit über Quint-Präsenz in 7#11 Akkorden | Vermischung von Theorie (mit 5) und Voicing (ohne 5) | Commit `fe66637` | **BEHOBEN** |

---

## 2. Offene technische und organisatorische Risiken

### 1. ADR-001 Owner Sign-Off (GUI-Framework)
- **Risiko:** Vorzeitige Bindung an PySide6 oder Tkinter könnte zu Refactoring-Aufwand führen, wenn der Project Owner ein anderes Framework (z. B. Web-basiertes Tauri/Electron) bevorzugt.
- **Gegenmaßnahme:** Eingehaltene Gating-Regel (ADR-004). Der bisherige Code in `src/steps/` ist zu 100 % headless und unabhängig vom GUI-Framework.

### 2. GitHub Actions Queue-Latenz auf kostenlosen Runnern
- **Risiko:** Jobs in öffentlichen/kostenlosen GitHub Actions Organisationen geraten gelegentlich in Wartezustände, wenn viele Workflows parallel laufen.
- **Gegenmaßnahme:** Lokale Verifikation über Unittest-Suiten und Pre-Commit-Skripte sichert volle Testbarkeit auch offline ab.

### 3. Abgrenzung zum externen Projekt Glide
- **Risiko:** Versehentliches Hineinkopieren von Glide-Code (Tkinter Desktop Planer) in das STEPS-Repository.
- **Gegenmaßnahme:** Striktes Einhalten von Regel 9 (Decouple Glide) und kontinuierliche Überprüfung durch `check_structure.py`.
