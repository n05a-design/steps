# Implementierungsstand von STEPS

Dieser Leitfaden beschreibt den Code im selben Checkout. Der Einstieg für
Entwicklung ist die [Root-README](../README.md). Die [API-Referenz](theory/API.md)
wird aus den exportierten Python-Objekten erzeugt. Der hier dokumentierte Stand verwendet `main` bei Commit
[`779e2f7ccbe75d6f4e7b145c249d58a7bf562eee`](https://github.com/n05a-design/steps/commit/779e2f7ccbe75d6f4e7b145c249d58a7bf562eee)
als Produkt-Baseline. PRs #158–#164 ergänzen Save/Open, Lokalisierung,
Akkordbearbeitung, Neuordnung, Undo/Redo sowie Tonart-/Dur-Moll-/Tempo-Kontext.
PR #164 ergänzt editierbare Taktart sowie Start-Ticks und Dauern pro
Akkordereignis. Dieser Arbeitszweig ergänzt die bar:beat:tick-Projektion für die
Startposition; gespeichert und exportiert werden weiterhin absolute Tickwerte.
Implementierung, Test, fachliche Abnahme und Veröffentlichung sind getrennte
Statusangaben.

## Versionen und Freigabestatus

| Wert | Fundstelle und Bedeutung |
|---|---|
| `0.2.0-dev` | [VERSION](../VERSION), aktueller Entwicklungsstand |
| `0.2.0.dev0` | [`src.steps.__version__`](../src/steps/__init__.py) und [pyproject.toml](../pyproject.toml), PEP-440-Schreibweise des Entwicklungspakets |
| v0.1.0 | Vorhandenes GitHub-Release/Tag; keine Aussage über den heutigen 1.0-Reifegrad |
| 1.0.0 | Noch nicht durch ein angenommenes ADR definiert oder terminiert; siehe [Zielbild und Readiness](product/V1.0.0_PRODUCT_CONTRACT.md) |
| Phase 5.1 | Historischer Entwicklungsstand des Headless-Kerns |
| V6.6/V6.7 | Stände der Forschungsbibliothek |
| 3.53.0 | Glide-Referenzstand |

Der Checkout enthält einen nutzbaren Python-Kern sowie eine Tkinter-Desktop-
Vorschau und einen CLI-Einstieg. `pyproject.toml` definiert ein setuptools-
Build-System und einen `steps`-Entry-Point. Ein daraus gebautes, unterstütztes
und plattformgeprüftes Desktop-Installationspaket ist damit nicht belegt.
[Offene Punkte](../research/gaps/OPEN_GAPS.md) ·
[Entscheidungsregister](../decisions/DECISION_REGISTER.md)

## Laufzeit und Grenzen

| Bereich | Implementierung | Verhalten und Grenze |
|---|---|---|
| Tonhöhe und Schreibweise | [pitch.py](../src/steps/theory/pitch.py) | Tonklasse und diatonische Schreibweise sind eigene Typen. Frequenzberechnung nutzt gleichstufige Stimmung mit standardmäßig 440 Hz. `INT` verwendet B/B♭, `DE` H/B. Für mehrdeutige Eingaben die Konvention explizit setzen. Chromatische Transposition kann auch bei Verschiebung um null die enharmonische Schreibweise normalisieren. Diatonische Transposition legt Buchstabe und Oktave über die Stufenzahl fest und weist unpassende Halbtonwerte ab (seit 17.11.2026). |
| Intervalle, Dreiklänge, Septakkorde | [interval.py](../src/steps/theory/interval.py), [triad.py](../src/steps/theory/triad.py), [seventh.py](../src/steps/theory/seventh.py) | Berechnungen für klingenden Abstand und diatonische Intervalle, Akkordkonstruktion, Umkehrungen, Drop-2 und Shell-Voicings. |
| Akkordsymbole | [chord.py](../src/steps/theory/chord.py) | Explizit registrierte Qualitäten und Aliasse. `CM7` ist Dur, `Cm7` Moll. Slash-Bass ändert die tiefste Note, die Rezeptur bleibt vom Grundton abgeleitet. Theoretische und für ein Voicing ausgewählte Tonklassen können sich unterscheiden. `C11` ist aktuell nicht registriert. |
| Stufen und Transposition | [engine.py](../src/steps/progression/engine.py) | Stufenauflösung in vorgegebenem Dur-/Moll-Kontext, ausgewählte Sekundärfunktionen und Generalbassfiguren. Keine Tonarterkennung aus Audio oder Auswahl einer kontextabhängigen Analyse. `V7(alt)` wird abgewiesen. Der Vertrag für Mischformen wie `V7(6)` ist offen. |
| Stimmführung | [voice_leading.py](../src/steps/progression/voice_leading.py), [engine.py](../src/steps/progression/engine.py) | Standardsequenz mit durchgehender Stimmenzahl. Der Solver minimiert die Summe absoluter Halbtonbewegungen je Übergang innerhalb ±12 Halbtönen pro Stimme. Er prüft Tonklassen, Bass, MIDI 0–127 und Stimmenreihenfolge. Der strikte Modus prüft parallele Quinten und Oktaven sowie gleichartige reine Außenstimmenintervalle in Gegenbewegung. Unlösbare Vorgaben lösen `VoiceLeadingError` aus. Das Startlayout akzeptiert `CLOSE`, `DROP2`, `SHELL` und `ROOTLESS`. Folgeakkorde können andere Lagen haben. Vollständiger Kontrapunkt und Spielbarkeit bleiben eigene Abnahmen. |
| Progressionskatalog | [Historischer Katalog](../knowledge/concepts/progressions/CHORD_PROGRESSION_REFERENCE_LIBRARY.md), [App-Lernmaterial](../knowledge/concepts/progressions/REVIEWED_PROGRESSIONS.md) | Die allgemeine API bietet 28 Bestandsprogressionen. Für die [App-Schnittstelle](../app/knowledge.py) sind drei Pilotbeispiele fachlich freigegeben. App-Schnittstelle und Lernmaterial verwenden dieselbe [Datenbasis](../src/steps/progression/reviewed_progressions.json). Die [Abnahmeliste](../knowledge/benchmark/PILOT_ABNAHME.md) dokumentiert die Freigaben. |
| Recherche und Quellen | [Quellenregister](../knowledge/sources/README.md), [Ingestion](../knowledge/INGESTION_PIPELINE.md) | App-Adapter und Renderer lösen Quellen-IDs im Produktregister auf und prüfen die fassungsgebundenen Freigaben aller Pilot-Aussagen. CI führt denselben Validator aus. Forschungsclaims und Rohmedien werden über den App-Adapter nicht geladen. |
| Desktop, Audio, MIDI und Speicherung | [app](../app/README.md), [Architekturziel](architecture/ARCHITECTURE_OVERVIEW.md) | `app.main` startet einen CLI-/Headless-Pfad oder ein Tkinter-Fenster. `StepsMainWindow` bietet Akkord hinzufügen, ausgewählten Akkord ändern/entfernen/verschieben, Tonart-/Dur-Moll-/Tempo-/Taktart-Kontext setzen, pro Akkordereignis Startposition in `Takt:Zählzeit:Tick` sowie Dauer in Ticks bearbeiten, Transposition, Analyseanzeige, Undo/Redo, MIDI-Dateiauswahl/-Export sowie projektbezogene Öffnen-/Speichern-Dialoge mit Dirty-Prompt und Fehlerdialogen. Takt und Zählzeit sind 1-basiert, der Tick ist der nullbasierte Offset innerhalb der Taktart-Zählzeit; die Projektion nutzt PPQ und Taktart. Gespeichert und exportiert werden absolute Start-Ticks und positive Dauern in der aktiven PPQ-Auflösung. Eine Taktartänderung verändert nur die Projektion, nicht gespeicherte Ticks oder Dauern; Lücken und Überlappungen werden nicht aus der Progressionsreihenfolge hergeleitet. Der Kontext wird validiert und als eine Session-Aktion gespeichert. Session-Laden prüft Notation, Tonart, Modus, Taktart, Event-Timing und Akkordsymbole, bevor es den Zustand austauscht. Bei beschädigter Hauptdatei lädt die Storage-Schicht ein gültiges Backup und meldet diesen Zustand in der Desktop-Oberfläche; `load_project()` bleibt rückwärtskompatibel. Bedienfehler werden sichtbar abgewiesen. Headless-Tests decken die Actions ab; native Plattform-/Accessibility-Abnahme bleibt offen. SMF-Writer und -Parser sowie automatisierte Roundtrips sind vorhanden; unabhängige DAW-Abnahme ist separat zu belegen. Wiedergabe ist nach [ADR-007](../decisions/ADR-007-audio-nur-dateiexport-v01.md) nicht Teil von v0.1. |
| Internationalisierung | [Internationalisierungsvertrag](engineering/INTERNATIONALIZATION.md), [`app.i18n`](../app/i18n.py) und [Kataloge](../app/locales/) | PR #159 ergänzt `system`/`en`/`de`, System-Fallback, persistierte Benutzereinstellung, Laufzeitumschaltung im Hauptfenster sowie `--language` für die CLI. Katalogparität, Platzhalter, Persistenz, UI-Wechsel und Notationsunabhängigkeit sind automatisiert getestet; unabhängige Übersetzungs-, native Plattform- und Accessibility-Abnahme bleibt offen. Die UI-Sprache ändert `INT`/`DE` nicht. Siehe [#154](https://github.com/n05a-design/steps/issues/154). |

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

## Desktop-Prototyp und Produktgrenzen

Der bestehende Desktop-Einstieg ist mehr als ein theoretischer Architekturentwurf:
die Tkinter-Shell ist unter `app/ui/main_window.py` implementiert und
`tests/test_desktop_app_entrypoint.py` enthält einen GUI-Initialisierungstest,
der ohne Display übersprungen werden kann. Der Headless-CLI- und Controller-
Vertikalschnitt wird separat geprüft.

Das ist **kein** Nachweis für eine veröffentlichungsreife Desktop-App. PR #158
ergänzt Save/Open mit Rückfrage bei ungespeicherten Änderungen; PR #159 ergänzt
die MIDI-Dateiauswahl und Sprachumschaltung. Dieser Arbeitszweig verbindet
Hinzufügen, Ändern, Entfernen, Verschieben und Undo/Redo mit der UI und weist
ungültige Eingaben sichtbar ab. Die Bedienpfade sind headless getestet. Noch offen sind
native Accessibility-/Plattformprüfung, unabhängige Übersetzungsabnahme,
Wiederherstellungs- und Kompatibilitätsabnahme, Installer und Benutzerabnahme. Die
[1.0.0-Readiness-Matrix](product/V1.0.0_PRODUCT_CONTRACT.md#readiness-and-gap-matrix)
ordnet diese Lücken nach Status.

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
