# 06 — Shell-Erhalt, Zwei-Fenster-Mehrdeutigkeit und echte UI-Abnahme

## Was der Auftrag **nicht** erlaubt

„Oberfläche außerhalb der zwei Fenster soll bestehen bleiben“ und „nur die Seitenliste mit den Punkten ohne Funktionen“ bedeutet **keine vollständige Löschung des produktiven Glide-Daten-/Command-/View-Stacks**. Erforderlich ist eine *neue Steps-Shell* mit eigenem Datendomänenlayer. Glide bleibt im Ursprungsrepository unverändert funktionsfähig. Auch „funktionslose Seitenliste“ bedeutet nicht unbedienbar: Selection, Expand/Collapse, Hide/Show, Keyboard, Focus, Empty-State und Scroll bleiben funktionale Shell-Mechanismen. Alte Task-Aktionen dagegen dürfen nicht unerkannt im Hintergrund weiterlaufen.

## Drei konkurrierende Fensterinterpretationen

| Variante | Beschreibung | Vorteile | Gefahr/Kosten | Empfehlung |
|---|---|---|---|---|
| W1 | Ein OS-Fenster mit zwei getrennten Inhaltsflächen (Main/Secondary) | Bestehender Glide-`side_view` und Layout weiterverwendbar, weniger Windowmanager- und Focus-Komplexität | Begrenzter Platz auf kleinen Displays, potenziell ungewünschte Nebenflächen | Technischer **Referenzentwurf**, keine Nutzerfreigabe |
| W2 | Ein OS-Fenster mit zwei gleichberechtigten, andockbaren Split-Panes | Flexibles Music-/Drum-Arbeiten und alternative Views | Splitter, DPI, Persistenz und aktiver Pane schwerer, `side_view` nicht ausreichend | Später prüfen, wenn echte Benutzerflüsse es verlangen |
| W3 | Zwei separate native OS-Fenster (`Tk`/`Toplevel`) | Mehrmonitor, freies Arrangement und zwei vollwertige große Arbeitsflächen | Fokus/Aqua/Dialogs, mehrere Fensterpositionen, Modalität, Handle-/Eventlebensdauer; potenzielle Tk-Interpreterprobleme | **Nicht ohne explizite UX-Entscheidung** |

Bis diese Produktentscheidung getroffen ist, dürfen Tests und Dummy-Views nur beweisen, dass **zwei austauschbare Zielansichten** verfügbar sind. Es darf keine fiktive Nutzerfreigabe in ADRs stehen. Ein späteres Split-Pane oder `Toplevel` darf den fachlichen ViewModel-Vertrag nicht ändern müssen.

## Preserve / Remove / Adapt / Defer — Komponentenvertrag

| Bestandsteil | Sollzustand in Steps-Shell | Verifikationsbedingung |
|---|---|---|
| Hauptfensterrahmen, Skalierung, Geometrie, Minimierung | Preserve + Produkt-Adapter | kaltes Starten, Wiederherstellen, schmale/große Fenster, Mehrmonitor |
| Kopf mit Logo, Titel, Unterzeile, Symbolknöpfen | Preserve Mechanismen, neue ProductIdentity | korrekte Steps-Produkttexte/Assets, keine historische Glide-Marke als Steps-Identität |
| Theme hell/dunkel, Designrollen, Akzentfarben, Schriftwahl, Gewicht | Preserve Mechanismen | 4 Glide-Schriftstil-Baselines nur wo mit lizenzierter Ressource ausgewählt; Theme-/Fontwechsel mit Restart und Glyphfallback |
| Seitenleistenbereiche/Navigation | Preserve Layout und Hide/Fold/Select, Replace Domain | Default-Einträge zu Steps-Seiten und neutralen Dummy-Zielen, keine Task-Commands |
| Einklappen/Verbergen/Wiederherstellen Seitenleiste | Preserve | Maus + Tastatur, Fokus, Scroll/Selection, Persistenz, keine Restfläche |
| Suche/Bearbeitungsflächen | Preserve Widgettyp, Rebind SearchProvider | leere Suche, keine Tasktreffer, Fokus/Shortcut, längste Eingabe, Disabled und Invalid |
| Einstellungen | Preserve Settings-UI, Replace Userdata-/Produktwerte | eigener Storage, Migrationsplan, unbekannte Settings, Restart |
| Menüs/Befehle/Action-Palette | Adapt durch CommandRegistry | keine versteckten Glide-Aktionen, keine doppelten Keyboardpfade, Disabled-Gründe |
| Haupt-/Nebenansichts-/Editorfläche | Replace **Inhalt**, Preserve Host | zwei getrennte ViewModels und Lifecycle, schnelles Umschalten, Leercanvas |
| Focus-/Toast-/Error-/Ladezustand | Preserve Regeln, neu anbinden | UI responsive, Fehler sichtbar, keine sensiblen Logs |
| Datenobjekte Aufgaben/Seiten/Notizen/Pinnwände | **Nicht in Steps-Core übernehmen** | kein Cross-App-/Glide-Dateikontakt; nur ausdrücklich gewählte UI-/Dokumentfunktionen adaptiert |
| Kalender/Today/Planung/Notion | Defer/Exclude | keine Laufzeitimports und keine versteckten Buttons aus alter App |
| Undo/Redo, Speichern/Backup | Preserve **Vertrag**, Replace Fachschema | Domaintransaktionen mit eigener Steps-Data-Identity, Sicherungs-/Restoretest |
| Pixel-Zeichnung | Optional, nicht Teil Basisshell | nur bei fachlichem Bedarf mit eigenem Datenvertrag und Lizenz-/Performanceprüfung |
| Systembenachrichtigungen/Drag&Drop | Optional Adapter | kein Netzwerk-/OS-Zwang, graceful degradation |
| Gestaltungs- und Entscheidungsdokumentation | Preserve Governance, nicht historische Produktentscheidung | eine autoritative Quelle je Thema, datierte Nachweise unverändert |

## Zustandsmodell: Sidebar

`visibility={expanded, collapsed, hidden}` und `selection={none, id}` sind getrennt; `collapsed` zeigt Symbole oder kompakte Darstellung, `hidden` beansprucht keinen Inhaltplatz. `ToggleCollapse`: expanded ↔ collapsed; `ToggleVisibility`: expanded/collapsed ↔ hidden mit gemerkter letzter sichtbarer Variante. Speichern/Rückkehr muss klar entscheiden, ob Sichtzustand pro Fenster, global oder pro Workspace gilt. Alte Glide-Pfade `pages/lists/notes/drawings` aus `sidebar_policy.py` sind **Domain** und dürfen nicht als universeller Name verwendet werden. Neue Navigation braucht Provider-/Elementtypen und stabile IDs.

## Zustandsmodell: Zwei Flächen

`SlotState={unmounted, mounting, active, suspended, disposing}`, und pro Slot genau ein aktiver `view_id`. `mount`: Widget erstellen und Callback-Owner registrieren; `activate`: Fokus/Keyboard-Routing; `suspend`: teure Zeichnung/Audio-Preview stoppen; `dispose`: `after_cancel`/Eventbindings/Bildrefs/Streams freigeben, kein später Callback an toten Widget. Schnellfolge `A→B→A→Close→B` darf nur B aktiv lassen; kein Thread aktualisiert Tk direkt. Ein Empty-State beschreibt die nächste erlaubte Aktion, keine leere scheinbar defekte Rahmenfläche.

## UI-/Accessibility-Matrix

**Dimensionen:** Windows/macOS/Linux; Light/Dark/High contrast; alle vier aktuellen Schriftstile (Rubik, DM Mono, DM Serif Display, Charis SIL) und gewünschte Gewichtsstufen; Font-Datei vorhanden/fehlend; OS-Scaling und Tk-Skalierung; kleine/übliche/maximale Fenster; Sidebar expanded/collapsed/hidden; zwei Slots offen/leer/befüllt/geschlossen; Keyboard-only; Fokuswechsel zu Fremd-App; getrennte/Toplevel-Window-Focus; mehrere Displays. **Full Cartesian Product ist unrealistisch**: Pairwise-Auswahl plus deterministische Pflichtkombinationen für bekannte kritische Risiken, benannte Coverage-Grenzen.

**Konkrete Invarianten:** Keine abgeschnittene Aktionsbeschriftung; Icons mit semantischem Namen, nicht nur Farbe; aktiver Navigationseintrag klar wahrnehmbar; Hover/Focus/Selected nicht widersprüchlich; keine wiederverwendete Glide-Produkt-ID in UI-Titeln; jede geschlossene View gibt Flächen und Callback-Token frei; Dialog bleibt beim Modell/Widgethost; keine Layoutschleifen durch `update()`/`update_idletasks()` in reentranten Bindings. Glide-Designregeln D66–D77 weiter als Ausgangspunkt lesen, aber Änderungen an Steps-Branding sind eigenständige Produktentscheidungen.

## Minimale automatisierte Vertragsfälle (neues Projekt)

- `shell_import_does_not_touch_glide_data`: Sperre realen Glide-Pfad via Access-Spy, starte Steps isoliert. **Negativgegenprobe** absichtlich eingekoppelter Glide-Import muss Test rot machen.
- `sidebar_states_3_by_2`: (expanded/collapsed/hidden) × (Maus/Tastatur), id/scroll/focus beibehalten, keine verschluckte Aktion.
- `commands_no_task_side_effects`: Suche/Shortcut/Contextmenu nach Steps startet keinen alten Glide-Aufgaben-Handler.
- `secondary_mount_dispose`: 100 schnelle Wechsel, keine ausstehenden Callbacks/Fremdwidgets; Tk-`after`-Tokencheck.
- `theme_change_all_fonts`: kontrast- und textmetrische Checks; manuelle visuelle Matrix bleibt trotzdem nötig.
- `root_shutdown_during_io`: Worker-Ergebnis nach geschlossenem Root ignorieren/kontrolliert melden, kein Tk-Write aus Fremdthread.
- `settings_restart`: rein lokale Datei, Schema/Version, persistierter Sidebarzustand, keine fremde App-Datenöffnung.

**Abnahmerisiko:** UI-Screenshots zeigen nur eine bestimmte Pixelkombination. Ein UI-Paket ist erst nach realer Bedienung in repräsentativen Zustandsfolgen und Zuordnung der Laufzeit/Plattform zum jeweiligen Quellstand abgenommen.
