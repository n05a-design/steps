# STEPS V5.4 – Kanonisches Eventmodell und Standardschnittstellen

**Stand:** 2026-11-08 · **Status:** neue ausführliche Arbeitsfassung; nicht vollumfänglich begutachtet · **Urheberschaft:** eigenständiges Lehrmaterial

## Strikte Entitäten
`Project`, `TempoChange`, `MeterChange`, `Section`, `Pitch`, `NoteEvent`, `ChordEvent`, `DrumHit`, `ArrangementEvent`, `AutomationEvent`, `AnalysisAssertion`, `SourceRecord`, `LicenseDecision` haben **separate IDs**. MIDI-Numbers und Chord Symbols sind serialisierte Eigenschaften, nicht universale Musikobjekte. Ereigniszeiten werden als rationale Viertelpositionen mit Tempo-Map gespeichert.

## Harmonic analysis event
Beispiel JSON: `{ "id": "AN-001", "event_id": "CH-003", "lens": "roman_in_key", "local_key": "C:maj", "label": "V7/ii", "alternatives": [], "status": "proposed", "source_ids": ["SRC54-003"] }`. Quellenverweis auf DCML bedeutet *Syntaxhilfe*, nicht dass ein menschlicher Editor A7 in diesem Stück definitiv so hören muss.

## Externe Formate
- MusicXML: Notation/Spelling/Durations/Voices, SRC54-008/009; Divisions pro Viertel, damit Time-Math korrekt ist.
- MIDI: note number, note-on/off, velocity, channels, CC und Tempo-Map; Notenschreibung geht bei Umwandlung ggf. verloren.
- DCML: formale Roman-Numeral-Grammatik, mit explizitem lokalem Kontext, SRC54-003.
- JAMS: mehrere Annotationsspuren pro Titel, Validation für Chord/Beat/Sections, SRC54-022.
- partitura: potenzieller Adapter für MusicXML, MIDI, MEI und Humdrum, SRC54-023; erst nach realem Dependency-Test in Steps übernehmen.

## Migrations- und Lizenzdaten
Erst die historischen V1–V5.3-IDs inventarisieren, bevor ein Import eine kanonische ID vergibt. `legacy_aliases` darf Duplikate referenzieren und muss die ursprünglichen Provenienzen erhalten. Korpora vor Import pro Teilbestand auf `commercial_use`, `redistribute_notes`, `derive_analysis`, `source_attribution` prüfen. ChoCo-Subsetlizenzen unterscheiden sich (SRC54-021).

## Fehlerszenarien
Ambige Enharmonik, verschiedene MIDI-Middle-C-Namen, polyrhythmische Events, Taktwechsel, anacrusis/auftakt, konkurrierende Harmonieanalysen, GUI-Notenrundung, fehlende Originalaufnahme, unklare Rechte. Diese Zustände sind Modellfälle, keine bloßen Edgecase-Ausnahmen.
