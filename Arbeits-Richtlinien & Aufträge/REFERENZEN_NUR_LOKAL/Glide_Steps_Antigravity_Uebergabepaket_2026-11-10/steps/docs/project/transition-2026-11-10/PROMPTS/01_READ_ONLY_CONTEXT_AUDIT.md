# P01 – Steps-Gesamtinventur und lokale Übergabe (nur lesend)

## Direkt nutzbarer Prompt

Du bist technischer Projekt-Auditor für `n05a-design/steps`. **Nur lesen und analysieren**; keine Repository-Schreiboperation, kein `git pull`, `reset`, `clean`, `stash`, History-Rewrite, automatische Migration oder ungetestete Skriptausführung.

1. Erfasse `git status --porcelain`, aktuelles Arbeitsverzeichnis, Remote, Branch, Voll-SHA, Status der Submodule/Worktrees. Vergleiche gezielt `main` mit dem für den 10.11.2026 beobachteten `75329fef46878a5ac816cef3690e612a9e8fe52c`. Abweichungen/neuere lokale Arbeit haben Vorrang vor eingefrorenen Dokumentständen.
2. Lies die vollständigen **projektrelevanten Textdokumente**: `AGENTS.md`, `SKILL.md`, `ANALYSE_REPOSITORY.md`, `STEPS_Zielstruktur.md`, `docs/project/overview/Steps_Projekt_Overview_konsolidiert_2026-11-09.md`, `docs/project/Archiv/`, `docs/architecture/`, `research/gaps/OPEN_GAPS.md`, `knowledge/legacy/STEPS_BIBLIOTHEK_README.md`, `skills/music-harmony-coach/`, `schemas/` und die aktuelle V3-Masterprüfung, falls im lokalen Bestand. Dokumentiere alle nicht zugänglichen Quellen explizit.
3. Erzeuge *lokal ohne Inhaltskopien fremder Werke* ein vollständiges Dateiinventar nach Dateityp, Bereich, Größe, Hash, Provenienzstatus, historischer Version, Verdachtsduplikat und rechtlichem Prüfstatus. **Keine automatische Deduplizierung**. Prüfe, ob die sechste ursprüngliche Fable-Quelle im öffentlichen Originalarchiv fehlt. Quell-/Asset-Menge nicht mit rechtlich verwertbaren Werken gleichsetzen.
4. Erstelle einen vollständigen Crosswalk aller ursprünglichen W01–W40, G01–G34, DEC01–DEC26, mit aktuellem Nachweis/Status und Quellpfad. Bewahre die Historie; wo V3-Register schon existiert, verlinke es statt Einträge neu und widersprüchlich zu kopieren.
5. Trenne Implementierung, Scaffold, Forschung, lizenzierte Beispiele, Rechtsrisiken und Ideen. Finde veraltete oder widersprechende Status-/Versionsangaben. Die existierenden `src/steps`- und `app`-READMEs sind **keine Implementierungsnachweise**.
6. Liefere eine priorisierte `read-only` Übersicht über (a) bestätigte Fakten (b) zeitlich überholte Aussagen (c) unaufgelöste Widersprüche (d) Daten-/Rechterisiken (e) umsetzbare Arbeitsaufträge. Prüfe Links und Indizes, ohne fremde Originale zu ändern.

## Akzeptanz

Vollständige Inventurliste der lokal erreichbaren Quellen; gemessene Anzahl pro Format; geschlossener, quellverlinkter W/G/DEC-Crosswalk; keine als vollständig gelesenen ungelesenen PDFs/MIDI behaupten; Keine Git-/Dateimutation. Ein **separater** Vorschlag für neue Dokumente ist erlaubt, aber nicht direkt umsetzen.
