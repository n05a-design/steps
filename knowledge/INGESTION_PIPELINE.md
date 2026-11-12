# Bibliotheks-Pipeline: Quelle → Claim → Wissen → Code

> Die [Pilotfreigabe](concepts/progressions/README.md) verbindet konkrete Fundstellen und Gegenchecks mit menschlichen, fassungsgebundenen Freigaben. App, Renderer und CI prüfen dieselben JSON-Daten und das Produktquellenregister. Der folgende Q0–Q6-Prozess beschreibt das weitergehende Ziel.


> **Kritischer Aktualitätsnachtrag (10.11.2026, nach GitHub PR #75):** Der folgende Basisteil stammt aus dem früheren Paket und kann für Glide `main` noch den historischen Commit `61a2f3a`/Version 3.50.7 nennen. Der erneut verifizierte Stand ist **Glide `9e767bea` (3.53.0)**; der hochgeladene `app.pyw` ist blobgleich mit diesem HEAD, nicht aber bereits alle weiteren Module und Ressourcen unabhängig verifiziert. Aktuelle Bewertungen und Entscheidungsgates stehen in [`docs/project/PROJECT_OVERVIEW.md`](../docs/project/PROJECT_OVERVIEW.md) und [`docs/audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md`](../docs/audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md). Aussagen im folgenden Basisteil bleiben als **historisch datierte Ausgangsnotizen** erhalten, keine unmarkierte aktuelle Wahrheit.

**Stand:** 10.11.2026 (Europe/Berlin). **Status:** Entwurf und Prüfauftrag, keine Umsetzung/Freigabe. **Referenzstände:** Steps `main` `75329fef46878a5ac816cef3690e612a9e8fe52c`; Glide `main` `61a2f3ac2f0e1880e7fd8c0f3cfd9da0d0c9f16d`; lokal bereitgestellter Glide-Code `3.53.0`, SHA-256 `d7e19151eb0862a8ff58c4cc5e7d06a0452cde1daa73830ff97f54247bc75271`.

**Evidenz:** `UPLOAD` = bereitgestellte Datei, `GITHUB` = gelesener Remote-Stand, `BERICHTET` = in Unterlagen behauptet, `VORSCHLAG` = neue Empfehlung, `OFFEN` = unbestätigt. Kein dokumentierter Test bedeutet nicht bestanden.

## Einheitlicher Prozess für neue Crawls, Dateien und Ordner

**Q0 Auftrag:** Zweck, Domain, Suchgebiet, erlaubte Quellen, Lizenzgrenzen, Crawl-Frequenz, erwartete Dateien und Datenschutz definieren. Bestand vor neuem Crawl abgleichen. Keine technischen Robots-/Nutzungsbedingungen umgehen; Captures mit rechtlicher Begründung.

**Q1 Inventar:** `source_id` aus kanonischem Identifier (DOI/ISBN/URL oder internem stabilen Alias), `work_id`, Titel/Autor/Auflage/Jahr/Sprache, `accessed_at`, `canonical_url`, `source_type`, `local_path`, `sha256`, `parent_snapshot`, License `UNKNOWN/RESTRICTED/VERIFIED`, `redistribution_allowed`, `derivative_text_allowed`, `reviewer`, `last_checked`, Status pro Quelle; Fehlwerte bleiben `null`, nicht erraten. Neue Verzeichnisnamen in Taxonomie erheben und auf Konflikt/Reserve prüfen.

**Q2 Extraktion:** Parser-Version, Seiten-/Kapitel-/Zeitstempel-/Notations-Locators, Ausgabe/Encoding, Confidence, Fehler/geschützte Passagen. Originalbytes unverändert, Extraktionsoutput gesondert, Text-Lizenz prüfen. OCR nur falls notwendig und mit Qualitätsprüfung.

**Q3 Claim-Extraktion:** Je Claim `claim_id`, `source_id`, locator, Originalaussage als kurze zulässige Zusammenfassung, fachliche Paraphrase/eigene Definition, `claim_type` (`theoretical_rule`, `descriptive`, `empirical_frequency`, `creative_suggestion`, `pedagogical`), `framework`, `styles`, `preconditions`, `confidence`, `potential_conflicts`.

**Q4 Konsolidierung:** semantische Duplikate als Referenzen statt neue Kopien; Gegenbeispiele und alternative Deutungen **niemals löschen**, sondern als `supports`, `contradicts`, `qualifies`, `supersedes`, `same_work_as` relational führen. Beispiel: `E7 → Am`: a-Moll primäre Dominante, C-Dur Zwischendominante V7/vi.

**Q5 Wissen:** `concept_id`, Definitionsscope, `source_claims`, explizite Rule-Vs-Interpretation, musikalisch korrekte Beispiel/Negativfälle, `tested_by`, Review/License, schema-Version. Unreviewed-Einträge nur in staging.

**Q6 Tests:** Schemas, Notationsroundtrip, Formate, enharmonische Schreibweise (F# ≠ Gb semantische Schreibung, gleicher Pitch Class), Stufen/Stimmführung, Roman Numerals und MIDI-Tempo. Jeder kanonische Regelclaim muss mindestens einen pass/fail Test oder eine explizite Testausnahme haben.

**Q7 Integration:** App benutzt validierte API/JSON/SQLite-Adapter, lädt keine 1000 Markdown-Dateien bei jedem Start. Suchindex kann generiert werden; Source-IDs/Versionen stabil halten. Skill führt dieselben Daten und einen genauen Retrieval-/Citation-Testpfad; Modellantworten ohne Locator als nicht belegt markieren.

**Q8 Pflege:** neue Crawl-Snapshots getrennt, Delta-Report, defekte URLs/License-Änderungen, Review-Queue, Changelog, Index-Gültigkeitskontrolle. Nur diff-basierte Aktualisierung bei späteren Crawl-Aufträgen.

## Typische Konflikte, die sichtbar bleiben müssen

- 20 historische Forschungsquellen vs 60 vorhandene PDF-Dateien im aktuellen Git-Tree: **keine Eins-zu-eins-Beziehung nachgewiesen**.
- V6.6 1.000 Files aktuell vs historische Übersichten mit anderen Summen: Scope/Version festhalten, nicht zusammenziehen.
- 21 und 39 doppelt nummeriert: eigene eindeutige IDs und Inhalte vergleichen; keine unprüfte Fusion.
- Alte Quellabdeckung-CSV erklärt 89 aus früheren sechs Dokumenten extrahierte Nachweiszeilen, nicht den Vollbestand der 1.931 Repo-Dateien.

## Prüfreport pro Lauf

Erzeuge `source_intake_<date>.json` mit Input-Manifest, Scope, Quellzahl, neue/aktualisierte/unveränderte/ausgeschlossene Quellen, Rechtsstatus-Counts, Claim-Review-Counts, kaputte Referenzen, Duplikat-Cluster, erzeugte Fixtures, SHA-Hashes, Programme/Versionen und ausdrücklich ungelesene/unverifizierte Originale. Kein öffentliches Git-Commit mit sensiblen PDF-Texten oder privaten Credentials.
