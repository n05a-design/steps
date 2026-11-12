# Python-API von STEPS

Erzeugt mit `python scripts/render_api_reference.py`.
Der [Implementierungsstand](../IMPLEMENTATION.md) beschreibt Grenzen und Beispiele.

- Repository-Version `0.0.0-dev`
- Paketversion `0.0.0.dev0`

## `src.steps.theory`

| Export | Signatur |
|---|---|
| [`MusicTheoryError`](../../src/steps/theory/exceptions.py) | Ausnahmetyp |
| [`InvalidPitchClassError`](../../src/steps/theory/exceptions.py) | Ausnahmetyp |
| [`InvalidDiatonicStepError`](../../src/steps/theory/exceptions.py) | Ausnahmetyp |
| [`InvalidAlterationError`](../../src/steps/theory/exceptions.py) | Ausnahmetyp |
| [`PitchRangeError`](../../src/steps/theory/exceptions.py) | Ausnahmetyp |
| [`InvalidIntervalError`](../../src/steps/theory/exceptions.py) | Ausnahmetyp |
| [`ChordConstructionError`](../../src/steps/theory/exceptions.py) | Ausnahmetyp |
| [`VoiceLeadingError`](../../src/steps/theory/exceptions.py) | Ausnahmetyp |
| [`ProgressionParsingError`](../../src/steps/theory/exceptions.py) | Ausnahmetyp |
| [`PitchClass`](../../src/steps/theory/pitch.py) | `(val: 'int')` |
| [`NoteSpelling`](../../src/steps/theory/pitch.py) | `(step: "Literal['C', 'D', 'E', 'F', 'G', 'A', 'B']", alteration: 'int' = 0, octave: 'int' = 4) -> None` |
| [`midi_to_pitch_class`](../../src/steps/theory/pitch.py) | `(midi_note: 'int') -> 'PitchClass'` |
| [`midi_to_frequency`](../../src/steps/theory/pitch.py) | `(midi_note: 'int', a4_ref: 'float' = 440.0) -> 'float'` |
| [`frequency_to_midi`](../../src/steps/theory/pitch.py) | `(freq: 'float', a4_ref: 'float' = 440.0) -> 'float'` |
| [`parse_spelling`](../../src/steps/theory/pitch.py) | `(note_str: 'str', convention: "Literal['INT', 'DE', 'AUTO']" = 'AUTO') -> 'NoteSpelling'` |
| [`ChromaticInterval`](../../src/steps/theory/interval.py) | `PERFECT_UNISON`, `MINOR_SECOND`, `MAJOR_SECOND`, `MINOR_THIRD`, `MAJOR_THIRD`, `PERFECT_FOURTH`, `TRITONE`, `PERFECT_FIFTH`, `MINOR_SIXTH`, `MAJOR_SIXTH`, `MINOR_SEVENTH`, `MAJOR_SEVENTH`, `PERFECT_OCTAVE`, `MINOR_NINTH`, `MAJOR_NINTH`, `AUGMENTED_NINTH`, `PERFECT_ELEVENTH`, `AUGMENTED_ELEVENTH`, `MINOR_THIRTEENTH`, `MAJOR_THIRTEENTH` |
| [`DiatonicInterval`](../../src/steps/theory/interval.py) | `(number: 'int', quality: 'IntervalQuality', direction: 'Literal[1, -1]' = 1) -> None` |
| [`semitones_between`](../../src/steps/theory/interval.py) | `(note_a: 'int', note_b: 'int') -> 'int'` |
| [`directed_semitones`](../../src/steps/theory/interval.py) | `(note_from: 'int', note_to: 'int') -> 'int'` |
| [`invert_semitones_modulo12`](../../src/steps/theory/interval.py) | `(semitones: 'int') -> 'int'` |
| [`transpose_spelling`](../../src/steps/theory/interval.py) | `(spelling: 'NoteSpelling', interval: 'DiatonicInterval', direction: 'Literal[1, -1]' = 1) -> 'NoteSpelling'` |
| [`interval_between_spellings`](../../src/steps/theory/interval.py) | `(spelling_a: 'NoteSpelling', spelling_b: 'NoteSpelling') -> 'DiatonicInterval'` |
| [`TriadQuality`](../../src/steps/theory/triad.py) | `MAJOR`, `MINOR`, `DIMINISHED`, `AUGMENTED`, `SUS4`, `SUS2`, `ADD9` |
| [`construct_triad`](../../src/steps/theory/triad.py) | `(root: 'int \| PitchClass', quality: 'TriadQuality') -> 'list[PitchClass]'` |
| [`invert_triad_voicing`](../../src/steps/theory/triad.py) | `(voicing_midi: 'list[int]', inversion: 'int') -> 'list[int]'` |
| [`get_triad_pitch_class_set`](../../src/steps/theory/triad.py) | `(root: 'int \| PitchClass', quality: 'TriadQuality') -> 'set[int]'` |
| [`SeventhQuality`](../../src/steps/theory/seventh.py) | `DOMINANT_SEVENTH`, `MAJOR_SEVENTH`, `MINOR_SEVENTH`, `HALF_DIMINISHED`, `DIMINISHED_SEVENTH`, `MINOR_MAJOR_SEVENTH`, `LYDIAN_DOMINANT` |
| [`construct_seventh`](../../src/steps/theory/seventh.py) | `(root: 'int \| PitchClass', quality: 'SeventhQuality', full_theoretical: 'bool' = False) -> 'list[PitchClass]'` |
| [`invert_seventh_voicing`](../../src/steps/theory/seventh.py) | `(voicing_midi: 'list[int]', inversion: 'int') -> 'list[int]'` |
| [`make_drop2_voicing`](../../src/steps/theory/seventh.py) | `(close_voicing_midi: 'list[int]') -> 'list[int]'` |
| [`make_shell_voicing`](../../src/steps/theory/seventh.py) | `(root_midi: 'int', quality: 'SeventhQuality') -> 'tuple[int, tuple[int, int]]'` |
| [`ChordDefinition`](../../src/steps/theory/chord.py) | `(root: 'NoteSpelling', quality: 'str', bass: 'Optional[NoteSpelling]' = None) -> None` |
| [`Voicing`](../../src/steps/theory/chord.py) | `(notes: 'tuple[int, ...]', voicing_type: "Literal['CLOSE', 'DROP2', 'SHELL', 'ROOTLESS', 'OPEN', 'CUSTOM']" = 'CLOSE', bass_override: 'Optional[int]' = None) -> None` |
| [`parse_chord`](../../src/steps/theory/chord.py) | `(symbol: 'str', convention: "Literal['INT', 'DE', 'AUTO']" = 'AUTO') -> 'ChordDefinition'` |
| [`CHORD_TEMPLATES`](../../src/steps/theory/__init__.py) | Datenwert |

## `src.steps.progression`

| Export | Signatur |
|---|---|
| [`VoiceLeadingStyle`](../../src/steps/progression/voice_leading.py) | `STRICT_COUNTERPOINT`, `JAZZ_POP` |
| [`absolute_semitone_distance`](../../src/steps/progression/voice_leading.py) | `(voicing_a: 'list[int]', voicing_b: 'list[int]') -> 'int'` |
| [`circular_pc_distance`](../../src/steps/progression/voice_leading.py) | `(voicing_a: 'list[int]', voicing_b: 'list[int]') -> 'int'` |
| [`detect_voice_crossing`](../../src/steps/progression/voice_leading.py) | `(voicing: 'list[int]') -> 'bool'` |
| [`detect_voice_overlap`](../../src/steps/progression/voice_leading.py) | `(voicing_a: 'list[int]', voicing_b: 'list[int]') -> 'bool'` |
| [`detect_parallel_fifths_octaves`](../../src/steps/progression/voice_leading.py) | `(chord_a: 'list[int]', chord_b: 'list[int]', style: 'VoiceLeadingStyle' = <VoiceLeadingStyle.STRICT_COUNTERPOINT: 'STRICT_COUNTERPOINT'>) -> 'list[str]'` |
| [`guide_tone_resolution`](../../src/steps/progression/voice_leading.py) | `(seventh_midi: 'int', target_third_midi: 'int') -> 'int'` |
| [`optimize_smooth_voice_leading`](../../src/steps/progression/voice_leading.py) | `(source_voicing: 'list[int]', target_pcs: 'set[int] \| list[int]', bass_pc: 'Optional[int]' = None, style: 'VoiceLeadingStyle' = <VoiceLeadingStyle.JAZZ_POP: 'JAZZ_POP'>) -> 'list[int]'` |
| [`CanonicalProgression`](../../src/steps/progression/engine.py) | `(prog_id: 'str', name: 'str', roman_numerals: 'str', default_key: 'str', chords_str: 'str', context: 'str', sources: 'str') -> None` |
| [`CANONICAL_PROGRESSIONS`](../../src/steps/progression/__init__.py) | Datenwert |
| [`get_progression`](../../src/steps/progression/engine.py) | `(prog_id: 'str') -> 'CanonicalProgression'` |
| [`list_progressions`](../../src/steps/progression/engine.py) | `() -> 'list[CanonicalProgression]'` |
| [`resolve_roman_degree`](../../src/steps/progression/engine.py) | `(degree_str: 'str', key_root: 'str \| NoteSpelling' = 'C', is_minor_key: 'bool' = False, *, convention: "Literal['INT', 'DE', 'AUTO']" = 'AUTO') -> 'ChordDefinition'` |
| [`generate_progression_voicings`](../../src/steps/progression/engine.py) | `(chords: 'list[ChordDefinition] \| CanonicalProgression', style: 'VoiceLeadingStyle' = <VoiceLeadingStyle.JAZZ_POP: 'JAZZ_POP'>, initial_voicing_type: "Literal['CLOSE', 'DROP2', 'SHELL', 'ROOTLESS']" = 'CLOSE', bass_octave: 'int' = 3) -> 'list[Voicing]'` |
| [`analyze_progression_voice_leading`](../../src/steps/progression/engine.py) | `(voicings: 'list[Voicing]', style: 'VoiceLeadingStyle' = <VoiceLeadingStyle.JAZZ_POP: 'JAZZ_POP'>) -> 'Dict[str, Any]'` |

## `app.knowledge`

| Export | Signatur |
|---|---|
| [`get_reviewed_progression`](../../src/steps/progression/engine.py) | `(prog_id: 'str') -> 'ReviewedProgression'` |
| [`list_reviewed_progressions`](../../src/steps/progression/engine.py) | `() -> 'tuple[ReviewedProgression, ...]'` |

## Domänenobjekte

### [ReviewedProgression](../../src/steps/progression/engine.py)

`ReviewedProgression(progression: 'CanonicalProgression', lesson: 'str', source_ids: 'tuple[str, ...]', reviewed_on: 'str') -> None`

### [NoteSpelling](../../src/steps/theory/pitch.py)

`NoteSpelling(step: "Literal['C', 'D', 'E', 'F', 'G', 'A', 'B']", alteration: 'int' = 0, octave: 'int' = 4) -> None`

- `pitch_class` (Eigenschaft)
- `midi_number` (Eigenschaft)
- `frequency` (Eigenschaft)
- `is_enharmonic_with(self, other: 'NoteSpelling', ignore_octave: 'bool' = False) -> 'bool'`
- `transpose_diatonic(self, step_delta: 'int', semitone_delta: 'int') -> 'NoteSpelling'`
- `transpose_chromatic(self, semitones: 'int') -> 'NoteSpelling'`
- `render(self, convention: "Literal['INT', 'DE']" = 'INT', unicode_accidental: 'bool' = False) -> 'str'`

### [DiatonicInterval](../../src/steps/theory/interval.py)

`DiatonicInterval(number: 'int', quality: 'IntervalQuality', direction: 'Literal[1, -1]' = 1) -> None`

- `is_compound` (Eigenschaft)
- `octaves` (Eigenschaft)
- `semitones` (Eigenschaft)
- `signed_semitones` (Eigenschaft)
- `invert(self) -> 'DiatonicInterval'`

### [ChordDefinition](../../src/steps/theory/chord.py)

`ChordDefinition(root: 'NoteSpelling', quality: 'str', bass: 'Optional[NoteSpelling]' = None) -> None`

- `template` (Eigenschaft)
- `theoretical_intervals` (Eigenschaft)
- `default_voiced_intervals` (Eigenschaft)
- `theoretical_pitch_classes` (Eigenschaft)
- `pitch_class_set` (Eigenschaft)
- `voiced_pitch_classes` (Eigenschaft)
- `category` (Eigenschaft)
- `is_triad` (Eigenschaft)
- `is_seventh` (Eigenschaft)
- `is_extended` (Eigenschaft)
- `symbol` (Eigenschaft)
- `contains_pitch_class(self, pc: 'int | PitchClass') -> 'bool'`
- `to_voicing(self, bass_octave: 'int' = 3, voicing_type: "Literal['CLOSE', 'DROP2', 'SHELL', 'ROOTLESS']" = 'CLOSE') -> 'Voicing'`

### [Voicing](../../src/steps/theory/chord.py)

`Voicing(notes: 'tuple[int, ...]', voicing_type: "Literal['CLOSE', 'DROP2', 'SHELL', 'ROOTLESS', 'OPEN', 'CUSTOM']" = 'CLOSE', bass_override: 'Optional[int]' = None) -> None`

- `midi_notes` (Eigenschaft)
- `bass_note` (Eigenschaft)
- `soprano_note` (Eigenschaft)
- `transpose(self, semitones: 'int') -> 'Voicing'`
- `invert(self, inversion: 'int') -> 'Voicing'`

### [CanonicalProgression](../../src/steps/progression/engine.py)

`CanonicalProgression(prog_id: 'str', name: 'str', roman_numerals: 'str', default_key: 'str', chords_str: 'str', context: 'str', sources: 'str') -> None`

- `chord_definitions` (Eigenschaft)
- `transpose(self, semitones: 'int') -> 'list[ChordDefinition]'`

## Akkordqualitäten

Intervalle sind Halbtöne relativ zum Akkordgrundton. `CLOSE` verwendet
die Standardintervalle unter Berücksichtigung des expliziten Basses.

| Qualität | Aliasse | Theoretische Intervalle | Standardintervalle |
|---|---|---|---|
| `(leer)` | `maj`, `M` | `(0, 4, 7)` | `(0, 4, 7)` |
| `m` | `m`, `min`, `-` | `(0, 3, 7)` | `(0, 3, 7)` |
| `dim` | `dim`, `o`, `°` | `(0, 3, 6)` | `(0, 3, 6)` |
| `aug` | `aug`, `+` | `(0, 4, 8)` | `(0, 4, 8)` |
| `sus4` | `sus4`, `sus` | `(0, 5, 7)` | `(0, 5, 7)` |
| `sus2` | `sus2` | `(0, 2, 7)` | `(0, 2, 7)` |
| `add9` | `add9`, `add2` | `(0, 2, 4, 7)` | `(0, 2, 4, 7)` |
| `6` | `6`, `maj6` | `(0, 4, 7, 9)` | `(0, 4, 7, 9)` |
| `m6` | `m6`, `min6`, `-6` | `(0, 3, 7, 9)` | `(0, 3, 7, 9)` |
| `7` | `7`, `dom7` | `(0, 4, 7, 10)` | `(0, 4, 7, 10)` |
| `maj7` | `maj7`, `^7`, `M7`, `Δ`, `Δ7` | `(0, 4, 7, 11)` | `(0, 4, 7, 11)` |
| `m7` | `m7`, `min7`, `-7` | `(0, 3, 7, 10)` | `(0, 3, 7, 10)` |
| `m7b5` | `m7b5`, `-7b5`, `ø`, `ø7`, `half-dim` | `(0, 3, 6, 10)` | `(0, 3, 6, 10)` |
| `dim7` | `dim7`, `o7`, `°7` | `(0, 3, 6, 9)` | `(0, 3, 6, 9)` |
| `m(maj7)` | `m(maj7)`, `mmaj7`, `m^7`, `-^7`, `minmaj7` | `(0, 3, 7, 11)` | `(0, 3, 7, 11)` |
| `7#5` | `7#5`, `7aug`, `7+` | `(0, 4, 8, 10)` | `(0, 4, 8, 10)` |
| `maj7#5` | `maj7#5`, `^7#5`, `maj7+` | `(0, 4, 8, 11)` | `(0, 4, 8, 11)` |
| `7sus4` | `7sus4`, `7sus` | `(0, 5, 7, 10)` | `(0, 5, 7, 10)` |
| `9` | `9`, `dom9` | `(0, 4, 7, 10, 14)` | `(0, 4, 10, 14)` |
| `maj9` | `maj9`, `^9`, `M9`, `Δ9` | `(0, 4, 7, 11, 14)` | `(0, 4, 11, 14)` |
| `m9` | `m9`, `min9`, `-9` | `(0, 3, 7, 10, 14)` | `(0, 3, 10, 14)` |
| `7b9` | `7b9`, `7(b9)`, `dom7b9` | `(0, 4, 7, 10, 13)` | `(0, 4, 10, 13)` |
| `7#9` | `7#9`, `7(#9)`, `dom7#9`, `hendrix` | `(0, 4, 7, 10, 15)` | `(0, 4, 10, 15)` |
| `7#11` | `7#11`, `7(#11)`, `lydian_dom` | `(0, 4, 6, 7, 10)` | `(0, 4, 6, 10)` |
| `7b5` | `7b5`, `7(b5)` | `(0, 4, 6, 10)` | `(0, 4, 6, 10)` |
| `7b13` | `7b13`, `7(b13)` | `(0, 4, 7, 10, 20)` | `(0, 4, 10, 20)` |
| `13` | `13`, `dom13` | `(0, 4, 7, 10, 14, 21)` | `(0, 4, 10, 14, 21)` |
| `maj13` | `maj13`, `^13`, `M13` | `(0, 4, 7, 11, 14, 21)` | `(0, 4, 11, 14, 21)` |
| `m11` | `m11`, `min11`, `-11` | `(0, 3, 7, 10, 14, 17)` | `(0, 3, 10, 14, 17)` |
