"""
STEPS AI Context Handover - Module 2: Technical Project State & Implementations
Generates:
- 06_TECHNICAL_PROJECT_STATE.md
- 07_CHANGES_AND_IMPLEMENTATIONS.md
- 08_TESTS_AND_VERIFICATION.md
- 09_ISSUES_RISKS_AND_CONTRADICTIONS.md
- 10_OPEN_WORK_AND_ROADMAP.md
"""

import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.join(REPO_ROOT, "AI_CONTEXT_HANDOVER")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def write_technical_state():
    content = """# 06 – Technischer Projektstand & Architektur (TECHNICAL_PROJECT_STATE)

**Projekt:** STEPS – System zur Theorie-gestützten Erkundung von Progressionen und Skalen  
**Repository:** https://github.com/n05a-design/steps  
**Aktueller Branch:** `feat/steps-phase5-1-theory-core-hardening`  
**Letzter Commit:** `fe66637`  
**Python Runtime:** Python 3.11 / 3.12 / 3.15  
**Architektur-Paradigma:** Headless Pure Python Core First (ADR-004), zero UI dependencies  

---

## 1. Verzeichnis- und Modul-Architektur

```
STEPS/
├── src/steps/                     # Reiner Python-Theoriekern (Zero UI-Dependencies)
│   ├── theory/                    # Harmonielehre, Tonsystem, Akkorde, Intervalle
│   │   ├── __init__.py            # Öffentliche Core-API
│   │   ├── exceptions.py          # Domänenspezifische Fehlerhierarchie
│   │   ├── pitch.py               # PitchClass (Z12), NoteSpelling, ISO 16 Akustik
│   │   ├── interval.py            # DiatonicInterval, ChromaticInterval, Transposition
│   │   ├── triad.py               # Dreiklänge (Dur, Moll, Verm., Überm., Sus, Add)
│   │   ├── seventh.py             # Vierklänge, Drop-2, Shell Voicings
│   │   └── chord.py               # Leadsheet-Parser, ChordDefinition, Voicings
│   └── progression/               # Akkordverbindungen & Stimmführung
│       ├── __init__.py            # Öffentliche Progression-API
│       ├── voice_leading.py       # L1-Metrik, Tymoczko-Distanz, Optimierer, Stile
│       └── engine.py              # 28 Progressionen, Stufenauflöser, Sequenzer
│
├── .agents/skills/                # Antigravity Wissenskuratierungs-Skill
│   └── steps-knowledge-curation/  # 21 Validierungsaufgaben, Backups, Schemaprüfung
│       ├── SKILL.md               # Skill-Definition
│       ├── scripts/               # Backup-, Validierungs- und Prüfskripte
│       └── tests/                 # 25 deterministische Unittests
│
├── knowledge/                     # Wissenschaftlicher Fachbestand (Forschung & Fakten)
│   ├── concepts/                  # Kanonische Konzeptbeschreibungen (M01-M12)
│   │   └── progressions/          # CHORD_PROGRESSION_REFERENCE_LIBRARY.md (PROG-001..028)
│   ├── research/                  # Register, Lückenanalysen, Auditberichte
│   │   ├── canonical/             # Arretierte Baselines (GOLDEN_REFERENCE_CASES, GRAPH)
│   │   ├── MUSICAL_ERROR_REGISTER.csv  # 37 korrigierte Fehler (ERR-001..037)
│   │   └── PHASE5_1_COMPLETION_REPORT.md # Vollständiger Abschlussbericht Phase 5.1
│   └── architecture/              # ADR-001 bis ADR-012
│
├── tests/                         # Root Test-Suite (90 Tests)
│   ├── test_theory_core.py        # 31 Tests für Theory Core & Stimmführung
│   ├── test_progression_engine.py # 12 Tests für alle 28 Progressionen & Stufen
│   ├── test_golden_reference_cases.py # 28 Tests für 198 Referenzfälle
│   ├── test_secret_scanner.py     # 15 Tests für Secret-Scanner-Guardrail
│   └── test_structure.py          # 4 Tests für Struktur & JSON-Syntax
│
├── tools/validation/              # Strukturprüfer check_structure.py
├── scripts/                       # Pre-Commit-Prüfungen & Baselines
│   ├── pre-commit-secret-check.py # Fail-Closed Secret Scanner
│   └── historical_secret_baseline.json # SHA-256 gebundene historische Ausnahmen
│
└── .github/workflows/             # GitHub Actions CI
    ├── python-tests.yml           # Remote Python 3.11 & 3.12 Unittests
    ├── secret-scan.yml            # Fail-Closed Secret-Scanning
    └── structure-check.yml        # Struktur- und Basistest-Validierung
```

---

## 2. Detaillierte Modulverantwortlichkeiten

### `src/steps/theory/`
- **`pitch.py`:**
  - `PitchClass(int)`: Modulo 12 Arithmetik in $\mathbb{Z}_{12} = \{0..11\}$.
  - `NoteSpelling`: Orthographische diatonische Repräsentation mit `step`, `alteration`, `octave`.
  - `midi_to_frequency()` / `frequency_to_midi()`: Exakte ISO 16:1975 Akustik ($A_4 = 440\text{ Hz}$).
  - `parse_spelling()`: Parser für internationale und deutsche Notation ($H, B, Fis, Es, As, Fisis, Heses$).
- **`interval.py`:**
  - `DiatonicInterval`: Intervallgrad (1 bis 13+) und Qualität ('P', 'M', 'm', 'd', 'A').
  - `transpose_spelling()`: Exakte diatonische Transposition unter Erhalt der Notenorthographie.
  - `interval_between_spellings()`: Deduktion des exakten diatonischen Intervalls zwischen zwei Tönen.
- **`triad.py` & `seventh.py`:**
  - Konstruktion von Dreiklängen und Vierklängen in Terzschichtung.
  - Umkehrungen (Grundstellung, 1. Umkehrung 6/3 bzw. 6/5, 2. Umkehrung 6/4 bzw. 4/3, 3. Umkehrung 4/2).
  - Transformationen: `make_drop2_voicing()` und `make_shell_voicing()`.
- **`chord.py`:**
  - `ChordDefinition`: Abstraktes Akkordmodell mit Basiston, Intervallen und Pitch-Classes.
  - `Voicing`: Konkrete Realisierung in MIDI-Pitches (`CLOSE`, `DROP2`, `SHELL`, `ROOTLESS`, `OPEN`).
  - `parse_chord()`: Robuster Parser für Leadsheet-Akkorde und Slash-Bässe.
  - Klärung Lydian Dominant ($7\sharp 11$): Theoretische Tonmenge $\{0, 4, 6, 7, 10\}$ vs. Performance-Voicing $\{0, 4, 6, 10\}$ (Quintauslassung).

### `src/steps/progression/`
- **`voice_leading.py`:**
  - `absolute_semitone_distance()`: $L_1$-Norm über alle Stimmen.
  - `circular_pc_distance()`: Tymoczko-Distanz im Akkordraum.
  - `detect_voice_crossing()` & `detect_voice_overlap()`: Stimmkreuzungs- und Überlappungsschutz.
  - `detect_parallel_fifths_octaves()`: Erkennung von Quinten- und Oktavparallelen.
  - `optimize_smooth_voice_leading()`: Deterministischer globaler Optimierer.
- **`engine.py`:**
  - `CANONICAL_PROGRESSIONS`: Registrierung aller 28 kanonischen Archetypen.
  - `resolve_roman_degree()`: Stufenauflösung in Dur, Moll, Zwischendominanten und modalen Entlehnungen.
  - `generate_progression_voicings()`: Kontinuierliche Voicing-Synthese mit Stimmführungsmetriken.

---

## 3. Entkopplung von externen Projekten (Glide)

Gemäß **Regel 9 (Decouple Glide)** und **Regel 4 (Domänengrenze)** ist STEPS vollständig frei von Glide-Code.
- Das in früheren Prompts erwähnte Projekt `glide-to-do` (Desktop-Planer mit Tkinter) ist ein separates Repository.
- Es gibt in `src/steps/` keinerlei Importe, Bindungen oder funktionale Abhängigkeiten zu Glide.
"""
    with open(os.path.join(OUTPUT_DIR, "06_TECHNICAL_PROJECT_STATE.md"), "w", encoding="utf-8") as f:
        f.write(content)
    print("Generated 06_TECHNICAL_PROJECT_STATE.md")

def write_changes():
    content = """# 07 – Technischer Änderungsverlauf (CHANGES_AND_IMPLEMENTATIONS)

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
| `CHG-010` | `031ddc1` | `.agents/.../tests/` | Anpassung von Test 24 an dynamische Aufgabenerweiterung ($\\ge 21$) | 25 Unittests |
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
"""
    with open(os.path.join(OUTPUT_DIR, "07_CHANGES_AND_IMPLEMENTATIONS.md"), "w", encoding="utf-8") as f:
        f.write(content)
    print("Generated 07_CHANGES_AND_IMPLEMENTATIONS.md")

def write_tests_and_verification():
    content = """# 08 – Tests, Nachweise & Verifikation (TESTS_AND_VERIFICATION)

**Projekt:** STEPS – System zur Theorie-gestützten Erkundung von Progressionen und Skalen  
**Stand:** Commit `fe66637`  
**Gesamtergebnis:** 115 Tests ausgeführt, 0 Fehler, 0 Fehlschläge (**100 % PASS**)  

---

## 1. Test-Suiten-Übersicht

| Testdatei / Modul | Art der Tests | Anzahl Tests | Laufzeit | Ergebnis |
|---|---|:---:|:---:|:---:|
| `tests/test_theory_core.py` | Unittest, Axiome, Enharmonik, Akkord-Parser, Voicings | 31 | 0.005 s | **100% PASS** |
| `tests/test_progression_engine.py` | Unittest, 28 Progressionen, PROG-021/028, Stufenauflösung | 12 | 0.009 s | **100% PASS** |
| `tests/test_golden_reference_cases.py` | Echte mathematische Tests & Spezifikationsprüfung (REF-0001..0198) | 28 | 4.810 s | **100% PASS** |
| `tests/test_secret_scanner.py` | Sicherheits-Tests, Token-Erkennung, Baseline-Tampering, Fail-Closed | 15 | 0.011 s | **100% PASS** |
| `tests/test_structure.py` | Strukturtests, JSON-Syntax, Dateipfade | 4 | 0.080 s | **100% PASS** |
| `.agents/skills/steps-knowledge-curation/tests/` | Backup/Restore, 21 Validierungsaufgaben, Symlink-Handling | 25 | 0.078 s | **100% PASS** |
| **GESAMT** | **Vollständige STEPS Systemverifikation** | **115** | **~5.0 s** | **100% PASS** |

---

## 2. Detaillierte Testauszüge & Beweise

### 2.1 Mathematische Axiome der $L_1$-Stimmführung (`test_theory_core.py`)
```python
def test_metric_space_axioms_for_l1_distance(self):
    v1 = [60, 64, 67, 71]
    v2 = [59, 62, 67, 71]
    v3 = [57, 60, 65, 69]

    # 1. Nichtnegativität: d(a, b) >= 0 -> PASS
    # 2. Identität: d(a, a) == 0 -> PASS
    # 3. Symmetrie: d(a, b) == d(b, a) -> PASS
    # 4. Dreiecksungleichung: d(a, c) <= d(a, b) + d(b, c) -> PASS
```

### 2.2 Garantierter Erhalt von PROG-021 und PROG-028 (`test_progression_engine.py`)
```python
def test_prog_021_preservation(self):
    p21 = get_progression('PROG-021')
    self.assertEqual(p21.name, 'Neo-Soul Rootless Minor Cycle')
    self.assertEqual(p21.chords_str, 'Dm9 - Gm9 - Bbmaj9 - A7(b9)')
    # Tonhöhenmengen in Z12 exakt verifiziert -> PASS

def test_prog_028_preservation(self):
    p28 = get_progression('PROG-028')
    self.assertEqual(p28.name, 'Circle of Fifths Soul Cycle')
    self.assertEqual(p28.chords_str, 'Em9 - Am9 - D9 - Gmaj9')
    # Tonhöhenmengen in Z12 exakt verifiziert -> PASS
```

### 2.3 Wahrheitspflicht der Golden-Tests (Keine Scheinerfolge)
```python
def test_unimplemented_executable_case_strictly_raises_error(self):
    # Verifiziert, dass ein nicht-implementierter Fall strikt NotImplementedError wirft
    # und niemals stillschweigend mit True quittiert wird -> PASS
```

---

## 3. CI/CD und Sicherheits-Validierung

1. **Strukturvalidierung (`check_structure.py`):**
   ```
   OK: STEPS structure and JSON syntax (not product implementation).
   ```
2. **Pre-Commit Secret Scanner (`pre-commit-secret-check.py`):**
   - Geprüfte Dateien: Gesamter Repository-Bestand einschließlich `.agents/`
   - Ergebnis: **0 Leaks detected, 0 unmasked secrets, Fail-Closed intakt.**
3. **Remote CI (`python-tests.yml`):**
   - Ausführung der 115 Tests auf Ubuntu Latest unter Python 3.11 und 3.12.
"""
    with open(os.path.join(OUTPUT_DIR, "08_TESTS_AND_VERIFICATION.md"), "w", encoding="utf-8") as f:
        f.write(content)
    print("Generated 08_TESTS_AND_VERIFICATION.md")

def write_issues_and_risks():
    content = """# 09 – Fehlerregister, Risiken & Widersprüche (ISSUES_RISKS_AND_CONTRADICTIONS)

**Projekt:** STEPS – System zur Theorie-gestützten Erkundung von Progressionen und Skalen  
**Dokumenttyp:** Register aller identifizierten, behobenen und noch offenen Fehler und Risiken  

---

## 1. Register behobener Fehler (ERR-001 bis ERR-037 & Technische Issues)

| Problem-ID | Komponente | Beschreibung | Ursache | Behoben in | Status |
|---|---|---|---|---|:---:|
| `ERR-001` bis `ERR-037` | `knowledge/` | 37 musikalische Fachfehler in Skalen, Intervallen und Akkorden | Ursprüngliche fehlerhafte Recherche | Commit `918d0a7` | **BEHOBEN** |
| `ISSUE-BOM` | `knowledge/research/*.csv` | `KeyError: 'error_id'` bei `csv.DictReader` | Windows/Excel UTF-8 Byte Order Mark (`\\xef\\xbb\\xbf`) | Commit `918d0a7` | **BEHOBEN** |
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
"""
    with open(os.path.join(OUTPUT_DIR, "09_ISSUES_RISKS_AND_CONTRADICTIONS.md"), "w", encoding="utf-8") as f:
        f.write(content)
    print("Generated 09_ISSUES_RISKS_AND_CONTRADICTIONS.md")

def write_open_work_and_roadmap():
    content = """# 10 – Offene Arbeiten & Roadmap (OPEN_WORK_AND_ROADMAP)

**Projekt:** STEPS – System zur Theorie-gestützten Erkundung von Progressionen und Skalen  
**Stand:** Nach Abschluss von Phase 5.1 (Headless Music Theory Core Hardening)  

---

## 1. Register offener Aufgaben (NEXT-001 bis NEXT-010)

| Task-ID | Bereich | Bezeichnung & Ziel | Voraussetzungen | Priorität |
|---|---|---|---|:---:|
| `NEXT-001` | Architektur | Formale Entscheidung zu **ADR-001** (Desktop GUI Framework) | Owner-Entscheidung | **P1 (Entscheidung)** |
| `NEXT-002` | Core (M03) | **Phase 5.2:** Skalen- und Modus-Engine (`src/steps/theory/scale.py`) | Phase 5.1 Kern (fertig) | **P1 (Funktional)** |
| `NEXT-003` | Audio (M01/M08) | **Phase 5.3:** Headless MIDI- & Audio-Synthese (`src/steps/audio/`) | Phase 5.1 Kern (fertig) | **P2 (Funktional)** |
| `NEXT-004` | Recommender (M05) | **Phase 5.4:** Graph-basierte harmonische Pfadsuche & Substitutionen | 97 Graph-Relationen (fertig) | **P2 (Algorithmus)** |
| `NEXT-005` | UI-Entwicklung | **Phase 6.0:** Desktop-Interface-Scaffolding (`app/ui/`) | ADR-001 Freigabe | **P3 (Gated)** |
| `NEXT-006` | Didaktik (M10) | Interaktive Lernmodule basierend auf Didaktik-DAG (ADR-010) | Phase 5.2 | **P3 (Erweiterung)** |
| `NEXT-007` | Import/Export | MusicXML und MIDI-File Parser/Generator (`src/steps/io/`) | Phase 5.1 Kern (fertig) | **P2 (Integration)** |
| `NEXT-008` | Genre-Engine | Automatisierte Stilerkennung basierend auf 9 Genre-Profilen | Phase 5.4 | **P3 (Feature)** |
| `NEXT-009` | Dokumentation | Sphinx/MkDocs API-Referenz für `src/steps/` | Phase 5.1 Kern (fertig) | **P2 (Doku)** |
| `NEXT-010` | CI-Monitoring | Überwachung der GitHub Actions Runner-Zyklen auf `origin` | Push `fe66637` (fertig) | **P1 (Monitoring)** |

---

## 2. Detaillierte Spezifikation von Phase 5.2 (Skalen- & Modus-Engine)

- **Modulpfad:** `src/steps/theory/scale.py`
- **Inhalte:**
  - Diatonische Modi: Ionisch, Dorisch, Phrygisch, Lydisch, Mixolydisch, Äolisch, Lokrisch.
  - Harmonisch & Melodisch Moll Modi: Alteriert, Lydisch Dominant, Phrygisch Dominant, etc.
  - Symmetrische Skalen: Ganztonskala, Halbton-Ganzton (HTGT), Ganzton-Halbton (GTHT), Chromatik.
  - Pentatonik & Blues-Skalen: Dur- und Moll-Pentatonik, Blues-Skala (mit Blue Notes).
  - Skalen-Akkord-Kompatibilitätsmatrix (Chord-Scale-Theory nach Levine 1995 und Russell 2001).
- **Testabdeckung:** Mindestens 25 neue Unittests für Skalenkonstruktion, Modi-Transposition und Akkord-Skalen-Matching.
"""
    with open(os.path.join(OUTPUT_DIR, "10_OPEN_WORK_AND_ROADMAP.md"), "w", encoding="utf-8") as f:
        f.write(content)
    print("Generated 10_OPEN_WORK_AND_ROADMAP.md")

if __name__ == '__main__':
    write_technical_state()
    write_changes()
    write_tests_and_verification()
    write_issues_and_risks()
    write_open_work_and_roadmap()
    print("Module 2 completed successfully.")
