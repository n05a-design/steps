# STEPS – Owner Decision Brief: Offene Grundsatzentscheidungen (Phase 4.17)

**Datum:** 2026-11-11  
**Status:** DOKUMENTIERT & ENTSCHEIDUNGSREIF (Owner Action Required)  
**Kanonische Autorität:** `%LOCALAPPDATA%\StepsKnowledge\OFFENE_ARBEITSAUFFORDERUNGEN.md`  
**Referenzdokument:** Phase 4.17 Master Prompt, Teil I & VII  

---

## 1. Zweck dieses Briefs

Gemäß Arbeitsvertrag (Regel 2: *Preservation-first*, Regel 3: *Verifikation*, Regel 6: *Datenherkunft* und Regel 10: *Kritische offene Fragen*) dürfen architektonische, lizenzrechtliche und sicherheitsrelevante Grundsatzfragen **niemals eigenmächtig von KI-Agenten entschieden oder stillschweigend gelöst werden**.

In Phase 4.17 wurden alle historischen Architekturentscheidungen (ADRs) auf ihre ursprünglichen Identitäten zurückgeführt (siehe `ADR_HISTORICAL_IDENTITY_MATRIX.csv` und `ADR_IDENTITY_LOCK_REPORT.md`). 

Dieser Brief stellt dem Project Owner die entscheidungsreifen Vorlagen mit konkreten Handlungsoptionen, Risiken und Empfehlungen vor.

---

## 2. Die entscheidungsreifen Grundsatzfragen

### 2.1 OA-0001: Urheberrechts- und Veröffentlichungsrisiken in Git-Historie (P0)
* **Sachverhalt:** In frühen Commits (insb. `a14c3f3`) wurden 7 kommerzielle Musiktheorie-Fachbücher (PDFs), 53 weitere Dokumente, 74 Ableton-MIDIs und 33 Web-Dumps in das öffentliche Git-Repository eingecheckt.
* **Aktuelle Sicherung:** Vollständig inventarisiert in `02_RIGHTS_AND_PUBLICATION_RISK_TRIAGE.csv` und `REPOSITORY_RIGHTS_RISK_ASSESSMENT.md`.
* **Entscheidungsoptionen für den Owner:**
  - **Option A (Empfohlen):** Repository auf GitHub auf **Privat** stellen. Neutralisiert externe Haftungs- und DMCA-Risiken sofort, ohne Historie oder Klone zu beschädigen.
  - **Option B:** Kontrollierte Entfernung aus künftigen Commits (`git rm`), Historie bleibt vorerst bestehen.
  - **Option C:** Gezieltes Umschreiben der Git-Historie via `BFG Repo-Cleaner` mit Force-Push (erfordert Neuklonen aller Klone).
* **Erforderliche Aktion:** Eigentümerentscheidung zu Option A, B oder C.

---

### 2.2 OA-0033: GitHub Secret Scanning Alerts #1–#3 (P1)
* **Sachverhalt:** GitHub Secret Scanning hat drei Google API Keys in veralteten Ableton-Blog-Asset-Dateien (`research/STEPS_Bibliothek/`) gemeldet. Zusätzlich existiert ein statischer AWS-Client-Key in denselben Blog-HTMLs.
* **Aktuelle Sicherung:** Alle 33 Fundstellen (4 eindeutige Tokens) sind kryptographisch gebunden (`secret_sha256`) in `scripts/historical_secret_baseline.json` quarantänisiert. CI und Pre-Commit-Hooks blockieren jede Manipulation fail-closed (15/15 Mutationstests bestanden).
* **Entscheidungsoptionen für den Owner:**
  - **Option A (Empfohlen):** Alerts im GitHub Security Tab als *„Won't fix / Public Third-Party Key“* schließen (da Schlüssel zu externen Blogs von 2018 gehören und YouTube-Player-Demos sind).
  - **Option B:** Zusammen mit OA-0001 (Option C) per History-Rewrite tilgen.
* **Erforderliche Aktion:** Schließung der Alerts im GitHub Security Tab.

---

### 2.3 ADR-001: Desktop-Fensterarchitektur (1 Root / 2 Panes vs. 2 Toplevel)
* **Zugehörige Aufgabe:** `OA-0003`
* **Fragestellung:** Wie soll die Benutzeroberfläche von STEPS modularisiert werden?
* **Option A (Empfohlen):** Ein Hauptfenster (Root) mit zwei vertikalen Panes (links Theorie/Progression, rechts Visualisierung).
* **Option B:** Zwei getrennte OS-Toplevel-Fenster.
* **Erforderliche Aktion:** Formelle Annahme von Option A in `decisions/DECISION_REGISTER.md`.

---

### 2.4 ADR-002: MVP-Umfang & Phasen-Splitting (Harmonik v0.1 vs. Drums v0.2+)
* **Zugehörige Aufgaben:** `OA-0004`, `OA-0012`
* **Fragestellung:** Welcher Funktionsumfang bildet das Minimum Viable Product (v0.1) von STEPS?
* **Option A (Empfohlen):** Reiner Fokus von v0.1 auf den testbaren Harmonielehre-Kern in `src/steps/theory/`. Drums und Rhythmus-Engines werden für v0.1 zurückgestellt und in v0.2+ implementiert.
* **Option B:** Parallele Entwicklung von Harmonik und Drums vor dem ersten Release.
* **Erforderliche Aktion:** Formelle Annahme von Option A in `decisions/DECISION_REGISTER.md`.

---

### 2.5 ADR-005: Fachmodell Harmonielehre (Pitch-Class vs. Spelling & Enharmonik)
* **Zugehörige Aufgabe:** `OA-0005`
* **Fragestellung:** Wie werden Tonhöhen, deutsches H/B vs. internationales B/Bb und Enharmonik modelliert?
* **Option A (Empfohlen):** Strikte mathematische Trennung von Modulo-12 Tonklasse ($p \in \mathbb{Z}_{12}$) und notationaler Rechtschreibung (Spelling-Objekt). Sprachraum-Projektion (deutsches H/B) nur in der Darstellungsschicht; interner Kern nutzt eindeutige Indizes.
* **Option B:** Reine Verwendung von Fließkomma-/Integer-MIDI-Noten ohne syntaktische Enharmonik.
* **Erforderliche Aktion:** Formelle Annahme von Option A in `decisions/DECISION_REGISTER.md`.

---

### 2.6 ADR-011: Release-Packaging- und Auslieferungsmodell (PyPI vs. Standalone)
* **Zugehörige Aufgabe:** `OA-0013`
* **Fragestellung:** Wie wird STEPS verpackt und verteilt?
* **Option A (Empfohlen):** Duales Modell: Headless-Kern auf PyPI als Wheel; Desktop-App als Standalone-Bundle via PyInstaller.
* **Option B:** Reine Quellcode-Auslieferung via Git.
* **Erforderliche Aktion:** Kenntnisnahme und Bestätigung von ADR-011.

---

### 2.7 ADR-012: Aufbewahrungs- und Bereinigungsrichtlinie für Web/MIDI-Dateien
* **Zugehörige Aufgaben:** `OA-0001`, `OA-0033`
* **Fragestellung:** Wie verfahren wir dauerhaft mit den Drittanbieter-Dateien in `research/STEPS_Bibliothek/`?
* **Option A:** Vollständige physische Löschung aus dem Arbeitsbaum und Aufnahme in `.gitignore`.
* **Option B:** Quarantäne in einem lokalen, nicht getrackten Ordner außerhalb des Repositories.
* **Erforderliche Aktion:** Freigabe der Bereinigungsstrategie.
