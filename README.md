# STEPS – Musiktheorie- und Progressionskern

STEPS stellt einen Python-Kern für Tonhöhen, Intervalle, Akkordsymbole,
Stufenauflösung, Transposition und Stimmführung bereit. Der Checkout enthält
eine Schnittstelle für fachlich freigegebene Lernbeispiele. Die drei
Pilotbeispiele liegen zur menschlichen Fachabnahme vor. Die Desktop-App befindet sich
in Vorbereitung.

Der Entwicklungsstand steht in [VERSION](VERSION), die Paketversion in
[`src.steps.__version__`](src/steps/__init__.py). Der Quellcode steht unter
[Mozilla Public License 2.0](LICENSE). Die Rechte an Forschungsquellen werden
je Quelle erfasst.

## Schnellstart

Aus dem Repository-Root mit Python 3.11 oder 3.12:

```sh
python -B -m unittest discover -s tests
python -B scripts/verify_reference_integrity.py
python -B scripts/render_api_reference.py --check
```

Die [Testanleitung](tests/README.md) beschreibt die Prüfungen, die CI-Matrix
und die Grenzen der Golden Cases. Die [Pilotfreigabe](knowledge/concepts/progressions/README.md) beschreibt den gesonderten Publikationscheck.

## Dokumentation

- [Implementierungsstand und Funktionsgrenzen](docs/IMPLEMENTATION.md)
- [Python-API und unterstützte Akkordqualitäten](docs/theory/API.md)
- [Geprüfte Lernbeispiele und Datenpflege](knowledge/concepts/progressions/README.md)
- [Architektur, Entscheidungen und offene Fragen](docs/README.md)
- [Historische Fassungen und Audits](archive/INDEX.md)
