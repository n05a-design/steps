# Progressionen und Stimmführung

Das Paket löst römische Stufen in einem angegebenen Tonartkontext auf und erzeugt Voicings für Akkordfolgen.

| Einstieg | Inhalt |
| --- | --- |
| [engine.py](engine.py) | Bestandskatalog, Stufenauflösung, Transposition und Voicing-Ablauf. |
| [voice_leading.py](voice_leading.py) | Distanz, Stimmenanalyse, Stilprofile und Solver. |
| [reviewed.py](reviewed.py) | Lädt den Pilotkatalog und validiert Quellenreferenzen sowie fassungsgebundene Freigaben. |
| [Pilotdaten](reviewed_progressions.json) | Fachliche Aussagen und Beispieldefinitionen für App und Renderer. |
| [Pilotfreigaben](reviewed_progression_approvals.json) | Nachweisreferenzen für die konkreten Datensätze. |

Katalogänderungen mit [Progressionstests](../../../tests/test_progression_engine.py) prüfen. Änderungen am Lernmaterial folgen dem [Freigabeablauf](../../../knowledge/concepts/progressions/README.md).

[Zur Bereichsübersicht](../README.md)
