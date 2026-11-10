# 04 — Vollständigerer Anforderungsraum, Scope und Nutzenmodell

## Vier unterschiedliche Produktebenen

| Ebene | Was sie ist | Was sie nicht ist | Vertrauensgrenze |
|---|---|---|---|
| Glide Produkt | Bestehende Offline-Desktop-App für Aufgaben, Planung, Seiten, Notizen, Pinnwände, Zeichnungen | Keine Musiktheorie-App; darf nicht zugunsten Steps amputiert werden | Eigene Produktdaten, Schemas, UI- und QA-Verträge |
| Shared Desktop Core (vorerst Konzept) | Wiederverwendbare **Mechanismen**: Shell, Navigation, Design, Settings, Commands, Userdata-Adapter, Lifecycle und Tests | Kein direkter Zugriff auf Glide-Aufgaben, Steps-Akkorde oder vom Projekt versteckte globale Pfade | API/Version/Port-Vertrag, Datenisolation, Lizenz-/Ressourcenmanifest |
| Steps Produkt | Eigenständiges Musikwerkzeug für **Chord-/Drum-Progressions, Harmonieexploration, MIDI-Export und Lernen** | Nicht bloße Umbenennung von Glide, nicht automatisch Full DAW | Eigene Domain/Daten-/App-Identität, eigene QA/Accessibility |
| Steps Forschung/Knowledge/Skill | Großes Research-Archiv + daraus gezielt verifizierte Knowledge/Concepts + AI-Workflows | Eine Datei in Git ist weder eine fachlich geprüfte Regel noch automatisch zur Publikation berechtigt | Provenienz, Lizenz, Beweiskette, Eval und Fachreview |

## Nutzer-/Zielgruppenhypothesen

Die historischen Berichte nennen Anfänger, fortgeschrittene Musiker, Songwriter, Lehrkräfte und Producer. **Keine neue aktuelle Nutzerforschung** belegt Größe, Zahlungsbereitschaft, Barrieren oder tatsächliche Priorität dieser Gruppen. Diese Persona-Hypothesen sind daher keine freigegebene Marktstrategie. Für den ersten funktionierenden Vertical Slice sind zwei Jobs-to-be-done sinnvoll: (A) Akkordfolge erzeugen/analysieren/verändern und die Änderung speichern; (B) eine rhythmische Folge im Sequencer bearbeiten und mit einem validierbaren MIDI-Export kombinieren. Der didaktische Nutzen sollte an überprüfbaren Erklärungen statt generischen KI-Beschreibungen sichtbar werden.

## Funktionsanforderungen aus aktuellem Nutzerwunsch (verbindlich als Ziel, nicht Umsetzung)

**Desktop-Grundgerüst:** Äußere Oberfläche aus Glide als Baseline behalten: sichtbarer und einklappbarer Seitenleistenbereich, vollständiges Verbergen/Wiedereinblenden, Liste von Navigationspunkten ohne alte Glide-Task-Kommandos, Kopf mit Logo/Titel/Untertitel, Symbolaktionen, Such-/Bearbeitungsfelder, Einstellungen, Typografie, Farbrollen, globale Prozess-/Fehlermeldungen, gespeicherte UI-Preferences, Tastaturbefehle, Zugänglichkeit, Größen- und DPI-Verhalten. Zwei gewünschte 'Fenster' müssen getrennt spezifiziert werden. Die Menüstruktur darf nicht nur dekorativ wirken: Nicht freigegebene Kommandos müssen als deaktiviert begründet oder bewusst entfernt werden, ohne versteckte alte Mutation.

**Shared Core:** Wiederverwendung muss bidirektional möglich sein — eine Kernänderung später in Glide **und** Steps mit explizitem Paketupdate integrieren; keine automatische rückwirkende Übernahme jeder Glide-App-Änderung. Entwickler müssen nachvollziehen, welcher Core-Commit/API-Zweig, welche Ports, Ressourcen, Testverträge und OS-Grenzen in welcher App verwendet werden.

**Steps Domäne:** Akkordfolgen und Drumfolgen als unabhängige, optional synchronisierte Objekte; Tonart/Modus, enharmonische Schreibweise, Voicings, Harmonic Rhythm, Takt/Tempo/Patternlänge, Timeline und Takte, Tempo-/Positionsmodell, Undo/Redo, Import/Export, MIDI-Metadaten und Versionierung. Speichern/Öffnen und Export im Offline-Betrieb. Musiktheoretische Erklärungen mit Kontext- und Mehrdeutigkeitsangaben. Dynamische Vorschlagslisten und Erklärungen benötigen nachvollziehbare Regel-/Datenquellen.

**Knowledge:** Alle Originalquellen inventarisieren, Quellrechte trennen, mehrere historische Forschungsstände verlinken, keine belastbaren Erkenntnisse verlieren; verifizierte Aussagen in konzeptuell kanonische Records überführen; Skill als selektiver Zugriff und kein paralleles Lehrbuch. Fachliche Korrekturen müssen durch Tests/Referenzen und Quell-ID nachvollziehbar werden.

**Prozess:** AI-Agenten nach eindeutigen Verantwortlichkeiten und getrennten Worktrees einsetzen; Ausgaben mit SHA, Diffs, echten Testbefehlen, Plattform, Skips und Human-Gate übergeben. Bestehendes Glide-3.53-Projekt parallel durch Copilot stabilisieren, ohne Steps-Rewrite im selben Workspace.

## Nichtfunktionale Anforderungen, die funktional mitentscheiden

- Offline-first und vollständige Datenkontrolle, kein stilles Netz, keine fremden Datendateien öffnen.
- Atomarer Commit, Lock-Semantik, Backup/Restore, Schema-Migration, beschädigte Daten und unterbrochene Prozesse; nicht nur 'Datei schreiben'.
- Klarer Ownership-Pfad für UI-, Domain-, Settings-, Undo- und Cachezustand. Stabile IDs und UI-Projektionen nach Undo/Import/Restart.
- Tk-Hauptthread für Widgetzugriffe, `after`-Token-Verwaltung, kein toter Interpreter, kein doppelter Eventhandler, Fokus/Modality, DPI/Mehrmonitor.
- Plattformmatrix Win/macOS/Linux, Python-/Tk-Build, Bundling, Font-/Icon-Lizenzen; keine Verwechslung von CI-Runner mit menschlicher Hardwareabnahme.
- Accessibility: Tastatur zuerst, Screenreader-Semantik soweit native Plattform unterstützt, kontraststabile Rollen, Beschriftung und skalierte Eingabeflächen; fehlende Readerunterstützung als Grenze.
- Langfristige Wartung: kleiner API-Oberflächenbereich, Deprecations, Regressionstests, Backports, Distribution ohne Live-Netz, Handbuch und Changelog.

## Scope- und Prioritätsgrenzen

**Zielprodukt:** Chord + Drum + MIDI + Theorie ist der ausdrücklich benannte Gesamtauftrag. **Erster Vertical Slice** ist als Technikexperiment eine neutrale Shell und **eine** durchgängige Datenaktion. **MVP** ist erst durch Nutzerentscheidung definiert. Aussagen alter Handovers über spätere Drums bezogen sich auf damalige Research-Priorität; weder V1 noch V2 darf das Produktziel ohne Freigabe kürzen.

**Nicht automatisch Teil des MVP:** Cloudkonten, Onlinedienste, vollständige DAW, Studioeffekte, Sampling-Engine, Echtzeit-Audio mit garantierter Latenz, MusicXML-Export, ML-Modelltraining, Community-Server, Lizenzdownloads im Installer, Notion-Aufgaben und Kalender. Solche Erweiterungen als ADR mit Nutzerwert/Kosten/Sicherheitsfolgen bewerten.

## Nutzerflussbasierte Abnahmeszenarien (Mindestumfang)

1. **Neustart ohne Glide-Datenkontakt:** Steps startet bei absichtlich ungültigem Glide-Produktordner; legt nur eigene Pfade an. Navigation und Einstellungen funktionieren offline.
2. **Layout-Beharrung:** Seitenliste sichtbar → eingeklappt → verborgen → wieder sichtbar, jeweils aktive Seite, Scrollposition und Fokusrückkehr nachvollziehbar; nach App-Neustart erwartete Preferences.
3. **Pane-Interaktion:** Inhalt in Fläche 1 auswählen; Fläche 2 öffnen/ersetzen/schließen; nach schnellem Wechsel keine alten Callbacks oder unbenutzte weiße Restfläche.
4. **Akkord-Workflow:** Tonart/Notation wählen, zwei Akkorde erstellen, einen verändern, speichern, Neustart, Undo/Redo; alternative Lesart explizit statt 'richtig/falsch'.
5. **Rhythmus-Workflow:** 4/4, zwei Pattern mit Step-Offsets und Velocity erzeugen; Tempo setzen und quantisierte vs. expressive Wiedergabe/Export unterscheiden; Roundtrip-Dauer unverändert.
6. **MIDI-Workflow:** Gleicher PPQ-Wert, Tempo- und Time-Signature-Metaevent; Tick-/Beatlängen, Kanal, Percussion-Kanal 10 (MIDI 1.0 Zählweise), Note-Off-Reihenfolge, nichtnegative Delta-Zeiten; Import-Roundtrip bis auf dokumentierte Informationsverluste.
7. **Fehlerpfade:** Dateisystem voll, Schreiblock verloren, korrupte Schema-Version, fehlende Schrift, deaktivierter MIDI-Port, Benutzer-Exit im laufenden Callback, nicht vorhandene Quelle; keine stillen Änderungen.
8. **Barrierefreiheit:** Voller Keyboard-Flow bei 125–200 % Skalierung und schmaler Fensterbreite; Aktionen semantisch beschriftet und nicht nur über Symbolfarbe unterscheidbar.
9. **Lizenz- und Provenienzfluss:** Erklärung mit Quellen-ID, Rechteklasse und zwei möglichen Theorielesarten, ohne nicht freigegebene Volltexte in Output oder Bundle.

## Entscheidungsspezifische Akzeptanz

Im Repository `audit/REQUIREMENTS.csv` stehen zusätzliche Anforderungen mit Quellankern, Scope-/Schnittstellenbezug, Priorität und explizitem Abschlussnachweis. `USER_REQUIREMENT` ist eine starke Aussage über **gewünschtes** Verhalten, aber kein Test einer vorhandenen Implementation. Eine neue Produktentscheidung ist erst `ACCEPTED`, wenn der Projektverantwortliche sie ausdrücklich bestätigt oder ein dokumentierter früherer Beschluss nachweisbar gilt.
