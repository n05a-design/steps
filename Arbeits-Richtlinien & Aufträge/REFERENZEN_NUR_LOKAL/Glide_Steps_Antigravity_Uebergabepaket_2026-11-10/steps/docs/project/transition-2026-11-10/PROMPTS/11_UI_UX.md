# P11 – UI/UX für zwei musikalische Arbeitsflächen

## Direkt nutzbarer Prompt

Du bist UI-Architekt und UX-Researcher für Steps. Priorität ist **ein vollständiger Chord+Drum-Workflow**, nicht eine detailgenaue Kopie sämtlicher Glide-Ansichten. Lies Glide `docs/DESIGN_RICHTLINIEN.md`, die bewährten Navigations-/Theme-/Fokusverträge, das Steps-PRD und den dokumentierten tatsächlichen Window-Host. Differenziere **native Fenster** von zwei Content-Panes/Arbeitsbereichen.

Erstelle ein Content-/Navigation-Modell: links umschaltbare Seitenliste mit modularen Navigationseinträgen und Zuständen, rechts bzw. innerhalb der zwei Hostflächen editierbarer Akkord-/Drum-Editor und ergänzende Hilfe/Inspector/Knowledge-Fläche je vereinbarter Fenstersemantik. Erhalte Ein-/Ausblenden und Einklappen der Sidebar, Titelleiste, Logo-Platz, Symbolbuttons, Suche/Input, Settings, Theme- und Schriftrollen, Tastaturbedienung, Scroll/Fokus und Lebenszyklus. Produktneutrale UI-Komponenten referenzieren semantische Tokens statt Glide-Konstanten.

Definiere: BPM/Taktart/Tonart/Notation, Chord-Lanes, Drum-Grid und Velocity, Auswahl/Undo/Redo, Copy/Paste, Speicherung, MIDI-Export, Fehl- und Leerzustände, Zoom/Fokus, Tooltips, Erkenntniskarten sowie Themes für Light/Dark/High Contrast. Keyboard-Golden-Flows, Screenreader-Alternativen für Grid, motorische Bedienbarkeit, native DPI-/Mehrmonitor-Matrix; Tk-spezifische Einschränkungen ehrlich dokumentieren.

Erstelle zuerst Wireframes und Ablaufdiagramme plus priorisierte Usability-Fälle; baue **nur den schmalen, testbaren UI-Vertikalschnitt** nach bestätigtem Shell-Vertrag. Fremde konkurrierende Screenshots nicht blind übernehmen; eigenständige Marke. Vergleiche messbar mit ursprünglicher Glide-Shell, ohne frühere Glide-Tests als Steps-Tests zu zählen.

## Akzeptanz

Zwei klar definierte Hostbereiche; Navigation/Sidebar vollständig bedienbar; eine simulierte chord-to-drum Nutzerreise mit echten Datenmodellen und Save-Mock; Accessibility-Matrix; keine Behauptung native Abnahme, wenn nicht durchgeführt.
