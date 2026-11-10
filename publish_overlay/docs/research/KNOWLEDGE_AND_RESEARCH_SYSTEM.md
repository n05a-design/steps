# Steps Knowledge Base – Fachsystem, Ingestion, Reconciliation und wachsende Bibliothek

**Entscheidungsstatus:** vorgeschlagenes Zielsystem; keine bestätigte produktiv befüllte Quellenregistry. **Forschungsanker:** [Research Foundation](https://github.com/n05a-design/steps/blob/75329fef46878a5ac816cef3690e612a9e8fe52c/research/notes/deep-research/legacy/01_STEPS_Research_Foundation.md), [Product Blueprint](https://github.com/n05a-design/steps/blob/75329fef46878a5ac816cef3690e612a9e8fe52c/research/notes/deep-research/legacy/02_STEPS_Knowledge_Base_Product_Blueprint.md), [PROJECT_CONTEXT_HANDOVER](https://github.com/n05a-design/steps/blob/75329fef46878a5ac816cef3690e612a9e8fe52c/research/notes/deep-research/legacy/PROJECT_CONTEXT_HANDOVER.md), [Codex-KB-Auftrag](https://github.com/n05a-design/steps/blob/75329fef46878a5ac816cef3690e612a9e8fe52c/research/notes/deep-research/legacy/04_CODEX_KNOWLEDGE_BASE_FOUNDATION_PROMPT.md).

## 1. Drei Ebenen – kein „Skill = Bücher in einen Prompt“

1. **Original- und Provenienzschicht:** lokal zugängliche und rechtlich geprüfte Originaldateien, bibliografischer Datensatz, Hash, Ausgabe, URL/DOI, konkreter Fundort. Rohkopien können *privat* bleiben. Ein Git-Dateiname begründet weder vollständigen Textimport noch erlaubte Weitergabe.
2. **Kanonische, originär formulierte Wissensschicht:** Concept-, Claim-, Relation-, Example-, Rule- und Testobjekte mit eigenen IDs, expliziter Geltung, Mehrdeutigkeit und Zitierstellen. Diese Schicht ist der eigentliche Wert für die App und die KI-Agenten.
3. **Zugriffsschicht:** Skill/Agent-Router, Suchindex/CLI/API, UI-Erklärung, Tests. Ein Skill informiert die Agenten bei Benutzung, er ersetzt keine Referenzdatenbank und trainiert kein externes Sprachmodell dauerhaft.

Das bestehende Steps-Repository hat `knowledge/sources/registry.yaml` mit `sources: []` und wenige Platzhalter-Ordner. Dem stehen historische 20 Initialquellen, 1.000 Dateien im V6.6-Legacybaum und sieben Research-/Handoverdokumente gegenüber. **Daher: Bibliotheksdateien vorhanden ≠ fachliche Wissensbasis eingepflegt.** Die 49 Legacy-Hauptordner mit doppelten Präfixen `21_*`/`39_*` bleiben Quellenablage; keine unkritische Fusion nach Nummer oder Dateiname.

## 2. Entitäten und Prüfkriterien

| Objekt | Minimalfelder | Muss verifiziert werden | Antipattern |
|---|---|---|---|
| `Source` | `source_id`, Titel, Autor (nullable), Ausgabe/Datum, Original-URL/DOI, `local_path`, SHA, `rights_status`, `ingest_status`, Reviewer | Identität, tatsächlicher Bytebestand, Nutzungszweck und Weitergaberecht | Titel aus Dateiname als gesichert, `CC BY` pauschal |
| `Extract` | Source-ID, Parser/Version, Zeichencodierung, Seiten-/Abschnittslocator, Fehlerquote, `extraction_sha`, Zeitpunkt | Quelltext und Locator rückführbar | Text als angeblich „vollständig gelesen“ ohne Parserbericht |
| `Claim` | claim-ID, original paraphrased wording, Locator, Scope/Framework, Evidenztyp, Status, Konfliktlinks | Quellenstelle belegt Anspruch, eigene Paraphrase abgegrenzt | Interview/YouTube als normatives Musikgesetz |
| `Concept` | dauerhafte ID, Bezeichnung und Aliasse, Definitionen nach Framework, prerequisites, applies_to | mehrere Quellen/Geltung, keine erfundene Konsensdefinition | Harmonieschulen stillschweigend zusammenlegen |
| `Relation` | Typ, gerichtete Argumente, Vorbedingungen, Kontext, Quelle/Regel-ID | symmetrisch vs gerichtet, Gegenbeispiele | `DOMINANT_OF` als symmetrisches Nachbarpaar |
| `Example` | synthetische eigene Folge, Tonalität, Modus, Notation, Zeitachse, erwartete Analyse, Tests | tatsächlich auflösbar und ohne geschützten Songtransfer | Kopie aus vollständigem Song/Sheet-Music |
| `Rule/Test` | `rule_id`, Inputs, erwartete Outputs, Framework und negativer Gegenfall, Testcode | unabhängig reproduzierbar | `confidence=.95` als ungeprüfte Wahrscheinlichkeit |
| `Revision` | import batch, previous/current source hash, reviewer, changed claims, rollback | idempotente Änderungsfolge | zweimaliger Crawl überschreibt Geschichte |

## 3. Fachliche Taxonomie ist breit, Produkt-MVP schmal

**Kern, sofort:** Tonklassen/Note Spelling/Oktaven/Intervalle; Skalen/Modi und Tonalität; Akkorde (Identity vs. Spelling vs. Voicing vs. Symbol vs. Funktion); harmonische Progression, Rhythmusposition, Stimmführung; alternative Deutungen und theoretische Linsen (klassische Funktionsharmonik, Jazz, Pop, modal, transformational). **Mitstrukturieren:** Motive, Melodieharmonisierung, Reharmonisierung, Notation, MIDI/MusicXML/JAMS, Drums/Grooves, kulturelle und historische Kontexte, kognitive Theorie, Didaktik. **Archivieren, später bewerten:** komplette Produktionskette Recording/Synthesis/Mixing/Mastering, Ableton-Interviews und Kurse, Video/Live, Distribution. Ein Fachbestand ist kein App-Featureversprechen.

Die musikwissenschaftliche Unterscheidung **theoretische Regel / empirisches Korpusmuster / kreative Heuristik** muss durch sämtliche Wissens-, Engine- und UI-Schichten erhalten bleiben. Stilbezogene oder kulturgebundene Erklärungen nicht als universell deklarieren. `music21`, Open Music Theory, ChoCo, Billboard, MusicXML und JAMS sind zunächst **Prüf- oder Forschungsreferenzen**, keine behaupteten integrierten Laufzeitabhängigkeiten.

## 4. Ingestion-Lifecycle: idempotent, inkrementell, überprüfbar

| Phase | Eingang | Ausgang | Stop-Gate |
|---|---|---|---|
| I00 Erlaubnis & Auftrag | Quelle/URL, erwartete Verwendung, verantwortlicher Auftraggeber | source request mit Nutzungsrechten/Robots-/Datenschutz-Check | gesperrte oder unklare Veröffentlichung |
| I01 Inventar | Dateibaum/URL-Liste | `candidate_source_registry`, SHA, canonical URL, charset, Sprachgruppe | reale Originale nicht auffindbar |
| I02 Sicherung & Quarantäne | originale Bytes | unveränderliche private Ablage, Source-ID, Hash | Pfad traversal, gefährlicher Dateityp, zu groß |
| I03 Extraktion | erlaubte Quellen | Textsegmente, Parserdiagnose, Seitenanker, Extraktionshash | nicht validierbarer Locator, zerstörter Text |
| I04 Claim-Aufbereitung | Segmente | eigene kurze Claim-/Conceptkandidaten mit Zitieranker | nur Modellvermutung statt Quellenbeleg |
| I05 Konfliktvergleich | bestehende IDs + neue Kandidaten | Alias-/Konfliktcluster, alternative Lenses, Change Delta | Semantik versehentlich überschrieben |
| I06 Fach-/Rechte-Review | Konfliktqueue, Originalstelle | accepted/rejected/needs_review, Reviewer, Lizenzstatus | fehlende menschliche/rechtliche Freigabe |
| I07 Golden Tests | fachliche Regeln, positive/negative Beispiele | Fixtures und Regressionen | nicht reproduzierbar, kein Grenzfall |
| I08 Veröffentlichung | reviewed objects + public/private scope | versionierter KB-Release, Manifest, Changelog | nicht erlaubte Volltexte/Assets |
| I09 Nutzung/Monitoring | Queries, Citation audit | Lexikalsuche/Skill/UI, Drift- und Frischehinweise | falsche Quellenzitate oder veraltete Claims |

**Inkrementalität:** Canonical URL + Edition/Datei-SHA sind keine universell austauschbaren Identitäten. Dasselbe Buch in neuer Auflage bleibt verknüpft, aber versioniert; eine übersetzte Webseite ist eine Sprachvariante, kein automatisch gleichwertiger Claim. Zwei Hash-identische Dateien können als absichtliche Historie separat referenziert werden. `batch_id`, `first_seen`, `last_checked`, `extractor_version`, `reviewer`, `previous_sha`, `changed_claim_ids` und `rollback_manifest` pro Verarbeitungslauf.

## 5. Retrieval-Kriterien und Prompt-Injection-Abwehr

**Version 0:** strukturierte YAML/JSON-Daten + deterministische Exaktsuche/Tokenindex; Quellstelle und Status immer anzeigen. **Version 1 nur nach Messung:** BM25/SQLite FTS oder semantische Embeddings gegen exakt dieselben 20–50 realistischen Evalfragen testen. **Keine voreilige Graphdatenbank.** Evaluationsklassen: korrektes Konzept, vollständig unterstützte Quelle/Locator, bewusstes Nichtwissen, richtige Alternativanalysen, kein langlebig falscher Quellenlink, korrektes Nutzungsrecht. Metriken: Treffer@k, Citation Precision, False-Support-Rate und Gegenbeispiel-Handling; fehlende Quellstellen nicht als Treffer werten.

Ein HTML/PDF/Transcript ist *Dateninhalt*, nicht Agenteninstruktion. Crawler-/Dokumenttexte dürfen keine Shell-Befehle auslösen, zusätzliche APIs aufrufen, öffentliche Files schreiben oder Review-Status ändern. Trenne Quellenreader, extrahierende KI und publizierenden Agenten mit separaten Berechtigungen. Parserlimits: maximale Dateigröße, Seiten-/Zeichenbudget, Zeitlimit, Archive-Expandratio, No-Follow für Symlinks, keine Pfad-Traversal, erlaubte Contenttypen, gehashte Unterordner. Kein Upload privater Bücher an externe KI ohne entsprechende Recht-/Datenschutzentscheidung.

## 6. Rechts-/Veröffentlichungsrealität des bereits öffentlichen Repos

60 PDF-Dateien/ca. 452 MB sind im Steps-Repository nach älterem Audit aufgeführt; am aktuellen Snapshot 60 PDFs im Git-Tree bestätigt, **nicht** jede rechtlich einzeln geprüft. Das ist kein Beweis einer Rechtsverletzung, aber ein **zeitkritischer Rechte-Prüfauftrag**: Prioritäten nach fremden Verlagstiteln, Downloadquellen, Terms, Metadaten und Explizit-Lizenzen. Die MPL-2.0-Datei des App-Repos deckt Drittwerke nicht pauschal ab. Ein `git rm` beseitigt frühere öffentliche Git-Commits nicht. Keine rechtlich nicht autorisierte Korpus-Bereitstellung in ZIP, CI-Artifact oder Skill-Verteilung. Rechtliche Entscheidungen gegebenenfalls mit qualifizierter juristischer Prüfung.

## 7. Quellenportfolio und nicht auffüllbare Lücken

- **20 Initial-PDF/TXT:** Namen und beschriebene Bedeutung aus Original-Overview Kap. 3; manche Extraktion und Lizenz nur historisch behauptet. Erst mit Source Cards und Bytehash zu `reviewed` anheben.
- **Deep Research (7 Dokumente):** `research/notes/deep-research/legacy/`: two papers, Master Research Prompt, Handover-Prompt, Codex-KB-Prompt, generated Handover und Start-README. Ein Handover existiert bereits und ist Status `draft`; frühere Behauptung „fehlt“ ist nach heutigem HEAD zu korrigieren.
- **V6.6 / V6.7:** 1.000 tatsächliche Dateien im historischen V6.6-Baum; die V6.7-Skripte und die lokale Delta-Behauptung beweisen keinen aktuellen vollständigen Source-Ingest.
- **Ableton:** Interviewkandidaten und Blog-Katalogstände 28, 143, 199, 262, 609 etc. sind *verschiedene Grundgesamtheiten*; vor Aussagen über Abdeckungsquoten vollständige Datensatzlisten und Query-Scope fordern.
- **Styles/Kulturen:** Archivdichte in westlich-zentrierter Funktionsharmonik, Jazz/Pop und Ableton-Workflows ist kein Repräsentativitätsbeleg. Segmentbasiertes Coverage-/Sampling-Review erforderlich.

## 8. Vier Testbatches statt 1.000 Quellen auf einmal

**Batch A (Grundlagen):** 5 gut identifizierte, erlaubte Quellen; 10 Concepts, 20 Claims, 10 positive und 10 negative Examples; Rechte und Quellenverknüpfung sämtlich geprüft. **Batch B (Harmonik):** 10–20 funktionale/modale und Jazz-/Pop-Konzepte mit **unterschiedlichen Deutungen**. **Batch C (Progressions-/Korpusbeispiele):** rein synthetische musikalische Sequenzen, Spelling, Transposition, Measure/Tick-Layer, alternative Analysen. **Batch D (Drums/Produktion):** erst wenn Scope/Lizenz/Timemodel festgelegt; Metadaten vor fremden MIDI-Packs. Diese Zahlen sind **Abnahmevorschläge**, nicht vorhandener Bestand oder unausweichlicher Projektplan.

## 9. Kontinuierliche Wartung

`source-registry-check`, `id-reference-check`, `evidence-locator-check`, `license-gate`, `claim-diff-review`, `theory-fixture-check`, `retrieval-eval` und `public-export-scan` laufen bei jedem passenden PR. Jährliche oder quellenabhängige Revalidierung von Seiten-URLs, Lizenztexten und Korpusversionen; jede semantische Korrektur erzeugt `reason`, `supersedes` und Regressionstest. KI-Token-Guthaben dürfen nicht bestimmen, ob die Wissensbasis reproduzierbar ist – alle relevanten Fakten und Entscheidungen stehen versionskontrolliert außerhalb der Chats.

**Ausdrücklich nicht geliefert:** 20 neu reviewte Claims, real gepars­te PDFs, SQLite/Graphdatenbank, fertiger Retrieval-Indexer, lauffähiger Steps-Harmony-Engine-Code. Das sind zukünftige Arbeitspakete, keine Leistungen dieser Dokumentationsprüfung.
