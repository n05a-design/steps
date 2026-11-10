# Kritischer Vorher–Nachher-Vergleich, verbleibende Unsicherheiten und Maßnahmen

**Ziel:** Die Verbesserung wird nur dort beansprucht, wo sich ein *konkreter Nachweis* geändert hat. Mehr Seiten oder Prompts gelten **nicht** als Evidenz für fertig entwickelte Software. **V1** = erstes 66-Dateien-Paket vom 10.11.2026; **V2** = unabhängige statische Zweitprüfung und fachliche Nachträge; **Finales Auditpaket** = V2 + diese ergänzten fachlichen Verträge, Requirements-Trace und Validierung. Original-V1 und Quellarchive bleiben unverändert.

## A. Konkrete Gegenüberstellung

| Untersuchungsachse | V1 – bisheriger Stand | Festgestellter Mangel | Im Audit konkret erweitert oder korrigiert | Weiterhin unsicher | Nächste nachweisbare Aktion |
|---|---|---|---|---|---|
| Projektidentität und Zielbild | P1–P5, Harmony-first als Hypothese | Drums, Audio, wissenszentrierte und produktzentrierte Ziele nicht entschieden | Drei Visionsebenen und 4 MVP-Varianten mit Nutzer-/Technik-Gates | Owner wählt v0.1 nicht | ADR-PROD-01 und Testabläufe freigeben |
| Herkunft und Dokumentabdeckung | 7 Uploads, 1 Screenshot und 992-Zeilen-Overview archiviert | 7 bereits im Repo liegende Deep-Research-/Handover-Dokumente übersehen | Research-Refs mit tatsächlichen Git-Blob-SHAs, 28 historische REQs integriert | vollständige Endfreigabe Research Paper fehlt | Quelle zu Claim reviewen, Owner-Version bestätigen |
| Aktueller Glide-Stand | remote 3.50.7 vs. lokaler 3.53.0 | inzwischen veralteter Vergleich | Remote bei `9e767bea` (PR #75) ebenfalls 3.53.0; lokales `app.pyw` Git-Blob-identisch | übrige 93 Module und 165 Ressourcen nicht lokal gegengeprüft; CI/Mensch | vollständiger Freeze mit Asset-/Modulmanifest |
| Steps-Code | korrekter Hinweis Scaffold ≠ App | überwiegt Dokumente, keine Domain-/End-to-End-Spur | Musikdomain und 16 testbare Invarianten mit fehlendem Code klar benannt | keine ausgeführten Steps-Produkttests | 1. vertikaler Chord→Save/Load→SMF-Slice |
| Glide-Fork/Extraktion | 2-Pane-Shell als Startannahme, 94 Module als Potenzial | Monolith, globale Import-Nebenwirkungen und verdeckte Aktionen unterschätzt | 4 Strategien, zwei Vergleichsspikes, 30 Shell-Prüfszenarien, Method-/Side-Effect-CSV | keine tatsächliche Extraktion validiert | B vs. D Spike mit gleichen Kriterien |
| Navigation „ohne Funktionen“ | Buttons weiter sichtbar, Callback-Rückbau grob | Tastatur, Kontextmenu, Drag, globales UI-Action-System könnte alte Mutationen auslösen | No-op-Negativfälle, Router/CommandRegistry und No-Glide-Touch | UI noch nicht isoliert | S01–S30 implementieren und OS-testen |
| Fachmodelle | Pitch/H/B, E7 Kontext als Beispiele | Daten-/Notation-/Timeline-Contracts nur skizziert | Invarianten für Spelling, Voicing, Alternativanalysen, PPQ/Tempo/SMF | detaillierte Schema-ADRs und Testcode fehlen | Golden Fixtures + Schema-Versionierungs-ADR |
| Wissensbibliothek | Source-Registry leer erkannt; Pipeline vorgeschlagen | „Dokumentieren“ mit tatsächlicher Ingestion verwechselt | Source/Extract/Claim/Concept/Relation/Rule/Example/Revision, 10 Gates, idempotente Batches | Bücher/Editionen und Rechte unreviewt; KB weiterhin leer | Batch A mit echten, zulässigen Quellen, Review und Citation-Evals |
| Skill | `SKILL.md` als Router | Retrievalqualität, Quellenbezug und Cross-Provider-Tests nicht belegt | Retrieval-Alternativen + Citation-Fidelity + Halluzinations-/Injection-Fälle | noch keine ausgeführten Eval-Sets | 20–50 repräsentative Evalfragen und Blank/Incorrect-Erkennung |
| Wissenschaftlichkeit/Bias | alternative Linsen erwähnt | westlich geprägte Korpora, Kultur-/Genre-Grenzen, Autoritätsskala | Theory vs. empirical vs. heuristic strikt, Sampling-/Bias-Review | tatsächliche Corpus-Abdeckung | Quellen pro Stil/Framework stratifizieren |
| MIDI/Audio/Drums | Funktionswünsche ohne konkrete Fehlerfälle | Tick/Tempo/Loop/Synth-/Device-Fragen, Drums-Timeline fehlten | gemeinsames Timeline-Ziel, SMF0/1, Note-off, Geräte-/API-Fallback, Groove-Tests | Playback-Backend, Synth-Rechte, DAW-Validierung | 10 MIDI Gold-Dateien + DAW-Probe |
| Persistenz/Recovery | Save/Load/Backup als allgemeiner Port | unklarer Crash-/DataRoot-/Migration-/Lock-Vertrag | Transaktions-/Version-/No-Glide-Touch-Matrix | Atomizität auf realem Dateisystem nicht geprüft | 16 konkrete IO/Recovery-Tests |
| Design/UX | Glide-Designprinzipien übernommen | Bedienbarkeit, Lernen, A11y unzureichend bewertet | Didaktische Lernstufen + 10 UX-/native A11y-Fälle | tatsächliche Screenreader-/Usability-Daten fehlen | fünf beobachtete Nutzeraufgaben, OS-Accessible-Probe |
| Wettbewerb/Markt | alte Wettbewerbslisten | unbewiesene Alleinstellung als Chord Explorer | aktuelle Hookpad-Herstellerbelege + Falsifikations-Checkliste | kein vollständiger Preis-/Version-/Hands-on-Vergleich | 3–5 Produkt-Tests unter identischen Aufgaben |
| Urheberrecht/Security | Warnung vor externen PDFs | bereits veröffentlichte 60 PDFs und Webcaches; History-Löschung nicht simpel; Ingestion-Angriffsfläche | eigener P0-Rechte-/History-Track, Threat Model, Scope pro Asset | keine juristische Einzelfreigabe oder vollständige Repo-History-Inventur | private juristische Rechteprüfung und Publikationsentscheid |
| QA | allgemeine Quality Gates | Dokumentation, Code-/Fachtests und native Abnahme zu wenig getrennt | Q0–Q7, Evidence-Record, 30+16+16 Zieltests und Paketintegritätstest | keine Steps-End-to-End-Tests bestanden | unabhängige CI und menschliche OS-/Musikprüfung |
| Entwicklungs-/KI-Prozess | 24 allgemeine Arbeits-Prompts | viel duplizierter Vertrags-Text; wenig konkrete Nachweise je Auftrag; Tokenkontext bricht | separates Multi-Agent-Handover, 28-REQ-Trace, geforderte SHA und No-Permission-Eskalation | reale Aufgabenzuordnung und Accounts nicht prüfbar | path ownership, Issue-IDs, sauberer PR-Prozess |
| GitHub-Integration | Versuch Branch, HTTP 403 | Remote nicht beschrieben trotz „push:true“ | permission-failure sauber dokumentiert, lokales nicht-destruktives Einspielskript | Schreibrechte dieses Chat-Connectors weiterhin nicht nutzbar | lokaler Feature-Branch oder manueller PR |

## B. Untersuchungsausmaß – keine falsche Prozentzahl

Das Untersuchungsraster umfasst **33 Dimensionen** (`manifests/INVESTIGATION_COVERAGE_33_V2.csv`) und **28 aus dem ursprünglichen Research-Handover identifizierte Requirements** (`manifests/REQUIREMENTS_TRACE_28.csv`). Dies sind **zwei verschiedene Taxonomien**, daher weder 33+28 als Anzahl unterschiedlicher Anforderungen deklarieren noch aus 100% CSV-Feldern „100% Projekttests“ ableiten. Im gesamten ersten Paket gab es 24 Prompts, aber keine erbrachten UI-, Audio- oder KB-Integrationstests. Das bleibt ausdrücklich offen.

**Quelle der 28 REQs:** [PROJECT_CONTEXT_HANDOVER.md, Kap. 03](https://github.com/n05a-design/steps/blob/75329fef46878a5ac816cef3690e612a9e8fe52c/research/notes/deep-research/legacy/PROJECT_CONTEXT_HANDOVER.md); dessen `CONFIRMED` bezeichnet den Stand des damaligen Forschungs-/Handover-Dokuments, nicht aktuelle Owner-Freigabe dieser Auditprioritäten.

## C. Korrekturen, die vorher als sicher wirkten

1. **Glide-Baseline:** GitHub-`main` ist nicht mehr 3.50.7; Commit und Dateikopie beweisen jetzt Übereinstimmung von `app.pyw`, aber nicht des *gesamten* Arbeitsstandes. Diese Asymmetrie ist im Freeze-Gate festgehalten.
2. **Ein bestehendes Handover:** Das Projekt besitzt schon `PROJECT_CONTEXT_HANDOVER.md` mit 28 REQs und 17 Kapiteln; der historische README-Text behauptet teils das Gegenteil. Keine zweite Source of Truth aus dem Nichts schaffen.
3. **24 Prompts ≠ 24 umsetzungsreife Features:** Sie sind Arbeitsaufträge, keine Diffs, keine Tests und kein Beleg für Code/Research-Ingestion. Ihre Qualität wird individuell am testbaren Deliverable gemessen.
4. **„Dopplungen entfernt“:** Inhaltlich vollständige Deduplizierung über PDF/HTML/MIDI ist nicht bewiesen. 160 Git-Blob-Gruppen (Steps `75329fef`) sind objektiv identische Inhalte in mehreren Pfaden, keine automatisch löschbaren semantischen Dubletten.
5. **Zwei Fenster:** ein Bildschirmfoto kann UI-Aufteilung stützen, aber nie die spätere Fensterarchitektur autorisieren. UI-Bedeutung bleibt Entscheidung.
6. **KB-Freigabe:** `sources: []` trotz 1.000 Archivdateien belegt, dass fachliche Nutzungsvorbereitung und Ingestion nicht abgeschlossen sind.
7. **Open Source:** MPL-2.0-Datei erlaubt keine pauschale Neuveröffentlichung extern recherchierter Originalwerke, Live Sets, Sounds oder Website-Caches.
8. **Wettbewerb:** Der Hersteller dokumentiert für Hookpad bereits Chord-Empfehlungen, Erklärungsbezug, Drum-/Playback-Kanäle und MIDI-Export. Die bloße Existenz dieser Features ist kein Alleinstellungsmerkmal von Steps.
9. **Glide-Komponentenzählung:** 94 Module/25 Bausteine sind Systemregistereinträge, keine 94 produktneutralen oder 25 fertig portierbaren Libraries.
10. **V6.6 Zahl:** 1.000 überprüfte Legacy-Dateien im archivierten Baum des aktuellen Repos sind eine andere Menge als 1.146/1.306/≈1.166 historische Tabellenbehauptungen.

## D. Priorität nach Risikowirkung

### P0 – vor riskanter Implementierung

- **R01 Öffentliches Drittmaterial:** Bestand und Historie mit fachlichem Rechtescope beurteilen; keine neuen fremden Uploads oder Public-Exports. Parallel zur Entwicklung möglich, Veröffentlichung bis zum Review eingeschränkt.
- **R02 Drift der Codebasis:** 3.53.0 vollständiges Modul-/Resource-/QA-Manifest, lokale/remote Differenz und native Prüfgrenzen.
- **R03 Produkt-/Fenstersemantik:** zwei UI-Skizzen, vier MVP-Varianten mit Kriterien, Owner-ADR.
- **R04 Domain ohne Sackgasse:** Notation/Chord/Timeline/Drums/Tempo-Fixtures vor persistiertem Projektformat.
- **R05 Quelle vor Skill:** ein komplett rechtlich überprüfter Batch und eine echte Abfrage mit Citation Test.

### P1 – nach den ersten Vertical Slices

- **R06 Shell-Extraktion:** minimaler isolierter Prototyp B vs. D, negative Tests gegen Glide-Schreibpfade und verdeckte Commands.
- **R07 Qualität:** automatisierte und native Testmatrizen; experimentell geprüfte Learning/UX/A11y-Kriterien.
- **R08 Betriebsfähigkeit:** Source-/Claim-Registry-Schemaversion, Dokumentenpflege, CI/Release- und KI-Agenten-Handover.

### P2 – danach skalieren

- Korpus-/Statistikmodelle mit Bias-Audit, komplexes Reharmonisieren, umfassende Producing-/Ableton-Archive, Audio-Synth/Live Playback, Realtime Device Handling, ML/RAG nur nach empirischem Nutzenvergleich.

## E. Was diese Auditfassung ausdrücklich nicht liefert

Weder sämtliche 1.931 Steps-Repo-Dateien noch alle 1.542 Glide-Repo-Dateien wurden textinhaltlich vollständig gelesen; ein Dateibauminventar ist kein Seitenreview. Die vorhandenen Bücher/PDFs, Drittanbieter-Apps und MIDI-Projekte wurden nicht einzeln verifiziert. Es gibt **keinen** geschriebenen Steps-App-Code, keine nachgewiesenen Steps-Tests und keine freigegebene neue Knowledge-Quelle durch dieses Audit. Direkter GitHub-Push/PR war nicht möglich; die Repositories blieben unverändert. Die neu erzeugten Quell-/Anforderungs- und Testindizes sind **Planungs- und Prüfinstrumente**, keine implizite Produktfertigstellung.

## F. Konkrete erste sechs Arbeitspakete mit Deliverables

| Reihenfolge | Eigentümerrolle | Eingang | Liefergegenstand | Akzeptanz |
|---|---|---|---|---|
| A0 | Verantwortlicher + Rechteprüfung | aktueller Steps-Tree | Rechts-/Publikationsregister für PDFs/Web/Audio | jeder priorisierte Dateityp statusdifferenziert, keine automatische Veröffentlichung |
| A1 | Glide-Copilot + unabhängige QA | `main` 3.53.0 + lokale Kopie | source/assets/tests Hashfreeze und offene plattformspezifische QA | alle 93 Module und Ressourcen verglichen, echte native Ergebnisse separat |
| A2 | Produkt/Design | User-Feedback, aktueller Screenshot | 2 Architektur-Wireframes, 4 MVP-Scopes, Entscheidungsblatt | Owner-Entscheidung nicht als Agentenmeinung ersetzt |
| A3 | Musiktheorie-Engine | Research Papers + `schemas/` | Pitch-/Chord-/Timeline-Minimalschema und T01–T16 Tests | Tk-frei, keine offenen H/B-Fehler |
| A4 | UI-Engine | eingefrorene Glide-Referenz | B/D-Spikes, jeweils gleicher Shell-Testkatalog | keine Glide-UserData berührt, Szenarien S01–S30 mit Status |
| A5 | Forschungs-/Quellenreview | 5 rechtlich geeignete Originale | 10 Concepts, 20 Claims, 20 Pos-/Negativfälle und Citation-Evals | Original-Links und Reviewer, zweiter Import idempotent |

Die Mengen für A5 sind bewusst ein **Pilot-Gate**, keine vollendete Knowledge Base oder statistisch validierte Qualität. Nach jeder Runde `docs/roadmap/` und die 28-REQ-Traceability entsprechend neuer Evidenz fortschreiben.
