# Priorisierte Restblocker und nächste ausführbare Aktionen

Dies ist der Evidenzindex zum Nachtbericht, kein konkurrierender
Aufgabenmaster. Kanonisch bleibt das lokale Register unter
`%LOCALAPPDATA%/StepsKnowledge/OFFENE_ARBEITSAUFFORDERUNGEN.md`,
insbesondere OA-0001, OA-0033 und OA-0034.

| Priorität | Bestand | Konkrete Voraussetzung und nächste Aktion | Grenze |
| --- | --- | --- | --- |
| P0 | Historische Exposition dreier Google-Schlüssel | Autorisierte Eigentümer bewerten Berechtigungen, Einschränkungen, Missbrauch und ggf. Rotation/History-Bereinigung. [69 bereinigte Vorkommen](SECRET_GUARDRAIL_166_2026-11-14.md); die AWS-Muster waren eingebettete JPEG-Daten. | Aktueller Vollscan und CI #168 bestehen. Historische Exposition und Sicherheitsfreigabe bleiben offen; keine Baseline-Erweiterung oder History-Umschreibung. |
| P0 | OA-0001, vorhandene Fremd-PDFs/MIDIs/Webassets | Rechteinhaber/Owner bestätigen zulässige Veröffentlichung und Archivbehandlung. | Lesbarkeit, Dateibesitz und Metadaten sind keine Rechtefreigabe. |
| P0 | Required-Check-Policy | Owner prüft die beiden aktiven Rulesets und macht insbesondere den Secret-Scan sowie gewünschte Python-Prüfungen zu verbindlichen Gates. | Aktuell ist als erforderlicher Statuscheck nur der geschützte Pilot-Evidenzcheck registriert; keine Regeln oder Rechte wurden geändert. |
| P1 | Sechs CSS-Pflichtfälle | Rechte am gesamten Bundle und dauerhafte Archivzuordnung belegen. | Bereits bestätigte technische Lieferkette schließt diese Pflichtfälle nicht. |
| P1 | Sechs historische Definitionslücken | NODE_DEFINITION_PROPOSALS.json fachlich prüfen; Zielrichtung, Instrument/Rolle, Aufnahme und Geltungsbereich entscheiden. | Vorschläge bleiben außerhalb der historischen Knotenauflösung. |
| P1 | 58 offene Kanten und 38 Stichproben | Einzelnotizen in GRAPH_AUDIT_MATRIX.csv bearbeiten: Korpus/Aufführung, Arrangement, Lernwirksamkeit, Namensraum oder Typ/Richtung prüfen. | Keine der 97 Kanten ist vollständig unabhängig fachlich abgenommen. |
| P1 | CDR-010 | Den gesonderten C6/9(#11)-Sammlungsvorschlag fachlich prüfen; historischen FAIL erhalten. | Kein automatisches Ersetzen der Kante. |
| P1 | 12 Coach-Abnahmen | Tatsächliche Antworten mit Modell-/Skill-Version, Quellen und unabhängiger menschlicher Rubrikbewertung erheben. | Selbst geschriebene Musterantworten zählen nicht als unabhängige Abnahme. |
| P1 | Drei Hör-/Spielabnahmen | PAT-031-Taktgruppierung, P02-Hand/Fingersatz/Tempo und die beiden Loop-Fassungen praktisch prüfen. | WAV-Messungen und kleine L1-Distanzen ersetzen Hören/Spielen nicht. |
| P1 | SRC-033 | Historische Robert-Prehn-Publikation mit bibliografischem Original belegen oder ihre Ablösung autorisieren. | Das erreichbare Oliver-Prehn-Chart ist ein anderes Werk; keine Nichtexistenz behauptet. |
| P1 | Vier PPR-MIDI-Provenienzen | Originallieferung, Paket-Dateiliste, README und Rechtebeleg beibringen. | 112 technisch lesbare SMFs bestätigen keine Zuordnung zu den vier Lieferungen. |
| P2 | Forschungsclaims | CLAIM_AUDIT_MATRIX.csv abarbeiten: insbesondere Hindemith-Locator und Linn1988/MPC3000-Zuschreibung. 21 Platzhalter nur mit echten neuen Aussagen/Fundstellen füllen oder autorisiert stilllegen. | Keine bibliografischen Daten erfinden. Vorhandene Quellenprüfungen sind begrenzt und ohne menschliche Freigabe. |
| P2 | Zwei beschädigte MakingMusic.pdf-Kopien | Originale erhalten; lesbare vorhandene MakingMusic_DennisDeSantis.pdf als untersuchte Alternative nutzen. Ersatz-/Aussonderungsentscheidung und Rechte dokumentieren. | Nicht stillschweigend überschrieben; alternative Datei ist nicht automatisch dieselbe Edition. |
| P2 | 64 jetzt einzeln geprüfte Golden-Spezifikationsbeispiele | [Prüfmatrix](GOLDEN_64_PRUEFMATRIX_2026-11-14.csv): 43 getrennte Modellrechnungen, sechs bestehende GM-Tabellenchecks, sieben explizite Originalkonflikte. Neue Fallversionen und konkrete Arrangements anhand der Einzelvorschläge fachlich entscheiden. | Alle 64 operativ untersucht; ihre Originale und Fach-/Quellenfreigaben werden nicht durch Modell-PASS geschlossen. |
| P2 | Paket-/Publikationsarchitektur | F-A04-01: Verträge für Dateidatenquelle/Distribution und ADR-Scope festlegen; heutiger Checkout-Test ist kein Installations-/Paketnachweis. | Keine unbeauftragte Desktop-/Importerentwicklung. |
| P2 | Lokale Hauptcheckouts und externe Ablagen | Die ältere OneDrive-Arbeitskopie enthält eigene Differenzen und bleibt unangetastet. Gesamtvergleich und Übernahme weiterer veröffentlichungsgeeigneter Daten separat mit Originalhash/Review durchführen. | Dieser Branch ist keine vollständige Synchronisierung aller lokalen Bestände. |

[Alle 27 PENDING-Fälle einzeln](NACHT_PENDING_2026-11-14.csv)
· [33 Fable-Befunde mit technischen Referenzen](NACHT_FABLE_ABGLEICH_2026-11-14.csv)
