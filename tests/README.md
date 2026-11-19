# Tests und Prüfbefehle

Aus dem Repository-Root mit einer Python-Version aus der CI-Matrix 3.11 bis 3.14 ausführen.

| Prüfung | Befehl | Aussage |
|---|---|---|
| Kern-Suite | `python -B -m unittest discover -s tests -p 'test_*.py' -v` | Theorie- und Progressionscode, kuratierte Daten, unabhängiger Golden-Evaluator, Referenzintegrität, Secret-Scanner und Projektstruktur |
| Curation-Suite | `python -B -m unittest discover -s .agents/skills/steps-knowledge-curation/tests -v` | Hilfsskripte und isolierte Abläufe mit temporären Registern. |
| Referenzidentität | `python -B scripts/verify_reference_integrity.py` | Prüft geschützte Referenzdateien und Inhalte gegen die hinterlegte Baseline. |
| Lernmaterial | `python -B scripts/render_reviewed_progressions.py --check` | Prüft Quellen, die menschlichen Freigaben der konkreten Fassungen und den generierten Text. Vor Abschluss der Pilotabnahme blockiert diese Prüfung. |
| API-Dokumentation | `python -B scripts/render_api_reference.py --check` | Prüft die generierten API-Exporte, Akkordqualitäten und Versionen gegen den Code. |
| Logo und App-Symbol | `python -B scripts/build_brand_assets.py --check` | Prüft die SHA-256 der SVG-Master und die Bildpunkte der abgeleiteten PNG- und ICO-Dateien. Die Kern-Suite führt denselben Vergleich aus. |
| Python-Wheel-Artefakt | `python -B -m unittest tests.test_package_artifacts -v` | Baut ein temporäres Wheel, prüft den `steps`-Entrypoint sowie EN/DE-Kataloge und Brand-Ressourcen und startet die aus dem Wheel installierte Headless-App. Das belegt kein signiertes Desktop-Installer-Artefakt. |
| Dokumentationskonsistenz | `python -B scripts/check_documentation_consistency.py --check` | Prüft Snapshot-Commits, Versionachsen und ausgewählte README-Aussagen. Es erzwingt keine neue SHA bei jedem Merge. |
| UI-Textinventar | `python -B scripts/check_ui_text_inventory.py --check` | Erkennt literal hartcodierte aktive Widget-/Dialogtexte in `app/`. |
| CLI-Textinventar | `python -B scripts/check_cli_text_inventory.py --check` | Erkennt CLI-Beschreibungen, Hilfetexte und Prints, die nicht über `LocaleManager.translate()` laufen. |
| Release-/Versionkonsistenz | `python -B scripts/check_release_consistency.py --check` | Prüft `VERSION`, Paket-/Python-Version, Changelog und vorhandene Release-Tags, ohne neue Artefakte oder Tags zu erzeugen. |

[GitHub Actions](../.github/workflows/python-tests.yml) führt die Kern- und
Curation-Suiten sowie den API-Abgleich auf Ubuntu mit Python 3.11, 3.12, 3.13 und 3.14
aus. Weitere Jobs prüfen den Skill auf macOS und Windows, die Wissensabdeckung
und die Veröffentlichung des Pilotmaterials.
Ein separates Ubuntu/Xvfb-Native-UI-Smoke startet das Tkinter-Hauptfenster und
prüft die verkabelte Kernbedienung. Das ist eine Linux-Automatisierungsprobe,
keine native macOS-/Windows-Abnahme und kein Ersatz für Screenreader-/Sichtprüfung.
Die Kern-Suite prüft die Veröffentlichungspfade mit isolierten synthetischen
Freigaben. Damit werden keine Desktop-, Audio- oder Produkt-MIDI-Abläufe abgenommen.

Die [Golden-Datendatei](golden_cases/README.md) enthält 198
Fälle. Davon werden 120 ausgeführt und 78 strukturell als
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
