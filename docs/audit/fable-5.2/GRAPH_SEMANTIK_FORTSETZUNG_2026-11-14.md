# Graphfortsetzung: 18 Semantik- und Quellenentscheidungen

Basis ist `main` 80763f82e95bdfff6f2fd56497286c7f03f27e63 nach dem externen Merge von PR #57. PR #56 war bereits zuvor integriert. Diese Fortsetzung untersucht alle 18 im vorherigen Paket als Quellen-/Semantikentscheidung eingeordneten Kanten. Sie ersetzt keine historischen Quellen und erteilt keine Fach-, Rechte- oder Sicherheitsfreigabe.

## Ergebnis und Grenzen

| Nachweis | Vorher | Jetzt |
| --- | ---: | ---: |
| Historische Kanten | 97 | 97 |
| Begrenzte gestützte Stichproben | 39 | 41 |
| Historischer FAIL | 1 | 1 |
| Offene Kanten | 57 | 55 |
| Kanten mit technischer Gegenprüfung | 59 | 72 |
| Ausführbare Graphproben | 40 | 57 |
| Unabhängige vollständige Fachabnahmen | 0 | 0 |

Die [18 Einzelvorschläge](GRAPH_SEMANTIK_18_2026-11-14.csv) besitzen jeweils einen SHA-256-Anker auf die historische Registerzeile, einen gesonderten Relationstyp, notwendige Kontextbedingungen und ausgeschlossene Aussagen. Alle 18 Vertragsprüfungen bestehen. Bei 16 Vorschlägen bestehen begrenzte Modellprüfungen, davon eine bereits vorhandene Montuno-Entwurfsprüfung; zwei bleiben ausdrücklich `NOT_EXECUTED`. Diese Zählungen sind unterschiedliche Kategorien und werden nicht addiert oder als 18 musikalische Freigaben ausgegeben.

## Individuelle Bearbeitung

| Kante | Präzisierung und technisch prüfbarer Umfang |
| --- | --- |
| CR-002 | Oktave als Referenzintervall statt Variante eines Stimmungssystems. |
| CR-004 | Alterierte Tonbenennung ist auch ohne Notensystem darstellbar; Notationskontext explizit. |
| CR-006 | Enharmonische Schreibweise und Stufenfunktion nur im deklarierten Tonart-/Moduskontext. |
| CR-017 | I/IV/V als ausgewählte Hauptfunktionsdreiklänge, keine Gleichsetzung mit allen Stufen. |
| CR-025 | Eigenes SMF-Kontrollbeispiel mit PPQ-Zeitbasis; SMPTE ausdrücklich ausgeschlossen. |
| CR-027 | Swing-Zeitpunkt benötigt Paarbreite und Indexkonvention: Achtel und Sechzehntel ergeben unterschiedliche Tickpositionen. |
| CR-028 | GM1-Geräteprofil ausdrücklich vorausgesetzt; beliebiges MIDI-Gerät impliziert keine GM-Konformität. |
| REL-009 | Harmonischer Skalenkontext legt die konkrete Stufenfunktion fest. |
| REL-011 | One-Drop-Schlagzeugkontrolle benötigt keine Keyboardspur; keine Genre-Authentizitätsabnahme. |
| REL-027 | 58 Prozent als Quellenwert der konkreten UKG-Übung, keine universelle Stilnorm. |
| REL-028 | MusicXML-Perkussionsnummern sind einsbasiert, MIDI-Daten nullbasiert; Notationsposition ist keine Tonhöhe. |
| REL-031 | Quellgebundene Cross-Stick-Einsätze von PAT-027; keine vollständige Gitarren-/Klavier-Batida. |
| REL-034 | Historische Domänen M01–M12 getrennt von späteren Bereitschaftsgliederungen. |
| REL-036 | 28 konkrete Stufendreiklang-Instanzen über vier Skalen; keine Behauptung von 28 verschiedenen Tonklassenmengen. |
| CDR-014 | Neuer Montuno-Entwurf mit deklarierten Ereignissen; keine Rekonstruktion einer historischen Originalfigur. |
| CDR-019 | Rhythmische Analogie getrennt von historischer Herkunft. Herkunftsprüfung bleibt ohne ausreichende Originalquelle offen; kein Modell-PASS. |
| CDR-020 | GM1-Kanal-/Perkussionskontext von einer beliebigen SMF-Datei getrennt. |
| CDR-021 | Akzentbehauptung benötigt benannte Surdo-Rolle und Ensemblekontext; keine universelle Norm, kein Modell-PASS. |

Zusätzlich prüft ein Entwurf die gemeinsame Periodenlänge einer Glockenfigur und der tatsächlichen vier Akkorde von PROG-025: acht Glockenzyklen und drei Harmoniezyklen treffen nach 23040 Ticks zusammen. Dies ist eine Rechenkontrolle eines neuen Entwurfs, keine historische Transkription oder stilistische Abnahme. Vorzeichen allein bestimmen den Leitton nicht; natürliche und erhöhte siebte Stufe werden getrennt geprüft.

## Quellen und unabhängige Formatkontrollen

Das [Quellenprotokoll](GRAPH_SEMANTIK_QUELLEN_2026-11-14.json) dokumentiert Version, Hash und genaue Fundstellen. Die MMA-Spezifikation 96.1, dritte Ausgabe, wurde aus einem Drittspiegel lokal geprüft. PDF-Seiten 133, 147 und 151 wurden zusätzlich gerendert und visuell gelesen. Ein Bytevergleich mit einer offiziell ausgelieferten Datei liegt nicht vor. Die Datei wird nicht veröffentlicht. Die GM1-Anforderung von mindestens 47 Perkussionsklängen ist keine Obergrenze für Geräte.

Die [W3C-MusicXML-Perkussionsdarstellung](https://www.w3.org/2021/06/musicxml40/tutorial/percussion/) stützt den Indexversatz: Kanal 10 und `midi-unpitched` 39 entsprechen MIDI-Kanalindex 9 und Notennummer 38. Fünf eigenständige Indexkontrollen und fünf selbst erzeugte SMF-Dateien wurden [separat geprüft](GRAPH_SEMANTIK_FORMATKONTROLLEN_2026-11-14.json). Die MIDI-Dateien wurden mit Mido unabhängig zurückgelesen. Die kleinen Kontrollgeneratoren sind Auditwerkzeuge; sie bescheinigen keinen vollständigen Produkt-Exporter oder MusicXML-Konverter.

Vier Kanten erhalten einen begrenzten aktuellen Primärspezifikationsnachweis. `source_assertion_verified` bleibt dort ausdrücklich falsch: Die gesamte historische Aussage ist damit nicht freigegeben. CDR-010 bleibt historisch `FAIL`.

## Implementierung und Reproduktion

- [Vorschläge](../../../knowledge/relations/GRAPH_SEMANTIC_PROPOSALS.json), [Prüfer](../../../scripts/audit_graph_semantics.py) und [Modelloperationen](../../../scripts/graph_semantic_probes.py) trennen Kontextvertrag, Modell und menschliche Abnahme.
- [Regressionstests](../../../tests/test_graph_semantics.py) prüfen unter anderem manipulierte Originalidentitäten, fingierte Abnahmen, fehlende Kontexte, doppelte XML-Felder, Indexgrenzen und PPQ-/SMPTE-Verwechslung.
- Die [vollständige Kantenmatrix](../../../knowledge/relations/GRAPH_AUDIT_MATRIX.csv) bleibt die Gesamtansicht aller 97 Original-IDs. Die historischen Originalregister und Golden-Master/-Mirror bleiben erhalten.

```text
python -B scripts/audit_graph_semantics.py --check
python -B scripts/audit_graph.py --check
python -B -m unittest discover -s tests -p 'test_*.py'
python -B -m unittest discover -s .agents/skills/steps-knowledge-curation/tests
python -B scripts/run_knowledge_benchmark.py --scope all --json-out benchmark.json
python -B scripts/pre-commit-secret-check.py --scan-all
```

Lokal bestehen 249 Kern- und 36 Skilltests. Der Knowledge-Benchmark bleibt bei 92 PASS / 0 FAIL / 27 PENDING; sein Exitcode 1 kennzeichnet weiterhin fehlende Pflichtnachweise. Der vollständige Secret-Scan meldet 0 quarantänisierte und 0 neue Befunde. Ontologie-, Referenz-, Quellenbereinigungs-, Golden-, API-, Publikations- und Coverage-Prüfungen bestehen ebenfalls. 923 interne Links wurden geprüft: keine neuen aktiven Fehler, 25 bereits dokumentierte historische Archivverweise. GitHub-Ergebnisse werden im Git-Übergabenachweis des Pakets festgehalten; lokale Ergebnisse sind keine vorweggenommene CI-Freigabe.

## Tatsächlicher Restbestand

Die sechs historischen Definitionslücken sind nicht durch neue Beispiele geschlossen. Herkunftsaussagen, Surdo-Rollen, Korpusprüfungen, Hör-/Spiel-/Coach-Abnahmen, CSS-Bundle-Rechte und historische Sicherheitsbewertung bleiben offen. 55 Graphkanten bleiben offen, CDR-010 bleibt beanstandet. Dieses Paket ist eine abgeschlossene Bearbeitung der 18 ausgewählten Fälle bis zur ausgewiesenen Evidenzgrenze; das Gesamtaudit ist nicht vollständig abgeschlossen. Die [priorisierte Restliste](NACHT_RESTBLOCKER_2026-11-14.md) führt die weiteren Voraussetzungen.
