# STEPS V4 – wissenschaftliche Freigabe, Provenienz und Urheberrecht

## Sechs strikt getrennte Stufen

1. `named_candidate`: Titel/Autor wird nur als Recherchehinweis geführt.
2. `metadata_checked`: Offizielle Verlags-/Korpus-/Dokumentationsseite geöffnet und Metadaten gelesen.
3. `selected_text_checked`: Spezifische zugängliche Seite/Abschnitt wurde gelesen und verlinkt.
4. `claim_located`: Ein genau formulierter Claim hat Quelle, Edition, Kapitel/Abschnitt oder konkrete Seite, Datum und Kontext.
5. `theory_reviewed`: Fachgutachter hat Kontext, Gegenbeispiele, Geltungsbereich und eventuelle Alternative geprüft.
6. `approved_for_distribution`: Inhalt und konkrete Beispielfiguren/Lizenzen sowie Attribution wurden getrennt freigegeben.

**Kein automatischer Stufenaufstieg.** Eine Verlagsseite ist nicht das vollständige Buch. Ein als `reviewed` markierter Schematest macht keinen musikalischen Interpretationsreview. Alte `turn...search...`-Marker werden nicht als dauerhafte Belege übernommen.

## Claim-Record (Pflichtschema bei späterem Review)

```yaml
id: CLAIM-000001
statement: "Der konkrete überprüfbare Sachverhalt, mit Stilkontext"
claim_type: definition | mathematical_invariant | historical_finding | empirical_observation | editorial_hypothesis
status: draft
source_id: EXT-V4-...
edition: ""
exact_locator: null
reviewer: null
review_date: null
counterexamples: []
applicability: []
license_review: pending
related_rule_ids: []
related_test_ids: []
```

## Republishing-Entscheidung

Original-PDFs, proprietäre Notenseiten, kommerzielle Produkte, geschützte Originalaufnahmen und Dataset-Inhalte ohne explizites Wiederverwendungsrecht bleiben außerhalb des öffentlichen Repositories. Von freien offenen Lehrwerken übernommene Textpassagen sind nicht automatisch Lizenz-gleich mit Code. Die hier selbst verfassten didaktischen Beispiele sind ohne Übernahme fremder Kompositionen erstellt; eine globale Ähnlichkeits- oder Originalitätsprüfung ist nicht abgeschlossen.

## Dokumentationsstatus

- V1 und V3 bleiben unveränderte historische Eingaben. Ein früherer Handover nannte den Master-Prompt zu Unrecht nicht auffindbar; für dieses Paket ist er im Archiv nachweisbar.
- Die finale ursprüngliche Research-Paper-Fassung wurde nicht als zusätzliche separate Datei nachgewiesen; V3/V4 bilden neue eigenständige Synthesen.
- Der tatsächliche Zustand des Steps-Repositories wurde in diesem Dokumentationslauf nicht geprüft.
- V4 baut keine produktive STEPS-App und führt keine Git-Merges aus.
