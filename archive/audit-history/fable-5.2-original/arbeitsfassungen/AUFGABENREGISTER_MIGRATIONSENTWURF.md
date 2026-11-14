# STEPS – Migrationsentwurf zum Aufgabenregister

**Historischer Speicherort:** `%LOCALAPPDATA%\StepsKnowledge\OFFENE_ARBEITSAUFFORDERUNGEN.md`  
**Datenstand:** 10. November 2026, 21:35 Uhr (Phase 3.1 Deep Analysis & Skill Hardening)  
**Geltungsbereich:** Gesamtes STEPS-Projekt einschließlich historischer Register, Forschungsdokumente und Audits  
**Status:** Migrationsentwurf aus dem Repository-Snapshot vom 11.11.2026. SHA-256 des Exports `dd27e30cfc706d6d2aa8b0a94bcd245e9c4f8804fb272db0c0665096f1cdc7f3`.

---

## 1. Zusammenfassung aller Arbeitsaufforderungen

| ID | Titel | Kategorie | Priorität | Status | Owner-Entscheidung? |
|---|---|---|:---:|:---:|:---:|
| **OA-0001** | Beseitigung der Urheberrechts- und Veröffentlichungsrisiken (P0-1) | Rechte & Veröffentlichung | P0 | `OPEN` | JA |
| **OA-0002** | CI-Pfadfilter-Erweiterung für src/steps/** (CI-Trigger-Fix) | CI / Qualitätssicherung | P1 | `DONE_VERIFIED` | NEIN |
| **OA-0003** | Beschlussfassung ADR-001 (Fensterarchitektur: 2-Pane vs 2-Toplevel) | Architektur / UI-Shell | P0 | `OWNER_DECISION_REQUIRED` | JA |
| **OA-0004** | Beschlussfassung ADR-002 (MVP-Umfang: Phasen-Splitting Harmonik vs. Drums) | Produktstrategie / Roadmap | P0 | `OWNER_DECISION_REQUIRED` | JA |
| **OA-0005** | Beschlussfassung ADR-005 (Notationskonventionen & Enharmonik) | Musiktheorie / Datenmodell | P0 | `OWNER_DECISION_REQUIRED` | JA |
| **OA-0006** | Implementierung T-06 (Tk-freier Musiktheorie-Domänenkern in src/steps/theory/) | Implementierung / Fachmodell | P1 | `OPEN` | NEIN |
| **OA-0007** | Realisierung Shell-Spikes B vs. D (Entkopplung der Glide-Shell) | Architektur / UI-Shell | P1 | `OPEN` | JA |
| **OA-0008** | Bereinigung und Strukturierung der Knowledge-Registry (registry.yaml) | Wissensbasis / Provenienz | P1 | `OPEN` | NEIN |
| **OA-0009** | Bereinigung defekter relativer Markdown-Links (Link-Reparaturplan) | Dokumentation / Integrität | P2 | `OPEN` | NEIN |
| **OA-0010** | Reparatur der Mojibake-Kodierung in INVESTIGATION_COVERAGE_33_V2.csv | Dokumentation / Datenqualität | P2 | `OPEN` | NEIN |
| **OA-0011** | Härtung & Validierung Antigravity-Skill 'steps-knowledge-curation' | Skill / Tooling | P1 | `DONE_VERIFIED` | NEIN |
| **OA-0012** | Beschlussfassung ADR-002: Drums-Zurückstellung für v0.1 (Klarstellung) | Produktstrategie | P0 | `OWNER_DECISION_REQUIRED` | JA |
| **OA-0013** | Historische Aufgabe T-04: Package Scaffolding (src/steps/ Paketstruktur) | Infrastruktur | P0 | `DONE_VERIFIED` | Erledigt |
| **OA-0014** | Aufbau der Golden Test Suite v0.1 (T01..T16 / 100+ Musiktheorie-Tests) | Qualitätssicherung / Fachtests | P1 | `OPEN` | NEIN |
| **OA-0015** | Implementierung der Stimmführungs-Distanzmetrik (Tymoczko Metric) | Musiktheorie / Algorithmen | P1 | `OPEN` | NEIN |
| **OA-0016** | Datenimporter für offene Harmonik-Korpora (ChoCo & When in Rome) | Korpus / Statistik | P2 | `OPEN` | NEIN |
| **OA-0017** | Reparatur oder kontrollierte Aussonderung von MakingMusic.pdf | Wissensbasis / Datenintegrität | P2 | `OPEN` | NEIN |
| **OA-0018** | Automatisierte Validierungs-Pipeline für 112 Standard-MIDI-Dateien | Datenqualität / Audio-Engine | P2 | `OPEN` | NEIN |
| **OA-0019** | Formalisierung der hierarchischen Syntaxgrammatik (Rohrmeier Generative Syntax) | Musiktheorie / Formale Grammatik | P2 | `OPEN` | NEIN |
| **OA-0020** | Integration der Cyclic-Group Transpositionslogik (Z12 / Modulo 12) | Musiktheorie / Datenmodell | P1 | `OPEN` | NEIN |
| **OA-0021** | Spezifikation der Contrapuntal Motion Klassifizierung | Musiktheorie / Algorithmen | P2 | `OPEN` | NEIN |
| **OA-0022** | Implementierung der parametrisierbaren Swing-Ratio & Micro-Timing Engine (M07) | Rhythmik / Audio-Engine | P1 | `OPEN` | NEIN |
| **OA-0023** | Ausarbeitung erweiterter Genre-Profile (Techno, Boom-Bap, UK Garage, Trap) (M09) | Musikforschung / Genre-Atlas | P1 | `OPEN` | NEIN |
| **OA-0024** | Didaktische Reduktions-Engine für Klavieranfänger (M10/M12) | Pädagogik / UI-Interaktion | P1 | `OPEN` | NEIN |
| **OA-0025** | Formalisierung der Akkordumkehrungs-Engine und Voicing-Klassifikation (M04) | Musiktheorie / Kernmodell | P1 | `OPEN` | NEIN |
| **OA-0026** | Stilistische Differenzierung von Stimmführungsregeln (M06) | Musiktheorie / Algorithmen | P1 | `OPEN` | NEIN |
| **OA-0027** | Implementierung formaler Property-Based Tests für Musiktheorie-Invarianten (M01/M04) | Qualitätssicherung / Fachtests | P1 | `OPEN` | NEIN |
| **OA-0028** | Bereitstellung der Standard-SMF-Parser & Serialisierungs-Engine (M11) | Infrastruktur / MIDI-Engine | P1 | `OPEN` | NEIN |
| **OA-0029** | Implementierung der rationalen MIDI-Zeit-Engine & variablen PPQ-Konvertierung (M11) | Infrastruktur / MIDI-Engine | P1 | `OPEN` | NEIN |
| **OA-0030** | Implementierung der Shell-Voicing & Guide-Tone-Engine (M04/M10) | Musiktheorie / Algorithmen | P1 | `OPEN` | NEIN |
| **OA-0031** | Implementierung des musikalischen Referenz-ID Integritäts-Checkers (M01-M12/Skill) | Qualitätssicherung / Tooling | P1 | `OPEN` | NEIN |
| **OA-0032** | Implementierung der Cross-Domain Empfehlungs-Engine (Harmonik <-> Drums <-> Piano) | Musiktheorie / Algorithmen | P2 | `OPEN` | NEIN |
| **OA-0033** | SECURITY – Triage & Behebung der Google API Key Alerts (#1–#3) | Sicherheit / Secret Scanning | P1 | `OWNER_DECISION_REQUIRED` | JA |

---

## 2. P0 – Kritische Blocker und Sofortentscheidungen

### OA-0001: Beseitigung der Urheberrechts- und Veröffentlichungsrisiken (P0-1)

* **Kategorie:** Rechte & Veröffentlichung · **Status:** `OPEN` · **Ursprung:** EXPLICIT
* **Beschreibung:** 7 kommerzielle Lehrbücher und Z-Library-Dateien sowie 53 weitere PDFs, 74 Ableton-MIDIs und kompilierte Binaries liegen im öffentlichen Git-Repository.
* **Quellen & Fundstellen:** 02_RIGHTS_AND_PUBLICATION_RISK_TRIAGE.csv; 04_P0_BLOCKERS_AND_ACTION_PLAN.md; W-04; G-04
* **Historischer Kontext:** Im Phase-2A-Audit identifiziert; betrifft Haftung und DMCA-Risiko.
* **Betroffene Bereiche:** `research/STEPS_Bibliothek/; .git history; GitHub-Repository-Einstellungen`
* **Erbrachte Nachweise:** Triage-CSV mit 965 Triagedateien vollständig erstellt
* **Verbleibende Arbeiten:** Owner-Entscheidung treffen: Repo auf 'Privat' schalten oder Git-Historie bereinigen
* **Abhängigkeiten & Blocker:** Keine / Wartet auf Owner-Beschluss
* **Abnahmekriterien:** Repo privat ODER geschützte Blobs aus Git entfernt
* **Erforderliche Owner-Entscheidung:** JA: Option A (privat) vs. Option C (Purge)
* **Empfohlener nächster Schritt:** Entscheidung durch Project Owner herbeiführen

---

### OA-0003: Beschlussfassung ADR-001 (Fensterarchitektur: 2-Pane vs 2-Toplevel)

* **Kategorie:** Architektur / UI-Shell · **Status:** `OWNER_DECISION_REQUIRED` · **Ursprung:** EXPLICIT
* **Beschreibung:** Klassifizierung der Fenstersemantik: 1 Tk-Root mit zwei Panes (Sidebar + Workspace) vs. zwei getrennte OS-Toplevel-Fenster.
* **Quellen & Fundstellen:** ADR-001-Fensterarchitektur.md; N-02; SHELL_EXTRACTION_DEEP_SPEC.md
* **Historischer Kontext:** Entwurfsempfehlung: Option A (1 Root, 2 Panes, modale Dialoge).
* **Betroffene Bereiche:** `decisions/ADR-001-Fensterarchitektur.md; decisions/DECISION_REGISTER.md; app/ui/`
* **Erbrachte Nachweise:** Entwurfsvorlage in Phase 2D vollständig ausgearbeitet
* **Verbleibende Arbeiten:** Owner-Bestätigung von Option A
* **Abhängigkeiten & Blocker:** Keine / Wartet auf Owner
* **Abnahmekriterien:** ADR-001 Status = ACCEPTED mit Datum und Owner-Signatur
* **Erforderliche Owner-Entscheidung:** JA: Option A bestätigen
* **Empfohlener nächster Schritt:** Beschluss durch Owner

---

### OA-0004: Beschlussfassung ADR-002 (MVP-Umfang: Phasen-Splitting Harmonik vs. Drums)

* **Kategorie:** Produktstrategie / Roadmap · **Status:** `OWNER_DECISION_REQUIRED` · **Ursprung:** EXPLICIT
* **Beschreibung:** Festlegung des Scopes für v0.1: Reiner Fokus auf Harmonik und Akkorde (v0.1); Drums, Groove-Grid und Live-Audio in v0.2.
* **Quellen & Fundstellen:** ADR-002-MVP-Umfang.md; REQ-024; N-01; PROJECT_CONTEXT_HANDOVER.md:162
* **Historischer Kontext:** Handover REQ-024 deklarierte Drums als DEFERRED; Produktvision nannte Drums. Lösung: Phasen-Splitting.
* **Betroffene Bereiche:** `decisions/ADR-002-MVP-Umfang.md; decisions/DECISION_REGISTER.md; Roadmap`
* **Erbrachte Nachweise:** Entwurfsvorlage in Phase 2D vollständig ausgearbeitet
* **Verbleibende Arbeiten:** Owner-Bestätigung von Option A (Phasen-Splitting)
* **Abhängigkeiten & Blocker:** Keine / Wartet auf Owner
* **Abnahmekriterien:** ADR-002 Status = ACCEPTED
* **Erforderliche Owner-Entscheidung:** JA: Scope v0.1 bestätigen
* **Empfohlener nächster Schritt:** Beschluss durch Owner

---

### OA-0005: Beschlussfassung ADR-005 (Notationskonventionen & Enharmonik)

* **Kategorie:** Musiktheorie / Datenmodell · **Status:** `OWNER_DECISION_REQUIRED` · **Ursprung:** EXPLICIT
* **Beschreibung:** Verbindliche Festlegung des Notenmodells: Internes internationales 12-TET-Spelling mit umschaltbarer Ein-/Ausgabe-Projektion (international B/Bb, deutsch H/B).
* **Quellen & Fundstellen:** ADR-005-Notationskonventionen.md; MUSIC_DOMAIN_AND_MIDI.md:42; W-05
* **Historischer Kontext:** Vermeidet Ambiguitäten bei isoliertem 'B' und sichert verlustfreie Enharmonik (Cs != Db).
* **Betroffene Bereiche:** `decisions/ADR-005-Notationskonventionen.md; src/steps/theory/`
* **Erbrachte Nachweise:** Entwurfsvorlage in Phase 2D vollständig ausgearbeitet
* **Verbleibende Arbeiten:** Owner-Bestätigung von Option A
* **Abhängigkeiten & Blocker:** Keine / Wartet auf Owner
* **Abnahmekriterien:** ADR-005 Status = ACCEPTED
* **Erforderliche Owner-Entscheidung:** JA: Notationsmodell bestätigen
* **Empfohlener nächster Schritt:** Beschluss durch Owner

---

### OA-0012: Beschlussfassung ADR-002: Drums-Zurückstellung für v0.1 (Klarstellung)

* **Kategorie:** Produktstrategie · **Status:** `OWNER_DECISION_REQUIRED` · **Ursprung:** INFERRED
* **Beschreibung:** Formelle Verknüpfung der historischen Anforderung REQ-024 mit ADR-002. War in Phase 3 fälschlich als DONE_VERIFIED markiert, obwohl ADR-002 noch den Status PROPOSED trägt.
* **Quellen & Fundstellen:** PROJECT_CONTEXT_HANDOVER.md:162; REQ-024; ADR-002; Phase 3.1 Audit-Korrektur
* **Historischer Kontext:** Solange ADR-002 nicht formell durch den Owner gezeichnet ist, bleibt die Zurückstellung von Drums eine vorgeschlagene Marschrichtung, keine verifizierte Tatsache.
* **Betroffene Bereiche:** `docs/product/PRODUCT_STRATEGY_AND_MVP.md; decisions/ADR-002-MVP-Umfang.md`
* **Verbleibende Arbeiten:** Owner-Freigabe von ADR-002 abwarten; danach Status auf SUPERSEDED_BY_ADR002 setzen.
* **Abhängigkeiten & Blocker:** OA-0004
* **Abnahmekriterien:** ADR-002 angenommen
* **Erforderliche Owner-Entscheidung:** JA

---

## 3. P1 – Technische und fachliche Voraussetzungen

### OA-0002: CI-Pfadfilter-Erweiterung für src/steps/** (CI-Trigger-Fix)

* **Kategorie:** CI / Qualitätssicherung · **Status:** `DONE_VERIFIED` · **Ursprung:** EXPLICIT
* **Commit:** e2826fec433ab3988cf4cd835ddd0b500c29058b
* **Prüfung:** Die Workflow-Läufe 42905452820 und 42905512016 stehen für den PR-Commit aa8fba142f668d5a87f0892f9d1c5b7c144927e6 auf success.
* **Abnahmebeleg:** https://github.com/n05a-design/steps/pull/6
* **Abnahmekriterien:** Änderungen unter src/**, tests/** und .agents/** lösen den Strukturworkflow aus.
* **Beschreibung:** Workflow .github/workflows/structure-check.yml überwacht nun src/**, tests/**, pyproject.toml und .agents/**. Vollständig verifiziert über PR #6 und in `main` integriert (Merge Commit e2826fe).
* **Quellen & Fundstellen:** 02_CI_COVERAGE_ANALYSIS.md; .github/workflows/structure-check.yml; PR #6
* **Betroffene Bereiche:** `.github/workflows/structure-check.yml`, `tests/test_structure.py`
* **Erbrachte Nachweise:** GitHub Actions Runs #42905452820 und #42905512016 grün (SUCCESS); Merge in `main` bestätigt.
* **Verbleibende Arbeiten:** Keine. Aufgabe erfolgreich abgeschlossen.

---

### OA-0006: Implementierung T-06 (Tk-freier Musiktheorie-Domänenkern in src/steps/theory/)

* **Kategorie:** Implementierung / Fachmodell · **Status:** `OPEN` · **Ursprung:** EXPLICIT
* **Beschreibung:** Erstellung der reinen, unvollständigen Domänenlogik in src/steps/theory/ (PitchClass, Accidental, NoteSpelling, Scale, Chord) mit 100% Goldentests.
* **Quellen & Fundstellen:** 04_T06_READINESS_SPEC.md; MUSIC_DOMAIN_AND_MIDI.md; REQ-002..004
* **Betroffene Bereiche:** `src/steps/theory/ (pitch.py, intervals.py, scales.py, chords.py); tests/theory/`
* **Verbleibende Arbeiten:** Quellcode implementieren und Unit-Tests zum Bestehen bringen
* **Abnahmekriterien:** Alle 16 Goldentests bestehen; kein Tkinter-Import; 0 Seiteneffekte
* **Empfohlener nächster Schritt:** Branch feat/steps-theory-domain-t06 anlegen und implementieren

---

### OA-0007: Realisierung Shell-Spikes B vs. D (Entkopplung der Glide-Shell)

* **Kategorie:** Architektur / UI-Shell · **Status:** `OPEN` · **Ursprung:** EXPLICIT
* **Beschreibung:** Entwicklung zweier isolierter Vergleichsspikes unter den 30 Shell-Szenarien (Spike B: selektive Extraktion; Spike D: neutrale Tk-Shell mit Glide-Designverträgen).
* **Quellen & Fundstellen:** SHELL_EXTRACTION_DEEP_SPEC.md; 07_STEPS_ARCHITECTURE_AND_START_GATE.md
* **Betroffene Bereiche:** `app/ui/; src/steps/ports/`
* **Verbleibende Arbeiten:** Spike B und Spike D in isoliertem Testverzeichnis aufbauen und vergleichen
* **Abnahmekriterien:** App startet ohne Glide-Datenkontakt; S01..S30 verifiziert
* **Empfohlener nächster Schritt:** Spike-Konzeption starten nach T-06

---

### OA-0008: Bereinigung und Strukturierung der Knowledge-Registry (registry.yaml)

* **Kategorie:** Wissensbasis / Provenienz · **Status:** `OPEN` · **Ursprung:** EXPLICIT
* **Beschreibung:** Befüllung der leeren knowledge/sources/registry.yaml mit einem ersten validierten Pilotbatch rechtlich freier Quellen.
* **Quellen & Fundstellen:** knowledge/sources/registry.yaml; INGESTION_PIPELINE.md; REQ-005..007; G-09
* **Betroffene Bereiche:** `knowledge/sources/registry.yaml; knowledge/concepts/`
* **Verbleibende Arbeiten:** 1-3 gemeinfreie / freigegebene Quellen identifizieren, claims extrahieren und schema-validieren
* **Abnahmekriterien:** Mindestens 1 valide Quelle mit Claims und Abfragetest registriert
* **Empfohlener nächster Schritt:** Pilotbatch mit gemeinfreiem Standardwerk starten

---

### OA-0011: Härtung & Validierung Antigravity-Skill 'steps-knowledge-curation'

* **Kategorie:** Skill / Tooling · **Status:** `DONE_VERIFIED` · **Ursprung:** EXPLICIT
* **Commit:** 3a95765ed17cfddeaa23b6d808dd6e8a89ef73ae
* **Prüfung:** 36 Skilltests auf macOS sowie Windows im CI-Lauf 43361781637. Snapshot-Restore und Rücksicherung in einem temporären Ziel bytegleich geprüft.
* **Abnahmebeleg:** https://github.com/n05a-design/steps/pull/15
* **Abnahmekriterien:** Backup mit Manifest, validierter atomarer Restore und Wiederherstellung des Vorzustands.
* **Beschreibung:** Standardisierter Agent-Skill in .agents/skills/steps-knowledge-curation/ mit 17 Dateien, 5 Curation-Tools und 25 Unittests. Vollständig verifiziert und in `main` integriert (Merge Commit dbd319a via PR #5).
* **Quellen & Fundstellen:** Phase 3.1–4.1 Master Prompts; PR #5; .agents/skills/steps-knowledge-curation/
* **Betroffene Bereiche:** `.agents/skills/steps-knowledge-curation/`
* **Erbrachte Nachweise:** 25/25 Tests lokal grün (0.084s); E2E-Pipeline verifiziert; Neuinstallationsprüfung bestanden; Merge in `main` bestätigt.
* **Verbleibende Arbeiten:** Keine. Skill ist produktiv im Repository verfügbar.

---

### OA-0014: Aufbau der Golden Test Suite v0.1 (T01..T16 / 100+ Musiktheorie-Tests)

* **Kategorie:** Qualitätssicherung / Fachtests · **Status:** `OPEN` · **Ursprung:** INFERRED
* **Beschreibung:** Aufbau von mindestens 100 deterministischen Unit-Tests für elementare Musiktheorie (Tonhöhen, Intervalle, Skalen, Akkorde, enharmonische Äquivalenz, Transposition).
* **Quellen & Fundstellen:** 01_STEPS_Research_Foundation.md (Recommended acceptance tests); Forschungs- und Projektgrundlage.md (Minimal Viable Deliverables)
* **Betroffene Bereiche:** `tests/theory/`
* **Verbleibende Arbeiten:** Testsuite gegen T-06 Domain Core erstellen
* **Abnahmekriterien:** 100+ Tests bestehen deterministisch ohne UI-Abhängigkeit

---

### OA-0015: Implementierung der Stimmführungs-Distanzmetrik (Tymoczko Metric)

* **Kategorie:** Musiktheorie / Algorithmen · **Status:** `OPEN` · **Ursprung:** INFERRED
* **Beschreibung:** Berechnung minimaler Tonverschiebungen unter Oktaväquivalenz zur objektiven Bewertung von Akkordübergängen unabhängig von Stufenbezeichnungen.
* **Quellen & Fundstellen:** 01_STEPS_Research_Foundation.md (Section Voice-leading geometry); Dmitri Tymoczko "A Geometry of Music"
* **Betroffene Bereiche:** `src/steps/voiceleading/`
* **Verbleibende Arbeiten:** Algorithmus zur minimalen euklidischen / Manhattan-Distanz zwischen Akkord-Voicings implementieren
* **Abnahmekriterien:** Minimaldistanz-Tests für Common-Practice-Kadenzen und mediantische Rückungen bestehen

---

## 4. P2 & P3 – Qualität, Wartung und langfristige Vorhaben

### OA-0009: Bereinigung defekter relativer Markdown-Links (Link-Reparaturplan)

* **Kategorie:** Dokumentation / Integrität · **Status:** `OPEN`
* **Beschreibung:** 683 von 923 relativen Markdown-Links lösen lokal nicht auf (überwiegend in archivierten Paketkopien).
* **Quellen:** link_check_broken.csv (Phase 1); NEW-015
* **Verbleibende Arbeiten:** Kanonische Dokumente reparieren; Archivdateien als 'historischer Pfadstand' kennzeichnen

---

### OA-0010: Reparatur der Mojibake-Kodierung in INVESTIGATION_COVERAGE_33_V2.csv

* **Kategorie:** Dokumentation / Datenqualität · **Status:** `OPEN`
* **Beschreibung:** Datei manifests/INVESTIGATION_COVERAGE_33_V2.csv ist doppelt UTF-8-kodiert (Umlaute zerschossen).
* **Quellen:** manifests/INVESTIGATION_COVERAGE_33_V2.csv; NEW-005
* **Verbleibende Arbeiten:** Datei sauber re-enkodieren ohne Informationsverlust

---

### OA-0016: Datenimporter für offene Harmonik-Korpora (ChoCo & When in Rome)

* **Kategorie:** Korpus / Statistik · **Status:** `OPEN` · **Ursprung:** INFERRED
* **Beschreibung:** Erstellung von Datenadaptern für JAMS/ChoCo und When in Rome zur empirischen Absicherung von Akkordübergangswahrscheinlichkeiten.
* **Quellen & Fundstellen:** 01_STEPS_Research_Foundation.md; 02_STEPS_Knowledge_Base_Product_Blueprint.md
* **Betroffene Bereiche:** `src/steps/corpus/`
* **Verbleibende Arbeiten:** Parser für JAMS-Dateien und RomanText evaluieren und implementieren

---

### OA-0017: Reparatur oder kontrollierte Aussonderung von MakingMusic.pdf

* **Kategorie:** Wissensbasis / Datenintegrität · **Status:** `OPEN` · **Ursprung:** EXPLICIT
* **Beschreibung:** Die Datei research/STEPS_Bibliothek/MakingMusic.pdf ist beschädigt und kann nicht als PDF geparst werden.
* **Quellen & Fundstellen:** 01_STEPS_Research_Foundation.md (Line Initial Sources v1.0 table); OPEN_GAPS.md
* **Betroffene Bereiche:** `research/STEPS_Bibliothek/MakingMusic.pdf`
* **Verbleibende Arbeiten:** Datei reparieren, neu beschaffen oder formell als defekt kennzeichnen und aus dem aktiven Review ausschließen

---

### OA-0018: Automatisierte Validierungs-Pipeline für 112 Standard-MIDI-Dateien

* **Kategorie:** Datenqualität / Audio-Engine · **Status:** `OPEN` · **Ursprung:** INFERRED
* **Beschreibung:** Erstellung eines automatisierten Testskripts, das alle 112 inventarisierten MIDIs auf Abspielbarkeit, Trackanzahl, Notenereignisse und Timing prüft.
* **Quellen & Fundstellen:** STEPS Project Export.md (Section MIDI Parsing Example); MIDI_ANALYSIS_REGISTER.csv
* **Betroffene Bereiche:** `tools/validation/check_midis.py; research/STEPS_Bibliothek/`
* **Verbleibende Arbeiten:** Skript basierend auf mido implementieren und in CI/Audit integrieren

---

### OA-0019: Formalisierung der hierarchischen Syntaxgrammatik (Rohrmeier Generative Syntax)

* **Kategorie:** Musiktheorie / Formale Grammatik · **Status:** `OPEN` · **Ursprung:** INFERRED
* **Beschreibung:** Ausarbeitung formaler Grammatikregeln für funktionale Kadenzen (Tonic -> Predominant -> Dominant -> Tonic) als kontextfreie Baumstruktur.
* **Quellen & Fundstellen:** 01_STEPS_Research_Foundation.md; Martin Rohrmeier "Towards a generative syntax of tonal harmony"
* **Betroffene Bereiche:** `src/steps/theory/syntax.py`
* **Verbleibende Arbeiten:** Grammatikbaum-Datenstrukturen definieren

---


### OA-0020: Integration der Cyclic-Group Transpositionslogik (Z12 / Modulo 12)

* **Kategorie:** Musiktheorie / Datenmodell · **Status:** `OPEN` · **Ursprung:** INFERRED
* **Beschreibung:** Mathematische Absicherung der Transpositions-Invarianz nach David Wright (Mathematics and Music, CLM-0047, CLM-0042): Intervalladdition als Modulo-12-Gruppenoperation über Z_12 mit Erhalt der Intervallvektoren.
* **Quellen & Fundstellen:** Mathematics_and_Music.pdf; the-chord-wheel.pdf; CLM-0042; CLM-0047
* **Betroffene Bereiche:** src/steps/theory/pitch.py; src/steps/theory/spelling.py
* **Verbleibende Arbeiten:** Transpositionsmethode implementieren und gegen Invariante T07 testen
* **Abnahmekriterien:** Modulo-12 Arithmetik bildet Transpositionen verlustfrei und enharmonisch korrekt ab

### OA-0021: Spezifikation der Contrapuntal Motion Klassifizierung

* **Kategorie:** Musiktheorie / Algorithmen · **Status:** `OPEN` · **Ursprung:** INFERRED
* **Beschreibung:** Implementierung der relativen Stimmbewegungs-Klassifikation (gegenläufig, schräg, ähnlich, parallel) gemäß THE_ELEMENTS_OF_MUSIC (CLM-0051) zur automatisierten Erkennung von Parallelen und Stimmführungsmustern.
* **Quellen & Fundstellen:** THE_ELEMENTS_OF_MUSIC.pdf; CLM-0051; MUSIC_DOMAIN_AND_MIDI.md (T10)
* **Betroffene Bereiche:** src/steps/voiceleading/motion.py
* **Verbleibende Arbeiten:** Motion-Classifier für Paare aufeinanderfolgender Voicings implementieren
* **Abnahmekriterien:** Korrekte Erkennung von Contrary, Oblique, Similar und Parallel Motion in Testfällen

---

## 5. Nachweislich abgeschlossene Aufgaben (DONE_VERIFIED)

### OA-0013: Historische Aufgabe T-04: Package Scaffolding (src/steps/ Paketstruktur)

* **Kategorie:** Infrastruktur · **Status:** `DONE_VERIFIED`
* **Commit:** 190228a352c9417d381a6470cc56d4f4b83ed2fc
* **Prüfung:** Historischer Struktur- und Importtest im Merge von PR #4 dokumentiert. Struktur und Import des aktuellen Kerns lokal erneut geprüft.
* **Abnahmebeleg:** https://github.com/n05a-design/steps/pull/4
* **Abnahmekriterien:** Importierbare Paketstruktur unter src/steps und erfolgreiche Repository-Strukturprüfung.
* **Abschlussbeleg:** Gemergt in main @ 190228a (PR #4); Strukturtest check_structure.py und Importtest PASS (Exit-Code 0).
* **Quellen:** PR #4; Commit 190228a; 01_POST_MERGE_BASELINE.md

---

### OA-0022: Implementierung der parametrisierbaren Swing-Ratio & Micro-Timing Engine (M07)

* **Kategorie:** Rhythmik / Audio-Engine · **Status:** `OPEN` · **Ursprung:** INFERRED
* **Beschreibung:** Realisierung einer mathematisch präzisen Swing-Engine mit einstellbarer Swing-Ratio rho (1.0 bis 2.0) und dynamischer Tick-Verschiebung für Standard-MIDI-Events (480/960 PPQ).
* **Quellen & Fundstellen:** MUSIC_KNOWLEDGE_ONTOLOGY.md (M07-04); GENRE_HARMONY_AND_DRUM_ATLAS.md; GAP-M07
* **Betroffene Bereiche:** `src/steps/progression/`, `src/steps/ports/`
* **Verbleibende Arbeiten:** Algorithmus zur ungeraden 8tel-/16tel-Streckung implementieren und mit GM-Drum-Patterns testen.
* **Abnahmekriterien:** Goldentests REF-0020 und REF-0021 erfolgreich; sauberer Swing ohne Jitter.
* **Empfohlener nächster Schritt:** Spezifikation der Zeit-Transformationsfunktion nach T-06.

---

### OA-0023: Ausarbeitung erweiterter Genre-Profile (Techno, Boom-Bap, UK Garage, Trap) (M09)

* **Kategorie:** Musikforschung / Genre-Atlas · **Status:** `OPEN` · **Ursprung:** EXPLICIT
* **Beschreibung:** Erweiterung des GENRE_HARMONY_AND_DRUM_ATLAS über die Piloten Pop und House hinaus um detaillierte Harmonik- und Drum-Event-Matrizen für Techno, Boom-Bap, UK Garage und Trap basierend auf den vorhandenen SMF-MIDI-Beständen.
* **Quellen & Fundstellen:** research/STEPS_Bibliothek/Drums Progression/; GENRE_HARMONY_AND_DRUM_ATLAS.md
* **Betroffene Bereiche:** `research/STEPS_Bibliothek/`, `knowledge/concepts/styles/`
* **Verbleibende Arbeiten:** MIDI-Tracks analysieren, Velocity- und Timing-Kurven erfassen, Event-Tabellen dokumentieren.
* **Abnahmekriterien:** Mindestens 4 neue vollständige Genreprofile mit 2- bis 4-taktigen Event-Tabellen.
* **Empfohlener nächster Schritt:** Batch-2-Analyse der PPR-MIDI-Korpora in Phase 4.1.

---

### OA-0024: Didaktische Reduktions-Engine für Klavieranfänger (M10/M12)

* **Kategorie:** Pädagogik / UI-Interaktion · **Status:** `OPEN` · **Ursprung:** EXPLICIT
* **Beschreibung:** Konzeption und Implementierung einer automatischen Voice-Leading- und Fingersatz-Empfehlungskomponente, die komplexe Akkordfolgen für Anfänger ergonomisch auf minimalen Handweg am Klavier abbildet (Smooth Voice-Leading).
* **Quellen & Fundstellen:** PIANO_LEARNING_PATH.md; MUSIC_KNOWLEDGE_ONTOLOGY.md (M10-06, M12-04)
* **Betroffene Bereiche:** `src/steps/theory/`, `app/ui/`
* **Verbleibende Arbeiten:** Umkehrungs-Optimierer basierend auf minimaler Tastatur-Distanz entwerfen.
* **Abnahmekriterien:** Automatische Generierung von Anfänger-Fingersätzen für Pop-Four-Chords; Vermeidung von Handsprüngen.
* **Empfohlener nächster Schritt:** Integration in die Akkord-Generierungslogik nach T-06.

---

### OA-0025: Formalisierung der Akkordumkehrungs-Engine und Voicing-Klassifikation (M04)

* **Kategorie:** Musiktheorie / Kernmodell · **Status:** `OPEN` · **Ursprung:** EXPLICIT
* **Beschreibung:** Realisierung eines formalen Algorithmus zur Bestimmung von Akkordumkehrungen basierend auf dem tiefsten Basston (Grundstellung 5/3, 1. Umkehrung 6, 2. Umkehrung 6/4) unter strikter Unterscheidung zwischen dem Hand-Voicing und der Gesamtakkord-Inversion (Korrektur ERR-006).
* **Quellen & Fundstellen:** MUSICAL_CORRECTION_TRACEABILITY.md; PIANO_EXERCISE_VALIDATION.md; ERR-006; Aldwell & Schachter Kap. 4–5
* **Betroffene Bereiche:** `src/steps/theory/chords.py`, `tests/theory/`
* **Verbleibende Arbeiten:** Python-Funktionen `get_inversion(bass_note, chord_notes)` und `detect_hand_voicing()` implementieren und gegen REF-0031 und REF-0032 testen.
* **Abnahmekriterien:** 100% korrekte Unterscheidung von A3-C4-E4 (Grundstellung) und A3-C4-F4 (1. Umkehrung).
* **Empfohlener nächster Schritt:** Integration in die Akkord-Logik von T-06.

---

### OA-0026: Stilistische Differenzierung von Stimmführungsregeln (M06)

* **Kategorie:** Musiktheorie / Algorithmen · **Status:** `OPEN` · **Ursprung:** EXPLICIT
* **Beschreibung:** Parametrisierbare Satzregeln-Engine für Voice-Leading, die zwischen strengem historischem Kontrapunkt (Verbot paralleler reiner Quinten/Oktaven) und modernen populären Genres (Pop, Rock Power-Chords, Jazz-Quartenharmonik) unterscheidet (Korrektur ERR-009).
* **Quellen & Fundstellen:** MUSICAL_CORRECTION_TRACEABILITY.md; ERR-009; Everett Foundations of Rock
* **Betroffene Bereiche:** `src/steps/theory/voice_leading.py`, `src/steps/progression/`
* **Verbleibende Arbeiten:** Stil-Filter in Voice-Leading-Prüfungen implementieren (`strict_classical` vs. `contemporary_pop`).
* **Abnahmekriterien:** Pop-Progression C-G-Am-F wirft im Pop-Modus keine Fehler für Quintfortschreitungen aus.
* **Empfohlener nächster Schritt:** Spezifikation im Rahmen von T-06 / M06.

---

### OA-0027: Implementierung formaler Property-Based Tests für Musiktheorie-Invarianten (M01/M04)

* **Kategorie:** Qualitätssicherung / Fachtests · **Status:** `OPEN` · **Ursprung:** EXPLICIT
* **Beschreibung:** Einführung von Hypothesis-basierten Property-Tests zur mathematischen Verifikation fundamentaler Musiktheorie-Invarianten (Oktav-Modulo-Invarianz, Umkehrungs-Tonmengen-Invarianz, Tymoczko-Metrik-Axiome nach L1-Norm).
* **Quellen & Fundstellen:** MUSICAL_PROPERTY_TEST_SPEC.md; Phase 4.3 Master Prompt; Tymoczko: Geometry of Music
* **Betroffene Bereiche:** `tests/theory/test_properties.py`, `src/steps/theory/`
* **Verbleibende Arbeiten:** Testmodul `tests/theory/test_properties.py` erstellen und mit Hypothesis-Strategien ausrüsten.
* **Abnahmekriterien:** 1.000 generierte Testfälle pro Eigenschaft ohne Fehlschlag; mathematische Metrik-Axiome formal verifiziert.
* **Empfohlener nächster Schritt:** Integration in die Testsuite von T-06.

---

### OA-0028: Bereitstellung der Standard-SMF-Parser & Serialisierungs-Engine (M11)

* **Kategorie:** Infrastruktur / MIDI-Engine · **Status:** `OPEN` · **Ursprung:** EXPLICIT
* **Beschreibung:** Implementierung eines leichtgewichtigen, rein Python-basierten Standard MIDI File Parsers und Exporters für SMF Format 0 und Format 1 mit Unterstützung für 480 PPQ, variabler Delta-Time-Dekodierung, Running Status und Standard Meta-Events (Tempo 0x51, TimeSignature 0x58).
* **Quellen & Fundstellen:** INDEPENDENT_MUSIC_VALIDATION_REPORT.md; MMA MIDI 1.0 Spec; SRC-003; SRC-009
* **Betroffene Bereiche:** `src/steps/ports/midi/`, `tests/integration/`
* **Verbleibende Arbeiten:** Parser-Klasse `SMFParser` in `src/steps/ports/midi/smf.py` implementieren und gegen die 112 Bibliotheks-MIDIs testen.
* **Abnahmekriterien:** Verlustfreier Roundtrip-Test (Lesen -> Schreiben -> Binärvergleich von Events) für Format-0-Dateien.
* **Empfohlener nächster Schritt:** Spezifikation im Anschluss an T-06.

---

### OA-0029: Implementierung der rationalen MIDI-Zeit-Engine & variablen PPQ-Konvertierung (M11)

* **Kategorie:** Infrastruktur / MIDI-Engine · **Status:** `OPEN` · **Ursprung:** EXPLICIT
* **Beschreibung:** Realisierung einer Zeit-Engine basierend auf exakten rationalen Brüchen (Python fractions.Fraction), um MIDI-Dateien beliebiger Division (96 bis 1920 PPQ) verlustfrei und ohne Rundungsjitter in interne STEPS-Ticks zu konvertieren und zu exportieren (Präzisierung 2.3).
* **Quellen & Fundstellen:** MATHEMATICAL_AND_TECHNICAL_REFINEMENTS.md; MMA MIDI 1.0 Spec; Dave Oppenheim SMF 1.0 Spec
* **Betroffene Bereiche:** `src/steps/ports/midi/time.py`, `src/steps/models/`
* **Verbleibende Arbeiten:** Rationale Zeitumrechnungsfunktionen implementieren und mit ungeraden PPQ-Werten (z. B. 384 und 960) testen.
* **Abnahmekriterien:** Bitgenauer Roundtrip-Test von Event-Zeitstempeln bei Konvertierung 960 PPQ -> 480 PPQ -> 960 PPQ.
* **Empfohlener nächster Schritt:** Integration in die Port-Architektur nach T-06.

---

### OA-0030: Implementierung der Shell-Voicing & Guide-Tone-Engine (M04/M10)

* **Kategorie:** Musiktheorie / Algorithmen · **Status:** `OPEN` · **Ursprung:** EXPLICIT
* **Beschreibung:** Entwicklung eines Voicing-Generators für 2-stimmige Shell-Voicings (Terz und Septime in rechter Hand, Grundton in linker Hand) mit automatischer Guide-Tone-Leitung (Halbtonauflösungen 7 -> 3) für Jazz- und Pop-Progressionen (Modul P05).
* **Quellen & Fundstellen:** PIANO_PRACTICE_REFERENCE_LIBRARY.md (Modul P05); Levine: Jazz Theory Book
* **Betroffene Bereiche:** `src/steps/theory/voicings.py`, `src/steps/progression/`
* **Verbleibende Arbeiten:** Python-Generator `generate_shell_voicings(progression)` schreiben und gegen PROG-003 testen.
* **Abnahmekriterien:** Erzeugung ergonomischer 2-stimmiger Shells für Two-Five-One Kadenzen ohne Handsprünge.
* **Empfohlener nächster Schritt:** Modulentwurf im Rahmen von T-06 / M04.

---

### OA-0031: Implementierung des musikalischen Referenz-ID Integritäts-Checkers (Skill / QA)

* **Kategorie:** Qualitätssicherung / Tooling · **Status:** `OPEN` · **Ursprung:** EXPLICIT
* **Beschreibung:** Integration von `ref_id_integrity_check.py` als automatisiertes Validierungstool `scripts/check_reference_ids.py` in den Antigravity Knowledge Curation Skill (`.agents/skills/steps-knowledge-curation/`). Erkennt Änderungen an musikalischen Identitäten (PROG, PAT, P, REF), verifiziert Referenzbeziehungen zwischen Goldentests und Bibliotheken und schlägt bei unzulässigen Ersetzungen oder toten Referenzen mit Exit-Code != 0 fehl (Korrektur und dauerhafte Prävention von ERR-020).
* **Quellen & Fundstellen:** REFERENCE_ID_INTEGRITY_REPORT.md; SKILL_CHANGE_PROPOSAL; ERR-020; Phase 4.6 Master Prompt
* **Betroffene Bereiche:** `.agents/skills/steps-knowledge-curation/scripts/`, `.agents/skills/steps-knowledge-curation/tests/`
* **Verbleibende Arbeiten:** Feature-Branch `feat/skill-reference-id-integrity` anlegen, Prüflogik und Unittests für Id-Invarianten implementieren, PR gegen `main` erstellen.
* **Abnahmekriterien:** Unittest-Suite im Skill verifiziert erfolgreiche Prüfung aller 75 bestehenden Identitäten und meldet Fehler bei gezielten Test-Konflikten.
* **Empfohlener nächster Schritt:** Vorbereitung des Feature-Branch `feat/skill-reference-id-integrity` nach Merge von PR #5.

---

### OA-0032: Implementierung der Cross-Domain Empfehlungs-Engine (Harmonik <-> Drums <-> Piano)

* **Kategorie:** Musiktheorie / Algorithmen · **Status:** `OPEN` · **Ursprung:** EXPLICIT
* **Beschreibung:** Realisierung eines domänenübergreifenden Beziehungs- und Empfehlungsmoduls in `src/steps/progression/recommender.py` basierend auf den relationalen Abbildungen in `MUSIC_CONCEPT_RELATIONS.csv`. Das Modul verknüpft gewählte Akkordprogressionen (z. B. PROG-017) automatisch mit kompatiblen Drum-Patterns (z. B. PAT-013), ergonomischen Klavier-Voicings (z. B. P08 Drop-2) und genretypischen Basslinien-Modellen für die UI- und Kompositions-Shell.
* **Quellen & Fundstellen:** MUSIC_CONCEPT_RELATIONS.csv; INTEGRATED_MUSICAL_CASE_STUDIES.md; Phase 4.7 Master Prompt
* **Betroffene Bereiche:** `src/steps/progression/`, `src/steps/theory/`, `app/ui/`
* **Verbleibende Arbeiten:** Relationales Datenmodell in Python definieren, Empfehlungs-Engine schreiben und gegen die Relationen REL-001 bis REL-013 testen.
* **Abnahmekriterien:** Eingabe einer beliebigen kanonischen PROG-ID liefert validierte Empfehlungs-Vektoren für Drum-Groove und Klavier-Voicing mit dokumentiertem Kompatibilitätsgrad.
* **Empfohlener nächster Schritt:** Modulentwurf im Anschluss an T-06.

---

### OA-0033: SECURITY – Triage & Behebung der Google API Key Alerts (#1–#3)

* **Kategorie:** Sicherheit / Secret Scanning · **Status:** `OWNER_DECISION_REQUIRED` · **Ursprung:** EXPLICIT
* **Beschreibung:** Drei von GitHub Secret Scanning gemeldete Google API Key Public Leaks in `research/STEPS_Bibliothek/` wurden untersucht. Eigentümerschaft ist `THIRD_PARTY_CONFIRMED` (öffentliche YouTube HTML5 Player Client-Keys in heruntergeladenen Ableton-Blog-Webassets aus Commit `a14c3f3`). Kein finanzielles oder sicherheitskritisches Risiko für private Ressourcen des Project Owners. Behebung erfordert Schließen der Alerts in der GitHub UI (Option B) sowie Quarantäne/Löschung der Web-Dumps im aktiven Tree und Einbettung in die Bereinigung P0-1.
* **Quellen & Fundstellen:** SECURITY_PUBLIC_LEAK_INVESTIGATION.md; SECURITY_FINDINGS_REGISTER.csv; SECURITY_REMEDIATION_PLAN.md; SECRET_SCANNING_PREVENTION_PLAN.md; GitHub Alerts #1, #2, #3
* **Betroffene Bereiche:** `research/STEPS_Bibliothek/`, `.gitignore`, `.github/workflows/`
* **Verbleibende Arbeiten:** Owner-Entscheidung: Schließen der Alerts in der GitHub UI als 'Won't fix / Public Third-Party Key' und Freigabe zur Entfernung der Web-Asset-Ordner aus dem Git-Tracking.
* **Abnahmekriterien:** Alle 3 Alerts in GitHub geschlossen; keine neuen unmaskierten Secrets im Repo; `.gitignore` schützt vor zukünftigen Web-Dumps.
* **Empfohlener nächster Schritt:** Owner schließt Alerts #1–#3 in GitHub UI.
