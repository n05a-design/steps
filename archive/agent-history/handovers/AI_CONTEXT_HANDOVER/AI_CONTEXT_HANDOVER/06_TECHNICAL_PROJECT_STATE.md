# 06 – Technischer Projektstand & Architektur (TECHNICAL_PROJECT_STATE)

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
  - `midi_to_frequency()` / `frequency_to_midi()`: Exakte ISO 16:1975 Akustik ($A_4 = 440	ext{ Hz}$).
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
