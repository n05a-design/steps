# Glide → Steps: konservativer Rückbau auf eine Zwei-Bereiche-Shell


> **Kritischer Aktualitätsnachtrag (10.11.2026, nach GitHub PR #75):** Der folgende Basisteil stammt aus dem früheren Paket und kann für Glide `main` noch den historischen Commit `61a2f3a`/Version 3.50.7 nennen. Der erneut verifizierte Stand ist **Glide `9e767bea` (3.53.0)**; der hochgeladene `app.pyw` ist blobgleich mit diesem HEAD, nicht aber bereits alle weiteren Module und Ressourcen unabhängig verifiziert. Aktuelle Bewertungen und Entscheidungsgates stehen in [`docs/project/PROJECT_OVERVIEW.md`](../../docs/project/PROJECT_OVERVIEW.md) und [`docs/audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md`](../../docs/audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md). Aussagen im folgenden Basisteil bleiben als **historisch datierte Ausgangsnotizen** erhalten, keine unmarkierte aktuelle Wahrheit.

**Stand:** 10.11.2026 (Europe/Berlin). **Status:** Entwurf und Prüfauftrag, keine Umsetzung/Freigabe. **Referenzstände:** Steps `main` `75329fef46878a5ac816cef3690e612a9e8fe52c`; Glide `main` `61a2f3ac2f0e1880e7fd8c0f3cfd9da0d0c9f16d`; lokal bereitgestellter Glide-Code `3.53.0`, SHA-256 `d7e19151eb0862a8ff58c4cc5e7d06a0452cde1daa73830ff97f54247bc75271`.

**Evidenz:** `UPLOAD` = bereitgestellte Datei, `GITHUB` = gelesener Remote-Stand, `BERICHTET` = in Unterlagen behauptet, `VORSCHLAG` = neue Empfehlung, `OFFEN` = unbestätigt. Kein dokumentierter Test bedeutet nicht bestanden.

## Ziel und Nicht-Ziele

**Zielzustand S0:** eine startende Steps-Desktop-Shell mit zwei persistenten Hauptbereichen **A – Seitenleiste/Navigation** und **B – neutraler Arbeitsbereich**. Es gibt weiter das Anwendungshauptfenster, Rahmen, Titelzeile, Logo-/Icontechnik, Menüs, Systemeinstellungen und vorhandene cross-cutting Infrastruktur. Die Navigationsliste besteht aus einfachen (optionalen zusammenklappbaren) Punkten mit Label und Status „geplant“; noch **keine** Todo-Aktionen oder vorgetäuschten Musikfunktionen. Klicks sind entweder explizit deaktiviert oder zeigen einen klar beschrifteten, sicheren leeren Workspace; kein stilles Aufrufen des Glide-Editors. Das ist eine UI-Arbeitshypothese. Falls zwei separate Tk-Fenster beabsichtigt sind, muss ein eigener ADR die Wurzel-/Toplevel-/Fokus-/Modalitätsprobleme definieren, bevor das umgesetzt wird.

**Nicht-Ziele S0:** produktive Akkord-/Drum-Engine, alte Task-Daten nach Steps migrieren, alte Aufgabenlisten umbenennen und als Progression speichern, eigenständige GUI-Framework-Rewrite, Entfernen von QA/CI/Dialogs/Undo- oder Storage-Infrastruktur, massenhafte Modul-/Dateilöschung, Font-/Bildübernahme ohne Lizenzfreigabe, OS-Identitätskonstanten von Glide in Steps übernehmen.

## 1. Inventar und Backup vor erstem Code-Schnitt

- Bestehenden **lokalen** Glide-Arbeitsbaum (3.53.0, mehrere Module) inkl. Hashliste, Font-/Logo-/SVG-Mastern und Dialog-, Test- und Design-Unterlagen sichern. Der Einzelupload `Glide-Aufgaben-und-Listen_v3.53.0.pyw` ist nicht das gesamte System.
- Native QA zum Baseline-Commit durchführen. `git status`, clean branch, `git diff`, `git rev-parse HEAD`, `GLIDE_SYSTEM_VERSION`, `VERSION`, `pyproject`, `requirements`, `AGENTS`, `DESIGN_RICHTLINIEN`, Quellen-/Dateizählungen. Nutzerdateien stets unter isoliertem Datenverzeichnis; Glide testweise nur mit `GLIDE_DATA_DIR` in temporärem Verzeichnis starten.
- Startbilder bei üblichen Breiten (schmal, mittel, breit), Light/Dark/System, Kompaktmodus, Schriften (Rubik, DM Mono, DM Serif Display, Charis SIL **im lokalen 3.53**), Sidebar offen/schmal/ausgeblendet. Die Remote-3.50.7-Fontpalette ist älter. DPI und OS dokumentieren.
- Alle UI-Aktionen und Verantwortungsstellen (Widget/Callback/Modul/View/Storage) protokollieren. Noch nichts löschen.

## 2. Sichtbare Shell – Erhaltungsvertrag

| Bereich | Unbedingt erhalten | Nur neutralisieren/an Steps koppeln | Nicht ungeprüft übernehmen |
|---|---|---|---|
| App-Lifecycle | Tk/Tcl-Start, Hauptfenster, Fehlercallback, geordnetes Shutdown, Session-Management | neue Steps-IDs/Pfade/Version/Logs | Glide App Bundle ID, `GLIDE_DATA_DIR`, globale Monkey-Patches ohne Audit |
| Linke Leiste | Breite, Layout, Header, Listenelemente, Scrollbars, Collapse/Hide/Narrow, Fokus/Tastatur, Hover, Theme/Zählervorschau | `SidebarItem` mit stabiler ID/Label ohne Domain-Aktion | Todo-Namen/Zähler/Mutationen als Schritte-Fachobjekte |
| Rechte Fläche | Titel/Unterzeile, Cards, leeres Editorfeld, platzhaltende Layout-/Scrollcontainer, Resizing | `WorkspaceHost` mit no-op view, später Progression-Editor | Todo-Kacheln, „Heute“-Dashboard-Queries |
| Kopf/Menu | Logo-/Markenerzeugung, Typografie, Toolsymbolknöpfe, Menü/Tooltip/Shortcuts, Fokus | Steps-Logo/-Name/-Produkt-ID und konkrete Aktionen später | Glide-Logo oder Windows AppUserModelId einfach kopieren |
| Suche/Eingabe | Widget, Placeholder, Clear-Icon, Esc, Tastatur und Fokustests | explizit leerer Such-Provider (`NO_INDEX`) + „noch nicht verfügbar“ | Index in Glide-Tasks durchsuchen |
| Einstellungen | dialog management, persistente Theme-/Font-/Sidebar-Größe, Dark/Light/System, Ausrichtungs-/Kontrastregeln | eigenes Steps-Settings-Schema und neue App-Paths | Einstellungen/Cache der bestehenden Glide-Nutzer ändern |
| Prozesse | Callback-/Timer-Abbau, asynchrone Generation Guards, Exception-Protokoll, sicheres Save/Load, Tests/Packaging | Schritt für Schritt neue Ports/Adapter | Hintergrundservices, die Glide-Taskdaten voraussetzen |
| Grafiken | SVG-Rasterung, Symbolabdeckung und Fallback, Fontmanager, optische Glyph-Zentrierung | neue eigene Markenassets & Rechtsprüfung | proprietäre/fragliche Fonts oder fremde Inspirationsgrafiken |
| Entscheidungen | Designregeln, ADR-Vorlagen, Quelle/BOM, Checklists | Steps-spezifisch portieren, Glossar und Token bei Bedarf | alte Glide-Produktgrenzen als Steps-Produktbeschluss |

**Besonders kritisch:** Nicht bloß `pack_forget` oder `destroy()` auf beliebige Widgets anwenden; zuerst sämtliche Referenzen/`after`-Callbacks/Bindings/Save-Observer/Toolbar-Hosts anschauen, da `ListApp` 1.866 Methoden umfasst. Nicht getarnte Arbeit im unsichtbaren Todo-Dashboard weiterlaufen lassen.

## 3. Konkrete lokale Codeanker (AST aus Upload; Zeilen sind nur Snapshot-Hinweise)

- `ListApp` ab ca. Zeile **15.533**; nur anhand **Funktionsnamen** und Aufrufgraph ändern.
- Seitenleiste: `create_list_sidebar` ~37.695; `sidebar_section_open` ~26.342; `toggle_sidebar_section` ~26.358; `create_drawings_sidebar` ~38.498; `toggle_sidebar_narrow` ~66.255; `toggle_sidebar` ~66.327.
- Kompaktmodus: `compact_mode_active` ~66.347; `enter_compact_mode` ~66.379; `leave_compact_mode` ~66.418; `remember_compact_geometry` ~66.452.
- Header: `sync_header_action_host` ~43.761; `pack_header_controls` ~43.842; `update_header_title` ~44.254; `sync_header_logo` ~53.593.
- Suche/Workspace: `set_search_placeholder` ~49.373; `clear_search` ~49.636; `focus_search` ~49.644; `sync_overview_search` ~27.655; `show_settings_dialog` ~31.172.
- Fenster/Prozesse: `save_window_geometry` ~45.312; `defer_window_menu_commands` ~47; `get_app_data_dir` ~387 (Glide-basiert und neu zu isolieren).
- Greifbare generische Widgetklassen: `RoundedButton`, `RoundedContainer`, `ThemedAutoScrollbar`, `ResponsiveColumns`, `ButtonFlow`, `AppOptionMenu`, `CanvasLabel`. Diese sind auf Klassenniveau Kandidaten – **nicht** automatisch getrennt importierbar.

## 4. Reversibler Schrittplan

### R0 – Kopie und technische Inventur

Separater Steps-Feature-Branch auf dem aktuellen Steps-`main`. Glide bleibt **unverändert**. Port-Schnittstellen identifizieren: `ThemeService`, `WindowState`, `SidebarState`, `NavigationRegistry`, `WorkspaceHost`, `PreferencesStore`, `ResourceLoader`, `ActionRegistry`, `SearchProvider`, `Logger/Diagnostics`. Für jeden Baustein Herkunftscommit, Lizenz, API und Dependencies erfassen. Der frühere Rückbau darf als **Plan/Diff-Preview** erscheinen, nicht als unbeobachtetes automatisches Skript.

### R1 – neutrale Shell und Markenidentität

Steps-eigene Tk-Root/Entry-Point-/Pfad-/Lock-Identität; zwei Bereichscontainer aufbauen, konstante Navigator-Daten als reine IDs/Labels. Headbar-Token und Logo-Raster-Mechanik nur mit **eigenem Steps-Logo** nutzen. Alle Todo-Services abkoppeln; anfänglich keine echte Datei-/Modellkonvertierung. Start/Exit und Theme-Umschaltung sichern.

### R2 – Navigation ohne Produktfunktion

Statische Punkte können erhaltene Namen als **Platzhalter** anzeigen oder vorläufig musikneutrale IDs verwenden. Stabiler Navigationseintrag-Vertrag: `{id,label,icon_role,group,enabled:false,route:null}`. Kein `command`-Callback auf Glide-Aktionen. Klick entweder ohne Wirkung + Erklärung oder öffnet einen einzigen klar markierten `ComingSoonView`; keine versprochene Funktion. Sidebareinzug, Abschnitts-Klappen, gesamte Leiste ausblenden/einblenden, Kompaktmodus, Scroll-/Fokus-Restore und Zustands-Persistenz **sind funktional**. Das sind Shell-Fähigkeiten und kein Widerspruch zur deaktivierten Seitenliste.

### R3 – rechte Arbeitsfläche und Eingaben

Neutrale Titelleiste, Unterzeile, Toolbar-Stil und leere Arbeitsfläche. Globales Suchfeld bleibt sichtbar und bedienbar (Fokus, Text, `Esc`, Clear), aber Trefferpipeline ist ein **NullSearchProvider**; Ergebnisse klar „Noch nicht verbunden“. Die Settings-/Font-/Theme-/Designsteuerung arbeitet an Steps-Settings im neuen App-Verzeichnis; keine Glide-Benutzerdatei lesen. Schrittweise austauschbare `WorkspaceView`-Schnittstelle definieren.

### R4 – technische Ports und Tests

Smoke: `python`-Start/Exit, 2 Hauptbereiche, Mode/Resize, unterbrochene Animation, `after_idle`-Menüs auf macOS, Root-Abbau, Fonts, Symbolabdeckung/ASCII-Fallback, Session Locks/SaveResult/atomic write mit eigenen Schemas. Alt-Glide-Tests als Referenz, **nicht** grün auf Steps ohne tatsächlichen Testlauf. Alle zusätzlichen Prozesse werden bei Schließen beendet.

### R5 – Musikmodule nur nach neuem Domänenvertrag

Ein `ProgressionDocument` ohne Glide-Aufgaben-IDs, neue Storage-Transaktion, Chord-/Note-Spelling-Modelle und Kontextanalysen. RouteRegistry kann erste Sidebar-Items erst nach Modul-Tests aktivieren. `Undo/Redo`-Muster nur nach transaktionaler Isolierung. Audio/MIDI und Drums nicht von Anfang an in der Shell erzwingen.

## 5. Definition of Done S0

- [ ] Steps startet mit **einem** Hauptfenster und **zwei sichtbaren Primärflächen**; eine alternative Zwei-Toplevel-Architektur ist nicht stillschweigend implementiert.
- [ ] Menüs, Icons, Fonts, Settings-Dialog, Light/Dark/System, Toolbar, Suchfeld, Scrolling, Sidebar-/Kompaktsteuerung demonstriert.
- [ ] Alle Sidebar-Einträge mit deterministischem No-op bzw. expliziter Placeholder-View; **keine** Todo-Fachdaten laden/mutieren.
- [ ] Steps-Datenpfad, Lock, Cache, Bundle-ID und Backups vollständig getrennt von Glide.
- [ ] Tests auf dem konkreten Commit, mindestens Windows native UI und automatisierte Linux-Prüfung; macOS bei Freigabe vor Release plus menschliche Sichtprüfung (kleine Breite, DPI, Fokus).
- [ ] `SOURCE_MAP`, `LICENSE_MAP`, `FILES_CHANGED`, `COMPATIBILITY_REPORT`, `SIDEBAR_ACTION_AUDIT` und Vorher-/Nachher-Bilder vorhanden; keine altbetroffenen Ressourcen/Quellen verloren.
- [ ] Keine inaktiven Timer/Callback-Tcl-Fehler, keine importierten Glide-Nutzerdaten, kein versehentliches Schreiben in Glide-Verzeichnis.

**Erst danach** wird der Music-Workspace in die leere rechte Fläche eingeführt.
