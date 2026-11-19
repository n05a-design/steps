# Native UI und Bedienbarkeit

Dieser Ordner dokumentiert den vorgesehenen Testbereich. Eine native Desktop-Suite steht mit der Desktop-Implementierung aus.

Der Ubuntu-CI-Smoke startet Tkinter unter Xvfb und prüft Fenster-Initialisierung,
Progression, Kontextänderung, Undo, Akkordbearbeitung, Transposition und MIDI-
Export über die native Widget-Verkabelung. Das ersetzt keine menschliche
macOS-/Windows-/Linux-Sichtprüfung, Screenreader-Abnahme oder native Dialog-
Akzeptanz.
Zusätzliche macOS-/Windows-Matrix-Jobs starten denselben Widget-/Controller-
Pfad auf den jeweiligen Hosted Runnern. Ein Skip wegen fehlendem Tkinter oder
Display bleibt ein nicht bestätigter Plattformfall, kein automatischer
Plattformfreigabe-Nachweis.

| Einstieg | Inhalt |
| --- | --- |
| [App-UI](../../app/ui/README.md) | Implementierungsgrenze und Zielstruktur. |
| [Qualitätsgates](../../docs/quality/QUALITY_GATES.md) | Kriterien für Plattform- und Bedienabnahme. |

[Zur Bereichsübersicht](../README.md)
