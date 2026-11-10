# STEPS V5.4 – DAW-Workflow vom Session-Brief bis zum reproduzierbaren Export

**Stand:** 2026-11-08 · **Status:** neue ausführliche Arbeitsfassung; nicht vollumfänglich begutachtet · **Urheberschaft:** eigenständiges Lehrmaterial

## Produktionsprojekt vs. Partitur
Eine Produktionssession enthält Zeitachsen, Spuren, Busse, Sends, Effekte, Automation, Sample-Pfade, Samplerate, Metadaten und Importversionen. Ein MusicXML-Export bewahrt vor allem notierte Musik, nicht automatisch Plugins und Mixbus-Routing; MIDI kann CCs, Noten, Tempo-Map tragen, nicht authentische Audioverarbeitung. Schritte sollten Datenverluste bei Formatwechsel sichtbar machen.

## Standardisierte Projektstruktur
`project.json` (Tempo/Time Signature und Referenz), `composition/` (MIDI/MusicXML), `drums/`, `sources/` (URI + Nutzungsrechte, keine undokumentierten Binärkopien), `renders/` (WAV-Metadaten/Hashes), `mix_decisions.md` (A/B-Versuche), `qa.json` (Checks). Unveränderliche Quell-Dateihashes erlauben verlässliche Ableitungsrelationen.

## Export-Check
1. Start-/Endposition prüfen (Pickup und Schlussrelease).
2. Tempo-Map und Tickauflösung beim MIDI-Reimport vergleichen.
3. WAV-Renders getrennt nach Sample Rate, Bit Depth, Kanalanzahl, Interpolation/dither stage erfassen.
4. Alle Samples und Plug-in-Versionen in einem lokalen, privaten Manifest nachhalten; keine unkontrollierte Weitergabe kommerzieller Assets.
5. Stereo/Mono Vergleich und Pegelabgleich. Ein schwacher Mono-Downmix kann auf ungünstige Phasen-/Stereo-Verarbeitung hindeuten; eine rein negative Korrelationszahl beweist nicht allgemein ein schlechtes Arrangement.

## Reimport-Szenarien
MIDI importiert nach anderer DAW: `note_number`, `note_on/off`, `velocity`, `program/channel`, `tempo_map` und `CC` erhalten. Live/FL-Oktavnamen können abweichen, deshalb `display_octave_mapping` getrennt speichern. Audiovergleich nur mit bekanntem Instrument/Preset und Renderengine; identische MIDI ist nicht gleich identischer Klang.

**Abgrenzung:** Hersteller-spezifische Bedienanweisungen sind in die jeweiligen offiziellen Manual-Verweise (z. B. SRC54-010–012) zu verlinken; keine Behauptung globaler Kompatibilität.
