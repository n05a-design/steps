# Konzeptrelationen

Die Tabelle führt typisierte Beziehungen und dokumentiert deren Prüfstatus. Die App-Schnittstelle für Lernbeispiele lädt den Graphen derzeit nicht.

| Einstieg | Inhalt |
| --- | --- |
| [Relationsregister](MUSIC_CONCEPT_RELATIONS.csv) | Kanten-IDs, Endpunkte, Typen und Beschreibungen. |
| [Graph-Gegenproben](FABLE_GRAPH_REVIEW.md) | Belegte Zuordnungen, Aliasse und offene Knoten. |
| [Formatknoten mit Quellenbelegen](FORMAT_NODE_EVIDENCE.csv) | Definitionen mit konkreten Fundstellen in General MIDI und MusicXML. |
| [Musikalische Knoten mit Quellenbelegen](MUSIC_NODE_EVIDENCE.csv) | Sechs Definitionen zu melodischen Mollmodi und Drop-2; keine Fachfreigabe. |
| [Belege je Kante](RELATION_EVIDENCE.csv) | Vier begrenzte Quellen-/Rechennachweise, einschließlich eines beanstandeten Polychord-Vergleichs. |
| [Referenzprüfung](../../scripts/verify_reference_integrity.py) | Struktur und Identität. |

Für eine neue fachliche Zuordnung Endpunkte, Richtung und Geltungsbereich anhand einer konkreten Fundstelle oder Gegenprobe prüfen.

Der [Nachweisstand vom 14.11.2026](../../docs/audit/fable-5.2/GRAPH_NACHWEISE_2026-11-14.md)
trennt bestandene Gegenprüfungen von der Bewertung der ursprünglichen
Graphaussage. Bei CDR-010 bestätigt die bestandene Gegenprobe einen
beanstandeten Vergleich; die Matrix führt die Kante deshalb als FAIL.
Alle 97 Registerzeilen bleiben `REVIEW_REQUIRED`.

[Zur Bereichsübersicht](../README.md)
