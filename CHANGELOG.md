# Änderungsprotokoll

## Unreleased – 0.8.0-dev (2026-11-24)

### Hinzugefügt / Geändert
- **Windows-Dateisperren und Musikprüfung.** STEPS prüft aktive Projektbesitzer mit einem Prozesshandle, ohne ein Windows-Konsolensignal auszulösen. Der SMF-VLQ-Codec prüft die Vier-Byte-Grenze in beide Richtungen. MVVE vergleicht weitere Akkorderweiterungen und ergänzt generierte Mutationen, Parser-Eigenschaften und transponierte Exportfälle. [Nachweise](docs/audit/2026-11-28/MVVE_V21.md)
- **MVVE-Musikprüfung.** Unabhängige Referenzfälle für Tonhöhen, Akkorde, Skalen, Harmonisierung, Bassrollen und exakte Akkorderkennung. Die bestehende Zufallsprüfung meldet Infrastrukturfehler und speichert reproduzierbare Fälle. Technische PR-, Zeitplan- und Release-Prüfungen wurden erweitert. [Nachweise und offene Freigaben](docs/audit/2026-11-27/MVVE_V2.md)
- **Keyboard, Skalen und Übungen.** Alterierte und erweiterte Basstöne erhalten ihre musikalische Rolle ohne widersprüchliche klassische Bezifferung. Skalen und Übungsdefinitionen prüfen ihre Werte beim Erstellen. Bei einer leeren Antwort zeigen Übungen mit Sollregister auch die fehlenden konkreten Töne.
- **MIDI-Dateiprüfung.** Der SMF-Parser lehnt abgeschnittene Header auch dann ab, wenn der Header keine Tracks deklariert.
- **Musik-Keyboard (Vorschlag ADR-018, Branch `feat/steps-music-keyboard-interactive-engine`):**
  - Reine Keyboard-Domäne `src/steps/keyboard/`: 88-Tasten-Modell (A0–C8), Rollen und kontextuelle Schreibweise aller Akkordtöne, Skalen-Überlagerung, Zustandsmodell mit fester Darstellungspriorität, mehrdeutigkeitsbewusste Akkorderkennung ohne Konfidenzwerte, Stimmführungsvergleich konkreter Voicings, getrennte Eingabezustände und ein Übungspilot mit sechs Aufgaben (KI-Entwurf, nicht fachlich geprüft, nicht veröffentlichbar).
  - Modaler Keyboard-Dialog (Werkzeuge-Menü und Seitenleiste) mit Progressionsvorschau, freier Eingabe (Maus und Computertastatur) und Übungsmodus; einzige Projektänderung ist das rückgängig machbare Einfügen eines erkannten Akkords.
  - Port-Spezifikation `src/steps/ports/live.py` für Live-MIDI-Eingang und Notenvorschau nur mit Testadaptern; ADR-007 (nur Dateiexport) bleibt unverändert, ADR-019 vorgeschlagen.
  - `ProgressionSessionController.remove_listener`; 144 neue EN/DE-Katalogeinträge.
- **Universelle Glide-Flächenkomponenten (`RoundedSurfaceCard`) & einheitliche Abstände:**
  - Austausch sämtlicher verbliebener eckiger `tk.Frame`-/`tk.LabelFrame`-Container durch `RoundedSurfaceCard` (`ThemeManager.make_surface_card`) in Hauptfenster (`sidebar_frame`, `sidebar_rail_frame`, `toolbar_card`, `prog_frame`, `info_header_card`, `detail_frame`), `NextChordPanel`, `ReviewedProgressionLibraryDialog` (`top_card`, `list_frame`, `preview_frame`, Akkord-Vorschaukarten), `VoiceLeadingLabDialog` (`nav_card`, Vergleichspanels) und `MidiExportOptionsDialog` (Optionsgruppen).
  - Eckensicheres Innen-Inset (`_min_corner_inset`, `_effective_pad_x`, `_effective_pad_y`) und Live-Geometrie-Synchronisation bei `set_theme(...)`, sodass innere Widgets bei allen Rundungsstufen (`large` 18px, `standard` 12px, `subtle` 6px, `flat` 0px) sauber innerhalb der gerundeten Kontur liegen.
  - Beseitigung innerer rechteckiger Rahmen um `tk.Listbox` (`chord_listbox`, `candidates`) und schreibgeschützte `tk.Text`-Vorschauen (`configure_readonly_preview` nutzt `highlightbackground=colors.bg_surface` und behält `highlightcolor=colors.border_focus` für Tastaturfokus); `PianoRoll` zeichnet einen gerundeten Canvas-Hintergrund (`rounded_rect_points`).
  - Durchgehende `8 px` (`sp.sm`) Abstände zwischen allen Karten und `PanedWindow`-Teilern (`MainWindow`, `NextChordPanel`, `ReviewedProgressionLibraryDialog`, `VoiceLeadingLabDialog`) sowie kontraststarke Mischfarben (`_blend_hex`) für lesbare Beschriftungen auf deaktivierten `RoundedButton`-Schaltflächen.
- **Glide-Kopfzeile, macOS Dock-Symbol & zweispaltige Einstellungen (`AppearanceDialog`):**
  - Seitenleisten-Toggle (`◧`) und Einstellungen-Button (`⚙`) oben rechts in der Kopfzeile sowie beschrifteter Einklappen-Button (`«  Einklappen` / `«  Collapse`) unten links in der Seitenleiste.
  - macOS Dock-Icon nutzt `MACOS_ICON_SHARE = 824 / 1024` in `app/brand.py` für plattformkonforme Randabstände auf Apple-Systemen.
  - Zweispaltiger Glide-Einstellungsdialog mit abgerundeten Auswahlfeldern (`GlideOptionSelector`), Farb-Swatches, `AccentMonogramTile`, Sprachwahl (`system` / `de` / `en`) und Echtzeit-Vorschau.
- **Eigenständiger Desktop-Startweg außerhalb von DAW-Software:**
  - `app/start.py` (`bytecode_cache_dir()`, `check_python_version()`, `ensure_repo_on_path()`), `app/__main__.py` (`python3 -m app`), `STEPS.pyw`, ausführbares `STEPS.command` (macOS Finder) und `[project.gui-scripts]` `steps-desktop = "app.start:main"` in `pyproject.toml`.
- **Versionierung:** Anhebung von Paket (`0.8.0.dev0`), App (`0.8.0-dev`) und Dokumentation.

## [0.7.0-dev] - 2026-11-24

### Hinzugefügt / Integriert
- **Vollständige Glide-Anpassungsparität (10 Themes, 10 Hintergründe, 8 Akzente, Einstellungen-Persistenz):**
  - **10 kanonische Glide-Themes:** Integration aller 10 Designs aus Glide v1.0.2 in `tokens.json` und `ThemeManager`:
    - `dark`: Dunkel
    - `light`: Hell
    - `glass-dark`: Liquid Glass · dunkel
    - `glass-light`: Liquid Glass · hell
    - `dopamine`: Dopamin · kräftige Farben
    - `contrast-dark`: Kontrast dunkel (Okabe-Ito CVD)
    - `contrast-light`: Kontrast hell (Okabe-Ito CVD)
    - `minimal-dark`: Minimal dunkel (reine Helligkeitsabstufung)
    - `minimal-light`: Minimal hell
    - `pixel`: Pixel · Blockfarben
    - Sowie systemkonformer Automatik-Modus (`system`) mit Paarauflösung über `glide_shell.system_appearance.resolve`.
  - **Akzentfarben-Anpassung (`accent_color`):** Freie Wahl der Akzentfarbe (`accent` Lila, `clear` Blau, `due_action` Türkis, `export` Grün, `flag` Gelb, `delete` Rot, `import` Braun, `muted` Kontrastgrau) mit dynamischer Berechnung der invertierten Textfarbe für garantierte WCAG 2.2 AA Kontraste ($\ge 4{,}5:1$).
  - **10 Hintergrund-Farbtöne:** Vollständige Auswahl aus Designvorgabe (`default`), Wie Fensterfläche (`surface`), Lila (`accent`), Blau (`clear`), Türkis (`due_action`), Grün (`export`), Gelb (`flag`), Rot (`delete`), Braun (`import`) und Kontrastgrau (`muted`).
  - **Einstellungs-Persistenz (`app/settings.py`):** Atomare, plattformkonforme Persistenz aller Benutzereinstellungen (`settings.json`) unter `platform_data_dir("STEPS")` mit Umgebungs-Override `STEPS_DATA_DIR` für isolierte Tests (Regel WA-49/WA-50, Regel 10).
  - **Erweiterter AppearanceDialog:** Modaler Dialog mit Canvas-Scrollbar (`ThemedAutoScrollbar`), zweispaltigem Aufbau, Echtzeit-Vorschaukarte (`RoundedSurfaceCard`, `RoundedButton`, Titel, Untertitel, Akzentknopf, Hintergrund-Insel), Schaltern für Schriftgewicht, bewegte Rückmeldung (≤ 150 ms nach B03) und ergänzende Hinweise (B06).
  - **Hauptfenster-Menüs:** Vollständige Menüs unter Einstellungen für Sprache, Design (10 Varianten), Akzentfarbe (8 Töne), Hintergrund (10 Töne), Rundung (4 Stufen), Schriftgröße (3 Stufen) und Schriftgewicht (3 Stufen).
  - **Glide-Design-Komponenten überall:**
    - `RoundedButton` als Standard-Buttonkomponente mit abgerundeten Ecken, fließendem Übergang zur Trägerfläche (`carrier_bg`), echten Theme-Tokens, Tastaturfokusring und Hover-/Active-Feedback plattformübergreifend auf allen Betriebssystemen (macOS, Windows, Linux).
    - `ThemedAutoScrollbar` in allen Dialogen und Bereichen (`ReviewedProgressionLibraryDialog`, `VoiceLeadingLabDialog`, `NextChordPanel`, `AppearanceDialog`, `MainWindow`).
    - Vollständige Beseitigung aller verbliebenen Vor-Glide-Hex-Farbcodes (`#121319`, `#1E222C`, `#F3F1ED`, `#60A5FA` etc.) zugunsten der kanonischen Glide Shell 0.6.2 / Glide v1.0.2 Design-Tokens.
  - **Trägerflächen-Hierarchie (B17/B19):** Saubere Trennung von Fenstergrund (`colors.bg_window` als Trägerinsel), Inhaltskarten (`RoundedSurfaceCard` mit `colors.bg_surface` und `corner_radius`) und Unterleisten ohne unruhige Schmuckelemente.
  - **Fenstergeometrie-Persistenz & CLI-Parität:** Speicherung und Wiederherstellung der Hauptfenstergeometrie (`window_geometry`) und Kompaktmodus-Geometrie (`saved_compact_geometry`) gemäß B15; CLI-Option `--theme` akzeptiert alle 10 Glide-Designs.
- **Versionierung:** Anhebung von Paket (`0.7.0.dev0`), App (`0.7.0-dev`) und Dokumentation.

## [0.6.0-dev] - 2026-11-24

### Hinzugefügt / Integriert
- **Vollständiges Glide-Designsystem (Tokens & Paletten):**
  - Alle vorherigen STEPS-Design-Tokens in `design/tokens/tokens.json` wurden vollständig durch die kanonischen Farbwerte, Schriftgrößen, Abstände und Rundungen aus Glide v1.0.2 (`app.pyw`, `ui_design.py`) überschrieben.
  - **Dunkelmodus (`dark`):** Glide Canvas (`#111113`), Card Surface (`#1C1C1E`), Active/Field (`#2C2C2E`), Border (`#3A3A3C`), Text (`#F5F5F7`), Muted (`#A1A1A6`), Placeholder (`#939398`), Akzent/Auswahl (`#C66CF3`), Export/Bestätigen (`#30D158`), Löschen/Warnung (`#FF5950`), Cyan (`#40C8E0`), Blau (`#2C95FF`), Gelb (`#FFC038`).
  - **Hellmodus (`light`):** Glide Canvas (`#F5F5F7`), Card Surface (`#FFFFFF`), Hover (`#D8E9FE`), Active/Line (`#E5E5EA`), Border (`#D8D8DE`), Text (`#15243C`), Muted (`#6E6E73`), Placeholder (`#707074`), Akzent/Auswahl (`#9E4AC8`), Export/Bestätigen (`#22813A`), Löschen/Warnung (`#D43128`), Cyan (`#227B8B`), Blau (`#086FD6`), Orange (`#A35F00`).
  - **Kontrast- und Minimal-Themes:** Reines Okabe-Ito-Kontrastpaar und ruhige Helligkeitsabstufung der Minimal-Designs.
  - Alle Paletten sind mathematisch nachgewiesen WCAG 2.2 AA konform ($\ge 4{,}5:1$ Fließtext).
- **ThemedAutoScrollbar:**
  - Austausch nativer OS-Scrollbars durch `glide_shell.custom_controls.ThemedAutoScrollbar` für Akkordliste und Detailansicht im Hauptfenster.
  - Theme-Farbübernahme (`bg_surface`, `bg_surface_hover`, `border`, `harmonic_tonic`) mit abgerundeten Daumen und automatischem Ausblenden bei vollständiger Sichtbarkeit.
- **Dynamische Typografie & Skalierung:**
  - `apply_theme` aktualisiert alle Fensterelemente (Titel, Untertitel, Überschriften, Formularbeschriftungen, Radiobuttons, Eingabefelder, Aktionsknöpfe, Listen und Textansichten) dynamisch mit den über `font_scale` skalierten Schriftgrößen.
- **Versionierung:** Anhebung von Paket (`0.6.0.dev0`), App (`0.6.0-dev`) und Dokumentation.

## [0.5.0-dev] - 2026-11-24

### Hinzugefügt / Integriert
- **Glide Anpassungs-Parität & Customization:** Vollständige Parität zu den Anpassungsmöglichkeiten der Glide Shell:
  - Neuer modaler Dialog „Erscheinungsbild anpassen…“ (`AppearanceDialog`, Tastaturkürzel `⌘`/`Ctrl+,`) mit interaktiver Live-Vorschau (`RoundedSurfaceCard`, `RoundedButton`).
  - 9 wählbare Hintergrund-Farbtöne (`default`, `surface`, `accent`, `clear`, `due_action`, `export`, `flag`, `delete`, `muted`) mit intelligenter Farbtönung (`with_background`), die den Lesekontrast nach WCAG 2.2 AA ($\ge 4{,}5:1$) garantiert.
  - Einstellbare Eckenrundung: Standard (12 px), Groß (18 px), Dezent (6 px), Scharf (0 px) für alle Trägerkarten und Aktionsknöpfe.
  - Dynamische Schriftgrößenskalierung: Kompakt (90 %), Standard (100 %), Groß (115 %).
  - Canvas-basierte Widgets mit echten abgerundeten Ecken (`RoundedSurfaceCard`, `RoundedButton`) auf Basis von `glide_shell.custom_controls.rounded_rect_points`.
  - Vollständige Menüintegration unter Einstellungen mit Submenüs für Design, Farbton, Rundung und Schriftgröße (ausgerichtete Häkchen nach D71).
  - 100 % zweisprachige Lokalisierung (DE/EN) aller Anpassungsoptionen ohne wortwörtliche GUI-Texte.
- **Tests & Qualität:** 15 neue Unittests für Custom-Widgets, Farbkontrast, Eckenrundung und Schrifttypografie (`tests/test_custom_widgets.py`, `tests/test_theme_tokens.py`, `tests/test_glide_shell_integration.py`).
- **Versionierung:** Anhebung von Paket (`0.5.0.dev0`), App (`0.5.0-dev`) und Dokumentation.

## [0.4.0-dev] - 2026-11-24

### Hinzugefügt / Integriert
- **Glide Designsystem & Themes:** Vollständige Integration des portablen Glide-Designvertrags ([`docs/design/GLIDE_DESIGN_CONTRACT.md`](docs/design/GLIDE_DESIGN_CONTRACT.md)) mit 6 barrierefreien Themes (`dark`, `light`, `contrast-dark`, `contrast-light`, `minimal-dark`, `minimal-light`) plus automatischer Systemerkennung (`glide_shell.system_appearance`).
- **Farben & Barrierefreiheit (WCAG 2.2 AA):** Alle Paletten in `design/tokens/tokens.json` erfüllen mathematisch nachgewiesen $\ge 4{,}5:1$ Kontrast für Fließtext und $\ge 3:1$ für Großschrift/Platzhalter. Kontrast-Themes nutzen Okabe-Ito CVD-sichere Akzente für harmonische Funktionen (Tonika, Subdominante, Dominante, Alteriert, Moll); Minimal-Themes bieten ruhige Graustufen-Differenzierung nach Helligkeitsabstand.
- **Flächen-Hierarchie:** Saubere Schichtung aus Fensterhintergrund (`bg_window`), Trägerkarten (`bg_surface`, 1px Rand, `FLAT`), aktiver Auswahl (`bg_active`) und Hover-Flächen (`bg_surface_hover`).
- **Buttons & Schutz (B15, D63):** Unmittelbares Button-Hover-Feedback, aktive Tastenmarkierung (`set_button_active`), 24-Zeichen-Beschriftungsbegrenzung (`clip_button_text`) gegen Textüberlauf sowie Flachrelief mit Fokusrahmen.
- **Texte & Menüs (D71, B11):** Bündig ausgerichtete Menühäkchen (`aligned_menu_markers`), D66-Metrikenzeile mit Tonart, Tongeschlecht, BPM und Taktart, zweisprachige Lokalisierung (DE/EN) aller neuen Themes.
- **2-Pane Shell & Breakpoints:** Einklappbare Seitenleiste (200px breit / 64px Symbol-Rail / ausgeblendet), responsive Dichte-Breakpoints (Header 1120/900, Höhe 850/780, Auto-Rail < 760), Kompaktmodus (`520 × 720` bis `480 × 560`) mit Geometriewiederherstellung.
- **Tests & Qualität:** 10 neue Design- und Kontrasttests in `tests/test_theme_tokens.py` und 9 Integrationsprüfungen in `tests/test_glide_shell_integration.py`.
- **Versionierung:** Upgrade von Paket (`0.4.0.dev0`), App (`0.4.0-dev`) und Dokumentation.

## [0.3.0-dev] - 2026-11-23

- Die Entwicklungs- und Paketversion für STEPS wurde nach der Migration auf `glide_shell` `0.6.2` auf `0.3.0-dev` (`0.3.0.dev0` in `pyproject.toml` und `src/steps/__init__.py`, `CURRENT_APP_VERSION` in `src/steps/storage/project_io.py`) sowie in der Dokumentation aktualisiert.
- Die Desktop-Anwendung baut produktiv auf der übernommenen `glide_shell` (`0.6.2` aus Glide `v1.0.2`, Commit `7dcd8dc04366f88943fa17827882cef4d81421b8`, System `V1.86`, MPL-2.0) auf (`app_host.AppHost`, `modal_session`, `window_lifetime`, `window_geometry`, `system_appearance`, `custom_controls`, `desktop_adapter`, `text_fit`, portabler Designvertrag `DESIGN_RICHTLINIEN.md` inkl. WCAG-AA-Kontrastanpassung für `harmonic_subdominant` im Light-Mode sowie Agenten-Skills).
- Die Musikprüfung stellt reproduzierbare Zufallsfragen zu acht Bereichen. Septakkord-Umkehrungen und eindeutige Dominantstufen wurden korrigiert.
- Roadmap, Implementierungsstand, 1.0-Zielbild und Aufgabenregister beschreiben den Stand nach PR #265 mit Etappen bis 1.0. Eine Prüfung relativer Markdown-Links läuft in der CI. Issue-Vorlagen verwenden eine versionierte Label-Taxonomie.

- Das MIDI-Exportstudio zeigt die tatsächlich vorbereiteten Noten und hält den Export an, wenn sich das Projekt während der Dateiauswahl ändert.

- Der Progressionskatalog bezeichnet die Stufen von `Em9–Am9–D9–Gmaj9` durchgehend relativ zu natürlichem e-Moll.

- Das Stimmführungslabor berechnet Power-Voicings aus Grundton und Quinte und bevorzugt im Quartalprofil benachbarte reine Quarten. Notierte Slash-Bässe bleiben erhalten.

- Der Wissensadapter gibt freigegebene Pilot-Aussagen mit allen Fundstellen aus und meldet fehlende Nachweise bei unbelegten Abfragen.
- Die Laufzeitprüfung des Wissensadapters prüft die 25 Referenzfragen auf Status, Claim-IDs und Quellen. Der Adapter erkennt die beiden dokumentierten englischen Fragen zur B-Notation.

- Der Next Chord Explorer behält gültige Vorschläge bei doppelten Vorzeichen und lässt einzelne nicht darstellbare Schreibweisen aus.
- Der Akkordexplorer zeigt Literaturverweise mit Fundstelle und kennzeichnet Rechenregeln und Arrangementideen. `source_id` ist in der Python-API optional.
- Das Quellenmenü des Akkordexplorers öffnet hinterlegte Literaturhinweise für die Auswahl und den angehefteten Vergleich.
- Der Akkordexplorer zeigt die konkreten Modellbegründungen auf Deutsch oder Englisch mit der Akkordschreibweise des Projekts.

- Die MIDI-Akkordspur bleibt bei enger Lage innerhalb einer Oktave. Drop-2 erhält die gewünschte Stimmverteilung und wird bei unpassender Lage im Exportstudio deaktiviert.

- Anfänger-Voicings spielen den notierten Slash-Bass. Die Reduktion erhält die verminderte Quinte von Septakkorden und zeigt die tatsächlich ausgelassenen Töne.

- Die Desktop-Transposition erhält die harmonischen Stufen und die Schreibweise der Slash-Bässe relativ zur Projekttonart.

- Der Harmonie-Inspektor zeigt die berechnete Stufe für den ausgewählten Akkord in der Projekttonart.

- Die Stufenanalyse berücksichtigt Grundtonschreibweise, Akkordqualität, Umkehrung und direkt folgende Ziele von Zwischendominanten. Der Next Chord Explorer trennt Grundtonbewegung von Auflösung und ergänzt Dur- und Mollvarianten von Jazz-ii–V–I.

- Der Harmonie-Inspektor zeigt nur Skalen, die sämtliche Akkordtöne und einen notierten Slash-Bass enthalten. Die Anfängeransicht zeigt die berechneten Bewegungen der rechten Hand mit Startton, Zielton und Halbtonabstand.

- Im Next Chord Explorer lassen sich zwei Kandidaten mit ihren Begründungen und Quellen vergleichen. Der Vergleich bleibt beim Wechsel der Oberflächensprache verfügbar.

- Das MIDI-Exportstudio zeigt überlappende Noteneinsätze auf derselben Tonhöhe und demselben Kanal an. Die Vorschau reagiert auf Voicing und Notenlänge und nennt den ersten betroffenen Tick.

- Das Akkordmenü dupliziert Ereignisse an ihrem Ende oder teilt sie in der Mitte. Beide Aktionen unterstützen Tastenkürzel in der Progressionsliste, Undo und Redo.

- Der Timing-Editor akzeptiert den Start in Takt, Zählzeit und Tick oder als absoluten Tickwert. Fehler markieren das betroffene Eingabefeld. Escape stellt die gültigen Werte wieder her.
- Rationale Zeitumrechnungen bleiben auch bei sehr großen Tickpositionen exakt.

- Bei großem Tonumfang passt das Stimmführungslabor den Abstand der Tonhöhenbeschriftungen an.
- Die Analyse der Anfänger-Voicings verwendet dynamische Programmierung. Damit lassen sich auch lange Akkordfolgen analysieren.
- Die Progressionsliste zeigt Start und Dauer je Akkord. Neue oder verschobene Akkorde bleiben sichtbar. Wahl- beziehungsweise Alt-Taste und Auf/Ab verschieben den gewählten Akkord. Beim Sprachwechsel bleiben Entwürfe und Scrollposition erhalten.

- Das Stimmführungslabor markiert das ausgewählte Akkordereignis in beiden Piano-Rolls. Die Auswahl erfolgt über das Ausklappfeld oder per Klick auf eine Note. Der gemeinsame Zeitzoom zeigt die Übersicht oder einen Ausschnitt auf der absoluten Tick-Achse.

- Das Stimmführungslabor zeigt pro Stil den MIDI-Tonumfang und pro Akkordwechsel die vorzeichenbehaftete Halbtonbewegung jeder vergleichbaren Stimme.

- Quellen und Freigabebelege des ausgewählten Bibliotheksbeispiels lassen sich über ein per Tastatur erreichbares Menü im Standardbrowser öffnen.

- Die Bibliothek zeigt Akkordkarten mit Referenztonart und harmonischen Stufen. Bleibt das Beispiel beim Filtern ausgewählt, bleibt auch die Leseposition in den Quellen- und Freigabedetails erhalten.

- Der Next Chord Explorer fokussiert die Kandidatenliste und zeigt den ersten Vorschlag. Pfeiltasten wechseln die Vorschau, Enter oder „Auswahl hinzufügen“ übernimmt den Akkord. Ein Wechsel der Oberflächensprache erhält die Auswahl im selben Projektkontext.

- Beim Öffnen und Speichern von Projekten erklärt STEPS typische Dateifehler auf Deutsch und Englisch. Die Sicherungswiederherstellung greift auch bei fehlerhafter UTF-8-Kodierung und nennt die verwendete Sicherung.

- Modale Desktop-Dialoge geben den Fokus nach dem Schließen zurück. Projektkürzel sind auf das Hauptfenster begrenzt.
- Bibliotheksvorschau und Stimmführungsdetails sind mit Tab erreichbar und seitenweise per Tastatur scrollbar. Die Schaltflächen des Stimmführungslabors behalten auch bei kleiner Fensterhöhe ihren Platz.

- Der MIDI-Dateidialog übernimmt den Projekttitel als Namensvorschlag und öffnet bei weiteren Exporten den zuletzt erfolgreich gewählten Ordner des Projekts.
- MIDI-Exporte ersetzen die Zieldatei erst nach einem vollständigen Schreibvorgang. Der Exportdialog zeigt lokalisierte Dateifehler und lässt einen erneuten Versuch zu.

- Der eigenständige Harmonie-Inspektor zeigt Grund- und Skalentöne in der Projektnotation. Tastaturvoicings für deutsche Vorzeichennamen bleiben auch nach der Akkordreduktion berechenbar.
- Bewegungswerte der Anfänger-Voicings und konkrete Stimmführungswarnungen stehen in EN/DE zur Verfügung. Didaktische Originalhinweise bleiben als solche sichtbar.

- Das MIDI-Exportstudio prüft jedes Voicing vor der Dateiauswahl und nennt den ersten Akkord, der einen Modus blockiert.
- Die Progressionsbibliothek verknüpft Suchbegriffe aus Akkorden, Titeln und Quellen. Eine weiterhin sichtbare Auswahl bleibt beim Ändern der Suche erhalten. Katalogfehler erscheinen vor der Speicherrückfrage.
- Die geprüfte Bibliothek zeigt und lädt transponierte Übungskopien in INT oder DE. Die Originalfassung mit Quellen und Freigaben bleibt sichtbar.

- Der Next Chord Explorer bewahrt die Akkordauswahl auf Aqua, zeigt lokalisierte Beziehungen samt Provenienz und verhindert die Übernahme überholter Empfehlungen.
- Die Python-API für Drums, Piano und Bass weist kreative Ideen und prüfpflichtige Forschungsbezüge aus. Aufrufer erhalten für `confidence` künftig `None`.
- Das Stimmführungslabor zeigt zwei Stilprofile mit vergleichbaren Piano-Rolls, Bassverlauf und Übergangsmetriken.
- Der ausgewählte Übergang steht in beiden Vorschauen oben. Das Labor zeigt seine tiefsten MIDI-Noten und die kumulierte Bewegung bis zum Folgeakkord.
- Das Werkzeugmenü, besser lesbare Aqua-Schaltflächen und die Tastaturvorschau verbessern den Desktop-Ablauf. Ein lokales macOS-App-Bundle enthält Branding, Kataloge und das Quellenregister. Der Wheel-Smoke prüft jetzt auch die installierte Bibliothek.

- Das lokalisierte MIDI-Exportstudio bietet die ADR-017-Optionen für Voicing, Notendauer und SMF-Format; die bisherigen CLOSE-/10-Tick-/Format-1-Defaults und der unveränderte Projektzustand bleiben erhalten.
- Die Desktop-Progressionsbibliothek bietet Suche und Vorschau für die drei freigegebenen Beispiele, einschließlich unveränderter Claim-Texte und ihrer Quellen-/Reviewbelege. Das Laden beginnt erst nach Auswahl und verwendet weiterhin die Dirty-State-Rückfrage; neue Claims oder Übersetzungsfreigaben entstehen nicht.
- Der Next-Chord-Explorer aktiviert das Übernehmen jetzt erst nach einer gültigen Kandidatenauswahl; fehlende oder veraltete Auswahlen bleiben sichtbar abgewiesen.
- Das Desktop-Stimmführungslabor vergleicht die vorhandenen Stilprofile anhand kumulierter absoluter MIDI-Bewegung und erkannter Warnungen, ohne den Projektstil zu ändern. Erst „Stil verwenden“ ändert den undo-/redo-fähigen Projektwert; Bewegungswerte sind keine universelle Rangfolge.
- Der Projekt-MIDI-Export ignoriert Text in Anmerkungsspuren und weist ungültige Akkordsymbole oder MIDI-Noten zurück, statt Events still zu überspringen.
- Fehler beim Anwenden des optionalen App-Symbols werden protokolliert, ohne den Desktop-Start abzubrechen.
- Die Desktop-Akkordanalyse schlägt nur registrierte Skalen vor und zeigt Fehler bei der Berechnung gültiger Kandidaten an, statt sie still zu verwerfen.
- Fehler im optionalen Anfänger-Voicing-Viewmodel werden protokolliert, ohne die übrige Akkordanalyse zu verwerfen.
- Fehler einer Desktop-Session-Listener-Aktualisierung werden protokolliert, ohne weitere Listener-Updates zu unterbrechen.
- **Verhaltensänderung:** `NoteSpelling.transpose_diatonic` löst bei Stufen- und Halbtonwerten, die kein Intervall bilden, `InvalidAlterationError` aus, statt still die Oktave zu verschieben (zuvor C4 `(0, 11)` → Cb5). Gültige Intervalle sind unverändert.
- **Verhaltensänderung:** `knowledge/research/run_golden_test_suite.py` schreibt ohne Argumente keine Dateien mehr; `--output-dir` exportiert, `--update-baseline` erneuert die versionierten Berichte.
- Entscheidungen ADR-001, 003, 004, 006, 007 und 013–017 angenommen (v0.1 = Akkorde + MIDI-Export, Lizenz MPL-2.0/CC BY 4.0); siehe [Register](decisions/DECISION_REGISTER.md). Der MIDI-Export ist im Kern und in den Prototyp-Pfaden implementiert und Bestandteil des v0.1.0-Releases; externe DAW-Abnahme und vollständiger Desktop-Produktablauf bleiben getrennte Nachweise.
- Tonhöhen, Intervalle, Akkordauflösung, Stufenparser und Stimmführung sind als Python-Schnittstellen verfügbar.
- Dur- und Moll-Aliasse mit `M` und `m` werden unterschieden. Unlösbare Voicing-Vorgaben melden einen Fehler.
- App-Adapter und Lernmaterial verwenden dieselbe kuratierte Progressionsdatei.
- Logo und App-Symbol liegen als [Master](design/brand/README.md) im Repository. `app.brand` stellt sie der App zentral bereit, die Root-README zeigt das App-Symbol.
- Die Root-README ist als Projektseite neu gegliedert und erscheint auf der GitHub-Startseite. Die frühere `.github/README.md` heißt jetzt [`GITHUB_UND_CI.md`](.github/GITHUB_UND_CI.md).
- Der [Implementierungsstand](docs/IMPLEMENTATION.md) und die [generierte API-Referenz](docs/theory/API.md) beschreiben den Entwicklungsstand und die verfügbaren Funktionen.
- 1.0.0-Zielbild, Ist-Stand und offene Freigabegates konsolidiert; Produkt- und GitHub-Dokumentation gegen den aktuellen Stand ergänzt.
- Der Desktop-Prototyp ergänzt projektbezogenes Öffnen/Speichern mit Dateiauswahl, Rückfrage bei ungespeicherten Änderungen und sichtbaren Fehlern. Session-Dateien bewahren Tonart und Mollmodus; fehlerhafte Akkordsymbole werden vor einem Zustandswechsel abgewiesen.
- Der Desktop-Prototyp bietet einen persistierten Sprachschalter für Englisch/Deutsch/System, lokalisierte Desktop- und CLI-Texte sowie eine MIDI-Dateiauswahl mit sichtbarem Exportfehler. Notationskonvention und Projektdaten bleiben unabhängig von der UI-Sprache; native Plattform- und Übersetzungsabnahme stehen aus.
- Die Oberfläche verbindet Akkord-Ändern/Entfernen/Verschieben und Undo/Redo mit der Progressionssession. Ungültige Akkorde und das Entfernen des letzten Akkords werden mit lokalisierten Hinweisen abgewiesen; Tastenkürzel sind unter Windows/Linux und macOS verfügbar.
- Tonart, Dur-/Mollmodus, Tempo und Taktart können gemeinsam im Desktop gesetzt und als eine Session-Änderung rückgängig gemacht werden. Eingaben werden validiert und in Projekten sowie MIDI-Metadaten gespeichert. Pro Akkordereignis lässt sich die Startposition als `Takt:Zählzeit:Tick` eingeben; Dauer und gespeicherter/exportierter Zeitpunkt bleiben absolute Tickwerte. Ein Taktartwechsel ändert nur die Positionsprojektion, nicht die Ereigniszeit.
- Beim Öffnen eines beschädigten Projekts meldet die Desktop-Oberfläche jetzt EN/DE lokalisiert, dass ein gültiges Backup geladen wurde. Die Storage-API liefert parallel einen kompatiblen Load-Status mit Backup-Pfad; bestehende `load_project()`-Aufrufe behalten ihren Rückgabewert.
- Projektdateien werden über einen expliziten 0.x→1.0.0-Migrationspfad und dokumentierte 1.x-Normalisierungen geladen. Zukunftsschemas mit höherer Major-Version werden weiterhin abgewiesen. Der Load-Status nennt die angewendeten Migration-IDs; fehlende Projekttitel bleiben ein Fehler statt still aufgefüllt zu werden.
- Beim Öffnen eines migrierten Legacy-Projekts zeigt die Desktop-Oberfläche eine lokalisierte EN/DE-Meldung mit den angewendeten Migration-IDs. Die Meldung unterscheidet Projektwiederherstellung aus einem Backup von Schema-Normalisierung.
- Ungültige oder außerhalb des Schemas liegende Werte in Projekt-Zeiteinstellungen werden beim Laden unter der bestehenden Migration `MIG-006 normalize-time-settings` auf dokumentierte sichere Standardwerte normalisiert. Der Quellstatus und die Projekt-Schema-ID bleiben unverändert; ein automatisierter Regressionstest deckt PPQ, Taktart, Tempo und Tempo-Punkte ab.
- Die kanonische Implementierungs- und Changelog-Dokumentation wurde auf den Merge-Stand von PR #190 und MIG-006 abgestimmt. PR #191 hielt die Statussynchronisation zusammen mit dem unveränderlichen Baseline-Nachweis auf dem damaligen Stand fest: die vollständige Suite bestand bei Commit `93ab98960a484adc9e7cf8f3927e9c81b157d5e9` aus 747 Tests.
- Der Projektname lässt sich in der Desktop-Oberfläche editieren und wird gemeinsam mit Tonart, Mollmodus, Tempo und Taktart als eine undo-/redo-fähige Kontextaktion gespeichert.
- Die Desktop-Dateiaktionen bieten jetzt „Neu“ mit `Ctrl+N`/`⌘N`, Dirty-State-Rückfrage und sauberem Wechsel auf eine neue Standard-Progression ohne die Historie des vorherigen Projekts.
- Der vorgeschlagene Save-As-Dateiname wird jetzt plattformübergreifend bereinigt (ungültige Zeichen, Windows-Gerätenamen und leere Namen).
- Der Desktop-Kontext bietet eine eigenständige, bestätigte Auswahl der musikalischen Notationskonvention (`INT`/`DE`). Die Umstellung konvertiert Tonart und Akkordsymbole explizit und lässt Ticks, Tempo, Taktart und Projektstruktur unverändert.
- Dokumentationssnapshots werden jetzt über eine wiederholbare Konsistenzprüfung abgesichert, die Commit-Belege validiert, ohne jeden neuen Merge-SHA automatisch nachzuführen.
- Neue versionierbare GitHub-Community-Vorarbeiten decken Discussion-Forms, Wiki-, Project- und Funding-Owner-Actions ab; keine Live-Veröffentlichung oder fremde Kontoanlage erfolgt dadurch.
- Ein reproduzierbares DAW-Importprotokoll trennt automatische SMF-Roundtrip-Belege ausdrücklich von menschlicher Independent-DAW-Abnahme.
- Die CI ergänzt macOS-/Windows-Matrix-Smokes für denselben Tkinter-Widget-/Controller-Pfad; native menschliche Plattform- und Accessibility-Abnahmen bleiben ausdrücklich offen.
- Der Desktop-Informationsbereich zeigt jetzt die bestehende Beginner-Keyboard-Voicing-Ermittlung mit linker/rechter Hand, Fingerempfehlungen und Stimmführungsübergängen in Englisch und Deutsch.
- Das Python-Wheel enthält jetzt die Desktop-App, Locale-Kataloge, Design-Tokens und Markenressourcen, damit der konfigurierte `steps`-Einstieg und seine Laufzeitressourcen gemeinsam installiert werden.
- Der Desktop-Nächster-Akkord-Explorer liefert Kontext-/Relationsempfehlungen aus der Progressionssession und setzt ausgewählte Kandidaten als lokale Desktop-Aktion.
- Die Desktop-Dateiaktionen können eine freigegebene Progression aus dem lokalen Reviewed-Beispielkatalog als neues Projekt laden, mit Dirty- und Katalogfehlerbehandlung.
- Die Desktop-Sitzung und das Hauptfenster bieten einen getrennten, persistierten Stimmführungsstil für klassische, Jazz-/Pop- und zeitgenössische Kontexte; Auswahl und Zusammenfassung werden undo-/redo-fähig wiederverwendet.
- Der kanonische Implementierungsstand wurde auf `main`-Commit `b09946f18db6668ce628159b4c2e3e3be2968213` synchronisiert. PRs #197–#200 sind gemergt; die vollständige Suite bestand bei diesem Implementierungsstand aus 758 automatisierten Tests.
- PR #201 synchronisierte die aktive Statusdokumentation auf den dokumentierten Merge-Stand `961701ead06b703653a9cc9ff2e38d2450d056d7`.
- GitHub Issue- und PR-Vorlagen, Dependabot-/Release-Notizkonfiguration und ein YAML-/Issue-Form-Prüfworkflow ergänzt. GitHub-Wiki, Projects, Labels und Funding bleiben explizite Inhaberhandlungen.
- Der Desktop-Sessionexport folgt jetzt ADR-017: genau vier CLOSE-Stimmen (Dreiklänge mit Grundtonverdopplung; Erweiterungen mit Grundton, Terz, Septime und höchster Erweiterung) in der Akkordspur, separate Bassspur, passendes Tonart-Metadatum und gespeicherte Event-Zeiten. Der Exportservice bietet zusätzlich DROP2/ROOTLESS, 95%-Notenlänge und SMF Format 0. Zehn SHA-256-Goldenfälle und ein UI-Save/Open/Export-Smoke prüfen den Ablauf; DAW-Abnahme bleibt separat.
- PR #206 prüft die zehn ADR-017-Goldenexporte zusätzlich durch erneutes Parsen mit `SMFParser`; dies belegt die interne Dateistruktur, nicht den Import in eine unabhängige DAW.
- Das kanonische STEPS-Aufgabenregister wird nach Owner-Entscheidung versioniert unter `docs/operations/OFFENE_ARBEITSAUFFORDERUNGEN.md` geführt, analog zum einzelnen Entwicklungsplan in Glide. Der externe Masterpfad wird nicht mehr vorausgesetzt; historische OA-IDs bleiben bis zur Evidenzprüfung unverändert.
- Tk-Smoke-Jobs für Ubuntu/Xvfb, Windows und macOS schlagen jetzt fehl, wenn Tk nicht initialisiert werden kann, statt den GUI-Test unbemerkt zu überspringen. Das belegt keine menschliche Accessibility- oder Plattformfreigabe.

## Frühere Architekturvorbereitung

- Zielstruktur für App, Domäne, Wissensbasis, Forschung, Design, Entscheidungen und Tests beschrieben.
- Konservative, auditierbare Migration vorbereitet; **keine Aussage über fertigen App-Code**.
- Historische Wissensbibliothek wird als Legacy-Facharchiv abgegrenzt.

> Dieser Abschnitt dokumentiert die frühere Strukturvorbereitung.
