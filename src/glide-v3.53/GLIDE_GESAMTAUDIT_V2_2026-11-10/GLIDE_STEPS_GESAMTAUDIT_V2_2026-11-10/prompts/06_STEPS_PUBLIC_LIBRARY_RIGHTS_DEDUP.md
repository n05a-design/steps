# Bestehenden öffentlichen Steps-Bestand auf Rechte, Duplikate und Quellnachweise prüfen

**Prompt-ID:** `06_STEPS_PUBLIC_LIBRARY_RIGHTS_DEDUP` · **Arbeitsart:** ANALYSE (read-only, KEINE Datei löschen oder History umschreiben) · **Roadmap:** P2

> Lies zuerst `00_AGENTENVERTRAG.md` und die aktuellen Projekt-`AGENTS.md`. Dieser Prompt ist nicht die Freigabe für Remote-Änderungen.

## Begründeter Eingang / Primärquellen

Steps `main` voller Git-Tree und historische Inventare; `research/STEPS_Bibliothek`, `research/competitors`, `knowledge/legacy`, `ANALYSE_REPOSITORY.md`, `.gitignore`, `LICENSE`, `AGENTS.md`, Mozilla MPL FAQ, GitHub History Docs.

## Fachlich konkreter Arbeitsauftrag

Erzeuge ein reproduzierbares Tree- und bei lokalem Git-Zugriff SHA256-Dateiinventar nach aktuellem HEAD: Pfad, Blob-SHA, Dateigröße, Vermutungs-Rechtstatus, Urheber, Original-URL, Asset-klasse, Public/Private, Querverweise. Vorherige Größen (1931 Dateien, 60 PDFs ~452MB, 160 identische Gruppen/426 Extrapfade) nur als Vergleichsbasis, neu berechnen. Analysiere jede Gruppe getrennt: tatsächliches Binärduplikat, historische Variante, gleicher Inhalt mit anderem Provenienzkontext, eingefrorenes Quellarchiv. Erstelle eine Rights-Review-Queue nach Risiko (vollständige fremde Bücher/kommerziell, kopierte Websites, UI-Screenshots, eigene/CC-Bausteine, Code/Fonts). Erläutere MPL-2.0 file-level Copyleft vs. Rechte fremder Inhalte; **keine** juristische Schlussbehauptung aus Dateinamen. Bewerte Git-History-Folgen und sichere veraltete Links/Hashes vor einem möglichen späteren Rechtsverfahren. Entscheide **keine** History-Rewrite- oder Löschstrategie ohne Owner/Legal-Gate.

## Reproduzierbare Abnahmen und Gegenproben

Audit muss ohne Ausführen fremder MIDI-/HTML-/PDF-Skripte arbeiten, nur Metadaten/Dateien öffnen. Vergleiche `git ls-files`, Tree, Manifest, SHA; keine falsch identifizierte Löschung einer historisch anderen Datei. Rechte-Filterprobe: `unknown` darf nicht als `approved` in öffentliche Bundlemanifest-Dateiliste gelangen.

## Ergebnis und Übergabeformat

`RIGHTS_TRIAGE.csv`, `DUPLICATE_GROUPS.csv`, `SOURCE_PROVENANCE.csv`, `PUBLICATION_BLOCKERS.md`, `HISTORY_IMPACT.md`, kleine nichtdestruktive ADR-Optionen mit Owner/Legal-Review.

Nutze das exakt dokumentierte Format des Agentenvertrags mit `PASSED/FAILED/SKIPPED/NOT_RUN`, vollständigen Quell- und Laufzeitangaben. Weise zu jedem Blocker die kleinste mögliche Folgeprobe und das verantwortliche Gate aus.

## Grenzen und STOP

Kein `git rm`, kein Force-Push, keine Veröffentlichung der Rohmaterialien, keine ZIP-Kopie fremder Bücher in ein Reviewpaket. Wenn Zugriff auf Inhalte eingeschränkt: `UNKNOWN`, Pfad/Blob dokumentieren.
