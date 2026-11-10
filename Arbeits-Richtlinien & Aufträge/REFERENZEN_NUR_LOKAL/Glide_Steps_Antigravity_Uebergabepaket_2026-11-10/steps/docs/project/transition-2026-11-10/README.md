# STEPS – Projektinterne Übergabe und Arbeitsgrundlage

**Stand:** 10.11.2026 · **Status:** additive Projektgrundlage für eine eigenständige Open-Source-Musik-App; **keine App-Freigabe**. Dieses Dokument hält die im Gespräch beschriebenen Ziele, Werkzeugübergaben, geplante Glide-Abzweigung und Arbeitsregeln dauerhaft fest.

## Projektidentität

**Steps**: unabhängige, offen entwickelte Anwendung für Akkord- und Drum-Progressionen, experimentelles Erkunden von Harmonie, MIDI-Export und Musiktheorie-Lernen. Interessengruppen: Lernende, Songwriter/Hobbyproduzenten und Lehrende. Kein umbenanntes Glide und keine automatische vollständige DAW; Musik-/Klang-/Exportumfang wird durch eine zu bestätigende PRD begrenzt.

**Glide**: eigenständiger Desktop-Planer für Aufgaben, Projekte, Tagesplanung, Pinnwände und Pixel-Zeichnungen, Python/Tkinter. Die Oberfläche und systemischen Schutzmechanismen dienen als **potenzielle technische Vorlage** für Steps. Produktdaten bleiben strikt getrennt. Das gemeinsame System soll langfristig versioniert und pro Komponente in unterschiedliche Projekte übernommen werden können.

**Gegenwärtige Arbeitsteilung der KI-Umgebungen:** VS-Code-Copilot bearbeitet den letzten Glide-Stand; ein Wechsel auf Google Antigravity soll die **lokale Arbeitskopie** übergeben. Weitere verfügbare KI-Systeme sind ChatGPT, Claude und Gemini/Antigravity; Quoten und Termine sind flüchtige Betriebsangaben und **keine dauerhaften Architekturentscheidungen**. Claude/Fable 5.2 ist eine geplante spätere Option, keine Voraussetzung für Start oder Test.

## Verbindliche Unterlagen, keine neue Duplikat-Wahrheit

1. Dieses README als Gesprächs- und Arbeitsauftrag lesen.
2. `AGENTS.md`, `ANALYSE_REPOSITORY.md`, `STEPS_Zielstruktur.md`, `docs/architecture/architecture.md`, `docs/architecture/legacy-mapping.md`, `docs/architecture/migration.md` und `docs/system_reuse/GLIDE.md` lesen.
3. Bestehende fachliche Masterkonsolidierung bleibt `docs/project/overview/Steps_Projekt_Overview_konsolidiert_2026-11-09.md` mit sechs Quellen A–F, 40 Widersprüchen, 34 Lücken und ihren Originalbelegen. Technische Originalbeispiele und Archivdokumente unter `docs/project/` erhalten.
4. Zusätzlich existiert im Nutzer-Dateibestand die neuere `STEPS_Masterreview_V3_2026-11-10.md` mit 26 Untersuchungsdimensionen und dem `STEPS_Historienregister_100_V3.csv`. Diese V3-Masterprüfung war bei dieser Vorbereitung **noch nicht vollständig nach `steps/main` importiert**. Keine unrichtige Behauptung, sie liege bereits als aktueller Repo-Master vor. V2-Installer wegen reproduziertem Symlink-Escape **nicht verwenden**.
5. `knowledge/legacy/STEPS_BIBLIOTHEK_README.md`, `skills/music-harmony-coach/.../SKILL.md` und `knowledge/sources/RIGHTS_POLICY.md` für Forschung/Skill-Rollen lesen. Den Skill nicht als trainiertes Modell oder geprüfte Wissensbasis darstellen.
6. Glide-Quelle `01_Repository/Glide/src/glide/README.md` §9 und `00_Arbeitsvorbereitung/Glide_Uebergabe.md` für Reuse nutzen; lokales VS-Code-/Antigravity-Delta ist zusätzlich einzulesen.

## Wie hier gearbeitet wird

- **Preservation-first:** keine Löschungen, History-Rewrites, pauschalen Forks oder automatischen Datenimporte. Unterschiedliche historische Versionen bleiben nachvollziehbar.
- **Dokumentations-Wahrheit:** `PROJECT_OVERVIEW.md` ergänzt das Bestehende um aktuellen Transfer-/Produktauftrag und Prüfstände, ersetzt nicht sechs Originaldokumente oder die V3-Historie.
- **Kanonische Trennung:** `src/steps` = UI-freie Musikdomäne; `app/` = UI, Shell, Adapter, Lifecycle; `knowledge/` = validiertes eigenes Wissen; `research/` = Quellen, Rohmaterial und Recherche, nicht automatisch runtime-geeignet.
- **Gemeinsame Basis:** erst einen Glide-Service und einen UI-Host separat evaluieren, 2-Consumer-Verträge messen, dann über ein gemeinsam versioniertes Paket entscheiden.
- **Ein Schwerpunkt pro Agentenlauf:** kleine Diffs, eindeutige Quelldatei und SHA, fachliche Goldentests, unabhängige Review-Gates und reproduzierbarer Handover.
- **Externes Material:** öffentlich gespeicherte PDFs/HTML/Downloads/Screenshots/MIDI/Audio nur mit dokumentierter Rechte-/Provenienzprüfung. Eine Code-MPL-Lizenz macht Bücher und Audio nicht frei.

## Neuen Auftrag finden

- Produkt / Funktion: `PRODUCT_REQUIREMENTS.md` und `PROMPTS/02_PRODUCT_SCOPE.md`
- Roadmap / Gates: `ROADMAP_AND_GATES.md`
- UI-Grundgerüst: `ARCHITECTURE_AND_2_PANE_SHELL.md`, `MODULE_REUSE_MATRIX.md`, `PROMPTS/03_SHELL_MIGRATION.md`
- Gemeinsamer Systemkern: `PROMPTS/04_SHARED_CORE.md`
- Musiktheorie / Datenmodelle / MIDI: `PROMPTS/05_DOMAIN_MODEL.md`, `PROMPTS/06_MIDI_TIMELINE.md`
- Wissen / Quellen / Skill: `KNOWLEDGE_SKILL_PLAN.md`, `PROMPTS/07_KNOWLEDGE_INGESTION.md`, `PROMPTS/08_SKILL_EVALUATION.md`
- Sicherheit / Tests / Release: `QUALITY_AND_SECURITY.md`, `PROMPTS/09_QA_SECURITY.md`, `PROMPTS/10_RELEASE_GOVERNANCE.md`
- Konzepte, Entscheidungen, Gefahren: `SOURCE_AND_CONFLICT_REGISTER.md`, `DECISION_REGISTER.md`

## Zielzustand (langfristig, keine Ist-Aussage)

Eine funktionsfähige Steps-App mit zwei austauschbaren Arbeitsbereichen in vertrauter Shell, Akkord- und Drum-Spuren auf gemeinsamem Zeitraster, eigenständigem Projektformat und sicheren Speicher-/Undo-/MIDI-Verträgen, überprüfbar fachlichen Erklärungen und einem **kuratierbaren**, nicht halluzinierenden Harmony-Skill. Quellcode und Community-Contributions offen; benutzte fremde Materialien lizenzkonform. Gemeinsam genutzte Systembausteine durch stabile Contracts aktualisierbar, ohne Glide oder Steps bei jeder Änderung direkt mitzuändern.
