# 08 – Tests, CI und Beweiskraft

**Nachweislegende:** **G** = in dieser Sitzung über die GitHub-Verbindung direkt kontrolliert (nur ausdrücklich genannter Prüfgegenstand); **U** = Originalmeldung des Nutzers in der aktuellen Unterhaltung (meist Wiedergabe eines Antigravity-Abschlussberichts); **K** = eingeschränkte frühere Gesprächszusammenfassung; **A** = frühere Assistentenempfehlung/-auftrag; **D** = abgeleitete Bewertung, keine Repository-Verifikation; **X** = nicht zugänglich/nicht geprüft. Erfolgsmeldungen sind nicht automatisch unabhängig bestätigte Produkteigenschaften.

## Status je Phase

| Phase | In Bericht genannte Tests | Eigene Verifikation dieser Sitzung | Bewertung |
|---|---|---|---|
| Phase 3.1 | 19/19 Skill | keine Ausführung | historisch gemeldet |
| Phase 3.2 | 23/23 Skill | keine Ausführung | historisch gemeldet |
| Master-Audit | 72/72 (47 Kern+25 Skill) | Ergebnisbericht auf GitHub vorhanden | nicht selbst reproduziert |
| Phase 4.18 | 89/89 (17 neue vs. 4.17/Skill) | Commit und Bericht vorhanden | nicht selbst reproduziert |
| Phase 5.1 | 115/115 (90 Tests in `tests/` +25 Skill) | Bericht + Python-Workflow + Testdatei vorhanden | nicht selbst reproduziert |

### Korrekte Phase-5.1-Verteilung laut eingesehenem Abschlussbericht

| Datei/Testgruppe | Anzahl |
|---|---:|
| `tests/test_theory_core.py` | 31 |
| `tests/test_progression_engine.py` | 12 |
| `tests/test_golden_references.py` | 28 |
| `tests/test_secret_scanner.py` | 15 |
| `tests/test_structure.py` | 4 |
| Knowledge Curation Skill | 25 |
| **Summe** | **115** |

**Wichtig:** Die Formulierung „90 Core-Tests + 28 Golden +25 Skill“ ist potenziell missverständlich: Die **90 Tests im `tests/`-Verzeichnis enthalten bereits die 28 Golden-Tests** (31+12+28+15+4=90). 90+28+25 wäre eine Doppelzählung. Die oben stehende Sechseraufteilung erklärt die 115 korrekt.

### Golden Reference Cases ≠ Testmethoden

Frühere Referenzbasis: 198 Cases, davon 67 rechnerische und 131 Spezifikations-/Dokumentationsbeispiele. Die Phase-5.1-Testsuite enthält 28 Testmethoden unter einer Golden-Tests-Datei. Ohne Einzelnachweis kann man weder 198 vollständig ausführbare Unittests noch eine Eins-zu-eins-Überdeckung aller 198 Referenzeinträge behaupten.

## Tatsächlich eingesehene Remote-Prüfdaten

- GitHub Commit `fe66637`: `feat(theory): harden music theory and progression core (Phase 5.1)` mit den angekündigten Dateien (G).
- `.github/workflows/python-tests.yml`: Push-Trigger auf main/feat/fix/chore, PR auf main, ubuntu-latest, Matrix Python **3.11/3.12**, `python -B -m unittest discover -s tests -p "test_*.py" -v`, plus Skill-Tests (G).
- Für `fe66637` ergab die GitHub Actions API insgesamt sechs angelegte Workflow-Runs, einschließlich Python Tests, Repository structure, Secret Scanning Guardrail. Abgefragte Python-Runs **43097534590** und **43097015761** erschienen als `queued`, `conclusion=null`; zu Run 43097534590 wurden **0 Jobs** aufgelistet. Das ist kein erfolgreicher Laufnachweis.
- GitHub Combined Commit Status lieferte eine leere `statuses`-Liste. Dieser Endpunkt erfasst nicht alle Check-Runs und darf nicht als Fehler- oder Erfolgsaussage interpretiert werden.
- Die vom Nutzer in früheren Berichten genannten Struktur-/Security-CI-Runs (z. B. 43094728367, 43094728397) wurden hier nicht mit kompletten Logs revalidiert.

## Reproduzierbare Startbefehle (nicht hier ausgeführt)

```powershell
Set-Location 'C:\Users\Timvo\OneDrive\Github\steps'
git status --short --branch
git log --oneline --graph --decorate -20
git show --stat --oneline fe66637
python -B -m unittest discover -s tests -p 'test_*.py' -v
python -B -m unittest discover -s .agents/skills/steps-knowledge-curation/tests -v
python tools/validation/check_structure.py
python scripts/pre-commit-secret-check.py --all-files
```

**Prüfung vor Ausführung:** Befehle und Test-Nebenwirkungen anhand des aktuellen Repository-Stands prüfen; Secrets nicht drucken. Auf Windows Python-Version, Interpreter und PATH dokumentieren. Prüfe den tatsächlich für den Workflow verwendeten Commit und nicht nur den früheren Feature-Commit.

## Weitere gezielte QA

Für `PitchClass`, `NoteSpelling` und Intervalltranspositionen: Doppelvorzeichen, Oktavgrenzen, MIDI 0/127, internationale/deutsche Schreibweisen, Roundtrip unter ausdrücklich definierten Domänen. Für `ChordDefinition`: theoretisches Set vs. konkretes Voicing. Für Voice Leading: gleiche Stimmzahl, Zuordnung/Permutationssymmetrie, unzulässige parallele Bewegung nur in strengem Kontrapunkt. Für Progressionen: Kontext, Roman-Degree-Resolver in Moll, Zwischendominanten, nicht nur Referenzstrings.
