# 06 – Technischer Stand, Architektur und Schnittstellen

**Nachweislegende:** **G** = in dieser Sitzung über die GitHub-Verbindung direkt kontrolliert (nur ausdrücklich genannter Prüfgegenstand); **U** = Originalmeldung des Nutzers in der aktuellen Unterhaltung (meist Wiedergabe eines Antigravity-Abschlussberichts); **K** = eingeschränkte frühere Gesprächszusammenfassung; **A** = frühere Assistentenempfehlung/-auftrag; **D** = abgeleitete Bewertung, keine Repository-Verifikation; **X** = nicht zugänglich/nicht geprüft. Erfolgsmeldungen sind nicht automatisch unabhängig bestätigte Produkteigenschaften.

## Git-Referenzkette

```text
Phase 4.16  1657339 (historischer Prüfstand)
Phase 4.17  422ec962650e19a60b8c58520ea039a99c3befcb
  ↓ (direkte Abstammung laut 4.18; Compare-API bestätigt 422ec96 -> fe66637 3 Commits ahead)
Master-Audit 918d0a7105fabecbdb015f6bfe9ccc876e7f8ce2
  ↓
Phase 4.18  bb14fce85a8136560add49ff724a1b0d982f47ab
  ↓ (Parent von fe66637 durch GitHub API unabhängig bestätigt)
Phase 5.1   fe6663747250bf73ff28f4b7c591e8cf42f799d0
  ↓ (als zweiter Parent der Merge-Commit-Struktur)
main Merge PR #9 02f3776b24be52e3f00a973b3ad50f82d95e4abd
```

**Präzision:** `main` besitzt einen Merge-Commit. „lineare Entwicklung“ beschreibt die inhaltliche Phase-Kette auf der Feature-Seite, nicht den Graphen aller Git-Branches insgesamt.

## Repo-Module

| Pfad | Aufgabe | Herkunft / Abnahme |
|---|---|---|
| `src/steps/theory/exceptions.py` | domänenspezifische Fehlerhierarchie | G Commit-Pfad / U Bericht |
| `src/steps/theory/pitch.py` | PC Z12, Spelling, MIDI, Frequenz, EN/DE, Transpositionen | G Commit-Pfad / U Semantik |
| `src/steps/theory/interval.py` | diatonische/chromatische Intervalle inkl. 9/11/13 | G Commit-Pfad / U Semantik |
| `src/steps/theory/triad.py` | Dreiklangtypen/Inversionen | G Commit-Pfad / U Funktion |
| `src/steps/theory/seventh.py` | Vierklänge und Voicing-Modelle | G Commit-Pfad / U Funktion |
| `src/steps/theory/chord.py` | ChordDefinition, Akkordsymbole/Slash, Voicings | G Commit-Pfad / U Funktion |
| `src/steps/progression/voice_leading.py` | L1-/PC-Kreisdistanzen, Counterpoint/Jazz-Pop, Optimierung | G Commit-Pfad / U Funktion |
| `src/steps/progression/engine.py` | Registry 28 Progressionen; Roman-Degree-Resolver; Analyse | G Commit-Pfad / U Funktion |
| `.github/workflows/python-tests.yml` | Python 3.11/3.12, unittest discover `tests` und Skill | G Dateiinhalt geprüft, Run queued |
| `tests/test_theory_core.py` | Theorieprüfungen | G Dateiexistenz im Diff / U Testbericht |
| `tests/test_progression_engine.py` | 28-Progressionsregister und Roman-Resolver | G Dateiinhalt teilweise eingesehen |
| `knowledge/research/PHASE5_1_COMPLETION_REPORT.md` | Originaler Phase-5.1-Bericht | G von GitHub ausgelesen |

## Fachliche Repräsentationen (dokumentiert, noch unabhängig zu qualifizieren)

- Chromatische Pitch Class: `Z12 = {0,...,11}`; Notenorthographie `NoteSpelling` trennt Stammton, Vorzeichen und Oktave. `C#4` und `Db4` klingen gleich, sind notationsseitig verschieden.
- MIDI-Gleichung: `(octave+1)*12 + base_pc(step) + alteration`; A4=MIDI 69/440 Hz.
- Intervall-Engine erhält diatonische Stufeninformation bei enharmonischen Gleichheiten.
- `ChordDefinition` beschreibt harmonischen Gegenstand, `Voicing` konkrete belegte Töne; reduzierte Jazz-Voicings dürfen nicht als vollständiges theoretisches Akkordset gelten.
- Stimmführung: lokale L1- und zyklische Pitch-Class-Distanzen sowie stilabhängige Regeln. Die mathematischen Eigenschaften sind domänenspezifisch zu belegen.
- Progression: `PROG-021` und `PROG-028` ausdrücklich unterschiedene Archetypen.

## API- und Datenrisiken

- Vor einer Änderung Signaturen/Typen im tatsächlichen Merge-Commit auslesen, nicht vom Chatprotokoll ableiten.
- Mehrstimmige Optimierung kann lokale Minimierung von globaler Sequenzoptimierung unterscheiden; Anspruch in Bericht nicht unbesehen übernehmen.
- `src/glide-v3.53` Legacy bleibt unverändert, keine STEPS-API-Quelle.
- CI-Gates und Agentenberichte getrennt halten.
