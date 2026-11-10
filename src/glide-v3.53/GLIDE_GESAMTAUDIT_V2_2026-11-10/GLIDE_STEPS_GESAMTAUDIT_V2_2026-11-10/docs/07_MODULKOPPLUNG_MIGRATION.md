# 07 — Nachweisbare Kopplungen, Modulstrategie und Safe-Strangler-Migration

## Befund und methodische Grenze

Das aktuelle Systemregister listet 94 Glide-Hauptmodule und 25 Kandidatenpakete. Die neue Prüfung hat die meisten separaten `.py`-Dateien über GitHub-Quelltextabrufe und deklarierte `import`/`from`-Angaben ausgewertet. **Dies ist kein vollständiger dynamischer Import-/Callgraph:** relative `importlib`, import-time side effects, lazy import, `app.pyw` (3,59 MB), Tk-Events, Nutzdatenobjekte und native Ressourcen erfordern einen echten lokalen AST-/Runtime-Lauf. Daher ist *reuse-potential* nur `PROPOSED`, nicht `TESTED`. Das Einzelfile-`app.pyw` ließ sich über die verwendete Schnittstelle nicht vollständig abfragen; weitergehende Behauptungen über konkrete Methoden beruhen auf Glide-Architektur-/Systemdokumenten.

## Explizit beobachtete Importkanten (Auswahl aus direkt gelesenen Quellmodulen)

| Modul | Lokale Imports | Kopplungsfolge |
|---|---|---|
| `appearance.py` | `backdrop` | Theme pure logic kann als Kette übernommen werden, aber Anwendung auf Tk-Widgets/Fontmetriken gesondert |
| `logo.py` | `svg_geometry`, `logo_raster`, `brand` | Logo wird nur mit Ressourcen-/Markentransfer produktneutral |
| `svg_geometry.py` | `brand` | selbst vermeintlich generische SVG-Geometrie ist markengekoppelt |
| `side_view.py` | `object_references` | Secondary View ist nicht unabhängig von Glide-Objektreferenzen |
| `action_menu.py` | `content_search` | Palette/Aktion hat Abhängigkeit auf Suchnormalisierung |
| `drawing_image.py` | `drawing` + direkter Tk-Import | Tk-Bildadapter darf nicht in eine Tk-freie Core-Package-Schicht |
| `image_preview.py` | `preview_tools`, `image_conversion` + Tk | Bildhost, Cache, Runtime getrennt behandeln |
| `session_guard.py` | `backup_snapshot`, `data_lock`, `storage_health` | Speicher-/Lock-/Recovery-Regeln als atomare Einheit prüfen, nicht einzeln kopieren |
| `persistence.py` | `save_result` | Commit- und Post-Commit-Fehlerstatus vollständig übernehmen |
| `schema_backups.py` | `storage_health` | Backup-Policy und Speichergrenzen gemeinsam testen |
| `markdown_tree.py` | `object_references`, `page_markdown`, `drawing`, `task_references` | **Task-/Seiten-/Zeichnungs-Domain**, kein generischer Markdown-Adapter |
| `page_restore.py` | `object_references`, `task_references`, `attachment_paths` | Referenz- und Asset-IDs/Restore hängen am Glide-Schema |
| `notion_import.py` | `notion_archive`, `notion_hierarchy`, `notion_reimport`, `object_references`, `page_restore`, `source_metadata`, `task_references` | Hohe transitive fachliche Kopplung, nicht als Steps-MVP übernehmen |
| `ics_busy.py` | `ics_recurrence`, `ics_timezone`, `timezones`, `occupied_time` | Kalenderzeit ≠ musikalische Tick-/Beatzeit |
| `busy_calendar.py` | `ics_busy`, `ics_recurrence`, `occupied_time`, `timezones` | unabhängig vom Musikdomainmodell und daher ausschließen |
| `day_relief.py` | `planning`, `occupied_time` | Aufgabenplanungsdomäne, bewusst nicht in Shared Core |
| `exchange_recipes.py` | `exchange_patch`, `ui_design` | Datenaustausch kann UI-/Produktanahmen tragen |
| `core_accessibility.py` | `accessibility`, `accessibility_bindings` | reiner Semantik-Kern vs. Plattform-/Widgetadapter zu prüfen |

## Einordnung aller 25 dokumentierten Bausteine

| ID | Entscheidungsklasse | Ziel in Steps | Besonderes Gate |
|---|---|---|---|
| B01 Theme/Design | ADAPT P0 | Palette/Font/Theme pure policies, UI-Adapter | Fenster-/Glyph-/DPI-Tests |
| B02 Brand/Logo | ADAPT P0 | Algorithmus + eigene Steps-Assets | Masterfile, Lizenz, Plattform-Paketicons |
| B03 Window/Layout | ADAPT P0 | Geometrie-Policy, WindowHost | Lifecycle, Fokus, Resize, 2-Fensterwahl |
| B04 UI-Navigation | REBUILD-ADAPTER P0 | Neutraler NavigationProvider und CommandRouting | keine Glide-IDs |
| B05 Persistence | REUSE-CONTRACT P0 | Commit-/Lock-Plan mit Steps-Schema | Crash/Restore, Fremdprodukt-Isolation |
| B06 Backup | REUSE-CONTRACT P1 | Snapshot-/Restore-Policy | Format-/Asset-/Versionsregression |
| B07 Exchange | DEFER | nur sichere generische Reader bei Bedarf | Rechts-/Eingangsparsing |
| B08 Media | OPTIONAL | Bildpreview für Musikblätter | Thread/Freigabe/UI-Hooks |
| B09 Accessibility | ADAPT P0 | Rollen/Widgetsemantik | Keyboard/Reader/Mac/Win/Linux |
| B10 QA/Release | ADAPT P0 | CI-/Beleg-/SBOM-Prozess | keine alten Glide-Paths/alte QA-Siegel |
| B11 Task Planning | EXCLUDE | Glide bleibt alleiniger Besitzer | Importverbots-Test |
| B12 Time/Focus | OPTIONAL | evtl. UI-Timer, **nicht** BPM-Musikmodell | Clock/Thread/Screen |
| B13 Search/Action | ADAPT P1 | Suchprovider, Commands | einheitliche Actions und Disabled Gründe |
| B14 ICS/Timezone | EXCLUDE | nicht für MIDI-Takte verwenden | Importverbots-Test |
| B15 Rich Text | DEFER/ADAPT | eigene Steps-Lernnotizen später | Schema-/Lizenz-/Taskreferenzen |
| B16 Undo/Mutation | REUSE-SEMANTICS P0 | transaktionaler Stack, eigene Musikkommandos | stale-reference/redo/save/undo |
| B17 Attachment/Restore | ADAPT P1 | eig. Project-MIDI/Assetimport | ZIP traversal, symlink, Disk full |
| B18 Home Widgets | DEFER | neue Musik-Overview später | kein Taskdashboard |
| B19 Sidebar/Secondary | ADAPT P0 | neutrale Selection/SlotProvider | Return Focus, Cleanup, Scroll |
| B20 Pixel Drawing | EXCLUDE-NOW | kein Harmony-Produktbedarf bestätigt | nur bei späterer Freigabe |
| B21 Diagnostics/Health | ADAPT P0 | Fehler-/Sicherheitsberichte | Pfade redigiert/Logs getrennt |
| B22 Notion Adapter | EXCLUDE-NOW | kein Aufgabenimport in Steps | fachliches Scope-Gate |
| B23 Governance | REUSE-PROCESS P0 | Dokumentations-/QA-Regeln übertragen | neue Steps-Entscheidungen statt Glide-D-Kopien |
| B24 Bootstrap/Settings | REFACTOR-HARD P0 | RuntimePaths, SettingsStore, StartAdapter | WA-49 side effects, OS-/Data-ID |
| B25 OS-Integration | OPTIONAL | DnD/Notifications/External-open | capability check, native Builds |

**P0** bedeutet Priorität im technischen Core-Schnitt, nicht automatisch Release-MVP. Exclude/Defer bewahrt die Originalfunktion in Glide.

## Phasenplan der Extraktion

**E0: Reproduktive Baseline.** Lokaler frischer isolierter Checkout am ausgewählten Glide-SHA. Kein Schreibzugriff auf echte Nutzerdaten. Modul-/AST-/Importgraph, Testabdeckung, Source-/Resourcehashes, aktuelle Tk-Version, widget tree, Aktionen. Der Copilot-Entwicklungszweig wird **nicht** parallel bearbeitet.

**E1: Runtime/State-Port.** `RuntimePaths` explizit, DataDir-Auflösung vor jeglicher Importschleife; UI-Commands getrennt von Domain-Mutationen. Die bestehende Glide-API bleibt zunächst gleich, Wrapper delegieren an neue interne Port-Methoden. App-Fachoperationen bleiben funktionsgleich; negative Regressionen als Gegenprobe.

**E2: Ein vertikaler, kleiner UI-Schnitt.** Theme/Logo oder ein reiner Sidebar-State als eigenständige Testkomponente. Zuerst `GLIDE_TEST` im getrennten Arbeitsbaum, danach Steps-Dummy-Consumer. Originale i. d. R. nicht massenhaft verschieben; alte Importnamen vorübergehend als Kompatibilitätsadapter.

**E3: Shell und zwei Slots.** UI-Komponenten nur über neutrale Command-/Navigation-/Workspace-Ports; die Slots tragen keine Taskmodelle. Test: kein Import von `task_editing`, `planning`, `object_references` aus Steps-Shell zur Laufzeit. Lifecycle-Fokus, Modality, DPI, Regression, keine fehlende Restfläche.

**E4: Gemeinsame Core-Releases.** Erst nach bilateraler Integration in Glide und Steps, stabiler `Public API`, klarer Packaging-/License-/SBOM-Matrix. Core-Version aus eigenem Git-Tag/ChangeLog statt `GLIDE_SYSTEM_VERSION` abzuleiten. Produktupdates dürfen bewusst zeitversetzt bleiben.

## Nicht-Regression für Glide

Trotz Extraktion müssen alle bisherigen Tab-/Sidebar-/Context-/Undo-/Save-/Backups/-Exports/-Settings-Funktionen erhalten bleiben; Struktur- und Datenformatversion nicht unbemerkt verändern. Backward-compatible Facades können temporär sinnvoll sein; *zwei getrennte Implementierungen derselben Fachmutation dürfen nicht entstehen*. Performance auf denselben künstlichen Fixtures und derselben Tk-/OS-Version mit Median/p95 und Fehler-/Undo-Vollständigkeit vergleichen. Flutter/Qt/Migration der GUI wird nicht nebenbei eingeführt.

## Offene technische Belege

- AST des vollständigen `app.pyw` und aller dynamischen Event-/Importpfade.
- Abhängigkeitsgraph einschließlich Ressourcen, native Tk-DLL/Fonts, Tools und Tests, nicht nur Python-Imports.
- Quell- vs. ausgelieferte `07_Python-Versionen`-Dateien für denselben 3.53-Stand.
- Exakte Version-/Schema-/Konfigurations- und Windows/macOS/Linux-Pfadstrategie des neuen Steps.
- Reale Laufzeiten und Regressionstoleranzen der neuen Shell auf synthetischen Daten.
- Restore/Undo/Shutdown bei Worker-/Tk-Teardown und schreibgesperrtem Datenordner.

Diese Punkte gehören in echte Codex-/Claude-Implementierungsprüfungen, nicht als bereits bestätigte Fähigkeiten in README-Texte.
