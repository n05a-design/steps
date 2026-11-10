# STEPS-Wissensbibliothek und Harmony-Skill: Governance und Umsetzung

## Was vorhanden ist

- Roh-/Rechercheinventar unter `research/STEPS_Bibliothek/`, historische V6.6/V6.7-Indizes/Generatoren, wissenschaftliche Ausgangsquellen, konkurrenzbezogene Unterlagen, Kurse, MusicXML/MIDI und Produktionsmaterialien.
- `knowledge/legacy/STEPS_BIBLIOTHEK_README.md` ordnet den historischen Ordnerbestand; zwei doppelt belegte Ordnernummern/heterogene Zahlensysteme sind im Bestandsaudit beschrieben.
- `skills/music-harmony-coach/2026-11-10 – music-harmony-coach/SKILL.md` und fünf Referenzen existieren. Diese Referenzen sind keine automatisch validierte bibliografische Beweiskette.
- `knowledge/sources/registry.yaml` hat `sources: []`; einige JSON-Schemas liegen vor. **Keine kuratierte Laufzeit-Knowledgebase belegt.**

## Zielmodell der Wissensobjekte

```text
Work(id,title,authors,license_status)
  └── Edition(id,work_id,publication,year,identifier)
       └── Asset(id,edition_id,local_path_or_url,sha256,rights_status)
            └── Claim(id,asset_id,locator,paraphrase,context,reviewer,review_status)
                 └── Concept(id,notation,style,alternatives,claim_ids,test_ids)
                      └── Exercise(id,concept_ids,expected_answers,negative_cases)
```

**Hinweis:** Pseudomodell als Vorschlag, nicht in vorhandenen Schemas implementiert. Bestehende `schemas/source.schema.json` und V2-Entwürfe sind laut V3 **nicht ohne Migration kompatibel**. Kein Schema überschreiben, ohne Versionierung, Rückwärtskompatibilität und Fixtures.

## Stufenplan

1. **Bibliotheksinventur (read-only):** Pfad, Hash, Größe, Dateityp, Werk/Edition, Dublettengruppe, Herkunft, vorhandene Zitate, vorhandene Markdownlinks; Git-Historie und Migrationsergebnisse getrennt. Keine Binärdateien in Git nachkopieren.
2. **Rights-Triage:** `approved`, `review_required`, `restricted_local`, `rejected`. Trenne „persönlich lesen“, „an KI zur Analyse senden“, „Quelltext zitieren“, „öffentlich hosten“, „in Demo-Soundpack verteilen“.
3. **Pilot 3–5 Quellen** unterschiedlicher Art, z. B. eigener Theorieentwurf, gemeinfreies Werk, ein frei lizenziertes Dokument. Keine Rechte aus Titeln oder Download-URLs folgern. Für jede 3–5 überprüfbare Claims und mindestens einen Ambiguitätsfall.
4. **Konzeptkarten** für Akkordtöne, Enharmonik, Funktion, Stimmführung, Stil-/Moduswechsel; jede eigene Zusammenfassung statt ungeprüfter Volltext.
5. **Skill-Routing:** Nutzerfrage → Intent/Notation/Stil → relevante freigegebene Claims → regelgestützte Antwort → Quellen-/Unsicherheitsangabe. `restricted_local` nicht in Cloud-Prompts leiten.
6. **Evaluation:** mindestens 30 geplante Tests (zunächst 10 kritische Negativ-/Konfliktfälle), darunter deutsches H/B, C7 vs Cmaj7, V7/vi, Slash-Chord, Enharmonik, parallele Voice-Leading-Alternativen und fehlende Seitenbelege.
7. **Skalierung:** erst nach Pilot auf 20 ursprünglich katalogisierte Fachquellen; dann Forschungsarchiv thematisch priorisieren.

## Skill vs Agentenregel vs Anwendung

- `AGENTS.md` / `.agents/rules/`: stets geltende Grenzen, Dokumenthierarchie, Rechte, Fehlerlogik.
- `skills/music-harmony-coach/.../SKILL.md`: wiederverwendbarer, schrittweiser Workflow für Harmonielehre/Retrieval/Analyse.
- `knowledge/`: geprüfte fachliche Claims/Relations und Index.
- `src/steps/`: deterministische Rechenlogik (Akkord-/Intervall-/Timeline-Algorithmen) **nicht** von LLM-Antworten abhängig.

## Abnahmekriterien

Keine erfundenen Buchtitel, Seitenzahlen oder fachlichen Quellen; keine verdeckte Weitergabe lokaler Restricted-Dateien; Ergebnisse verweisen auf Claim-IDs und Versionen, erwähnen Alternativen, scheitern kontrolliert bei fehlender Quellenbasis, sind nicht mit älteren V6.6-Generatorzahlen gleichzusetzen.
