# Glide → neutrales Systemfundament: Extraktionsplan

## Keine sofortige Gesamtextraktion

Quelle: `01_Repository/Glide/src/glide/README.md` (System 1.15, besonders Paketbezüge B01–B25, Abschnitt 9). Ältere 94-Dateien-Modulliste ist eine Bestandsaufnahme von 3.50.5; sie ersetzt das aktuelle Inventar nicht. Der zentrale `app.pyw`/`ListApp` ist groß und eng gekoppelt. 88 von 94 Dateien ohne direkten tkinter-Import bedeuten **nicht** 88 fertige Pakete. Nur gemessene, separat getestete Reuse-Kandidaten übernehmen.

## Drei Ebenen

- **A – Product Shell (potenziell teilbar):** Haupt-/Neben-Arbeitsansicht, Fensterrahmen, Split/Collapse, Sidebar-Container, Navigation/History, Kopf/Logo/Titel, Toolbar, Suchfeldhost, Dialog-/Fokusverwaltung, Themes, Schriftrollen, Einstellungen, Tastatur/Accessibility, Lifecycle, Recovery-Schnittstellen.
- **B – austauschbare Adapter:** `NavigationProvider`, `PageTreeProvider`, `ActionRegistry`, `DocumentProvider`, `SettingsStore`, `PersistencePort`, `SearchProvider`, `MediaProvider`, `NotificationPort`. Immer Steps-eigene IDs und Typen, keine Task-Objekte voraussetzen.
- **C – Produktdomäne:** Glide-Aufgaben, Heute/Planung, Pinnwände, Notizen, Pixelwerkstatt **bleiben in Glide**. Für Steps neue Musik-/Zeit-/MIDI-Domäne. Das Zwei-Fenster-Layout ist nicht automatisch ein neues Produktdatenmodell.

## Erste konkrete Kandidaten (nur nach Prüfung)

| Pakettyp | Vorhandene Glide-Module | Potenzial / Gefahr | Erste unabhängige Abnahme |
|---|---|---|---|
| Design / Tokens | `appearance.py`, `ui_design.py`, `font_catalog.py`, `brand.py`, `glyph_metrics.py`, `symbol_policy.py` | Themen-/Fontsystem sinnvoll, Branding und Tk-Metriken gekoppelt | eigene Farbtokens/Branding, Light/Dark, fehlende Glyphen, DPI, no Glide import |
| Kopf / Assets | `logo.py`, `logo_raster.py`, `svg_geometry.py`, `backdrop.py` | SVG/PNG nutzbar, Glide-Master/Marke nicht neutral | eigene Steps-Icons, Lizenz, 16–1024px, native Paketicons |
| Navigation | `sidebar_policy.py`, `side_view.py`, `compact_mode.py`, `view_definition.py`, `action_catalog.py`, `action_menu.py` | `side_view`/`view_definition` können Aufgaben-/Seitenannahmen tragen | Stable IDs, Umschalten/ausblenden/History, Tastatur, kein stilles Speichern |
| Suche/Interaktion | `content_search.py`, `interaction_policy.py`, `render_retention.py` | Textlogik eher portabel; Widget-Host und Cache-Lebensdauer kritisch | Null-Suchprovider, Cancel, Caches nach IDs, Fokus und Destroy |
| Speicherung | `save_result.py`, `persistence.py`, `data_lock.py`, `load_phases.py`, `editor_flush.py`, `undo_history.py` | starke Kandidaten für Schutzlogik; Glide-Schema nie implizit übernehmen | isolierter Steps-Datenordner, atomic save, Lock, Crash-Simulation, Undo |
| Sicherung / Dateisicherheit | `backup_snapshot.py`, `backup_catalog.py`, `attachment_paths.py`, `runtime_diagnostics.py` | generischer Vertrag möglich; projektbezogene Pfade/Restore prüfen | Traversal, zwei Schreiber, Restore bei Fehler, kein Glide-Produktivzugriff |
| QA und Build | `tests/tools`, `packaging`, `.github/workflows` | Muster nutzbar, aber starke Namens-/Plattform-/Lizenzbindung | CI in Steps neu, echte Domain-Tests, eigener SBOM und Paket-SHA |

**Nicht als Erstes extrahieren:** `app.pyw` als komplette Library; `today_view`, `task_references`, `planning`, `day_proposal`, `pinboard_pages`, `page_restore`, `drawing` etc. ohne klaren Steps-Nutzen. `app.pyw` nur unter kontrolliertem `ShellController`-Interface und Verhaltenstests schrittweise schneiden.

## Vorgeschlagene API-Verträge (Entwurf, nicht Ist-Stand)

```python
from typing import Protocol

class PaneContent(Protocol):
    def mount(self, host, context) -> None: ...
    def can_close(self) -> bool: ...
    def unmount(self) -> None: ...

class NavigationProvider(Protocol):
    def entries(self) -> tuple: ...
    def resolve(self, entry_id: str): ...

class AppContext(Protocol):
    @property
    def app_id(self) -> str: ...
    @property
    def data_dir(self): ...
    @property
    def design_tokens(self): ...
```

Ein echter Schnitt verlangt konkretere Typen, Fehlerkontrakte, `mount/unmount`-Garantien und eine Entscheidung über Root-/Toplevel-Hosts. Die Beispiel-API ist **keine vorhandene Funktion** und nicht ungeprüft zu kopieren.

## Extraktionsschritte

0. G0/G1: gesicherte 3.53.0-Releasebasis, Quellhash, vollständige Zustands-/Screenshot- und Event-Regression (Fenster, Sidebar, alle Designs).
1. Architektur-Graph: alle Imports, Methodenaufrufe, globalen Tk-Handles, Dateipfade, State Owner und ein-/ausgehenden Ereignisse des Shell-Bereichs statisch und dynamisch erfassen.
2. Ein einziges reines Modul als Spike (z. B. `compact_mode.py` oder `save_result.py`) mit neutraler Testhost-API. Kein `ListApp`-Import im unabhängigen Paket.
3. Einen UI-Host isolieren, ohne dessen Verhalten zu verändern: Haupt-/Neben-Container austauschbar, Schleusen für Suche und Aktionen.
4. Adapter nach tatsächlichem Verbraucherbedarf aufbauen. Gleiche Tests in Glide und leerer Steps-Shell laufen lassen.
5. **Erst nach zwei Konsumenten:** Versioniertes `shared-shell`/`shared-kits`-Projekt oder Repo/Package entscheiden (vendoring/lockfile/git-subtree/Package). Kein automatisches Upstream-Sync-Skript, bevor APIs und Releases stabil sind.

## Backport-Governance

Für jede Änderung: Ursprung, betroffene Pakete, Consumer-Matrix, SemVer/Datei-Policy, Changelog, Lizenzhinweise, reproduzierbare Tests, Integrations-PR pro App, Migrationsbedarf, Deprecation-Plan und Rollback. Gemeinsame Änderung ist nur dann „einfach modulweise“ einsetzbar, wenn beide Apps denselben vertraglich definierten API-Stand unterstützen.
