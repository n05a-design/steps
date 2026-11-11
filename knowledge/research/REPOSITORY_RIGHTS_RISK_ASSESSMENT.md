# STEPS – Repository Rights, Copyright Risk & History Assessment (Phase 4.17)

**Datum:** 2026-11-11  
**Status:** FULLY RECONCILED & DECISION-READY (Gate 6 Passed)  
**Autor:** Leitender Compliance Auditor & Knowledge Architect  
**Zugehörige Aufgaben:** `OA-0001`, `OA-0033`, `ADR-010`, `ADR-012`  
**Referenzdokument:** Phase 4.17 Master Prompt, Teil V  

---

## 1. Sachverhalt & Bestandsaufnahme

Im Rahmen des Phase-2A-Audits und der darauffolgenden Sicherheitsanalysen wurden im STEPS-Repository urheberrechtlich geschützte Fremdwerke identifiziert, die in früheren Commits (insbesondere `a14c3f3da4f7a4bc8ebaa75f0ef4de15b625d2cb` vom 10.11.2026) in das Git-Repository eingecheckt wurden.

### 1.1 Betroffene Fremdmaterialien (Inventar aus `02_RIGHTS_AND_PUBLICATION_RISK_TRIAGE.csv`)
1. **7 kommerzielle Musiktheorie-Fachbücher (PDFs):**
   - Volltexte von Verlagen wie Schirmer, W. W. Norton, Sher Music Co., Berklee Press (Aldwell/Schachter, Levine, Mulholland, Kostka/Payne, etc.).
2. **53 weitere Fachdokumente & Auszüge:**
   - PDF-Scans, Papers und Vorlesungsskripte Dritter.
3. **74 Ableton-Groove-MIDIs:**
   - Standard-MIDI-Dateien aus kommerziellen Ableton-Packs.
4. **33 Web-Asset-Dateien (HTML/JS Blog-Scrapes):**
   - Webseiten-Dumps von Ableton-Blogbeiträgen (2018–2020), die verwaiste YouTube-Player-Keys enthalten (Gegenstand von `OA-0033`).

---

## 2. Differenzierung: Aktiver Branch vs. Historische Git-Objekte

Um eine fundierte Entscheidung zu treffen, muss technisch exakt differenziert werden:

| Kategorie | Physischer Speicherort | Risiko im aktuellen Tree | Risiko in der Git-Historie |
|---|---|---|---|
| **Kommerzielle Lehrbücher (7 PDFs)** | `research/STEPS_Bibliothek/` | Liegen im lokalen Dateisystem; sind im aktuellen Commit enthalten | Permanenter Git-Blob in Commit `a14c3f3` |
| **Blog-HTML-Dumps (33 Dateien)** | `research/STEPS_Bibliothek/` | Ausführbare Skripte; enthalten YouTube Client-Keys | Permanenter Git-Blob in Commit `a14c3f3` |
| **Eigene Forschungsartefakte** | `knowledge/`, `docs/`, `src/` | **Kein Risiko:** Eigenständig verfasste Dokumente, Open-Source-Code, bibliographische Zitate (Zitatrecht gem. § 51 UrhG) | Unbedenklich |

---

## 3. Die vier Handlungsoptionen für den Project Owner

### Option A: Vorläufige Zugriffsbegrenzung (Repository auf Privat stellen) – EMPFOHLEN
* **Beschreibung:** Das GitHub-Repository `https://github.com/n05a-design/steps` wird in den Repository-Einstellungen auf **Privat** gestellt.
* **Vorteile:**
  - Sofortige und vollständige Neutralisierung aller externen Urheberrechts- und Haftungsrisiken.
  - Keine Umgehung oder Zerstörung der Git-Historie (kein Rebase, kein Force-Push).
  - Bestehende Forks und Klone bleiben intakt.
  - Alle bisherigen Commits, Tags und Branches bleiben 100 % nachvollziehbar.
* **Nachteile:** Vorübergehend nicht öffentlich einsehbar (bis zur Bereinigung vor dem v0.1 Release).

### Option B: Kontrollierte Entfernung aus künftigen Commits
* **Beschreibung:** Die urheberrechtlich geschützten PDF- und HTML-Dateien werden per `git rm` aus dem aktiven Verzeichnisbaum entfernt und in `.gitignore` aufgenommen.
* **Vorteile:** Der aktuelle Branch ist frei von geschützten Volltexten; keine Fremdbytes im neuesten Commit.
* **Nachteile:** Die historischen Blobs verbleiben in vergangenen Commits (`a14c3f3`). Bei einem öffentlichen Repo können diese über alte Commit-SHAs weiterhin abgerufen werden.

### Option C: Gezielte Bereinigung der Git-Historie (BFG Repo-Cleaner / git-filter-repo)
* **Beschreibung:** Vollständiges Umschreiben der Git-Historie, bei dem alle PDF- und HTML-Dateien aus allen Commits getilgt werden.
* **Vorteile:** Permanentes Verschwinden aller Fremd-Blobs aus der gesamten Git-Datenbank.
* **Nachteile:**
  - Erfordert einen destruktiven Force-Push (`git push --force`).
  - Verändert alle Commit-SHAs im Repository; zerstört die Referenzierbarkeit früherer Auditberichte.
  - Alle existierenden Klone und Forks werden ungültig und müssen neu geklont werden.

### Option D: Separate rechtmäßige Quellenverwaltung (Dual-Repository / Local Archive)
* **Beschreibung:** Auslagerung aller schutzwürdigen Recherche-Volltexte in ein privates, lokales Archiv-Verzeichnis außerhalb des Git-Trackings. Im STEPS-Repository verbleiben ausschließlich strukturierte Metadaten, Zitate und wissenschaftliche Belege.
* **Vorteile:** Langfristig saubere Open-Source-Architektur; strikte Einhaltung von Regel 6 (*Datenherkunft*).

---

## 4. Strikte Owner-Grenze (Rule 2 & Rule 6)

Gemäß Arbeitsvertrag und ethischen Leitlinien gilt:
- **Keine automatische Privatisierung durch KI-Agenten.**
- **Kein eigenmächtiger Force-Push und kein History-Rewrite.**
- **Keine stillschweigende Löschung historischer Forschungsunterlagen.**

Die Entscheidung über die Wahl von Option A, B, C oder D verbleibt verbindlich beim **Project Owner**.
