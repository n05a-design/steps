# STEPS · Kontextpaket für das Fable-5.2-Audit

Stand der Vorbereitung: 2026-11-12. Alle Pfade gelten relativ zum Repository-Root auf der unten genannten Revision.
Abschnitt 7 enthält ungeprüfte Behauptungen und bekannte Probleme. Sie sind Prüfgegenstand, kein Ergebnis.

## 1. Projektziel

STEPS soll ein modulares Musiktheorie- und Kompositionssystem werden. Den Anfang bildet ein reiner, testbarer Python-Kern unter `src/steps/`. Er umfasst Tonhöhe, Intervalle, Akkorde, Stufen und Stimmführung. Desktop-App, Audio, MIDI-Ein- und -Ausgabe sowie Persistenz sind nicht implementiert. `app/` enthält bisher nur einen Adapter für drei fachlich freigegebene Lernbeispiele. Arbeitsvertrag: `AGENTS.md`.

## 2. Verifizierte Git-Baseline

| Wert | Stand |
|---|---|
| Repository | `n05a-design/steps` (GitHub) |
| Prüfrevision | `main` = `22f3f5f348d060abfd4e2ffc917d0c95a639441e` (Merge von PR #11, 2026-11-12) |
| Tree-IDs | `src/steps` `bea2a328…`, `tests` `d9cdeb50…`, `knowledge` `55267704…`, `.agents/skills` `1eb8fb7c…` |
| PR #11 | Gemergt. Head `15100b8`, enthält `b0abd41` plus zwei Korrekturcommits zu Pilotstatus, Archivpfaden und Quellenbelegen |
| Version | `VERSION` = `0.0.0-dev`, `src.steps.__version__` = `0.0.0.dev0`. „Phase 5.1“ und „V6.6/V6.7“ sind Projekt- bzw. Bibliotheksstände, keine App-Version |
| Weitere Branches | Vorbereitungs-Branch `claude/fable-5-2-audit-prep` enthält nur dieses Paket. Ältere lokale Feature-Branches sind in `main` aufgegangen oder historisch und nicht Prüfgegenstand |

## 3. Ausgeführte Prüfungen der Vorbereitung

Lokal unter Windows 11 mit Python 3.15.1 auf `22f3f5f`. Die CI prüft mit 3.11 und 3.12 (`.github/workflows/python-tests.yml`). Für 3.11/3.12 liegt lokal kein Lauf vor: `NOT_RUN`.

| Befehl | Ergebnis |
|---|---|
| `python -B -m unittest discover -s tests -p "test_*.py"` | 120 Tests, OK |
| `python -B -m unittest discover -s .agents/skills/steps-knowledge-curation/tests` | 25 Tests, OK |
| `python -B scripts/render_api_reference.py --check` | Exit 0 |
| `python -B scripts/run_knowledge_benchmark.py --scope pilot` | PASS 8 · FAIL 0 · PENDING 0 |
| `python -B scripts/run_knowledge_benchmark.py --scope publication` | PASS 3 · FAIL 0 · PENDING 0 |
| `python -B scripts/run_knowledge_benchmark.py --scope all` | PASS 37 · FAIL 1 · PENDING 32, Exit 1. FAIL: `KB-M11-ALTER` (CLAIM-011) |
| `python -B scripts/run_knowledge_benchmark.py --check-review-sheet knowledge/benchmark/PILOT_ABNAHME.md` | Exit 0 |
| `python -B scripts/render_reviewed_progressions.py --check` | Exit 0 |
| `python -B scripts/audit_knowledge_coverage.py --check` | Ohne PyYAML Exit 1 (fehlende Abhängigkeit). Mit `PyYAML==6.0.3` aus `knowledge/benchmark/requirements.txt` Exit 0 |
| `python -B scripts/verify_reference_integrity.py` | Exit 0 |

Nach den Läufen war der Working Tree sauber. Diese Ergebnisse belegen nur, dass die Prüfungen bestehen. Musikalische Korrektheit belegen sie nicht.

## 4. Aktive Modul-Landkarte

| Modul | Öffentliche Schnittstelle (Auszug) | Zeilen |
|---|---|---|
| `src/steps/theory/pitch.py` | `PitchClass`, `NoteSpelling` (`pitch_class`, `midi_number`, `frequency`, `transpose_diatonic`, `transpose_chromatic`, `render`), `parse_spelling` (INT/DE/AUTO), `midi_to_frequency`, `frequency_to_midi` | 425 |
| `src/steps/theory/interval.py` | `ChromaticInterval`, `DiatonicInterval` (`semitones`, `invert`), `transpose_spelling`, `interval_between_spellings`, `semitones_between`, `directed_semitones`, `invert_semitones_modulo12` | 234 |
| `src/steps/theory/triad.py` | `TriadQuality`, `construct_triad`, `invert_triad_voicing` | 75 |
| `src/steps/theory/seventh.py` | `SeventhQuality`, `construct_seventh`, `invert_seventh_voicing`, `make_drop2_voicing`, `make_shell_voicing` | 124 |
| `src/steps/theory/chord.py` | `CHORD_TEMPLATES`, `parse_chord`, `ChordDefinition` (`theoretical_intervals`, `symbol`, `to_voicing` CLOSE/DROP2/SHELL/ROOTLESS), `Voicing` | 504 |
| `src/steps/theory/exceptions.py` | Fehlerhierarchie unter `MusicTheoryError` | 52 |
| `src/steps/progression/engine.py` | `resolve_roman_degree`, 28 Bestandsprogressionen (`get_progression`, `list_progressions`, `CanonicalProgression.transpose`), `generate_progression_voicings`, `analyze_progression_voice_leading`, `get_reviewed_progression` | 589 |
| `src/steps/progression/voice_leading.py` | `optimize_smooth_voice_leading` (L1-Suche), `detect_parallel_fifths_octaves`, `detect_voice_crossing`, `detect_voice_overlap`, Distanzmetriken | 185 |
| `src/steps/progression/reviewed.py` | Publikationssperre: Claims mit Fingerabdruck, Produktquellen, menschliche Freigaben. `load_reviewed_catalog`, CLI `--review-manifest` | 277 |
| `src/steps/progression/reviewed_progressions.json`, `reviewed_progression_approvals.json` | Pilotdaten (PROG-001, -003, -009) und 8 Freigaben | – |
| `app/knowledge.py` | Re-Export `get_reviewed_progression`, `list_reviewed_progressions` | 5 |

Generierte API-Referenz: `docs/theory/API.md`. Verhaltensgrenzen laut Projekt: `docs/IMPLEMENTATION.md`. Fachmodell und Invarianten: `docs/engineering/MUSIC_DOMAIN_AND_MIDI.md`.

`src/steps/models/` und `src/steps/ports/` enthalten nur `__init__.py`. Nicht implementiert (Stand `docs/IMPLEMENTATION.md`): Skalen- und Modusmodul, Tonarterkennung, Auswahl unter mehreren Analysen, `C11`, `V7(alt)`, Rhythmus/Drums, MIDI-I/O, Desktop.

## 5. Skill-Landkarte

| Skill | Status | Dateien |
|---|---|---|
| `steps-knowledge-curation` | aktiv, mit Skripten und Tests in CI | `.agents/skills/steps-knowledge-curation/` (`SKILL.md`, `README.md`, `references/*.md`, `scripts/*.py`, `templates/*.md`, `tests/*.py`) |
| `steps-project` (Root-Router) | aktiv, nur Text | `SKILL.md` |
| `music-harmony-coach` | historischer Entwurf, laut `skills/music-harmony-coach/README.md` keine Faktengrundlage | `skills/music-harmony-coach/2026-11-10 – music-harmony-coach/` (Pfad mit Datum und Gedankenstrich U+2013) |
| Skill-Design | nur Konzept | `skills/SKILL_DESIGN.md`, `skills/README.md` |

Seiteneffekte von `steps-knowledge-curation`: `scripts/backup_knowledge.py` kopiert und stellt wieder her (`shutil.copy2`, `unlink`). Das Master-Register liegt außerhalb des Repos unter `%LOCALAPPDATA%\StepsKnowledge\OFFENE_ARBEITSAUFFORDERUNGEN.md`.

## 6. Wissensbasis, Tests und Register

| Bestand | Pfad | Umfang |
|---|---|---|
| Produktquellen (Publikationssperre) | `knowledge/sources/registry.yaml` (JSON-Inhalt) | 7 Quellen, alle `rights_status: approved` |
| Kuratierte Quellen | `knowledge/sources/curated_sources_registry.yaml` | 37 Einträge |
| Claim-Register | `knowledge/sources/MUSIC_SOURCE_CLAIM_REGISTER.csv` | 66 Claims: 35 `VERIFIED_TRUE`, 21 `PLACEHOLDER`, 8 `REVIEW_REQUIRED`, 2 `SOURCE_REVIEW_REQUIRED` |
| Relationen | `knowledge/relations/MUSIC_CONCEPT_RELATIONS.csv` | 97 Zeilen |
| Kataloge | `knowledge/concepts/progressions/CHORD_PROGRESSION_REFERENCE_LIBRARY.md`, `knowledge/concepts/chords/PIANO_PRACTICE_REFERENCE_LIBRARY.md`, `knowledge/concepts/styles/DRUM_GROOVE_REFERENCE_LIBRARY.md`, `knowledge/concepts/styles/GENRE_RESEARCH_LATIN.md` | 28 PROG, 19 P, 31 PAT |
| Benchmark | `knowledge/benchmark/cases.json`, `COVERAGE.csv`, `THEMENSTICHPROBEN.md`, `PILOT_ABNAHME.md` | 70 Fälle |
| Golden Cases | Master `knowledge/research/golden_cases/golden_reference_cases.json`, Spiegel `tests/golden_cases/golden_reference_cases.json` (hashgleich) | 198: 63 UNIT, 3 PROPERTY, 1 INTEGRATION, 131 SPECIFICATION_EXAMPLE |
| Fehlerregister | `knowledge/research/03_FACHLICHE_FEHLER.md`, `research/gaps/OPEN_GAPS.md` | – |
| Entscheidungen | `decisions/DECISION_REGISTER.md` | ADR-001…012, alle `proposed` |

Tests: `tests/test_theory_core.py` (34), `tests/test_progression_engine.py` (12), `tests/test_reviewed_progressions.py` (7, darunter 336 Transpositionsfälle), `tests/test_pilot_publication.py` (13), `tests/test_golden_reference_cases.py` (10), `tests/test_knowledge_benchmark.py` (6), `tests/test_reference_integrity.py` (22), `tests/test_secret_scanner.py` (15), `tests/test_structure.py` (1). Die Zahlen zählen Testmethoden. Laufzeitfälle innerhalb einer Methode sind nicht mitgezählt.

## 7. Dokumentierte Selbstauskünfte und bekannte Probleme (ungeprüft)

Diese Punkte stammen aus Repository-Dokumenten. Fable übernimmt sie nicht als Befund, sondern prüft sie.

1. `tests/README.md`: Der Golden-Check testet einen Referenz-Evaluator in `tests/test_golden_reference_cases.py`, nicht die Laufzeitfunktionen.
2. `knowledge/benchmark/COVERAGE.csv`: Golden Cases 198 formal geprüft, 0 fachlich untersucht. Forschungsclaims 66 formal, 3 fachlich untersucht.
3. `research/gaps/OPEN_GAPS.md`: vereinfachte Dominanten in PROG-020/-027, `alt`-Suffix offen, vollständige Kontrapunkt- und Spielbarkeitsprüfung offen, PAT-031 ohne Taktgrenzen.
4. Benchmark `KB-M11-ALTER`: Der Fall erwartet für CLAIM-011, dass der behauptete MusicXML-`alter`-Wertebereich falsch ist. Der Lauf meldet FAIL.
5. `knowledge/benchmark/THEMENSTICHPROBEN.md`: 11 Stichproben, davon 2 beanstandet.
6. `scripts/verify_reference_integrity.py` gibt „100% CANONICAL REFERENCE & SCHEMA INTEGRITY VERIFIED“ aus. Geprüft wird Identität gegen eine Baseline, nicht musikalische Wahrheit.
7. `knowledge/research/independent_golden_test_engine.py` liest Daten aus `%LOCALAPPDATA%\StepsAudit\…`. Er ist im Repository nicht reproduzierbar.
8. Frühere Audits mit Gesamtaussagen: `docs/audit/00_GESAMTBEWERTUNG_UND_METHODIK.md` bis `05_VALIDIERUNGSBERICHT.md`, `archive/INDEX.md` (Master-Audit V2, OpenAI-Prüfpaket).

## 8. Nicht weitergeben und nicht lesen

- `scripts/historical_secret_baseline.json`, `tests/fixtures/synthetic_secrets.json` und Inhalte von Secret-Scan-Befunden. Werte nie zitieren.
- `research/` (rund 643 MB, darunter gespeicherte Webseiten mit Fremd-CSS/JS), `archive/`, `source_archive/`: nur gezielt für D7, keine Volltexte übernehmen.
- `src/glide-v3.53/` (Glide-Referenzcode, externe Lizenz) und `src/steps-0.00/` (nur README-Gerüst).
