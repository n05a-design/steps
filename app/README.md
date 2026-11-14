# App-Schicht

[`app.knowledge`](knowledge.py) ist der Python-Adapter für die drei
[Pilotbeispiele](../knowledge/concepts/progressions/README.md).
Nach vollständiger menschlicher Abnahme liefert
`list_reviewed_progressions()` die freigegebenen Beispiele.
`get_reviewed_progression("PROG-003")` liefert das Einzelbeispiel
mit Aussagen, Freigabedaten und Datenversion. Sein Feld `progression` kann
an `src.steps.progression.generate_progression_voicings` übergeben werden.
Bei fehlenden oder veralteten Freigaben meldet die Schnittstelle
`PublicationError`, einen Untertyp von `ProgressionParsingError`.

Desktop-Start, Oberfläche und Plattformintegration sind Ziel dieser Schicht.
Der [Implementierungsstand](../docs/IMPLEMENTATION.md) beschreibt den
vorhandenen Kern und die Grenzen der App-Schnittstelle.

| Ordner | Zuständigkeit |
| --- | --- |
| [core](core/README.md) | App-Start und Zusammensetzung der Komponenten. |
| [ui](ui/README.md) | Ansichten, Navigation und Interaktion. |
| [adapters](adapters/README.md) | Betriebssystem- und Integrationsgrenzen. |
| [audio](audio/README.md) | Geplante Audio- und MIDI-Anbindung. |

Für Berechnungen und Fachmodelle ist der [Python-Kern](../src/steps/README.md)
zuständig. [Adapter-Tests](../tests/test_reviewed_progressions.py) prüfen die
vorhandene Wissensschnittstelle.
