# 02 – Vollständiges Anforderungsregister (REQ-001 bis REQ-030)

**Projekt:** STEPS – System zur Theorie-gestützten Erkundung von Progressionen und Skalen  
**Geltungsbereich:** Sämtliche im Chatverlauf geäußerten Nutzeranforderungen, Architekturanforderungen und Qualitätsgates  
**Rückverfolgbarkeit:** Anforderung $\to$ Entscheidung $\to$ Arbeitsauftrag $\to$ Implementierung $\to$ Test $\to$ Status  

---

## 1. Systematische Anforderungsmatrix

| ID | Anforderungsgegenstand | Ursprung | Ziel & Beschreibung | Nachweis / Test | Status |
|---|---|---|---|---|:---:|
| `REQ-001` | Pure Python Package Scaffolding | Phase 2B (T-04) | Schaffung eines standardkonformen Python-Pakets `src/steps/` ohne Fremdimplementierungen | PR #4 (`190228a`), `pyproject.toml` | **ERFÜLLT** |
| `REQ-002` | Preservation-First Prinzip | AGENTS.md (Regel 2) | Keine stillschweigende Löschung oder Überschreibung historischer Notizen, IDs oder Dateien | Test-Suite `test_reference_integrity.py` | **ERFÜLLT** |
| `REQ-003` | Enharmonische Trennung (ADR-005) | Phase 4.3, 4.18 | Strikte Trennung von diatonischer Notenorthographie (NoteSpelling) und Z12 PitchClass | `tests/test_theory_core.py` | **ERFÜLLT** |
| `REQ-004` | Zweisprachige Nomenklatur | AGENTS.md (Regel 5) | Explizite Unterscheidung von int. B/Bb und deutschem H/B sowie Beugungen (Fis, Es, As, Fisis, Heses) | `NoteSpelling.render()`, `parse_spelling()` | **ERFÜLLT** |
| `REQ-005` | Akustische ISO 16-Stimmung | M01, Phase 5.1 | Standard-Frequenzberechnung basierend auf $A_4 = 440.0\text{ Hz}$ (MIDI Note 69) | `midi_to_frequency()`, `frequency_to_midi()` | **ERFÜLLT** |
| `REQ-006` | Intervall-Arithmetik & Inversionen | M01, M03, Phase 5.1 | Mathematische Invariante: $i + \text{invert}(i) \equiv 0 \pmod{12}$; Trennung diatonisch/chromatisch | `DiatonicInterval.invert()`, `semitones` | **ERFÜLLT** |
| `REQ-007` | Zusammengesetzte Intervalle | Phase 5.1 | Unterstützung von Intervallen über die Oktave hinaus (None, Undezime, Tredezime) | `DiatonicInterval(9, 'M').semitones == 14` | **ERFÜLLT** |
| `REQ-008` | Dreiklangs-Konstruktion | M04, Phase 4.18 | Exakte Terzschichtung für Dur, Moll, Vermindert, Übermäßig, Sus4, Sus2, Add9 | `construct_triad()`, Inversionen 6/3, 6/4 | **ERFÜLLT** |
| `REQ-009` | Vierklangs- und Voicing-Engine | M04, Phase 4.18 | Dom7, Maj7, m7, m7b5, dim7, m(maj7); Drop-2 und Shell Voicings | `make_drop2_voicing()`, `make_shell_voicing()` | **ERFÜLLT** |
| `REQ-010` | Lydian Dominant Klärung | REF-0035, Phase 5.1 | Trennung zwischen theoretischer Formel $\{0, 4, 6, 7, 10\}$ und voicings $\{0, 4, 6, 10\}$ (Quint-Auslassung) | `c7_11.theoretical_intervals`, `c7_11.default_voiced_intervals` | **ERFÜLLT** |
| `REQ-011` | Umfassender Leadsheet-Parser | M04, Phase 5.1 | Parsen von Akkordsymbolen (Triads, Sevenths, Extensions, Slash-Chords, deutsche Akkorde wie H7) | `parse_chord()` in `src/steps/theory/chord.py` | **ERFÜLLT** |
| `REQ-012` | $L_1$-Metrikraum für Stimmführung | M06, Phase 5.1 | Nachweis aller 4 metrischen Axiome (Nichtnegativität, Identität, Symmetrie, Dreiecksungleichung) | `test_metric_space_axioms_for_l1_distance` | **ERFÜLLT** |
| `REQ-013` | Tymoczko Kreisdistanz auf $\mathbb{Z}_{12}$ | M06, Phase 4.18 | Distanzfunktion im geometrischen Akkordraum: $\min(|\Delta|, 12 - |\Delta|)$ | `circular_pc_distance()` | **ERFÜLLT** |
| `REQ-014` | Stimmführungs-Stile | M06, Phase 5.1 | Trennung von strengem Kontrapunkt (Parallelenverbot) und Jazz/Pop (Parallelverschiebungen erlaubt) | `VoiceLeadingStyle.STRICT_COUNTERPOINT` vs `JAZZ_POP` | **ERFÜLLT** |
| `REQ-015` | Stimmkreuzungs- und Überlappungsprüfung | M06, Phase 5.1 | Erkennung von $v_i \ge v_{i+1}$ und Überlappungen von Stimmlagen aufeinanderfolgender Akkorde | `detect_voice_crossing()`, `detect_voice_overlap()` | **ERFÜLLT** |
| `REQ-016` | Deterministischer Voicing-Optimierer | M06, Phase 5.1 | Berechnung der optimalen, minimalen Stimmführungsbewegung ohne Stimmkreuzung | `optimize_smooth_voice_leading()` | **ERFÜLLT** |
| `REQ-017` | Kanonische 28 Progressionen | M05, Phase 5.1 | Vollständige programmatische Registrierung von `PROG-001` bis `PROG-028` | `list_progressions()`, `CANONICAL_PROGRESSIONS` | **ERFÜLLT** |
| `REQ-018` | Strikter Erhalt von PROG-021 | Phase 4.17, 5.1 | Garantierte Bewahrung von PROG-021 (*Neo-Soul Rootless Minor Cycle*: `Dm9 - Gm9 - Bbmaj9 - A7(b9)`) | `test_prog_021_preservation` | **ERFÜLLT** |
| `REQ-019` | Strikter Erhalt von PROG-028 | Phase 4.18, 5.1 | Garantierte Bewahrung von PROG-028 (*Circle of Fifths Soul Cycle*: `Em9 - Am9 - D9 - Gmaj9`) | `test_prog_028_preservation` | **ERFÜLLT** |
| `REQ-020` | Stufenauflöser (Roman Numerals) | M05, Phase 5.1 | Auflösung von Stufen in Dur, Moll, Zwischendominanten ($V7/V$) und modalen Entlehnungen ($\flat\text{II}7, iv$) | `resolve_roman_degree()` | **ERFÜLLT** |
| `REQ-021` | Progressions-Voicing-Sequenzer | M05, M06, Phase 5.1 | Generierung kontinuierlicher 4-stimmiger Voicing-Ketten mit Stimmführungs-Metrikanalyse | `generate_progression_voicings()`, `analyze_progression_voice_leading()` | **ERFÜLLT** |
| `REQ-022` | Headless Core Priorität (ADR-004) | AGENTS.md, ADR-004 | Reine Python-Logik in `src/steps/theory/` ohne UI-Abhängigkeiten vor formaler GUI-Entscheidung | Keine UI-Imports in `src/steps/` | **ERFÜLLT** |
| `REQ-023` | Glide-Entkopplung | AGENTS.md (Regel 9) | Keine Vermischung von Glide-Desktop-Code mit dem STEPS-Theorie-Kern | Separate Repositories, Quarantäne gewahrt | **ERFÜLLT** |
| `REQ-024` | Fail-Closed Secret Scanning | Phase 4.16 | Automatisierte Erkennung von API-Schlüsseln; strikte SHA-256 Bindung historischer Baselines | `scripts/pre-commit-secret-check.py`, CI Workflow | **ERFÜLLT** |
| `REQ-025` | Remote Python CI Test Suite | Phase 5.1 | Automatisierte Ausführung aller Unit- und Curation-Tests auf GitHub Actions für Python 3.11/3.12 | `.github/workflows/python-tests.yml` | **ERFÜLLT** |
| `REQ-026` | Curation Antigravity Skill | Phase 3 | Pflege, Validierung und Backup des Wissensbestands über dedizierten Agent-Skill | `.agents/skills/steps-knowledge-curation/` | **ERFÜLLT** |
| `REQ-027` | 198 Golden Reference Cases | Phase 4.15 | Absicherung aller 198 kanonischen Referenzfälle mit semantischen Hashes und Null-Toleranz-Schutz | `knowledge/research/canonical/GOLDEN_REFERENCE_CASES_CANON.json` | **ERFÜLLT** |
| `REQ-028` | 97 Semantische Relationen | Phase 4.18 | Konsistente Graph-Topologie aus 38 Cross-Domain Links, 36 Progression Links, 23 Extension Links | `knowledge/research/canonical/KNOWLEDGE_GRAPH_RELATIONS_CANON.json` | **ERFÜLLT** |
| `REQ-029` | UTF-8 BOM Beseitigung | Phase 4.18 | Vollständige Entfernung störender Byte Order Marks (`\xef\xbb\xbf`) aus allen CSV-Dateien | Alle CSVs als UTF-8 ohne BOM validiert | **ERFÜLLT** |
| `REQ-030` | Keine Scheinerfolge bei Tests | AGENTS.md (Regel 3) | Unimplementierte Tests werfen strikt `NotImplementedError` statt unechter Pass-Werte | `test_unimplemented_executable_case_strictly_raises_error` | **ERFÜLLT** |

---

## 2. Abnahmekriterien und Erfüllungsgrad

- **Gesamtanzahl identifizierter Kernanforderungen:** 30
- **Davon vollständig erfüllt:** 30 (100 %)
- **Offene oder zurückgestellte Anforderungen:** 0 blockierende funktionale Kernanforderungen.
- **Zukünftige Anforderungen (Roadmap Phase 5.2+):** Skalen-Engine (M03), Audio/MIDI-Synthese (M08), Graph-basierte Pfadsuche (M05).
