# Golden-Master

Die JSON-Datei ist der kanonische Golden-Bestand. Der Testspiegel wird aus diesem Master synchronisiert.

| Einstieg | Inhalt |
| --- | --- |
| [Golden-Master](golden_reference_cases.json) | Fall-ID, Eingaben, Sollwerte, Kontext und Testklasse. |
| [Datenvertrag](../GOLDEN_DATA_SOURCE_OF_TRUTH.md) | Herkunft und geschützte Identität. |
| [Testspiegel](../../../tests/golden_cases/README.md) | Synchronisierung und Auswertung. |

Vor einer Korrektur den Fall fachlich belegen und die erforderliche Migration erfassen. Danach aus dem Repository-Root `python -B scripts/build_unified_golden_cases.py --check` ausführen.

[Zur Bereichsübersicht](../README.md)
