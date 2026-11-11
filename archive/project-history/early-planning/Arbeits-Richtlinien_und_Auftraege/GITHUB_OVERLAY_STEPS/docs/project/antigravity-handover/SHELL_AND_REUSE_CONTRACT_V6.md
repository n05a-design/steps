# Glide 3.53.0 → neutrale STEPS-Shell: Erhaltung, Rückbau und Modulpflege

## Baseline

**STEPS-Projekt**, Glide-Referenz `src/glide-v3.53/` aus `n05a-design/glide-to-do@9e767bea5e21063466a28ac3a679406484ad5d5f`. Glide App `3.53.0` erfolgreich geprüft; Systemkatalog `1.15`. Ein isoliert entwickeltes gemeinsames SDK existiert noch nicht. V1.15 nennt 94 Module, 147 Features, 25 Reuse-Paketkandidaten und 311 Test-/Werkzeugdateien (vor Implementation per Manifest/AST prüfen).

## Verbindliches Ziel aus dem Nutzerauftrag

Die äußere vertraute Glide-Oberfläche **außerhalb der künftig zwei Arbeits-/Inhaltsbereiche** bleibt visuell und funktional erhalten. Zu behalten: Hauptfenster-Lifecycle, Window-Controls, Größenänderung/DPI, feste Header-/Tool-Leisten, Logo/Überschrift/Untertitel, alle bestehenden System-Symbolbuttons und deren semantische Rollen, Design-Richtlinien und alle vorgesehenen Themes/Fonts, Einstellungen samt Theme/Font/Preferences, Menüs, Tooltips, Tastatur/Fokus, Prozesse/Diagnosen, neutrale Eingabe- und Bearbeitungsflächen wie Suchfeld, Sidebar-Layout/Seitenpunkte, Auswahl, Ein-/Ausklappen/Verbergen der Seitenliste/Seitenleiste, persistierte Layout-States, Dialoge, Accessibility, Save-/Backup-/Crash-Recovery-Konzepte, Undo-/Callback-/After-Lebensdauer, Tests/CI/Packaging-Muster, Doku- und Entscheidungsbelege. Screenshots/gegenwärtige GUI als Visual-Regression-Baseline vor dem Schnitt sichern.

**Zwei Fenster vs. zwei Bereiche:** historische Texte sprechen teilweise von „zwei Fenstern“, detaillierte Specs modellieren *ein OS-Hauptfenster mit Sidebar und Workspace* und optionaler Nebenansicht. Die konkrete Tk-Topologie anhand `app.pyw` und visueller Referenz ermitteln; Entscheidungen in ADR notieren. **Kein zweites `Tk()`-Root** und keine ungebetene Layoutneuerfindung. Bis Owner-Entscheid ein reversibles Zwei-Bereiche-Gerüst mit den vorhandenen nativen Fensterfähigkeiten als Referenz ansetzen.

## Mit STEPS neu zu verbinden

STEPS-eigener Name, App-/Bundle-ID, Logo/Branding mit Lizenzprüfung, `STEPS_DATA_DIR` und Systemdatenordner, Locks/Caches/Logs/Settings/Backups, Projekt-/Musikdatenformat, Routing/Navigation-IDs, neutraler SearchProvider, Workspace-/Editor-Host und domainneutrale Controller-/Command-Ports. Keine Umbenennung historischer Glide-Nachweise oder fremder Lizenzvermerke.

## Zu deaktivieren, erst nach Abhängigkeitsanalyse zu entfernen

Todo-Spezifika: TaskItem, Deadlines, Kalender-/Tagesplanung, Pinnwand-/Aufgaben-/Seiten-Backends, Task-Suche, alte Daten-/Migrationswege, Task-Zähler, To-do-Actions, Wiederholungen, API-/Callback-Routen und Hintergrundaufträge. Die Seitenliste zeigt **nur sichere neutrale Navigationspunkte**; nicht implementierte Features dürfen erklärtes No-op bieten, keine versteckte Task-Mutation. Jede entfernte Routine im `ACTION_DEPENDENCY_REGISTER` mit Auslöser, Status, Test, Rollback und Ursprungs-SHA dokumentieren.

## Abhängigkeits- und Versionsvertrag

Jedes geteilte Modul erhält `component_id`, `source_file@glide_sha`, `version`, `api_contract`, `import_chain`, `runtime_side_effects`, `owned_state`, `asset_dependencies`, `license_status`, `consumer_versions`, `tests`, `semantic_diff`, `migration_notes`, `rollback`. Vor einem zweiten unabhängigen Consumer Status `candidate`. Änderungen am gemeinsamen Grundgerüst laufen in klaren Versionen und müssen **in STEPS und Glide je gesondert** getestet und freigegeben werden; kein blindes Synchronisieren. Mehrfach kopierter Quellcode ohne gepflegtes Manifest ist kein Framework.

## Prüfsequenz

1. Baseline-Bytevergleich `src/glide-v3.53/` gegen Glide-Commit, inklusive Artefaktkopien, Fonts, Images, Packaging, Importketten und Testfixtures; SHA-Manifest.
2. AST/Callgraph der `ListApp`, Startup-Seiteneffekte (sys.path, tk.Menu-Patches, Datenpfad-Anlage, stdout, Cache), Callback-/After-Lifecycle, Datenzugriffe und Service-Kopplung erheben.
3. Konkrete Modul-/UI-Routen per keep/adapt/isolate/remove_later/reject entscheiden; 30 Shell-Szenarien aus `docs/engineering/SHELL_EXTRACTION_DEEP_SPEC.md` mappen.
4. Sicherheits-ADR zwischen inkrementellem Rückbau, Shell-Extraktion, Hybrid und kleiner UI-Paritäts-Gegenprobe nach vergleichbaren Aufwand-/Risiko-/A11y-/QA-Maßen.
5. **Erst nach Owner-Freigabe** Implementierung auf eigenem STEPS-Branch, mit eigener DataRoot-Isolation, negativen No-Glide-Write-/No-Glide-Read-Tests, UX-Screenshots, Sprach-/Theme-/DPI-/Focus-Tests.
6. Danach unabhängige STEPS-Fachmodule (Pitch/H/B, Chord, Progression, Time/Events, Drums, MIDI, Audio/Playback separat) entwickeln; Musiktests und STEPS-Release nicht aus Glide-Grün ableiten.

## Harte Stopps

Schreibzugriff auf Glide-Produktivdaten, fremde Nutzer-/Backupdateien, globale ungeprüfte Tk-Patches, unkontrollierte Imports, nicht eindeutig freigegebene Assets, alte Task-Callbacks über neutrale Punkte, verlorene Undo-/Backup-/Recovery-Verträge, Migration ohne Rücknahmeplan, ungeprüfter Lizenztransfer, gebrochene Settings/DPI/Focus/Shell-Funktionen. Jeder Stopp erhält Registereintrag, nicht Verschweigen.
