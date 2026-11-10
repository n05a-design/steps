# Steps-Fachmodell: Musiktheorie, Harmonie, Akkorde, Rhythmus, MIDI und Erklärung

**Status:** Vorschlag zur fachlichen Spezifikation und Akzeptanzprüfung; kein ausgeführtes Produkt. Quellen: `01_STEPS_Research_Foundation.md`, `02_STEPS_Knowledge_Base_Product_Blueprint.md`, `PROJECT_CONTEXT_HANDOVER.md` im Steps-Research-Archiv; konsolidierte Overview §§2–3 und 8–9; im Repo vorhandene JSON-Schemas sind ein *Scaffold*, keine voll validierte Musik-Engine.

## 1. Warum „Akkordliste“ nicht genug ist

Akkorde als reine Strings reichen für die spätere Anwendung nicht aus. `F#` und `Gb` haben im gleichstufigen 12-Ton-System gleiche Pitch Class, aber unterschiedliche Schreibweise und Harmonierolle. `C7`, `Cmaj7`, `Cm7`, `C/E` und `C7/G` erfordern getrennte Strukturinformationen. `V7/vi` ist eine **Analyse** im Kontext C-Dur, kein zeitloses Attribut des Akkords E7. Auch das musikalische Timing muss unabhängig von Rendering und Taktanzeige verwaltet werden.

**Unverhandelbare Trennungen:**

1. **Klingende Höhe** (`Pitch`/MIDI note/frequency) ≠ **Pitch Class** (bei 12-TET 0–11) ≠ **Note Spelling** (`F#`, `Gb`, `H`, `B`) ≠ **temperierte Stimmung**.
2. **Akkordidentität** (tonale Tonklassenstruktur) ≠ **Akkordsymbol** (Text) ≠ **Voicing** (gespielte Tonhöhen inkl. Oktaven/Dopplungen) ≠ **Inversion/Slash Bass** ≠ **theoretische Funktion** im Kontext.
3. **Progressionsobjekt** (Klangfolge) ≠ **Rhythmische Ereignisse** (Position/Dauer) ≠ **Phrasen-/Formabschnitt** ≠ **Stil-/Kontextmetadaten** ≠ **Analyse**.
4. **Theoriefakt** ≠ **Korpusstatistik** ≠ **kreativer Vorschlag** ≠ **mögliche Interpretation eines LLM**.
5. **Notation** ≠ **MIDI-Export** ≠ **Playback-Audio**. Ein MIDI-File enthält keine zwingend verlässlich transportierte Funktionsanalyse.

## 2. Kernobjekte und Abhängigkeiten

```text
TuningSystem (12-TET im Startumfang; andere später)
NoteName {letter, accidental, locale} -> PitchClass {0..11}
Pitch {pitch_class, octave, tuning}
Interval {diatonic_steps, chromatic_distance, direction}
Scale {tonic_spelling, mode_id, degree_set, tuning_id}
ChordIdentity {root, degree_recipe, quality, alterations, omissions}
ChordSymbol {notation_system, original_text, normalized_structure}
Voicing {ordered_notes, velocity?, duration?, bass_note?}
HarmonicContext {global_key, local_key?, style, theory_framework, phrase_position}
HarmonicAnalysis {chord_ref, context_ref, roman, function, alternative[], confidence?}
Progression {id, bars, events, context_changes, provenance}
RhythmEvent {onset_ticks, duration_ticks, meter_ref, groove_ref?}
GroovePattern {instrument_mapping, steps, microtiming, velocity, swing, meter}
PlayableSequence {tracks, events, tempo_map, time_signature_map, ppq}
```

Diese Typen sind *Modellkandidaten*. Vor Umsetzung muss entschieden werden, ob `ChordIdentity` über die Tonklassen oder intervallische Recipe normalisiert wird, wie Inversion vom Bass unterschieden wird und welche Symbolparser erlaubt sind. Eine untypisierte Note wie `B` darf bei gemischten deutschen/internationalen Quellen **nicht** automatisch als eindeutige Klasse behandelt werden.

### Minimale fachliche Invarianten

| ID | Regel und Negativfall | Beabsichtigte Testwirkung |
|---|---|---|
| T01 | C-Dur = C D E F G A H (deutsche Namen); international letzter Ton B | korrekte Locale-Projektion |
| T02 | deutsches `B` bedeutet Bb, internationales `B` B natural | ohne Locale: Ablehnung/Ambiguitätsmeldung |
| T03 | `F#`/`Gb` gleiche 12-TET-Pitch-Class, aber andere diatonische Rolle | No spelling-loss bei round-trip |
| T04 | C7 = C E G Bb; Cmaj7 = C E G H/B natural | Qualitätsunterscheidung |
| T05 | Cm7 = C Eb G Bb | Moll/Sus/Add nicht still ersetzen |
| T06 | C/E klingt mit E als Bass; Symbolparser erkennt Slash-Bass getrennt | Inversion nur bei passenden Akkordtönen; fremder Bass separat |
| T07 | `C–G–Am–F` +2 Halbtonschritte → `D–A–Bm–G` international | Transposition inkl. enharmonischer Strategie |
| T08 | E7→Am ist in a-Moll Dominante V7, in C-Dur V7/vi | Kontextabhängigkeit |
| T09 | `bVII→I` nicht pauschal als klassische authentische Kadenz erklären | Stilmodell und alternative Analyse |
| T10 | gleiche Noten als verschiedene Voicings können verschiedene Stimmführungskosten haben | keine reine Set-Metrik als „beste Stimmführung“ |
| T11 | kein Chord ohne korrekte Dauer- und Taktposition | Storage/Playback-Konsistenz |
| T12 | `no3`, `sus4`, Extensions/Alterations werden nicht durch einfachen Major/Minor-Flag überschrieben | komplexe Akkordsymbole prüfen |
| T13 | alternative Analysen mit unterschiedlicher Quelle/Framework werden nicht automatisch in eine Wahrheit gemergt | Konfliktprovenienz |
| T14 | exportierte MIDI-Note-ons haben passende Note-offs auch bei Loop/Stop/überlappenden gleichen Tonhöhen | Noten-Hänger verhindern |
| T15 | Tempoänderung mitten in einer Progression beeinflusst Tick→Sekunden-Umrechnung | Scheduler/SMF-Tempo-Map |
| T16 | Swing/Humanize müssen bei gleichem Seed reproduzierbar und begrenzt sein | generatives Timing testbar |

## 3. Typsichere Harmoniebeziehungen statt unmotivierter „nächster Akkord“

Für jede vorgeschlagene Kante `source_chord → candidate_chord` muss genau angegeben sein: `relation_type`, `framework`, `key_context`, `style_scope`, `preconditions`, `explanation_claim_ids`, `counterexamples`, `source_evidence`, `heuristic_score` (falls verwendet), `review_status`. Beispiel-Typen: `DIATONIC_WITH`, `DOMINANT_OF`, `RESOLVES_TO`, `BORROWED_FROM`, `COMMON_TONE_WITH`, `VOICE_LEADING_NEAR`, `TRANSFORMATION_OF`, `SUBSTITUTES_FOR`. Eine Relation darf *gerichtet* sein; `DOMINANT_OF` ist nicht automatisch symmetrisch.

**Beispiel A:** `E7 → Am` im Kontext a-Moll, funktional: E7 als V7 mit Leitton G#; im Kontext C-Dur: E7 als V7/vi. Ein Chord-Layer darf beide Lesarten zulassen; die UI muss den lokalen/globalen Kontext sichtbar machen. **Beispiel B:** `C → Fm` in C-Dur: chromatische Entlehnung aus c-Moll/Modal Interchange möglich; in anderem Kontext kann sich eine andere Funktion ergeben. Der UI-Text darf nicht behaupten, „dieser Akkord ist immer so“.

**Voice Leading:** Ein Minimalabstand ist nur nach Festlegung der Voicings, Register, Instrumentengrenzen und Gewichtung messbar. Wenn nur Chordsymbole vorhanden sind, darf eine angezeigte „Voice-leading-Ähnlichkeit“ nur als Kandidat oder abstrakte Tonklassenmetrik erscheinen, nicht als physikalisch eingespielte Bewegung.

**Korpora:** `ChoCo`, Billboard und `When in Rome` sind Referenz-/Akquisekandidaten; es ist in diesem Audit nicht bewiesen, dass alle Datensätze in Steps importiert, rechtlich geprüft und nutzbar sind. Quellenbericht-Counts müssen bei tatsächlicher Übernahme erneut erhoben werden.

## 4. Gemeinsames Chord-/Drum-Zeitmodell

Ein gemeinsames Zeitmodell ist eine *technische Vorarbeit*, keine Festlegung, dass Drums im ersten Release enthalten sein müssen. Minimaler `MusicTime`-Vertrag:

- musikalische Position intern in **ganzzahligen Ticks** einer deklarierten `PPQ`-Auflösung, nicht ausschließlich `float Sekunden`. Takt-/Zählzeitprojektion nutzt die aktuelle Taktart-/Tempo-Map.
- **Dauer separat von Onset** (ein Akkord kann über Taktgrenzen gehalten werden). Rests/pauses sind explizite Ereignisse, keine magischen `None`-Chords.
- ein Event enthält `track_id`, `event_type`, `start_tick`, `duration_tick`, `payload`, `source_id` für erklärbare Verarbeitung.
- Drum-Events enthalten Instrument-Key/GM-Pitch (falls exportiert), Velocity und ggf. Mikrozeitverschiebung. Ein Pattern kann symbolische Kick/Snare/HiHat-Rollen über Mapping zu MIDI übersetzen.
- Swing/Humanize sind **abgeleitete Transformationsoperationen**, die Originalnoten nicht unbemerkt überschreiben; `seed`, `amount`, `boundaries` und Konfliktlösung (keine negativen Ticks) werden gespeichert.
- Tempo, Meter und Loop-Regionen werden versioniert und in Save/Load/Export mitgeführt; UI-Taktgitter ist eine Projektion, nicht das persistierte musikalische Original.

**Konsequenz für MVP:** Auch wenn Drums später kommen, sollte Steps das Projektformat nicht auf „one chord per bar“ festlegen. Sonst erzwingen Sync, Wechsel auf halbe Takte, Piano Roll und Drum-Grooves ein frühes Breaking Change.

## 5. MIDI- und Audio-Engineering-Grenze

Die MIDI Association stellt SMF-Spezifikation und ergänzende RP bereit: https://midi.org/standard-midi-files . Bei Mido bedeutet `message.time` in **MIDI-Tracks** eine nonnegative Delta-Zeit in Ticks, nicht zwingend absolute Zeit/Sekunden; der Tempo-Meta-Event benutzt µs/Viertelnote (vgl. https://github.com/mido/mido/blob/main/docs/messages/index.rst und https://github.com/mido/mido/blob/main/docs/meta_message_types.rst ). `music21` ist ein Referenzoracle/Adapterkandidat, kein nachgewiesen integrierter Engine-Kern: https://music21.org/music21docs/moduleReference/moduleChord.html .

### Abnahmeplan MIDI-Datei (künstliche Testdaten)

1. **Type 0**: 1 Track + Tempo + Time Signature + Noten, Round-trip; events nach Tick-Position identisch.
2. **Type 1**: Meta/Tempo-Track plus Chord-/Drum-Tracks, korrekte Kanalzuordnung und simultane Events.
3. **Tempo-Wechsel**: 120→90 BPM mitten im Song, Dauervergleich unter Verwendung der Tempo-Map, nicht fälschlich 1 Tempo global.
4. **Note-offs**: Wiederholte gleich hohe Noten mit Überlappung, Stop/Seek/Loop erzeugen keine hängenden Töne; Release/All-notes-off Backend-spezifisch prüfen.
5. **Velocity**: 1..127 für aktive Noten; 0-velocity Note-on im MIDI-Importer als möglicher Note-off behandeln.
6. **Ausgabegerät**: kein MIDI-Port vorhanden → Datei-Export weiterhin möglich, Playback-Status `unavailable`, keine App-Blockierung.
7. **Kanal/Drums**: GM Channel 10 (in APIs oft Index 9) bewusst dokumentieren; Map nicht mit automatisch jedem Drumtrack auf denselben Backend-Kanal verwechseln.
8. **Meta-Events**: Ende des Tracks, Tracknamen, Time Signatures, Sequence-Tempo und importierte unknown Events korrekt behandeln oder als Verlust ausweisen.
9. **Ressourcenlimits**: sehr große/defekte .mid-Dateien kontrolliert abbrechen; Parser darf nicht die Tk-Eventloop blockieren.
10. **DAW-Probe**: exportierte Testdatei in unabhängigem Programm öffnen und tatsächlich hören; Ergebnis/Versionsstand protokollieren.

### Playback-Subsystem

`Timeline` → `Scheduler` (monotonic clock, cancellation, look-ahead) → `PortMIDI` / `SynthBackend` / `NullBackend`. GUI darf Anfragen einstellen und Status erhalten, aber keine Audio-Sleeps im Tk-Callback ausführen. Vom Worker kommende Ergebnisse gehen kontrolliert an den UI-Thread zurück; nach Close dürfen keine Spät-Callbacks auf zerstörte Widgets zugreifen. **Nicht** aus der Existenz von SMF-Export auf stabile Echtzeit-Audioausgabe schließen. Verschiedene Backends/OS unterscheiden sich bei Latenz, Buffering, Device-Lifecycle und Softsynth-Lizenzen.

## 6. Datentransfer und Schema-Version

Die derzeitigen `schemas/chord.schema.json` und `schemas/progression.schema.json` sind Stubs mit Strings; deshalb für erste *proof-of-concept* Fixtures geeignet, aber keine umfassende Semantik für dynamischen Tonartwechsel, Note Spelling, Akkord-Voicings, Mehrdeutigkeiten, Timing/Tempo und Drum-Layer. Ein Breaking Change muss `schema_version`, Migrationspfad und Rückwärtslesbarkeit im Datenformat dokumentieren. Vorher Testfixtures definieren, dann Schema vereinbaren. Ein einmaliges `chord.symbol` ist ein **Anzeigeinput**, nicht die einzige Truth Source.

## 7. Fachreview statt Pseudogenauigkeit

Eine `confidence: 0.95` in historischen JSON-Beispielen ist keine empirisch kalibrierte Wahrscheinlichkeit. Wenn es keine definierte Kalibrierung und Ground-Truth-Daten gibt, besser `evidence_level` und `review_status` + erklärbare Regeln verwenden. Positive und negative Beispiele müssen Gegenmodelle enthalten; kulturelle Stiltraditionen können andere Regeln priorisieren. Fachliche Quellen sollten autoritative, peer-reviewte oder sorgfältig belegte Arbeiten von Foren-/Marketing-/Transkripten unterscheiden.

## 8. Nächste überprüfbare Liefergegenstände

- Ein `pitch_spelling`-Contract mit deutschen/internationalen Fixtures und belastbarer Fehlerbehandlung.
- Ein `chord`-Parser, dessen AST absolute und relative musikalische Attribute getrennt hält.
- Eine unveränderliche `ProgressionTimeline` mit Copy/Undo-Test, auch ohne GUI und Audio.
- Eine `harmony_analysis`-Schnittstelle, die *mehrere Interpretationen* statt eine einzelne Note zurückgeben kann.
- Ein `MIDI Export POC` mit 10 Gold-Dateien und unabhängiger Re-Import-Prüfung.
- Eine MusicTime-/Groove-Fixture für eine einfache 4/4 Drumprogression, **ohne** daraus einen beschlossenen MVP-Termin abzuleiten.
- Ein fachliches Reviewprotokoll, das Theoriemodell, Datenquelle, Regel-ID und Gegenbeispiel zurückverfolgt.

**Abnahme:** keine Fachregel ohne Test und kenntlich gemachten Kontext; keine öffentliche Quelle ohne Rechteprüfung; keine Audio-/Dateifunktion ohne Round-trip und Failure-Beleg.
