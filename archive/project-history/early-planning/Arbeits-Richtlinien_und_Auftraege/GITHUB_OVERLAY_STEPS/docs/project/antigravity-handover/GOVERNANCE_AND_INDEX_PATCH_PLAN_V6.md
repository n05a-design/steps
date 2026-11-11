# Konkrete Nachtragspunkte an bestehenden STEPS-Einstiegen (V6, Vorschlag)

Nicht eigenmächtig vorhandene kanonische Dateien überschreiben. Nach Zustimmung als kleiner, separater Dokumentations-PR mit Tests/Linkcheck:

| Bestehende Datei | Minimaler Nachtrag | Warum |
|---|---|---|
| `AGENTS.md` | „**STEPS ist der aktive Workspace; `src/glide-v3.53/` ist die auf Glide 3.53 eingefrorene Referenz. Alle fachlichen Ergebnisse inkl. Analysen, allgemeiner Ausgaben und historischer KI-Arbeiten müssen nach `docs/operations/AI_CONTINUITY_PROTOCOL_V6.md` persistent registriert werden. Bei jeder Sitzung `STATE.json`/`OUTPUT_REGISTER.csv`/`NEXT_SESSION_HANDOVER.md` fortführen. Keine produktive Änderung oder Veröffentlichung ohne Gate/Ownerfreigabe.**“ | Modellneutraler Startvertrag, unabhängig von Antigravity |
| Root-`README.md` | Link zum `docs/project/antigravity-handover/README.md`, daneben aktueller STEPS-HEAD als datierter Snapshot, ausdrücklich „Glide 3.53 grün ≠ Steps-App fertig“. | Neue Nutzer/Modelle finden die korrekte Einstiegsschiene |
| Root-`SKILL.md` | Workflow-Schritt vor Produktarbeit: „Zuerst vorhandenes Ergebnisregister/Handover/Coverage und Quellenstatus lesen; jedes neue Audit-/Analyseergebnis in Outputregister sichern“. | Keine flüchtigen Ergebnisse |
| `docs/project/PROJECT_OVERVIEW.md` | Datierter Nachtrag zu Steps `1fc07e23...`, vollständigem `src/glide-v3.53/`-Import, Owner-Entscheidung, CI-Scope und Link zur V6-Anforderungsliste; Historie beibehalten. | Kein konkurrierender Masterbericht |
| `docs/operations/MULTI_AGENT_EXECUTION_AND_HANDOVER.md` | Referenz auf verbindlichen V6-Kontinuitätsvertrag, Tests und Retrospektiv-Register. | Konsistente Prozess-Single-Source |
| `prompts/README.md` | Neue Prompts `32`, `33`, `34`, `35` verlinken und `30/31` als V5-Vorlage/Meta-Review einordnen; ohne Bestandsprüfung keine doppelte 30/31 anlegen. | Auftragssuche und Versionslinie |
| `src/steps-0.00/README.md` | Vollständiger, überprüfbarer Patchentwurf in `SRC_README_PATCH_PROPOSAL_V6.md`. | Projektziel explizit im `src`-Kontext verankert |
| `tools/validation/check_structure.py` | **Noch kein Patch.** Erst Architektur-ADR über `src/steps/` als importierbaren Paketrootschritt; dann Validator, Tests, CI und Dokumentationspfade gemeinsam korrigieren. | Fehlgeschlagene Steps-Struktur-CI ohne Scheinlösung beheben |

Prüfgrenze: Diese Tabelle ist ein **Änderungsplan**. Keine der hier genannten bestehenden Dateien wurde in diesem Paket aktualisiert. Alle neuen Dateien sind additive Pfade und keine Abnahme eines produktiven STEPS-Codes.
