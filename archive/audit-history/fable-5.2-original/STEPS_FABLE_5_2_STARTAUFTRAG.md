# STEPS · Startauftrag für das Fable-5.2-Audit

Diese Nachricht startet das unabhängige Gesamtaudit von STEPS. Sie legt fest, wo die Unterlagen liegen, wie die Umgebung eingerichtet ist und wohin die Ergebnisse geschrieben werden. **Den Auftrag selbst gibt der Masterprompt vor. Bei jedem Widerspruch gilt der Masterprompt.** Nichts in dieser Nachricht lockert eine seiner Regeln.

Arbeite selbstständig von Phase 1 bis Phase 6. Frag nur nach, wenn du ohne Antwort nicht weiterkommst (z. B. fehlende Berechtigung, fehlende Abhängigkeit).

---

## 0. Verbindliche Unterlagen – zuerst vollständig lesen

| Rang | Datei | Inhalt |
|---|---|---|
| 1 | `~/steps-fable-pack/STEPS_FABLE_5_2_MASTERPROMPT.md` | Auftrag, Regeln 1–7, Vorgehen, Pflichtuntersuchungen D1–D7, Befundstandard, Berichtsgliederung |
| 2 | `~/steps-fable-pack/STEPS_FABLE_5_2_AUDIT_SCOPE.md` | Prüfmatrix mit IDs K01–K13, S01–S04, W01–W08, T01–T07, A01–A04, H01–H02 und Ausschlüssen |
| 3 | `~/steps-fable-pack/STEPS_FABLE_5_2_CONTEXT_PACK.md` | Baseline, Modul- und Skill-Landkarte, Register, Prüfläufe der Vorbereitung. Abschnitt 7 ist ungeprüft |
| 4 | diese Nachricht | Umgebung, Fundorte, Ablage der Ergebnisse |

Lies außerdem **nicht**:
- den Branch `origin/claude/fable-5-2-audit-prep` im Klon. Er enthält Vorbereitungsnotizen, die deine Unabhängigkeit beeinträchtigen würden. Die drei Paketdateien oben genügen.
- `origin/main` (`3f78cc8`). Prüfgegenstand ist ausschließlich `22f3f5f`.
- andere Dateien in `~/steps-fable-pack/` außer den drei Paketdateien und deinen eigenen Ergebnissen.

---

## 1. Arbeitsumgebung (Stand 2026-11-12, vor Übergabe geprüft)

| Punkt | Stand |
|---|---|
| Checkout | `~/steps-fable-audit`, frischer Klon außerhalb von OneDrive |
| Revision | `HEAD` losgelöst auf `22f3f5f348d060abfd4e2ffc917d0c95a639441e`, Arbeitsverzeichnis sauber |
| Spätere Commits | `origin/main` = `3f78cc8` liegt 3 Commits später. Sie ändern nur `.gitattributes` und den Dateimodus von `scripts/git-hooks/pre-commit`, keinen Prüfpfad. Nicht auschecken, nicht prüfen |
| Python | `python3` = 3.14.5, `python3.12` = 3.12.16 (CI-Version), `python3.13` = 3.13.18. **3.11 ist nicht installiert** → für 3.11 gilt `NOT_RUN`. Einen Befehl `python` gibt es nicht |
| Zusatzpaket | `PyYAML==6.0.3` laut `knowledge/benchmark/requirements.txt`, nur für `scripts/audit_knowledge_coverage.py` |
| Paketimport | `src.steps` ist nicht installierbar. Importe laufen vom Repository-Root aus über `src.steps`, ohne `-I` |
| Ergebnisse | `~/steps-fable-pack/results/` |
| Experimente | `~/steps-fable-pack/work/` (Gegenproben-Skripte, Arbeitskopie für Mutationen) |

Einrichtung, einmalig, alles außerhalb des Checkouts:

```bash
mkdir -p ~/steps-fable-pack/results ~/steps-fable-pack/work/probes
python3.12 -m venv ~/steps-fable-pack/.venv312
~/steps-fable-pack/.venv312/bin/pip install PyYAML==6.0.3
```

Danach gilt in jedem Befehl `PY=~/steps-fable-pack/.venv312/bin/python`. Ersetze `python` in den Befehlen des Masterprompts und des Kontextpakets durch `$PY`. Rufe immer mit `-B` auf, damit im Checkout kein `__pycache__` entsteht.

**Gegenproben-Skripte** liegen in `~/steps-fable-pack/work/probes/<ID>_<thema>.py` und werden so ausgeführt:

```bash
cd ~/steps-fable-audit && PYTHONPATH=. "$PY" -B ~/steps-fable-pack/work/probes/K07_stufen.py
```

**Arbeitskopie für Mutationsversuche** (K11, T02, S01). Nie im Checkout mutieren. Diese Kopie enthält weder Glide noch Secret-Dateien, ist rund 5 MB groß, und die Pilot- und Kerntests laufen darin:

```bash
mkdir -p ~/steps-fable-pack/work/copy && git -C ~/steps-fable-audit archive 22f3f5f -- src app tests knowledge scripts tools docs AGENTS.md pyproject.toml VERSION ':(exclude)src/glide-v3.53' ':(exclude)src/steps-0.00' ':(exclude)scripts/historical_secret_baseline.json' ':(exclude)tests/fixtures' ':(exclude)tests/test_secret_scanner.py' | tar -x -C ~/steps-fable-pack/work/copy
```

In der Kopie gibt es kein Git. Was `git rev-parse HEAD` braucht (`scripts/run_knowledge_benchmark.py`, `tests/test_knowledge_benchmark.py`), führst du deshalb nur im Checkout aus.

**Sauberkeitsprüfung:** `git -C ~/steps-fable-audit status --porcelain` muss zu Beginn und nach jeder Phase leer sein. Ist die Ausgabe nicht leer, halte die Dateiliste fest. Entfernst du Dateien, die nachweislich dein eigener Lauf erzeugt hat, vermerke das. Eine Seiteneffekt-Datei eines Repository-Werkzeugs ist selbst ein möglicher Befund (T05/T06).

---

## 2. Fundorte in der Ablage

Alle Pfade gelten relativ zu `~/steps-fable-audit` auf `22f3f5f` und sind vor der Übergabe auf Existenz geprüft. Was hier steht, ist eine Behauptung des Repositorys und kein Beleg (Masterprompt, Regel 2).

| Zweck | Pfad | Für IDs |
|---|---|---|
| Arbeitsvertrag (Nr. 4 Domänengrenze, Nr. 5 H/B-Notation) | `AGENTS.md` | K02, A04, D1 |
| Verhaltensgrenzen laut Projekt | `docs/IMPLEMENTATION.md` | K01–K12 |
| API-Vertrag (generiert) | `docs/theory/API.md`, Generator `scripts/render_api_reference.py --check` | K01–K10 |
| Fachmodell und Invarianten | `docs/engineering/MUSIC_DOMAIN_AND_MIDI.md` | K01, K02, S01 |
| Theorie-Kern | `src/steps/theory/pitch.py`, `interval.py`, `triad.py`, `seventh.py`, `chord.py`, `exceptions.py` | K01–K06, K13 |
| Progression-Kern | `src/steps/progression/engine.py`, `voice_leading.py`, `reviewed.py` | K07–K11 |
| Pilotdaten und Freigaben | `src/steps/progression/reviewed_progressions.json`, `reviewed_progression_approvals.json` | K11, W08, D5 |
| Wissensadapter | `app/knowledge.py` | K12, A03, D5 |
| Aktiver Skill | `.agents/skills/steps-knowledge-curation/` (`SKILL.md`, `README.md`, `references/`, `scripts/`, `templates/`, `tests/`) | S01, D4 |
| Root-Router | `SKILL.md` | S02 |
| Historischer Coach | `skills/music-harmony-coach/README.md` und der Unterordner mit Datum und Gedankenstrich U+2013 | S03 |
| Skill-Design | `skills/SKILL_DESIGN.md`, `skills/README.md` | S04 |
| Produktquellen (JSON-Inhalt trotz `.yaml`) | `knowledge/sources/registry.yaml` | W01 |
| Claim-Register | `knowledge/sources/MUSIC_SOURCE_CLAIM_REGISTER.csv` | W02 |
| Kuratierte Quellen | `knowledge/sources/curated_sources_registry.yaml` | W03 |
| Kataloge | `knowledge/concepts/progressions/CHORD_PROGRESSION_REFERENCE_LIBRARY.md`, `knowledge/concepts/chords/PIANO_PRACTICE_REFERENCE_LIBRARY.md`, `knowledge/concepts/styles/DRUM_GROOVE_REFERENCE_LIBRARY.md`, `knowledge/concepts/styles/GENRE_RESEARCH_LATIN.md` | W04, K08 |
| Relationen | `knowledge/relations/MUSIC_CONCEPT_RELATIONS.csv` | W05 |
| Benchmark | `knowledge/benchmark/cases.json`, `COVERAGE.csv`, `THEMENSTICHPROBEN.md`, `PILOT_ABNAHME.md`, Runner `scripts/run_knowledge_benchmark.py`, Abdeckung `scripts/audit_knowledge_coverage.py` | W06, T05 |
| Golden Cases | `knowledge/research/golden_cases/golden_reference_cases.json`, Spiegel `tests/golden_cases/golden_reference_cases.json`, `knowledge/research/GOLDEN_DATA_SOURCE_OF_TRUTH.md` | W07, T03 |
| Fehler- und Lückenregister | `knowledge/research/03_FACHLICHE_FEHLER.md`, `research/gaps/OPEN_GAPS.md` | W04, W07, Restrisiken |
| Entscheidungen | `decisions/DECISION_REGISTER.md` | A01–A04 |
| Tests | `tests/README.md`, `tests/test_*.py` | T01–T07 |
| Referenzintegrität | `scripts/verify_reference_integrity.py` | T04 |
| Strukturprüfung | `tools/validation/check_structure.py` | T06, T07 |
| CI | `.github/workflows/python-tests.yml`, `structure-check.yml`, `secret-scan.yml` | T06 |
| Frühere Audits | `docs/audit/00_GESAMTBEWERTUNG_UND_METHODIK.md` bis `docs/audit/05_VALIDIERUNGSBERICHT.md` | H01, D7 |
| Archivindex | `archive/INDEX.md` (nur von dort aus gezielt in Master-Audit V2 und OpenAI-Prüfpaket) | H02, D7 |

Gesperrt nach Masterprompt Regel 5 und Kontextpaket Abschnitt 8:
- **Nie lesen, nie zitieren:** `scripts/historical_secret_baseline.json`, `tests/fixtures/synthetic_secrets.json`, Ausgaben des Secret-Scans.
- **Nicht öffnen:** `src/glide-v3.53/`, `src/steps-0.00/`, `research/` außer `research/gaps/`.
- **Nur für H01/H02 und gezielt:** `archive/`, `source_archive/`.

---

## 3. Ablauf und Arbeitsergebnisse je Phase

Führe parallel `~/steps-fable-pack/results/ARBEITSNOTIZEN.md`, stichwortartig. Aktualisiere die Datei nach jeder Phase mit: erledigte IDs, offene IDs, vergebene F-IDs (nur Kurzzeile), ausgeführte Befehle mit Exit-Code. Wird dein Kontext gekürzt, setzt du anhand dieser Datei fort, ohne von vorn anzufangen.

### Phase 1 · Prüfbasis (Masterprompt Schritt 1)
1. `git -C ~/steps-fable-audit rev-parse HEAD` und `status --porcelain` festhalten.
2. Mit `$PY` (3.12) alle Befehle aus Kontextpaket Abschnitt 3 ausführen und die Ergebnisse dagegenhalten:
   - `-m unittest discover -s tests -p "test_*.py"`
   - `-m unittest discover -s .agents/skills/steps-knowledge-curation/tests`
   - `scripts/render_api_reference.py --check`
   - `scripts/run_knowledge_benchmark.py --scope pilot`, `--scope publication`, `--scope all`
   - `scripts/run_knowledge_benchmark.py --check-review-sheet knowledge/benchmark/PILOT_ABNAHME.md`
   - `scripts/render_reviewed_progressions.py --check`
   - `scripts/audit_knowledge_coverage.py --check`
   - `scripts/verify_reference_integrity.py`
3. Ergänzend die Kernsuite einmal mit `python3.13` und `python3`. Gibt es versionsabhängige Abweichungen, sind sie ein Befund. 3.11 bleibt `NOT_RUN`.
4. Jede Abweichung von Abschnitt 3 des Kontextpakets wird ein Befund oder ein vermerkter Umgebungsunterschied. Ordne selbst ein, was davon zutrifft, und begründe es.

**Ergebnis:** Prüfbasis-Tabelle (Befehl, Python-Version, Exit-Code, Kurzergebnis, Abweichung) für Berichtsabschnitt 2.

### Phase 2 · P0 (Masterprompt Schritt 2 und 3)
IDs: **K01, K02, K03, K05, K07, K11, W01, W08**.
- Für jede ID zuerst Code und Vertrag lesen (`docs/theory/API.md`, `docs/IMPLEMENTATION.md`, `docs/engineering/MUSIC_DOMAIN_AND_MIDI.md`).
- **Mindestens 10 eigene Gegenproben je ID**, darunter Grenzfälle und ungültige Eingaben. Den Sollwert schreibst du **vor** der Ausführung ins Skript, mit kurzer Herleitung als Kommentar. Erst danach führst du aus und notierst den Ist-Wert. So bleibt nachvollziehbar, dass der Sollwert nicht aus der Ausgabe stammt.
- Bei K02 und K05 jede Aussage mit Konvention kennzeichnen (DE: H/B, Hes … · INT: B/Bb …). Bei Mehrdeutigkeit alle vertretbaren Lesarten angeben.
- K11 mit Mutationsversuchen in der Arbeitskopie: Fingerabdruck verändern, Link verändern, Freigabe entfernen, Freigabe selbst eintragen. Halte fest, was die Sperre erkennt und was nicht.
- W08 und D5: Kettenprotokoll für PROG-003 und PROG-009 als Tabelle mit Stationen, Fundstelle, Prüfergebnis und Bruchstelle.

**Ergebnis:** P0-Befunde im YAML-Schema, Gegenprobentabelle (auch bestandene Fälle), Kettenprotokoll.

### Phase 3 · P1 (Masterprompt Schritt 4)
IDs: **K04, K06, K08, K09, K10, S01, W02, W04, W06, W07, T01, T02, T03, T05, A03**.
- K09: Optimalität des Stimmführungssolvers durch Brute-Force-Gegenrechnung auf kleinen Fällen prüfen.
- W07 und D3: mindestens 20 Golden Cases aus allen Domänen M01–M12 fachlich prüfen, davon mindestens 10 `SPECIFICATION_EXAMPLE`. Dazu den Benchmark-FAIL `KB-M11-ALTER` einordnen.
- W02: Stichprobe von mindestens 8 Claims über M01–M12.
- S01 und D4: Kernfrage des Masterprompts – kann etwas ohne ausreichenden Nachweis als `VERIFIED`, `DONE_VERIFIED` oder freigegeben gelten? Beim Skill über Skripte und Tests prüfen, bei `reviewed.py` über die Ergebnisse aus K11.

**Ergebnis:** P1-Befunde, Erweiterung der Gegenprobentabelle.

### Phase 4 · P2 und P3, soweit das Budget reicht
IDs: K12, K13, S02, S03, S04, W03, W05, T04, T06, T07, A01, A02, A04, H01, H02. **P0 wird nie gekürzt.**

### Phase 5 · Abgleich mit vorhandenen Ergebnissen (Masterprompt Schritt 5)
Halte deine Ergebnisse gegen Golden Cases, Benchmark, Claim-Register und D7. Für D7 prüfst du drei bis fünf Gesamtaussagen aus `docs/audit/` und über `archive/INDEX.md` und gibst ihre tatsächliche Reichweite auf `22f3f5f` an.

### Phase 6 · Abschlussbericht (Masterprompt Schritt 6)
Siehe Abschnitt 4. Spätestens wenn absehbar ist, dass Budget oder Kontext nicht reichen, schreibst du den Bericht mit dem erreichten Stand. Offene IDs stehen dann als `NICHT_GEPRÜFT` oder `TEILWEISE` mit Grund in der Abdeckungsmatrix und in Abschnitt 8 „Fortsetzung“. Ein unvollständiger Bericht ist besser als keiner.

---

## 4. Ausgabe

- **Bericht:** `~/steps-fable-pack/results/FABLE_AUDIT_REPORT_<JJJJ-MM-TT>.md` mit dem Datum des Laufs. Gliederung genau nach Masterprompt Abschnitt „Abschlussbericht“, Punkte 1–8. Befunde im YAML-Schema des Masterprompts, ohne zusätzliche Felder. Das Projekt übernimmt den Bericht später unverändert nach `docs/audit/fable-5.2/results/`.
- **Belege:** Gegenproben-Skripte bleiben in `~/steps-fable-pack/work/probes/`. Im Feld `reproduction` steht der vollständige Befehl, mit dem sich der Befund nachstellen lässt.
- **Fachquellen:** Hast du Webzugriff, nimmst du nur Metadaten und kurze Belegstellen mit Fundort (URL, Kapitel oder Seite). Ohne Webzugriff steht im Feld `reference` die Herleitung, ausdrücklich als solche gekennzeichnet. Erfinde keine Seitenzahlen.
- **Antwort im Chat am Ende:** höchstens 15 Zeilen. Dazu gehören Befunde je Priorität, die drei wichtigsten Risiken, offene IDs und der Pfad zum Bericht. Den Bericht nicht in den Chat kopieren.

---

## 5. Grenzen

- Im Checkout `~/steps-fable-audit` nichts ändern: keine Commits, kein Push, kein PR, kein `checkout` und kein `switch`, kein `fetch`.
- Mutationen nur in `~/steps-fable-pack/work/copy`.
- Ein grüner Test belegt nur seine Assertion. Ein Statusfeld (`VERIFIED_TRUE`, `PASS`, „100 %“) ist eine Behauptung (Masterprompt Regel 2 und 7).
- Deutsches H/B und internationales B/B♭ in jeder Aussage auseinanderhalten. Enharmonische Schreibweisen sind verschiedene Objekte.
- Befehle möglichst bündeln, damit wenige Berechtigungsabfragen nötig sind.

---

## 6. Ungeprüfte Hinweise aus der Einrichtung dieser Umgebung

Diese Hinweise sind wie Kontextpaket Abschnitt 7 zu behandeln: Sie sind Prüfgegenstand, kein Ergebnis.

1. Die Prüfläufe in Kontextpaket Abschnitt 3 liefen unter Windows 11 mit Python 3.15.1.
2. Auf diesem Mac lief die Root-Suite vor der Übergabe auf einem Stand mit identischem Code (`22f3f5f` plus `.gitattributes`) mit Python 3.14: 120 Tests, OK. In der Skill-Suite schlug `test_03_exact_duplicate_identification` fehl. Die Meldung vergleicht `/private/var/…` mit `/var/…`. Ordne selbst ein, ob das ein Produkt-, Test- oder Umgebungsbefund ist.

---

## Start

Lies jetzt die Dateien aus Abschnitt 0 in der Rangfolge 1 bis 3. Richte danach die Umgebung nach Abschnitt 1 ein und beginne mit Phase 1.
