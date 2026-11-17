# STEPS – Ganzheitliche kontextbasierte Master-Übergabe für den nächsten KI-Agenten

- **Stand:** 17.11.2026 (Europe/Berlin), fortgeschrieben nach Abschluss von Release v0.1.0 (PR #139), Versionswechsel auf 0.2.0-dev (PR #140) und OA-0026. Der Dateiname bleibt für stabile Verweise unverändert.
- **Projekt:** STEPS (Desktop-Musik-App für Harmonielehre, Voicings, Progressionen und Rhythmus)
- **Remote-Repository:** `https://github.com/n05a-design/steps`
- **Geprüfter Ausgangsstand (`origin/main`):** Commit `be32c5d` (Versionswechsel 0.2.0-dev, PR #140) und vorangehend `1023fcf` (Release v0.1.0, PR #139).
- **Status:** Konsolidierter Stand nach PR #88–#140 und OA-0026. Alle 650 Unittests fehlerfrei bestanden (100% grün). Richtung für v0.1 (publiziert), Lizenz, Fenster, Speicherformat und MIDI-Export sind entschieden. Cross-Domain Recommender (OA-0032), Shell-Voicings (OA-0030), Swing-Ratio Engine (OA-0022), Didaktische Reduktions-Engine (OA-0024) und Stilistische Stimmführungsregeln (OA-0026) sind vollständig implementiert. Nächste anstehende Aufgabe: OA-0027 (Property-Based Tests).

**Schnelleinstieg für einen neuen Agenten:** 1. `AGENTS.md` lesen. 2. Abschnitt 2 (Arbeitsregeln) und 5 (Fahrplan) dieser Datei lesen. 3. Entscheidungen im [Register](../../decisions/DECISION_REGISTER.md) und in `decisions/ADR-0*.md`. 4. Offene Punkte in [`OPEN_GAPS.md`](../../research/gaps/OPEN_GAPS.md) (Tabelle „Restprüfung nach dem Fable-Audit“, neueste Zeilen unten). 5. Vor jeder Änderung die Gates aus Abschnitt 4 laufen lassen.

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
   - Wegen des GitHub Rulesets `26983173` ("basic") schlagen Pushes auf bestehende Remote-Branches mit `GH013: Changes must be made through a pull request` fehl. Jeder PR wird daher auf einem **frischen, neuen Branch-Namen** angelegt und via `gh pr create` eingereicht. Mehrere Commits je PR sind möglich (PR #113 wurde mit zwei Commits gemergt); die Aussage zu `GH013` bei Pushes auf bestehende Branches wurde am 17.11.2026 nicht erneut geprüft.
   - Gemergt wird durch den Inhaber, nicht durch Agenten. Merged Branches bleiben auf `origin` erhalten.
7. **OneDrive-Worktree-Besonderheit:**
   - Das Hauptcheckout liegt unter OneDrive (`~/Library/CloudStorage/OneDrive-Persönlich/Github/steps`); Agenten arbeiten in eigenen Worktrees (z. B. `.claude/worktrees/<name>`). Der Worktree `fix_onedrive_git_index` liegt außerhalb von OneDrive unter `~/.gemini/antigravity/worktrees/steps/`. Maschinenpfade gehören nicht in versionierte Dokumente – Verweise immer relativ setzen.
   - OneDrive neigt dazu, die Index-Datei eines Worktrees (`.git/worktrees/<name>/index`) bei Schreibkollisionen in `index 2` oder `index (<Datum>)` umzubenennen. Git meldet dann plötzlich alle 2.900+ Dateien als "gelöscht".
   - **Lösung:** Den Index sofort mit `git reset -q HEAD` (niemals `--hard`) wiederherstellen. Die Dateien auf der Platte bleiben dabei 100% unberührt. Die von OneDrive erzeugten Konfliktkopien im `.git`-Verzeichnis nicht löschen.
   - Der Pfad enthält „ö“ in zwei Unicode-Schreibweisen (NFC/NFD). Einzelne Editor-Werkzeuge lehnen den Pfad deshalb ab; Python- und Shell-Aufrufe aus dem Repository-Root funktionieren.
   - `git worktree list` zeigt neun veraltete Einträge (`prunable`) früherer Windows-/Temp-Worktrees. Nicht ohne Rückfrage bereinigen.
8. **Git-Identität:** Auf dem Mac ist kein `user.name`/`user.email` konfiguriert; die automatische Ableitung aus dem Rechnernamen scheitert je nach Netz. Identität beim Inhaber erfragen und je Commit mit `git -c user.name=… -c user.email=… commit` übergeben, keine globale Konfiguration ändern.
9. **Inhaberentscheidungen statt Fachabnahme:** Entscheidungen des Inhabers werden als „Inhaber“ mit Datum eingetragen und ausdrücklich nicht als unabhängige Fachabnahme bezeichnet. `scripts/audit_graph.py` erzeugt `GRAPH_AUDIT_MATRIX.csv` und weist dort jede Freigabe ab; menschliche Bewertungen liegen deshalb in eigenen, per `original_row_sha256` gebundenen Dateien (`GRAPH_HUMAN_REVIEW_v*.csv`).

---

## 3. Konsolidierte Audit-Befunde und Entscheidungen (PR #88 – #115 und Folgebranch)

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
- **Bekannte Nebenwirkung:** `run_golden_test_suite.py` überschreibt bei jedem Lauf fünf versionierte Dateien unter `knowledge/research/` (`FINAL_REFERENCE_CASE_VALIDATION.csv`, `GOLDEN_TEST_CLASSIFICATION_AUDIT.csv`, `MUSICAL_REFERENCE_VALIDATION.csv`, `GOLDEN_TEST_EXECUTION_REPORT.md`, `REAL_GOLDEN_TEST_EXECUTION_REPORT.md`) mit Zeitstempel, Laufzeiten, Plattform, Commit und CRLF→LF. Fachlich ändert sich nichts. **Behoben:** Ohne Argumente schreibt der Runner jetzt nichts; `--output-dir <Pfad>` exportiert, `--update-baseline` erneuert die versionierten Berichte bewusst (abgesichert durch `tests/test_golden_runner_outputs.py`).

### 3.9 Sitzung 16./17.11.2026: Korrekturen, Abnahmen und Richtungsentscheidungen
| PR | Inhalt |
| --- | --- |
| #111 | Diese Übergabe portabel gemacht (11 absolute `file:///`-Links → relativ), Ausgangsstand nachgezogen, Fahrplan korrigiert (Kern existiert bereits). |
| #112 | `knowledge/research/run_golden_test_suite.py` schreibt ohne Argumente nichts mehr; `--output-dir` exportiert, `--update-baseline` erneuert die versionierten Berichte; `tests/test_golden_runner_outputs.py`. |
| #113 | Abnahmebogen A1–A6, B1–B9 vom Inhaber entschieden (12 freigegeben, A1/B1 Korrektur, B2 Beleg fehlt), in zwei getrennten Commits. |
| #114 | Fehler behoben: `NoteSpelling.transpose_diatonic` verschob bei unpassenden Stufen/Halbtönen still die Oktave (C4 `(0, 11)` → Cb5); jetzt `InvalidAlterationError`. `tests/test_transpose_diatonic_strict.py` mit Eigenschaftsprüfung über alle 35 Schreibweisen. Gefunden über eine Zeilenmessung des Kerns: 85,3 % (831/974 Zeilen) werden von den Tests ausgeführt; Lücken sind fast nur Fehlerpfade. |
| #115 | [ADR-013](../../decisions/ADR-013-v01-umfang-akkorde-und-midi-export.md) (v0.1 = Akkorde + MIDI-Export, Drums v2, Zielgruppe Produzierende), [ADR-014](../../decisions/ADR-014-theorie-perspektiven-und-kontext.md) (Perspektivenmodell mit `paradigm`/`source`/`StyleContext`), [ADR-015](../../decisions/ADR-015-kernvertraege-intervalle-voicing-notation.md) (Kernverträge), [ADR-016](../../decisions/ADR-016-v7alt-alterierte-dominante.md) (`V7alt`); Graph-Abnahme v1 (25 Kanten). |
| Folgebranch | [ADR-017](../../decisions/ADR-017-midi-export-v01.md) (MIDI-Export), [ADR-007](../../decisions/ADR-007-audio-nur-dateiexport-v01.md) (nur Dateiexport), [ADR-001](../../decisions/ADR-001-ein-fenster-zwei-bereiche.md) (ein Fenster, zwei Bereiche), [ADR-003](../../decisions/ADR-003-glide-nur-shell-und-infrastruktur.md) (Glide nur Shell), [ADR-004](../../decisions/ADR-004-lizenz-und-marke.md) (Code MPL-2.0, eigene Wissensdaten CC BY 4.0), [ADR-006](../../decisions/ADR-006-json-mit-schema-version.md) (JSON, ganzzahlige `schema_version`); ADR-014 mit Hindemith I,2; Graph-Abnahme v2 mit allen 97 Kanten. |
| #116–#133 | SMF-Writer und MidiExportService in `src/steps/midi/` integriert; Kernverträge, Graphabnahme und Desktop-Shell-Verbindungen realisiert. |
| #134 | **OA-0032**: Cross-Domain Empfehlungs-Engine (`src/steps/progression/recommender.py`). Bidirektionale 4-Domänen-Relationen (Harmonik $\leftrightarrow$ Drums $\leftrightarrow$ Piano $\leftrightarrow$ Bass), 28 Archetypen, 97 Relationen, 9 Tests. |
| #135 | **OA-0030**: Shell-Voicing & Guide-Tone-Engine (`src/steps/theory/voicings.py`). Modul P05, LH Bassfundament, RH Guide Tones (3 & 7), Halbtonauflösungen, DE H vs INT B, 10 Tests. |
| #136 | **OA-0022**: Parametrisierbare Swing-Ratio & Micro-Timing Engine (`src/steps/models/swing.py`). REF-0020 (Straight), REF-0021 (Triplet), Roger Linn MPC 61% (+26 Ticks / 36,11 ms @ 90 BPM; ERR-034), Invariante CR-027, Friberg-Sundström Swing-Decay (CDR-017), 10 Tests. |
| #137 | **OA-0024**: Didaktische Reduktions- und Anfänger-Voicing-Engine (`src/steps/theory/beginner_voicing.py`). Reversible Reduktion von Vierklängen auf Dreiklänge, Pop Four Chords (C -> G -> Am -> F) Golden Case, 71% Bewegungsreduktion, RH Fingersatz 1-2-5/1-2-4, LH 5-1-2-4, 10 Tests (Gesamttests: 642). |
| #138 | **Docs**: Konsolidierte Master-Übergabe auf Commit `cc0c3f9` nach Abschluss von PR #134–#137. |
| #139 | **Release v0.1.0**: Erstes stabiles GitHub-Release von STEPS (Harmonik-Kern, Voicings, Rhythmik & MIDI-Export), Tag `v0.1.0`, Commit `1023fcf`. |
| #140 | **Chore**: Versionswechsel auf `0.2.0-dev` für Phase 5.4/v2 Entwicklung, Commit `be32c5d`. |
| PR (Folge) | **OA-0026**: Stilistische Differenzierung von Stimmführungsregeln (`src/steps/theory/voice_leading.py`). `VoiceLeadingStyle` (`STRICT_CLASSICAL`, `STRICT_COUNTERPOINT`, `CONTEMPORARY_POP`, `JAZZ_POP`, `POWER_CHORDS`, `QUARTAL_JAZZ`), Everett (2009) Power-Chords & Planing vs. Fux (1725) Kontrapunkt, Integration in `ProgressionSession` & `ProgressionSessionController`, 8 Tests (Gesamttests: 650). |

**Wichtige Abgleiche aus dieser Sitzung**, damit sie nicht erneut aufkommen:
- Ein vorgeschlagener Lizenzwechsel zu MIT/Apache wurde verworfen: Das Repository steht unter MPL-2.0, aus Glide übernommene Dateien müssen MPL-2.0 bleiben.
- Glide hat kein Musik-Datenmodell und keinen Parser; Wiederverwendung nur für die UI-Shell.
- 95 % Notenlänge hätte bei ganztaktigen Akkorden 100 ms Lücke ergeben (120 BPM); Standard ist deshalb Dauer minus 10 Ticks.
- CDR-019 darf nicht `HISTORICAL_ORIGIN` heißen, weil der Inhaber bei A5 einen Kausalanspruch ausgeschlossen hat; Typ `ATTRIBUTED_INTERPRETATION`.

---

## 4. Testarchitektur und Qualitätsgates

**Lokale Einrichtung:** `python3 -m pip install -r knowledge/benchmark/requirements.txt` (PyYAML 6.0.3, nur für Audit-Skripte; der Kern hat keine Laufzeitabhängigkeit).

**Stand 17.11.2026 (nach PR #140 und OA-0026):** **650 Unittests fehlerfrei bestanden (100% grün)**; `verify_reference_integrity.py` meldet 17 ADRs, 28 Progressionen, 31 Drum-Patterns, 19 Klaviermodule, 198 Unified Golden Cases und 97 Concept Relations. Die vollständige CI-Liste steht in [`.github/workflows/python-tests.yml`](../../.github/workflows/python-tests.yml); lokal mindestens zusätzlich `python3 -B scripts/audit_graph.py --check`, `python3 -B tools/validation/check_structure.py`, `python3 -B scripts/render_api_reference.py --check` und `python3 -B scripts/pre-commit-secret-check.py`. Neue ADRs brauchen einen Eintrag in `CANONICAL_ADR_THEMES` (`scripts/verify_reference_integrity.py`) und die erwartete Anzahl in `tests/test_reference_integrity.py`; der ADR-Status im Register muss ein reiner Wert sein (`proposed`, `accepted`, `rejected`, `superseded`).

Bevor ein PR eingereicht wird, müssen folgende Tests lokal fehlerfrei durchlaufen:
1. **Gesamte Unittest-Suite:**
   ```bash
   python3 -m unittest discover tests
   ```
   *Soll:* Ran 650 tests ... OK.
2. **Referenzintegrität:**
   ```bash
   python3 scripts/verify_reference_integrity.py
   ```
   *Soll:* 100% CANONICAL REFERENCE & SCHEMA INTEGRITY VERIFIED (Exitcode 0).
3. **Restricted Local Check:**
   ```bash
   python3 -m unittest tests/test_restricted_local.py
   ```
   *Soll:* OK (keine Klasse-E-Volltexte im Git).
4. **Knowledge Coverage CI-Gate (`scripts/audit_knowledge_coverage.py --check`):**
   - **Kritischer Hinweis:** GitHub Actions vergleicht `knowledge/benchmark/COVERAGE.csv` bitgenau mit der Anzahl der getrackten Dateien unter `research/`, `archive/`, `source_archive/`, `knowledge/legacy/` und `knowledge/research/`.
   - **Regel:** Niemals neue Dateien in diese 5 Ordner legen, ohne `COVERAGE.csv` nachzuziehen! Alle neuen Berichte und Dokumentationen gehören nach `docs/audit/` oder `docs/audit/fable-5.2/`!
5. **Secret-Remediation Baseline:**
   ```bash
   python3 scripts/verify_secret_remediation.py
   ```
   *Soll:* `{"residual_occurrences": 0, "baseline_unchanged": true}` (Exitcode 0).
6. **API-Dokumentations-Synchronität:**
   ```bash
   python3 scripts/render_api_reference.py --check
   ```
   *Soll:* Synchron (Exitcode 0).

---

## 5. Konkreter Fahrplan für den nächsten Agenten

Stand 17.11.2026 (nach PR #140 und OA-0026). Die vorherigen Arbeitspakete AP 1 (SMF-Writer), AP 2 (Kernverträge) und AP 3 (Graphabnahme) sowie die Funktionsblöcke OA-0032, OA-0030, OA-0022, OA-0024 und OA-0026 sind vollständig abgeschlossen.

### Nächste anstehende Aufgaben (Priorisierter Backlog)

#### 1. OA-0027: Implementierung formaler Property-Based Tests für Musiktheorie-Invarianten (M01/M04)
- **Ziel:** Robuste Invariantentests mittels automatischer Generierung zufälliger Tonhöhen, Intervalle und Akkordumkehrungen.
- **Geprüfte Invarianten:**
  - Modulo-12-Zyklizität: $\text{transpose}(P, 12) \equiv P$
  - Intervall-Umkehrung: $\text{invert}(\text{interval}) + \text{interval} = 12$
  - Enharmonische Äquivalenz und Vorzeichenverträglichkeit

#### 2. OA-0028 / OA-0029: Rationale MIDI-Zeit-Engine & SMF-Parser (M11)
- **Ziel:** Exakte rationale Zeitrechnung (`fractions.Fraction`) zur Vermeidung von Float-Drift bei triolischen und ungeraden Taktteilungen sowie vollständiger Standard-MIDI-File-Parser.

### Qualitätswerkzeuge (nur mit Zustimmung des Inhabers zur Paketinstallation)
- Vorgeschlagen und noch nicht installiert: `ruff` (in `pyproject.toml` konfiguriert), `mypy` (Kern deklariert `py.typed`), `coverage` mit Schwelle (Kern derzeit 85,3 % Zeilen), `hypothesis`, `mutmut`.

### Rechte und Kennzeichnung
- Lizenzkennzeichnung je Ordner nach [ADR-004](../../decisions/ADR-004-lizenz-und-marke.md) (SPDX für Code, CC BY 4.0 nur für eigene Wissensdaten, Fremdinhalte laut Rechteinventar); Markenprüfung „STEPS“ steht aus.

### Restpunkte ohne Blockade
- B2: Hindemith Kap. XIII im Original-PDF sichten; A6: Montuno-Entwurf anhören (beide nach v0.1).
- Offene Richtungsfragen mit geringer v0.1-Wirkung: Datenschema-Felder und Undo, Glide-Shell-Spike, Governance ([`PROJECT_OVERVIEW.md`](../project/PROJECT_OVERVIEW.md) §8).
