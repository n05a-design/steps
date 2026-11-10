> **STEPS Research Library V5.3 · Stand 08.11.2026 · Status: Fachliche Arbeitsreferenz, nicht unabhängig peer-reviewed.** Eigene Synthese und eigene Beispiele; externe Quellen sind jeweils unter „Nachweise“ angegeben. Unterrichtsbeispiele sind keine genreuniversellen Vorschriften. Das Kapitel dokumentiert Wissen, nicht nachgewiesene Implementierung in Steps.

# V5.3 Datenmodell – getrennte musikalische, technische und belegende Ebenen

## Schichten und semantische Abgrenzung
- **`symbolic_score`**: notierte/musikalisch intendierte Events, Tonhöhen, Stimmen, Takt/Tempo, Harmoniesymbole.
- **`performance_events`**: tatsächlich in MIDI notierte Ereignisse inklusive Note-off, CC, Timing-Offsets, Velocity.
- **`instrument_state`**: Kit-Mapping, Sampler-Envelope, Choke-Groups, Synth-Patches; nicht aus MIDI allein rekonstruierbar.
- **`audio_evidence`**: gerenderter Klang, Messwerte, Klangbeurteilungen mit Datei-Hash/Abhörbedingungen.
- **`research_provenance`**: Quellenausgabe, Seite/Abschnitt, Rechte, Erschließungsstatus, widersprechende Belege.

## Kernvertrag DrumPattern 0.1 – in `14_DATENMODELLE` umgesetzt
`id`, `title`, `style_orientation`, `bpm`, `meter`, `bars`, `steps_per_bar`, `step_duration_beats`, `events[]`, `instrument_map`, `groove`, `source_status`, `license`, `revision`, `qa`. `steps_per_bar` ist kontextabhängig: 4/4 im 16tel-Raster hat 16, 7/8 im Achtelraster hat 7. Alle Step-Indizes sind *nullbasiert* in JSON und MIDI-Konvertierung; UI-Dokumentation kann zusätzlich einsbasierte Zählung zeigen. `channel` als 0–15 MIDI-Wert, Kanal 9 ist in der üblichen GM-Konvention der zehnte Kanal.

## Mess- und Beschreibungsbeispiele
- `played_pitch = 27` bei A4=440 in 12-TET → etwa 38.89 Hz, aber nicht notwendigerweise die tatsächlich hörbare Grundfrequenz eines transponierten Samples.
- `drum_note=36` mit `role=kick` gilt für die **eigene** GM-Map; in fremden Instrumenten ist die Zuordnung `unverified`.
- `offset_ticks=30` bei `ppq=480` und 4/4-16tel-Step 120 ticks = +0,25 Steps. Die Offsetgrenze darf nicht blind auf getaktete 7/8-Figuren angewendet werden.
- `total_duration_ticks` muss für das jeweilige Taktmaß von tatsächlichen Tempo-/PPQ-Ereignissen abgeleitet werden.

## Schema-Evolution und Quellenbindung
Nicht die gesamte historische V1–V5.2-Bibliothek unter einem unbekannten Schema reparieren. V5.3 fügt ein **neues explizit versioniertes Schema** mit stabilen eigenen IDs hinzu; die Altschemata bleiben unverändert. Migration erst nach Mapping und Tests. Der automatische Validator kann Eventgrenzen, Geschwindigkeiten, kanalbezogene MIDI-Semantik und Quellreferenzen prüfen, aber keine stilistische Hörqualität bescheinigen.

## Mini-Traces
`V53-DR01` → `DR53-01` → `study-01.json` + `study-01.mid` → Timing-/Velocity-Tests → `SRC-V53-ABLETON-GROOVE` als technische Referenz, nicht als Beleg, dass das original-komponierte Pattern „typisches House“ repräsentiert. `V53-DYN02` → Kompressor-Workshop → Ableton-Audio-Effects-Quelle → geplanter Audio-A/B-Test. `V53-COMP03` → Topline-Workshop → eigene melodische Skizze → noch kein ausgerendertes Gesangsbeispiel.

### Nachweise
W3C Music Notation: https://www.w3.org/groups/cg/music-notation/ . music21 Roman Numerals: https://music21.org/music21docs/moduleReference/moduleRoman.html . MIDI-Richtlinien: https://midi.org/ .
