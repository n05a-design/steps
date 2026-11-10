> **STEPS Research Library V5.3 · Stand 08.11.2026 · Status: Fachliche Arbeitsreferenz, nicht unabhängig peer-reviewed.** Eigene Synthese und eigene Beispiele; externe Quellen sind jeweils unter „Nachweise“ angegeben. Unterrichtsbeispiele sind keine genreuniversellen Vorschriften. Das Kapitel dokumentiert Wissen, nicht nachgewiesene Implementierung in Steps.

# Producer Workflows als interoperative, reproduzierbare Prozesse

## Ausgabeverträge statt DAW-Screenshots
Die Bibliothek soll nicht voraussetzen, dass jeder Nutzer Ableton Live besitzt. Ein Workshop muss mindestens eine DAW-neutrale Notendaten- bzw. Ereignisrepräsentation anbieten: `tempo_map`, `meter`, `ppq`, `tracks`, `note_events`, `controllers`, `automation`, `instrument_role`, `audio_assets`, `permissions` und `export_settings`. Für ausnotierte harmonische Musik sind MusicXML und ggf. andere Symbolformate zusätzlich sinnvoll; MusicXML ist nicht automatisch ein Ersatz für samplegenaue DAW-Automation.

## Drei Artefakte mit unterschiedlichen Fähigkeiten
**MIDI:** Note-on/off, Controller, programmbezogene Events und Tempo-/Zeitsignaturevents im File; es transportiert grundsätzlich nicht die eigentliche Sample-Waveform oder jedes DAW-Plugin-Preset. **MusicXML:** Notation, Stimmen, Taktstrukturen und Harmoniesymbole; kein vollständiges Mixing-Projektformat. **WAV/FLAC:** gerenderte Audiodaten, ohne zugängliche Harmonieobjekte oder modifizierbare MIDI-Begleitspur. Ein `round_trip` muss daher die *zu erwartenden* erhaltenen Eigenschaften spezifizieren, statt vollen Projektidentitätserhalt zu behaupten.

## Reproduzierbarer Exporttest
1. Ein zweitägiger (2-Takt) Original-Groove in JSON mit `PPQ=480` und Tempo 120 BPM. 2. MIDI exportieren; re-importieren; absolute und relative Eventzeit/Velocity vergleichen. 3. Diesen MIDI-Clip in einer beliebigen DAW öffnen und mit neutralem GM-Kit abspielen; Instrument-Pitch-Mapping dokumentieren. 4. Klang-/Mixer-Einstellungen separat als textliche Rezeptur erfassen. 5. Bei Melodie- und Harmoniepart zusätzlich MusicXML-Export mit Key/Time Signature und Stimme prüfen. 6. Interoperabilitätsverlust explizit reporten.

## DAW-spezifische Details
Abletons Groove Pool kann Timing-/Velocity-Änderungen in Echtzeit oder per Commit auf Clips anwenden; beim Export ist deshalb relevant, ob die Groove-Transformation bereits in Events geschrieben wurde. Simpler/Sampler/Drum Rack können komplexes Playbackverhalten erzeugen, das eine Standard-MIDI-Datei nicht erfasst. Der genaue Oktavname ist per DAW zu unterscheiden; MIDI-Notennummer dient als stabiler Anker.

## Qualitäts- und Rechteprüfung
Bei Presets und Samples muss der Verwendungsstatus pro Asset geprüft werden. Samples dürfen nicht aus proprietären Packs in die offene STEPS-Bibliothek kopiert werden. Der dokumentierte Workflow muss ohne bezahlte Plug-ins nachvollziehbar bleiben, sofern nicht anders gekennzeichnet.

### Nachweise
W3C Music Notation Community Group (MusicXML/SMuFL/MNX): https://www.w3.org/groups/cg/music-notation/ . Ableton Live 12 Handbuch MIDI/Grooves: https://www.ableton.com/de/live-manual/12/ . MIDI Association: https://midi.org/ .
