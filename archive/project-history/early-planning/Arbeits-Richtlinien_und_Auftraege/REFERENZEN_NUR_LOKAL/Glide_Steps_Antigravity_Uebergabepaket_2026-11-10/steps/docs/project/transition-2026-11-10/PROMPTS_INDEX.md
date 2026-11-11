# STEPS – Agentenprompts als versionierte Arbeitsaufträge

**Status:** geprüfte Entwürfe; keine automatische Ausführung und kein Implementierungsbeleg. Jeder Prompt soll in **einer separaten Sitzung / einem separaten Themenbranch** ausgeführt werden. Die Reihenfolge ist eine Empfehlung; P01–P04 sind vor risikohaften Produktänderungen erforderlich.

| Kennung | Prompt | Ergebnis | Vorgänger-Gate |
|---|---|---|---|
| P01 | `PROMPTS/01_READ_ONLY_CONTEXT_AUDIT.md` | exakter lokaler Stand, Quellregister, Diskrepanzen | keine Schreiboperation |
| P02 | `PROMPTS/02_PRODUCT_SCOPE.md` | PRD, zwei-Fenster-Wording und Entscheidungsvorlagen | P01 |
| P03 | `PROMPTS/03_SHELL_MIGRATION.md` | isolierte Shell auf neutralem Testhost, zuerst Plan | Glide QA G1, P01/P02 |
| P04 | `PROMPTS/04_SHARED_CORE.md` | Component Contract, SemVer und Consumer-Spike | P03 bzw. isolierte Komponente |
| P05 | `PROMPTS/05_DOMAIN_MODEL.md` | deterministisches Musik-/Projektmodell | P02 |
| P06 | `PROMPTS/06_MIDI_TIMELINE.md` | Track/Event/Timing, parsergeprüfter Export | P05 |
| P07 | `PROMPTS/07_KNOWLEDGE_INGESTION.md` | Rechte- und Provenienz-Pipeline, 3–5 Pilotquellen | P01/P02 |
| P08 | `PROMPTS/08_SKILL_EVALUATION.md` | Skills, Retrieval, Grounding/Eval | P07 |
| P09 | `PROMPTS/09_QA_SECURITY.md` | nicht überspringbare CI, Negativtests | P05/P06/P03 |
| P10 | `PROMPTS/10_RELEASE_GOVERNANCE.md` | Release-Gate, Lizenz/SBOM, Branchschutz | P09 |
| P11 | `PROMPTS/11_UI_UX.md` | Musik-Workflow und Accessibility | P02, P03 |
| P12 | `PROMPTS/12_COMPETITOR_RESEARCH.md` | aktuelle Task-Vergleiche und validierte Positionierung | P02 |

**Gemeinsamer Vertrag für alle Prompts:**
- Vorher `AGENTS.md`, `SKILL.md`, bestehende Steps-Overview, aktuelle V3-Prüfung und das neu importierte `README.md` dieser Transition lesen. Arbeitsbaum, SHA, Branche, lokale Änderungsdaten, Rechte/Third-Party-Bestand dokumentieren.
- Vor der ersten tatsächlichen Änderung als **Arbeitsplan** Komponenten, Dateien, Tests, Risiken und Abhängigkeiten nennen. Keine stillen Annahmen über abgeschlossene Vorarbeiten.
- Nur kleine überprüfbare Changesets, keine Massengeneratoren, keine fremden Web-Caches/PDFs in neue öffentliche Pfade, keine History-Rewrites. V2-Installer niemals ausführen.
- Vor Start prüfen, ob der Codeowner einen Merge-/Release-/Asset-Transfer freigegeben hat. Für neue Abzweigungen nur eigene Branches; nie `main` direkt verändern.
- Jede Aufgabe mit Pfad, Änderungsumfang, `git diff --check`, Testkommando und Resultat, vollständiger SHA und offenen Punkten dokumentieren. Status `PASS/FAIL/SKIPPED/NOT_TESTED` ausdrücklich trennen.
- Kein neuer zweiter kanonischer Plan. Aktualisierungen in den vorhandenen Projekt-/Architektur-/Entscheidungsdokumenten verlinken, historische Einträge nicht löschen.
