# Glide 3.53: Baseline, Freigabegates und tatsächlicher Teststand

**Prompt-ID:** `01_GLIDE_353_BASELINE_QA` · **Arbeitsart:** ANALYSE (keine Codeänderungen) · **Roadmap:** P0/P1

> Lies zuerst `00_AGENTENVERTRAG.md` und die aktuellen Projekt-`AGENTS.md`. Dieser Prompt ist nicht die Freigabe für Remote-Änderungen.

## Begründeter Eingang / Primärquellen

Glide `VERSION`, `GLIDE_SYSTEM_VERSION`, `00_Arbeitsvorbereitung/Glide_Uebergabe.md`, `docs/07_QA_BERICHT.md`, `docs/05_QA_TESTPLAN.md`, `scripts/pflege/abgleich_07.py`, GitHub Actions und jeweiliger konkreter Commit.

## Fachlich konkreter Arbeitsauftrag

Lies zuerst den aktuellen HEAD und die letzte Pipeline. Erstelle eine Tabelle für jede testende Entität (CI-Job, lokal eingefrorener Windows-Volltest, Linux-Test, nativer macOS-Gesamttest, native Paketstarts, menschliche Sicht/DPI/Mehrmonitor-Abnahme): `SHA`, Datum, OS/Python/Tk, Kommando/Run-ID, Exit, Skips, Artefakt-Hashes, manuelles Urteil. Trenne `3.53.0` als in Git vorhanden, Pipeline vollständig grün, Paket gebaut, tatsächlich gestartete App, menschlich akzeptierte UI und für Release autorisiert. Führe `historical red` gesondert statt daraus einen aktuellen Rotstatus zu machen. Prüfe `src/glide`↔`07_Python-Versionen`-Hashabgleich nur, wenn Zugriff und Testumgebung wirklich vorhanden sind; keinen fremden Freeze ohne Zustimmung verändern. Wenn ein Check bei gleicher SHA offen ist, benenne die passende zwingende Gegenprobe; reduziere nie Qualitätsgrenzen zugunsten eines schnellen grünen Status. Exakte 3.53-Quellbasis für spätere Steps-Spikes und freigegebene Produktbasis separat markieren.

## Reproduzierbare Abnahmen und Gegenproben

Keine Tests in echter Nutzerablage. Bei Prüferlaubnis nur isolierte `GLIDE_DATA_DIR`-Daten, feste Test-Commit-ID und Tk-Version. Regression bei Schriftwechsel D77 (vier Familien, Gewicht, UI-Symbole), Fensterkopf D75/76, `test_tempo330`, `test_seitenkarten`, `test_arbeitsmodi`, Undo/Save/Startup; notiere Skips. Wenn kein OS-Zugriff: `NOT_RUN`, nicht `PASS`.

## Ergebnis und Übergabeformat

`baseline_status.md`, `CI_MATRIX.csv`, `RELEASE_GATE.md`, Liste fehlender Build-/Hardware-/Humanbelege, *exakte* Testbefehle nur aus tatsächlich vorhandenen Quellen. Entscheidung „für experimentellen Branch akzeptabel“ separat von „Release approved“.

Nutze das exakt dokumentierte Format des Agentenvertrags mit `PASSED/FAILED/SKIPPED/NOT_RUN`, vollständigen Quell- und Laufzeitangaben. Weise zu jedem Blocker die kleinste mögliche Folgeprobe und das verantwortliche Gate aus.

## Grenzen und STOP

Ein neuer HEAD ohne zuordenbare Testläufe, ein roter Pflichtlauf, fehlende Datenisolation oder ungeklärte OS-Abnahme verhindert die jeweilige Freigabe. Nicht automatisch `main` überschreiben, mergen, taggen oder veröffentlichen.
