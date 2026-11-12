# Datenschemata

Hier liegen die JSON-Schema-Entwürfe für [Quellen](source.schema.json), [Konzepte](concept.schema.json), [Akkorde](chord.schema.json), [Progressionen](progression.schema.json) und [Analyseergebnisse](analysis.schema.json). Die [Strukturprüfung](../tools/validation/check_structure.py) liest die Dateien als JSON und prüft Schema-Draft und Pflichtfelder. Das App-Lernmaterial hat ein separates, vom [Loader](../src/steps/progression/engine.py) geprüftes JSON-Format.
