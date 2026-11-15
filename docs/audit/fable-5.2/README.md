# Fable-Audit 5.2

Die Nachprüfung erfasst die Befunde des Fable-Audits und verweist auf die reproduzierbaren Prüfungen und zugehörigen Nachweise.

| Einstieg | Inhalt |
| --- | --- |
| [Maßnahmenplan](STEPS_FABLE_5_2_MASSNAHMENPLAN.md) | Alle 33 Befund-IDs, Prioritäten und Abnahmekriterien. |
| [Nachprüfung](STEPS_FABLE_5_2_NACHPRUEFUNG.md) | Basiscommit, Gegenproben und bestätigte Abweichungen. |
| [Prüfumfang](STEPS_FABLE_5_2_AUDIT_SCOPE.md) | Prüfmatrix und erwartete Nachweise. |
| [Quellenabgleich](STEPS_FABLE_5_2_QUELLENABGLEICH.md) | Fundstellen, historischer Abgleich und Wiederherstellung aus dem Register-Snapshot. |
| [Hör- und Spielproben](STEPS_FABLE_5_2_ABNAHMEPROBEN.md) | WAV-Erzeugung, Messungen und Kriterien für menschliche Abnahmen. |
| [Archivnachweise](STEPS_FABLE_5_2_ARCHIVNACHWEISE.md) | Historische MIDI- und CSS-Stände mit Hashes. |
| [Fortsetzung nach PR #50](FORTSETZUNG_2026-11-13.md) | Reproduzierter Main-Stand, offene Fälle, lokale Bestände und wiedergefundene CSS-Registerfassung. |
| [CSS-Provenienz](CSS_PROVENIENZ_2026-11-14.md) | Archivierte Playerseiten, Live-CDN-Hashvergleich und weiterhin offene Bundle-Rechte. |
| [Graphnachweise](GRAPH_NACHWEISE_2026-11-14.md) | Sechs zusätzliche Knoten, vier Gegenprüfungen, beanstandete Polychord-Zuordnung und offene IDs. |
| [CDR-010 und weitere Graphknoten](GRAPH_KLAERUNG_CDR010_2026-11-14.md) | Präziser Korrekturvorschlag, Bearbeitung aller 74 bisherigen Restknoten und 49 verbleibende Definitionen. |
| [Originalontologie wiedergefunden](ONTOLOGIE_WIEDERFUND_2026-11-14.md) | Windows-Originale, 41 historische Definitionsanker, acht einzeln geprüfte Restknoten und sechs verbleibende Definitionen. |
| [Nacht-Audit nach PR #54](NACHT_AUDIT_2026-11-14.md) | Vollständige Graphmatrix, sechs Definitionsvorschläge, Quellen-/MIDI-/PDF-Gegenprüfungen und offene Sicherheits-/Fachfreigaben. |
| [PR-22-Freigabenachweis](PR22_HASHABGLEICH_2026-11-13.md) | Fassungsgebundener Nachweis der damaligen Pilotfreigaben. |

Den aktuellen Prüfstand liefert der [Benchmark](../../../knowledge/benchmark/README.md). Fehlende Belege sind in den [offenen Nachweisen](../../../research/gaps/OPEN_GAPS.md) erfasst.

[Zur Bereichsübersicht](../README.md)

[Sicherheitskorrektur Guardrail #166](SECRET_GUARDRAIL_166_2026-11-14.md): vollständige Bereinigung des aktuellen Stands; historische Sicherheitsbewertung offen.

[Fortsetzung: alle 64 übrigen Golden-Beispiele und Quellen](GOLDEN_64_QUELLENPRUEFUNG_2026-11-14.md): 43 getrennte Modellprüfungen, sieben historische Konflikte und neue Primärnotenkontrolle zu CDR-018.

[Fortsetzung nach PR #56: Konfliktrevisionen und Graph](KONFLIKTE_GRAPH_FORTSETZUNG_2026-11-14.md): 15 ausführbare Golden-Vorschläge, 40 Graphproben, versioniertes ERR-026 und neue Prüfmaterialien; externe Freigaben offen.

[Fortsetzung nach PR #57: 18 Graph-Semantikfälle](GRAPH_SEMANTIK_FORTSETZUNG_2026-11-14.md): 41 begrenzte Stichproben / 1 FAIL / 55 OPEN, 57 Graphproben und getrennte Primärspezifikationskontrollen; keine externe Freigabe.

[Fortsetzung nach PR #58: 14 Korpusfälle und CDR-019/CDR-021](GRAPH_KORPUS_QUELLEN_FORTSETZUNG_2026-11-14.md): verifizierte GMD-Teilmenge, Rollen-/Akzenttrennung und konkretisierte Quellenketten; 41 Stichproben / 1 FAIL / 55 OPEN, 73 technische Kantenprüfungen und58 Graphproben. Externe Freigaben bleiben offen.

[Fortsetzung nach PR #59: Originalsuche und weitere Korpuskomponenten](ORIGINALQUELLEN_KORPUS_FORTSETZUNG_2026-11-14.md): 890 Billboard-Harmonieannotationen und664 versionierte Genre-/Tempoeinträge tatsächlich ausgewertet; Quellenoriginale und sämtliche14 Korpusbehauptungen bleiben ohne Vollfreigabe.

[Pilot-Event nach schnellem externem Merge](PILOT_PR_EVENT_RACE_2026-11-14.md): fehlendes flüchtiges Merge-Ref durch exakt identitätsgebundenen abgeschlossenen Merge prüfen; historischer roter Lauf bleibt erhalten.

[Fortsetzung nach PR #61: gemeinsame RWC-Zeitachsen und Garcia2023](RWC_GARCIA_FORTSETZUNG_2026-11-14.md): 100 gemeinsam identifizierte RWC-Harmonie-/Beat-/MIDI-Stücke,18 Swing-Chart-/Drum-Takes, deklarierte rhythmische Teilmuster und neuer begrenzter Autorenbeleg. Alle14 Korpusbehauptungen und ältere Originalseiten bleiben offen.

[Abgleich nach PR #70 und Pattern-Fortsetzung](ABGLEICH_PATTERN_FORTSETZUNG_2026-11-14.md): aktualisierte Restposten, strengere REL-001/REL-005-Notenrastermessung und CAPH-Referenz4195N; Fach-, Rechte- und Sicherheitsfreigaben offen.

[Fortsetzung nach autorisiertem Push](PATTERN_QUELLEN_FORTSETZUNG_2026-11-15.md): konkrete Aufnahme-/Quelldateibindung des Patternvalidators korrigiert; Loader-Lieferung statisch geprüft und Schreiner-Editionsfrage präzisiert. Keine neue Fach- oder Rechtefreigabe.

[Synkopenprüfung nach PR #71/#72](PATTERN_SYNKOPE_ORIGINALSUCHE_2026-11-15.md): historischen REF-0030-Tickanker wieder zugeordnet, Kick-Synkope mit zwei Toleranzen gemessen und Originalzugänge zu CDR-019 getrennt dokumentiert. Fach-/Rechte-/Sicherheitsabnahmen offen.

[Swing-Quellenprüfung nach PR #73](GMD_SWING_QUELLEN_FORTSETZUNG_2026-11-15.md): herausgeberdokumentiertes GMD-Instrumentmapping, elf Swing-Performances mit konkreten Teilmuster-Prüfstellen und Schreiner-Ausgabe mit ISBN; keine Harmoniekopplungs- oder Fachfreigabe.
