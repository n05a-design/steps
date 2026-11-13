# Implementierungsstand von STEPS

Dieser Leitfaden beschreibt den Code im selben Checkout. Der Einstieg für
Entwicklung ist die [Root-README](../README.md). Die [API-Referenz](theory/API.md)
wird aus den exportierten Python-Objekten erzeugt. Der hier dokumentierte
Kern- und Pilotstand wurde am 12. November 2026 auf Commit `b0abd41` abgeglichen.

## Versionen und Freigabestatus

| Wert | Fundstelle und Bedeutung |
|---|---|
| `0.0.0-dev` | [VERSION](../VERSION) im Repository |
| `0.0.0.dev0` | [`src.steps.__version__`](../src/steps/__init__.py) im Python-Paket |
| Phase 5.1 | Historischer Entwicklungsstand des Headless-Kerns |
| V6.6/V6.7 | Stände der Forschungsbibliothek |
| 3.53.0 | Glide-Referenzstand |

Der Checkout enthält einen nutzbaren Python-Kern. Die [Projektkonfiguration](../pyproject.toml) definiert derzeit kein Build-System. Desktop-Start, verpackte App und öffentliche Produktfreigabe stehen aus. [Offene Punkte](../research/gaps/OPEN_GAPS.md) · [Entscheidungsregister](../decisions/DECISION_REGISTER.md)

## Laufzeit und Grenzen

| Bereich | Implementierung | Verhalten und Grenze |
|---|---|---|
| Tonhöhe und Schreibweise | [pitch.py](../src/steps/theory/pitch.py) | Tonklasse und diatonische Schreibweise sind eigene Typen. Frequenzberechnung nutzt gleichstufige Stimmung mit standardmäßig 440 Hz. `INT` verwendet B/B♭, `DE` H/B. Für mehrdeutige Eingaben die Konvention explizit setzen. Chromatische Transposition kann auch bei Verschiebung um null die enharmonische Schreibweise normalisieren. |
| Intervalle, Dreiklänge, Septakkorde | [interval.py](../src/steps/theory/interval.py), [triad.py](../src/steps/theory/triad.py), [seventh.py](../src/steps/theory/seventh.py) | Berechnungen für klingenden Abstand und diatonische Intervalle, Akkordkonstruktion, Umkehrungen, Drop-2 und Shell-Voicings. |
| Akkordsymbole | [chord.py](../src/steps/theory/chord.py) | Explizit registrierte Qualitäten und Aliasse. `CM7` ist Dur, `Cm7` Moll. Slash-Bass ändert die tiefste Note, die Rezeptur bleibt vom Grundton abgeleitet. Theoretische und für ein Voicing ausgewählte Tonklassen können sich unterscheiden. `C11` ist aktuell nicht registriert. |
| Stufen und Transposition | [engine.py](../src/steps/progression/engine.py) | Stufenauflösung in vorgegebenem Dur-/Moll-Kontext, ausgewählte Sekundärfunktionen und Generalbassfiguren. Keine Tonarterkennung aus Audio oder Auswahl einer kontextabhängigen Analyse. `V7(alt)` wird abgewiesen. Der Vertrag für Mischformen wie `V7(6)` ist offen. |
| Stimmführung | [voice_leading.py](../src/steps/progression/voice_leading.py), [engine.py](../src/steps/progression/engine.py) | Standardsequenz mit durchgehender Stimmenzahl. Der Solver minimiert die Summe absoluter Halbtonbewegungen je Übergang innerhalb ±12 Halbtönen pro Stimme. Er prüft Tonklassen, Bass, MIDI 0–127 und Stimmenreihenfolge. Der strikte Modus prüft parallele Quinten und Oktaven sowie gleichartige reine Außenstimmenintervalle in Gegenbewegung. Unlösbare Vorgaben lösen `VoiceLeadingError` aus. Das Startlayout akzeptiert `CLOSE`, `DROP2`, `SHELL` und `ROOTLESS`. Folgeakkorde können andere Lagen haben. Vollständiger Kontrapunkt und Spielbarkeit bleiben eigene Abnahmen. |
| Progressionskatalog | [Historischer Katalog](../knowledge/concepts/progressions/CHORD_PROGRESSION_REFERENCE_LIBRARY.md), [App-Lernmaterial](../knowledge/concepts/progressions/REVIEWED_PROGRESSIONS.md) | Die allgemeine API bietet 28 Bestandsprogressionen. Für die [App-Schnittstelle](../app/knowledge.py) sind drei Pilotbeispiele fachlich freigegeben. App-Schnittstelle und Lernmaterial verwenden dieselbe [Datenbasis](../src/steps/progression/reviewed_progressions.json). Die [Abnahmeliste](../knowledge/benchmark/PILOT_ABNAHME.md) dokumentiert die Freigaben. |
| Recherche und Quellen | [Quellenregister](../knowledge/sources/README.md), [Ingestion](../knowledge/INGESTION_PIPELINE.md) | App-Adapter und Renderer lösen Quellen-IDs im Produktregister auf und prüfen die fassungsgebundenen Freigaben aller Pilot-Aussagen. CI führt denselben Validator aus. Forschungsclaims und Rohmedien werden über den App-Adapter nicht geladen. |
| Desktop, Audio, MIDI und Speicherung | [app](../app/README.md), [Architekturziel](architecture/ARCHITECTURE_OVERVIEW.md) | Der App-Adapter ist importierbar. Ein Desktop-Einstieg, Wiedergabe, Import/Export, Persistenz und automatische Harmonieanalyse sind in diesem Checkout nicht als Produktabläufe implementiert. |

Ein konkretes `Voicing` speichert MIDI-Noten als unveränderliche Folge
in Stimmenreihenfolge. `midi_notes` liefert die Noten nach Tonhöhe
sortiert. Transpositionen und Rotationen erwarten Ganzzahlen.
Bei `SHELL` verwenden Septakkorde und ihre Erweiterungen die Terz bzw.
Suspension und die Septime, Sextakkorde die Terz und Sexte. Dreiklänge
und Add-Akkorde verwenden die Terz bzw. Suspension und die Quinte.
Ein angegebener Slash-Bass liegt unten. `DROP2` setzt eine Auswahl von
genau vier Tonklassen inklusive Slash-Bass voraus. Beim fehlenden
Slash-Bass verzichtet `ROOTLESS` auf den Grundton im gesamten Voicing.

`Cmadd9` und die C-Stufe `iadd9` ergeben C–E♭–G–D. Die theoretische
None liegt 14 Halbtöne über dem Grundton. Das Standardvoicing darf
ihre Tonklasse als Sekunde platzieren. `iadd9(6)` setzt E♭ in den Bass.
Eine Septakkordfigur wie `iadd9(65)` wird abgewiesen.
[Kris P. Shaffer, Lead-Sheet Chord Symbols, S. 1](https://openmusictheory.github.io/Graphics/Handouts/LSandFBsymbols.pdf)
· [Music Theory for the 21st-Century Classroom, § 31.1 Jazz Chord Basics](https://musictheory.pugetsound.edu/mt21c/JazzChordBasics.html)

## Ein Beispiel vom Symbol bis zum Voicing

```python
from src.steps.theory import parse_chord
from src.steps.progression import generate_progression_voicings, get_progression, resolve_roman_degree

assert parse_chord("CM7", "INT").theoretical_intervals == (0, 4, 7, 11)
assert resolve_roman_degree("ii7", "C").symbol == "Dm7"
example = get_progression("PROG-003")
voicings = generate_progression_voicings(example)
assert [v.bass_note % 12 for v in voicings] == [2, 7, 0]
```

Die [Pilotfreigabe](../knowledge/concepts/progressions/README.md) beschreibt den zusätzlichen Zugang zu geprüften Lehrtexten.

[Testanleitung](../tests/README.md) · [Quellen und Archiv](../archive/INDEX.md)

## GitHub-Nachweis für die Pilotfreigaben

Die App prüft die lokal gespeicherten Freigaben gegen die Fingerabdrücke und kann
die geprüften Pilotbeispiele offline anzeigen. Für die Freigabe eines Git-Stands
prüft `python -B scripts/verify_pilot_review_evidence.py --revision <commit-sha>`
zusätzlich die Originalkommentare per GitHub-API. Bei Netzfehlern oder abweichenden
Belegen schlägt dieser Befehl fehl. Die zwei bestehenden Nachweise behalten ihr
Format. Für neue Freigaben trägt ein zugelassenes Reviewkonto (`n05a-design` oder `timvontrostorff`) eine Zeile
`STEPS-APPROVED <claim-id> <fingerprint>` in einen PR-Kommentar ein. Datum ist
der Tag der Erstellung in UTC. Nach einer Bearbeitung ist ein neuer Kommentar
erforderlich. Eine fachliche Prüfung der Fundstelle bleibt Teil des Reviews.

Der Workflow `Pilot review evidence` vergleicht die Daten des Merge-Kandidaten
mit diesen Nachweisen. Er führt den Prüfer aus dem Basiscommit aus und meldet
`steps/pilot-review-evidence` auf dem PR-Commit. Nach Einführung auf `main` muss
der Repository-Verantwortliche diesen Status als erforderlichen Check und
menschliche Freigaben für Änderungen am Prüfer, Workflow und den Reviewkonten
über die Repository-Regeln absichern. Bei geänderter Basis oder widerrufenem
Beleg vor der Freigabe einen frischen Lauf verlangen. Für einen Release den
Belegcheck für den exakten Release-Commit ausführen.
