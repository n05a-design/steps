# 33 Untersuchungsdimensionen – Abdeckungs- und Nachweismatrix

**Stand:** 10.11.2026. **Bewertung:** fachliche Audit-Schätzung, keine objektiv gemessene „Prozentvollständigkeit“. `V1-Tiefe` bezeichnet, wie weit der Erstbericht den Untersuchungsaspekt operativ abgedeckt hat, **nicht**, ob das Projekt selbst fertig ist. Jede Zeile hat einen konkreten Prüfbeweis, der noch einzuholen ist.

**Insgesamt:** 33 Dimensionen, gruppiert nach Produkt, Fachwissen, Technik, Daten, Design und Governance. Matrix maschinenlesbar in `manifests/INVESTIGATION_COVERAGE_33_V2.csv`.

## Produkt

### D01 – Vision und Abgrenzung (P0; V1: teilweise)
**Vorherige Grenze:** P1–P5 beschrieben, aber Vision/MVP/Produktlinie nicht entschieden.
**Ergänzung:** Versionierte Product Charter mit Erfolgskriterien, Ausschlüssen und Falsifikatoren. Primärer Arbeitsnachtrag: `docs/product/PRODUCT_STRATEGY_AND_MVP.md`.
**Noch ungeklärt / Gate:** Owner-ADR, Zielgruppen- und Nutzertest.

### D02 – Nutzerszenarien und Jobs-to-be-done (P1; V1: knapp)
**Vorherige Grenze:** Personas ohne echte Beobachtungen, keine identifizierten Kernaufgabenketten.
**Ergänzung:** Konkrete Aufgaben, Testaufbauten, Onboarding- und Abbruchkriterien je Persona. Primärer Arbeitsnachtrag: `docs/product/PRODUCT_STRATEGY_AND_MVP.md`.
**Noch ungeklärt / Gate:** 5 repräsentative Usability-Sitzungen oder begründete Proxy-Tests.

### D03 – MVP-Scope Chords und Drums (P0; V1: teilweise)
**Vorherige Grenze:** Drums behalten, aber ohne begründeten Sequenzierungsentscheid.
**Ergänzung:** Vergleich Harmonie-only, dualer Minimal-Slice und Rhythm-first mit Kosten-/Nutzen-Gates. Primärer Arbeitsnachtrag: `docs/audit/03_ALTERNATIVEN_UND_ENTSCHEIDUNGEN.md`.
**Noch ungeklärt / Gate:** ausdrücklicher Scope-ADR.

### D04 – Wettbewerb und Differenzierung (P1; V1: teilweise)
**Vorherige Grenze:** ältere Marktbehauptungen ungeprüft; keine aktuelle Primärquellenmatrix.
**Ergänzung:** Hersteller-Funktionsvergleich, überprüfbare Hypothese „erklärbare Verbindungen“. Primärer Arbeitsnachtrag: `docs/product/MARKET_AND_VALIDATION.md`.
**Noch ungeklärt / Gate:** Demo-/Feature-Test mit identischen Tasks.

### D05 – Eingabe-/Navigationskonzept (P0; V1: knapp)
**Vorherige Grenze:** „2 Fenster“ auf 2 Pane-Vermutung reduziert.
**Ergänzung:** Begriffe, Navigationsmodell, Arbeitsbereich, Kollaps-/Tastatur-Matrix. Primärer Arbeitsnachtrag: `docs/engineering/SHELL_EXTRACTION_DEEP_SPEC.md`.
**Noch ungeklärt / Gate:** UI-ADR und Walkthrough.

### D06 – Lernziele und Didaktik (P1; V1: Lücke)
**Vorherige Grenze:** keine Kompetenzstufen, Lernpfad, Feedback-/Fehlerdidaktik.
**Ergänzung:** Lern-Outcome-Matrix, adaptive Hilfen, Fehlkonzepte, didaktische Bewertung. Primärer Arbeitsnachtrag: `docs/product/LEARNING_AND_EXPERIENCE.md`.
**Noch ungeklärt / Gate:** fachliche Review von Aufgaben und Lernerfolg.

### D07 – Accessibility und Inklusion (P1; V1: teilweise)
**Vorherige Grenze:** Designschutz genannt, aber kein kompletter Tastatur-/Screenreader-/Motion-Vertrag.
**Ergänzung:** Fokusmatrix, Beschriftungen, Kontrast, Farbenblindheit, reduzierter Bewegung, Performance. Primärer Arbeitsnachtrag: `docs/product/LEARNING_AND_EXPERIENCE.md`.
**Noch ungeklärt / Gate:** native A11y-Matrix pro Plattform.

### D08 – Internationalisierung und Musiknotation (P1; V1: teilweise)
**Vorherige Grenze:** DE H/B korrekt erkannt, aber kein echter lokalisierbarer Eingabevertrag.
**Ergänzung:** Parser-/Spelling-/Display-Locales, Fehlerfälle, Text-/Hilfestrategie. Primärer Arbeitsnachtrag: `docs/engineering/MUSIC_DOMAIN_AND_MIDI.md`.
**Noch ungeklärt / Gate:** Notationstransformations- und UX-Test.

## Fachwissen

### D09 – wissenschaftliche Taxonomie und Geltung (P0; V1: teilweise)
**Vorherige Grenze:** keine kontrollierte Konzept-Hierarchie oder Framework-Konflikte produktiv.
**Ergänzung:** Konzept-/Claim-Layer mit mehreren Theorieschulen und Gegenbeispielen. Primärer Arbeitsnachtrag: `docs/research/KNOWLEDGE_AND_RESEARCH_SYSTEM.md`.
**Noch ungeklärt / Gate:** goldene Theory-Fixtures+Review.

### D10 – Quellenbestand und Rechte pro Quellobjekt (P0; V1: teilweise)
**Vorherige Grenze:** Registry leer; Git-Files als Inhalt gezählt.
**Ergänzung:** Source-Registry + Bytehash + Nutzungsrecht + Locator + Verfallsprüfung. Primärer Arbeitsnachtrag: `docs/research/KNOWLEDGE_AND_RESEARCH_SYSTEM.md`.
**Noch ungeklärt / Gate:** samplegestützter Provenienz-Audit.

### D11 – zwei Deep-Research-Papiere und Übergabe (P0; V1: fehlend)
**Vorherige Grenze:** sieben vorhandene Research-Dateien nicht im V1-Quellenkontext abgebildet.
**Ergänzung:** neuer Research-Quellkanon samt Handover-/Codex-Prompt-Konfliktprüfung. Primärer Arbeitsnachtrag: `docs/audit/02_KORREKTUREN_UND_WIDERSPRUECHE.md`.
**Noch ungeklärt / Gate:** Inventar der sieben Dateien+Owner Review.

### D12 – Ingestion, Crawling, incremental updates (P1; V1: teilweise)
**Vorherige Grenze:** nur grobe Pipeline; keine Idempotenz/Update-/Rechte-Policy.
**Ergänzung:** Kanonisierung, versionierte Delta-Batches, Parser-Evidenz, Review, Snapshot. Primärer Arbeitsnachtrag: `docs/research/KNOWLEDGE_AND_RESEARCH_SYSTEM.md`.
**Noch ungeklärt / Gate:** zweifacher Import ohne neue Claims.

### D13 – Wissensretrieval und AI Skill (P1; V1: teilweise)
**Vorherige Grenze:** Skill-Ansatz ohne Retrieval-Metrik und Halluzinationskategorien.
**Ergänzung:** RAG-vs-Lexikalsearch, Evals, citation-matching, Provider-Neutralität. Primärer Arbeitsnachtrag: `docs/research/KNOWLEDGE_AND_RESEARCH_SYSTEM.md`.
**Noch ungeklärt / Gate:** 20+ dokumentierte Evals mit Belegen.

### D14 – Korpora, Verzerrungen, Musikkulturen (P2; V1: Lücke)
**Vorherige Grenze:** Genre-/Stilabdeckung ohne kuratorische Sampling-/Bias-Methodik.
**Ergänzung:** Style/Musiktradition/Annotation/Corpus-Bias als expliziter Forschungsstrang. Primärer Arbeitsnachtrag: `docs/research/KNOWLEDGE_AND_RESEARCH_SYSTEM.md`.
**Noch ungeklärt / Gate:** Coverage- und Bias-Review pro Korpus.

### D15 – Deduplizierung und semantische Varianten (P0; V1: teilweise)
**Vorherige Grenze:** 426 Git-Blob-Duplikate gezählt, keine Review-Entscheidung.
**Ergänzung:** 3-stufiger Hash/CanonURL/Concept-Clustering-Prozess, niemals blind löschen. Primärer Arbeitsnachtrag: `docs/research/KNOWLEDGE_AND_RESEARCH_SYSTEM.md`.
**Noch ungeklärt / Gate:** Referenz-/Inhaltsverlust gleich null.

## Technik

### D16 – Glide-Reuse-Modulabgleich (P0; V1: teilweise)
**Vorherige Grenze:** 94 Module nur summarisch, kein abnahmeorientiertes Einzelmapping.
**Ergänzung:** 94-Zeilen-Reuse-CSV, 25-Pakete-CSV, konkrete Isolation-Gates. Primärer Arbeitsnachtrag: `manifests/GLIDE_94_MODULE_REUSE_AUDIT_V2.csv`.
**Noch ungeklärt / Gate:** repräsentative Modul-Ports getestet.

### D17 – Glide-Monolith und Laufzeit-Side-Effects (P0; V1: unterschätzt)
**Vorherige Grenze:** Bilder/Methodennamen bekannt, aber Importzeit-Globaländerungen nicht systematisch.
**Ergänzung:** AST-Klassen, 1.866 Methoden, Side-Effect-Register, importfreier Auszugsplan. Primärer Arbeitsnachtrag: `docs/engineering/SHELL_EXTRACTION_DEEP_SPEC.md`.
**Noch ungeklärt / Gate:** kein Glide-Datenkontakt beim Steps-Start.

### D18 – Alternativen zur Glide-Abzweigung (P0; V1: Lücke)
**Vorherige Grenze:** Fork-and-prune als impliziter Standard.
**Ergänzung:** Vergleich Fork/Extract/Hybrid/Scratch auf Aufwand, Regessions-/Lizenzrisiko. Primärer Arbeitsnachtrag: `docs/audit/03_ALTERNATIVEN_UND_ENTSCHEIDUNGEN.md`.
**Noch ungeklärt / Gate:** zwei Prototypen mit identischem UI-Slice.

### D19 – Architekturports, Lifecycle, asynchrone Jobs (P0; V1: teilweise)
**Vorherige Grenze:** benannte Ports ohne Event-/Thread-/Cancellation-Vertrag.
**Ergänzung:** Eventgrenzen, Generation-ID, UI-Thread, Cancellation, Race/Shutdown. Primärer Arbeitsnachtrag: `docs/engineering/SHELL_EXTRACTION_DEEP_SPEC.md`.
**Noch ungeklärt / Gate:** konkurrierende Events deterministisch geprüft.

### D20 – Domänenmodell Pitch/Chord/Progression (P0; V1: teilweise)
**Vorherige Grenze:** grobe Modellbegriffe, noch kein metrischer Normalisierungs-/Spelling-Vertrag.
**Ergänzung:** kanonische Entitäten, Invarianten, negative Tests, Domain von UI getrennt. Primärer Arbeitsnachtrag: `docs/engineering/MUSIC_DOMAIN_AND_MIDI.md`.
**Noch ungeklärt / Gate:** schema+domain golden fixtures.

### D21 – Audio-/MIDI-Timing und Portabilität (P1; V1: teilweise)
**Vorherige Grenze:** nur SMF-Roundtrip allgemein, keine Tick-/Tempo-/Notenaus-Fälle.
**Ergänzung:** PPQ, Tempo-Map, Notenüberlappung, Stopp/Seek/Loop, Fallback, Drift. Primärer Arbeitsnachtrag: `docs/engineering/MUSIC_DOMAIN_AND_MIDI.md`.
**Noch ungeklärt / Gate:** SMF-Files + Clock-Simulation + OS Proben.

### D22 – Drum/Chord gemeinsames Zeitmodell (P1; V1: knapp)
**Vorherige Grenze:** Drums als Nachfolgephase, Rhythmusarchitektur fehlte.
**Ergänzung:** Bars/Beats/Ticks, velocity/swing/humanize, Pattern-Versioning. Primärer Arbeitsnachtrag: `docs/engineering/MUSIC_DOMAIN_AND_MIDI.md`.
**Noch ungeklärt / Gate:** deterministische Groove-/Exportfixtures.

## Daten

### D23 – Save/Load/Migration/Recovery (P0; V1: teilweise)
**Vorherige Grenze:** JSON+atomic writer vorgeschlagen, nicht auf Crash-/Schema-Fälle gemappt.
**Ergänzung:** Migrations- und Dirty-State-Vertrag, Rollback, getrennte Datenroots. Primärer Arbeitsnachtrag: `docs/engineering/DATA_STORAGE_AND_PORTABILITY.md`.
**Noch ungeklärt / Gate:** Power-loss/Lock/Corrupt/Restore Tests.

### D24 – Suche, Index, semantischer Graph (P1; V1: knapp)
**Vorherige Grenze:** Recherche und App-Suche zu stark vermischt.
**Ergänzung:** separate domänenbezogene Sucharten, progressive Lexikal/Semantik-Entscheidung. Primärer Arbeitsnachtrag: `docs/research/KNOWLEDGE_AND_RESEARCH_SYSTEM.md`.
**Noch ungeklärt / Gate:** präzise Retrieval-Evaluation.

### D25 – Performance und Ressourcen (P1; V1: teilweise)
**Vorherige Grenze:** Glide-Zahlen nicht Steps-Baseline; willkürliche Schwellen drohen.
**Ergänzung:** Messprotokoll mit echten Workloads, memory/cold-start/latency. Primärer Arbeitsnachtrag: `docs/quality/VERIFICATION_PLAN_V2.md`.
**Noch ungeklärt / Gate:** gleiche Maschine/Daten vor-nach.

## Design

### D26 – Theme/Tokens/Schriften/Assets (P0; V1: teilweise)
**Vorherige Grenze:** erhaltene Design-Regeln erwähnt, aktuelle D77/Fontmatrix nicht integriert.
**Ergänzung:** vollständiger UI-Erhaltungscontract; Lizenz der einzelnen Fontdateien. Primärer Arbeitsnachtrag: `docs/engineering/SHELL_EXTRACTION_DEEP_SPEC.md`.
**Noch ungeklärt / Gate:** 4 Stile x Gewicht x Theme x DPI.

### D27 – Responsive/Fokus/Kompaktmodus (P0; V1: teilweise)
**Vorherige Grenze:** No-op-Sidebar ohne transitive Eventmatrix.
**Ergänzung:** Sichtbarkeit, Shadow actions, Shortcuts, Deep links, Input/Focus. Primärer Arbeitsnachtrag: `docs/engineering/SHELL_EXTRACTION_DEEP_SPEC.md`.
**Noch ungeklärt / Gate:** Tastatur+Fenster+Menü Regression.

## Governance

### D28 – Security Privacy Supply-Chain (P0; V1: knapp)
**Vorherige Grenze:** Lizenz & SBOM genannt, keine Threat- und Datenflussmodellierung.
**Ergänzung:** Threat Modell für PDFs/ZIP/HTML/MIDI/Parser, Injection/Secrets, least privilege. Primärer Arbeitsnachtrag: `docs/quality/SECURITY_AND_RIGHTS_GATE.md`.
**Noch ungeklärt / Gate:** automatisierte und manuelle Threat Checks.

### D29 – Lizenz, bereits öffentliche Fremdwerke (P0; V1: teilweise)
**Vorherige Grenze:** Fremd-PDFs bemerkt, keine konkrete Eskalationsroute.
**Ergänzung:** Pro Objekt Recht, Historie, git-filter-repo nur koordiniert, nicht automatisch. Primärer Arbeitsnachtrag: `docs/quality/SECURITY_AND_RIGHTS_GATE.md`.
**Noch ungeklärt / Gate:** Rights-Matrix und publikationsfähiger Checkout.

### D30 – GitHub-Stand, Tags, PR und Release (P0; V1: teilweise)
**Vorherige Grenze:** V1 remote main Glide 3.50.7 veraltet; push:true nicht ausreichend.
**Ergänzung:** jetzt Glide 3.53.0, Git Blob-Match, PR #74/#75, Release-Gates getrennt. Primärer Arbeitsnachtrag: `docs/audit/02_KORREKTUREN_UND_WIDERSPRUECHE.md`.
**Noch ungeklärt / Gate:** neuer CI-/Build-/Release-Nachweis.

### D31 – Multimodell-KI-Agenten / Tokenlimit (P1; V1: teilweise)
**Vorherige Grenze:** rollenbasierte Aufgabenteilung ohne Commit-/Failure-/Review-Protokoll.
**Ergänzung:** Repository-first, branches, task ledger, confidence and handover budgets. Primärer Arbeitsnachtrag: `docs/operations/AGENT_COLLABORATION_PROTOCOL.md`.
**Noch ungeklärt / Gate:** 2-Agenten-Simulation ohne Konflikt.

### D32 – Projektsteuerung/Timeline/Entscheidungen (P1; V1: teilweise)
**Vorherige Grenze:** Phasenliste ohne Kapazitätsmodell oder konkrete Meilensteinprüfung.
**Ergänzung:** Gates + Ressourcenabhängigkeit + kill/switch criteria + ADR-RACI. Primärer Arbeitsnachtrag: `docs/operations/EXECUTION_BACKLOG.md`.
**Noch ungeklärt / Gate:** Owner-Zuordnung und Sprint Review.

### D33 – Berichtsvalidierung, Traceability, Qualitätsaudit (P0; V1: Lücke)
**Vorherige Grenze:** keine lückenlose Source→Requirement→Decision→Implementation→Test-Kette.
**Ergänzung:** Anforderungs-IDs, Evidenz-/Stufenregister, dokumentierte Negativbefunde. Primärer Arbeitsnachtrag: `docs/quality/VERIFICATION_PLAN_V2.md`.
**Noch ungeklärt / Gate:** traceable examples und Artifacts QA.

## Auswertung der Matrix

Die Dimensionen mit P0 sind kein Ersatz für Produktentscheidungen. Die meisten sind *vor einer irreversiblen Änderung* zu prüfen: Datensicherheit, Versionierung, Plattformidentität, Rechtslage, alter vs. neuer Runtime-Zuschnitt und Nachvollziehbarkeit des Recherchestands. Ein bearbeitetes P0-Thema wird nur dann abgeschlossen, wenn seine letzte Spalte durch einen Nachweis beantwortet ist.

**Vollständigkeit ist mehrdimensional:** Scope-/Artefaktabdeckung, Quellengültigkeit, technische Verifikation, Produkterfolg, Lizenzfreigabe, Operationsfähigkeit. Ein Gradindikator ohne klare Grundgesamtheit führt in die Irre.
