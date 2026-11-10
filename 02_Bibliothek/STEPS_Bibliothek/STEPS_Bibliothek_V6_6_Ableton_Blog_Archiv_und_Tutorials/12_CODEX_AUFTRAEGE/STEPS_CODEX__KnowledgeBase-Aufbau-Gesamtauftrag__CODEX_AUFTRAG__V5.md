# STEPS — CODEX MASTER EXECUTION PROMPT V5

**Version:** 5.0.0-research-draft · **Scope:** Music Theory + Harmony + Chord Progressions + Composing, vier gleichrangige Säulen. **Ausführung im echten Steps-Repository, das hier noch nicht überprüft wurde.**

## Verbindlicher Auftrag

Übernimm die Rolle eines Teams aus Music Theorist, Composer, Computational Music Researcher, Knowledge Engineer, Data/Schemas Engineer, Open-Source Maintainer und QA Engineer. Prüfe den tatsächlichen Repository-Stand. Integriere danach die V1–V5 Research Library mit **wirklich gefüllter, quellen- und revisionsfähiger Knowledge Base**. Bearbeite nicht lediglich ein neues Konzeptpapier; lege nachvollziehbare Wissensobjekte, Belege, Szenarios, Regeln, Progressionen, kompositorische Muster, Tests und validierte Dokumentation an.

**WICHTIG:** Die Research Library ist nicht die bestehende Codebasis. Die 27 in V5 recherchierten Quellen sind nicht 27 vollständig durchgearbeitete Bücher. Die 1.378 generierten Progressionsvarianten sind nicht empirisch 1.378 unterschiedliche musikalische Muster. Die 16 neuen Notenstudien sind technisch prüfbare Lehrstudien, keine unabhängigen Fachgutachten.

## Arbeitsgrenzen

- Bearbeite nur das echte Steps-Projekt; verwechsle es nicht mit Glide oder einem anderen Repo.
- Vor Änderungen: read-only Git-Status, Branch, AGENTS.md, Tests, Lizenz, Struktur, vorhandene Daten.
- Keine bestehenden Änderungen verwerfen; nichts unkontrolliert überschreiben; keine Repo-Duplikate.
- Kein Git-Merge ohne ausdrücklichen Auftrag. PR/Branch/Änderungsreport statt stillschweigendem Push nach main.
- Keine geschützten PDF-Bücher, kommerziellen Noten/Produktgrafiken oder ungeprüften Datensätze in ein öffentliches Repo kopieren.
- Keine Behauptung, Quellen seien geprüft, wenn nur Verlagssnippets gelesen wurden; keine erfundenen Seitenzahlen.
- Drum-Engine und Drum-Korpora sind deferred; Rhythmus, Metrik und Harmonic Rhythm sind gegenwärtiges Forschungs-/Composing-Thema.
- ML und Corpus-Ranking erst nach Daten-/Lizenz-/Testbasis, kein Ersatz für erklärbare Regeln.

## Maßgebliche Eingaben

`00_START_HERE.md`, `01_Neuforschung/`, alle `02_Fachbaende/`, `03_Analysewerkstatt/`, `04_Kompositionslabor/`, `05_Wissensobjekte/`, `06_Quellen_und_Rechte/`, dieses Handover und `08_Validierung/`. Historische V4 inklusive V3 und V1 in `00_ARCHIV_V4_Unveraendert/`. Alle weiteren ursprünglichen PDF/TXT-Dateien nur, wenn im Codex-Lauf tatsächlich lokal/über Connector vorhanden.

## Ausführbare Arbeitspakete mit Gates

### P00 — Repository-State und Eigentumsgrenzen

**Aufgabe:** Read-only Gitstatus/Branches/AGENTS/Build/Tests/Dokumentation prüfen.

**Belegbare Deliverables:** `SOURCE_STATE_AUDIT, Arbeitsbranch-/Diff-Plan`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** Keine bestehenden Nutzeränderungen gelöscht oder verschwiegen.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P01 — Archiv-/Versionenabgleich

**Aufgabe:** V1, V3, V4, V5 logisch inventarisieren und Duplicate Hashes vergleichen.

**Belegbare Deliverables:** `ARCHIVE_VERSION_CROSSWALK`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** V4 unverändert; Master-Prompt und Handover nachgewiesen.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P02 — Datei-/Quelleninventar

**Aufgabe:** 20 Initialquellen und 27 neu webgeprüfte V5-Titel auseinanderhalten.

**Belegbare Deliverables:** `SOURCE_REGISTRY und SOURCE_AVAILABILITY`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** Eintrag existiert oder fehlt: kein fiktives Lokalisieren.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P03 — Lizenz-/Public-Gate

**Aufgabe:** Jedes PDF, Lehrwerk, Notenbeispiel, MIDI, Corpus-Subset auf Redistribution prüfen.

**Belegbare Deliverables:** `LICENSE_REGISTER, blocked-public-files`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** Kein geschütztes Rohwerk öffentlich committet.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P04 — Quellenorte und bibliografische Verifikation

**Aufgabe:** DOI/ISBN/Edition, URLs, echte Kapitel-/Seiten-Locators manuell/automatisch nachprüfen.

**Belegbare Deliverables:** `CITATION_RESOLUTION_REGISTER`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** Landingspages nur Metadaten; keine Fake-Belege.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P05 — Datenqualität V4/V5

**Aufgabe:** Schema, IDs, referenzielle Integrität, Duplikate, alte Prüfberichte.

**Belegbare Deliverables:** `BASELINE_DQ_REPORT`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** Defekte und nicht ausführbare Checks dokumentiert.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P06 — Domain-Taxonomie

**Aufgabe:** Vier gleichrangige Theoriebereiche und Querschnittsdomänen versionieren.

**Belegbare Deliverables:** `TAXONOMY and controlled aliases`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** Music Theory/Harmony/Chord Progressions/Composing getrennt auffindbar.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P07 — Pitch und Enharmonik

**Aufgabe:** Pitch Class, notierte Note, deutsche H/B, 12-TET, Tuning eindeutig modellieren.

**Belegbare Deliverables:** `PITCH_SPELLING_SPEC and fixtures`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** Gb/F# bewusst unterscheidbar, Akkordschreibweise konsistent.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P08 — Intervalle und Scale Modes

**Aufgabe:** Intervalle aus Notenbuchstaben + Halbtönen, Modus-Zentrum von Tonmaterial trennen.

**Belegbare Deliverables:** `INTERVAL_SCALE_RULES and tests`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** Enharmonische Intervallqualität; Dorian ohne Zentrumsnachweis nicht behaupten.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P09 — Chord-Symbol-Grammatik

**Aufgabe:** Lead sheet vs Harte vs DCML vs RomanNotation/Dialekt prüfen.

**Belegbare Deliverables:** `CHORD_PARSER_CONTRACT`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** C/E ≠ V/ii; add9, sus4, alt, missing thirds getestet.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P10 — Tonartenmodell

**Aufgabe:** Global/local/modal centers, tonicization vs modulation als separate Felder.

**Belegbare Deliverables:** `KEY_CONTEXT_SCHEMA`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** V/vi erzwingt keine Modulation.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P11 — Functional Harmony

**Aufgabe:** Tonikaler/PD/D-Bereich und reale Kadenzbedingungen präzisieren.

**Belegbare Deliverables:** `FUNCTIONAL_RULES and counterexamples`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** V-I nicht immer formale Kadenz; style_scope Pflicht.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P12 — Minor and Modal

**Aufgabe:** Melodisch/harmonisch/natürlich-Moll Kontext, modale Zentren dokumentieren.

**Belegbare Deliverables:** `MINOR_MODAL_CONCEPTS`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** Em in A-Moll nicht pauschal falsch; Dorian nie nur Tonmenge.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P13 — Chromatic Harmony

**Aufgabe:** Mixture, aug6, Neapolitan, mediants, applied/altered chords prüfen.

**Belegbare Deliverables:** `CHROMATIC_RULES and analytical_lenses`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** Quelle, Kontext, Counterexample pro Rule.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P14 — Jazz Harmony

**Aufgabe:** Guide Tones, ii-V-I, Tritone, Backdoor, Extensions und Voicings.

**Belegbare Deliverables:** `JAZZ_RULES and typed examples`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** Db7/G7 nicht als 1:1-Klänge gleichgesetzt.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P15 — Pop/Rock/Blues

**Aufgabe:** Loop-Tonikaambiguität, Blues I7, Formfunktion in Pop/Rock.

**Belegbare Deliverables:** `POPULAR_STYLE_LENSES`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** Pop/Blues nicht ungeprüft mit klassischem Satz bewertet.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P16 — Progression-Datenschema

**Aufgabe:** Onset, Dauer, Akkord, Voicing, Analysis, Section pro Ereignis.

**Belegbare Deliverables:** `PROGRESSION_SCHEMA and migrations`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** Alle 1.378 V5-Varianten eindeutig im geprüften Import.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P17 — Kuratierter Progressionsatlas

**Aufgabe:** 53 neue Familien gegen vorhandene Atlas-Objekte deduplizieren und prüfen.

**Belegbare Deliverables:** `PROGRESSION_FAMILY_REGISTRY`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** Klare Kennzeichnung der Transpositionsvarianten.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P18 — Voice Leading

**Aufgabe:** Stimmenidentität, Range, Register, Common Tones, Dispersion, Crossing.

**Belegbare Deliverables:** `VOICELEADING_SPEC and golden/negative cases`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** Style-specific checks und legitime Ausnahmen.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P19 — Motivik und Transformation

**Aufgabe:** Motif, contour, transpose, invert, retrograde, augment, diminish, fragment.

**Belegbare Deliverables:** `MOTIF_TRANSFORMATION_ENGINE_SPEC`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** Pivot/Meter/Operation order eindeutig, Tests reproduzierbar.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P20 — Form- und Phrasenmodelle

**Aufgabe:** Classical sentence/period vs Pop verse/prechorus/chorus getrennt.

**Belegbare Deliverables:** `FORM_FUNCTION_ONTOLOGY`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** 8 Takte allein beweisen keinen Satz oder Periode.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P21 — Kompositionsprojekt

**Aufgabe:** Brief, Constraints, Material, Section, Theme, Arrangement und Revision.

**Belegbare Deliverables:** `COMPOSITION_OBJECT_SCHEMA`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** Keine Gleichsetzung Piece=ChordProgression.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P22 — Composing Workflows

**Aufgabe:** Mehrere Workflow-Reihenfolgen für Bass-first, Melody-first, Loop-first.

**Belegbare Deliverables:** `COMPOSING_WORKFLOW_DOC`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** Sichtbare Nutzerentscheidungen statt Auto-Behauptungen.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P23 — Instrumentierung

**Aufgabe:** Range, Transposition, Doublings, Spielbarkeit, Artikulation datieren.

**Belegbare Deliverables:** `INSTRUMENT_PROFILE_CARDS`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** Instrumente fachreviewpflichtig, keine Fantasie-Ranges.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P24 — Etüden-Review V4/V5

**Aufgabe:** 30 ältere und 16 neue Lehrstudien rhythmisch/melodisch/notationstechnisch prüfen.

**Belegbare Deliverables:** `STUDY_REVIEW_REPORT, revised sketches`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** Keine MIDI-Parsebarkeit als musikalische Validität ausgeben.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P25 — Hör-/Revisionsbibliothek

**Aufgabe:** Hörbasierter A/B-Plan, Hörkriterien, formale Ziele und Nutzerentscheidungen.

**Belegbare Deliverables:** `LISTENING_REVIEW_PROTOCOL`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** Gleiche Lautstärke/Tempo/Timbre für isolierte Harmonievergleiche.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P26 — Computational Standards

**Aufgabe:** MIDI, MusicXML, DCML, JAMS, music21 als Import/Export prüfen.

**Belegbare Deliverables:** `INTERCHANGE_MATRIX`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** Schnittstellenverluste und Datenrechte explizit.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P27 — Korpora und empirische Evidenz

**Aufgabe:** ChoCo/When-in-Rome/RS-Korpus Grenzen, Grain, Genre Bias, Lizenz.

**Belegbare Deliverables:** `CORPUS_READINESS_EVALUATION`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** Keine vorgetäuschten Genreprozente.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P28 — Kulturspezifischer Forschungsbereich

**Aufgabe:** Maqam/Raga/Afrikanische Rhythmuspraxen ohne West-Universalismus.

**Belegbare Deliverables:** `CULTURAL_RESEARCH_GATES`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** Traditionsspezifische Reviewer, keine erzwungene Roman-Harmony.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P29 — Produkt-UX und Erklärung

**Aufgabe:** Harmonic Explorer, Why This Chord, Composer Workbench als originale Konzepte.

**Belegbare Deliverables:** `EXPLAINABLE_UX_SPEC`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** Quellenstatus und Alternativanalysen sichtbar.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P30 — Codex-Skill-Integration

**Aufgabe:** Kompakter SKILL.md-Router + tiefe referenzierte KB statt Skill-Enzyklopädie.

**Belegbare Deliverables:** `SKILL_REFERENCE_MAP and evals`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** Nicht existierende Dateien nicht referenzieren.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P31 — Testinfrastruktur & CI

**Aufgabe:** Validatoren, musiktheoretische Goldens, Counterexamples, import smoke tests.

**Belegbare Deliverables:** `TEST_MATRIX and CI candidate`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** Mechanische Tests und expert review getrennt.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P32 — Qualitäts-/Quellen-Gates

**Aufgabe:** Claim→SourceLocator→Rule→Example→Test Verbindung prüfen.

**Belegbare Deliverables:** `TRACEABILITY_COVERAGE_REPORT`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** Reviewed-Status nur bei echter Beleg-/Review-Kette.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P33 — Dokumentation/Versionierung

**Aufgabe:** SemVer für Schemata, KB-Releases, Changelog, Alterationsgeschichte.

**Belegbare Deliverables:** `MAINTENANCE_PROTOCOL`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** Keine alte Geschichte stillschweigend überschrieben.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

### P34 — Pull Request Übergabe

**Aufgabe:** Alle Änderungen/Tests/Abweichungen/Reviewstatus vorlegen.

**Belegbare Deliverables:** `PR or patch + IMPLEMENTATION_REPORT`. Speicherort an tatsächlichen Repository-Stil anpassen; keine blind erzeugten doppelten Verzeichnisse.

**Abnahme:** Kein automatischer Merge; keine Falsch-Fertigmeldungen.

**Abhängigkeiten:** Repository Baseline P00/P01/P02 sowie geklärter Schreibscope; fachlich relevante Quellen und Historie berücksichtigen.

**Status im Abschlussreport:** `implemented | partly_implemented | blocked | proposed_only | not_started` mit Pfad, Anzahl und Testergebnis.

## Reihenfolge und Rollout

| Wave | Pakete | Minimal-Gate |
|---|---|---|
| 0 | P00–P05 | Read-only Bestand, Quellen/Rechte/alte Versionen geklärt |
| 1 | P06–P12 | Pitch-Spelling, Tonart, Akkord-/Symbol- und Funktionsmodelle mit Tests |
| 2 | P13–P18 | Breite Harmonie, Stilkontexte, reale Progression und Voice Leading |
| 3 | P19–P25 | Composing mit Motiven, Form, Arrangement, eigentlichen Lehrstücken und Review |
| 4 | P26–P30 | Standards, Corpus-Lizenzen, kulturelle Grenzen, UX und Skill |
| 5 | P31–P34 | QA, Traceability, Versionierung, PR und vollständiger Bericht |

## Qualitätstests: Unterschied technische vs. fachliche Validierung

1. `python 08_Validierung/validate_v5.py` aus der V5-Bibliothek als Baseline ausführen und Ergebnis dokumentieren; dann Projekt-Evaluatoren anpassen.
2. Unit Tests für Enharmonik (F# vs. Gb), Intervallbuchstabierung, globale/lokale Tonart, sekundäre Dominanten, modal-centered vs ii–V, Jazzalterationen, Blues I7.
3. Harmonic Rhythm/Onset/Durations mit 4/4 und 3/4; Test für korrektes Übergreifen von Formgrenzen.
4. 53 neue Familien und 1.378 Varianten nach Idempotenz, Key-Spelling und Variantenherkunft prüfen; Variantenzahl nie als empirische Zahl ausgeben.
5. 16 V5-Partituren: MIDI Type 1, 4 Stimmen, XML, 32 Takte, Spannungsfälle – **musikalisches Review offen**. 30 V4-MIDIs separat prüfen.
6. Claims müssen verlinkbare SourceID + echten Locator und Reviewer für `reviewed` besitzen. `landing_page_checked` reicht nicht.
7. Style-Lenses: keine klassische Kadenzprüfung als alleiniger Blues-/Pop-/Maqam-/Raga-Validator.
8. Bei formal unterschiedlichen Analysen ein dokumentiertes Alternativmodell statt fiktiver eindeutiger Lösung.

## Definition of Done auf Repository-Ebene

- Tatsächlich befüllte Source Registry mit `original_available`, `read_status`, `license_status` und `review_status`.
- Fachlich bearbeitete Concept Cards mit Scope, Gegenbeispielen und nachvollziehbaren Fundstellen.
- Typisierte Rules, eigene Progressions- und Kompositionsobjekte, konkrete Source-to-Claim-to-Test-Beziehungen.
- Theory and Composing Datasets im bestehenden Projekt integriert, nicht lediglich aufgelistet.
- Mechanisch validierte importierte Dateien und separat offen dokumentierte musikfachliche Reviews.
- Keine unterdrückten Lücken, keine unkontrollierten Raw-Book-Uploads, kein unbegründeter `reviewed`-Status.
- Ein PR/Änderungsbericht mit Diff, Pfaden, Tests, Source Coverage, Qualität, Blockern und priorisierten Folgewellen.

## Schlussausgabe (Pflicht)

A. Repository-Ausgangszustand und erhaltene Nutzeränderungen. B. Quellen: verfügbar/gelesen/teilweise/blocked/rechtlich ungeklärt. C. Tatsächliche Knowledge-Coverage je vier Säulen und Repertoire-Scope. D. Regeln/Beispiele/Composing-Studien: erstellt/importiert/geprüft/nicht geprüft. E. Tests: ausgeführt/bestanden/fehlgeschlagen/nicht möglich. F. Fachliche Konflikte/alternative Analysen. G. PR/Branch/Dateiänderungen. H. Nächste konkrete, priorisierte Arbeitspakete.

**Starte mit dem read-only Repository-Audit, sichere die Historie und arbeite danach in machbaren, überprüfbaren Batches. Stelle keinen Zeitplan oder Merge als selbstverständlich dar.**
