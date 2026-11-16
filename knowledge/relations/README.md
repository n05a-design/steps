# Konzeptrelationen

Der [Nacht-Auditbericht](../../docs/audit/fable-5.2/NACHT_AUDIT_2026-11-14.md)
führt den aktuellen Stand. [97 Einzelkanten](GRAPH_AUDIT_MATRIX.csv) trennen
Definition, Quellenstand, technische Probe und ausstehende menschliche
Abnahme. [Prüfplan und Modellproben](GRAPH_AUDIT_PLAN.json) sowie
[sechs getrennte Definitionsvorschläge](NODE_DEFINITION_PROPOSALS.json)
bewahren alle historischen Originale. Die sechs historischen Lücken werden
durch Vorschläge nicht automatisch geschlossen. Spätere Zahlen beschreiben
frühere Auditstände.

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
| [Menschliche Abnahme v1](GRAPH_HUMAN_REVIEW_v1.csv) | 25 Inhaberentscheidungen vom 17.11.2026 (23 mit Patch freigegeben, CR-024 abgelehnt, CDR-010 ersetzt), je Zeile über `original_row_sha256` an die Matrix gebunden. Die erzeugte Matrix bleibt unverändert `AUSSTEHEND`. |
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

[Aktuelle Fortsetzung nach PR #56](../../docs/audit/fable-5.2/KONFLIKTE_GRAPH_FORTSETZUNG_2026-11-14.md): 39 gestützte Stichproben / 1 FAIL / 57 OPEN, 40 Modellproben und [versionierte Fehleridentitäten](VERSIONED_ERROR_IDENTITIES.json). Keine vollständige unabhängige Fachabnahme.

[Fortsetzung nach PR #57: 18 Graph-Semantikfälle](../../docs/audit/fable-5.2/GRAPH_SEMANTIK_FORTSETZUNG_2026-11-14.md): 41 begrenzte Stichproben / 1 FAIL / 55 OPEN, 57 Graphproben und getrennte Primärspezifikationskontrollen; keine externe Freigabe.

[Fortsetzung nach PR #58: 14 Korpusfälle und CDR-019/CDR-021](../../docs/audit/fable-5.2/GRAPH_KORPUS_QUELLEN_FORTSETZUNG_2026-11-14.md): verifizierte GMD-Teilmenge, Rollen-/Akzenttrennung und konkretisierte Quellenketten; 41 Stichproben / 1 FAIL / 55 OPEN, 73 technische Kantenprüfungen und58 Graphproben. Externe Freigaben bleiben offen.

[Fortsetzung nach PR #59: Originalsuche und weitere Korpuskomponenten](../../docs/audit/fable-5.2/ORIGINALQUELLEN_KORPUS_FORTSETZUNG_2026-11-14.md): 890 Billboard-Harmonieannotationen und664 versionierte Genre-/Tempoeinträge tatsächlich ausgewertet; Quellenoriginale und sämtliche14 Korpusbehauptungen bleiben ohne Vollfreigabe.

[Fortsetzung nach PR #61: gemeinsame RWC-Zeitachsen und Garcia2023](../../docs/audit/fable-5.2/RWC_GARCIA_FORTSETZUNG_2026-11-14.md): 100 gemeinsam identifizierte RWC-Harmonie-/Beat-/MIDI-Stücke,18 Swing-Chart-/Drum-Takes, deklarierte rhythmische Teilmuster und neuer begrenzter Autorenbeleg. Alle14 Korpusbehauptungen und ältere Originalseiten bleiben offen.

**Menschliche Abnahme v1 (17.11.2026).** Der Inhaber hat 25 der 97 Kanten entschieden ([`GRAPH_HUMAN_REVIEW_v1.csv`](GRAPH_HUMAN_REVIEW_v1.csv)). Grundlage ist seine geprüfte Fassung der Matrix (Datei `GRAPH_AUDIT_MATRIX_REVIEWED_v1.csv`, SHA-256 `e944eba07bd316098336de3d9dcf90f91822dcc51b8a52b1ac6f8760f9c5d50c`, nicht versioniert): Darin sind gegenüber der Matrix nur `relation_status`, `human_review` und `production_use_allowed` in genau diesen 25 Zeilen geändert und zwei Spalten (`proposed_relation_type`, `audit_decision_note`) ergänzt; alle übrigen Felder sind identisch. Die Abnahme liegt bewusst in einer eigenen Schicht, weil `scripts/audit_graph.py` die Matrix aus `GRAPH_AUDIT_PLAN.json` erzeugt und dort jede Freigabe als verfrüht abweist. Die Übernahme in Plan und Generator ist ein eigener Schritt. Zu CDR-010 passt die Ersatzkante zum vorhandenen Vorschlag `C6_9_SHARP11_COLLECTION` in [`GRAPH_CORRECTIONS.json`](GRAPH_CORRECTIONS.json): D-Dur über C-Dur ergibt die Tonklassen {0, 2, 4, 6, 7, 9}. Als Slash-Akkord gelesen wäre D/C dagegen D7/C; die Polychord-Lesart muss deshalb ausdrücklich bleiben.
