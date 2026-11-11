# STEPS – ADR Owner Decision Brief: Ratifikationsvorlagen (Phase 4.17)

**Datum:** 2026-11-11  
**Status:** ENTSCHEIDUNGSREIF (Wartet auf Beschluss des Project Owners)  
**Kanonische Quelle:** `decisions/DECISION_REGISTER.md`  
**Referenzdokument:** Phase 4.17 Master Prompt, Teil I & VII  

---

## 1. Übersicht der entscheidungsreifen Architekturvorlagen

Die folgenden zentralen Architekturentscheidungen (ADRs) sind fertig ausgearbeitet, historisch konsolidiert und gegen unzulässige Umwidmung gelockt. Sie bedürfen der formellen Zeichnung durch den Project Owner.

---

### 2. Die fünf Kernentscheidungen im Detail

### 2.1 ADR-001: Desktop-Fensterarchitektur (1 Root / 2 Panes vs. 2 Toplevel)
* **Zugehörige Aufgabe:** `OA-0003`
* **Fragestellung:** Wie soll die grafische Benutzeroberfläche von STEPS v0.1 modularisiert werden?
* **Option A (Empfohlen):** Ein Hauptfenster (Root) mit zwei vertikalen Panes (links Harmonik- und Progressionskontrolle; rechts Noten-, Voicing- und Groove-Visualisierung).
  - *Vorteile:* Höchste plattformübergreifende Stabilität (Windows, macOS, Linux); keine Fokus-Verluste; einfachere State-Synchronisation.
  - *Nachteile:* Feste Bildschirmaufteilung, geringere Flexibilität auf Multi-Monitor-Setups.
* **Option B:** Zwei unabhängige OS-Fenster (Toplevel).
  - *Vorteile:* Frei auf mehreren Monitoren verschiebbar.
  - *Nachteile:* Hohe Komplexität beim Window-Management; Fokus-Probleme unter Tkinter.
* **Empfohlene Entscheidung:** Option A annehmen (`ACCEPTED`).

---

### 2.2 ADR-002: MVP-Umfang & Phasen-Splitting (Harmonik v0.1 vs. Drums v0.2+)
* **Zugehörige Aufgaben:** `OA-0004`, `OA-0012`
* **Fragestellung:** Welcher Funktionsumfang bildet das Minimum Viable Product (v0.1) von STEPS?
* **Option A (Empfohlen):** Strikte Fokussierung von v0.1 auf die **reine, testbare Harmonielehre** (Tonklassen, Intervalle, Dreiklänge, Vierklänge, Kadenzen, Stimmführung). Schlagzeug-Muster (Drums) und erweiterte Rhythmus-Engines werden für v0.1 zurückgestellt und in v0.2+ implementiert.
  - *Vorteile:* Scharfe Domänengrenze; minimierte Angriffsfläche für Regressionen; schnelle Kernabnahme.
  - *Nachteile:* Eingeschränkte Cross-Domain Visualisierung im allerersten Release.
* **Option B:** Gleichzeitige Realisierung von Harmonik und vollständiger Drum-Engine in v0.1.
  - *Nachteile:* Verdopplung der Entwicklungs- und Testkomplexität vor dem ersten Release.
* **Empfohlene Entscheidung:** Option A annehmen (`ACCEPTED`).

---

### 2.3 ADR-005: Fachmodell Harmonielehre (Pitch-Class vs. Spelling & Enharmonik)
* **Zugehörige Aufgabe:** `OA-0005`
* **Fragestellung:** Wie werden Notennamen, deutsches H/B vs. internationales B/Bb und Enharmonik modelliert?
* **Option A (Empfohlen):** Strikte Trennung von **mathematischer Tonklasse** ($p \in \mathbb{Z}_{12}$, z. B. $10$) und **notationaler Rechtschreibung** (Spelling-Objekt, z. B. `Bb` vs. `A#`). Explizite Sprachraum-Projektion: Deutsches H/B wird nur in der Präsentationsschicht/UI gerendert; das interne Kernmodell nutzt standardisierte semantische Bezeichner.
  - *Vorteile:* Eindeutige Modulo-12 Berechnungen ohne enharmonische Mehrdeutigkeiten; exakte musiktheoretische Korrektheit im Kontrapunkt.
  - *Nachteile:* Leicht höherer Modellierungsaufwand als bei einfachen Integer-MIDI-Zahlen.
* **Empfohlene Entscheidung:** Option A annehmen (`ACCEPTED`).

---

### 2.4 ADR-011: Release-Packaging- und Auslieferungsmodell (PyInstaller vs. Wheel)
* **Zugehörige Aufgabe:** `OA-0013`
* **Fragestellung:** In welcher Form soll STEPS an Endanwender und Entwickler ausgeliefert werden?
* **Option A (Empfohlen):** Duales Modell:
  1. `steps-theory` als reines, headless Python-Paket (Wheel) auf PyPI (ohne GUI-Abhängigkeiten).
  2. `STEPS Desktop` als eigenständiges Standalone-Bundle via PyInstaller für Endanwender.
* **Empfohlene Entscheidung:** Option A annehmen (`ACCEPTED`).

---

### 2.5 ADR-012: Aufbewahrungs- und Bereinigungsrichtlinie für Web- & MIDI-Dateien
* **Zugehörige Aufgaben:** `OA-0001`, `OA-0033`
* **Fragestellung:** Wie wird mit den historischen Drittanbieter-Dateien in `research/STEPS_Bibliothek/` umgegangen?
* **Option A (Vorläufige Begrenzung):** Repository auf GitHub auf **Privat** stellen. Keine Historienbereinigung notwendig.
* **Option B (Aktive Bereinigung):** Dateien aus dem aktuellen Tree entfernen; Historie unverändert lassen.
* **Option C (Vollständiger Purge):** Bereinigung via `BFG Repo-Cleaner` mit anschließendem Force-Push.
* **Empfohlene Entscheidung:** Option A sofort ausführen; Option C bei geplanter Open-Source-Veröffentlichung.
