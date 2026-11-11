# Glide Shell Framework – validierter Architekturbericht

**Prüf- und Entscheidungsgrundlage für die Auskopplung eines wiederverwendbaren Python-/Tkinter-App-Fundaments**  
**Datum:** 11. November 2026  
**Status:** Architekturkonzept *mit dokumentierten Korrekturen validiert*; **keine** Implementierungs-, QA- oder Releasefreigabe  
**Projekt:** [n05a-design/glide-to-do](https://github.com/n05a-design/glide-to-do)

## 1. Management-Zusammenfassung

Die Grundidee ist technisch sinnvoll: Glide sollte eine gemeinsame, **fachneutrale Desktop-Shell** verwenden, während Aufgaben, Listen, Projekte, Seiten, Notizen, Pinnwände, Planung und alle fachlichen Daten-/Mutationswege in Glide bleiben. Eine zweite App kann dann die Shell benutzen, ohne Glide zu importieren. Fensterverwaltung, Layout, Themes, Bedienkomponenten, allgemeine Einstellungen, Kommandoregistrierung und Lebenszyklus lassen sich zentral pflegen.

**Validierungsurteil:** **Bestanden als korrigiertes Architektur-Zielbild.** Nicht bestanden wäre dagegen die Aussage, das Framework sei bereits implementiert, isoliert getestet, plattformweit freigegeben oder unmittelbar übertragbar. Im 3.55.0-Entwicklungsbranch ist ein neues Shell-Konzept dokumentiert, aber keine unabhängig nutzbare Shell nachgewiesen.

**Priorisierte Empfehlung:** Ein *minimaler Shell-Kern* mit klaren App-Schnittstellen; erweiterte Dienste und generisches Undo/Redo zunächst außerhalb des Kernpakets lassen. Den Umbau nur **inkrementell** mit Verhaltenserhalt, synthetischen Testdaten und einem zweiten, Glide-freien Demo-Host durchführen. Kein Big-Bang-Refactoring von `ListApp` und kein sofortiges Abspalten eines neuen Repositorys.

## 2. Prüfgrundlage und Methodik

### 2.1 Explizit geprüfte Git-Stände

| Referenz | Git-Stand | Bedeutung |
|---|---|---|
| `main` | `594f4c85eb60370a44282b06fcb8017df8181d70` | Gemergter Ausgangsstand 3.54.0 (PR #76) |
| `feat/glide-3.55.0-development` | `fd979937708a664b715fdacdb5fd9f8d41fa78a4` | Aktueller Entwicklungsstand 3.55.0, **nicht** als Release freigegeben |

Beim Vergleich lag der Entwicklungsbranch **zwei Commits vor `main` und keinen dahinter**. Im Entwicklungsbranch wurde `docs/GLIDE_SHELL_FRAMEWORK_KONZEPT.md` neu hinzugefügt. Die Systemdokumentation nennt für 3.54.0 Glide-System V1.16; der Entwicklungsbranch dokumentiert Glide-System V1.17.

### 2.2 Prüfungstiefe

Lesend geprüft wurden das neue Shell-Konzept, Architektur- und Systemregister, Entwicklungsplan und QA-Bericht sowie die relevanten Module `runtime_config.py`, `compact_mode.py`, `ui_design.py`, `appearance.py`, `settings_compat.py`, `action_catalog.py`, `side_view.py` und `undo_history.py` anhand der über den GitHub-Connector verfügbaren Inhalte. Das Repository wurde **nicht** verändert.

**Einschränkung:** Die vollständige, große `app.pyw` wurde nicht erneut lückenlos als AST und Aufrufgraph analysiert. Es wurden **keine** lokalen oder nativen Laufzeit-, UI-, Integrations-, Daten- oder Performance-Tests von dieser Prüfung ausgeführt. Aussagen über bereits bestandene Tests stammen aus dem versionierten QA-Bericht, **nicht** aus eigenen Testausführungen. Eine belastbare Umbau-Aufwandsschätzung benötigt eine gesonderte Import-/Callback-/Zustandsanalyse auf dem ausgewählten Arbeitscommit.

## 3. Validierte Befunde und notwendige Korrekturen

| Kennung | Befund | Bewertung und Konsequenz |
|---|---|---|
| V01 | Das Wiederverwendungsziel ist bereits im Glide-System als B01/B03/B04/B09/B24 und weiteren Bausteinkandidaten dokumentiert. | **Bestätigt.** Dies sind Kandidaten, keine freigegebenen Bibliotheken. |
| V02 | Die zentralen Fenster-, Dialog-, Layout- und Steuerroutinen sind noch in `ListApp` integriert. | **Bestätigt durch System-/Architekturdokumentation.** Grenze für schrittweise Auslagerung; kein unkontrolliertes Umorganisieren. |
| V03 | Glides „Nebenansicht“ verwendet den eingebetteten Inspektorbereich. | **Korrektur nötig:** Dual-Pane und separates OS-Fenster (`tk.Toplevel`) sind unterschiedliche Produkteigenschaften. Das 3.55-Konzept vermischt sie stellenweise. |
| V04 | `compact_mode.py` enthält bereits reine Geometrieregeln, einschließlich Normal-/Kompakt-Mindestgrößen. | **Bestätigt.** Geeigneter Pilotbaustein; Produktvorgaben müssen bei Nutzung in anderen Apps parametrisiert werden. |
| V05 | `ui_design.py` enthält sowohl allgemeine Layout-/Typografie-Regeln als auch aufgaben-/ansichtsspezifische Hilfen (`task_title`, `today_columns`). | **Bestätigt.** Nur neutrale Teile extrahieren; kein blindes Verschieben der gesamten Datei. |
| V06 | `action_catalog.py` kodiert Glide-spezifische Aktionen wie Import, Tagesvorschlag, Aufgaben und Pinnwände. | **Bestätigt.** Shell bekommt generische Aktionsregistrierung; die Aktionstabelle bleibt Glide-Verantwortung. |
| V07 | `runtime_config.py` bietet seiteneffektfreie Pfadauflösung und isolierbare Tests. | **Teilweise bestätigt.** Das Modul selbst ist rein auflösend, verwendet jedoch `APP_NAME = "Glide"` und Glide-Dateinamen. Vollständig neutrales Bootstrap und Freisein *aller* App-Importe von Seiteneffekten wurden hier nicht unabhängig nachgewiesen. |
| V08 | Das 3.55-Konzept beschreibt `undo_history.py` als generischen Memento-/Command-Stack. | **Sachlich zu weitgehend.** Der geprüfte Code ist ein `RedoHistory`-Helfer für den von Glide gehaltenen Undo-Stapel und enthält einen pinnwandspezifischen Eintrag. Kein fertiger produktneutraler Undo-Dienst. |
| V09 | Das Konzept schreibt historische Linux-Timeouts pauschal einem Modal-Grab-Deadlock zu. | **Nicht hinreichend belegt.** Symptome, Ursachen und Schutzmaßnahmen müssen anhand konkreter Logs und Reproduktionen getrennt werden; Shell darf nicht auf einer ungeprüften Fehlerursache basieren. |
| V10 | Der 3.55-QA-Bericht dokumentiert gezielte erfolgreiche Prüfungen und `release_ready=false`. | **Bestätigt als dokumentierter Stand.** Keine unabhängige Framework-Integration und keine abschließende native Gesamtfreigabe. |

### Konsequenzen für den vorherigen Bericht

Die ursprüngliche Liste von zehn Kernbereichen und zahlreichen Diensten ist als **Langfrist-Katalog** weitgehend sinnvoll, aber für ein erstes Framework zu breit priorisiert. „Alles P1“ vergrößert Kopplungsfläche, Testmatrix und Release-Risiko. Außerdem ist die frühere Zeitspanne von 21–40 Entwicklertagen **keine belastbare Aufwandsschätzung**, solange `ListApp`-Aufrufgraph, Callback-Lebensdauer, Einstellungen und Tests nicht systematisch vermessen wurden. Sie wird deshalb **nicht** als Planungszusage übernommen.

## 4. Präzise Grenze: Was gehört in die Shell?

### 4.1 Kernpaket – verbindliches Ziel für Version 0.x

| Kernbereich | Verantwortung der Shell | App-Verantwortung |
|---|---|---|
| **App-Bootstrap und Lifecycle** | genau ein kontrollierter Tk-Interpreter, Initialisierung/Shutdown, Callback-Cleanup, Laufzeitadapter | Produktstart, Datenprüfung, Änderungs-/Speichersperren, Abbruchentscheidung |
| **Window Manager** | `Tk`-Root, optionale `Toplevel`-Fenster, Fensterlage, Mindestgrößen, Fokus/Schließen, Bildschirmgrenzen | welche Fenster der Anwender benötigt und welche Inhalte dort erscheinen |
| **Layout und Breakpoints** | Layout-Zonen/Slots, Größenmessung, Reflow/Überlauf, Pane-Host, Resize-Debouncing | Reihenfolge/Priorität der Glide-Ansichten, Sichtbarkeit fachlicher Funktionen |
| **Themes und Design Tokens** | Light/Dark/Systemmodus, neutrale Farbrollen, Abstände, Schriften und Skalierung | Glide-Markenfarben, produktbezogene Statusfarben, inhaltliche Bedeutung |
| **UI-Grundkomponenten** | Buttons, Eingaben, Schalter, Menüs, Listen-/Scrollbar-Grundbau, Tooltip- und Dialog-Host | Aufgabenzeilen, Rich-Text-Editor, Pinnwandkarten, fachliche Dialoginhalte |
| **Action/Shortcut Registry** | IDs, Ausführung, Verfügbarkeit, Tastaturkürzel, Menu-/Palette-Adapter | Definition und Implementierung konkreter Glide-Aktionen |
| **Settings-Host** | typsichere Registrierung, neutrale UI, Validierung, Namespaces, atomarer Schreibdienst *für Shell-Einstellungen* | Fachsettings, Datenmigration, eigene Werte und deren Speicher-/Kompatibilitätsverträge |
| **Accessibility-Basis** | Tastatur, Fokus, semantische Widget-Grundrollen, Kontrast/Skalierung | sinnvolle fachliche Labels, Lesereihenfolge und Zustände in Glide-Ansichten |
| **Application Contract** | API/Ports für Window-, Theme-, Actions-, Settings-, Slot- und Lifecycle-Dienste | Implementierung eines App-Adapters ohne Rückimport aus der Shell |

**Kriterium für die Paketgrenze:** Eine Datei/Funktion darf nur dann im Kern liegen, wenn sie mit einer synthetischen „Demo-App“ ohne Glide-Datenformat, Glide-Pfade, Glide-Aktionskennungen und Glide-Ressourcen importierbar und sinnvoll testbar ist.

### 4.2 Erweiterungen – optional, nicht im ersten Kern voraussetzen

- Branding/Icons, Font-Ressourcen und AppInfo/Hilfe: als **konfigurierbare Adapter**; keine Glide-Logos oder Namen im neutralen Paket.
- Toasts, Systembenachrichtigungen, Drag-and-drop, Clipboard, Shell-Logging und Systemintegration: optionale **Capabilities**; Plattformverfügbarkeit und Datenschutz explizit behandeln.
- Theme-/Widget-Testkit, Screenshot-/Layoutmessungen, Packaging-Helfer: Entwicklungswerkzeuge, nicht zwingend Laufzeitabhängigkeiten.
- Ein allgemeiner Reversibilitäts-/Undo-Dienst kann später als **eigenständige zusätzliche Bibliothek** untersucht werden. Er darf nicht stillschweigend Glides Daten-Undo oder Mutationsgrenzen ersetzen.
- Allgemeine Sicherung, Migration, Import-/Export- und Datenbankdienste sind höchstens **separate, ausdrücklich beauftragte Kits**; keine Abhängigkeit der visuellen Shell.

### 4.3 Muss in Glide bleiben

Fachmodelle, Aufgaben und Wiederholungen, Listen/Projekte, Tages-/Wochenplanung, Kalendersemantik, Seiten-/Notizeditoren, Pinnwand- und Pixel-Werkstatt, der Fachsuchindex, `item_change`/`sidebar_change`, Undo/Redo auf Nutzerdaten, Persistenz, Datenformate, Backups, Imports/Exports, Datenlocks und alle zugehörigen Sicherheits- und Migrationsregeln.

Die Shell darf diese Konzepte weder kennen noch selbst eine zweite Daten-/Mutationslogik einführen. Der Speicherort einer App ist für die Shell ein konfigurierter Namespace, **kein** Anlass, Glide-Daten automatisch zu öffnen.

## 5. Fenster, Breakpoints und Layout – verbindlicher Begriffsvertrag

**A. Eine App mit zwei Inhaltsbereichen (Dual-Pane):** Ein `Tk`-Hauptfenster enthält mindestens zwei Layoutslots; ein Bereich kann optional ausgeblendet oder innerhalb derselben Inhaltsfläche überlagert werden. Das beschreibt Glides vorhandenen Haupt-/Nebenansichts-Mechanismus deutlich besser als „zwei unabhängige Fenster“.

**B. Zwei unabhängige OS-Fenster (Multi-Window):** Ein `Tk`-Root und zusätzliche `tk.Toplevel`-Fenster mit separaten Fokus-/Geometrie-/Dialogkontexten, aber **einem** kontrollierten Tk-Interpreter und einem Event-Loop. Sie können dieselben Fachobjekte unterschiedlich zeigen, doch Mutation und Datenbesitz bleiben beim jeweiligen App-Controller.

**Empfehlung:** Dual-Pane als verpflichtende Shell-0.x-Fähigkeit, `Toplevel` als getrennten, späteren Vertrags- und Testbereich. Ein echtes zweites Arbeitsfenster nur dann zur Startbedingung machen, wenn es ausdrücklich Produktanforderung ist. Modale Dialoge können bereits früher über den Dialoghost geführt werden.

**Responsive Regeln:** Trennung von (1) generischem Mechanismus und (2) anwendungsabhängigen Schwellen/Verdrängungsregeln. Glides derzeitige Normal-/Kompakt-Minima (860 × 700 bzw. 480 × 560 in `compact_mode.py`) sind **Glide-Konfiguration**, nicht universelle Zahlen. Breitenentscheidungen sollten reale Schrift-/Widgetmaße, DPI und Inhaltsprioritäten berücksichtigen. Bei weniger Platz nicht stillschweigend Funktionen entfernen; Überlauf/Alternative und Tastaturzugang absichern.

## 6. API- und Zustandsregeln

Die verbindliche Abhängigkeitsrichtung lautet:

```text
Glide-Domäne (ohne Tk / ohne Shell-Import)
             ↑ wird verwendet durch
Glide-App-Adapter / Controller
             ↓ nutzt definierte öffentliche API
Glide Shell Framework
             ↓
Tkinter / Betriebssystem
```

Ein neutraler `ApplicationDescriptor` sollte Name, App-ID, Icon-/Ressourcenprovider, Shell-Themes, Fensterkonfiguration, Daten-/Cache-Namespace, lokale Einstellungen und gewählte Capabilities deklarieren. Die App registriert `ViewFactory`-Slots und Aktionen mittels stabiler IDs und erhält über Shell-Schnittstellen Ereignisse und Kontext.

**Ownership:** Der Shell gehören Tk-Interpreter, Rahmen, Event-Bindings, Window-/Dialog-Handles und deren Cleanup. Dem App-Controller gehören fachliche Auswahl, Objekte, Undo-/Speicherzustand und Fachrenderer. Keine globalen Singletons zwischen Anwendungen, keine stillen bidirektionalen Imports, keine Callback-Duplikate oder lang lebenden Widgetverweise in Domänenobjekten. Tk-Updates ausschließlich auf dem zuständigen Tk-Thread.

**Settings:** Shell- und App-Einstellungen getrennt versionieren/namespacen. Bestehende Glide-Dateien nicht verschieben oder automatisch migrieren. Für jede neue Einstellung Typ, Vorgabe, Gültigkeitsgrenzen, Wiederherstellung unbekannter gültiger Werte und Fehlermeldung dokumentieren.

**Daten- und Instanzlocks:** Ein Shell-Lifecycle darf einen generischen Exit-/Window-Hook bieten; App-Datenbesitz und Schutz vor parallelem Schreiben bleiben ausdrücklich in Glide. Ein globaler Single-Instance-Zwang ist **keine** ungeprüfte allgemeine Shell-Policy.

## 7. Empfohlene Umsetzung in Freigabestufen

| Stufe | Maßnahme | Verbindliches Prüftor |
|---|---|---|
| **0 – Baseline** | Referenzcommit festlegen; UI-/Fenster-/Callback-/State- und Datei-Importgraph erfassen, Testmatrix und Öffnungspunkte dokumentieren | Architekturkarte mit konkreten Aufrufern, Widgetbesitz und datierten QA-Belegen; keine Verhaltensänderung |
| **1 – Neutrale Regeln** | Theme-Tokens, pure Geometrieregler, neutralen Runtime-Konfigurationsvertrag isolieren | Pure Unit-Tests, keine Glide-Imports und keine neuen Import-Seiteneffekte |
| **2 – App-API** | `ApplicationDescriptor`, Action Registry, View Slots, Settings-Namespaces hinzufügen | Demo-App ohne Glide-Code startet, zeigt zwei Slots, registriert Aktion und speichert nur Testsettings |
| **3 – Fenster-/Dialoghost** | Root/`Toplevel`/Modal-/Fokuslebensdauer und Callback-Aufräumen schrittweise hinter Schnittstelle bringen | Wiederholtes Öffnen/Schließen, verlorene Fenster-/Modalkontexte, Escape/Fokus, Xvfb und native Tests |
| **4 – Komponenten/Theme** | Bestehende Custom Controls und Designanwendung hinter neutralen UI-Adapter bringen | Widget-API-Kompatibilität und Designs mit kleinen/großen Fenstern, Schrift, DPI und Tastatur prüfen |
| **5 – Glide-Adaption** | Glide schrittweise an Shell-Schnittstellen anbinden; bestehende Adapter als Fassade erhalten | Gleiches Nutzerverhalten, gleiche Datendateien/IDs, gleiche Undo-/Redo-/Backup-/Import- und Ladewege |
| **6 – Paket-Freigabe** | Erst jetzt Paketierung/Versionierung und ggf. separates Shell-Repository entscheiden | Zwei unabhängige Hosts auf gepinnter Shell-Version; Windows/macOS/Linux nachgewiesen; Lizenz-/Quellbezug, Package-Build und Rollback |

Keine Entwicklungs- oder Release-Freigabe wird allein durch diesen Bericht erteilt. Die bestehende Glide-Version 3.55.0 bleibt ein **Entwicklungsbranch**, dessen QA-Bericht die offenen Gesamttore ausdrücklich nennt.

## 8. Reproduzierbare Prüf- und Abnahmematrix

**Isolation:** Import von `glide_shell` in frischem Prozess ohne Glide im `sys.path`; Demo-App mit zwei Inhaltsbereichen und synthetischer Beispielansicht. Keine Zugriffe auf Glide-Produktivdaten oder -Profile.

**Fenster & Ereignisse:** Wechsel Normal/Kompakt, Haupt-/Nebenpane, mehrere echte `Toplevel`-Fenster, Modal-/Nichtmodal-Abbau, Verlust des OS-Fokus, Menüklick unter macOS, mehrfaches Öffnen/Schließen, `after`-Cleanup und fehlender Display-Server. Kein UI-Livelock und keine unbehandelten Tcl-Fehler.

**UI/Accessibility:** Mindest-/Maximalgrößen, gemessene Breakpoints, Kontrast, hohe Schrift/DPI, Touch-/Maus-/Tastaturfokus, Screenreader wo beauftragt, Tooltips, deaktivierte Aktionen mit Begründung, kein Platzhalter-/Restflächenartefakt nach Ausblenden.

**Daten:** bestehende Glide-Daten unter strenger Isolation; JSON-/Settings-Kompatibilität, Undo/Redo, Backups, Restore, Datenlocks, atomare Speicherung und Neustart. Fehlereinwurf bei unterbrochener Speicherung, fehlendem Berechtigungsrecht und verlorenen Fenstern. Nur synthetische Testdaten.

**Plattformen:** Windows 11 mit projektreferenzierter Python-/Tk-Matrix; Linux/Xvfb mit selbst gebauter Tk-Version; macOS Aqua nativ. Tk-8.6-Kompatibilität nur im tatsächlich vorgesehenen Umfang behaupten. Versions- und Hardwarebelege an konkrete Commit-SHAs binden.

**Performance:** vor/nach Umbau identische künstliche Szenarien, Kaltstart und Warmstart, View-Switch, Resize-/Reflow-Zyklen, Speicher, Mediannutzung und p95. Reine Dateiaufteilung ist **kein** Performance-Nachweis.

## 9. Risiken und Entscheidungen

| Priorität | Risiko | Gegenmaßnahme |
|---|---|---|
| Kritisch | UI-Refactoring verändert Datenmutations-/Undo-Verhalten | App-Fassaden und End-to-End-Regressionen an bestehenden Mutationsgrenzen |
| Kritisch | Tk-Reentranz/Layout-Livelock, hängende Grabs oder verwaiste Callbacks | gezielte Ereignis-/Lifecycletests und reale Dialog-/Fenstersequenzen |
| Hoch | Unterschiedliche DPI-/Menü-/Fokussemantik auf drei Plattformen | native Plattformmatrix je geänderter Shell-Version |
| Hoch | Unabsichtliche Kopplung durch Settings-/App-Identitäten und globale Zustände | `ApplicationDescriptor`, eigene Namespaces und striktes Importverbot Shell → Glide |
| Hoch | Änderung an Public API zwingt andere Apps zum ungeprüften Upgrade | SemVer mit kompatiblen Adaptern; gepinnte Versionen, Changelog, Migrationshinweise |
| Mittel | Zu frühe Repository-Abspaltung erzeugt Doppelpflege | anfänglich modulare Ablage im vorhandenen Glide-Repository; erst nach zweitem Host auslagern |
| Mittel | Ressourcen-/Fremdcode-Lizenzkonflikte | MPL-2.0 und Drittanbieter-Lizenzen/Schriften/Symbole je Shell-Paket prüfen; Herkunft und Quellbezug erhalten |

**Noch zu entscheiden:** Ist mit „zwei Fenstern“ wirklich Dual-Pane gemeint oder sollen zwei unabhängig positionierbare Arbeitsfenster ein Muss sein? Dieses Detail bestimmt die Reihenfolge und den Testaufwand. Die Architektur sollte beide Wege zulassen, ohne sie zu vermischen.

## 10. Endgültige Empfehlung und Validierungsstatus

1. **Freigabe als Konzeptgrundlage:** ja, **nach** den hier genannten Korrekturen. Keine automatische Freigabe des neuen branchinternen `GLIDE_SHELL_FRAMEWORK_KONZEPT.md` in seiner unveränderten Fassung.
2. **Freigabe als implementiertes Framework:** nein. Neutraler Host, vollständiger Importgraph, unabhängiger App-Start und native Matrix sind nicht nachgewiesen.
3. **Unmittelbarer nächster Auftrag:** Analyse-/Designpaket „Stufe 0 + API-Spezifikation“ ohne Quellumbau; die Erkenntnisse in der zuständigen kanonischen Glide-Dokumentation mit nachvollziehbarer Entscheidung verankern.
4. **Danach:** begrenzter vertikaler Pilot mit `compact_mode`-/Theme-Regeln, `ApplicationDescriptor`, zwei Slots und Demo-Host. Glide-Verhalten und Daten unangetastet lassen.
5. **Aufwand:** derzeit keine seriöse verbindliche Zahl. Nach Graphinventar und Pilotumfang pro Modul/Prüfpfad schätzen; frühere 21–40 Tage ausdrücklich nur als **nicht validierte Orientierungsgröße** behandeln.

**Dieser Bericht ist eine validierte, korrigierte Architektur- und Entscheidungsgrundlage – kein Testprotokoll einer existierenden Framework-Implementierung.**

---

## Quellen (per Commit fixiert)

- **S1** – [Glide 3.55 Shell-Konzept](https://github.com/n05a-design/glide-to-do/blob/fd979937708a664b715fdacdb5fd9f8d41fa78a4/01_Repository/Glide/docs/GLIDE_SHELL_FRAMEWORK_KONZEPT.md) – vorgeschlagene Module/Phasen; kritische Aussagen sind oben bewertet.
- **S2** – [Glide-System V1.17 und Übernahmevertrag](https://github.com/n05a-design/glide-to-do/blob/fd979937708a664b715fdacdb5fd9f8d41fa78a4/01_Repository/Glide/src/glide/README.md) – Modul- und Bausteinkatalog, Freigabegrenzen.
- **S3** – [Architekturregeln](https://github.com/n05a-design/glide-to-do/blob/594f4c85eb60370a44282b06fcb8017df8181d70/01_Repository/Glide/docs/02_ARCHITECTURE.md) – `ListApp`, eingebettete Nebenansicht, Fenster-/Dialog-/Callback-Regeln, WA-32/39/49.
- **S4** – [Glide-Designrichtlinien](https://github.com/n05a-design/glide-to-do/blob/594f4c85eb60370a44282b06fcb8017df8181d70/01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md) – Responsive und Interaktionsregeln.
- **S5** – [runtime_config.py](https://github.com/n05a-design/glide-to-do/blob/fd979937708a664b715fdacdb5fd9f8d41fa78a4/01_Repository/Glide/src/glide/runtime_config.py), [Unit-Tests](https://github.com/n05a-design/glide-to-do/blob/fd979937708a664b715fdacdb5fd9f8d41fa78a4/01_Repository/Glide/tests/unit/test_runtime_config.py) – seiteneffektfreie Pfadauflösung bei weiterhin festen Glide-Kennungen.
- **S6** – [compact_mode.py](https://github.com/n05a-design/glide-to-do/blob/fd979937708a664b715fdacdb5fd9f8d41fa78a4/01_Repository/Glide/src/glide/compact_mode.py) – neutrale Geometrie mit Glide-Defaults.
- **S7** – [ui_design.py](https://github.com/n05a-design/glide-to-do/blob/fd979937708a664b715fdacdb5fd9f8d41fa78a4/01_Repository/Glide/src/glide/ui_design.py) und [action_catalog.py](https://github.com/n05a-design/glide-to-do/blob/fd979937708a664b715fdacdb5fd9f8d41fa78a4/01_Repository/Glide/src/glide/action_catalog.py) – gemischte Rollen und produktbezogene Aktionskennungen.
- **S8** – [undo_history.py](https://github.com/n05a-design/glide-to-do/blob/fd979937708a664b715fdacdb5fd9f8d41fa78a4/01_Repository/Glide/src/glide/undo_history.py) – Glide-geführter Undo-/Redo-Vertrag, kein fertiger universeller Dienst.
- **S9** – [QA-Bericht 3.55.0](https://github.com/n05a-design/glide-to-do/blob/fd979937708a664b715fdacdb5fd9f8d41fa78a4/01_Repository/Glide/docs/07_QA_BERICHT.md) – dokumentierte Prüfungen und Freigabegrenzen (`release_ready=false`).
- **S10** – [MPL-2.0-Lizenz](https://github.com/n05a-design/glide-to-do/blob/594f4c85eb60370a44282b06fcb8017df8181d70/LICENSE) – rechtliche Rahmenbedingung für Codeübernahmen; keine Einzelberatung zu Fremdcode.
