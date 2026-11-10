# STEPS – Prompt-Index und qualitätsgesicherte Ausführungsfolge

**Bearbeitungsstand:** Kritisches Audit 10.11.2026. **Bestand:** 24 zuvor erstellte Arbeitsaufträge, fachlich um aktuelle Prüfankern/Negativfälle ergänzt; zusätzlich **5 spezialisierte** Prüf- und Implementierungsaufträge 25–29. Die ursprünglichen 24 Dateien stehen in `archive/v1_prompts/` unverändert für Diff/Provenienz zur Verfügung.

**Vor jeder Ausführung:** `docs/project/PROJECT_OVERVIEW.md`, `docs/audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md`, `docs/operations/MULTI_AGENT_EXECUTION_AND_HANDOVER.md`, `manifests/REQUIREMENTS_TRACE_28.csv` und das konkrete Zielmodul lesen. Beide Repository-Commits im Prompt sind historische Snapshots – aktuellen `main`, Working Tree, Dateihashes und offene PRs erneut verifizieren. Stufe `Owner-Beschluss`, `Source-/Rechte-Review`, `Code/Tests`, `Native-Abnahme` nicht ersetzen. In der GitHub-Integration kann Schreiben trotz angezeigter `push:true`-Berechtigung scheitern; dann lokale Outputs und PR-Vorschlag ausliefern statt Erfolg behaupten.

| Phase | Datei | Hauptzweck | Abhängigkeit |
|---|---|---|---|
| Koordination | [01_ORCHESTRATOR.md](01_ORCHESTRATOR.md) | unabhängige Workstreams, Risiken und Handover | vor Parallelstarts |
| Glide-Freeze | [02_GLIDE_FINISH_FREEZE.md](02_GLIDE_FINISH_FREEZE.md) | Source-/QA-/Asset-Snapshot 3.53.0 | eigenständiges Glide-Audit |
| Glide-Reuse | [03_GLIDE_AUDIT_REUSE.md](03_GLIDE_AUDIT_REUSE.md) | 94 Module/25 Pakete einzeln prüfen | Glide-Freeze |
| Shell | [04_GLIDE_TO_STEPS_SHELL.md](04_GLIDE_TO_STEPS_SHELL.md) | isolierte Shell-Implementierung | ADR/Spikes |
| Navigation | [05_SIDEBAR_NOOP.md](05_SIDEBAR_NOOP.md) | frühere Todo-Actions neutralisieren | Shell-Gates |
| Design | [06_DESIGN_SETTINGS_BRANDING.md](06_DESIGN_SETTINGS_BRANDING.md) | Theme/Font/Settings/Logo | Lizenz/Design |
| Architektur | [07_ARCHITECTURE_PORTS.md](07_ARCHITECTURE_PORTS.md) | UI/Domain/Knowledge-Ports | Domain-/Scope-ADR |
| Theorie | [08_MUSIC_PITCH_CHORD.md](08_MUSIC_PITCH_CHORD.md) | Pitch/Chord-/Notation-Modelle | Research/Golden Tests |
| Progression | [09_PROGRESSIONS_EXPLORER.md](09_PROGRESSIONS_EXPLORER.md) | Harmoniegraph und Erklärung | Theory/KB |
| Drums | [10_DRUM_GRID.md](10_DRUM_GRID.md) | Groove-/Stepgrid mit gemeinsamer Timeline | Owner-Drum-Scope-ADR |
| MIDI | [11_MIDI_AUDIO.md](11_MIDI_AUDIO.md) | SMF, Playback und Backend-Failure | Timeline/Storage |
| Daten | [12_STORAGE_BACKUP.md](12_STORAGE_BACKUP.md) | eigene Steps-Project-Daten, Recovery | Schema/Identity |
| KB-Design | [13_KNOWLEDGE_ARCHITECTURE.md](13_KNOWLEDGE_ARCHITECTURE.md) | Claims/Concepts/Relations | Source-Rechte |
| Crawl | [14_SOURCE_INGESTION.md](14_SOURCE_INGESTION.md) | erlaubte Quellen ingesten | Registry/Licenses |
| Skill | [15_KNOWLEDGE_SKILL.md](15_KNOWLEDGE_SKILL.md) | Provider-neutraler Knowledge-Zugriff | echte geprüfte KB-Records |
| Tests | [16_QA_TEST_MATRIX.md](16_QA_TEST_MATRIX.md) | Q0–Q7/Nativ/Evals | jeweils nach Feature |
| Sicherheit | [17_RIGHTS_SECURITY.md](17_RIGHTS_SECURITY.md) | Rechte/Threat Model/History | sofortige P0 |
| Konkurrenz | [18_COMPETITOR_RESEARCH.md](18_COMPETITOR_RESEARCH.md) | aktuelle Feature-/Nutzervergleich | Product-MVP-ADR |
| Doku | [19_DOCUMENTATION_GOVERNANCE.md](19_DOCUMENTATION_GOVERNANCE.md) | Kanonische Quellen/IDs/ADRs | fortlaufend |
| Release | [20_RELEASE_PACKAGING.md](20_RELEASE_PACKAGING.md) | OS-Pakete, Rechte, SBOM | Q0–Q7 |
| Handover | [21_DAILY_HANDOVER.md](21_DAILY_HANDOVER.md) | Session-/Agentenwechsel | jede Session |
| Independent Review | [22_EXTERNAL_AUDIT.md](22_EXTERNAL_AUDIT.md) | Gegenhypothesen und Qualität | jeder Meilenstein |
| UI-Search | [23_UI_SEARCH_AND_EDITORS.md](23_UI_SEARCH_AND_EDITORS.md) | sichere Suche und Editoren | Shell/KB-Pfade |
| Index | [24_SOURCE_INDEX_SNAPSHOT.md](24_SOURCE_INDEX_SNAPSHOT.md) | Git-/Source-/Duplikat-Provenienz | vor Ingestion |
| **Neuer P0-Auftrag** | [25_KNOWLEDGE_PILOT_REAL_INGEST.md](25_KNOWLEDGE_PILOT_REAL_INGEST.md) | *tatsächlich* KB befüllen und Retrieval testen | Rechtsreview + Originalquellen |
| **Neuer P0-Auftrag** | [26_GLIDE_SHELL_COMPARE_SPIKES.md](26_GLIDE_SHELL_COMPARE_SPIKES.md) | Extrakt vs Scratch anhand 30 Tests | Glide-Freeze/Owner-Scope |
| **Neuer P0-Auftrag** | [27_PUBLIC_REPO_RIGHTS_HISTORY_AUDIT.md](27_PUBLIC_REPO_RIGHTS_HISTORY_AUDIT.md) | veröffentlichte PDFs/Assets/History bewerten | sofort, unabhängig von Produkt |
| **Neuer Reviewauftrag** | [28_INDEPENDENT_REQUIREMENTS_TRACE_AUDIT.md](28_INDEPENDENT_REQUIREMENTS_TRACE_AUDIT.md) | 28 REQs + 33 Dimensionen unabhängig falsifizieren | zentrale Quellen |
| **Neuer Produktauftrag** | [29_PRODUCT_LEARNING_VALIDATION.md](29_PRODUCT_LEARNING_VALIDATION.md) | Nutzertests, Konkurrenz, Lernwirksamkeit | Prototyp + Owner-Werte |

**Bewertung:** Prompts sind mögliche Arbeitsaufträge, keine erledigten Arbeitspakete. Kein Agent darf ohne Repo-/Source-/Rechteprüfung Produktänderungen implementieren oder historische Handover-IDs als freigegebene Roadmap interpretieren.
