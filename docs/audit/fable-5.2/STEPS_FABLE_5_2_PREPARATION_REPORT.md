# STEPS · Vorbereitungsbericht zum Fable-5.2-Audit

Erstellt am 2026-11-12 auf dem lokalen Branch `claude/fable-5-2-audit-prep` (ausgehend von `main` = `22f3f5f`). Nicht committet. Produktivcode, Skills und Wissensdaten wurden nicht geändert.

## 1. Git-Baseline und Abweichungen

- Die Remote-Abfrage (`git ls-remote`) zeigte `main` = `22f3f5f`, PR #11 gemergt (Head `15100b8`).
- Lokal war `origin/main` veraltet (`1880257`). Lokales `main` steht auf `dbd319a` vom 2026-11-10 und ist damit überholt.
- `git fetch` brach im OneDrive-Ordner mit `mmap failed` ab. Workaround: frischer Klon im temporären Verzeichnis, daraus `origin/main` in die Worktree geholt. Der Klon wurde danach entfernt. Der lokale Branch `codex/steps-verified-music-core` (`b0abd41`) ist in `main` enthalten.
- Die Korrekturen aus dem Selbstcheck an `b0abd41` sind in `22f3f5f` umgesetzt: Pilotstatus in README und `docs/IMPLEMENTATION.md`, Archivpfade, CLAIM-034, Hinweise in `COVERAGE.csv` und `GOLDEN_DATA_SOURCE_OF_TRUTH.md`, PAT-031. Nur stichprobenhaft am Diff gesehen, nicht inhaltlich geprüft.

## 2. Untersuchte Bereiche

Gelesen wurden die öffentlichen Schnittstellen aller Module in `src/steps/`. Vollständig gelesen: `pitch.py`, `chord.py` (Parser und Voicing), `engine.py` (Katalog, Stufenauflösung, Voicing-Generierung), `voice_leading.py` (Solver), `reviewed.py` (Freigabe). Außerdem gelesen: `app/knowledge.py`, alle drei Skill-Orte, `SKILL.md`, `pyproject.toml`, die CI-Workflows, `tests/README.md`, `docs/IMPLEMENTATION.md`, `research/gaps/OPEN_GAPS.md`, `decisions/DECISION_REGISTER.md` und die Register- und Benchmarkdateien in `knowledge/` (Zählung und Status).

Nicht untersucht: der Inhalt von `research/` (außer `gaps/`), `archive/`, `source_archive/`, `src/glide-v3.53/`, den Einmal-Generatoren in `scripts/`, `docs/project/`, `publish_overlay/`, `prompts/`, `templates/`, `tools/` (außer `tools/validation/check_structure.py` als Testabhängigkeit). Gründe stehen in der Prüfmatrix unter „Ausgeschlossen“.

## 3. Ausgeführte Prüfungen

Siehe Kontextpaket, Abschnitt 3. Lokal lief Python 3.15.1, nicht die CI-Versionen 3.11 und 3.12. Zusätzlich lief die Kernsuite im Kontextbündel: 105 Tests, ein erwarteter Strukturfehler wegen fehlendem `research/ableton`. Die Benchmarkpfade lassen sich nach `git init` ausführen.

## 4. Gefundene Dokumentationswidersprüche

Diese Punkte sind Rahmenbedingungen für die Übergabe. Fachlich bewertet wurden sie nicht und sie sind keine Fable-Befunde. Im Prompt sind sie als Prüffragen enthalten, ohne Antwort.

1. `SKILL.md` verweist auf `skills/music-harmony-coach/`. Der Skill liegt aber im Unterordner mit Datum und U+2013 im Namen.
2. `skills/SKILL_DESIGN.md` beschreibt `knowledge/sources/registry.yaml` als leer. Die Datei enthält 7 Quellen.
3. `src/steps-0.00/` ist ein reines README-Gerüst neben dem echten Paket `src/steps/`.
4. Das Claim-Register führt 35 Claims als `VERIFIED_TRUE`. `COVERAGE.csv` zählt 3 fachlich untersuchte Forschungsclaims.
5. `knowledge/research/independent_golden_test_engine.py` hängt von `%LOCALAPPDATA%` ab.
6. `audit_knowledge_coverage.py --check` schlägt ohne PyYAML fehl. CI installiert PyYAML im eigenen Job, die lokale Testanleitung erwähnt das nicht.

## 5. Tokenoptimierung

- Baseline, Inventar, Testläufe und Ausschlüsse übernimmt die Vorbereitung. Fable bestätigt sie nur.
- Die Prüfmatrix ordnet jede Frage einer ID und einer Datei zu. Fable muss weder Verzeichnisse durchsuchen noch Archive lesen.
- Prioritätsreihenfolge mit dem Schutz, P0 nie zu kürzen. Befundschema und Fortsetzungsvorlage ersparen einen erneuten Kontextaufbau.
- Kontextbündel 1,7 MB, Mindestauswahl P0 rund 56.000 Tokens (Schätzung). Kataloge und Golden-Case-Daten werden gezielt gelesen.

## 6. Unabhängigkeit

Verifizierte Fakten (Kontextpaket 2–6) und Selbstauskünfte des Repositorys (Kontextpaket 7) stehen getrennt. Eigene Verdachtsmomente der Vorbereitung erscheinen nur als offene Prüffragen in der Matrix, nie als Befund und nie mit vorweggenommener Antwort.

## 7. Selbstprüfung (Phase H)

| Nr. | Prüfpunkt | Ergebnis |
|---|---|---|
| 1 | Alle genannten Pfade existieren auf `22f3f5f` | Ja, skriptgestützt über alle Backtick-Pfade der Paketdateien geprüft. Treffer waren nur Nicht-Pfade wie `V/vi` und Branchnamen |
| 2 | Modul- und Skillnamen stimmen | Ja, aus `__init__.py`, `__all__` und dem Skill-Frontmatter übernommen |
| 3 | Historisches nicht als aktuell ausgegeben | Ja, Coach als historisch markiert, `steps-0.00` und Glide ausgeschlossen |
| 4 | Alle aktiven Musikmodule erfasst | Ja, K01–K13 decken alle Dateien in `src/steps/theory` und `src/steps/progression` ab, dazu `app/knowledge.py` |
| 5 | Alle aktiven Skills erfasst | Ja, S01–S04. Keine weiteren `SKILL.md` außerhalb der ausgeschlossenen Bereiche |
| 6 | Kern, Skills, Wissen und Tests verknüpft | W08 und D5 (Datenkette PROG-003/-009), T-Zeilen je Kernbereich |
| 7 | Unabhängige Prüfung verlangt | Regel 2, D1 und die Gegenproben in Schritt 3 |
| 8 | Bekannte Fehler nicht als Befund ausgegeben | Ja, Kontextpaket 7 ist ausdrücklich als ungeprüft markiert |
| 9 | Test- und Nachweisstatus getrennt | `evidence` und `test_status` sind getrennte Felder, `NOT_RUN` ist Pflicht |
| 10 | Kritische Fach- und Wissenschaftsfragen enthalten | D1, W01, W02, W07, D7 |
| 11 | Prüfgegenstände präzise | Jede ID mit Datei, Funktion und Beispiel-Eingaben |
| 12 | Kein Ballast | Keine Chatverläufe, keine Verzeichnislisten, keine Codekopien |
| 13 | Kontext ausreichend | Ja für P0 und P1 im Bündel. Einschränkung: externe Fachquellen muss Fable selbst abrufen können |
| 14 | Mit begrenztem Budget ausführbar | P0-Mindestauswahl von rund 56.000 Tokens plus Bericht. Fortsetzung möglich |
| 15 | Sicherheit und Rechte | Secret-Baseline, Fixtures, Abgleichs-CSV und Fremdmaterial sind aus dem Bündel ausgeschlossen. Dateisuche bestätigt, dass keine `*secret*`-Daten enthalten sind |
| 16 | Reproduzierbar und verwertbar | Revision fest, Befehle angegeben, YAML-Befunde, Rückgabeweg |

### Trockenlauf

Ohne Fable-Aufruf wurde durchgespielt, welche Dateien ein neuer Prüfer braucht:

- **Algorithmus K07, `resolve_roman_degree`.** Benötigt werden `engine.py`, `pitch.py` (`parse_spelling`, `transpose_diatonic`), `chord.py` (`ChordDefinition`, Templates), `exceptions.py`, dazu `tests/test_progression_engine.py`, `tests/test_pilot_publication.py` und `docs/theory/API.md`. Alles liegt im Bündel und in der Mindestauswahl. Im entpackten Bündel liefen Importe und Probeaufrufe aus dem Root. Dabei fiel auf, dass `python -I` den Root nicht im Pfad hat. Der Prompt nennt deshalb den Aufruf ohne `-I`.
- **Skill S01 und Freigabe K11.** Benötigt werden `.agents/skills/steps-knowledge-curation/` vollständig, `docs/engineering/MUSIC_DOMAIN_AND_MIDI.md`, `reviewed.py`, beide Pilot-JSONs, `knowledge/sources/registry.yaml` und `knowledge/benchmark/PILOT_ABNAHME.md`. Alles im Bündel. Nachgetragen wurde `PILOT_ABNAHME.md` in der Mindestauswahl. Einschränkung: Das echte Master-Register unter `%LOCALAPPDATA%` ist nicht verfügbar. S01 lässt sich nur an Skripten und Tests prüfen.

## 8. Verbleibende Einschränkungen

- Das Paket ist auf diesem Branch nicht committet. Bis zu einem Merge liegen die Dateien nur lokal und müssen Fable angehängt werden (Anleitung, Fall A).
- Python 3.11 und 3.12 lokal `NOT_RUN`.
- Ein konkretes Fable-Kontingent ist unbekannt. Die Budgetwerte sind Schätzungen.
- Externe Fachquellen sind nicht im Bündel (Rechte). Fable braucht Webzugriff oder eigene Kenntnisse mit ausgewiesener Herleitung.
- Das Master-Register des Curation-Skills liegt außerhalb des Repositorys und ist nicht prüfbar.
- Die lokale Ablage im OneDrive-Ordner stört `git fetch`. Spätere Läufe sollten aus einem Klon außerhalb von OneDrive arbeiten.
