# Python-API von STEPS

Erzeugt mit `python scripts/render_api_reference.py`.
Der [Implementierungsstand](../IMPLEMENTATION.md) beschreibt Grenzen und Beispiele.

- Repository-Version `0.3.0-dev`
- Paketversion `0.3.0.dev0`

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
| [`ScaleConstructionError`](../../src/steps/theory/exceptions.py) | Ausnahmetyp |
| [`PitchClass`](../../src/steps/theory/pitch.py) | `(val: 'int')` |
| [`NoteSpelling`](../../src/steps/theory/pitch.py) | `(step: "Literal['C', 'D', 'E', 'F', 'G', 'A', 'B']", alteration: 'int' = 0, octave: 'int' = 4) -> None` |
| [`midi_to_pitch_class`](../../src/steps/theory/pitch.py) | `(midi_note: 'int') -> 'PitchClass'` |
| [`midi_to_frequency`](../../src/steps/theory/pitch.py) | `(midi_note: 'int \| float', a4_ref: 'float' = 440.0) -> 'float'` |
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
| [`ModeCategory`](../../src/steps/theory/scale.py) | `DIATONIC_MAJOR`, `DIATONIC_MINOR`, `MELODIC_MINOR`, `HARMONIC_MINOR`, `PENTATONIC`, `BLUES`, `SYMMETRIC` |
| [`ScaleTemplate`](../../src/steps/theory/scale.py) | `(name: 'str', aliases: 'tuple[str, ...]', intervals: 'tuple[int, ...]', category: 'ModeCategory', characteristic_intervals: 'tuple[int, ...]', avoid_notes: 'tuple[int, ...]', triad_qualities: 'tuple[str, ...]', seventh_qualities: 'tuple[str, ...]') -> None` |
| [`ScaleDefinition`](../../src/steps/theory/scale.py) | `(root: 'NoteSpelling', template: 'ScaleTemplate', spellings: 'tuple[NoteSpelling, ...]') -> None` |
| [`SCALE_TEMPLATES`](../../src/steps/theory/__init__.py) | Datenwert |
| [`get_scale_template`](../../src/steps/theory/scale.py) | `(name_or_alias: 'str') -> 'Optional[ScaleTemplate]'` |
| [`construct_scale`](../../src/steps/theory/scale.py) | `(root: 'NoteSpelling', template_or_name: 'ScaleTemplate \| str') -> 'ScaleDefinition'` |
| [`parse_scale`](../../src/steps/theory/scale.py) | `(text: 'str', convention: "Literal['INT', 'DE', 'AUTO']" = 'AUTO') -> 'ScaleDefinition'` |
| [`ChordInversion`](../../src/steps/theory/inversion.py) | `ROOT_POSITION`, `FIRST_INVERSION`, `SECOND_INVERSION`, `THIRD_INVERSION` |
| [`FiguredBassSymbol`](../../src/steps/theory/inversion.py) | `TRIAD_ROOT`, `TRIAD_FIRST`, `TRIAD_SECOND`, `SEVENTH_ROOT`, `SEVENTH_FIRST`, `SEVENTH_SECOND`, `SEVENTH_THIRD` |
| [`InversionAnalysis`](../../src/steps/theory/inversion.py) | `(inversion: 'ChordInversion', figured_bass: 'str', bass_factor: 'str', root_pc: 'int', bass_pc: 'int', german_name: 'str', is_seventh_chord: 'bool') -> None` |
| [`detect_chord_inversion`](../../src/steps/theory/inversion.py) | `(notes: 'Union[List[int], Tuple[int, ...], Voicing]', root_pitch_class: 'Optional[int]' = None, is_seventh: 'Optional[bool]' = None) -> 'InversionAnalysis'` |
| [`detect_hand_voicing`](../../src/steps/theory/inversion.py) | `(hand_notes: 'Union[List[int], Tuple[int, ...], Voicing]', separate_bass_note: 'Optional[int]' = None, root_pitch_class: 'Optional[int]' = None) -> 'dict[str, Any]'` |
| [`GuideToneResolution`](../../src/steps/theory/voicings.py) | `(from_chord: 'str', to_chord: 'str', retained_note: 'Optional[int]', moving_note_from: 'int', moving_note_to: 'int', motion_semitones: 'int', resolution_type: "Literal['HALF_STEP_DOWN', 'HALF_STEP_UP', 'WHOLE_STEP_DOWN', 'WHOLE_STEP_UP', 'STATIC', 'LEAP']", total_l1_distance: 'int', description: 'str') -> None` |
| [`ProgressionShellVoicings`](../../src/steps/theory/voicings.py) | `(voicings: 'List[ShellVoicing]', resolutions: 'List[GuideToneResolution]', total_l1_distance: 'int', average_l1_distance: 'float', starting_layout: "Literal['7_3', '3_7']") -> None` |
| [`ShellVoicing`](../../src/steps/theory/voicings.py) | `(chord_symbol: 'str', root_pc: 'int', bass_note: 'int', guide_tones: 'Tuple[int, int]', third_note: 'int', seventh_note: 'int', layout: "Literal['7_3', '3_7']", lh_spelling: 'str', rh_spellings: 'Tuple[str, str]') -> None` |
| [`extract_guide_tone_pcs`](../../src/steps/theory/voicings.py) | `(chord: 'ChordDefinition') -> 'Tuple[int, int]'` |
| [`generate_shell_voicings`](../../src/steps/theory/voicings.py) | `(progression: 'Union[str, List[str], Any, List[ChordDefinition]]', key_root: 'str' = 'C', starting_layout: "Literal['7_3', '3_7', 'AUTO']" = 'AUTO', bass_octave: 'int' = 2, rh_octave: 'int' = 4, convention: "Literal['INT', 'DE']" = 'INT') -> 'ProgressionShellVoicings'` |
| [`BeginnerTriadInversion`](../../src/steps/theory/beginner_voicing.py) | `ROOT`, `FIRST`, `SECOND` |
| [`PedagogicalReduction`](../../src/steps/theory/beginner_voicing.py) | `(original_symbol: 'str', reduced_symbol: 'str', was_reduced: 'bool', omitted_factors: 'Tuple[str, ...]', explanation: 'str') -> None` |
| [`BeginnerChordVoicing`](../../src/steps/theory/beginner_voicing.py) | `(chord_symbol: 'str', reduced_symbol: 'str', inversion: 'BeginnerTriadInversion', lh_bass_note: 'int', lh_fingering: 'int', lh_spelling: 'str', rh_notes: 'Tuple[int, int, int]', rh_fingering: 'Tuple[int, int, int]', rh_spellings: 'Tuple[str, str, str]', rh_span_semitones: 'int', pedagogical_description: 'str', reduction: 'PedagogicalReduction') -> None` |
| [`BeginnerVoiceLeadingTransition`](../../src/steps/theory/beginner_voicing.py) | `(from_chord: 'str', to_chord: 'str', common_tones: 'Tuple[int, ...]', moving_voices: 'Tuple[Tuple[int, int, int], ...]', total_l1_distance: 'int', max_single_leap: 'int', has_hand_jump: 'bool', pedagogical_guidance: 'str', is_canonical_guidance: 'bool' = False) -> None` |
| [`BeginnerProgressionVoicings`](../../src/steps/theory/beginner_voicing.py) | `(voicings: 'List[BeginnerChordVoicing]', transitions: 'List[BeginnerVoiceLeadingTransition]', total_l1_distance: 'int', average_l1_distance: 'float', smoothness_score: 'float', has_any_hand_jumps: 'bool', movement_reduction_vs_root_percent: 'float') -> None` |
| [`reduce_chord_for_beginners`](../../src/steps/theory/beginner_voicing.py) | `(chord: 'Union[str, ChordDefinition]', convention: "Literal['INT', 'DE']" = 'INT') -> 'PedagogicalReduction'` |
| [`generate_beginner_inversions`](../../src/steps/theory/beginner_voicing.py) | `(chord: 'Union[str, ChordDefinition]', target_octave: 'int' = 4, convention: "Literal['INT', 'DE']" = 'INT') -> 'List[Tuple[BeginnerTriadInversion, Tuple[int, int, int]]]'` |
| [`determine_beginner_fingering`](../../src/steps/theory/beginner_voicing.py) | `(rh_notes: 'Tuple[int, int, int]', inversion: 'BeginnerTriadInversion', prev_rh_notes: 'Optional[Tuple[int, int, int]]' = None, chord_symbol: 'str' = '') -> 'Tuple[int, int, int]'` |
| [`generate_beginner_voicings`](../../src/steps/theory/beginner_voicing.py) | `(progression: 'Union[str, List[str], Any, List[ChordDefinition]]', starting_inversion: 'Optional[Union[str, BeginnerTriadInversion]]' = None, lh_octave: 'int' = 2, rh_octave: 'int' = 4, convention: "Literal['INT', 'DE']" = 'INT') -> 'BeginnerProgressionVoicings'` |
| [`VoiceLeadingStyle`](../../src/steps/theory/voice_leading.py) | `STRICT_CLASSICAL`, `STRICT_COUNTERPOINT`, `CONTEMPORARY_POP`, `JAZZ_POP`, `POWER_CHORDS`, `QUARTAL_JAZZ` |
| [`ContrapuntalMotion`](../../src/steps/theory/voice_leading.py) | `PARALLEL`, `SIMILAR`, `CONTRARY`, `OBLIQUE`, `STATIC` |
| [`VoiceLeadingViolation`](../../src/steps/theory/voice_leading.py) | `(rule_name: 'str', voice_indices: 'Tuple[int, int]', motion_type: 'str', pitch_interval: 'int', from_pitches: 'Tuple[int, int]', to_pitches: 'Tuple[int, int]', severity: "Literal['ERROR', 'WARNING', 'INFO']", explanation: 'str', stylistic_context: 'str') -> None` |
| [`VoiceLeadingEvaluation`](../../src/steps/theory/voice_leading.py) | `(from_voicing: 'Tuple[int, ...]', to_voicing: 'Tuple[int, ...]', style: 'VoiceLeadingStyle', is_valid: 'bool', violations: 'List[VoiceLeadingViolation]', l1_distance: 'int', max_voice_leap: 'int', contrapuntal_motion: 'Dict[str, Any]', stylistic_notes: 'List[str]') -> None` |
| [`classify_voice_motion`](../../src/steps/theory/voice_leading.py) | `(v1_start: 'int', v1_end: 'int', v2_start: 'int', v2_end: 'int') -> 'ContrapuntalMotion'` |
| [`analyze_contrapuntal_motions`](../../src/steps/theory/voice_leading.py) | `(voicing_a: 'Union[List[int], Tuple[int, ...]]', voicing_b: 'Union[List[int], Tuple[int, ...]]') -> 'Dict[str, Any]'` |
| [`detect_parallel_fifths_octaves`](../../src/steps/theory/voice_leading.py) | `(chord_a: 'Union[List[int], Tuple[int, ...]]', chord_b: 'Union[List[int], Tuple[int, ...]]', style: 'Union[str, VoiceLeadingStyle]' = <VoiceLeadingStyle.STRICT_COUNTERPOINT: 'STRICT_COUNTERPOINT'>) -> 'List[str]'` |
| [`detect_voice_crossing`](../../src/steps/theory/voice_leading.py) | `(notes: 'Union[List[int], Tuple[int, ...]]') -> 'bool'` |
| [`detect_voice_overlap`](../../src/steps/theory/voice_leading.py) | `(voicing_a: 'Union[List[int], Tuple[int, ...]]', voicing_b: 'Union[List[int], Tuple[int, ...]]') -> 'bool'` |
| [`evaluate_voice_leading_transition`](../../src/steps/theory/voice_leading.py) | `(chord_a: 'Union[List[int], Tuple[int, ...]]', chord_b: 'Union[List[int], Tuple[int, ...]]', style: 'Union[str, VoiceLeadingStyle]' = <VoiceLeadingStyle.CONTEMPORARY_POP: 'CONTEMPORARY_POP'>) -> 'VoiceLeadingEvaluation'` |

## `src.steps.progression`

| Export | Signatur |
|---|---|
| [`ContrapuntalMotion`](../../src/steps/theory/voice_leading.py) | `PARALLEL`, `SIMILAR`, `CONTRARY`, `OBLIQUE`, `STATIC` |
| [`VoiceLeadingStyle`](../../src/steps/theory/voice_leading.py) | `STRICT_CLASSICAL`, `STRICT_COUNTERPOINT`, `CONTEMPORARY_POP`, `JAZZ_POP`, `POWER_CHORDS`, `QUARTAL_JAZZ` |
| [`VoiceLeadingViolation`](../../src/steps/theory/voice_leading.py) | `(rule_name: 'str', voice_indices: 'Tuple[int, int]', motion_type: 'str', pitch_interval: 'int', from_pitches: 'Tuple[int, int]', to_pitches: 'Tuple[int, int]', severity: "Literal['ERROR', 'WARNING', 'INFO']", explanation: 'str', stylistic_context: 'str') -> None` |
| [`VoiceLeadingEvaluation`](../../src/steps/theory/voice_leading.py) | `(from_voicing: 'Tuple[int, ...]', to_voicing: 'Tuple[int, ...]', style: 'VoiceLeadingStyle', is_valid: 'bool', violations: 'List[VoiceLeadingViolation]', l1_distance: 'int', max_voice_leap: 'int', contrapuntal_motion: 'Dict[str, Any]', stylistic_notes: 'List[str]') -> None` |
| [`absolute_semitone_distance`](../../src/steps/progression/voice_leading.py) | `(voicing_a: 'list[int]', voicing_b: 'list[int]') -> 'int'` |
| [`analyze_contrapuntal_motions`](../../src/steps/theory/voice_leading.py) | `(voicing_a: 'Union[List[int], Tuple[int, ...]]', voicing_b: 'Union[List[int], Tuple[int, ...]]') -> 'Dict[str, Any]'` |
| [`circular_pc_distance`](../../src/steps/progression/voice_leading.py) | `(voicing_a: 'list[int]', voicing_b: 'list[int]') -> 'int'` |
| [`classify_voice_motion`](../../src/steps/theory/voice_leading.py) | `(v1_start: 'int', v1_end: 'int', v2_start: 'int', v2_end: 'int') -> 'ContrapuntalMotion'` |
| [`detect_voice_crossing`](../../src/steps/theory/voice_leading.py) | `(notes: 'Union[List[int], Tuple[int, ...]]') -> 'bool'` |
| [`detect_voice_overlap`](../../src/steps/theory/voice_leading.py) | `(voicing_a: 'Union[List[int], Tuple[int, ...]]', voicing_b: 'Union[List[int], Tuple[int, ...]]') -> 'bool'` |
| [`detect_parallel_fifths_octaves`](../../src/steps/theory/voice_leading.py) | `(chord_a: 'Union[List[int], Tuple[int, ...]]', chord_b: 'Union[List[int], Tuple[int, ...]]', style: 'Union[str, VoiceLeadingStyle]' = <VoiceLeadingStyle.STRICT_COUNTERPOINT: 'STRICT_COUNTERPOINT'>) -> 'List[str]'` |
| [`evaluate_voice_leading_transition`](../../src/steps/theory/voice_leading.py) | `(chord_a: 'Union[List[int], Tuple[int, ...]]', chord_b: 'Union[List[int], Tuple[int, ...]]', style: 'Union[str, VoiceLeadingStyle]' = <VoiceLeadingStyle.CONTEMPORARY_POP: 'CONTEMPORARY_POP'>) -> 'VoiceLeadingEvaluation'` |
| [`guide_tone_resolution`](../../src/steps/progression/voice_leading.py) | `(seventh_midi: 'int', target_third_midi: 'int') -> 'int'` |
| [`optimize_smooth_voice_leading`](../../src/steps/progression/voice_leading.py) | `(source_voicing: 'list[int]', target_pcs: 'set[int] \| list[int]', bass_pc: 'Optional[int]' = None, style: 'VoiceLeadingStyle' = <VoiceLeadingStyle.JAZZ_POP: 'JAZZ_POP'>) -> 'list[int]'` |
| [`CanonicalProgression`](../../src/steps/progression/engine.py) | `(prog_id: 'str', name: 'str', roman_numerals: 'str', default_key: 'str', chords_str: 'str', context: 'str', sources: 'str') -> None` |
| [`CANONICAL_PROGRESSIONS`](../../src/steps/progression/__init__.py) | Datenwert |
| [`ARCHETYPE_THEORY_METADATA`](../../src/steps/progression/__init__.py) | Datenwert |
| [`get_progression`](../../src/steps/progression/engine.py) | `(prog_id: 'str') -> 'CanonicalProgression'` |
| [`list_progressions`](../../src/steps/progression/engine.py) | `() -> 'list[CanonicalProgression]'` |
| [`resolve_roman_degree`](../../src/steps/progression/engine.py) | `(degree_str: 'str', key_root: 'str \| NoteSpelling' = 'C', is_minor_key: 'bool' = False, *, convention: "Literal['INT', 'DE', 'AUTO']" = 'AUTO', minor_accidentals: "Literal['major_reference', 'natural_minor']" = 'major_reference') -> 'ChordDefinition'` |
| [`generate_progression_voicings`](../../src/steps/progression/engine.py) | `(chords: 'list[ChordDefinition] \| CanonicalProgression', style: 'VoiceLeadingStyle' = <VoiceLeadingStyle.JAZZ_POP: 'JAZZ_POP'>, initial_voicing_type: "Literal['CLOSE', 'DROP2', 'SHELL', 'ROOTLESS']" = 'CLOSE', bass_octave: 'int' = 3) -> 'list[Voicing]'` |
| [`analyze_progression_voice_leading`](../../src/steps/progression/engine.py) | `(voicings: 'list[Voicing]', style: 'VoiceLeadingStyle' = <VoiceLeadingStyle.JAZZ_POP: 'JAZZ_POP'>) -> 'Dict[str, Any]'` |
| [`detect_progression_archetypes`](../../src/steps/progression/engine.py) | `(chords: 'list[str] \| list[ChordDefinition] \| CanonicalProgression', key_root: 'str \| NoteSpelling' = 'C', is_minor_key: 'bool' = False, allow_rotations: 'bool' = True, convention: "Literal['INT', 'DE', 'AUTO']" = 'AUTO') -> 'list[dict[str, Any]]'` |
| [`ProgressionSession`](../../src/steps/progression/session.py) | `(initial_chords: 'Optional[List[str]]' = None, key_root: 'str' = 'C', is_minor: 'bool' = False, convention: "Literal['INT', 'DE']" = 'INT', bpm: 'float' = 120.0, voice_leading_style: 'Union[str, VoiceLeadingStyle]' = <VoiceLeadingStyle.CONTEMPORARY_POP: 'CONTEMPORARY_POP'>, title: 'Optional[str]' = None)` |
| [`ChordRecommendation`](../../src/steps/progression/session.py) | `(candidate_symbol: 'str', relation_type: "Literal['DOMINANT_OF', 'RESOLVES_TO', 'BORROWED_FROM', 'VOICE_LEADING_NEAR', 'SUBSTITUTES_FOR', 'ROOT_MOTION', 'SCHEMA_CONTINUATION']", explanation: 'str', framework: 'str', source_id: 'str \| None' = None, source_locator: 'str \| None' = None, evidence_kind: "Literal['CREATIVE_SUGGESTION', 'MODEL_RULE', 'LITERATURE_REFERENCE']" = 'CREATIVE_SUGGESTION', reason_key: 'str \| None' = None, source_symbol: 'str \| None' = None) -> None` |
| [`DegreeAnalysis`](../../src/steps/progression/session.py) | `(index: 'int', symbol: 'str', roman_numeral: 'str', semitone_distance_to_next: 'Optional[int]' = None, voice_leading_warnings: 'tuple[str, ...]' = (), voice_leading_diagnostics: 'tuple[VoiceLeadingDiagnostic, ...]' = ()) -> None` |
| [`GuideToneResolution`](../../src/steps/theory/voicings.py) | `(from_chord: 'str', to_chord: 'str', retained_note: 'Optional[int]', moving_note_from: 'int', moving_note_to: 'int', motion_semitones: 'int', resolution_type: "Literal['HALF_STEP_DOWN', 'HALF_STEP_UP', 'WHOLE_STEP_DOWN', 'WHOLE_STEP_UP', 'STATIC', 'LEAP']", total_l1_distance: 'int', description: 'str') -> None` |
| [`ProgressionShellVoicings`](../../src/steps/theory/voicings.py) | `(voicings: 'List[ShellVoicing]', resolutions: 'List[GuideToneResolution]', total_l1_distance: 'int', average_l1_distance: 'float', starting_layout: "Literal['7_3', '3_7']") -> None` |
| [`ShellVoicing`](../../src/steps/theory/voicings.py) | `(chord_symbol: 'str', root_pc: 'int', bass_note: 'int', guide_tones: 'Tuple[int, int]', third_note: 'int', seventh_note: 'int', layout: "Literal['7_3', '3_7']", lh_spelling: 'str', rh_spellings: 'Tuple[str, str]') -> None` |
| [`generate_shell_voicings`](../../src/steps/theory/voicings.py) | `(progression: 'Union[str, List[str], Any, List[ChordDefinition]]', key_root: 'str' = 'C', starting_layout: "Literal['7_3', '3_7', 'AUTO']" = 'AUTO', bass_octave: 'int' = 2, rh_octave: 'int' = 4, convention: "Literal['INT', 'DE']" = 'INT') -> 'ProgressionShellVoicings'` |
| [`BeginnerChordVoicing`](../../src/steps/theory/beginner_voicing.py) | `(chord_symbol: 'str', reduced_symbol: 'str', inversion: 'BeginnerTriadInversion', lh_bass_note: 'int', lh_fingering: 'int', lh_spelling: 'str', rh_notes: 'Tuple[int, int, int]', rh_fingering: 'Tuple[int, int, int]', rh_spellings: 'Tuple[str, str, str]', rh_span_semitones: 'int', pedagogical_description: 'str', reduction: 'PedagogicalReduction') -> None` |
| [`BeginnerProgressionVoicings`](../../src/steps/theory/beginner_voicing.py) | `(voicings: 'List[BeginnerChordVoicing]', transitions: 'List[BeginnerVoiceLeadingTransition]', total_l1_distance: 'int', average_l1_distance: 'float', smoothness_score: 'float', has_any_hand_jumps: 'bool', movement_reduction_vs_root_percent: 'float') -> None` |
| [`BeginnerTriadInversion`](../../src/steps/theory/beginner_voicing.py) | `ROOT`, `FIRST`, `SECOND` |
| [`BeginnerVoiceLeadingTransition`](../../src/steps/theory/beginner_voicing.py) | `(from_chord: 'str', to_chord: 'str', common_tones: 'Tuple[int, ...]', moving_voices: 'Tuple[Tuple[int, int, int], ...]', total_l1_distance: 'int', max_single_leap: 'int', has_hand_jump: 'bool', pedagogical_guidance: 'str', is_canonical_guidance: 'bool' = False) -> None` |
| [`PedagogicalReduction`](../../src/steps/theory/beginner_voicing.py) | `(original_symbol: 'str', reduced_symbol: 'str', was_reduced: 'bool', omitted_factors: 'Tuple[str, ...]', explanation: 'str') -> None` |
| [`generate_beginner_voicings`](../../src/steps/theory/beginner_voicing.py) | `(progression: 'Union[str, List[str], Any, List[ChordDefinition]]', starting_inversion: 'Optional[Union[str, BeginnerTriadInversion]]' = None, lh_octave: 'int' = 2, rh_octave: 'int' = 4, convention: "Literal['INT', 'DE']" = 'INT') -> 'BeginnerProgressionVoicings'` |
| [`reduce_chord_for_beginners`](../../src/steps/theory/beginner_voicing.py) | `(chord: 'Union[str, ChordDefinition]', convention: "Literal['INT', 'DE']" = 'INT') -> 'PedagogicalReduction'` |
| [`BasslineModel`](../../src/steps/progression/recommender.py) | `(name: 'str', style_category: 'str', description: 'str', time_signature: 'Tuple[int, int]', tempo_range: 'Tuple[int, int]', pattern_description: 'str', evidence_status: "Literal['CREATIVE_SUGGESTION']" = 'CREATIVE_SUGGESTION') -> None` |
| [`CANONICAL_BASSLINE_MODELS`](../../src/steps/progression/__init__.py) | Datenwert |
| [`CANONICAL_DRUM_PATTERNS`](../../src/steps/progression/__init__.py) | Datenwert |
| [`CANONICAL_PIANO_MODULES`](../../src/steps/progression/__init__.py) | Datenwert |
| [`CrossDomainRecommendation`](../../src/steps/progression/recommender.py) | `(prog_id: 'str', prog_name: 'str', genre_scope: 'str', drum_grooves: 'List[RecommendationItem]', piano_voicings: 'List[RecommendationItem]', bassline_model: 'BasslineModel', explicit_relations: 'List[CrossDomainRelation]', overall_compatibility: 'str' = 'UNASSESSED') -> None` |
| [`CrossDomainRecommender`](../../src/steps/progression/recommender.py) | `(relations_path: 'Optional[str \| Path]' = None) -> 'None'` |
| [`CrossDomainRelation`](../../src/steps/progression/recommender.py) | `(relation_id: 'str', source_id: 'str', target_id: 'str', relation_type: 'str', epistemic_classification: 'str', domain_scope: 'str', formal_rule_or_strength: 'str', description: 'str', validation_status: 'str') -> None` |
| [`RecommendationItem`](../../src/steps/progression/recommender.py) | `(target_id: 'str', target_name: 'str', domain: 'str', relation_type: 'str', strength: 'str', confidence: 'Optional[float]', description: 'str', source_relation_id: 'Optional[str]' = None, evidence_status: "Literal['REVIEW_REQUIRED', 'CREATIVE_SUGGESTION']" = 'CREATIVE_SUGGESTION') -> None` |
| [`get_concept_relations`](../../src/steps/progression/recommender.py) | `(entity_id: 'str', relations_path: 'Optional[str \| Path]' = None) -> 'List[CrossDomainRelation]'` |
| [`get_recommender`](../../src/steps/progression/recommender.py) | `(relations_path: 'Optional[str \| Path]' = None) -> 'CrossDomainRecommender'` |
| [`recommend_for_drum_pattern`](../../src/steps/progression/recommender.py) | `(pat_id: 'str', relations_path: 'Optional[str \| Path]' = None) -> 'List[RecommendationItem]'` |
| [`recommend_for_piano_module`](../../src/steps/progression/recommender.py) | `(piano_id: 'str', relations_path: 'Optional[str \| Path]' = None) -> 'List[RecommendationItem]'` |
| [`recommend_for_progression`](../../src/steps/progression/recommender.py) | `(prog_id: 'str', relations_path: 'Optional[str \| Path]' = None) -> 'CrossDomainRecommendation'` |

## `app.knowledge`

| Export | Signatur |
|---|---|
| [`get_reviewed_progression`](../../app/knowledge.py) | `(prog_id: str) -> src.steps.progression.engine.ReviewedProgression` |
| [`list_reviewed_progressions`](../../app/knowledge.py) | `() -> tuple[src.steps.progression.engine.ReviewedProgression, ...]` |

## `app.brand`

| Export | Signatur |
|---|---|
| [`APP_ICON_SIZES`](../../app/brand.py) | Datenwert |
| [`LOGO_SIZES`](../../app/brand.py) | Datenwert |
| [`app_icon_ico_path`](../../app/brand.py) | `() -> 'Path'` |
| [`app_icon_path`](../../app/brand.py) | `(size: 'int' = 256) -> 'Path'` |
| [`apply_window_icon`](../../app/brand.py) | `(root) -> 'None'` |
| [`load_in_app_logo`](../../app/brand.py) | `(master, target_height: 'int' = 28)` |
| [`logo_path`](../../app/brand.py) | `(size: 'int' = 128) -> 'Path'` |

## Domänenobjekte

### [ReviewedProgression](../../src/steps/progression/engine.py)

`ReviewedProgression(progression: 'CanonicalProgression', lesson: 'str', source_ids: 'tuple[str, ...]', reviewed_on: 'str', claims: 'tuple[ApprovedClaim, ...]', catalog_version: 'str') -> None`

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

### [ScaleTemplate](../../src/steps/theory/scale.py)

`ScaleTemplate(name: 'str', aliases: 'tuple[str, ...]', intervals: 'tuple[int, ...]', category: 'ModeCategory', characteristic_intervals: 'tuple[int, ...]', avoid_notes: 'tuple[int, ...]', triad_qualities: 'tuple[str, ...]', seventh_qualities: 'tuple[str, ...]') -> None`

### [ScaleDefinition](../../src/steps/theory/scale.py)

`ScaleDefinition(root: 'NoteSpelling', template: 'ScaleTemplate', spellings: 'tuple[NoteSpelling, ...]') -> None`

- `name` (Eigenschaft)
- `intervals` (Eigenschaft)
- `pitch_classes` (Eigenschaft)
- `midi_notes` (Eigenschaft)
- `get_degree(self, degree: 'int') -> 'NoteSpelling'`
- `get_diatonic_triad(self, degree: 'int') -> 'ChordDefinition'`
- `get_diatonic_seventh(self, degree: 'int') -> 'ChordDefinition'`
- `render_text(self, convention: "Literal['INT', 'DE']" = 'INT', unicode_accidental: 'bool' = False) -> 'list[str]'`

### [InversionAnalysis](../../src/steps/theory/inversion.py)

`InversionAnalysis(inversion: 'ChordInversion', figured_bass: 'str', bass_factor: 'str', root_pc: 'int', bass_pc: 'int', german_name: 'str', is_seventh_chord: 'bool') -> None`

### [GuideToneResolution](../../src/steps/theory/voicings.py)

`GuideToneResolution(from_chord: 'str', to_chord: 'str', retained_note: 'Optional[int]', moving_note_from: 'int', moving_note_to: 'int', motion_semitones: 'int', resolution_type: "Literal['HALF_STEP_DOWN', 'HALF_STEP_UP', 'WHOLE_STEP_DOWN', 'WHOLE_STEP_UP', 'STATIC', 'LEAP']", total_l1_distance: 'int', description: 'str') -> None`

### [ProgressionShellVoicings](../../src/steps/theory/voicings.py)

`ProgressionShellVoicings(voicings: 'List[ShellVoicing]', resolutions: 'List[GuideToneResolution]', total_l1_distance: 'int', average_l1_distance: 'float', starting_layout: "Literal['7_3', '3_7']") -> None`

### [ShellVoicing](../../src/steps/theory/voicings.py)

`ShellVoicing(chord_symbol: 'str', root_pc: 'int', bass_note: 'int', guide_tones: 'Tuple[int, int]', third_note: 'int', seventh_note: 'int', layout: "Literal['7_3', '3_7']", lh_spelling: 'str', rh_spellings: 'Tuple[str, str]') -> None`

- `midi_notes` (Eigenschaft)
- `rh_span` (Eigenschaft)
- `is_seventh_below_third` (Eigenschaft)
- `to_dict(self) -> 'Dict[str, Any]'`

### [PedagogicalReduction](../../src/steps/theory/beginner_voicing.py)

`PedagogicalReduction(original_symbol: 'str', reduced_symbol: 'str', was_reduced: 'bool', omitted_factors: 'Tuple[str, ...]', explanation: 'str') -> None`

- `to_dict(self) -> 'Dict[str, Any]'`

### [BeginnerChordVoicing](../../src/steps/theory/beginner_voicing.py)

`BeginnerChordVoicing(chord_symbol: 'str', reduced_symbol: 'str', inversion: 'BeginnerTriadInversion', lh_bass_note: 'int', lh_fingering: 'int', lh_spelling: 'str', rh_notes: 'Tuple[int, int, int]', rh_fingering: 'Tuple[int, int, int]', rh_spellings: 'Tuple[str, str, str]', rh_span_semitones: 'int', pedagogical_description: 'str', reduction: 'PedagogicalReduction') -> None`

- `all_midi_notes` (Eigenschaft)
- `rh_center_pitch` (Eigenschaft)
- `to_dict(self) -> 'Dict[str, Any]'`

### [BeginnerVoiceLeadingTransition](../../src/steps/theory/beginner_voicing.py)

`BeginnerVoiceLeadingTransition(from_chord: 'str', to_chord: 'str', common_tones: 'Tuple[int, ...]', moving_voices: 'Tuple[Tuple[int, int, int], ...]', total_l1_distance: 'int', max_single_leap: 'int', has_hand_jump: 'bool', pedagogical_guidance: 'str', is_canonical_guidance: 'bool' = False) -> None`

- `to_dict(self) -> 'Dict[str, Any]'`

### [BeginnerProgressionVoicings](../../src/steps/theory/beginner_voicing.py)

`BeginnerProgressionVoicings(voicings: 'List[BeginnerChordVoicing]', transitions: 'List[BeginnerVoiceLeadingTransition]', total_l1_distance: 'int', average_l1_distance: 'float', smoothness_score: 'float', has_any_hand_jumps: 'bool', movement_reduction_vs_root_percent: 'float') -> None`

- `to_dict(self) -> 'Dict[str, Any]'`

### [VoiceLeadingViolation](../../src/steps/theory/voice_leading.py)

`VoiceLeadingViolation(rule_name: 'str', voice_indices: 'Tuple[int, int]', motion_type: 'str', pitch_interval: 'int', from_pitches: 'Tuple[int, int]', to_pitches: 'Tuple[int, int]', severity: "Literal['ERROR', 'WARNING', 'INFO']", explanation: 'str', stylistic_context: 'str') -> None`

- `violation_type` (Eigenschaft)
- `rule_source` (Eigenschaft)
- `to_dict(self) -> 'Dict[str, Any]'`

### [VoiceLeadingEvaluation](../../src/steps/theory/voice_leading.py)

`VoiceLeadingEvaluation(from_voicing: 'Tuple[int, ...]', to_voicing: 'Tuple[int, ...]', style: 'VoiceLeadingStyle', is_valid: 'bool', violations: 'List[VoiceLeadingViolation]', l1_distance: 'int', max_voice_leap: 'int', contrapuntal_motion: 'Dict[str, Any]', stylistic_notes: 'List[str]') -> None`

- `to_dict(self) -> 'Dict[str, Any]'`

### [VoiceLeadingViolation](../../src/steps/theory/voice_leading.py)

`VoiceLeadingViolation(rule_name: 'str', voice_indices: 'Tuple[int, int]', motion_type: 'str', pitch_interval: 'int', from_pitches: 'Tuple[int, int]', to_pitches: 'Tuple[int, int]', severity: "Literal['ERROR', 'WARNING', 'INFO']", explanation: 'str', stylistic_context: 'str') -> None`

- `violation_type` (Eigenschaft)
- `rule_source` (Eigenschaft)
- `to_dict(self) -> 'Dict[str, Any]'`

### [VoiceLeadingEvaluation](../../src/steps/theory/voice_leading.py)

`VoiceLeadingEvaluation(from_voicing: 'Tuple[int, ...]', to_voicing: 'Tuple[int, ...]', style: 'VoiceLeadingStyle', is_valid: 'bool', violations: 'List[VoiceLeadingViolation]', l1_distance: 'int', max_voice_leap: 'int', contrapuntal_motion: 'Dict[str, Any]', stylistic_notes: 'List[str]') -> None`

- `to_dict(self) -> 'Dict[str, Any]'`

### [CanonicalProgression](../../src/steps/progression/engine.py)

`CanonicalProgression(prog_id: 'str', name: 'str', roman_numerals: 'str', default_key: 'str', chords_str: 'str', context: 'str', sources: 'str') -> None`

- `chord_definitions` (Eigenschaft)
- `theory_profile` (Eigenschaft)
- `archetype_family` (Eigenschaft)
- `transpose(self, semitones: 'int') -> 'list[ChordDefinition]'`

### [ChordRecommendation](../../src/steps/progression/session.py)

`ChordRecommendation(candidate_symbol: 'str', relation_type: "Literal['DOMINANT_OF', 'RESOLVES_TO', 'BORROWED_FROM', 'VOICE_LEADING_NEAR', 'SUBSTITUTES_FOR', 'ROOT_MOTION', 'SCHEMA_CONTINUATION']", explanation: 'str', framework: 'str', source_id: 'str | None' = None, source_locator: 'str | None' = None, evidence_kind: "Literal['CREATIVE_SUGGESTION', 'MODEL_RULE', 'LITERATURE_REFERENCE']" = 'CREATIVE_SUGGESTION', reason_key: 'str | None' = None, source_symbol: 'str | None' = None) -> None`

### [DegreeAnalysis](../../src/steps/progression/session.py)

`DegreeAnalysis(index: 'int', symbol: 'str', roman_numeral: 'str', semitone_distance_to_next: 'Optional[int]' = None, voice_leading_warnings: 'tuple[str, ...]' = (), voice_leading_diagnostics: 'tuple[VoiceLeadingDiagnostic, ...]' = ()) -> None`

### [GuideToneResolution](../../src/steps/theory/voicings.py)

`GuideToneResolution(from_chord: 'str', to_chord: 'str', retained_note: 'Optional[int]', moving_note_from: 'int', moving_note_to: 'int', motion_semitones: 'int', resolution_type: "Literal['HALF_STEP_DOWN', 'HALF_STEP_UP', 'WHOLE_STEP_DOWN', 'WHOLE_STEP_UP', 'STATIC', 'LEAP']", total_l1_distance: 'int', description: 'str') -> None`

### [ProgressionShellVoicings](../../src/steps/theory/voicings.py)

`ProgressionShellVoicings(voicings: 'List[ShellVoicing]', resolutions: 'List[GuideToneResolution]', total_l1_distance: 'int', average_l1_distance: 'float', starting_layout: "Literal['7_3', '3_7']") -> None`

### [ShellVoicing](../../src/steps/theory/voicings.py)

`ShellVoicing(chord_symbol: 'str', root_pc: 'int', bass_note: 'int', guide_tones: 'Tuple[int, int]', third_note: 'int', seventh_note: 'int', layout: "Literal['7_3', '3_7']", lh_spelling: 'str', rh_spellings: 'Tuple[str, str]') -> None`

- `midi_notes` (Eigenschaft)
- `rh_span` (Eigenschaft)
- `is_seventh_below_third` (Eigenschaft)
- `to_dict(self) -> 'Dict[str, Any]'`

### [BeginnerChordVoicing](../../src/steps/theory/beginner_voicing.py)

`BeginnerChordVoicing(chord_symbol: 'str', reduced_symbol: 'str', inversion: 'BeginnerTriadInversion', lh_bass_note: 'int', lh_fingering: 'int', lh_spelling: 'str', rh_notes: 'Tuple[int, int, int]', rh_fingering: 'Tuple[int, int, int]', rh_spellings: 'Tuple[str, str, str]', rh_span_semitones: 'int', pedagogical_description: 'str', reduction: 'PedagogicalReduction') -> None`

- `all_midi_notes` (Eigenschaft)
- `rh_center_pitch` (Eigenschaft)
- `to_dict(self) -> 'Dict[str, Any]'`

### [BeginnerProgressionVoicings](../../src/steps/theory/beginner_voicing.py)

`BeginnerProgressionVoicings(voicings: 'List[BeginnerChordVoicing]', transitions: 'List[BeginnerVoiceLeadingTransition]', total_l1_distance: 'int', average_l1_distance: 'float', smoothness_score: 'float', has_any_hand_jumps: 'bool', movement_reduction_vs_root_percent: 'float') -> None`

- `to_dict(self) -> 'Dict[str, Any]'`

### [BeginnerVoiceLeadingTransition](../../src/steps/theory/beginner_voicing.py)

`BeginnerVoiceLeadingTransition(from_chord: 'str', to_chord: 'str', common_tones: 'Tuple[int, ...]', moving_voices: 'Tuple[Tuple[int, int, int], ...]', total_l1_distance: 'int', max_single_leap: 'int', has_hand_jump: 'bool', pedagogical_guidance: 'str', is_canonical_guidance: 'bool' = False) -> None`

- `to_dict(self) -> 'Dict[str, Any]'`

### [PedagogicalReduction](../../src/steps/theory/beginner_voicing.py)

`PedagogicalReduction(original_symbol: 'str', reduced_symbol: 'str', was_reduced: 'bool', omitted_factors: 'Tuple[str, ...]', explanation: 'str') -> None`

- `to_dict(self) -> 'Dict[str, Any]'`

### [BasslineModel](../../src/steps/progression/recommender.py)

`BasslineModel(name: 'str', style_category: 'str', description: 'str', time_signature: 'Tuple[int, int]', tempo_range: 'Tuple[int, int]', pattern_description: 'str', evidence_status: "Literal['CREATIVE_SUGGESTION']" = 'CREATIVE_SUGGESTION') -> None`

### [CrossDomainRecommendation](../../src/steps/progression/recommender.py)

`CrossDomainRecommendation(prog_id: 'str', prog_name: 'str', genre_scope: 'str', drum_grooves: 'List[RecommendationItem]', piano_voicings: 'List[RecommendationItem]', bassline_model: 'BasslineModel', explicit_relations: 'List[CrossDomainRelation]', overall_compatibility: 'str' = 'UNASSESSED') -> None`

### [CrossDomainRelation](../../src/steps/progression/recommender.py)

`CrossDomainRelation(relation_id: 'str', source_id: 'str', target_id: 'str', relation_type: 'str', epistemic_classification: 'str', domain_scope: 'str', formal_rule_or_strength: 'str', description: 'str', validation_status: 'str') -> None`

### [RecommendationItem](../../src/steps/progression/recommender.py)

`RecommendationItem(target_id: 'str', target_name: 'str', domain: 'str', relation_type: 'str', strength: 'str', confidence: 'Optional[float]', description: 'str', source_relation_id: 'Optional[str]' = None, evidence_status: "Literal['REVIEW_REQUIRED', 'CREATIVE_SUGGESTION']" = 'CREATIVE_SUGGESTION') -> None`

## Akkordqualitäten

Intervalle sind Halbtöne relativ zum Akkordgrundton. `CLOSE` verwendet
die Standardintervalle unter Berücksichtigung des expliziten Basses.

| Qualität | Aliasse | Theoretische Intervalle | Standardintervalle |
|---|---|---|---|
| `(leer)` | `maj`, `M` | `(0, 4, 7)` | `(0, 4, 7)` |
| `m` | `m`, `min`, `-` | `(0, 3, 7)` | `(0, 3, 7)` |
| `dim` | `dim`, `o`, `°` | `(0, 3, 6)` | `(0, 3, 6)` |
| `(b5)` | `(b5)` | `(0, 4, 6)` | `(0, 4, 6)` |
| `aug` | `aug`, `+` | `(0, 4, 8)` | `(0, 4, 8)` |
| `sus4` | `sus4`, `sus` | `(0, 5, 7)` | `(0, 5, 7)` |
| `sus2` | `sus2` | `(0, 2, 7)` | `(0, 2, 7)` |
| `add9` | `add9`, `add2` | `(0, 4, 7, 14)` | `(0, 2, 4, 7)` |
| `madd9` | `madd9`, `minadd9`, `-add9` | `(0, 3, 7, 14)` | `(0, 2, 3, 7)` |
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
| `7#11` | `7#11`, `7(#11)`, `lydian_dom` | `(0, 4, 7, 10, 18)` | `(0, 4, 6, 10)` |
| `7b5` | `7b5`, `7(b5)` | `(0, 4, 6, 10)` | `(0, 4, 6, 10)` |
| `7b13` | `7b13`, `7(b13)` | `(0, 4, 7, 10, 20)` | `(0, 4, 10, 20)` |
| `13` | `13`, `dom13` | `(0, 4, 7, 10, 14, 21)` | `(0, 4, 10, 14, 21)` |
| `maj13` | `maj13`, `^13`, `M13` | `(0, 4, 7, 11, 14, 21)` | `(0, 4, 11, 14, 21)` |
| `m11` | `m11`, `min11`, `-11` | `(0, 3, 7, 10, 14, 17)` | `(0, 3, 10, 14, 17)` |
