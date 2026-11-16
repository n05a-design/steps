# ADR-007: Audio/MIDI – in v0.1 nur Dateiexport

**Status:** accepted
**Datum:** 2026-11-17
**Entscheidungsträger / Beleg:** Inhaber, Gesamtspezifikation vom 17.11.2026; ersetzt den Vorschlag „Ports zuerst, Backend nach Plattform-/Lizenzbenchmark“ im [Register](DECISION_REGISTER.md)

## Kontext
Die Architektur sieht `Timeline → Scheduler → PortMIDI / SynthBackend / NullBackend` vor ([`MUSIC_DOMAIN_AND_MIDI.md`](../docs/engineering/MUSIC_DOMAIN_AND_MIDI.md)). Ein SMF-Export beweist keine stabile Echtzeitausgabe. Soundfonts bringen Größe und Lizenzfragen mit ([`RIGHTS_SECURITY_AND_RELEASE.md`](../docs/governance/RIGHTS_SECURITY_AND_RELEASE.md)).

## Entscheidung
- **v0.1:** nur Dateiexport nach [ADR-017](ADR-017-midi-export-v01.md). Kein In-App-Audio, kein Bundling von Soundfonts.
- **Option für v0.2:** betriebssystemeigener MIDI-Ausgang an virtuelle Ports (IAC auf macOS, loopMIDI auf Windows), damit die DAW live spielt. Eigene Entscheidung vor Umsetzung.

## Auswirkungen
- Keine Soundfont-Rechtekette und keine 30–140 MB zusätzlicher Daten in v0.1.
- Keine plattformabhängigen Audiotreiberfehler in v0.1; `NullBackend` genügt für Tests.
- UX-09 („fehlende Audioausgabe bei funktionierendem MIDI-Export“) in [`LEARNING_AND_EXPERIENCE.md`](../docs/product/LEARNING_AND_EXPERIENCE.md) ist damit bewusst in Kauf genommen; die Oberfläche muss den Weg in die DAW klar zeigen.
- Rückfall: Ein späteres Backend hängt sich an die vorhandene Port-Schnittstelle, ohne den Export zu ändern.
