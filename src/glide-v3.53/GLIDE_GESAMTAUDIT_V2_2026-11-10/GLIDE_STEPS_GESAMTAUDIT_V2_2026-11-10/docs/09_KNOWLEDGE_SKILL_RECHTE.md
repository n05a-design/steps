# 09 — Forschungsbibliothek, Rechte, Knowledge Base und AI-Skill

## Nachgewiesene Größen sind keine Qualitätskennzahlen

Steps `main@75329fef` umfasst 1.931 Dateien, davon 1.810 Dateien unter `research/` und ~668,22 MB der insgesamt ~668,68 MB logischen Dateigrößen. 60 PDFs mit insgesamt 451.999.999 Bytes (rund 452 MB) befinden sich im öffentlichen Git-Tree. Ein älterer Repo-Audit nannte 1.827 Dateien und 2.043 Tree-Einträge; dies ist ein **historischer Stand**, keine Diskrepanz ohne zeitliche Einordnung. Die erneute Tree-Metadatenberechnung bestätigte 160 Gruppen blob-identischer Inhalte, 426 zusätzliche Pfade und ~115,69 MB logische Mehrfachablage. **Git speichert identische Blobs intern dedupliziert**; die Zahl ist kein tatsächlicher Pack-/Download-Sparwert.

Einige PDF-Dateinamen lassen auf Lehrbücher/kommerzielle Werke und auf möglicherweise unklare Erwerbsquellen schließen. Aus dem Namen allein folgt weder eine Rechtsverletzung noch eine Nutzungs-/Redistributionslizenz. **Aber:** Bei bereits öffentlich versionierten Dateien muss die Rechteklärung priorisiert und nicht erst vor einem späteren Steps-Installer vorgesehen werden. Zudem enthält `research/competitors/` heruntergeladene Screenshots/HTML. Der Quellcode MPL-2.0 verleiht **keine** Nutzungsrechte an diesen Werken. Eine öffentlich verlinkte Bibliothek ≠ allgemeines Gemeingut.

## Vier Statusräume

1. **Archive:** unverändertes Rohmaterial mit SHA-256, lokaler Rechteklasse, Ursprung und Zugriffsbeschränkung. Öffentliches Repository darf nur enthalten, was dort rechtmäßig liegt; private Dateien sicher getrennt von Programmdaten/Repository.
2. **Research:** synthetisierte Forschung, alternative Hypothesen, Unsicherheiten und Quellenkritik, ausdrücklich kein Produktentscheid.
3. **Knowledge:** eigene definierte `Concept`, `Rule`, `Relation`, `Example`, `Claim`, `Citation` Records samt Source-ID/Edition/Fundstelle, Fachreview, Rechte-/Anwendbarkeitsstatus. Ein `verified`-Label ohne tatsächliche Prüfung ist ungültig.
4. **Skill:** Lese-/Analyse-/Antwort- und Toolworkflow mit wenigen Indexdateien. Kein paralleles Lehrbuch, keine heimliche Kopie geschützter Quellen, kein Ersatz für die Domain-Engine.

**Aktueller Stand:** `knowledge/sources/registry.yaml` enthält **0** Source-Records; `knowledge/concepts/` ist weitgehend nur Platzhalter. Root-`SKILL.md` ist ein Workflow-Index; der Harmony-Coach unter `skills/music-harmony-coach/...` besitzt einen ausführlicheren Instruktionsentwurf, aber kurze Referenzen ohne die versprochene fachliche Vollabdeckung. Das sind wertvolle Vorarbeiten, keine bereite fachliche QA.

## Source- und Claim-Nachweisschema

Für jede tatsächlich gesehene Quelle: `source_id`, Art, Work/Edition/Author, URL/DOI/Fundstelle, Bytes/SHA, Dateistand, RightsStatus, AllowedUses (local_analysis, internal_summary, public_paraphrase, redistribution, audio_distribution), Reviewer, LastReview, Primary/Secondary/Bias, CopyrightHolder, Retention, Link. Keine allein aus Dateinamen erzeugten `verified`-Labels.

Für jede Fachbehauptung: `claim_id`, `concept_id`, `statement`, `operational_conditions`, `style_theory_lens`, `evidence_locator`, `source_id`, `status`, `disagreements`, `test_case_id`, `knowledge_revision`. Dokumentierte Gegenaussagen dürfen nicht zusammengeglättet werden. Textliche Ähnlichkeit mehrerer Quellen ist keine gleiche Definition.

**Gate:** `rights_status=unknown` → nicht in öffentlich distribuierten Rohdaten/Models/Bundles; bei Zitat/Paraphrase die konkrete zulässige Nutzung getrennt bewerten. Ein pauschales 'nur Zitate' ersetzt keine rechtskonforme oder datenschutzrechtliche Prüfung. Vor einer Git-Historienänderung juristische/technische Beratung und separates, autorisiertes Verfahren.

## Ingestion als nachvollziehbare Pipeline

1. **Inventory:** Datei-/Blob-/URL-IDs, Quellstand, Hash, Format, DuplicateGroups, Lizenzhinweise, Metadatenkonflikte; Intake startet read-only.
2. **Rights Gate:** Prüfer entscheidet pro Quelle Nutzungs-/Weitergabestatus. Verdachtsfälle pausieren; nur lizenzfähige, eigene oder reine Metadaten weiter.
3. **Extraction:** Original bleibt unverändert, extrahierte Notizen separat, Page/Section/Timecode zurückverfolgen, dokumentierte OCR-/Encoding-/Tabellenfehler; PDF nicht blind per OCR als fachlich korrekt übernehmen.
4. **Semantische Normalisierung:** Begriffssystem/Tonnotation, Quellenstile, konkurrierende Analysen trennen, unabhängige Quellverifikation; `H`/`B`/`Bb` und Akkordsymbole konsistent.
5. **Schema-/Rule/Linkcheck:** Alle `source_ids` referenzieren echte zulässige Quellen; ein Claim hat eine verifizierbare Quelle und Domain-Test; Quellstatuspropagation bei Rücknahme einer Lizenz.
6. **Publication Filter:** Öffentliche, private und nicht zitierfähige Daten aus separaten Profilen bauen, exakt auflisten, `dry-run`-Manifest und redigierte Quellenangaben kontrollieren; keine Original-PDFs als Nebenprodukt.
7. **Skill Evaluation:** Fragen/Relevanzprüfung, korrekte Fundstellen, Failure-to-answer bei fehlenden Belegen, alternative Interpretationen, keine erfundenen Seitenzahlen, keine geschützten Großtextreproduktionen.
8. **Revisions-/Retrievalpflege:** Neuer Researchstand -> neue verlinkte Claims, kein Überschreiben historischer Entscheidungen; diff inkl. Betroffene UI-Lehrtexte und Golden-Tests.

## Deduplikationsstrategie ohne Verluste

- **Binär identisch** (SHA/Git Blob) ≠ **semantisch deckungsgleich** ≠ **historisch austauschbar**. Jede identische Kopie kann einen unterschiedlichen Verwendungs-/Quellkontext besitzen. Physische Löschung nur nach Registry-, Zitierungs-, Link-, Lizenz- und History-Review.
- Versionierte V6.6/V6.7-Dateien nicht blind mergen, insbesondere zwei Bereichsnummern `21` und `39` mit unterschiedlichen Themen.
- Alte Indexzahlen (z. B. „1.146 Dokumente“ oder „199/262 Ableton-Artikel“) bleiben historische Bezugsgrößen mit eigenem Korpus und Zeitraum; eine aktuelle Anzahl im Tree lässt sich nicht daraus errechnen.
- Zentrale `knowledge/sources/registry.yaml` und Concept-IDs sind **führende Quellen**; `SKILL.md` verweist darauf, keine alternative Claim-Datenbank.

## Fachliche Validität und alternative Methoden

Ein rein vektorbasierter Retrieval-Ansatz kann bei Musiktheorie kontextlose Aussagen verknüpfen; ein rein regelbasiertes System kann stilistische Variation nicht abbilden. **Empfehlung:** deterministische Pitches/Intervals/Chords als Code, erklärte Regelrelationen mit Provenienz und expliziten Kontextbedingungen als Knowledge; probabilistische/historische Musik-Korpora nur als *spätere Gewichtung*. ML/LLM für Erklärungen darf Nichtwissen und mehrere Lesarten ausgeben; verifizierte Algorithmen bleiben überprüfbar und deterministisch.

**Externe Datenquellen (noch zu prüfen):** ChoCo, When in Rome, Open Music Theory, music21, DCML, annotierte MIDI-/Groove-Korpora; für jede Quelle getrennte Lizenz/Terms, Herkunft, Bias, Edition, Format und wiederholbare Fachcases erforderlich. Keine Behauptung über ihre Freigabe im aktuellen Steps-Repo.

## Qualitative Skill-Tests

- Für `E7→Am` je nach Tonart V7–i oder V7/vi; mit Alternate Framework zulässig.
- Ohne Quellen-ID darf keine präzise Buchseite/Studienzahl erfunden werden.
- Bei Quellwiderspruch werden verschiedene Stile/Schulen und Grade der Evidenz erklärt.
- Strukturiertes Objekt muss das aktive JSON-Schema **und** fachliche Invarianten erfüllen.
- Skill-Antwort enthält keine ungefragt erzeugte lokale Netzverbindung oder hidden source path.
- Negative Testsets (Halluzinieren, falsche Notation, unzulässiges Zitat, fehlender Kontext, ungültige MIDI-Dauer) sind Teil jeder Skill-Revision.

## Rechtliche Referenzen und Warnhinweise

- Mozilla MPL 2.0: https://www.mozilla.org/en-US/MPL/2.0/ und FAQ https://www.mozilla.org/en-US/MPL/2.0/FAQ/ — file-level copyleft bei Covered Software; **kein** Freibrief für fremde Buch-/Musik-/Bilddateien.
- GitHub-Historienrisiken: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository — auch nach Entfernen aus aktuellem Tree können alte Klone, Forks und Commit-SHAs betroffen bleiben. History-Rewrite riskiert beschädigte PRs/Signaturen und Wiedereintrag.

**Keine Rechtsberatung:** Sichtbare Dateinamen und Metadaten begründen eine hohe *Prüfpriorität*, kein abschließendes Urteil über jede Datei. Bis zur Rechteklärung keine zusätzlichen fremden Materialien in öffentliches Git oder in das neue Gesamtpaket übernehmen.
