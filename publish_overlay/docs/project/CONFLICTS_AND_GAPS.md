# STEPS – aktualisiertes Widerspruchs-, Lücken- und Duplikatregister


> **Kritischer Aktualitätsnachtrag (10.11.2026, nach GitHub PR #75):** Der folgende Basisteil stammt aus dem früheren Paket und kann für Glide `main` noch den historischen Commit `61a2f3a`/Version 3.50.7 nennen. Der erneut verifizierte Stand ist **Glide `9e767bea` (3.53.0)**; der hochgeladene `app.pyw` ist blobgleich mit diesem HEAD, nicht aber bereits alle weiteren Module und Ressourcen unabhängig verifiziert. Aktuelle Bewertungen und Entscheidungsgates stehen in [`docs/project/PROJECT_OVERVIEW.md`](../../docs/project/PROJECT_OVERVIEW.md) und [`docs/audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md`](../../docs/audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md). Aussagen im folgenden Basisteil bleiben als **historisch datierte Ausgangsnotizen** erhalten, keine unmarkierte aktuelle Wahrheit.

**Stand:** 10.11.2026 (Europe/Berlin). **Status:** Entwurf und Prüfauftrag, keine Umsetzung/Freigabe. **Referenzstände:** Steps `main` `75329fef46878a5ac816cef3690e612a9e8fe52c`; Glide `main` `61a2f3ac2f0e1880e7fd8c0f3cfd9da0d0c9f16d`; lokal bereitgestellter Glide-Code `3.53.0`, SHA-256 `d7e19151eb0862a8ff58c4cc5e7d06a0452cde1daa73830ff97f54247bc75271`.

**Evidenz:** `UPLOAD` = bereitgestellte Datei, `GITHUB` = gelesener Remote-Stand, `BERICHTET` = in Unterlagen behauptet, `VORSCHLAG` = neue Empfehlung, `OFFEN` = unbestätigt. Kein dokumentierter Test bedeutet nicht bestanden.

## Erhalt historischer Register

Die ältere Übersicht führt **W-01 bis W-40** und **G-01 bis G-34** mit ausführlichen Einträgen und Quellenzeilen; diese bleiben vollständig erhalten in `source_archive/Steps_Projekt_Overview_konsolidiert_2026-11-09.md`, Kapitel 14 und 15. **Keine dieser Informationen wurde entfernt.** Hier wird nur die neue, tatsächlich am 10.11. verifizierte Delta-Lage beschrieben, ohne alte Einträge doppelt zu redigieren. Die 89 Quellabdeckungszeilen in `source_archive/Steps_Quellenabdeckung...csv` bleiben die Traceability-Matrix der früheren sechs Quellen.

## Aktuell entscheidungsrelevante Konflikte und Deltas

| ID | Priorität | Befund / Konflikt | Status / Entscheidungsvorlage |
|---|---|---|---|
| N-01 | P0 | Steps im Repository **Chord Progressions**, Nutzer nennt auch **Drum Progressions** und MIDI; ältere Overview vertagt Drums | Drums als Vision behalten, Zeitpunkt (MVP/Phase 2) Owner-ADR |
| N-02 | P0 | „Zwei Fenster“ gegen Screenshot mit einer Tk-Hauptshell, Sidebar und Arbeitsbereich | Reversible 2-Pane-Annahme; explizite Freigabe für echte 2 Toplevels |
| N-03 | P0 | Glide lokal 3.53.0 vs GitHub 3.50.7; Copilot arbeitet weiter | **keine** eigenständige Steps-Code-Abzweigung von ungesichertem lokalen Arbeitsstand |
| N-04 | P0 | Public `steps` enthält zahlreiche Fremd-PDFs/Webassets | Rechte-/History-Audit, bis dahin keine neuen fremden Volltexte pushen |
| N-05 | P1 | Snapshot älter `b42a990...` 1.827 Dateien, aktuell `75329fe...` 1.931 | datierte Auditstände statt zusammenrechnen; Delta-Manifest erstellen |
| N-06 | P1 | historische Bibliothek V6.6 unter `research/`, aber Legacy-Mapping verweist `02_Bibliothek/` | Verweis- und Linkprüfung, keine inhaltliche Migration ohne Review |
| N-07 | P1 | 49 ordner laut Screenshot und Repo sichtbar, 21/39 doppelt | Fallklassifizierung pro Datei/Quelle, keine automatische Folder-Merge |
| N-08 | P1 | Skill vorhanden, aber unter verschachteltem Datumsordner; `SKILL.md` root routet allgemein | Skill-Routen + Build-/Testvertrag, noch kein verified Ingest |
| N-09 | P1 | fachliche `registry.yaml` ist leer trotz 20 historischen Referenzen und 1.000 Archivdateien | Quellen mit provenance/review/license zuerst erfassen, nicht alle als approved |
| N-10 | P1 | `README_SETUP.md` sagt push false; aktueller Connector push true | historische Hinweise datieren, aktuelle Rechte nur von Live-Verbindung ableiten |
| N-11 | P1 | `Glide-System` V1.15 dokumentiert 147/25/311, GitHub-Code main 3.50.7 älter | Bestandsdatum/Commit je Modul erfassen, Isolation nicht aus Katalog ableiten |
| N-12 | P1 | historische Docs nennen ca. 1.146/1.166/1.306 V6.6-Dateien; aktueller gemessener Unterbaum 1.000 | unterschiedliche Zählgrenzen, nicht ohne Inventarrevision vereinheitlichen |
| N-13 | P1 | `docs/project/Archiv` hat fünf statt sechs historische Originale | Original C suchen/nachreichen; bis dahin nur Overview-Zitate verfügbar |
| N-14 | P1 | `src/steps` ist Scaffold trotz fertiger Theorie-Vorlagen | Implementierung und Fachtests separat nachweisen, kein Release aus README |
| N-15 | P2 | Nutzer nennt Modellzugriff „Fable 5.2“ und Tokens bis Mi/Do | nur als Ressourcenannahme verwenden; tatsächliche Plan-/Modellverfügbarkeit separat prüfen |

## Duplikat-Typen und sichere Behandlung

**D1 Byte-identisch:** 160 Git-Blob-Gruppen / 426 zusätzliche Pfade in Steps; Inventar und Verweisgraph, Rechte und Historie zuerst. Git dedupliziert identische Objekte womöglich schon. **D2 semantisch ähnlich:** 21- und 39-Ordner sowie Artikel-Sprachvarianten; nicht pauschal identisch. **D3 historisch:** 199/262/462/Ableton vs 28/143/609/123 (unterschiedliche Grundgesamtheiten und Versionen). **D4 sprachliche Wiederholung:** Nur in **neuen kanonischen Texten** entfernen, alte Belegtexte ungekürzt archivieren. **D5 Namenskonflikt:** unterschiedliche STEPS-Akronyme bleiben bis Entscheidung unaufgelöst.

## Blockierende Abnahmegates

- P0-A Owner: Steps Scope mit Drums/Audio/Offline/Plattformen und 2-Pane vs 2-Toplevel dokumentieren.
- P0-B Engineering: Glide 3.53.0 vollständig mit Modulen, Ressourcen, Tests, Repo-SHA sichern und Diff gegen 3.50.7 dokumentieren.
- P0-C Legal: Softwarecode, Fonts, Logos, PDFs, Midi, Websites/Blogassets je Material freigeben oder intern isolieren.
- P0-D Data: importierbare Source-IDs, schema-versions und Validation Seeds vor Knowledge-Integration schaffen.
- P0-E QA: durchgängiger Head-SHA, isolierte Testdaten, Cross-Platform-Tests, menschliche Sichtprüfung, keine Rotergebnisse übergehen.

**Offene Punkte dürfen nicht durch plausibles Raten geschlossen werden.** Ein beschlossener ADR sollte einen Ausgangskonflikt samt Belegen, verworfenen Optionen, Auswirkungen und Rücknahmeweg ausdrücklich verlinken.
