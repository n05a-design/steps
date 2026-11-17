# ADR-013: Umfang von v0.1 – Akkorde und MIDI-Export, Drums in v2

**Status:** accepted
**Datum:** 2026-11-17
**Entscheidungsträger / Beleg:** Inhaber, Entscheidung im Arbeitsgespräch vom 17.11.2026; ersetzt den Vorschlag ADR-002 und beantwortet ADR-PROD-01 und ADR-PROD-02 in [`PRODUCT_STRATEGY_AND_MVP.md`](../docs/product/PRODUCT_STRATEGY_AND_MVP.md) §8

## Kontext
[`PRODUCT_STRATEGY_AND_MVP.md`](../docs/product/PRODUCT_STRATEGY_AND_MVP.md) §3 vergleicht vier vertikale Schnitte: M1 Theory-only, M2 Chord + SMF-Export, M3 Chords + minimales Drum-Grid, M4 Research-first. Das historische Handover setzte Drums als `REQ-024` auf `DEFERRED`, die spätere Projektbeschreibung nannte sie Produktvision ([`PROJECT_OVERVIEW.md`](../docs/project/PROJECT_OVERVIEW.md) §1 und §8). Zielgruppe und Gewichtung zwischen Lernen und Spielen waren offen.

## Entscheidung
1. **v0.1 = M2:** Akkorde eingeben, transponieren und analysieren, als Standard-MIDI-Datei exportieren. Der Schwerpunkt liegt auf den Akkorden.
2. **Drums kommen in v2 der App.** Die vorhandene Drum- und Rhythmusforschung (`PAT-001`–`PAT-031`, 480-PPQ-Raster, GM-Kanal 10) bleibt erhalten und wird weiter gepflegt, ist aber kein Lieferumfang von v0.1.
3. **Primäre Zielgruppe:** Produzierende, die **beim Produzieren lernen**. Erklärungen sollen im Arbeitsfluss erscheinen (am konkreten Akkord, an der konkreten Progression), nicht als vorgelagerter Kurs.

## Auswirkungen
- Das Zeitmodell bleibt auf 480 PPQ ausgelegt, damit Drums in v2 ohne Datenformatbruch hinzukommen können (Empfehlung aus §3: M3 im Daten- und Zeitmodell zulassen).
- Nächste Kernarbeit: Akkord-Timeline (Taktposition, Dauer), deterministischer SMF-Export und Golden-Fälle für den Export (Gate laut §3: 10 goldene Exportfälle, Import in 2 unabhängigen Programmen).
- Erklärungen müssen kurz und kontextgebunden sein; die Perspektivenwahl folgt [ADR-014](ADR-014-theorie-perspektiven-und-kontext.md).
- Rückfall: Wird v0.1 ohne MIDI-Export zu groß, ist M1 (ohne Export) der kleinere Schnitt. Drums vorzuziehen erfordert ein neues ADR.

## Links
- [`docs/product/PRODUCT_STRATEGY_AND_MVP.md`](../docs/product/PRODUCT_STRATEGY_AND_MVP.md)
- [`docs/project/PROJECT_OVERVIEW.md`](../docs/project/PROJECT_OVERVIEW.md)
- [`manifests/REQUIREMENTS_TRACE_28.csv`](../manifests/REQUIREMENTS_TRACE_28.csv) (`REQ-024`)
