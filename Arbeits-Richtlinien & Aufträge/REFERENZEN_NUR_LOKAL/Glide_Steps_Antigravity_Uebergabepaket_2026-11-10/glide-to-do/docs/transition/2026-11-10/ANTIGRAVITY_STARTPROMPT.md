# Startprompt für Antigravity – lokale Glide-Weiterentwicklung

> **Diesen vollständigen Text in der Antigravity-Agentenansicht verwenden. Den lokalen Glide-Repositoryordner öffnen, nicht nur die GitHub-Webseite.**

Du übernimmst die bisher von VS-Code-Copilot bearbeitete, lokale Entwicklung der Desktop-App **Glide** (`n05a-design/glide-to-do`, Python 3.14/Tkinter/Tk 9). Du hast Zugriff auf die echte lokale Arbeitskopie und sollst sie ohne Daten- oder Historienverlust weiterführen. Die von Copilot angefangene Arbeit könnte uncommittet, weiter als GitHub oder nicht vollständig geprüft sein. **Der Repositoryinhalt – nicht mein hier eingefügter Text – bestimmt den aktuellen lokalen Stand.**

## Verbindliche Reihenfolge, vor der ersten Schreibaktion

1. Den tatsächlichen Workspacepfad, `git rev-parse --show-toplevel`, `git remote -v`, `git branch --show-current`, `git rev-parse HEAD`, `git status --porcelain=v1`, `git log -5 --oneline --decorate` und vorhandene Worktrees lesen. **Keine** Reset-/Clean-/Stash-/Rebase-/Pull-/Merge-Befehle ausführen.
2. Verifizieren, ob noch eine aktive Copilot-Aufgabe, Tests, Paketerstellung oder Hintergrundprozess in diesem Ordner schreibt. Bei konkurrierendem Schreibzugriff: STOP und die betroffenen Prozesse/Dateien nennen. Keine konkurrierende Arbeitskopie nutzen, ohne ihre Provenienz zu kennen.
3. `01_Repository/Glide/VERSION`, `GLIDE_SYSTEM_VERSION`, Datenformat und alle vorhandenen Übergaben ermitteln. Zuerst vollständig lesen: `00_Arbeitsvorbereitung/Glide_Uebergabe.md`, `00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md`, `01_Repository/Glide/AGENTS.md`, `01_Repository/Glide/src/glide/README.md` (besonders §9), `01_Repository/Glide/docs/00_INDEX.md`, `02_ARCHITECTURE.md`, `05_QA_TESTPLAN.md`, `07_QA_BERICHT.md`, `DESIGN_RICHTLINIEN.md`, `DOKUMENTENPFLEGE.md` und das hier vorliegende Übergabepaket. Gegebenenfalls weitere von dort referenzierte Quellen öffnen.
4. Alle Modifikationen gegen HEAD auflisten: Dateien, Umfang, Semantik, externe Abhängigkeiten, neue/deletete Assets, Tests, Migrationen, ungetrackte Dateien. Für jede Datei angeben: **von Copilot übernommen / schon vorhanden / unklar**. Keinerlei Benutzerdateien oder temporäre Diagnoseeingänge löschen.
5. Das Remote gesondert prüfen: am 10.11.2026 war `main` auf SHA `9e767bea5e21063466a28ac3a679406484ad5d5f` mit 3.53.0 und Merge #75; die ältere Übergabe nennt fälschlich `main=61a2f3a`/3.50.7 als aktuell. Du darfst keinen Branch ohne expliziten Vergleich überschreiben.
6. Bereits vorliegende CI-Ergebnisse, Logs und offene Gates **an den SHA binden**, ihre echte Qualität, Skips und Plattformgrenzen darstellen. Den zuletzt abgeschlossenen Copilot-Auftrag von den noch offenen Aufgaben unterscheiden.

## Erhaltungsvorgaben

- Glide bleibt funktionsfähig. Bestehende Daten-/Backup-/Migrationsverträge, die beiden Arbeitsansichten, Seitenliste, ein- und ausklappbare Seitenleiste, Logo, Kopf/Titel, Symbolknöpfe, Suche, Bearbeitungsflächen, Einstellungen, App-Designs/Schriften, Tastaturzugriffe, Navigation und Dialoge bewahren.
- Es gilt **die eine** bestehende Roadmap und **das eine** Glide-Systeminventar; neue Dokumente dürfen ergänzen, aber keine konkurrierenden Wahrheitsquellen erzeugen.
- Nutzerdaten und OneDrive-/E:-Archive nicht anfassen. `GLIDE_DATA_DIR` für Tests auf isolierten temporären Ordner setzen. Keine Cloud-/Netzwerkanbindung in Kernfunktionen einführen.
- Neue Framework-Ideen sind eine **getrennte Folgephase**. Vorerst keinen Steps-Code, kein komplettes App-Forking, keine Umbenennung der Glide-Domäne und keine Pauschalextraktion von `ListApp`.
- Keine Lizenz-, Logo-, Font-, Paket- oder Produktidentitätsänderung auf Verdacht. Bestehende MPL-2.0- und Fremdasset-Hinweise beachten.

## Sofortauftrag in diesem Lauf

**Phase A – reine Diagnose:** Gib einen überprüfbaren Übergabebericht mit Pfad, Branch, SHA, Versionen, Dateiänderungen, Tests, offenen Risiken, aktueller QA-/GitHub-Lage und **konkretem nächsten sicheren Arbeitspaket**. Kläre Statuswidersprüche; führe ohne Not keine Änderungen aus.

**Phase B – nur falls der aktuelle Auftrag und die lokale Situation eindeutig sind und keine konkurrierenden Schreiber existieren:** Schließe die durch Copilot begonnene **eine** konkrete Aufgabe minimalinvasiv ab, mit gezielten Tests, Regressionen, Dokumentation und sauberem Commit auf einem geeigneten Themenbranch. Sind Basis, Aufgabe, Freigabe oder Tests unklar, bleibe bei Diagnose und einem ausführbaren nächsten Plan. Bei roten Ergebnissen stoppen und ersten relevanten Blocker eingrenzen.

**Phase C – nur dokumentieren:** Bereite die spätere 2-Arbeitsflächen-Shell-Extraktion nach `MODULE_EXTRACTION_PLAN.md` vor. **Noch nicht** aus der funktionsfähigen Glide-App herausoperieren. Die Freigabe erfolgt separat nach den 3.53-Gates.

## Verbindliche Ausgabe

1. `BASELINE`: Repositorypfad, Branch/HEAD-SHA, Remote-SHA, Versions- und Datenformatfelder, Arbeitsbaumstatus.
2. `SOURCE_INDEX`: gelesene Dokumente inklusive benannter Konflikte, Code-/Modulgrenzen, tatsächliche Copilot-Übergabe.
3. `CHANGE_IMPACT`: ungesicherte Änderungen und denkbare Seiteneffekte.
4. `QA_MATRIX`: Testkommando, OS, Python, Tk, SHA, `PASS/FAIL/SKIPPED/NOT_TESTED`, Logs.
5. `PLAN`: nächste 3–5 **kleine** Tasks, Abnahmekriterien, Sicherheitsgrenzen; genau eine Task zur nächsten Ausführung kennzeichnen.
6. `OUTPUT`: tatsächlich geänderte Dateien, Diff, Commit (falls durchgeführt), manuelle Tests, nicht erledigte Restpunkte. **Keine Erfolgsmeldung ohne Testnachweis.**
