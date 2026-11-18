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
Tick-Dauer der Akkord-Events. Für den ausgewählten Akkord lassen sich absolute
Startzeit als `Takt:Zählzeit:Tick` und Dauer in Ticks bearbeiten; die Feldbeschriftung
zeigt die Projektauflösung (PPQ). Takt und Zählzeit beginnen bei 1; der Tickwert
ist der nullbasierte Versatz innerhalb einer Zählzeit der Taktart (in `6/8` also
innerhalb einer Achtelnote). Die Position ist eine Anzeige/Eingabeprojektion;
gespeichert und exportiert werden weiterhin absolute Start-Ticks. Ein Taktartwechsel
ändert deshalb die Anzeige, nicht den Ereigniszeitpunkt. Zeitlücken und
Überlappungen bleiben ausdrückliche Tick-Werte und werden nicht aus der
Progressionsreihenfolge oder Taktart abgeleitet.
Wenn beim Öffnen die Hauptdatei beschädigt ist, versucht die Storage-Schicht
eine Wiederherstellung aus dem neuesten gültigen Backup. Die Desktop-Oberfläche
zeigt in diesem Fall eine EN/DE-lokalisierte Rückmeldung. `load_project()` bleibt
API-kompatibel; `load_project_with_status()` ergänzt für Prüf- und Integrationspfade
Projekt sowie Wiederherstellungsstatus.
Legacy-Projekte bis zur aktuellen 1.x-Schemafassung werden konservativ über
den dokumentierten Migrationspfad normalisiert. Höhere Major-Versionen werden
abgewiesen; ein fehlender Projektname bleibt ein korruptes Projekt und wird nicht
still erfunden.
Wird beim Öffnen ein Legacy-Schema normalisiert, zeigt die Desktop-Oberfläche
eine separate, lokalisierte EN/DE-Meldung mit den angewendeten Migration-IDs.
Beim Laden aus einem Backup bleibt die Backup-Rückmeldung vorrangig.
Der Projektname ist in der Desktop-Oberfläche editierbar. Die Eingabe wird zusammen
mit Tonart, Modus, Tempo und Taktart atomisch angewendet und rückgängig gemacht;
ein leerer Name wird sichtbar abgewiesen.

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
