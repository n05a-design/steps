# Golden-Testspiegel

Die JSON-Datei spiegelt den kanonischen Golden-Master bytegleich. Änderungen beginnen im Master.

| Einstieg | Inhalt |
| --- | --- |
| [Spiegel](golden_reference_cases.json) | Fixture für den Golden-Evaluator. |
| [Master](../../knowledge/research/golden_cases/README.md) | Kanonischer Datenbestand. |
| [Evaluator](../test_golden_reference_cases.py) | Berechnet Sollfälle oder prüft Spezifikationsbeispiele strukturell. |

Aus dem Root `python -B scripts/build_unified_golden_cases.py --check` ausführen. Ohne `--check` synchronisiert das Skript den Spiegel.

[Zur Bereichsübersicht](../README.md)
