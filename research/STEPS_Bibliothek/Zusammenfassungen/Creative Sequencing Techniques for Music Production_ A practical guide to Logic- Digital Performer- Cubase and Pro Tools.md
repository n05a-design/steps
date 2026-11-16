---
werk: "Creative Sequencing Techniques for Music Production – A practical guide for Logic, Digital Performer, Cubase and Pro Tools"
autor: "Andrea Pejrolo"
verlag: "Focal Press (Imprint von Elsevier), Oxford / Burlington MA; First published 2005; © 2005 Andrea Pejrolo"
isbn: "0-240-51960-4"
seiten: 324   # PDF-Seiten, nicht Buchumfang
quelle_pdf: "research/STEPS_Bibliothek/Creative Sequencing Techniques for Music Production_ A practical guide to Logic- Digital Performer- Cubase and Pro Tools.pdf"
quelle_sha256: 7cc3a0bfc9f83d060eb8efb708ddb01af1c5e8c53bd2565cdf72acb4df1704d9
rechteklasse: E
original: restricted_local (per .gitignore ausgeschlossen)
grundlage: "Docling-Extrakt vom 14.11.2026; vollständige Gliederung, Abschnitte zu Quantisierung und Groove gelesen; korrigiert am 15.11.2026 nach PRUEFBERICHT.md; Einzelstellen am Original-PDF nachgeprüft am 16.11.2026"
stand: 2026-11-16
fachliche_freigabe: false
---

# Andrea Pejrolo: Creative Sequencing Techniques for Music Production (2005)

> Zusammenfassung in eigenen Worten. Die Programmversionen im Buch sind Stand 2005: Logic Pro (LP), Digital Performer (DP), Cubase SX (CSX) und Pro Tools (PT).

## Einordnung

Ein praxisorientiertes Lehrbuch für MIDI- und Audio-Sequencing im Projektstudio. Es erklärt Techniken programmunabhängig und zeigt sie jeweils in den vier damals führenden DAWs. Zum Buch gehörte laut Rückseite eine CD-ROM mit MIDI-Dateien, Samples und Beispieltracks sowie Software-Demos. Der Anhang listet die Beispiele nach CD-Track. Jedes Kapitel endet mit Zusammenfassung und Übungen.

## Gliederung und Kerninhalte

### 1. Studio-Grundlagen und MIDI
- Projektstudio und Ausstattung.
- **MIDI-Nachrichten:** Channel Voice, Channel Mode, System Real-Time, System Common, System Exclusive.
- Geräte: Synthesizer, Keyboard-Controller, Klangmodul, Sequencer. Vernetzung in Daisy-Chain- und Sterntopologie.
- Audio: Mischpult, Monitore, Rechner, Audiointerface, Ein- und Ausgänge.
- Kriterien für die DAW-Wahl (Ziele, Lernkurve, Funktionen, Rechner) und Budget.

### 2. Grundlegende Sequencing-Techniken
- Funktionsweise und Organisation eines Sequencers, MIDI- und Audiospuren, Projektorganisation.
- Klick und Tempo, MIDI-Aufnahme.
- **Editoren:** grafisch (Piano-Roll), Liste (Event-Liste), Noten. Undo-Tiefe.
- Grundlagen der Quantisierung. Destruktive und nichtdestruktive Audiobearbeitung.
- Automation: statisch, in Echtzeit, Bearbeitung. Lautstärke, Panorama, Mute.

### 3. Techniken für die Mittelstufe
- **Groove-Quantisierung und Humanisierung:** Quantisierungsfilter (welche Ereignisse quantisiert werden; Empfindlichkeit als Einzugsbereich um das Raster; Stärke als Anteil der Verschiebung, empfohlen etwa 50–80 %), **Swing-Quantisierung** und Groove-Vorlagen, die Timing, Velocity und Notenlänge formen. Die reine Zufallsfunktion hält der Autor für wenig brauchbar.
- Zum Swing: Ein Swing-Parameter erlaubt jede Abstufung zwischen geraden Achteln (0 %) und Triolenachteln (100 % in den meisten Programmen); natürlich wirken nach dem Autor Werte zwischen etwa 70 und 120 %. Der Autor empfiehlt, die Swing-Werte zwischen Songteilen leicht zu variieren (etwa ±10 %), damit der Groove menschlicher wirkt. Unterschiedliche Swing-Werte für verschiedene Spuren verbessern das Zusammenspiel.
- Layering von MIDI-Spuren sowie von MIDI und Audio.
- Drum-Editor. Alternative Controller: Gitarre/Bass-zu-MIDI, Drumpads, Blaswandler.
- Komplexe Tempospuren, Tempo- und Taktwechsel, Time-Stretching.
- Synchronisation (MIDI Clock, MTC), Backup und Archivierung, Berechnung der Projektgröße.

### 4. Fortgeschrittene Techniken
- Eigene Grooves erstellen und bearbeiten, Grooves aus Audio gewinnen, Audio quantisieren.
- Erweiterte MIDI-Editoren, Offline-Transformationen von MIDI-Daten, Echtzeit-MIDI-Effekte.
- Insert- und Send-Effekte. Video (QuickTime), SMPTE-Synchronisation, SysEx-Dumps.

### 5. MIDI-Orchestrierung
- **Rhythmusgruppe:** Klavier, Gitarre, Bass, Schlagzeug/Perkussion, jeweils mit Hinweisen zu Spielweise und realistischer Programmierung.
- **Streicher:** Sequencing, Klangbibliotheken, Panorama und Hall.
- **Blechbläser:** Trompete/Flügelhorn, Posaune, Horn, Tuba, Bibliotheken.
- **Holzbläser:** Saxofone, Flöten, Klarinetten, Oboe/Englischhorn, Fagott/Kontrafagott.
- **Synthese:** Hardware/Software, subtraktiv (analog), additiv, FM, Wavetable, Sampling, Physical Modeling, granular.

### 6. Mischen und Premastering
- Spurorganisation, Subgruppen, Rohmix.
- Panorama, Balance, **Frequenzverteilung**.
- Hall und Raum (inkl. Faltungshall), EQ, Dynamik (Kompressor, Limiter, Expander, Gate) in allen vier DAWs.
- Bounce, Dateiformate.
- Premastering: Normalisieren oder nicht, EQ, Multiband-Kompression, Limiter.

## Nutzen für STEPS

- **Drum- und Groove-Modul:** Die Beschreibung der Swing-Quantisierung als stufenloser Parameter zwischen gerade und triolisch sowie der Rat, Swing je Spur und Abschnitt zu variieren, sind direkt übertragbar auf die STEPS-Groove-Logik (z. B. Swing-Prozentwert, Quantisierungsstärke, Velocity). Für eine Humanize-Funktion ist zu beachten, dass der Autor reine Zufallsstreuung ablehnt und stattdessen Groove-Vorlagen empfiehlt. Die Prozentskala für Swing ist zwischen den Programmen nicht einheitlich und muss in STEPS eigens definiert werden.
- **MIDI-Export:** Das Kapitel zu MIDI-Nachrichten liefert die Begriffswelt für den MIDI-Export (Kanal, Program Change, Controller, SysEx), der in STEPS geplant ist.
- **Arrangement-Hinweise:** Die Hinweise zur Programmierung von Rhythmusgruppe und Bläsern eignen sich als Grundlage für spätere Voicing-Presets je Instrument (Lage, Umfang, typische Spielweise).

## Grenzen

- Technisch veraltet: DAW-Versionen, Menüs, Plug-ins und Hardware entsprechen 2005. Nur die Konzepte sind übertragbar.
- Keine Harmonielehre. Musiktheoretische Fragen werden nur am Rand berührt.
- Abbildungen und Screenshots fehlen im Extrakt.
