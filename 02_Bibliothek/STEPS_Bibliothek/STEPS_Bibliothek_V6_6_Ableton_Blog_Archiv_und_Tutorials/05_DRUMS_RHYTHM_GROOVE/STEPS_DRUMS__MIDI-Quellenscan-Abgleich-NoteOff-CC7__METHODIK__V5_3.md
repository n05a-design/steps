> **STEPS Research Library V5.3 · Stand 08.11.2026 · Status: Fachliche Arbeitsreferenz, nicht unabhängig peer-reviewed.** Eigene Synthese und eigene Beispiele; externe Quellen sind jeweils unter „Nachweise“ angegeben. Unterrichtsbeispiele sind keine genreuniversellen Vorschriften. Das Kapitel dokumentiert Wissen, nicht nachgewiesene Implementierung in Steps.

# Reproduzierbarer MIDI-Abgleich für lokale Steps-Dateien

## Bestandsgrenze
Die Nutzerangabe, dass PausePlayRepeat-MIDI-Pakete lokal im Steps-Ordner liegen, ist keine Bestätigung ihres Inhalts in diesem V5.3-Archiv. Das beigefügte Skript `15_TOOLS_SKRIPTE/STEPS_TOOLS__audit_midi_library__WERKZEUG__V5_3.py` arbeitet ausschließlich auf einem **explizit als Argument übergebenen** Verzeichnis und schreibt einen Bericht in einen separat benannten Zielordner. Ohne Zugriff auf den lokalen Steps-Ordner bleiben Checks mit `pending_local_access` ausgewiesen.

## Prüflogik
**1. Inventar:** Alle `.mid/.midi` und ZIP-Container in Scope zählen, SHA-256 berechnen, Größen, relative Pfade, ZIP-Lesbarkeit und Duplikatgruppen protokollieren. **2. Music file:** MIDI-Header, Format 0/1/2, Ticks per Beat, Trackname/Time-Signature/Tempo/CCs, Note-on/Note-off-Paarung pro Kanal und Ton bestimmen. **3. Mapping:** Kit-/Drumrollen über zugehörige Lektion, dokumentierte GM-Konvention oder lokales Mapping nachweisen; Note 36 ist ohne Kontext nicht zwingend Kick. **4. Timing:** Tempoevents, fehlende Tempoangaben, Takt/Beat-Offset, tatsächliche Swing-Verteilung und Off-Grid-Toleranz messen. **5. Audio-Verhalten:** MIDI-Notenende ist **nicht** identisch mit dem hörbaren Sample-Ende. Ohne Instrument-/Samplerzustand keine exakte Klangdauer behaupten.

## Konfliktfälle aus den Lernunterlagen
- UK Garage: `Straight/` und `Swung/` müssen als zwei Dateivarianten auf gleiche musikalische Ereignisse mit unterschiedlichem Timing vergleichbar sein. Nicht allein Dateiname als Beleg verwenden.
- Techno: ein Choke-Group-Verhalten ist Instrument-Mapping, nicht verlässliche Eigenschaft der MIDI-Events.
- D&B: Pulsieren des Subs kann diskrete Note-on/offs oder Audioamplitude sein; nicht aus einer angeblichen Originalaufnahme rekonstruieren.
- Rage/Trap: Fan-Remake; Note-off-Kontrollen, 808-Envelope und MIDI-Tonhöhe müssen getrennt werden. Kein Original-Session-Nachweis.
- CC7: Channel Volume auf Drums-Kanal und DAW-Faderautomation können ähnliche Lehrziele erfüllen, sind aber nicht dasselbe Eventmodell.

## Vergleichsbericht pro Datei
`file_id`,`sha256`,`source_id`,`style_claim`,`event_count`,`duration_bars`,`tempo_map`,`ppq`,`channel_notes`,`cc_summary`,`unclosed_notes`,`unverified_kit_map`,`hypothesized_source`,`license_status`,`reviewer`,`status`.

## Datenschutz und Rechte
Scan-Ergebnisse speichern standardmäßig nur Metadaten und Hashes; Original-MIDI kommerzieller Lektionen bleibt am vom Nutzer bestimmten privaten Ort. Repo-Commits von proprietären Midi-Dateien sind ohne Lizenzprüfung gesperrt. Prüfskript und eigene MIDI-Fallstudien sind unabhängig davon verwendbar.

### Nachweise
MIDI Association – Normenbezug: https://midi.org/ . GM-Percussion-Map als sekundäre öffentliche Spezifikationsdarstellung: https://midimusic.github.io/tech/midispec.html . Ableton-Manual zum Drum Rack: https://www.ableton.com/en/manual/instrument-drum-and-effect-racks/ .
