# STEPS – Ganzheitliche kontextbasierte Master-Übergabe für den nächsten KI-Agenten

- **Stand:** 16.11.2026 (Europe/Berlin)
- **Projekt:** STEPS (Desktop-Musik-App für Harmonielehre, Voicings, Progressionen und Rhythmus)
- **Remote-Repository:** `https://github.com/n05a-design/steps`
- **Geprüfter Ausgangsstand (`origin/main`):** Commit `d717cec` (nach Merge von PR #110); die erste Fassung dieses Dokuments bezog sich auf `93e8b5c` (PR #107)
- **Status:** Konsolidierter Master-Übergabestand nach PR #88–#110. Lokale Gates am 16.11.2026 auf `d717cec` nachgeprüft (Abschnitt 3.8 und 4); fachliche Menschabnahme weiterhin `AUSSTEHEND`.

---

## 1. Projektidentität, Leitbild und Domänengrenzen

### 1.1 Was ist STEPS?
STEPS ist eine eigenständige Musik-Desktop-Anwendung, die Musiker, Produzenten und Komponisten bei Harmonielehre, Voicing-Bildung, Akkordprogressionen und rhythmischer Fundierung unterstützt.

Es existieren drei strikt getrennte Projektachsen, die niemals miteinander vermengt werden dürfen:
1. **Produktachse (App-Code, Phase 5 MVP v0.1):**
   - `src/steps/`: Reiner, vollkommen UI-unabhängiger Python-Kern für Harmonielehre, Notenlogik, Enharmonik, Voicings und Takt/PPQ-Modelle.
   - `app/`: Ausschließlich Desktop-Start, Tkinter-UI-Shell (abgeleitet aus der bewährten Systemarchitektur von `glide-to-do`, jedoch ohne Todo-Fachlogik), Widgets und Controller.
   - *Wichtig (Rule 3 in `AGENTS.md`):* Die Versionsbezeichnung `V6.6 / V6.7` bezieht sich ausschließlich auf die historische Ableton-Blog-Forschungsbibliothek, **nicht** auf die App-Version! Die Paketversion des Kerns steht in [`src/steps/__init__.py`](../../src/steps/__init__.py) und lautet `0.0.0.dev0` (PEP 440); ein installierbares Build-System ist laut `pyproject.toml` noch nicht verifiziert.
2. **Forschungsachse (`knowledge/`, `research/`):**
   - Strukturierte Daten, Schemata, kanonische Progressions- und Rhythmikkataloge (`PROG-001..028`, `PAT-001..031`, `P01..P19`), Wissensgraphen und musikwissenschaftliche Belege mit strikter Provenienz.
3. **Archivachse (`archive/`, `source_archive/`):**
   - Historische Übergaben, alte Skripte und Dokumentationsstände aus früheren Projektphasen.

### 1.2 Musiktheoretische Grundprinzipien für STEPS
- **Tonbezeichnungen:** Deutsche Notation (H = B♮, B = B♭) und internationale Notation (B = B♮, B♭ = B♭) müssen an jeder Schnittstelle und im UI explizit und verwechslungsfrei geführt werden.
- **Enharmonik:** C♯ und D♭ sind musikalisch und funktional fundamental verschieden. Keine vorzeitige Einebnung auf Piano-Roll-Midi-Pitches (widerspricht dem didaktischen Kern von STEPS).
- **Funktionale Mehrdeutigkeit:** Verminderte Septakkorde, Medianten und Alterationen besitzen mehrere Deutungen je nach tonalem Zentrum (z. B. nach Schönberg, Hindemith, Aldwell/Schachter). Diese Mehrdeutigkeit muss im Datenmodell abbildbar bleiben.

---

## 2. Arbeitsvertrag und Governance für KI-Agenten (`AGENTS.md`)

Für alle Agenten (Codex, Claude, Gemini, Antigravity, ChatGPT) gelten ausnahmslos folgende verbindliche Regeln:
1. **Erst inventarisieren, dann verändern:** `main`-SHA, `git status`, Quelle, Lizenz, Dateihashes vor jeder Änderung prüfen.
2. **Preservation-first:** Keine stillschweigenden Löschungen, kein Force-Push, kein Rewrite der Historie, keine automatische Beseitigung historischer Versionen.
3. **Verifikation vor Behauptung:** `fachliche_freigabe` und `human_review` bleiben stets `false` bzw. `AUSSTEHEND`, solange kein Mensch die Freigabe erteilt hat. Keine erfundenen Testergebnisse oder APIs.
4. **Strikte Domänengrenzen:** `src/steps/` (reine Logik) $\neq$ `app/` (UI) $\neq$ `knowledge/` (Fakten mit Provenienz).
5. **Datenherkunft und Urheberrecht:** Keine Volltexte oder Seitenbilder urheberrechtlich geschützter Werke (Rechteklasse E) ins Git committen. Klasse E verbleibt als `restricted_local` ausschließlich auf der lokalen Festplatte.
6. **PR-Workflow und Ruleset 26983173:**
   - **Niemals direkt auf `main` pushen.**
   - Wegen des GitHub Rulesets `26983173` ("basic") schlagen Pushes auf bestehende Remote-Branches mit `GH013: Changes must be made through a pull request` fehl. Jeder PR muss daher auf einem **frischen, neuen Branch-Namen** mit genau einem vollständigen Commit angelegt und via `gh pr create` eingereicht werden.
7. **OneDrive-Worktree-Besonderheit:**
   - Das Hauptcheckout liegt unter OneDrive (`~/Library/CloudStorage/OneDrive-Persönlich/Github/steps`); Agenten arbeiten in eigenen Worktrees (z. B. `.claude/worktrees/<name>`). Der Worktree `fix_onedrive_git_index` liegt außerhalb von OneDrive unter `~/.gemini/antigravity/worktrees/steps/`. Maschinenpfade gehören nicht in versionierte Dokumente – Verweise immer relativ setzen.
   - OneDrive neigt dazu, die Index-Datei eines Worktrees (`.git/worktrees/<name>/index`) bei Schreibkollisionen in `index 2` oder `index (<Datum>)` umzubenennen. Git meldet dann plötzlich alle 2.900+ Dateien als "gelöscht".
   - **Lösung:** Den Index sofort mit `git reset -q HEAD` (niemals `--hard`) wiederherstellen. Die Dateien auf der Platte bleiben dabei 100% unberührt. Die von OneDrive erzeugten Konfliktkopien im `.git`-Verzeichnis nicht löschen.

---

## 3. Konsolidierte Audit-Befunde (PR #88 – #107)

In den zurückliegenden Arbeitssitzungen wurden sämtliche historischen Unklarheiten und offenen Lücken systematisch aufgearbeitet:

### 3.1 Historische Bibliotheksstruktur V6.6 / V6.7
- **Vier Strukturmodelle geklärt:** In [`docs/audit/BIBLIOTHEK_V6_6_V6_7_STRUKTUR_UND_ZAEHLMODELLE_2026-11-16.md`](../../docs/audit/BIBLIOTHEK_V6_6_V6_7_STRUKTUR_UND_ZAEHLMODELLE_2026-11-16.md) wurden die 4 Modelle (`V1/V3/V4`, `V5.0–V5.4`, `V6.0–V6.6` und `V6.7-Delta`) aufgeschlüsselt.
- **Exakte Zählkette:** Der historische Zuwachs von V5.0 (260 Dateien) bis V6.6 (1.145 Manifestdateien) wurde rechnerisch bewiesen ($1.145 - 148\text{ fehlend} + 3\text{ nicht gelistet} = 1.000\text{ versionierte Dateien im Repo}$).
- **148 fehlende Dateien zugeordnet:** In [`docs/audit/BIBLIOTHEK_V6_6_FEHLENDE_DATEIEN_2026-11-16.csv`](../../docs/audit/BIBLIOTHEK_V6_6_FEHLENDE_DATEIEN_2026-11-16.csv) und [`docs/audit/INDIZES_JSON_TXT_NACHPRUEFUNG_2026-11-16.md`](../../docs/audit/INDIZES_JSON_TXT_NACHPRUEFUNG_2026-11-16.md) wurde jede der 148 fehlenden Dateien ihrem Ursprungs-ZIP/RAR-Paket zugeordnet (34 V6.0, 29 V6.3, 62 V6.4, 10 V6.5, 13 V6.6).
- **Fachordner 21 und 39:** Die historische Doppelvergabe der Ordnernummern 21 und 39 weist keinerlei Datei- oder Inhaltsüberschneidung auf.

### 3.2 Statische Generator-Sicherheitsanalyse
- In [`docs/audit/GENERATOREN_SEITENEFFEKTE_2026-11-16.md`](../../docs/audit/GENERATOREN_SEITENEFFEKTE_2026-11-16.md) wurden 17 Skripte per Python-AST ohne Ausführung untersucht:
  - Kein Skript löscht oder verschiebt Dateien oder startet Fremdprozesse.
  - Nur der Ableton-Blog-Indexer besitzt Netzzugriff (beachtet `robots.txt`).
  - V6.7-Generatoren schreiben ZIP-Archive ins CWD und überschreiben gleichnamige Dateien.
  - `Ordnerliste.py` ist PowerShell-Code, kein Python.

### 3.3 Schutzfristen, Zusammenfassungen & Rechteklasse E
- 10 Werke der Rechteklasse E liegen nur lokal als `restricted_local` vor (`manifests/restricted_local_2026-11-14.csv`).
- Die 10 versionierten Zusammenfassungen in `research/STEPS_Bibliothek/Zusammenfassungen/` wurden gegen die Extrakte geprüft. Strukturnahe Abschnitte bei Aldwell/Schachter (TOC-Unterpunkte) und Stuart (Musterkatalog) wurden per Inhaberentscheidung gekürzt (PR #89).
- Nicht belegbare Gemeinfreiheits- und Schutzfristbehauptungen zu Hindemith und Schönberg wurden aus den Zusammenfassungen gestrichen. Die Z-Library-Herkunft von Müller ist transparent dokumentiert.

### 3.4 Swift-Rendering & Claim-Fundstellen an Original-Büchern
- Mittels `render_pdf.swift` wurden hochauflösende PNGs der Original-PDF-Seiten im Scratch-Verzeichnis gerendert und alle 9 Buchclaims (`CLAIM-002`, `007`, `014`, `026`, `027`, `029`, `031`, `035`, `041`) an den Originalseiten verifiziert ([`CLAIM_BUCHFUNDSTELLEN_2026-11-16.md`](../../docs/audit/fable-5.2/CLAIM_BUCHFUNDSTELLEN_2026-11-16.md)).
- Der Abnahmebogen für Fable 5.2 wurde um die Prüfpunkte B6–B9 erweitert ([`ABNAHMEBOGEN_2026-11-16.md`](../../docs/audit/fable-5.2/ABNAHMEBOGEN_2026-11-16.md)).

### 3.5 Quellenmetadaten W01–W03 und CLAIM-033
- In [`docs/audit/fable-5.2/QUELLENMETADATEN_UND_CLAIMS_W01_W03_2026-11-16.md`](../../docs/audit/fable-5.2/QUELLENMETADATEN_UND_CLAIMS_W01_W03_2026-11-16.md) wurden alle 5 Duplikatpaare in `curated_sources_registry.yaml` aufgelöst, alle 30 PDFs der Klassen A–D bibliografiert (inkl. CC-BY-Nachweis für Catherine Schmidt-Jones) und `CLAIM-033` (Linn MPC 96 PPQ vs. STEPS 480 PPQ) klargestellt.

### 3.6 HTML-Extrakte & OCR-Neuläufe
- In [`docs/audit/HTML_EXTRAKTE_UND_OCR_NACHPRUEFUNG_2026-11-16.md`](../../docs/audit/HTML_EXTRAKTE_UND_OCR_NACHPRUEFUNG_2026-11-16.md) wurden alle 18 eindeutigen HTML-Extrakte geprüft.
- `The Chord Wheel.html` wurde als SEO-/KI-Text mit halluzinierter Geschichte (*„Klaus Vogel 1997“*) identifiziert und für wissenschaftliche Zwecke gesperrt.
- Die OCR-Neuläufe `Music_Theory_Advanced_Level.md` und `Understanding_Basic_Music_Theory.md` (CC BY 2.0) wurden im Detail analysiert.

### 3.7 Katalog-Stichprobenprüfung W04
- In [`docs/audit/fable-5.2/KATALOG_STICHTEST_W04_2026-11-16.md`](../../docs/audit/fable-5.2/KATALOG_STICHTEST_W04_2026-11-16.md) wurden alle 19 Klaviermodule (`P01–P19`), 31 Drum-Patterns (`PAT-001–031`), 28 Akkordprogressions-Archetypen (`PROG-001–028`) und der [Latin-Katalog](../../knowledge/concepts/styles/GENRE_RESEARCH_LATIN.md) vollständig auditiert.
- 480-PPQ-Zeitachse, GM-Kanal-10-Mappings, Alla-breve-Dauern (Samba-Batucada) und Stimmführungen ($L_1$-Distanz) sind 100% verifiziert; 10 P, 5 PAT und 11 PROG werden aktiv im Benchmark getestet. Reale Spiel- und Hörabnahmen bleiben als `AUSSTEHEND` gekennzeichnet.

### 3.8 Skript-Exitcodes (PR #110) und Nachprüfung dieser Übergabe
- PR #110 machte die Graph-Probes ohne `PYTHONPATH` lauffähig, ergänzte in `scripts/verify_pilot_review_evidence.py` einen macOS-Zertifikats-Fallback und ersetzte in `scripts/execute_project_consolidation.py` den festen Aufruf `python` durch `sys.executable`.
- Nachprüfung am 16.11.2026 auf `d717cec` (macOS, Python 3.14.5), Exitcode jeweils 0: `verify_reference_integrity.py`, `audit_knowledge_coverage.py --check`, `graph_probes.py`, `graph_followup_probes.py`, `graph_semantic_probes.py`, `verify_historical_ontology.py`, `pre-commit-secret-check.py`, `verify_pilot_review_evidence.py` (8 Freigaben), `unittest discover tests` (402 Tests), Curation-Skill-Tests (36 Tests), `knowledge/research/run_golden_test_suite.py`.
- **Linkprüfung neu gezählt:** 1.534 versionierte Markdown-Dateien. In `docs/`, `knowledge/` und `research/gaps/` 0 defekte relative Links. Defekte relative Links bestehen nur im historischen Bestand (`source_archive/` 543, `archive/` 172, `research/` außerhalb `gaps/` 83) und bleiben nach Preservation-first unverändert.
- **Korrigiert:** Diese Übergabe enthielt 11 absolute `file:///Users/…/.gemini/…`-Links, die nur auf einer Maschine auflösten und vom bisherigen Linkcheck nicht erfasst wurden. Sie sind jetzt relativ.
- **Bekannte Nebenwirkung:** `run_golden_test_suite.py` überschreibt bei jedem Lauf fünf versionierte Dateien unter `knowledge/research/` (`FINAL_REFERENCE_CASE_VALIDATION.csv`, `GOLDEN_TEST_CLASSIFICATION_AUDIT.csv`, `MUSICAL_REFERENCE_VALIDATION.csv`, `GOLDEN_TEST_EXECUTION_REPORT.md`, `REAL_GOLDEN_TEST_EXECUTION_REPORT.md`) mit Zeitstempel, Laufzeiten, Plattform, Commit und CRLF→LF. Fachlich ändert sich nichts. Nach dem Lauf mit `git restore knowledge/research/` zurücksetzen und nicht versehentlich committen.

---

## 4. Testarchitektur und Qualitätsgates

**Lokale Einrichtung:** `python3 -m pip install -r knowledge/benchmark/requirements.txt` (PyYAML 6.0.3, nur für Audit-Skripte; der Kern hat keine Laufzeitabhängigkeit).

Bevor ein PR eingereicht wird, müssen folgende Tests lokal fehlerfrei durchlaufen:
1. **Referenzintegrität:**
   ```bash
   python3 scripts/verify_reference_integrity.py
   ```
   *Soll:* 100% CANONICAL REFERENCE & SCHEMA INTEGRITY VERIFIED (Exitcode 0).
2. **Restricted Local Check:**
   ```bash
   python3 -m unittest tests/test_restricted_local.py
   ```
   *Soll:* OK (keine Klasse-E-Volltexte im Git).
3. **Knowledge Coverage CI-Gate (`scripts/audit_knowledge_coverage.py --check`):**
   - **Kritischer Hinweis:** GitHub Actions vergleicht `knowledge/benchmark/COVERAGE.csv` bitgenau mit der Anzahl der getrackten Dateien unter `research/`, `archive/`, `source_archive/`, `knowledge/legacy/` und `knowledge/research/`.
   - **Regel:** Niemals neue Dateien in diese 5 Ordner legen, ohne `COVERAGE.csv` nachzuziehen! Alle neuen Berichte und Dokumentationen gehören nach `docs/audit/` oder `docs/audit/fable-5.2/`!

---

## 5. Konkreter Fahrplan für den nächsten Agenten

Der nächste Agent soll nahtlos an folgenden konkreten Punkten anknüpfen:

### Arbeitspaket 1: Begleitung der Fable-5.2-Menschabnahme
- Der [`ABNAHMEBOGEN_2026-11-16.md`](../../docs/audit/fable-5.2/ABNAHMEBOGEN_2026-11-16.md) enthält die Teile A (Graph-Inhaberentscheidungen) und B (Auditproben B1–B9). Sobald der menschliche Reviewer Punkte abzeichnet, Status in der Matrix nachführen.

### Arbeitspaket 2: Ausbau der Core-Implementierung (Phase 5 MVP v0.1)
- **Nicht bei null beginnen:** `src/steps/theory/` (`pitch`, `interval`, `chord`, `triad`, `seventh`, `exceptions`) und `src/steps/progression/` (`engine`, `voice_leading`, `reviewed` samt Bestands- und Freigabe-JSON) existieren bereits mit rund 2.600 Zeilen. `models/` und `ports/` sind nur Paketorte, `app/` umfasst rund 80 Zeilen Python. Verträge und API: [`docs/theory/API_VERTRAEGE.md`](../theory/API_VERTRAEGE.md), [`docs/theory/API.md`](../theory/API.md); Tests u. a. `tests/test_theory_core.py`, `tests/test_progression_engine.py`, `tests/test_voicing_contract.py`, `tests/test_notation_contract.py`.
- Vor neuem Code die vorhandenen Verträge lesen und gegen [`research/gaps/OPEN_GAPS.md`](../../research/gaps/OPEN_GAPS.md) (Abschnitt „Fachprüfung des Progressionskerns“) abgleichen. Offene Ausbaupunkte:
  - Intervall-, Akkord- und Skalen-Parser (mit strikter Unterscheidung von H/B und B/B♭).
  - Modus- und Syntax-Engine (unter Berücksichtigung von Aldwell/Schachter, Hindemith und Schönberg).
  - Anbindung der UI-Shell in `app/` ohne Vermischung mit der Fachdomäne.
