# Theorie-API

Hier liegen die musikalischen Grundtypen und Berechnungen. Geschriebene Note, klingender MIDI-Wert und Tonklasse haben eigene Verträge.

| Einstieg | Inhalt |
| --- | --- |
| [pitch.py](pitch.py) | Tonklassen, Notenschreibweise, Konventionen und Frequenz. |
| [interval.py](interval.py) | Chromatische und diatonische Intervalle sowie buchstabierte Transposition. |
| [chord.py](chord.py) | Akkordsymbole, Qualitäten, Slash-Bass und Voicing-Layouts. |
| [triad.py](triad.py) | Dreiklangbildung und Umkehrungen. |
| [seventh.py](seventh.py) | Septakkorde, Drop-2 und Shell-Voicings. |
| [exceptions.py](exceptions.py) | Fehlertypen für den Fachkern. |

Öffentliche Aufrufe stehen in der [API](../../../docs/theory/API.md). Relevante Regressionen stehen in [Theorie](../../../tests/test_theory_core.py), [Notation](../../../tests/test_notation_contract.py) und [Voicing](../../../tests/test_voicing_contract.py).

[Zur Bereichsübersicht](../README.md)
