# Fach- und Quellenschemata

Die JSON-Schema-Entwürfe beschreiben Datenaustausch und Dokumentation.

| Einstieg | Inhalt |
| --- | --- |
| [Quelle](source.schema.json) | Quelleneinträge und Nutzungsrahmen. |
| [Konzept](concept.schema.json) | Fachkonzepte und Bezüge. |
| [Akkord](chord.schema.json) | Akkorddarstellung. |
| [Progression](progression.schema.json) | Akkordfolgen. |
| [Analyse](analysis.schema.json) | Analyseergebnisse. |

Die [Strukturprüfung](../tools/validation/check_structure.py) prüft JSON-Syntax und ausgewählte Schema-Merkmale. Der [Pilot-Loader](../src/steps/progression/reviewed.py) validiert das eigene Laufzeitformat für Lernmaterial.

[Zur Bereichsübersicht](../README.md)
