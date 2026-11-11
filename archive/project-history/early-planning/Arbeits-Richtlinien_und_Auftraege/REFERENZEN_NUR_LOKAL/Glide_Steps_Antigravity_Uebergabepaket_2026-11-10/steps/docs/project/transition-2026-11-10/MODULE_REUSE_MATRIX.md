# Glide-Reuse-Matrix für Steps – Kandidaten, kein freigegebenes SDK

**Autorität:** Glide `01_Repository/Glide/src/glide/README.md` System 1.15, §9; ergänzende historische Bestandsinventur 3.50.5 mit 94 Dateien. Die Auswahl folgt konkretem Steps-Bedarf, nicht der Anzahl entkoppelter Importe.

| Gruppe | Module | Steps-Anwendung | Strategie | Risikograd |
|---|---|---|---|---|
| Theme/Tokens | `appearance.py`, `ui_design.py`, `font_catalog.py`, `backdrop.py` | Themen, Typografie, Layout | adaptieren, Marken/Fonts und Host trennen | mittel |
| Branding/Assets | `logo.py`, `logo_raster.py`, `svg_geometry.py`, `brand.py`, `glyph_metrics.py`, `symbol_policy.py` | Head/Logo/Icons | Reuse von Algorithmen; Steps-Master neu | hoch (Assets/Tk) |
| Fenstermodus | `compact_mode.py` | Geometrie, Nebenansicht | reiner Service als erster Spike | niedrig–mittel |
| Sidebar/Navigation | `sidebar_policy.py`, `side_view.py`, `view_definition.py`, `action_catalog.py`, `action_menu.py`, `interaction_policy.py` | Navigation und Command-Host | getrennte Provider/ActionPorts | hoch |
| Rendering | `render_retention.py`, `motion.py`, `load_phases.py` | Lebensdauer/Caches/Übergänge | gezielt, mit Negativtests | mittel–hoch |
| Suche/Knowledge | `content_search.py` | Suche im Wissensbestand | nur normalisierte, fachneutrale Textfunktionen; keine Task-Indizes | mittel |
| Daten-/Fehlerschutz | `save_result.py`, `persistence.py`, `data_lock.py`, `session_guard.py`, `storage_health.py`, `editor_flush.py`, `undo_history.py` | Projekt speichern, Locks, Undo | Port/Adapter mit Steps-eigenem Save-Schema | hoch |
| Backups/Assets | `backup_snapshot.py`, `backup_catalog.py`, `attachment_paths.py`, `restore_assets.py` | Sicherungen und referenzierte Medien | explizite Datei-/Path-Grenzen | hoch |
| QA/Build | `tests/tools`, `packaging`, `.github/workflows` | verifizierter Build, Paketierung | Muster nutzen, Scripts nicht unverändert kopieren | hoch |
| Task-spezifisch | `today_view.py`, `planning.py`, `task_references.py`, `day_proposal.py`, `page_restore.py`, `pinboard_pages.py` | normalerweise kein Steps-Bedarf | **nicht übernehmen** | hoch/geringer Nutzen |
| Pixel-/Mediendaten | `drawing.py`, `drawing_image.py` | evtl. später eigenes Grid/Notation | zunächst nicht, später Bedarf und Datenformat prüfen | mittel–hoch |

**Erst-Piloten:** `compact_mode.py` (reiner Fensterregel-Spike) plus ein explizit begrenzter Navigation-/Pane-Testhost. Alternativ `save_result.py` für ein reines Fehlerergebnisobjekt; keine parallele Extraktion aller Gruppen. Status für jede Einzelprüfung: `candidate / needs_adapter / accepted / rejected / not_tested`; selbst „accepted“ nur bei dokumentiertem zwei-seitigem Contract-Test.

**Aktualisierungsmodell:** Produktneutraler Code kann später eine eigene Version erhalten. Glide- und Steps-Versionen bleiben unabhängig. Vor Backport in beide Verbraucher: API-Diff, Migration, Lizenz, Regression, Cross-OS, Staging und Changelog; Änderungen nicht automatisch durch Git-Synchronisation verteilen.
