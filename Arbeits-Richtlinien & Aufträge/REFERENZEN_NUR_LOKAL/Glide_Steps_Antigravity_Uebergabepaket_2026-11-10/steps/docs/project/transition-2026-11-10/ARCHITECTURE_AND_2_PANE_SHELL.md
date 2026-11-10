# Zielarchitektur: Zwei-Inhaltsbereich-Shell mit austauschbarer Domäne

## Drei Zuständigkeitsgrenzen

1. **Produktneutrale Shell (späteres Systemkit)**: Fenstermanagement, `primary_pane_host`, `secondary_pane_host`, Aus-/Einblenden, Sidebartopologie, Kopf/Logo/Title/Toolbar, Symbolbuttons und Tooltips, Such-/Editor-Container, Status/Busy-Prozesse, Design-Rollen, Fonts, Settings, Fokus, Keyboard, Menüs, a11y, Lifecycle, Dialog Cleanup. Noch **keine eigenständige Library**.
2. **Integrationsadapter je App**: liefert Navigationseinträge, Aktionen, Ansichten, Suche, Benutzer-Einstellungen, Branding, Datenablage, Persistenz/Undo/Backup und optionale OS-/Audio-Dienste; keine zyklische Abhängigkeit.
3. **Steps-Fachdomäne**: `src/steps/` enthält reine Musik-/Event-/Harmoniemodelle, keine Widget- oder Datenpfad-Imports; App implementiert Präsentation, Controller, I/O, Audio-/MIDI-Port.

## Erhaltungsmatrix der Oberfläche

| Baustein | Neutraler Testhost | Glide | Steps |
|---|---|---|---|
| Zwei Inhaltsbereiche | Dummyansichten, Wechsel und Wiederherstellung | bestehende Task- und Seitenansichten | Chord-Editor / Harmonie-Inspector bzw. Drum-Pattern (später festlegen) |
| Seitenliste | vorhandene Optik, Einträge inert | vollständige bestehende Seitenfunktionen | über Steps-Navigation neu belegt |
| Sidebar einklappen/ausblenden | **funktioniert** | **funktioniert** | **funktioniert** |
| Kopf / Logo / Titel | generische Marken- und Textslots | Glide-spezifisch | eigene Steps-Marke und Icons |
| Symbolknöpfe / Aktionsleiste | Aktionports, deaktivierte Zustände, Tooltips | Glide-Aktionsregistry | Steps-Aktionen, kein Task-Parser |
| Suchfeld / Editor-Hosts | einander unabhängige Eingabeflächen, Fokus-/Flush-Vertrag | Glide-Suche/Editoren | Chords, Patterns, Knowledge-Suche |
| Appearance / Typografie | Light/Dark/System, vier Stilfamilien als **Glide-Ausgangsstand**, semantische Rollen | aktuell D77-Snapshot | ausgewählte, lizensierte eigene Konfiguration |
| Einstellungen | getrennte Namespaces je App, Migrations- und Fehlerschema | Glide-Einstellungen | Steps-Projekt-/Musikoptionen |
| Save/Undo/Backup | austauschbare Ports mit expliziter Commit-Grenze | Glide-Format 26 | Steps-eigenes Save-Schema, nie Glide-Dateien |

## Shell-Verhalten als Invarianten

- Wenn die Seitenliste ausgeblendet ist, bleibt die Aktion zum Einblenden verfügbar und Tastaturfokus landet deterministisch.
- Beim Öffnen/Schließen der Nebenansicht bleiben Hauptansicht, Scrollposition, aktiver Editor, History und laufende Timer nur gemäß explizitem Vertrag erhalten; keine verwaisten `after`-Callbacks oder Tk-Images.
- Widgets werden ausschließlich vom Tk-Hauptthread manipuliert; Hintergrundarbeit meldet Ergebnisse über sichere Queue/Dispatcher-Ports.
- Designänderung invalidiert Cache und Schriftmetriken; Symbolfall-back bleibt vorhanden; Tooltip-/A11y-Texte hängen an semantischen Aktionen statt an Unicode-Glyphen.
- Navigation vom Suchfeld/Editor führt vorher einen kontrollierten Flush/Save-Check aus und respektiert Cancel/Undo.
- Neutraler Testhost hat **keine** Glide-Daten-, Netz- oder Schritte-Abhängigkeit; fachliche Inaktivität der Seitenliste darf nicht versehentlich Sidebareigenschaften entfernen.

## Schnittstellenentwurf (nicht implementiert)

- `ShellHost` übernimmt Widget-Hierarchie und Lebenszyklus.
- `PaneProvider` liefert UI-Views und Identität, aber kein Owner von Storage.
- `NavigationProvider` liefert strukturierte Menüpunkte, History und Aktivierungsstatus.
- `ActionRegistry` ist die einzige Quelle für Commands, Tastaturkürzel, Command Palette und Button-Enablement.
- `DesignSystem` liefert Tokens/Fonts/Assets/semantische Rollen.
- `AppServices` bündelt `SettingsPort`, `SearchPort`, `PersistencePort`, `HistoryPort`, `NotificationPort`, optional `MidiPort`/`AudioPort`.

**API-Freeze erst nach Code-Audit:** Daten-/Fehlerverträge und Tk-Topologie an den realen `ListApp`-Eigenschaften und zwei erfolgreichen Tests festlegen. Die Namen oben sind Architekturvorschläge, nicht existierende Module.

## Testmatrix

Panes 1/2 an/aus; Sidebar sichtbar/eingeklappt/versteckt; unterschiedliche Fenstergrößen/Monitore/DPI; Navigation via Maus/Keyboard; 4 Schriftstilklassen und Gewichte; Themewechsel; Suchfeld-/Editor-Fokus; Wiederherstellung von Geometry/Settings; Crash/Reload; falsche IDs; leere Einträge; nach 1000 Wechseln keine ungebundene Callback-/Image-Leak-Explosion; kein Seitenleistenverlust, kein Datenpfad-Crossover.
