# Konzeptrelationen

Der [Originalfund unter Windows](../../docs/audit/fable-5.2/ONTOLOGIE_WIEDERFUND_2026-11-14.md) belegt jetzt alle 41 fehlenden historischen Definitionen. Zwei P10-Begriffe sind als Projektstrategie eingegrenzt; sechs Definitionen bleiben offen. Die historischen Domänen werden nicht automatisch auf spätere Gliederungen abgebildet. Keine neue Kanten-, Hör-, Spiel- oder Didaktikabnahme wurde erteilt. Die später folgenden Zahlen zu 49 offenen Definitionen beschreiben den vorherigen Prüfstand.

Die Tabelle führt typisierte Beziehungen und dokumentiert deren Prüfstatus. Die App-Schnittstelle für Lernbeispiele lädt den Graphen derzeit nicht.

| Einstieg | Inhalt |
| --- | --- |
| [Relationsregister](MUSIC_CONCEPT_RELATIONS.csv) | Kanten-IDs, Endpunkte, Typen und Beschreibungen. |
| [Graph-Gegenproben](FABLE_GRAPH_REVIEW.md) | Belegte Zuordnungen, Aliasse und offene Knoten. |
| [Formatknoten mit Quellenbelegen](FORMAT_NODE_EVIDENCE.csv) | Definitionen mit konkreten Fundstellen in General MIDI und MusicXML. |
| [Musikalische Knoten mit Quellenbelegen](MUSIC_NODE_EVIDENCE.csv) | Begrenzte Definitionen mit getrennter Kennzeichnung von Originalquelle, Projektbeispiel und Modellrechnung; keine Fachfreigabe. |
| [Belege je Kante](RELATION_EVIDENCE.csv) | Begrenzte Quellen-/Rechennachweise, einschließlich eines beanstandeten Polychord-Vergleichs. |
| [Explizite Korrekturvorschläge](GRAPH_CORRECTIONS.json) | Historisch gebundene Korrektur für CDR-010; REVIEW_REQUIRED und ohne Produktionsfreigabe. |
| [Wiedergefundene historische Definitionen](HISTORICAL_NODE_EVIDENCE.csv) | 41 Originaldefinitionen mit Zeile, SHA-256 und eigenem historischen Namensraum; keine Fachfreigabe. |
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
