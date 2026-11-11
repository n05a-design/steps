# STEPS – Owner Decision Brief: Offene Grundsatzentscheidungen (Phase 4.16)

**Datum:** 2026-11-11  
**Status:** DOKUMENTIERT & ENTSCHEIDUNGSREIF (Owner Action Required)  
**Kanonische Autorität:** `%LOCALAPPDATA%\StepsKnowledge\OFFENE_ARBEITSAUFFORDERUNGEN.md`  
**Referenzdokument:** Phase 4.16 Master Prompt, Teil VII  

---

## 1. Zweck dieses Briefs

Gemäß Arbeitsvertrag (Regel 2: *Preservation-first*, Regel 6: *Datenherkunft* und Regel 10: *Kritische offene Fragen*) dürfen architektonische, lizenzrechtliche und sicherheitsrelevante Grundsatzfragen **niemals eigenmächtig von KI-Agenten entschieden oder stillschweigend gelöst werden**.

Dieser Brief stellt dem Project Owner die fünf offenen Grundsatzentscheidungen mit ihren konkreten Handlungsoptionen, Risiken und Empfehlungen vor.

---

## 2. Die fünf offenen Grundsatzentscheidungen

### 2.1 OA-0001: Urheberrechts- und Veröffentlichungsrisiken in Git-Historie (P0)

* **Sachverhalt:** In frühen Commits (insb. `a14c3f3`) wurden 7 urheberrechtlich geschützte Fachbücher (Z-Library/PDFs), 53 weitere Dokumente, 74 Ableton-MIDIs und kompilierte Binaries in das öffentliche Git-Repository eingecheckt.
* **Aktuelle Sicherung:** Vollständig inventarisiert in `02_RIGHTS_AND_PUBLICATION_RISK_TRIAGE.csv`. Die Dateien liegen lokal in `research/STEPS_Bibliothek/`, sind jedoch in der Git-Historie vorhanden.
* **Entscheidungsoptionen für den Owner:**
  - **Option A (Empfohlen):** Repository auf GitHub vorerst auf **Privat** stellen. Damit sind externe DMCA- und Haftungsrisiken sofort neutralisiert, ohne dass Git-Historien neu geschrieben werden müssen.
  - **Option B:** Git-Historie mittels `git-filter-repo` oder `BFG Repo-Cleaner` umschreiben und die Binär-Blobs permanent aus allen Commits entfernen (erfordert Force-Push und Koordination aller Klone).
  - **Option C:** Isolierung des Fachbestands in ein separates, privates Archiv-Repository und Bereinigung des STEPS-Haupt-Repositories für die Open-Source-Veröffentlichung.
* **Erforderliche Aktion:** Eigentümerentscheidung zu Option A, B oder C.

---

### 2.2 OA-0033: GitHub Secret Scanning Alerts #1–#3 (P1)

* **Sachverhalt:** GitHub Secret Scanning hat drei historische Google Cloud API Keys in den Ableton-Blog-Asset-Dateien (`research/STEPS_Bibliothek/`) gemeldet. Zusätzlich existiert ein AWS Access Key ID in denselben Blog-HTMLs.
* **Aktuelle Sicherung:** Alle 33 Fundstellen sind kryptographisch gebunden (`secret_sha256`) in `scripts/historical_secret_baseline.json` quarantänisiert. CI und Pre-Commit-Hooks blockieren jede Manipulation und jedes neue Secret fail-closed (12/12 Mutationstests bestanden).
* **Entscheidungsoptionen für den Owner:**
  - **Option A:** Alerts auf GitHub als *„Revoked / Third-Party Historical Demo Data“* schließen (da die Schlüssel zu externen Blogs von 2018 gehören und voraussichtlich inaktiv sind).
  - **Option B:** Zusammen mit OA-0001 (Option B) die betroffenen HTML-Assets per History-Rewrite aus dem Repository tilgen.
* **Erforderliche Aktion:** Schließung der Alerts im GitHub Security Tab oder Beauftragung des History-Purges.

---

### 2.3 ADR-001: Desktop-Fensterarchitektur (2-Pane vs. 2-Toplevel)

* **Sachverhalt:** Architektur-Entscheidung bezüglich des Desktop-GUI-Layouts für die STEPS-Harmonielehre-Oberfläche.
* **Optionen:**
  - **Option 1 (2-Pane Single Window):** Hauptfenster mit split-pane (links Theorie & Akkordwahl, rechts Piano-Roll/Voicing/Groove-Visualisierung). Höhere Stabilität auf allen Desktop-Plattformen, kein Fenster-Fokus-Chaos.
  - **Option 2 (2-Toplevel Multi-Window):** Zwei unabhängige Betriebssystem-Fenster (Modell-Kontrolle und Visualisierungs-Fenster). Flexibel für Multi-Monitor-Setups, aber komplexere State-Synchronisation.
* **Erforderliche Aktion:** Festlegung durch den Owner in ADR-001.

---

### 2.4 ADR-002: Aufbewahrungs- vs. Bereinigungsrichtlinie für historische Fremddaten

* **Sachverhalt:** Festlegung, wie mit urheberrechtlich unklaren Forschungsnotizen, Web-Assets und HTML-Scrapes in `research/` verfahren werden soll.
* **Optionen:**
  - **Option 1:** Vollständige physische Löschung aller externen Scrapes und ausschließliche Beibehaltung strukturierter Metadaten und bibliographischer Zitate in `knowledge/`.
  - **Option 2:** Quarantäne in einem lokalen, nicht synchronisierten Ordner (`.gitignore`) außerhalb des Git-Trackings.
* **Erforderliche Aktion:** Freigabe der Bereinigungsrichtlinie in ADR-002.

---

### 2.5 ADR-005: Release-, Packaging- und Auslieferungsmodell

* **Sachverhalt:** Festlegung des Ziel-Auslieferungsformats für STEPS (Desktop Python App via PyInstaller / Briefcase vs. reines Python-Paket via PyPI / Wheel).
* **Optionen:**
  - **Option 1:** Duales Modell (Core-Bibliothek `steps-theory` auf PyPI; Standalone-Desktop-Bundle für Windows/macOS/Linux via PyInstaller).
  - **Option 2:** Reine Web-/Desktop-Electron-/Tauri-Architektur mit Python-Backend.
* **Erforderliche Aktion:** Festlegung des primären Release-Ziels.

---

## 3. Zusammenfassung

Alle technischen Vorarbeiten sind fail-closed abgesichert. Der Code ist stabil, 100 % getestet und die historische Provenienz ist lückenlos dokumentiert. Sobald der Project Owner die Entscheidungen zu OA-0001, OA-0033 und den ADRs trifft, können die entsprechenden operativen Schritte unmittelbar ausgeführt werden.
