# Modul- und Funktions-Reuse: Glide-System → Steps


> **Kritischer Aktualitätsnachtrag (10.11.2026, nach GitHub PR #75):** Der folgende Basisteil stammt aus dem früheren Paket und kann für Glide `main` noch den historischen Commit `61a2f3a`/Version 3.50.7 nennen. Der erneut verifizierte Stand ist **Glide `9e767bea` (3.53.0)**; der hochgeladene `app.pyw` ist blobgleich mit diesem HEAD, nicht aber bereits alle weiteren Module und Ressourcen unabhängig verifiziert. Aktuelle Bewertungen und Entscheidungsgates stehen in [`docs/project/PROJECT_OVERVIEW.md`](../../docs/project/PROJECT_OVERVIEW.md) und [`docs/audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md`](../../docs/audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md). Aussagen im folgenden Basisteil bleiben als **historisch datierte Ausgangsnotizen** erhalten, keine unmarkierte aktuelle Wahrheit.

**Stand:** 10.11.2026 (Europe/Berlin). **Status:** Entwurf und Prüfauftrag, keine Umsetzung/Freigabe. **Referenzstände:** Steps `main` `75329fef46878a5ac816cef3690e612a9e8fe52c`; Glide `main` `61a2f3ac2f0e1880e7fd8c0f3cfd9da0d0c9f16d`; lokal bereitgestellter Glide-Code `3.53.0`, SHA-256 `d7e19151eb0862a8ff58c4cc5e7d06a0452cde1daa73830ff97f54247bc75271`.

**Evidenz:** `UPLOAD` = bereitgestellte Datei, `GITHUB` = gelesener Remote-Stand, `BERICHTET` = in Unterlagen behauptet, `VORSCHLAG` = neue Empfehlung, `OFFEN` = unbestätigt. Kein dokumentierter Test bedeutet nicht bestanden.

Die Bestandsliste V1.15 nennt 94 Quelldateien, 147 Features, 25 Bausteine und 311 Test-/Werkzeugdateien; das **vollständige** Original ist `source_archive/README-Glide-System.md` (967 Zeilen). Keine hier verkürzte Tabelle ersetzt den Katalog mit sämtlichen Modul-IDs M001–M094 und Feature-IDs. Die folgende Tabelle ist die **arbeitsbezogene** Entscheidungsmatrix, keine Behauptung bereits durchgeführter Portierung.

| Welle | Kandidat/Modul | Wert für Steps | Kopplung/Risiko | Zielvertrag/Prüfung |
|---|---|---|---|---|
| W0 | `app.pyw` / `ListApp` | UI-Behaviors als Referenz | sehr hoch – 1.866 Methoden lokal | nur Methodenextraktion, niemals Ganzdatei als Steps-Domain |
| W1 | `appearance.py`, `ui_design.py`, `font_catalog.py` | Designpaare, Token, Fonts | Theme-Widget/Tk/Font-Lizenzen | `ThemeTokens`, isolierte Kontrast-/Runtime-Tests |
| W1 | `brand.py`, `logo.py`, `logo_raster.py`, `svg_geometry.py`, `glyph_metrics.py`, `symbol_policy.py` | eigene Logos/Symbole erstellen | Glide-Master, private Fonts, Host-Caches | `BrandAssetsPort`, externe Rechte, optische Tests |
| W1 | `compact_mode.py`, `sidebar_policy.py`, `render_retention.py` | Sidebar, Kompaktmodus, Widget-Lifecycle | ListApp-Callbacks | `SidebarState`, `ViewportState`, Alt-Toggle-Regression |
| W1 | `action_catalog.py`, `action_menu.py`, `interaction_policy.py` | Icon-Toolbar, Commands, Palette, Shortcuts | alte Task-Aktionsnamen | `ActionRegistry` mit deklarativen no-ops, alle Hotkeys prüfen |
| W1 | `release_notes.py`, `runtime_check.py`, `settings_compat.py` | Startcheck, Update-Hinweise, unbekannte Settings erhalten | Paths und Versionsformat | Steps-spezifische Version und Konfig |
| W1 | `motion.py` | sichere, unterbrechbare Übergänge | `after` / Tk Shutdown | Canvas-/Timer-Lifecycle-Tests |
| W2 | `persistence.py`, `save_result.py`, `save_comparison.py` | sicheres Schreiben, Backup, Fehlerzustände | Glide-Taskdaten, Autosave-Mutation | `StoragePort` mit Steps-Schema, Atomic/Restore Tests |
| W2 | `schema_backups.py`, `backup_catalog.py`, `storage_health.py`, `data_lock.py`, `session_guard.py`, `runtime_diagnostics.py` | Langlebigkeit, Lock, Diagnose, Restore | App-Pfade, Plattformen | eigene Steps-Ablage, Absturz-/Wiederanlauf-Fixtures |
| W2 | `content_search.py`, `side_view.py`, `view_definition.py`, `filter_explain.py` | Such-/Ansichtsoberfläche | Aufgabenfilter/IDs | `SearchProvider` Null → Knowledge/Progressions-Suche |
| W2 | `object_references.py`, `item_index.py` | relationale Verweise im UI | Glide-IDs / Task-Nesting | erst nach typisiertem Objektmodell anpassen |
| W2 | `page_markdown.py`, `markdown_tree.py`, `image_preview.py`, `attachment_policy.py` | Hinweise, Tutorials, lokale Ressource/Import | alte Blocktypen/Assets | Staged Markdown Reader, Rechte/Path Traversal-Tests |
| W3 | `drawing.py`, `drawing_image.py`, `animation.py`, `pinboard_pages.py` | perspektivisch musikalisches Canvas, Sequencer/Grid, visuelle Verbindungen | Pixel-/Pinnwandfachlogik | einzelne Canvas-Widgets isolieren, Musikdaten neu modellieren |
| W3 | `timezones.py`, `calendar_service.py`, `planning.py`, `focus_timer.py` | allgemeine Zeit-/Workflowfähigkeit optional | Todo-Domäne teils hoch | nur bei konkretem Musikanwendungsfall übernehmen |
| Ausschluss v0 | `task_editing.py`, `capture_parser.py`, `today_view.py`, `day_proposal.py`, `week_planning.py`, `eisenhower.py`, `routines.py` | nur Lernbeispiel für reine Services | stark task-spezifisch | **nicht** als Musikmodell kopieren; archivierte Referenz |
| Prozess | Glide `DESIGN_RICHTLINIEN`, `ARBEITSRICHTUNG`, `AGENTS`, QA-Tests, Packaging/CI/BOM | Design- und Entscheidungsprozess | historische Stand-/OS-Unterschiede | Steps-Contracts + eigene Nachweise, kein kopiertes Grün |

## Kanonische Migrationsdaten

Jeder Reuse-Eintrag erhält: `upstream_repo`, `upstream_commit`, `upstream_path`, `file_license`, `asset_license`, `owner`, `target_path`, `adaptation_reason`, `dependency_graph`, `replaced_calls`, `new_ports`, `regression_tests`, `status` (`candidate/isolated/ported/reviewed/rejected`), `rollback_ref` und `source_hash`. Bei Code unter MPL-2.0 die betroffenen Files/Notices/Source-Verfügbarkeit ordnungsgemäß behandeln; Drittasset-Lizenzen separat.

**Import-Richtung:** `src/steps` → keine Imports aus `app`, `glide`, `tkinter`, `research`, `knowledge/sources/raw`. `app` darf Ports aus `src/steps` implementieren, `knowledge` nur kuratierte Records an Services liefern, `research` niemals im Runtime-Startup parsen. UI-Aktionen trennen **Event → Command → Domain → State → Render**. Verboten: `import glide.app as steps`, globales Umschreiben von Glide-Userfiles oder automatische Wiederverwendung der `Glide`-Bundle-ID.

## Reihenfolge der Prüfungen

1. Vorher-Nachher-UI und Liste aller Buttons/Kombinationen aus Glide dokumentieren.
2. Kandidaten nach direkt/indirekt Tk-Import, harten `Glide`-Pfaden, Globals, Theme-Variablen, Dateiformat und Lizenzen statisch klassifizieren.
3. Minimalen portablen Wrapper in eigener Datei bauen, keine großflächige `ListApp`-Operation.
4. Unit- und deterministische UI-Regressionsfälle auf Windows/Linux/Mac mit separaten Testdaten und mindestens einem Negativfall.
5. Nur isoliert getestete Bausteine in Steps-Shell aktivieren; vorherige Bridge bleibt für Rollback nachvollziehbar.
