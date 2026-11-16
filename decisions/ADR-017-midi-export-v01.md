# ADR-017: MIDI-Export für v0.1

**Status:** accepted (Umsetzung offen)
**Datum:** 2026-11-17
**Entscheidungsträger / Beleg:** Inhaber, schriftliche Gesamtspezifikation vom 17.11.2026 mit Freigabe der Präzisierungen aus dem Repository-Abgleich

## Kontext
[ADR-013](ADR-013-v01-umfang-akkorde-und-midi-export.md) legt v0.1 auf Akkorde + MIDI-Export fest. Der Zielvertrag in [`MUSIC_DOMAIN_AND_MIDI.md`](../docs/engineering/MUSIC_DOMAIN_AND_MIDI.md) und der Prüfplan Q5 in [`VERIFICATION_PLAN_V2.md`](../docs/quality/VERIFICATION_PLAN_V2.md) nennen die technischen Prüfpunkte, aber keine Produktvorgaben. Das Gate aus [`PRODUCT_STRATEGY_AND_MVP.md`](../docs/product/PRODUCT_STRATEGY_AND_MVP.md) §3 verlangt 10 goldene Exportfälle und den Import in 2 unabhängigen Programmen.

## Entscheidung

| Parameter | Vorgabe v0.1 |
| --- | --- |
| Dateiformat | SMF Typ 1, 480 PPQ |
| Spuren | Track 0: globale Meta-Events · Track 1 „Chords“ (Kanal 1) · Track 2 „Bass“ (Kanal 2). Tracknamen als Meta 0x03. Option im Export: eine einzige Spur. |
| Notenlänge | Standard: Akkorddauer minus 10 Ticks (≈ 10 ms bei 120 BPM). Option: 95 % der Akkorddauer. Auf demselben Tick stehen Note-offs immer vor Note-ons (Vertrag T14). |
| Lage | Akkorde: 4-stimmig in enger Lage (`CLOSE`) im Bereich MIDI 48–72. Option: `DROP2` oder `ROOTLESS` (3-7-9-13). Bass: Grundton bzw. notierter Bass in MIDI 36–47 (C2–B2), über `ChordDefinition.to_voicing(..., bass_octave=2)`. |
| Velocity | Fest: Akkorde 90, Bass 100. Kein Humanize. Ergebnis ist deterministisch und hashbar. |
| Metadaten | Tempo (0x51) und Taktart (0x58) auf Track 0, Standard 120 BPM und 4/4. Tonart (0x59) nur bei diatonischem Dur oder Moll mit −7…+7 Vorzeichen; bei modalen Tonarten (z. B. D-Dorisch) oder mehr als 7 Vorzeichen weglassen. Kein Program Change (0xC0). |
| DAW-Abnahme | Reaper (strenger SMF-Parser) und MuseScore 4 (Taktart, Tonart, Notation); alternativ Ableton Live oder Logic Pro als zweites Programm. Ergebnis mit Versionsstand protokollieren. |
| Audio | Siehe [ADR-007](ADR-007-audio-nur-dateiexport-v01.md): kein In-App-Audio in v0.1. |

**Begründung:** Typ 1 mit getrennter Bassspur lässt sich in jeder DAW direkt auf zwei Instrumente routen. Die feste Lücke von 10 Ticks verhindert Kollisionen gleicher Folgetöne, ohne bei Pads hörbar zu werden; 95 % ergäbe bei einem ganztaktigen Akkord 96 Ticks, also 100 ms bei 120 BPM. Ohne Program Change setzt die DAW keine Instrumente unerwartet auf GM-Piano zurück. Die feste Velocity macht Golden-Fälle über Hashes und Ticks prüfbar.

## Auswirkungen
- Kern: ein reiner SMF-Writer ohne UI-Abhängigkeit (`src/steps/`), getrennt von `app/` (`AGENTS.md` Regel 4).
- Tests: 10 Golden-Exportfälle mit Byte-Hash; Prüfpunkte 1–10 aus `MUSIC_DOMAIN_AND_MIDI.md` §5, darunter Note-off-Reihenfolge, Tempo-Map und Meta-Events.
- Daten: Das Zeitmodell bleibt bei 480 PPQ, damit Drums in v2 ohne Formatbruch dazukommen.
- Rückfall: Jede Vorgabe ist ein Exportparameter; Änderungen brauchen neue Golden-Hashes, aber keine Datenmigration.

## Links
- [`docs/engineering/MUSIC_DOMAIN_AND_MIDI.md`](../docs/engineering/MUSIC_DOMAIN_AND_MIDI.md)
- [`src/steps/theory/chord.py`](../src/steps/theory/chord.py) (`ChordDefinition.to_voicing`, Voicing-Arten)
- [SMF-Spezifikation der MIDI Association](https://midi.org/standard-midi-files)
