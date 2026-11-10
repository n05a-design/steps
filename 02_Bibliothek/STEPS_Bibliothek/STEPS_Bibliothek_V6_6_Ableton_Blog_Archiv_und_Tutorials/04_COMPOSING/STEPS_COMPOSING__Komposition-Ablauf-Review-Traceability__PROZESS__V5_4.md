# STEPS V5.4 – Vom musikalischen Auftrag zur revisionsfähigen Komposition

**Stand:** 2026-11-08 · **Status:** ausgearbeitete Arbeitsfassung; stilistische und akustische Fachprüfung offen · **Urheberschaft:** eigene didaktische Beispiele

## Beispiel: 32 Takte als Projektgegenstand
**Ziel:** instrumentales 32-Takt-Stück mit hörbarer A/B-Form, 4/4 bei 104 BPM, Grundinstrumentierung Piano/Bass/Lead/Drums. A1 (T1–8) stellt Motiv M vor; A2 (T9–16) variiert Bass und Register; B (T17–24) schafft Kontrast durch Dichte und neue Harmonie; A3 (T25–32) kehrt motivisch zurück, schließt alternativ offen oder kadenzierend. Für echte Aufnahmen und Mixdown sind Audiowerkzeuge und Hörprüfung nötig.

## Versionierte Entscheidungen
`composition_brief` (Absicht), `motif_family`, `harmony_plan`, `voice_events`, `meter_map`, `groove_link`, `section_graph`, `render_info`, `review_findings` und `license` sind separate Datensichten. Ein Stück kann in mehreren Arrangements existieren. Die Versionierung sollte Materialänderungen, Umkehrungen und Mixrevisionen separat erfassen: `C04-A03` ist nicht nur die neueste Datei, sondern nachvollziehbare Abzweigung aus C04-A02.

## Review-Gates
R0 Schema korrekt und alle referenzierten IDs vorhanden. R1 Takte und metrische Struktur konsistent. R2 Pitch-/Voicing-/Form-Heuristiken dokumentiert, Warnungen nicht still übergangen. R3 von einem Menschen in der Zielästhetik angehört. R4 Rechte- und Veröffentlichungsstatus geklärt. R5 Export in mindestens zwei interoperablen Formaten nachvollziehbar. Keine Behauptung, R3 oder R4 allein durch MIDI-Test zu absolvieren.

## Fehlerbeispiele
- `Section=B` aber kein referenziertes neues oder variiertes Material: Info-Flag, nicht automatisch Fehler.
- Piano-Part notiert in einem unplausiblen Register: Instrumentenprofil prüfen.
- 808-Note-Off mit One-Shot-Sampler: MIDI-Dauer kann von klingender Dauer abweichen.
- Der vermeintliche „Drop“ hat keine Klangdynamik/Automation im Datenmodell: Drum- und Mastering-Events fehlen, keine Scheingenauigkeit.

## Deliverables
Eine kompakte **Kompositionsakte** pro Werk mit Partitur/MIDI, Entscheidungsprotokoll, Hörprotokoll, Claims zur Harmonik, verwendeten Sounds und Lizenzstatus. Die V5.4-Beispiele sind bewusst als *Etüden*, nicht als fertig produzierter Song, eingestuft.
