# app

Desktop-Start, GUI-Komposition und Plattformintegration. Keine doppelte Musiktheorie-Engine. Ein `__main__.py` entsteht erst mit einer ausführbaren Implementierung.

**Stand:** Struktur vorbereitet; Inhalte/Implementierung sind nur dann vorhanden, wenn hier tatsächlich weitere Dateien hinzugefügt wurden. Keine Produktfreigabe ableiten.

`app.knowledge.list_reviewed_progressions()` liefert die geprüften
Beispiele mit Lerntext und Quellen-IDs. Ein Einzelbeispiel lässt sich mit
`get_reviewed_progression("PROG-003")` laden. Dessen `progression` kann
direkt an `src.steps.progression.generate_progression_voicings` übergeben
werden.
