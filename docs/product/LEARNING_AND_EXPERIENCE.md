# Didaktik, UX und Accessibility – eigenständige Qualitätssäule

**Evidenzstand:** Forschungsziel in den zwei Deep-Research-Papers und der konsolidierten Overview; Glide-Designregeln (`01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md`, bei `9e767bea`) sind technische Vorbilder. **Keine** empirischen Lernerfolgstests oder plattformübergreifende Steps-A11y-Abnahme vorliegend.

## 1. Lernmodell: Erklären ≠ Begriffe ausgeben

Eine Lehrfunktion hat die Kette **Wahrnehmen → ausprobieren → Vorhersage → Erklärung → Anwendung → Rückmeldung**. Pro Konzept werden erfasst: Begriff, Voraussetzungen, Lernziel, prototypisches Beispiel, gezielt kontrastierender Gegenfall, Fehlerbild, Stil-/Rahmenabhängigkeit und Quelle. Beispiel Zwischendominante: `E7→Am` als V7 in a-Moll gegenüber V7/vi in C-Dur. Der Nutzer wählt Tonalitätsannahme, statt eine „einzig richtige“ Deutung vorgesetzt zu bekommen.

| Niveau | Ziel | Interaktion | Nachweis |
|---|---|---|---|
| Einstieg | Dreiklang, Grundton, Tonart unterscheiden | Notenfarben + Hören (optional), einfacher Text | 5 Testfälle, weniger als 2 fachliche Fehlzuordnungen in beobachtetem Test |
| Vertiefung | Stufen, Funktionen und Borrowing verstehen | Alternativen umschalten, Wirkung und Kontext anzeigen | Gegenbeispiele samt Style/Key/Mode richtig |
| Anwenden | 4–8-taktige Folge variieren | Transposition, Taktlängen, Substitute | identischer Timeline-/MIDI-Roundtrip |
| Kritisches Verstehen | Grenzen von Funktionstheorie vs. Pop/Jazz/Modalität erkennen | mehrere Analyse-Frames, Quellen- und Unsicherheitskarte | keine unbelegten universellen Aussagen |

**Lernwirksamkeit nicht aus Klickzahlen ableiten.** Vorher-/Nachherfragen, zeitverzögerte Wiederholung und qualitative Fehleranalyse getrennt erfassen; Produktanalytik nur mit Datenschutzentscheidung, idealerweise offline und freiwillig.

## 2. Erklärungskarten – reproduzierbare Inhalte

Eine Erklärungskarte enthält `concept_id`, `claim_id`, `display_title`, `preconditions`, `illustration`, `counterexample`, `theory_framework`, `style_context`, `source_locators`, `review_status`, `last_reviewed` und verständlichen Text. **Kritisch:** `confidence:0.95` ohne Kalibrierungsdaten suggeriert Präzision, daher zunächst Belegstufen statt Pseudo-Wahrscheinlichkeiten. Bei fehlenden Quellen muss die UI *„fachliche Einordnung – Quelle nicht geprüft“* anzeigen und den Eintrag nicht als kanonisch ausgeben.

## 3. Wahrnehmung und Interaktion

- **Farben:** nicht allein semantisch; Akkordfunktion auch durch Symbol, Label und zugänglichen Namen kennzeichnen. Hell/Dunkel und niedrige Farbsättigung prüfen.
- **Text:** konkrete Schriftfamilien aus Glide nur nach rechtlicher Font-/Ressourcenprüfung; getrenntes Schriftgewicht und UI-Größe; responsives Umbruchverhalten unter 860×700, 1280×800 und hoher DPI.
- **Audio:** Audiohinweise nicht als einzige Information. Stummmodus und Gerät-ausgefallen dürfen die musikalischen Kernhandlungen nicht verhindern.
- **Bewegung:** respektiert Motion-reduction; keine Pflichtanimation; Fokus bleibt auch bei Übergang stabil.
- **Kurzbefehle:** jede Mausaktion (Navigation, Zeile, Transport, Undo, Speichern, Taktwechsel, Komponentenwahl) benötigt einen Tab-/Hotkey-/Menüpfad und gut sichtbare Fokusmarkierung.
- **Fehlerfeedback:** unterscheide ungültige Chordsymbole, unvollständige Eingaben und musikalisch *ungewöhnliche, aber mögliche* Beziehungen. Letzteres ist **kein** Syntaxfehler.
- **Mehrsprachigkeit:** DE H/B und internationale B/Bb-Notation als eigenständige Anzeigenpräferenz; Quellnotation bleibt erhalten. Sprache und Tonbenennung sind getrennte Einstellungen.

## 4. Einschränkungen von Tkinter

Glide hat dokumentierte UI-Komponenten, FocusOut-/Cocoa-Menü-/Dialogfallstricke und ein systematisches Testsystem. Das ist wertvolles Vorwissen, aber kein automatischer Nachweis für OS-Screenreader. Eine realistische native A11y-Untersuchung pro Plattform kann dazu führen, dass für bestimmte Accessibility-Ziele alternative Widgets oder langfristig ein anderer Toolkit-Adapter erforderlich sind. Das darf nicht mit „ein Tk-UI ist plattformübergreifend, also vollständig barrierefrei“ verwechselt werden. Python-Tkinter-Threading und Interpretergrenzen sind offiziell beschrieben: https://docs.python.org/3/library/tkinter.html .

## 5. Testmatrix (Anforderungen, keine bestandenen Fälle)

| ID | Versuch | Bestehende Evidenz | Offen |
|---|---|---|---|
| UX-01 | Akkord-Input per Tastatur ohne Maus, Enter/Escape/Undo | fachlicher Soll-Fall | echte Steps-UI fehlt |
| UX-02 | Sidebar expanded → compact → hidden → expanded | Glide-Verhalten dokumentiert | Isolation und Steps-Routing |
| UX-03 | Wechsel System/Dark/Light während Erklärung sichtbar | Glide-Designregeln | Steps-Regressionslauf |
| UX-04 | German H/B vs International B/Bb und Fehlermeldung | Theorievorlagen | Parser und Nutzerverständnis |
| UX-05 | gleiche Relation in a-Moll vs C-Dur | musikalisch erklärt | qualifiziertes Fachreview |
| UX-06 | Screenreader liest Route, Label, Status, Erklärung | kein Steps-Nachweis | native macOS/Windows/Linux-Läufe |
| UX-07 | Zoom 150–200 % / High DPI, keine verdeckten Controls | Glide-Snapshots als Referenz | Steps-Stichtagsbericht |
| UX-08 | reduzierte Bewegung, keine Fokusverluste | Glide-Designprinzip | actual Steps-Ausführung |
| UX-09 | Fehlende Audioausgabe bei funktionierendem MIDI-Export | Architekturvorschlag | Backend und Fehlerprobe |
| UX-10 | Übungsfrage mit falscher Antwort: korrekt, nicht beschämend, kein Faktenfehler | didaktische Spezifikation | Nutzer-/Fachtest |

## 6. Dokumentations- und Review-Vertrag

Jede Lernfunktion besitzt einen exemplarischen Nutzerablauf, Konzept-/Quellen-IDs, fachlichen Reviewer, Bedien- und Accessibility-Test, Dokumentationslink sowie eine explizite Negativprobe. Revisionsgründe nicht nur mit „verbessert“ dokumentieren, sondern fachliche Änderung (z. B. lokaler vs globaler tonaler Kontext), UX-Grund, Datum, Version und Testdelta. Kein datenbasierter Lernerfolg ohne tatsächlich ausgewertete Tests behaupten.
