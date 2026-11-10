# Prüf- und Gegenbeispielkatalog V5.4

Das folgende Register unterscheidet **hard** (automatisierbare Invarianten), **interpretation** (musikalische Lesart) und **heuristic** (stilabhängiger Vorschlag). Die Regeln sind Codex-Testspezifikationen, nicht alle bereits im Steps-Repository implementiert.

### STEPS-R54-T01 — midi_pitch_range
**Typ:** `hard`. **Positivbedingung:** MIDI note 0..127. **Gegenbeispiel:** note=-1. **Quellenanker:** R12.

### STEPS-R54-T02 — midi_velocity_range
**Typ:** `hard`. **Positivbedingung:** positive note_on velocity 1..127; velocity 0 = off semantic. **Gegenbeispiel:** note_on=130. **Quellenanker:** R12.

### STEPS-R54-T03 — beat_duration
**Typ:** `hard`. **Positivbedingung:** duration beats >=0, note durations >0. **Gegenbeispiel:** negative duration. **Quellenanker:** R12.

### STEPS-R54-T04 — frequency_A4
**Typ:** `hard`. **Positivbedingung:** 12TET A440 MIDI69=440Hz. **Gegenbeispiel:** midi69=432 without a changed reference. **Quellenanker:** R12.

### STEPS-R54-T05 — octave_difference
**Typ:** `hard`. **Positivbedingung:** 12TET MIDI81/MIDI69=2. **Gegenbeispiel:** midi81=660Hz. **Quellenanker:** R12.

### STEPS-R54-T06 — enharmonic_id
**Typ:** `interpretation`. **Positivbedingung:** C# and Db may share pitch class but different spellings. **Gegenbeispiel:** force single spelling. **Quellenanker:** R01.

### STEPS-R54-T07 — interval_spelling
**Typ:** `interpretation`. **Positivbedingung:** d5 vs A4 differs by diatonic letters. **Gegenbeispiel:** infer interval only from semitones. **Quellenanker:** R01.

### STEPS-R54-T08 — roman_context
**Typ:** `interpretation`. **Positivbedingung:** ii/V depends on key & context. **Gegenbeispiel:** roman numeral without tonic lens. **Quellenanker:** R06.

### STEPS-R54-T09 — mode_evidence
**Typ:** `interpretation`. **Positivbedingung:** mode assignment needs centering/context. **Gegenbeispiel:** scale set alone implies mode. **Quellenanker:** R01.

### STEPS-R54-T10 — bar_duration
**Typ:** `hard`. **Positivbedingung:** meter 4/4=4 quarter beats per bar. **Gegenbeispiel:** 5 quarter beats in fixed 4/4 bar. **Quellenanker:** R10.

### STEPS-R54-T11 — tempo_positive
**Typ:** `hard`. **Positivbedingung:** BPM must be >0. **Gegenbeispiel:** BPM=0. **Quellenanker:** R12.

### STEPS-R54-T12 — swing_no_double_apply
**Typ:** `hard`. **Positivbedingung:** when committed=True no second base groove applied. **Gegenbeispiel:** duplicate groove twice. **Quellenanker:** R13.

### STEPS-R54-T13 — swing_label
**Typ:** `interpretation`. **Positivbedingung:** numeric swing timing has definition, no universal label. **Gegenbeispiel:** infer MPC preset from percent only. **Quellenanker:** R13.

### STEPS-R54-T14 — velocity_vs_loudness
**Typ:** `interpretation`. **Positivbedingung:** velocity not equal acoustical dB across sample patches. **Gegenbeispiel:** convert velocity110 to fixed dB. **Quellenanker:** R12.

### STEPS-R54-T15 — note_off_vs_audio_end
**Typ:** `interpretation`. **Positivbedingung:** MIDI gate is not sampler audible tail. **Gegenbeispiel:** equal note-off and end-of-audio. **Quellenanker:** R12.

### STEPS-R54-T16 — true_peak_vs_sample_peak
**Typ:** `hard`. **Positivbedingung:** true peak and sample peak are distinct metrics. **Gegenbeispiel:** always assert equality. **Quellenanker:** R16.

### STEPS-R54-T17 — ebu_scope
**Typ:** `interpretation`. **Positivbedingung:** EBU R128 -23LUFS is broadcast target not every music genre. **Gegenbeispiel:** force -23 for club masters. **Quellenanker:** R15.

### STEPS-R54-T18 — source_reuse
**Typ:** `hard`. **Positivbedingung:** license status required before copying protected data. **Gegenbeispiel:** private PPR MIDI redistributed by default. **Quellenanker:** R19.

### STEPS-R54-T19 — corpus_group_split
**Typ:** `hard`. **Positivbedingung:** same work_id must not appear in train and test. **Gegenbeispiel:** duplicate work in both. **Quellenanker:** R17.

### STEPS-R54-T20 — v5_archive_preserved
**Typ:** `hard`. **Positivbedingung:** all V5.3 old file SHA256 bytes unchanged. **Gegenbeispiel:** old file overwritten. **Quellenanker:** R12.

### STEPS-R54-T21 — voice_leading_lens
**Typ:** `heuristic`. **Positivbedingung:** parallel octaves flagged only when style scope warrants. **Gegenbeispiel:** universal prohibition. **Quellenanker:** R09.

### STEPS-R54-T22 — blues_dominant
**Typ:** `interpretation`. **Positivbedingung:** blues I7 not automatically V7/IV. **Gegenbeispiel:** all sevenths dominant function. **Quellenanker:** R05.

### STEPS-R54-T23 — progression_quality
**Typ:** `heuristic`. **Positivbedingung:** ranking weights transparent to user. **Gegenbeispiel:** rank=absolute aesthetic truth. **Quellenanker:** R05.

### STEPS-R54-T24 — analysis_multilens
**Typ:** `hard`. **Positivbedingung:** ambiguous loop may store >1 analysis. **Gegenbeispiel:** discard alternate parse. **Quellenanker:** R04.

### STEPS-R54-T25 — source_read_status
**Typ:** `hard`. **Positivbedingung:** abstract-only access is not full-text review. **Gegenbeispiel:** mark book as read. **Quellenanker:** R03.

### STEPS-R54-T26 — pitch_class_math
**Typ:** `hard`. **Positivbedingung:** pitch class = midi %12. **Gegenbeispiel:** midi60 mapped to pitch class 1. **Quellenanker:** R12.

### STEPS-R54-T27 — bar_16_step
**Typ:** `hard`. **Positivbedingung:** 4/4 with 16th grid has 16 steps. **Gegenbeispiel:** 12 steps with 4/4/16th mapping. **Quellenanker:** R12.

### STEPS-R54-T28 — mixed_meter
**Typ:** `hard`. **Positivbedingung:** use explicit beats/quarter conversion for 6/8. **Gegenbeispiel:** 6/8 always six quarter beats. **Quellenanker:** R01.

### STEPS-R54-T29 — chord_root_bass
**Typ:** `hard`. **Positivbedingung:** slash bass separate from chord root. **Gegenbeispiel:** G/B root changed to B. **Quellenanker:** R08.

### STEPS-R54-T30 — mei_musicxml_scope
**Typ:** `interpretation`. **Positivbedingung:** MusicXML and MEI exchange different semantic metadata. **Gegenbeispiel:** lossless guarantee across both. **Quellenanker:** R10.

### STEPS-R54-T31 — song_form_lens
**Typ:** `interpretation`. **Positivbedingung:** rock/pop form model not identical to Caplin classical. **Gegenbeispiel:** map all chorus to classical cadence. **Quellenanker:** R03.

### STEPS-R54-T32 — copyright_aggregator
**Typ:** `hard`. **Positivbedingung:** ChoCo licenses evaluated per source subset. **Gegenbeispiel:** blanket CC claim. **Quellenanker:** R18.
