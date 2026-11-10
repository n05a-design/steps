# STEPS – Codex: Migration der nach Stichworten strukturierten Bibliothek (V5.2)

## Auftrag

Die vorliegende Bibliothek V5.2 zunächst **nur analysieren** und mit dem echten lokalen Steps-Projekt und dessen Agentenregeln vergleichen. Das Paket ist eine vollständige Dateinamens-/Kategorien-Migration der 278 vorhandenen V5.1-Dateien, keine neue wissenschaftliche Quellenedition.

1. `git status`, Branch, AGENTS.md, Knowledge Base, Skills und bestehende Dokumentationsversionen prüfen; Änderungen erhalten.
2. `STEPS_DATEIENINDEX_ALLE_278.csv` einlesen: pro Datensatz old_path/new_path/sha256/domain/keywords/type/version/status vergleichen.
3. Ein kontrolliertes Zielverzeichnis im echten Repo festlegen; bestehende Inhalte weder löschen noch blind überschreiben.
4. Quellen, geschützte Kursoriginale und private MIDI-Artefakte anhand tatsächlicher Dateirechte **separat** halten. Nicht als öffentlich redistributierbar annehmen.
5. Für die vier ursprünglichen Hauptbereiche und die zwei neuen Forschungsbereiche je einen kanonischen Einstiegspfad vorsehen; Historie nur referenzieren.
6. Alte Links im Projekt prüfen; Migration/Redirect-Index aktualisieren, keine unreferenzierten Dateien zurücklassen.
7. Alle in `STEPS_ABDECKUNG_UND_LUECKEN.md` enthaltenen Teilgebiete gegen tatsächliche Repository-Inhalte prüfen; Status anhand Evidenz ggf. korrigieren.
8. Prioritäten P0-P2 aus `STEPS_PRIORISIERTES_LUECKENREGISTER.md` zu umsetzbaren, prüfbaren Aufgaben machen.
9. Nur geeignete, belegte und lizenzrechtlich zulässige Fachinhalte in die öffentliche Knowledge Base übernehmen; existierende Prüf- und Reviewstatus beibehalten.
10. Validierung: Pfadexistenz, IDs, SHA, Datenformate, Referenzauflösung, Versionsbezüge, Duplikate und fachliche Prüfungen getrennt protokollieren.

## Abnahme

- Im echten Repo ist ein navigierbarer kanonischer Bibliotheksindex vorhanden, ohne kaputte Links oder verlorene Originalinhalte.
- Jede importierte Datei ist mit fachlichem Gebiet, Zweck, Version, Herkunft und Prüfstatus eindeutig dokumentiert.
- Sechs Bereiche sind auffindbar, aber keine fehlenden Quellen oder nicht ausgeführten Tests werden als `reviewed` gekennzeichnet.
- PPR-Lektionstexte und private HTML/MIDI nicht ungeprüft öffentlich committet.
- Ein nachvollziehbarer PR/Diff mit Testbericht liegt vor; **kein Auto-Merge**.

**Dieses Dokument ergänzt den bisherigen Codex-Masterauftrag V5 und das Drum-/Producer-Arbeitspaket V5.1; es ersetzt keines von beiden.**
