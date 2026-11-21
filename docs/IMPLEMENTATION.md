# Implementierungsstand von STEPS

Dieser Leitfaden beschreibt den Code im selben Checkout. Der Einstieg für
Entwicklung ist die [Root-README](../README.md). Die [API-Referenz](theory/API.md)
wird aus den exportierten Python-Objekten erzeugt. Der am 20.11.2026 geprüfte
`main`-Stand ist Commit
[`e2faf276adf6d65caf81fe28f38521a176e0c283`](https://github.com/n05a-design/steps/commit/e2faf276adf6d65caf81fe28f38521a176e0c283);
der letzte Implementierungskommit ist
[`e2faf276adf6d65caf81fe28f38521a176e0c283`](https://github.com/n05a-design/steps/commit/e2faf276adf6d65caf81fe28f38521a176e0c283),
PR [#220](https://github.com/n05a-design/steps/pull/220).
Die historische Produkt-Baseline bleibt [`b67294a5161b42d281be4afdea5bb74b7385a786`](https://github.com/n05a-design/steps/commit/b67294a5161b42d281be4afdea5bb74b7385a786).
PRs #158–#163 ergänzen Save/Open, Lokalisierung,
Akkordbearbeitung, Neuordnung, Undo/Redo sowie Tonart-/Dur-Moll-/Tempo-Kontext.
PR #164 ergänzt editierbare Taktart sowie Start-Ticks und Dauern pro
Akkordereignis; PR #165 ergänzt die bar:beat:tick-Projektion, PR #166 die
Backup-Recovery-Meldung, PR #167/#168 den Migrationsstatus samt Desktop-Hinweis
PR #169 die editierbare Projektbezeichnung, PR #170 „Neu“ mit
Dirty-State-Rückfrage und sauberem Session-Reset sowie PR #176–#179 native UI-
und Packaging-Gates einschließlich Wheel-Bau/-Installation. PR #180/#181
halten den kanonischen Dokumentations- und Baseline-Stand konsistent.
Nach dieser unveränderlichen Baseline ergänzt PR #190 die Validierung und
Normalisierung ungültiger Projekt-Zeiteinstellungen unter der dokumentierten
Migration `MIG-006 normalize-time-settings`. PR #191 synchronisiert diesen
Merge-Stand mit dem kanonischen Dokumentationsbestand. PR #197 ergänzt den
Next-Chord-Explorer, PR #198 das Laden freigegebener Reviewed-Progressionen,
PR #199 die Stimmführungsstil-Auswahl und PR #200 die dokumentierte
Wheel-/Laufzeit-Ressourcenprüfung. PR #201 synchronisierte den damaligen
Dokumentationsstand. PR #203 richtet den Desktop-Sessionexport an ADR-017 aus,
PR #204 erzwingt die vier Akkordstimmen, PR #205 ergänzt optionale DROP2- und
ROOTLESS-Voicings, 95%-Notenlänge und SMF Format 0. PR #206 prüft zehn
SHA-256-Goldenexporte zusätzlich mit dem unabhängigen `SMFParser`. PR #220
vollendet den Desktop-Export- und Reviewpfad, einschließlich lokalisiertem
Exportstudio, Fehlerbehandlung und Controller-/Session-Anbindung.
Bei Commit `e2faf276adf6d65caf81fe28f38521a176e0c283` bestehen 791
automatisierte Tests; diese Zahl ist ein Testnachweis, keine Freigabe für
native Plattformen, Übersetzung, Accessibility oder DAW-Abnahme.
Gespeichert und exportiert
werden weiterhin absolute Tickwerte. Implementierung, Test, fachliche Abnahme
und Veröffentlichung sind getrennte Statusangaben.

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
| Stimmführung | [voice_leading.py](../src/steps/progression/voice_leading.py), [engine.py](../src/steps/progression/engine.py) | Standardsequenz mit durchgehender Stimmenzahl. Der Solver minimiert die Summe absoluter Halbtonbewegungen je Übergang innerhalb ±12 Halbtönen pro Stimme. Er prüft Tonklassen, Bass, MIDI 0–127 und Stimmenreihenfolge. Der strikte Modus prüft parallele Quinten und Oktaven sowie gleichartige reine Außenstimmenintervalle in Gegenbewegung. Unlösbare Vorgaben lösen `VoiceLeadingError` aus. Das Startlayout akzeptiert `CLOSE`, `DROP2`, `SHELL` und `ROOTLESS`. Folgeakkorde können andere Lagen haben. Das Desktop-Stimmführungslabor zeigt zwei unabhängig wählbare Stile mit denselben Tick- und Tonhöhenachsen. Die Noten stammen aus der tatsächlich ausgewerteten Voicing-Folge. Die Auswahl eines Akkordereignisses markiert dessen Zeitspanne in beiden Piano-Rolls. Sie übernimmt beim Öffnen die Auswahl aus der Progression. Das Ereignis lässt sich im Ausklappfeld oder durch Klick auf eine Note wählen. Links und Rechts wechseln im fokussierten Ausklappfeld das Akkordereignis oder die Zoomstufe. Der gemeinsame Zeitzoom mit 1×, 2×, 4× und 8× zentriert den Ausschnitt auf das gewählte Ereignis, soweit die Projektgrenzen es zulassen. Die Achse zeigt dabei absolute Projekt-Ticks. Die Tonhöhenachse reduziert bei großem Umfang die Anzahl der Beschriftungen, damit MIDI-Notennummern lesbar bleiben. Die Vorschauen nennen den MIDI-Tonumfang und pro Übergang die vorzeichenbehaftete Bewegung je Stimme von tief nach hoch. Bei unterschiedlicher Stimmenzahl weist die Vorschau auf die fehlende Zuordnung hin. Erkannte Parallelen und Gegenbewegungen erscheinen mit Intervall und betroffenen Stimmen in der UI-Sprache. Erst die ausdrückliche Anwendung speichert den Stil als undo-/redo-fähige Aktion. Bewegungswerte sind beschreibende Metriken, keine allgemeingültige Rangfolge. Vollständiger Kontrapunkt und Spielbarkeit bleiben eigene Abnahmen. |
| Progressionskatalog | [Historischer Katalog](../knowledge/concepts/progressions/CHORD_PROGRESSION_REFERENCE_LIBRARY.md), [App-Lernmaterial](../knowledge/concepts/progressions/REVIEWED_PROGRESSIONS.md) | Die allgemeine API bietet 28 Bestandsprogressionen. Für die [App-Schnittstelle](../app/knowledge.py) sind drei Pilotbeispiele fachlich freigegeben. Die Desktop-Bibliothek verknüpft mehrere Suchwörter aus den Beispielen und ihrer Provenienz. Beim Filtern bleiben eine weiterhin sichtbare Auswahl und ihre Leseposition erhalten. Die Akkordvorschau zeigt Referenztonart und ordnet den veröffentlichten Akkordsymbolen ihre Stufen zu. Die Textvorschau zeigt Claim-Texte unverändert zusammen mit Geltungsbereich, Gegenprüfung, Quellenfundstellen, Review-Konto und Freigabebeleg. Das Menü „Quellen und Freigabebelege“ öffnet die registrierten Links des ausgewählten Beispiels im Standardbrowser. Von der Vorschau aus erreicht Tab das Menü und die Leertaste öffnet es. Das Laden erzeugt erst nach ausdrücklicher Auswahl ein unabhängiges Projekt und behält die Dirty-State-Rückfrage bei. UI-Texte sind EN/DE lokalisiert; Claims werden nicht übersetzt oder neu freigegeben. App-Schnittstelle und Lernmaterial verwenden dieselbe [Datenbasis](../src/steps/progression/reviewed_progressions.json). Die [Abnahmeliste](../knowledge/benchmark/PILOT_ABNAHME.md) dokumentiert die Freigaben; die Bibliothek erweitert den freigegebenen Umfang nicht. |
| Recherche und Quellen | [Quellenregister](../knowledge/sources/README.md), [Ingestion](../knowledge/INGESTION_PIPELINE.md) | App-Adapter und Renderer lösen Quellen-IDs im Produktregister auf und prüfen die fassungsgebundenen Freigaben aller Pilot-Aussagen. CI führt denselben Validator aus. Forschungsclaims und Rohmedien werden über den App-Adapter nicht geladen. |
| Desktop, Audio, MIDI und Speicherung | [app](../app/README.md), [Architekturziel](architecture/ARCHITECTURE_OVERVIEW.md), [Projekt-Schema-Migration](architecture/PROJECT_SCHEMA_MIGRATION.md) | `app.main` startet einen CLI-/Headless-Pfad oder ein Tkinter-Fenster. Die Desktop-Kontextleiste zeigt die musikalische `INT`/`DE`-Notationskonvention getrennt von der UI-Sprache. Eine Umstellung wird bestätigt und konvertiert Tonart sowie Akkordsymbole explizit; Event-Ticks, Tempo, Taktart und Projektstruktur bleiben unverändert. `StepsMainWindow` bietet eine neue Standard-Progression mit Dirty-State-Rückfrage, Akkord hinzufügen, ausgewählten Akkord ändern/entfernen/verschieben, Tonart-/Dur-Moll-/Tempo-/Taktart-Kontext setzen, pro Akkordereignis Startposition in `Takt:Zählzeit:Tick` sowie Dauer in Ticks bearbeiten, Transposition, Analyseanzeige inklusive Beginner-Keyboard-Voicings und Stimmführungsübergängen, Undo/Redo, ein lokalisiertes MIDI-Exportstudio mit Voicing-, Notendauer- und SMF-Formatwahl sowie projektbezogene Öffnen-/Speichern-Dialoge mit Dirty-Prompt und Fehlerdialogen. Takt und Zählzeit sind 1-basiert, der Tick ist der nullbasierte Offset innerhalb der Taktart-Zählzeit; die Projektion nutzt PPQ und Taktart. Gespeichert und exportiert werden absolute Start-Ticks und positive Dauern in der aktiven PPQ-Auflösung. Eine Taktartänderung verändert nur die Projektion, nicht gespeicherte Ticks oder Dauern; Lücken und Überlappungen werden nicht aus der Progressionsreihenfolge hergeleitet. Der Kontext wird validiert und als eine Session-Aktion gespeichert. Session-Laden prüft Notation, Tonart, Modus, Taktart, Event-Timing und Akkordsymbole, bevor es den Zustand austauscht. Bei beschädigter Hauptdatei lädt die Storage-Schicht ein gültiges Backup und meldet diesen Zustand in der Desktop-Oberfläche; `load_project()` bleibt rückwärtskompatibel. 0.x- und 1.x-Projektstände werden über dokumentierte Migration-IDs normalisiert, höhere Major-Versionen werden abgewiesen und fehlende Projekttitel bleiben Fehler. Bedienfehler werden sichtbar abgewiesen. Headless-Tests decken die Actions ab; native Plattform-/Accessibility-Abnahme bleibt offen. SMF-Writer und -Parser sowie automatisierte Roundtrips sind vorhanden; unabhängige DAW-Abnahme ist separat zu belegen. Wiedergabe ist nach [ADR-007](../decisions/ADR-007-audio-nur-dateiexport-v01.md) nicht Teil von v0.1. |
| Internationalisierung | [Internationalisierungsvertrag](engineering/INTERNATIONALIZATION.md), [`app.i18n`](../app/i18n.py) und [Kataloge](../app/locales/) | PR #159 ergänzt `system`/`en`/`de`, System-Fallback, persistierte Benutzereinstellung, Laufzeitumschaltung im Hauptfenster sowie `--language` für die CLI. Katalogparität, Platzhalter, Persistenz, UI-Wechsel und Notationsunabhängigkeit sind automatisiert getestet; unabhängige Übersetzungs-, native Plattform- und Accessibility-Abnahme bleibt offen. Die UI-Sprache ändert `INT`/`DE` nicht. Siehe [#154](https://github.com/n05a-design/steps/issues/154). |

Der Next-Chord-Explorer zeigt Relationsart, theoretischen Rahmen, Quelle und
Erklärung als interpretative Empfehlung, nicht als kanonisch geprüften Fakt.
Die Übernahme bleibt gesperrt, bis ein gültiger Kandidat ausgewählt ist.

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

Beim Öffnen und Speichern übersetzt STEPS Fehler des Dateidialogs und
typische Dateifehler. Wiederherstellung gilt auch bei fehlerhafter
UTF-8-Kodierung. Nach erfolgreicher Wiederherstellung nennt der Dialog die
Sicherung und weist auf Speichern und Speichern unter hin. Wird eine neuere
Schemafassung abgewiesen, behält das aktive Projekt seinen Pfad und seine
Undo-Historie.

Bibliothek, Stimmführungslabor und MIDI-Export binden den Fokus an ihren
Dialog und geben ihn beim Schließen an das zuvor fokussierte Feld zurück.
Die Projektkürzel wirken im Hauptfenster. Bibliotheksvorschau und
Stimmführungsdetails sind per Tab erreichbar und mit Bild auf und Bild ab
scrollbar.

Die Progressionsliste zeigt zu jedem Akkord den Start in Takt, Zählzeit und
Tick sowie die Dauer in Ticks. Im Startfeld lässt sich alternativ eine
absolute Tickzahl ab null eingeben. Nach dem Übernehmen erscheint wieder
Takt:Zählzeit:Tick. Startfehler nennen die Grenzen der aktuellen Taktart.
Start- oder Dauerfehler wählen den Inhalt des betroffenen Feldes zur
Korrektur aus. Escape in einem der Timing-Felder stellt beide gespeicherten
Werte wieder her. Eine erneute Eingabe derselben Werte ändert die Historie
und den aktiven Akkordvorschlag nicht. Beim Hinzufügen und Verschieben scrollt die
Liste zur ausgewählten Zeile. In der fokussierten Liste verschieben
Wahltaste+Auf/Ab (macOS) oder Alt+Auf/Ab (Windows/Linux) das Akkordereignis
um eine Zeile. Sein absoluter Start und seine Dauer bleiben am Ereignis.
Ein Sprachwechsel übersetzt die Zeilen und bewahrt Auswahl, Scrollposition
sowie unfertige Eingaben.
Im Menü „Akkord“ erzeugt „Duplizieren“ eine Kopie mit derselben Dauer direkt
nach dem Ende des ausgewählten Ereignisses. Andere Start-Ticks bleiben
erhalten. So kann die Kopie ein benachbartes Ereignis überlappen.
„In der Mitte teilen“ erzeugt zwei direkt aufeinanderfolgende Ereignisse
mit demselben Akkordsymbol. Bei ungerader Dauer erhält der zweite Teil
den zusätzlichen Tick. Ereignisse mit einem Tick können dupliziert werden.
Beide Aktionen wählen die neue Zeile aus und belegen je einen Undo-Schritt.
Mit fokussierter Liste stehen Cmd+D und Cmd+T auf macOS sowie Ctrl+D und
Ctrl+T auf Windows und Linux zur Verfügung. Die
[ProgressionSession](../src/steps/progression/session.py) kapselt beide
Änderungen als Funktionen für den Controller.

Die Anfänger-Voicings berechnen die beste Folge iterativ und verwenden
bereits berechnete Teilpfade. Bewegungsmaß und Auswahl bei Gleichstand
folgen derselben Regel wie zuvor.

Der native MIDI-Dateidialog schlägt den Projekttitel als Dateinamen vor. Beim
ersten Export öffnet er für gespeicherte Projekte deren Ordner. Weitere
Exporte im selben Projekt öffnen den zuletzt erfolgreich verwendeten Ordner,
solange er verfügbar ist. Ein Projektwechsel setzt die Ordnerauswahl zurück.

Der Harmonie-Inspektor verwendet für Grund- und Skalentöne die Projektnotation.
Anfänger-Voicings behalten auch bei reduzierten Akkordsymbolen die gewählte
Schreibweise. Die Oberfläche zeigt gemeinsame Töne, Gesamtbewegung und
größten Sprung in EN/DE. Der ursprüngliche didaktische Hinweis bleibt als
Originaltext gekennzeichnet.

Bei Skalen zeigt der Inspektor eine Tonmengenprüfung. Die am Akkordgrundton
gebildete Skala muss alle theoretischen Akkordtöne und einen expliziten
Slash-Bass enthalten. Liegen benötigte Vorzeichen außerhalb des unterstützten
Schreibbereichs, weist der Inspektor darauf hin. Die Eignung für eine konkrete
Tonart und einen Stil ist eine zusätzliche musikalische Entscheidung. Die Anfängeransicht benennt für jede rechnerisch
bewegte Stimme der rechten Hand den Ausgangs- und Zielton und die vorzeichenbehaftete
Halbtonbewegung. Gemeinsame Tonhöhen in zwei Voicings und liegenbleibende
Stimmen sind unterschiedliche Messgrößen. Historische Originalhinweise aus
dem Pop-Beispiel behalten ihre Kennzeichnung.


Der Next Chord Explorer zeigt pro ausgewähltem Kandidaten die EN/DE-Beziehung,
die Originalerklärung und deren Provenienz. Beim Öffnen liegt der Fokus auf
dem ersten Vorschlag. Pfeiltasten wechseln die Vorschau, Enter oder
„Auswahl hinzufügen“ fügt den Akkord ein und fokussiert die Progression. Mit
Umschalt+Tab ist die schreibgeschützte Begründung erreichbar. Beim Wechsel
der Oberflächensprache bleibt die Auswahl erhalten, solange Projekt und
Ausgangsakkord unverändert sind. **Auswahl vergleichen** hält einen
Kandidaten fest und zeigt bei Auswahl eines anderen Kandidaten beide
Beziehungen, Begründungen und Provenienzen in der Vorschau. Der Vergleich
übersteht einen Sprachwechsel im selben Kontext. Ein Projekt- oder
Ausgangsakkordwechsel verwirft ihn. Einfügen bleibt an die aktuelle
Listenauswahl gebunden. Die Anwendung
prüft bei identischem Akkordsymbol auch den konkret gewählten Vorschlag.
Die MIDI- und Projektformate folgen denselben Verträgen.

Der bestehende Desktop-Einstieg ist mehr als ein theoretischer Architekturentwurf:
die Tkinter-Shell ist unter `app/ui/main_window.py` implementiert und
`tests/test_desktop_app_entrypoint.py` prüft GUI-Initialisierung, Tastenkürzel
und den Save/Open/MIDI-Exportpfad mit echten Session- und Controller-Objekten.
Außerhalb des strikten Smoke-Modus darf ein fehlendes Display den Test
überspringen; die CI-Smoke-Jobs setzen `STEPS_REQUIRE_DESKTOP_TK=1` und schlagen
bei fehlendem Tk fehl. Ubuntu nutzt Xvfb; Windows und macOS nutzen eigene Runner.
Diese Runner-Konfiguration ersetzt keine menschliche Accessibility- oder
Plattformabnahme.

Das ist **kein** Nachweis für eine veröffentlichungsreife Desktop-App. PR #158
ergänzt Save/Open mit Rückfrage bei ungespeicherten Änderungen; PR #159 ergänzt
die MIDI-Dateiauswahl und Sprachumschaltung. Dieser Arbeitszweig verbindet
Hinzufügen, Ändern, Entfernen, Verschieben und Undo/Redo mit der UI und weist
ungültige Eingaben sichtbar ab. Die Bedienpfade sind headless getestet. Noch offen sind
native Accessibility-/Plattformprüfung, unabhängige Übersetzungsabnahme,
Wiederherstellungs- und Kompatibilitätsabnahme, Installer und Benutzerabnahme. Die
[1.0.0-Readiness-Matrix](product/V1.0.0_PRODUCT_CONTRACT.md#readiness-and-gap-matrix)
ordnet diese Lücken nach Status.

`ProgressionSession.export_midi_file()` verwendet den ADR-017-Export mit
Conductor-, Chords- und Bass-Spur. Die Akkordspur enthält genau vier
CLOSE-Stimmen im Bereich MIDI 48–72; Dreiklänge werden mit dem Grundton
verdoppelt, Erweiterungsakkorde verwenden Grundton, Terz, Septime und die
höchste Erweiterung. Ein Slash-Bass wird separat auf der Bassspur ausgegeben.
Tempo, Taktart, passende Dur-/Moll-Tonartmetadaten und individuelle
Event-Startzeiten/-Dauern bleiben erhalten; deutsches `B` und `H` bleiben
getrennte Tonarten. Zehn SHA-256-Golden-Fälle prüfen den Session-Export auch
mit dem separat implementierten `SMFParser`; das ersetzt keine DAW-Abnahme.
Der Widget-Test speichert und öffnet ein Projekt über die native Tk-Verkabelung und prüft Bibliothek, Akkordvorschlag, Stilvergleich und SMF-Format 0. Der ergänzende Installations-Smoke verifiziert die Ressourcen aus dem Wheel und der [macOS-Entwicklungsbuild](../tests/native_ui/README.md) ergänzt den lokalen Start über ein App-Bundle. Unabhängige DAW-Importe sind weiterhin
nicht belegt. Das [DAW-Prüfprotokoll](quality/MIDI_DAW_MANUAL_PROTOCOL.md)
liefert einen Generator mit SHA-256-Manifest für sechs reproduzierbare
Importdateien einschließlich überlappender Einsätze in SMF 0 und 1.
Das lokalisierte MIDI-Exportstudio reicht optionale `CLOSE`/`DROP2`/`ROOTLESS`,
`FIXED_GAP`/`PERCENT_95` und SMF-Format-0/1-Einstellungen über Controller und
Session an denselben ADR-017-Exporter weiter. Die bisherigen CLOSE-/10-Tick-/
Format-1-Standards gelten, wenn CLOSE für die Progression verfügbar ist.
Die Voicing-Prüfung verwendet dieselbe Tonhöhenauswahl wie der Exporter.
Das Optionsfenster deaktiviert inkompatible Modi und nennt jeweils den ersten
blockierenden Akkord. Es prüft die Auswahl erneut vor der Dateiauswahl.
Die Timing-Vorschau verwendet die absoluten Start-Ticks und die tatsächlich
exportierten Notenlängen für das gewählte Voicing. Sie zählt jeden Einsatz,
der vor dem Ende einer vorherigen Note mit gleicher MIDI-Tonhöhe und
gleichem Kanal beginnt, und nennt den ersten betroffenen Tick. Gleichzeitige
Einsätze zählen ab der zweiten Note. Treffen Ende und nächster Start auf
demselben Tick zusammen, zählt der Einsatz als überlappungsfrei. Die Vorschau
ist informativ. Die Exportdatei folgt weiterhin ADR-017.
Der Exporter schreibt die vollständige MIDI-Datei zunächst in ein temporäres
Verzeichnis im Zielordner und ersetzt das Ziel erst nach einem erfolgreichen
Schreibvorgang. Bei einem Schreib- oder Ersetzungsfehler bleiben die vorhandenen
Dateibytes erhalten. Der Dialog beschreibt Dateifehler in EN/DE und bleibt für
einen weiteren Versuch geöffnet. Type 0 führt alle
exportierten Inhalte in einer Spur zusammen. Dies ist ein automatisierter
Desktop-Exportpfad, keine unabhängige DAW- oder Accessibility-Abnahme.
Der Projekt-Exporter interpretiert Textpayloads nur auf `CHORDS`-Spuren als
Akkordsymbole; fehlerhafte Akkordsymbole werden nicht still ausgelassen,
sondern werfen den Akkordfehler. Listen- und Einzelnoten-Payloads müssen
Ganzzahlen im MIDI-Bereich 0–127 enthalten; ungültige Noten erzeugen einen
Exportfehler statt eines unvollständigen Exports. Text auf `ANNOTATIONS`-Spuren
wird ignoriert.

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
