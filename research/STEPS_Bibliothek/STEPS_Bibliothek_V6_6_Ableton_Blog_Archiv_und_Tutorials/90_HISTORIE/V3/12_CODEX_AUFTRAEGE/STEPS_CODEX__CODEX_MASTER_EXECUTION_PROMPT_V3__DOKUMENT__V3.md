# STEPS – CODEX MASTER EXECUTION PROMPT V3

**Projekt:** STEPS – An independent, open-source chord progression app for exploring harmony & learning music theory, expanded with Composing.  
**Status:** Ausführbarer, umfangreicher Folgeauftrag zum realen Knowledge-Base-Aufbau; kein Anspruch, dass die 4 Säulen bereits produktiv implementiert sind.  
**Benötigter Zugriff:** echtes STEPS-Repository und lokal verfügbare Forschungsquellen. Ist kein Repo erreichbar, führe nur dokumentarische Prüfungen auf verfügbaren Dateien durch und benenne die Grenze.

## A. Mandat und Rolle

Handle als interdisziplinärer Lead für Music Theory, Harmony, Chord Progressions, Composing, Musical Form, Orchestration/Arrangement, Computational Music Theory, Knowledge Engineering, Library Science, QA und Open-Source Governance. Lies zuerst `00_START_HERE.md`, `03_Codex/PROJECT_CONTEXT_HANDOVER_V3.md`, `01_Forschung/00_RESEARCH_MONOGRAPH_V3.md` und die V1-Historie. Unterscheide ausnahmslos bestätigen Nutzerentscheidungen, geprüften Repository-Bestand, wissenschaftliche Belege, redaktionelle Drafts, Produktideen und offene Hypothesen. **Nicht mit einer weiteren Architekturprosa abschließen**: baue tatsächlich testbare, befüllte Datenstrukturen und dokumentierte, kuratierbare Einträge.

Arbeitsfolge: `Discover → Inventory → Freeze → Verify → Extract → Normalize → Differentiate lenses → Connect → Test → Expert Review → Document → Version → Expand`.

## B. Vier gleichberechtigte Wissenssäulen

**B1 – MUSIC THEORY:** Notation international/deutsch H/B, Stimmung/Temperament und Mikrotonalität, Pitch-/Intervallmodelle, Skalen/Modi/Familien, harmonische Grundbegriffe, Rhythmus/Metrum/Hypermetrik, musikalische Struktur, Tonalität, Formen, Kognition, Pädagogik. Prüfe Exaktheit von Spelling und instrumentenbezogener Darstellung. Nichtwestern Systeme separat und nur nach traditionell qualifizierter Evidenz.

**B2 – HARMONY:** Common-practice/Riemann/Roman Numerals, Tonika/Prädominante/Dominante, Kadenz, Mollvarianten, Modalität, Tonicization/Modulation, chromatische Akkorde, Jazz-/Blues-/Pop-/Rock-/Gospel-/Soul-/Neo-Soul-/R&B-/Film-/Electronic-Modelle, voice leading, neo-Riemannian transformations, Pitch-Class-Set and non-tonal systems. Stil-/Repertoiregrenzen explizit.

**B3 – CHORD PROGRESSIONS:** Progressionsfamilien mit Dauer, Key Center, Alternative Analysen, Bassführung/Voicing, Herkunft und melodischem Kontext; Cadential/Loop-/Modal-/Jazz-/Pop-/Blues-Modelle, Reharmonization, Substitutions, Ranking, Form-/Metrikbezug. Generiere keine scheinbar universelle Wahrscheinlichkeit. Die V3 Seed-Atlas-Einträge sind Originalillustrationen, nicht Corpus-Fakten.

**B4 – COMPOSING:** Eigenständige, gleichrangige Kompositionslehre. Materialgenerierung, Motive, Themen, Varianten, Sequenzierung, Inversion, Retrograde, Augmentation/Diminution, harmonisch/melodische Dramaturgie, Phrase, Period/Sentence, Songform, Formfunktionen, Kontrapunkt, Bass, Gegenmelodien, Orchestration, Arrangement, Textprosodie/Topline, repetitive/prozedurale/algorithmische Komposition, Feedback und Revision. Nutze die V3-Techniken und Originalstudien als Review-Basis; entwickle daraus kohärente, eigenständige Kompositionsbeispiele mit dokumentierten Invarianzverträgen. Die Harmonie muss zur musikalischen Zeit und Melodie passen.

**Verschoben:** vollständige Drum-/Groove-Engine, umfangreiche Drum-Datensatzimporte, komplettes UI-Redesign, produktive Blackbox-ML-Modelle; Rhythmus/Metrum/Timing bleibt als Composing-Kontext eingeschlossen.

## C. Verbindliche Lesereihenfolge und Ist-Audit

1. `git status`, Branch, Working Tree, aktuelle Struktur und `AGENTS.md` prüfen; keine fremden Änderungen überschreiben, nicht nach `main` mergen.
2. Bestehende Skill-Verzeichnisse, Dokumente, Research-Ordner, Quellarchive, Schemas, Tests, Python/Tkinter-Dateien und vorhandene echte Harmonieobjekte read-only inventarisieren. Erkenne Dubletten anhand Hash/Content, nicht nur ähnlichen Namen.
3. **V1-Archiv** als historische Quelle erhalten. Vorhandenes `PROJECT_CONTEXT_HANDOVER_V1.md` war ein *fertiges* Handover, nicht nur ein Auftrag; es enthält die mittlerweile veraltete Behauptung, `Master-Research-Prompt.md` fehle. In diesem V3-Paket ist er vorhanden. Historie nicht rückwirkend umschreiben, sondern V3 dokumentarisch als korrigierten Stand führen.
4. Frühere Forschungsberichte liefern Quellenkandidaten, wissenschaftliche Ideen und UX-Modelle, jedoch keine überprüften Repository-Fakten. Falls V2 ZIP wirklich vorhanden ist, deduplizieren und mit V3 zusammenführen; andernfalls als `unavailable_input` markieren.
5. Erstelle einen überprüfbaren Baseline-Report, der Code, Tests, Quellen, Rechte, Dokumentation und unbekannte Bereiche trennt.

## D. Arbeitspaket P0 – Ingestion, Bibliografie, Quellenrechte

Lies `05_Quellen/SOURCE_REGISTRY_VERIFIED_METADATA.json`, `05_Quellen/BIBLIOGRAPHY_ACQUISITION_QUEUE.json`, `05_Quellen/SOURCE_REVIEW_AND_BIBLIOGRAPHY_V3.md`. Darin sind derzeit 47 Einträge, von denen einige verschiedene Editionen, Alias-/Metadatenseiten oder Sekundärrezensionen betreffen; das sind **nicht 47 unabhängig voll gelesene wissenschaftliche Werke**. Die weiteren 50 Kandidaten sind nicht verifiziert. Normalisiere Identität, Editionsstand, Werk vs Rezension, DOI/ISBN, dauerhafte URL, Autorenschaft, Jahr, Quelltyp und Claim-Locators. Trenne `metadata_verified`, `full_text_accessible`, `section_read`, `exact_claim_verified`, `license_checked`, `redistribution_allowed`, `reviewed`.

Für die alten 20 Initialquellen: physisch prüfen, Hashes bilden, defekte `MakingMusic.pdf` gesondert markieren, `Music_Theory_Advanced_Level.pdf` bei Bedarf visuell prüfen. Verstehe fehlende Quellen nicht als gelesen. Proprietäre Bücher/Texte/Produktgrafiken nicht in öffentliches Git-Repo kopieren. Datensatz-Lizenzen auf Aggregator-, Annotation-, Score-, Audio- und Einzelcorpus-Ebene prüfen.

**Output:** eindeutige Source Registry, License Registry, Access Matrix, bibliografische Dauerlinks, Review-Queue mit P0/P1/P2.

## E. Arbeitspaket P1 – Taxonomie und Theorieobjekte

Prüfe `THEORY_CONCEPTS_V3.json` Objekt für Objekt (142 redaktionelle Konzepte, nicht 142 bestätigte Lehrbuchzitate). Normalisiere ID, Slug, DE/EN, Aliase, Voraussetzungen, SourceEvidence, Stil/Tradition, Beispiele, Gegenbeispiele und Beziehungen. Erst wenn eine genaue Quellenstelle nachweislich gelesen/validiert wurde, darf `claim_evidence.verified=true` gesetzt werden. Ergänze weitere Quellen bei Lücken statt nur alle V3-Definitionen auf `reviewed` zu stellen.

Priorisiere notarisch exakte Pitch-/Spelling-Objekte, Tonleitern/Modi, Chord Model, Form, historische vs Pop-/Jazz-Lenses und instrumentenbezogene Struktur. Prüfe deutsche H/B-Schreibung besonders sorgfältig; V3 verwendet internationale Chordsymbolbenennung. Für mikrotonale und nichtwestliche Systeme ein `unsupported_for_now` mit expliziter Repräsentationslücke setzen, wenn 12-TET nicht reicht.

**Output:** echte referenzierbare Konzepte, kontrollierter Wortschatz, Alias-Index, graphische Referenzen und Reviewstatus.

## F. Arbeitspaket P2 – Getrennte Harmoniesysteme und Regeln

Lies `TYPED_RULES_V3.json`. Die 77 Seed-Regeln sind `constraint`, `tendency`, `transformation`, `interpretation`, `heuristic`, `empirical_observation`; führe zusätzlich `convention` als möglichen Typ. Kein `tendency` darf unkritisch als unbedingte `constraint` codiert werden. Prüfe Spelling, genaue Relation, funktionale Unterordnung, Stil-/Repertoirekontext und denkbare Gegenfälle. Erstelle Ableitungsgraphen und mindestens einen positiven und einen negativen Golden Case für jede produktive Regel.

Insbesondere: führender Ton in Moll, Dominantseptakkord, sekundäre Dominanten, Neapolitaner, augmented-sixth, Backdoor, Tritonussubstitution, Blues I7, modal tonic, Pop-axis ambiguity, Voice Leading, P/L/R, Tn/TnI. Bei Konflikten mehrere `analytical_lens`-Objekte samt Urheberschulen zulassen.

**Output:** verifizierte, typisierte Rule Library; Exceptions/Countercases; SourceClaim-Links; Validierung.

## G. Arbeitspaket P3 – Chord Progressions und Reharmonisierung

Prüfe 95 vorhandene `PROG-V3-*`-Karten aus `PROGRESSION_ATLAS_V3.json`; sie enthalten verwandte Varianten/Transpositionen und stellen keine 95 eigenständigen Theorien dar. Verifiziere jeden Akkord, jede Roman-Numeral-Analyse, Key-Kontext, `V/x`, Lokales vs Globales Zentrum, Stilkonvention und relevante enharmonische Schreibweise. Markiere mehrdeutige Kontexte ausdrücklich. Erstelle konkrete per-event `start/duration`-Daten und, wo sinnvoll, eine originelle kurze Melodie- und Voice-Leading-Realisation. Bewahre die Datenstruktur `raw example → analysis alternatives → applicable rules → tests`.

Verbessere separate Familien (diatonic, applied dominant, mixture, modal, pop axis/plateau, blues, jazz, chromatic, film, electronic) und reiche für unterrepräsentierte Gebiete neue recherchierte Beispiele nach. Unlizenzierte Originalsong-Transkriptionen nicht öffentlich importieren.

**Output:** validierte Progression Library, Form-/Melodie-Links, mehrfach begründbare Lesarten, Reharmonization-Evaluationsfälle.

## H. Arbeitspaket P4 – Composing als eigenes Wissenssystem

Dies ist ein P1-Kernstück, nicht ein optionales Appendix. Die 69 `COMP-TECH-*`-Karten und 19 `ORIGINAL-STUDY-*`-Skizzen bieten einen Anfang, keine fertig komponierte Partitur. Prüfe musikalische Operationsdefinitionen, Intervall-/Dauerinvarianz, stilistischen Scope und pedagogical level. Entwickle die Kompositionstechniken zu ausführbaren/plausibel vorführbaren Workflows: `brief → motif/seed → transformation → melody/phrase → harmony → bass/voice leading → form/section → instrumentation/arrangement → evaluation/revision`.

Erstelle repräsentative **vollständig in eigenem Material** ausnotierte vier- bis achttaktige Miniaturen verschiedener Lenses (erst nach Validierung), mit Audit der Melodietöne, Notenlängen, Taktgrenzen, Tonarten, Stimmen und Harmonien. Erweitere anschließend zu Song-/Formplänen. Schreibe je Miniatur ein kommentiertes Composer Decision Log und mindestens eine begründete alternative Version. Benutzerautorschaft und Varianten müssen erhalten bleiben.

Wissenschaftliche Quellenkandidaten: Caplin/Schoenberg/Form, Gjerdingen/Sanguinetti/Partimento, Belkin/kompositorischer Aufbau, Nobile/Popform, Jazz/Voice Leading, Huron/Meyer/Erwartung und instrumentatorische Fachquellen. Ohne echten Volltextzugriff keine spezifischen Seitenzitate fingieren.

**Output:** echte Composition Pattern Library, Melodic Development Templates, Form models, Arrangement/Instrument Rules, original notated studies, Revisions-/Evaluationreport.

## I. Arbeitspaket P5 – Wissenschaftliche Konflikte und historische Breite

Stelle die Schulen neben- statt übereinander: klassisch/functional, German Riemann, modal, jazz, blues, pop/rock loop, transformational, geometric, posttonal. Ordne Quellen, historische Repertoires und Begriffsdifferenzen zu. Ein identischer Chord-String darf mehrere textliche und formale Analysen tragen. Nonwestern systems nur dort weiter modellieren, wo die Beleglage und Datenrepräsentation passen; keine reductive scale-classification.

**Output:** Lens/Tradition Register, Terminology Conflicts, Alternative Analysis Cases, Cross-Cultural Source Gaps.

## J. Arbeitspaket P6 – Datenmodelle und technische Validierung

Nutze den **bestehenden** Projektdatenstandard, sofern vorhanden; andernfalls versioniere die neue Schemafamilie `0.x`. Prüfe mit `python 04_Qualitaet/validate_v3.py` die V3-Datenstruktur und passe sie erst nach Review an. Ergänze JSON-Schema-Tests, referential integrity, unique IDs, link checks und negative cases. Bewahre `SpelledPitch` getrennt von `PitchClass`, lokale Tonika von globaler Tonika, Chord Symbol von Voicing, Formal Unit von Chord Event, Original Composition von fremdem Corpus-Material. Modellierung neuer Standardformate (Harte, DCML, MIDI, MusicXML, MEI) nur mit expliziten Konversionsverlusten.

Die V3-Evaluationcases sind teilweise maschinen-, teilweise musiktheoretisch oder menschlich zu prüfen. **Kein 'alle Tests bestanden', wenn nur JSON geladen wurde.**

**Output:** lauffähige Strukturtests + ausgeführte musiktheoretische Referenztests + list of skipped reviews with reason.

## K. Arbeitspaket P7 – Wissensabfragen, Skill- und App-Verknüpfung

Füge einen kleinen, testbaren Query-/Lookup-Kern hinzu, der Concept/Rule/Progression/Motif nach ID, Alias, Domain, Lens, Source/Reviewstatus findet. Keine großen App-/Tkinter-Umbauten im aktuellen Auftrag. Optional eine Read-only CLI oder Demo-Notebook, falls Projektkonventionen es erlauben. Ein zukünftiger Skill soll `SKILL.md` kurz halten und Informationen nur aus kuratierten Referenzen laden; Explain/Analyze/Generate/Compose/Reharmonize-Ausgaben müssen Source/Uncertainty mitliefern.

**Output:** Retrieval-Index, Navigations-README, dokumentiertes Agent/Skill Interface, minimale fachliche Evals.

## L. Arbeitspaket P8 – Rechts-/Lizenz-/Governance-Gate

Jede Aufnahme prüft Autor, Copyright, Lizenz, Redistribution, Urheber der Notenbeispiele, Textübernahmemenge und Zugriff. Kein Copyright-geschütztes Lehrbuch und keine kommerzielle Notensammlung ungeprüft commiten. Open Music Theory hat ShareAlike-Anforderungen; Rubin/Open Music Composition hat differente offene Lizenz – nicht unüberlegt zusammenkopieren. Fremdprodukt-UI nur abstrahieren, nicht charakteristisch kopieren.

**Output:** Lizenzmatrix, getrennte public/private/metadata-only Sources, sachliche Attribution.

## M. Arbeitspaket P9 – Abschluss und Versionierung

- `CHANGELOG`, Release Manifest, reviewed/draft counts, Source Coverage nach Fachgebiet.
- `open gaps` mit Quellenbedarf, Priorität, Status, nächstem Review.
- `Decisions/ADR`: bestätigte Nutzerentscheidungen getrennt von Architekturvorschlägen.
- Dokumentation mit direkten Source-ID-/Concept-/Rule-/Example-/Test-Verweisen aktualisieren, ohne historische Revisionen auszulöschen.
- Bei vorhandener PR-Verbindung: PR statt automatischem Merge; Tests und Dateien im PR-Bericht nennen.

**Output:** Reproduzierbarer Code-/Wissensdiff, QA-Ergebnis, Quellenabdeckung, fachlicher Reviewscope und priorisiertes Folgebündel.

## N. Definition of Done

Die Arbeit ist nur dann fertig, wenn ein echter Baseline-Audit vorliegt, dokumentierter Source-Access/Lizenzstatus existiert, eine substanzielle Anzahl source-reviewed Konzepte/Rules/Progressions/Compositions vorliegt, eindeutige IDs/Verknüpfungen geprüft sind, positive und negative Theorie-Fälle ausgeführt wurden und der unvollständige Teil exakt als Restbacklog ausgewiesen ist. Anzahl von Seed-Objekten ohne Quellenreview zählt **nicht** als wissenschaftlicher Abschluss. Ein neues Schema oder ein Ordnerbaum allein erfüllt **nicht** den Auftrag.

## O. Berichtsschablone

**A. Repository**: Branch, Working Tree, neue/angepasste Dateien, mögliche PR.  
**B. Sources**: identifiziert, tatsächlich lesbar, read sections, fully reviewed, license/redistribution reviewed.  
**C. Theory/Harmony/Progressions/Composing**: pro Säule Anzahl überprüfter Objekte und repräsentativer fachlicher Fälle.  
**D. Validation**: echte automatisierte Tests, manuelle Reviews, bekannte Fehler/Skipped Checks.  
**E. Provenance**: konkrete bibliografische und Source-Claim-Locators, unresolved old turn markers.  
**F. Decisions/Conflict/Risks**: getroffene vs vorgeschlagene Entscheidungen.  
**G. Next work packages**: priorisiert mit Acceptance Criteria.  

**Beginne jetzt mit der realen Prüfung der Repo- und Quellenlage und dem schrittweisen Aufbau der geprüften V3-Knowledge-Base. Kein Merge ohne ausdrücklichen Auftrag.**
