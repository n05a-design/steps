# Schnittstellen des Fachkerns

Das Paket enthält derzeit ein dokumentarisches `__init__.py`. Verträge für Persistenz, Wiedergabe und Import/Export sind Zielentwürfe.

| Einstieg | Inhalt |
| --- | --- |
| [Domänen- und Speicherverträge](../../../docs/architecture/DOMAIN_AND_STORAGE_CONTRACTS.md) | Vorgesehene Grenzen für Daten und Ports. |
| [`live.py`](live.py) | Vorgeschlagener Vertrag für Live-Noteneingabe (MIDI) und Notenvorschau; nur Testadapter, siehe [ADR-019](../../../decisions/ADR-019-live-audio-preview-and-midi-input.md). |
| [App-Adapter](../../../app/README.md) | Vorhandene Schnittstelle für freigegebene Lernbeispiele. |

[Zur Bereichsübersicht](../README.md)
