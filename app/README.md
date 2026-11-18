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

[`app.brand`](brand.py) ist der zentrale Zugriff auf Logo und App-Symbol.
`apply_window_icon(root)` setzt das Symbol eines Tk-Fensters und seiner
Dialoge. `logo_path(size)`, `app_icon_path(size)` und `app_icon_ico_path()`
liefern die Dateien aus [assets](assets/README.md). Quelle sind die
[Logo-Master](../design/brand/README.md).

Desktop-Start, Oberfläche und Plattformintegration sind Ziel dieser Schicht.
Der [Implementierungsstand](../docs/IMPLEMENTATION.md) beschreibt den
vorhandenen Kern und die Grenzen der App-Schnittstelle.

Die Progressionsoberfläche kann Akkorde hinzufügen, den ausgewählten Akkord
ändern, entfernen und innerhalb der Progression verschieben sowie Änderungen
rückgängig machen bzw. wiederholen.
Ungültige Akkorde und der Versuch, den letzten Akkord zu entfernen, werden
sichtbar abgewiesen. Die Bedienfelder und Fehlermeldungen folgen der gewählten
UI-Sprache.

Tonart, Dur-/Mollmodus, Tempo und Taktart lassen sich gemeinsam als musikalischer
Kontext ändern; die Eingabe wird als eine undo-fähige Aktion gespeichert. Die
Taktart wird im Format Zähler/Nenner eingegeben (z. B. `3/4` oder `6/8`) und in
Projektdatei und MIDI-Metadaten übernommen. Sie ändert nicht automatisch die
Tick-Dauer der Akkord-Events; einzelne Startzeiten und Dauern sind noch nicht
in der Oberfläche editierbar.

Die UI-Sprache unterstützt Englisch und Deutsch unabhängig von musikalischer
Notation. Die Auswahl `system`, `en` oder `de` wird als Benutzereinstellung
gespeichert; `--language` überschreibt sie nur für den aktuellen CLI-Lauf.
Übersetzungskataloge liegen unter [locales](locales/). Fachliche Lerninhalte
werden dadurch nicht automatisch übersetzt; ihre Sprachfassungen benötigen
eigene fachliche und sprachliche Reviews.

| Ordner | Zuständigkeit |
| --- | --- |
| [core](core/README.md) | App-Start und Zusammensetzung der Komponenten. |
| [ui](ui/README.md) | Ansichten, Navigation und Interaktion. |
| [adapters](adapters/README.md) | Betriebssystem- und Integrationsgrenzen. |
| [audio](audio/README.md) | Geplante Audio- und MIDI-Anbindung. |
| [assets](assets/README.md) | Logo, App-Symbol und Windows-Symbol. |

Für Berechnungen und Fachmodelle ist der [Python-Kern](../src/steps/README.md)
zuständig. [Adapter-Tests](../tests/test_reviewed_progressions.py) prüfen die
vorhandene Wissensschnittstelle, [Markentests](../tests/test_brand_assets.py)
die Logo-Dateien und ihren Zugriff.
