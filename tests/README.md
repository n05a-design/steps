# Tests und Prüfbefehle

Aus dem Repository-Root mit einer Python-Version aus der CI-Matrix 3.11 bis 3.14 ausführen.

| Prüfung | Befehl | Aussage |
|---|---|---|
| Kern-Suite | `python -B -m unittest discover -s tests -p 'test_*.py' -v` | Theorie- und Progressionscode, kuratierte Daten, unabhängiger Golden-Evaluator, Referenzintegrität, Secret-Scanner und Projektstruktur |
| Curation-Suite | `python -B -m unittest discover -s .agents/skills/steps-knowledge-curation/tests -v` | Hilfsskripte und isolierte Abläufe mit temporären Registern. |
| Referenzidentität | `python -B scripts/verify_reference_integrity.py` | Prüft geschützte Referenzdateien und Inhalte gegen die hinterlegte Baseline. |
| Lernmaterial | `python -B scripts/render_reviewed_progressions.py --check` | Prüft Quellen, die menschlichen Freigaben der konkreten Fassungen und den generierten Text. Vor Abschluss der Pilotabnahme blockiert diese Prüfung. |
| API-Dokumentation | `python -B scripts/render_api_reference.py --check` | Prüft die generierten API-Exporte, Akkordqualitäten und Versionen gegen den Code. |

[GitHub Actions](../.github/workflows/python-tests.yml) führt die Kern- und
Curation-Suiten sowie den API-Abgleich auf Ubuntu mit Python 3.11, 3.12, 3.13 und 3.14
aus. Weitere Jobs prüfen den Skill auf macOS und Windows, die Wissensabdeckung
und die Veröffentlichung des Pilotmaterials.
Die Kern-Suite prüft die Veröffentlichungspfade mit isolierten synthetischen
Freigaben. Damit werden keine Desktop-, Audio- oder Produkt-MIDI-Abläufe abgenommen.

Die [Golden-Datendatei](golden_cases/README.md) enthält 198
Fälle. Davon werden 98 ausgeführt und 100 strukturell als
Spezifikationsbeispiele geprüft. Der Golden-Check testet den
Referenz-Evaluator. Die [produktiven Theory-Tests](test_theory_core.py) prüfen
die Laufzeitfunktionen direkt, darunter die Frequenzberechnung. Die
[Progressionstests](test_progression_engine.py) prüfen unter anderem
Stufenauflösung und Voicing-Grenzfälle. [Katalog- und App-Tests](test_reviewed_progressions.py)
prüfen Tonklassen, Bass und MIDI-Grenzen in 336 Standardfällen
(28 Bestandsprogressionen in je 12 Transpositionen).

## Testmodule und Ablage

| Ordner | Inhalt |
| --- | --- |
| [Theorie](theory/README.md) · [Akkorde](chords/README.md) · [Enharmonik](enharmonics/README.md) | Wegweiser zu den ausführbaren Root-Testmodulen. |
| [Progressionen](progressions/README.md) · [Transposition](transposition/README.md) | Stufen-, Voicing- und Transpositionsproben. |
| [Integration](integration/README.md) · [Native UI](native_ui/README.md) | Vorhandene Integrationsproben und geplante Desktop-Abnahme. |
| [Fixtures](fixtures/README.md) · [Golden-Spiegel](golden_cases/README.md) | Synthetische Eingaben und Referenzfälle. |

Die Wissensabdeckung und die fachlichen Restabnahmen stehen im
[Benchmark](../knowledge/benchmark/README.md).
