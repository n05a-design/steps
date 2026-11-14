# Konzeptrelationen

Die Tabelle führt typisierte Beziehungen und dokumentiert deren Prüfstatus. Die App-Schnittstelle für Lernbeispiele lädt den Graphen derzeit nicht.

| Einstieg | Inhalt |
| --- | --- |
| [Relationsregister](MUSIC_CONCEPT_RELATIONS.csv) | Kanten-IDs, Endpunkte, Typen und Beschreibungen. |
| [Graph-Gegenproben](FABLE_GRAPH_REVIEW.md) | Belegte Zuordnungen, Aliasse und offene Knoten. |
| [Formatknoten mit Quellenbelegen](FORMAT_NODE_EVIDENCE.csv) | Definitionen mit konkreten Fundstellen in General MIDI und MusicXML. |
| [Musikalische Knoten mit Quellenbelegen](MUSIC_NODE_EVIDENCE.csv) | Begrenzte Definitionen mit getrennter Kennzeichnung von Originalquelle, Projektbeispiel und Modellrechnung; keine Fachfreigabe. |
| [Belege je Kante](RELATION_EVIDENCE.csv) | Begrenzte Quellen-/Rechennachweise, einschließlich eines beanstandeten Polychord-Vergleichs. |
| [Explizite Korrekturvorschläge](GRAPH_CORRECTIONS.json) | Historisch gebundene Korrektur für CDR-010; REVIEW_REQUIRED und ohne Produktionsfreigabe. |
| [Referenzprüfung](../../scripts/verify_reference_integrity.py) | Struktur und Identität. |

Für eine neue fachliche Zuordnung Endpunkte, Richtung und Geltungsbereich anhand einer konkreten Fundstelle oder Gegenprobe prüfen.

Der [Nachweisstand vom 14.11.2026](../../docs/audit/fable-5.2/GRAPH_NACHWEISE_2026-11-14.md)
trennt bestandene Gegenprüfungen von der Bewertung der ursprünglichen
Graphaussage. Bei CDR-010 bestätigt die bestandene Gegenprobe einen
beanstandeten Vergleich; die Matrix führt die Kante deshalb als FAIL.
Alle 97 Registerzeilen bleiben `REVIEW_REQUIRED`.

Die [weitere Fortsetzung](../../docs/audit/fable-5.2/GRAPH_KLAERUNG_CDR010_2026-11-14.md)
ordnet 25 der zuvor 74 Restknoten begrenzt zu und belässt 49 Definitionen
offen. Originalquelle, Projektbeispiel und eigene Modellrechnung werden in
`MUSIC_NODE_EVIDENCE.csv` getrennt gekennzeichnet. Ein Korrekturvorschlag
setzt weder historische Gegenbefunde noch fehlende Fachabnahmen außer Kraft.

[Zur Bereichsübersicht](../README.md)
