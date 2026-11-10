# STEPS 05 – Drum Programming, Rhythm & Groove: Forschungsnotizen V5.1

**Status:** aus konkreten bereitgestellten Unterrichtslektionen analysierte, selbstständig formulierte Notizen. Genres sind stilistische Praktiken, keine ausnahmslosen BPM-/Pattern-Vorschriften. Keine unlizenzierte Übernahme vollständiger Notentabellen, Samples, Audiodateien oder Lehrtexte.

## 1. Gemeinsame Musik- und Datenebenen

Eine Drum-Progression ist nicht nur eine Loop-Liste. Für Steps müssen getrennt modelliert werden: `pulse`, `meter`, `subdivision`, `onsets`, `durations`, `instrument_role`, `velocity`, `microtiming`, `swing/groove_transform`, `articulation`, `rests`, `accents`, `fills`, `sections`, `transitions`, `processing_proposal` sowie `provenance`.

Für einen 4/4-Takt mit sechzehn 16tel-Schritten gelten bei **einsbasierter** Zählung die Viertelpositionen 1/5/9/13. Das bedeutet nicht, dass Genre-Grooves nur 16tel kennen. Zusätzliche Taktarten, Swing-/Shuffle-Raster, Triolen, Off-grid-Interpretationen, Flam/Ratchets und polyrhythmische Ebenen sind eigene Features. Behalte unverändertes MIDI-Timing und eine separate quantisierte Analyseansicht.

**Zeitumrechnung:** `seconds_per_beat = 60/BPM` (wenn der Beat die Viertelnote ist); `seconds_per_16th = 15/BPM`; `seconds_per_4_4_bar = 240/BPM`. Für Swing reicht eine globale Prozentangabe nicht; dokumentiere die tatsächliche Verzögerung pro Subdivision und die anwendbaren Stimmen.

## 2. UK Garage / 2-Step – 132 BPM (PPR-DRUM-004)

Die bereitgestellte Lektion behandelt einen stilisierten Zwei-Takt-Groove mit ausgelassenem regulärem Beat-3-Kick, verteilten Kick-Akzenten und einem stabilen Snare-Backbeat. Offbeat-Hat-Paare und unterschiedliche Anschlagstärken erzeugen vor dem zeitlichen Swing bereits eine differenzierte Gewichtung. Die referenzierte MPC-Groove-Transformation verschiebt innerhalb der 16tel-Unterteilung bestimmte Zwischenpositionen; bei 132 BPM ergibt eine Verzögerung von `0.292` Sechzehnteln rund **33.2 ms**. Der Effekt ist vom DAW-Groove-Preset abhängig und darf nicht pauschal allen Garage-Titeln zugeschrieben werden.

Für Steps: Vergleiche (a) gerade quantisierte und (b) swing-verschobene Varianten **bei gleichen Velocity-Werten**; danach Velocity-Kontrast isoliert testen. Bewahre Fill- und Hook-Abschnitte als zeitliche Ereignisse statt als generische Sound-Tags. Die Lektion verwendet ein bestimmtes Ableton-Kit und Effekte; diese sind **Produktkontext** und keine musiktheoretische Voraussetzung.

## 3. Techno – 130 BPM (PPR-DRUM-002)

Die angegebene Studie verwendet geraden Four-on-the-Floor-Puls, deutlichen Backbeat, ein komplementäres Open-/Closed-Hat-Modell, akzentuierte 16tel und eine zusätzliche rhythmische Ebene mit periodisch verschobenen Impulsen. Sie erläutert Choke-Verhalten zwischen offenen und geschlossenen Hi-Hats und den Unterschied zwischen zyklischer rhythmischer Verschiebung und gewöhnlichem Swing. Änderungen von Ride, Crash, Fill und Dichte gliedern den Track über mehrere Abschnitte.

Für Steps: `choke_group`, `note_off_policy`, `pattern_cycle_length_steps` und `section_variants` sind separat abzubilden. Drei gegen vier Rastereinheiten können durch Versatz über die Taktzeit eine wechselnde Akzentposition bewirken; das allein macht ein Muster noch nicht automatisch zu einer bestimmten historischen Polyrhythmusform.

## 4. Drum & Bass / Sub Focus Style – 174 BPM (PPR-DRUM-003)

Die Studie zeigt ein zweischrittiges Kick-/Snare-Gerüst, differenzierte Hi-Hat-Lautstärken und eine eigenständige, periodisch pulsierende Subbass-Ebene. Das übermittelte Lehrbeispiel enthält eine **Transkriptionshypothese** zu einem E♭-Sub mit einem Rhythmus aus Achtelimpulsen. MIDI-Note 27 entspricht im üblichen MIDI-Frequenzmapping etwa **38.89 Hz**. Ob das Original per diskreten MIDI-Noten, Amplitudenmodulation oder Sidechain entstand, ist aus dem Audiomaterial nicht eindeutig ableitbar.

Für Steps: Speichere zwischen `audible_observation`, `tutorial_recreation`, `transcription_hypothesis` und `authenticated_original_session` unterscheidbare Provenienzstatus. Unterscheide Kick- und Sub-Rhythmus und führe `low_end_interaction` als Relation, nicht als unbelegte Aussage über Originalproduzenten. Die additive Demo-Arrangement-Reihenfolge ist eine **didaktische Bearbeitung**, keine Rekonstruktion des vollständigen Songs.

## 5. Rage/Trap – Miss the Rage Remake – 154 BPM (PPR-DRUM-001)

Der HTML-Text beschreibt ein viertaktiges Fan-Remake mit gestaffeltem Kick-/808-Verhältnis, geraden Hi-Hat-Unterteilungen und charakteristischen Versätzen zusätzlicher Snare-/Rim-Akzente. Besonders relevant ist die **Note-off- und Hüllkurvenproblematik**: Ein 808-Sampler im One-Shot-Betrieb kann trotz kurzer MIDI-Noten weiterspielen. Damit sind sichtbare MIDI-Notenlänge, tatsächliche Hüllkurve und hörbares Ende getrennte Daten. Der Unterricht weist einzelne FX-Trigger ausdrücklich als Remake-Elemente aus, nicht als belegte Originalproduktion.

Für Steps: `bass_trigger`, `audible_tail`, `sampler_playback_mode`, `envelope_release`, `pitch_slide_status` und `sample_transposition` unterscheiden; Tempo 154 BPM kann je nach musikalischem Kontext als Half-Time-Feel von 77 BPM wahrgenommen werden, ohne das Raster zu ändern. Nicht behaupten, dass das Remake autorisierte Produktionsstems oder eine Original-Session enthält.

## 6. Reproduzierbares Datenmodell als Arbeitsentwurf

```json
{
  "pattern_id":"STEPS-GROOVE-STUDY-001",
  "source_id":"PPR-DRUM-004",
  "genre_label":"uk-garage-study",
  "tempo_bpm":132,
  "meter":{"numerator":4,"denominator":4},
  "subdivision":"1/16",
  "time_origin":"bar_1_step_1",
  "events":[],
  "groove":{"type":"swing-transform","amount":null,"affected_steps":[],"source_preset":"unverified_local_midi"},
  "arrangement_sections":[],
  "audible_vs_midi_discrepancies":[],
  "copyright_review":"required",
  "verification":"schema_example_not_transcribed"
}
```

Nicht-leere Note-Events erst nach legalem Import der lokalen MIDI-Dateien erzeugen; das hier gezeigte Schema ist **kein ausgearbeitetes Drum-MIDI**.

## 7. Forschungsprogramm jenseits der Kurslektion

- Systematisch unterscheiden: Groove, Swing, Shuffle, Syncopation, Metrical Displacement, Polyrhythm, Metric Modulation, Microtiming, Ghost Notes und Accents.
- BPM-Bereiche pro Genre als Datenpunkte mit Korpus-/Stichprobenkontext statt harte Genredefinitionen behandeln.
- Sonische Ebene und rhythmische Syntax trennen: Ein identisches MIDI-Gitter kann bei anderem Kit, Envelope/Choke, Transienten und Dynamik anders wahrgenommen werden.
- Beziehungen zum Composing-Band: Bassline ↔ Kick ↔ Harmonic Rhythm ↔ Arrangement-Form ↔ Spannung und Pausen.
- Geeignete externe Forschungsrichtungen: Justin London (*Hearing in Time*), David Huron (Erwartung), Christopher Hasty (*Meter as Rhythm*), Forschung zu Groove/Microtiming, MIR-Beat-Tracking. Bei Aufnahme konkrete Edition, DOI und Lizenz einzeln prüfen; keine abgeschlossene Lektüre behaupten.
- Rechte: selbst erstellte abstrakte Studienfälle statt unveränderter kommerzieller MIDI-/Sample-Redistribution. Fan-Remakes und Audioanalysen klar als Interpretationen kennzeichnen.
