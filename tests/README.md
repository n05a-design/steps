# Tests und Prüfbefehle

Aus dem Repository-Root mit Python 3.11 oder 3.12 ausführen.

| Prüfung | Befehl | Aussage |
|---|---|---|
| Kern-Suite | `python -B -m unittest discover -s tests -p 'test_*.py' -v` | Theorie- und Progressionscode, kuratierte Daten, unabhängiger Golden-Evaluator, Referenzintegrität, Secret-Scanner und Projektstruktur |
| Curation-Suite | `python -B -m unittest discover -s .agents/skills/steps-knowledge-curation/tests -v` | Hilfsskripte und isolierte Abläufe mit temporären Registern. |
| Referenzidentität | `python -B scripts/verify_reference_integrity.py` | Prüft geschützte Referenzdateien und Inhalte gegen die hinterlegte Baseline. |
| Lernmaterial | `python -B scripts/render_reviewed_progressions.py --check` | Prüft Quellen, die menschlichen Freigaben der konkreten Fassungen und den generierten Text. Vor Abschluss der Pilotabnahme blockiert diese Prüfung. |
| API-Dokumentation | `python -B scripts/render_api_reference.py --check` | Prüft die generierten API-Exporte, Akkordqualitäten und Versionen gegen den Code. |

[GitHub Actions](../.github/workflows/python-tests.yml) führt die Kern- und
Curation-Suiten sowie den API-Abgleich auf Ubuntu mit beiden Python-Versionen
aus. Ein separater CI-Job prüft die Veröffentlichung des Pilotmaterials.
Die Kern-Suite prüft die Veröffentlichungspfade mit isolierten synthetischen
Freigaben. Damit werden keine Desktop-, Audio- oder Produkt-MIDI-Abläufe abgenommen.

Die [Golden-Datendatei](golden_cases/golden_reference_cases.json) enthält 198
Fälle. Davon werden 67 vom unabhängigen Referenz-Evaluator berechnet und 131
als Spezifikationsbeispiele geführt. Der Golden-Check testet den
Referenz-Evaluator. Die [produktiven Theory-Tests](test_theory_core.py) prüfen
die Laufzeitfunktionen direkt, darunter die Frequenzberechnung. Die
[Progressionstests](test_progression_engine.py) prüfen unter anderem
Stufenauflösung und Voicing-Grenzfälle. [Katalog- und App-Tests](test_reviewed_progressions.py)
prüfen Tonklassen, Bass und MIDI-Grenzen in 336 Standardfällen
(28 Bestandsprogressionen in je 12 Transpositionen).
