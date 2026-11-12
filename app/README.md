# App-Schicht

[`app.knowledge`](knowledge.py) ist der Python-Adapter für die einzeln
geprüften Lernbeispiele. `list_reviewed_progressions()` liefert alle Einträge
und `get_reviewed_progression("PROG-003")` liefert das einzelne Beispiel.
Sein Feld `progression` kann an
`src.steps.progression.generate_progression_voicings` übergeben werden.

Desktop-Start, Oberfläche und Plattformintegration sind Ziel dieser Schicht.
Der [Implementierungsstand](../docs/IMPLEMENTATION.md) beschreibt den
vorhandenen Kern und die Grenzen der App-Schnittstelle.
