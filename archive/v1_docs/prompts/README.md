# STEPS – wiederverwendbare KI- und Codex-Aufträge

**Stand:** 10.11.2026 (Europe/Berlin). **Status:** Entwurf und Prüfauftrag, keine Umsetzung/Freigabe. **Referenzstände:** Steps `main` `75329fef46878a5ac816cef3690e612a9e8fe52c`; Glide `main` `61a2f3ac2f0e1880e7fd8c0f3cfd9da0d0c9f16d`; lokal bereitgestellter Glide-Code `3.53.0`, SHA-256 `d7e19151eb0862a8ff58c4cc5e7d06a0452cde1daa73830ff97f54247bc75271`.

**Evidenz:** `UPLOAD` = bereitgestellte Datei, `GITHUB` = gelesener Remote-Stand, `BERICHTET` = in Unterlagen behauptet, `VORSCHLAG` = neue Empfehlung, `OFFEN` = unbestätigt. Kein dokumentierter Test bedeutet nicht bestanden.

**Ein Prompt = ein abgrenzbarer Arbeitsschnitt.** Alle 24 Prompts sind sofort kopierbar und enthalten gemeinsame Quellen-/Evidenz-/Git-Schutzregeln. Prompt 01 koordiniert, 02 friert Glide ein, 03–07 portieren die Shell, 08–12 gestalten die Musik-App, 13–15 bauen die Bibliothek und den Skill aus, 16–20 prüfen/liefern, 21–24 sichern Kontinuität und Aktualisierungen.

**Lesereihenfolge je Agent:** aktueller Steps-`AGENTS.md` → this archive `docs/project/SOURCE_AND_REPO_AUDIT.md` → eigener Prompt → darin referenzierte Originale → aktuelle GitHub HEADs → erst dann Änderungen. Die Git-Rechte müssen beim Agenten überprüft werden; `push:true` heute ist keine Dauerzusage. Für Codex ist `04_GLIDE_TO_STEPS_SHELL.md` der konkrete Portierungsauftrag, **erst nach** `02_GLIDE_FINISH_FREEZE.md` + `03_GLIDE_AUDIT_REUSE.md`.

| Datei | Bereich |
|---|---|
| [01_ORCHESTRATOR.md](01_ORCHESTRATOR.md) | Gesamtkoordination, Projektkontinuität und Priorisierung |
| [02_GLIDE_FINISH_FREEZE.md](02_GLIDE_FINISH_FREEZE.md) | Glide 3.53.0 abschließen und Ausgangsstand einfrieren |
| [03_GLIDE_AUDIT_REUSE.md](03_GLIDE_AUDIT_REUSE.md) | Glide Modul-, Feature-, Abhängigkeits- und Kopplungsaudit |
| [04_GLIDE_TO_STEPS_SHELL.md](04_GLIDE_TO_STEPS_SHELL.md) | Glide auf STEPS-Zweibereichs-Shell rückbauen |
| [05_SIDEBAR_NOOP.md](05_SIDEBAR_NOOP.md) | Seitenliste ohne Fachfunktion bewahren |
| [06_DESIGN_SETTINGS_BRANDING.md](06_DESIGN_SETTINGS_BRANDING.md) | Theme, Fonts, Logo, Header, Editorflächen und Einstellungen |
| [07_ARCHITECTURE_PORTS.md](07_ARCHITECTURE_PORTS.md) | Architektur, Events, Prozesse und Datenhaltung entkoppeln |
| [08_MUSIC_PITCH_CHORD.md](08_MUSIC_PITCH_CHORD.md) | Musiktheorie-Kern: Pitch, Intervalle, Skalen und Akkorde |
| [09_PROGRESSIONS_EXPLORER.md](09_PROGRESSIONS_EXPLORER.md) | Chord Progression Editor, Harmony Explorer und Erklärung |
| [10_DRUM_GRID.md](10_DRUM_GRID.md) | Drum Progressions, Groove und Beatmaking |
| [11_MIDI_AUDIO.md](11_MIDI_AUDIO.md) | MIDI, Audiowiedergabe und Export/Import |
| [12_STORAGE_BACKUP.md](12_STORAGE_BACKUP.md) | Steps-Projektformat, Speichern, Sicherungen und Versionsmigration |
| [13_KNOWLEDGE_ARCHITECTURE.md](13_KNOWLEDGE_ARCHITECTURE.md) | Kanonische Wissensdatenbank und Schemas |
| [14_SOURCE_INGESTION.md](14_SOURCE_INGESTION.md) | Neue Quellen, Bücher und Crawls systematisch ingestieren |
| [15_KNOWLEDGE_SKILL.md](15_KNOWLEDGE_SKILL.md) | Knowledge-Bibliothek als portablen AI-Skill anbinden |
| [16_QA_TEST_MATRIX.md](16_QA_TEST_MATRIX.md) | Quality Assurance, Regression und Plattformverifikation |
| [17_RIGHTS_SECURITY.md](17_RIGHTS_SECURITY.md) | Urheberrechte, Open Source, Abhängigkeiten und Sicherheitsreview |
| [18_COMPETITOR_RESEARCH.md](18_COMPETITOR_RESEARCH.md) | Wettbewerbsanalyse und funktionale Differenzierung |
| [19_DOCUMENTATION_GOVERNANCE.md](19_DOCUMENTATION_GOVERNANCE.md) | Dokumentpflege, Widersprüche, Dopplungen, Review und README |
| [20_RELEASE_PACKAGING.md](20_RELEASE_PACKAGING.md) | Packaging, CI, plattformneutrale Distribution und Releasing |
| [21_DAILY_HANDOVER.md](21_DAILY_HANDOVER.md) | Kontextübergabe zwischen Tokens, Accounts und Agenten |
| [22_EXTERNAL_AUDIT.md](22_EXTERNAL_AUDIT.md) | Unabhängiger Architektur-/Rechte-/Konzept-Gegencheck |
| [23_UI_SEARCH_AND_EDITORS.md](23_UI_SEARCH_AND_EDITORS.md) | Suchfeld, bearbeitbare Flächen und zukünftige Workspaces |
| [24_SOURCE_INDEX_SNAPSHOT.md](24_SOURCE_INDEX_SNAPSHOT.md) | Vollinventarisierung, Hash- und Deduplikatvergleich |
