# Technische Hauptspezifikation: Glide 3.53.0 → Steps Desktop-Shell

**Vertrag:** Die Steps-Shell ist ein **neues Produkt**, kein Glide mit geändertem Titel. Dieses Dokument beschreibt mögliche Umsetzung und Prüfungen, **noch keine genehmigte Codeänderung**. Ausgangscommit `n05a-design/glide-to-do@9e767bea5e21063466a28ac3a679406484ad5d5f`; lokaler Einzelcode bytegleich zum dortigen `src/glide/app.pyw` (`Git blob 0fc522fb...`). Gesamtsystemstand: 94 Python-Quellmodule/25 Paketkandidaten/147 Features laut Systemregister V1.15. Aktuelle 3.53.0-QA und D77-Designregeln zuerst lesen.

## 1. Die Erhaltungsabsicht richtig interpretieren

Der Wunsch „nur zwei Fenster, Seitenliste ohne Funktionen, alles andere soll bestehen bleiben“ ist intern widersprüchlich, wenn „alles“ alle Glide-Fachaktionen meint. Die tragfähige Arbeitsinterpretation ist eine **fähigkeitsbezogene Erhaltung**:

| Bereich / Fähigkeit | Beibehalten in S0 | Neu für Steps | Nicht von Glide mitnehmen |
|---|---|---|---|
| Fenster und Chome | äußere Form, Menüs, Status, Titel, Logo-Renderer, OS-Fensterbuttons, Kompaktmodus | eigene App-ID, Titel, aktiver Steps-Kontext | Glide-Namen, Pfade, AppUserModel-ID |
| Sidebar | Breite, Ein-/Ausklappen, Scroll-/Fokus-/Hoverzustände, Tastaturzugang, Section-Lifecycle, persistierte UI-Einstellungen | neutrale `NavigationItem`-IDs, RouteRegistry, Platzhalter-Gruppen | Glide-Aufgabenlabels, Todo-Aktionen, Mutation/DB-Bindungen |
| Header | Titel/Unterzeile, Aktions-Symbole, Tooltip-/Theme-Rollen, `D68`-farbige Ansicht | Steps-Ansichtsmetadaten; nur explizit funktionierende Controls | Fake-„Heute“-Zähler, erfundene Tasks |
| Suche | Eingabefeld, Clear/Esc, Fokus, Größenverhalten, Platzhalter, Menüzugriff | bewusst leere Suche mit Erklärung oder Demo-Index | Suche in Glide-Speicher, Alt-Notizen oder Fremddaten |
| Arbeitsfläche | Pane-/Card-/Editor-Grundbausteine, Scroll, Selektion, leere States, Field-Metriken | musikbezogener Platzhalter und später Chord Editor | Glide-Seiten-Aufgaben-Rendering, Task-Formulare |
| Settings | Theme, Font-Familie, Gewicht, Größe, Fensterzustand, UI-Hinweise, ggf. Animation | eigene versionierte Steps-Settings und saubere Defaults | Planungs-, Label-, Routine-, Notion-/ICS-/Todo-Konfiguration |
| Design | Tokens, Theme/Farben, 4 Stile, interner Glyphfallback, Kontrast, Gradient/Buttons | Steps-Brand-, Asset-/Logo-Wahl und Freigabe | vorhandenes Glide-Markenzeichen als fertiges Steps-Logo |
| Sicherheit | Crash-/Callback-Protokoll, atomare IO-, Backup-, Lock- und Speicherphasen-Konzepte | neutrale Ports, neue Projektdatei, Permission-/Error-Gates | `liste_speicher.json`/Glide-Dateisperre im Steps-Prozess |
| Tools/QA | Testsuiten als Referenz, Buildverfahren, statische UI-Designregeln | Steps-eigene Tests, Version, Lizenz-BOM, OS-Matrix | Glide-Version/Tests als Steps-Erfolg deklarieren |
| Specials | mögliche Pixel-/Pinboard-/Notiz-/Galerie-Routinen archiviert | optionale spätere Musikanwendungsfälle, falls spezifiziert | bloße Mitnahme aller Features in v0.1 |

**Markierung in der UI:** Es gibt drei bewusst unterscheidbare Zustände: `enabled` (Aktion mit Test), `disabled_planned` (sichtbarer Eintrag ohne Funktion, Tooltip/Tastaturmeldung „in Vorbereitung“) und `hidden` (nur nach Designentscheidung/Featureflag). „Funktionslos“ bedeutet *keine Datenmutation, keinen Alt-Routeraufruf, keine versteckte Hotkey-Aktion*, nicht einen Klick, der stillschweigend `return` ausführt und die Bedienperson verwirrt.

## 2. Reale statische Risiken in `app.pyw`

| Identifizierter Quellanker im Upload | Risiko für Steps | technische Bedingung |
|---|---|---|
| `defer_window_menu_commands()` wird auf Modulebene aufgerufen | globales Patchen von `tk.Menu.add_command` und `insert_command`; weiteres Tk-Verhalten pro Prozess beeinflusst | explizite kapselbare Menü-Factory, install-once, Test pro Tcl-Interpreter und OS |
| `_ensure_streams()` wird auf Modulebene aufgerufen | verändert `sys.stdout`/`sys.stderr` falls `pythonw` | eigene Logging-/Callback-Fehlerbehandlung ohne unerwartete Prozessglobaländerung |
| `BASE_DIR = get_app_data_dir()` auf Modulebene | kann beim Import echte Glide-Verzeichnisse anlegen und Data-Pointer lesen | **niemals** das Monolith-Modul nur zur Wiederverwendung importieren; Root erst nach Steps-Konfiguration bauen |
| `BACKUP_DIR`, `ATTACHMENTS_DIR`, Lock, Settings- und Save-Pfade global | mögliche Daten-/Sitzungskollision, unbeabsichtigter Datenzugriff | `StepsPaths` per expliziter Constructor-Injektion und isoliertem Temp-Testroot |
| `APP_BUNDLE_ID = de.shaye.glide` und `APP_USER_MODEL_ID = Shaye.Glide` | OS-Taskbar-/Notification-/Cache-Kollision | neue produktabhängige, fest beschlossene Identität |
| `_APP_FONT_CACHE` und `_ICON_FAMILY` global | Theme-/Tk-Interpreter-Lebensdauer und Fallback-Zustände | widget-/interpreterbezogene Cache-Invalidierung, Tests für Fontwechsel |
| `ListApp` ruft Hunderte Methoden und Delegates auf | ungezieltes Entfernen einer Navigation kann Save/Focus/Undo/Refresh beschädigen | Aktionsregistrierung statt direkte Mutation; kontraktfähige Ports |

**Direkte Messung:** `app.pyw` umfasst ca. 69.015 Zeilen, 39 top-level Klassen und 1.866 direkte `ListApp`-Methoden; die Analyse hat Methoden und direkte `self.method()`-Aufrufe unter `manifests/GLIDE_LISTAPP_METHOD_CALLS_V2.csv` abgelegt. Diese AST-Tabelle zeigt **syntaktische** Aufrufe, keine dynamische Erreichbarkeit, keine Callbacks aus `lambda`, `after`, Tk-`command`, Bindings und importierten Modulen vollständig aufgelöst. Daher ist sie *Startpunkt für Review*, nicht automatischer Beweis der Unabhängigkeit.

## 3. Konkrete Codeanker aus dem aktuellen 3.53.0-Upload

- `ListApp.__init__` um Zeile **17507**: Startzustand, Widgets, Bindings, Daten-/Settings-Lifecycle gemeinsam; nicht als vollständig neutrales Initialisierungsschema kopieren.
- `create_list_sidebar` um **37695**, `create_pages_sidebar` um **38472**, `build_sidebar_section` um **38579**: Layout und Fachdatensichten trennen.
- `set_sidebar_section_open` um **26347**, `apply_sidebar_sections` um **26361**: vorhandene Klappverträge/Theme nicht verlieren.
- `render_pinned_sidebar` um **26591** und `toggle_pinned_sidebar` um **26666**: klarstellen, ob „angepinnt“ im Steps-S0 überhaupt semantisch sinnvoll ist.
- `show_settings_dialog` um **31172**, `load_settings` um **19827**, `save_settings` um **19879**, `apply_theme` um **44312**: Style- und app-spezifische Einstellungen trennen.
- `set_search_placeholder` um **49373**, `submit_overview_search` um **27699**, `focus_search` um **49644**: Suche als UI-Port ohne Altbestand.
- `build_compact_header` um **66464**, `toggle_compact_mode` um **66374**, `enter_compact_mode` um **66379**, `leave_compact_mode` um **66418**: echtes Fokus-/Geometrieverhalten erhalten.
- `load_items` um **47150**, `save_items` um **47553**: **keine** direkte Übernahme – diese verfolgen Glides Task-Daten, nicht Steps-Projekte.
- `build_side_view_shell` um **24249**, `build_detail_pane_shell` um **24840**: zusätzliche Panel-Logik untersuchen; diese darf nicht fälschlich als Wunsch nach zwei OS-Fenstern interpretiert werden.

Die vollständige maschinenlesbare Ankerliste steht in `manifests/GLIDE_SHELL_ANCHORS_V2.csv`. **Zeilennummern gelten nur für die bytegleich geprüfte 3.53.0-Datei.** Keine Code-Suchfunktion allein anhand früherer 3.50.x-Zeilennummern bauen.

## 4. Zielverträge als implementierbare Ports

```text
StepsDesktopApp
 ├─ PlatformIdentity      app-id, bundle-id, data/cache/log paths
 ├─ ThemeService          tokens, fonts, weights, accessibility
 ├─ ShellController       navigation state, workspace state, event router
 │   ├─ SidebarView        one of expanded / compact / hidden; scroll, focus
 │   ├─ HeaderView         title, subtitle, symbol/tool actions
 │   ├─ WorkspaceView      empty / progressions / settings / dialogs
 │   └─ CommandRegistry    stable action ID -> enabled/disabled handler
 ├─ SettingsStore         explicit Steps schema, independent of projects
 ├─ ProjectStore          later versioned Steps projects and recovery
 ├─ BackgroundJobQueue    read-only results -> UI-mainthread marshaling
 └─ CrashReporter         minimal logs, no user PDFs/notes by default
```

**Proposed pseudo-contracts (keine bestehenden APIs):**

```python
@dataclass(frozen=True)
class NavigationItem:
    id: str
    label: str
    icon_id: str | None
    route_id: str | None
    state: Literal['enabled', 'disabled_planned', 'hidden']
    children: tuple['NavigationItem', ...] = ()

@dataclass(frozen=True)
class ShellState:
    sidebar_mode: Literal['expanded', 'compact', 'hidden']
    selected_route: str
    theme_id: str
    font_style: str
    font_weight: str

class CommandRegistry(Protocol):
    def resolve(self, action_id: str) -> ActionSpec: ...
    def execute(self, action_id: str, context: ActionContext) -> ActionOutcome: ...
```

*Das Beispiel ist ein Entwurf und nicht als produktiver Code zu kopieren, ohne Klassen, Python-Version, Typgrenzen, Serialisierung und Fehlerverhalten zu definieren.* Für eine `disabled_planned`-Aktion gilt `ActionOutcome(type='not_available')` und **zero side effects**. Jede reale Änderung erzeugt einen testbaren `ActionOutcome` inklusive Failure/Undo-Semantik. Widget-Callbacks bekommen IDs statt lebende, veraltende Domainobjekte; die Projektion wird nach einem Commit frisch aufgelöst. Die visuelle Seite darf nicht selbst speichern oder Hintergrundaufträge starten.

## 5. Stufenweiser, verlustfreier Realisierungsplan

**G0 – Prüfung ohne Codeänderung.** Vollständige `git status`, `git ls-files`, SHA-Manifest, Paket-/Resource-Hash, Liefer-/QA-Bericht und Lizenzprovenienz sichern. Auf Produkt-UI-Seite 1280×800, 860×700, Dark/Light, vier Schriftstile und Fokus-/Kompaktvarianten dokumentieren. Beispieldaten **synthetisch**; jeder Testpfad außerhalb echter Nutzerdaten.

**G1 – Screenshot-/Aktionsvertrag.** Bedienoberfläche mit Rollen statt Glide-Labels spezifizieren: `NavItem`, Header, Search, Toolbar, Settings, Workspace, Dialog; für jedes Widget `source_module`, `state_owner`, `callback`, `dependencies`, `action_type`, `persistence`, `test`. Aktions-IDs bekommen neue Steps-Namespaces. Alle Hover-, Focus- und Menüzugänge auch in eingeklappter Sidebar auflisten.

**G2 – Zwei Spikes.** Kleine, unabhängig startbare Versionen B und D aus `03_ALTERNATIVEN...`; kein Import des alten `app.pyw`, der beim Import Glide-Datenpfade erzeugt. Wenn ein kontrollierter Fork-Spike nötig ist, nur in gesondertem Temp-UserData-Root und neuer App-ID mit OS-Test.

**G3 – Isolierte Steps-Shell.** Neutrale Settings-/Theme-/Font-/Menu-/Command-/AppPaths-Module, UI-Shell ohne Aufgaben-/Kalender-/Pinnwanddaten; Titel und Logo werden *neu* parametriert. Keine Quellcode-„Delete bis grün“ Methode. Alle existierenden Komponenten werden anhand des 94-Modulregisters selektiv übernommen und mit Datei-/Lizenzhinweis dokumentiert.

**G4 – Navigator als neu verdrahtete Oberfläche.** Eine `NavigationRegistry` hält sichtbare Punkte und stable IDs. Ein Klick auf disabled Seiten ändert nicht den persistenten Datensatz; Navigation, Fokus und Sidebar-Klappen bleiben funktional. Hotkeys und Kontextmenüs dürfen keine versteckten Glide-Commands auslösen. Die globalen Menüs müssen auf tatsächlich verfügbare Steps-Kommandos verweisen.

**G5 – Domain-Schnitt im Workspace.** Ein einfacher Testbereich ruft eine vollständig Tk-freie Chord-Transposition auf. Diese liefert eine neue ViewModel-Instanz; danach kann der UI-Text aktualisiert werden. Kein Speichern bis der Projektformatvertrag freigegeben ist. Fokus-/Cancellation-/Undo-Verhalten durch eigene Tests belegen.

**G6 – Schutz und Abnahme.** Steps-App startet mit frischem Settings-Verzeichnis, definierten Fonts/Theme, externem Test-Root und kann schließen, ohne Datei in Glide-UserData zu öffnen/anzulegen. Zwei UI-Spikes auf identischem Testrechner vergleichen; sichtbare Parität dokumentieren; nur dann ADR akzeptieren und Steps-Produktarbeit auf diese Shell aufbauen.

## 6. No-op-Seitenleiste: Nebenwirkungen, die sonst leicht übersehen werden

| Aktion | Erwartung bei noch nicht implementierter Steps-Route | Negativer Test |
|---|---|---|
| Einfachklick | bleibt im aktuellen Workspace oder zeigt klaren Platzhalter; kein Glide-Fachdatenzugriff | Speicher-/Lock-/Backup-/Undo-Dateien bleiben unverändert |
| Doppelklick/Enter/Space | gleichbedeutend mit Einfachklick | keine automatische neue Todo-Seite |
| Rechtsklick/Shift+F10 | optional Info-Menü ohne alte Delete/Edit/Cut/Share-Aktionen | Kontextmenü kennt keine Glide-Routenkapazitäten |
| Drag-and-drop | kein Objektverschieben, keine Bindings an ItemWorkspace | unverändertes Navigationsmodell |
| Schnelleingabe | Eingabefeld bleibt, aber App-Zweck/Status ist erklärt | keine Task-Schnelleingabe im Hintergrund |
| Collapse/Expand | vorhandene Animation/Geometrie/Symbole erhalten | jede Einstellung bleibt nach Neustart erhalten |
| Hidden Sidebar / Kompakt | Fokus, Tab-Reihenfolge, Shortcut zum Wiederöffnen | Navigation ist nicht unerreichbar |
| Globale Suche | keine Suchabfrage in Glide-Daten; ohne Index: sinnvolle Leerantwort | keine alten Treffer, keine ungewollte Netzanforderung |
| Shortcut/Palette | sichtbare, auditable `CommandRegistry`-Antwort | alte `action_catalog`-IDs lösen keine Mutation aus |
| Settings | visuelle Einstellungen dauerhaft, Fachfelder gefiltert | eigene Steps-Datenpfade und Defaults |
| Window close / crash | ausstehende UI-Tasks werden abgebrochen und keine alten Daten gespeichert | Tk-Callbacks nach Root-Zerstörung werden nicht ausgeführt |
| Home/Kacheln | Platzhalter oder ausdrücklich neue Musik-Home-Funktion | keine „Heute 0/5“, Task-Kennzahlen, Abhakaktionen |

**Testprinzip:** Für jede No-op-Variante vorher und nachher SHA/Directory-Listing der isolierten Datenwurzeln, plus Fake-Command-Recorder. 100% beobachtete Aktionspfade dürfen keine verbotenen Writes auslösen. GUI-Regressionen müssen weiterhin manuell auf Windows, macOS, Linux geprüft werden.

## 7. Design- und OS-Vertrag

Der neue Glide-Stand D77 führt Modern=Rubik, Technisch=DM Mono, Kreativ=DM Serif Display und Klassisch=Charis SIL. Gewicht ist getrennt von Größe; automatisch kreative/klassische Schriften kräftiger. DejaVu Sans bleibt interner Symbolbegleiter wegen fehlender Glyphen. **Fontdateien werden nicht Bestandteil dieses Audit-ZIPs.** Vor Lieferung in Steps Fontlizenz und tatsächliche Ressourcenbytes prüfen; die Wahl des neuen Steps-Branding erfolgt gesondert.

Aus den Glide-Designrichtlinien müssen als testbare *Entwurfsverträge* übernommen bzw. bewusst ersetzt werden: keine sichtbaren altstilartigen nativen Tk-Widgets; schlüssige Kopf-Fluchten; Titel nur einmal; Themenfarbe für aktive Ansicht; Toolbar als Leistenknöpfe; klare Ruhe-/Hover-/Focuszustände; adaptive Grenzen/Restzähler; Contrast mindestens 4.5:1 für normalen Text; reduzierte Bewegung; keine dauerhaften doppelten Hinweise; Größenmatrix 1280 und 860, DPI, Themes, macOS/Aqua-Menü-Retrigger und FocusOut. Eine direkte 1:1-Übernahme aller früheren Pixelwerte ist keine Voraussetzung, **wohl aber die explizite Entscheidung über Abweichungen**. Quelle: `01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md` bei `9e767bea`.

## 8. 30 konkrete Shell-Abnahmeszenarien

`S01` leere Steps-App startet ohne Glide-Datenkontakt; `S02` Window close cancel; `S03` zweimaliger Neustart mit Settings; `S04` System-Themewechsel; `S05` Light; `S06` Dark; `S07` Akzentfarbe; `S08` Font Stil Rubik; `S09` DM Mono; `S10` DM Serif Display; `S11` Charis SIL; `S12` Schriftgewicht; `S13` hohe DPI; `S14` 860×700; `S15` 1280×800; `S16` Sidebar expanded; `S17` Sidebar compact; `S18` Sidebar hidden; `S19` Fokus für Wiederöffnung; `S20` Escape/Clear im Suchfeld; `S21` globaler Shortcut; `S22` deaktivierter Sidebar-Klick; `S23` deaktivierter Enter; `S24` deaktivierter Rechtsklick; `S25` deaktivierter Drag; `S26` deaktivierte Command-Palette; `S27` Dialog außerhalb Bildschirm; `S28` native Menü-Callback/Modalfolge; `S29` versehentliches Schreiben an Glide-Pfade verhindert; `S30` Crash-/Root-Teardown ohne hängenden Callback. Jede Prüfung erfasst OS/Python/Tk, Commit-SHA, Datenroot, Ergebnis, Screen/Trace und offene menschliche Sichtabnahme. Nicht alle Tests müssen sofort automatisierbar sein, aber die Matrix darf keine unbeantworteten Fälle als bestanden markieren.

## 9. Stopkriterien

**Sofort stoppen und Befund dokumentieren**, wenn die Steps-Test-App Glide-UserData berührt, eine nicht freigegebene Quell-/Asset-Datei einliest, ein „disabled“-Punkt alte fachliche Mutation auslöst, eine UI-Methode ablauf-/fokusabhängig unkontrollierbar wird, ein neuer Globalpatch in einem unabhängigen Prozess erscheint oder ein Teststand ohne referenzierbaren Commit und unveränderte Fixture-Blobs behauptet wird. Fehlende macOS- oder Linux-Tests sind keine „grünen“ Tests.

Weitere Anhänge: `manifests/GLIDE_94_MODULE_REUSE_AUDIT_V2.csv`, `manifests/GLIDE_25_PACKAGES_AUDIT_V2.csv`, `manifests/GLIDE_LISTAPP_METHOD_CALLS_V2.csv`, `manifests/GLIDE_IMPORT_SIDE_EFFECTS_V2.csv`, `docs/architecture/REUSE_AND_MIGRATION_MATRIX.md` (V1 – erhalten), `docs/quality/VERIFICATION_PLAN_V2.md`.
