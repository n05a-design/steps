# STEPS – Typisierte harmonische, kompositorische und interpretative Regeln V3

**77 Regel-/Interpretationsobjekte**, nicht alle gleich verbindlich.

Der Regeltyp ist Teil des Vertrages. `constraint` gilt nur unter den genannten mathematischen/notationellen Annahmen; `tendency` ist stilbedingt; `interpretation` eine analytische Lesart; `transformation` eine explizite Operation; `heuristic` eine Designentscheidung; `empirical_observation` verlangt Korpus- oder Forschungskontext.

## constraint

### RULE-V3-0001 · 12TET pitch class closure
**Aussage:** Only under explicit twelve-tone equal temperament, pc(x+12n)=pc(x).
**Illustration:** pc(60)=pc(72)=0
**Grenze/Ausnahme:** Not general to arbitrary tuning.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0002 · Equal temperament semitone
**Aussage:** Ratio between consecutive 12-TET semitone steps is 2^(1/12).
**Illustration:** A4 440Hz→A#4 466.16Hz approx
**Grenze/Ausnahme:** Frequency depends on reference A4.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0003 · Major triad
**Aussage:** A root-position major triad has pitch classes {0,4,7} relative to root in 12-TET.
**Illustration:** C E G
**Grenze/Ausnahme:** Pitch spelling distinct.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0004 · Minor triad
**Aussage:** A root-position minor triad has pitch classes {0,3,7} relative to root in 12-TET.
**Illustration:** C Eb G
**Grenze/Ausnahme:** Do not infer tonal function.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0005 · Diminished triad
**Aussage:** A root-position diminished triad has pitch classes {0,3,6} relative to root.
**Illustration:** B D F
**Grenze/Ausnahme:** Enharmonic spelling meaningful.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0006 · Augmented triad
**Aussage:** A root-position augmented triad has pitch classes {0,4,8} relative to root.
**Illustration:** C E G#
**Grenze/Ausnahme:** Symmetry can yield competing root interpretations.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0007 · Dominant seventh pitch model
**Aussage:** A conventional dominant-seventh chord has relative pitch classes {0,4,7,10}.
**Illustration:** G B D F
**Grenze/Ausnahme:** A dom7 voicing may omit fifth.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0008 · Major seventh pitch model
**Aussage:** A major-seventh chord has relative pitch classes {0,4,7,11}.
**Illustration:** C E G B
**Grenze/Ausnahme:** Major-seventh in jazz != dominant seventh.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0009 · Minor seventh pitch model
**Aussage:** A minor-seventh chord has relative pitch classes {0,3,7,10}.
**Illustration:** D F A C
**Grenze/Ausnahme:** Does not uniquely identify ii7.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0010 · Half-diminished seventh
**Aussage:** A half-diminished seventh chord has relative pitch classes {0,3,6,10}.
**Illustration:** B D F A
**Grenze/Ausnahme:** May be iiø7 in a minor key.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0011 · Fully diminished seventh
**Aussage:** A fully diminished seventh chord has relative pitch classes {0,3,6,9}.
**Illustration:** B D F Ab
**Grenze/Ausnahme:** Written diminished seventh, not major sixth.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0012 · German H/B conversion
**Aussage:** In conventional German note names H corresponds to English B and German B to English Bb.
**Illustration:** H-D-F = Bdim
**Grenze/Ausnahme:** Not all alphabets treat letters identically.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0013 · Roman key dependency
**Aussage:** Scale-degree interpretation requires a local key/mode or explicitly unknown tonal context.
**Illustration:** Dm=ii in C, iv in A minor
**Grenze/Ausnahme:** Identical pitches can have multiple analyses.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0014 · Chord slash-bass
**Aussage:** In lead-sheet chord slash notation, suffix after slash denotes specified bass pitch.
**Illustration:** C/E has E bass
**Grenze/Ausnahme:** Roman V/V uses slash differently.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0015 · Transposition class invariant
**Aussage:** Under transposition by k semitones, interval classes between pitch classes remain invariant.
**Illustration:** Cmaj to Dmaj = +2
**Grenze/Ausnahme:** Not spelling-invariant.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0016 · Modal interval model Dorian
**Aussage:** Dorian scale pattern in semitones relative tonic: 0,2,3,5,7,9,10.
**Illustration:** D E F G A B C
**Grenze/Ausnahme:** Context/tonic cannot be inferred from collection alone.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0017 · Modal interval model Lydian
**Aussage:** Lydian scale pattern: 0,2,4,6,7,9,11.
**Illustration:** F G A B C D E
**Grenze/Ausnahme:** Major-mode tonic ambiguous from notes alone.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0018 · Modal interval model Mixolydian
**Aussage:** Mixolydian scale pattern: 0,2,4,5,7,9,10.
**Illustration:** G A B C D E F
**Grenze/Ausnahme:** Dominant I7 need not resolve.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0019 · Harmonic minor interval model
**Aussage:** Harmonic minor scale intervals: 0,2,3,5,7,8,11.
**Illustration:** A B C D E F G#
**Grenze/Ausnahme:** Not sole minor-key melodic model.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0020 · Whole tone symmetric collection
**Aussage:** Whole-tone collection 0,2,4,6,8,10 contains six tones.
**Illustration:** C D E F# G# A#
**Grenze/Ausnahme:** Spelling choice matters.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0021 · Tn transposition
**Aussage:** Tn maps pc p to (p+n) mod 12.
**Illustration:** T2 {0,4,7}={2,6,9}
**Grenze/Ausnahme:** 12-TET pitch-class formalism only.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0022 · TnI inversion
**Aussage:** TnI maps pc p to (n-p) mod 12.
**Illustration:** T0I {0,4,7}={0,8,5}
**Grenze/Ausnahme:** Not same as retrograde melody.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0023 · Parallel P transformation
**Aussage:** Neo-Riemannian P switches major/minor while retaining root and fifth.
**Illustration:** C major C-E-G→C minor C-Eb-G
**Grenze/Ausnahme:** Triads under standard model.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0024 · Relative R transformation
**Aussage:** Neo-Riemannian R switches to relative triad with two shared notes.
**Illustration:** C major→A minor
**Grenze/Ausnahme:** Triadic context; tonal-center not necessarily switched.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0025 · Leittonwechsel L transformation
**Aussage:** Neo-Riemannian L changes one note by semitone to third-related triad.
**Illustration:** C major→E minor
**Grenze/Ausnahme:** Need explicit enharmonic notation.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0026 · Add9 vs ninth
**Aussage:** Cadd9 contains no implied seventh, C9 generally implies minor seventh.
**Illustration:** Cadd9 C E G D; C9 C E G Bb D
**Grenze/Ausnahme:** Conventions vary in real chord charts.
**Status:** editorial_draft_not_automatically_executed.

## tendency

### RULE-V3-0027 · Classical leading tone
**Aussage:** Leading tone typically resolves upward by semitone in common-practice cadential context.
**Illustration:** B→C over G7→C
**Grenze/Ausnahme:** Other voices, frustr. resolution and non-classical styles.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0028 · Dominant seventh tritone
**Aussage:** In classical cadences, 7th of V7 often resolves downward by step and leading tone upward.
**Illustration:** G7 F→E B→C
**Grenze/Ausnahme:** Other styles/voicings admit alternatives.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0029 · Classical V–I
**Aussage:** Dominant harmony conventionally creates potential for tonic closure with suitable placement.
**Illustration:** G7→C
**Grenze/Ausnahme:** Cadence is a contextual formal function.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0030 · Predominant to dominant
**Aussage:** ii/IV frequently support movement toward V in common-practice syntax.
**Illustration:** Dm7→G7
**Grenze/Ausnahme:** IV may also close rock songs.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0031 · Applied dominant target
**Aussage:** V7/x tends to tonicize its target x, but need not resolve literally.
**Illustration:** A7→Dm in C
**Grenze/Ausnahme:** Interrupted, deceptive or chained dominant cases.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0032 · Minor-mode leading tone
**Aussage:** V7 in tonal minor often contains raised leading tone.
**Illustration:** E7 G#→A in A minor
**Grenze/Ausnahme:** Aeolian modal practice may prefer v.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0033 · Classical cadential 64
**Aussage:** Cadential I64 is often dominant elaboration rather than independent tonic arrival.
**Illustration:** C/G–G7–C
**Grenze/Ausnahme:** Depends style and analysis system.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0034 · Jazz ii–V guide tones
**Aussage:** Sevenths and thirds of ii/V frequently resolve by semitone or common tones.
**Illustration:** Dm7 (F,C)→G7 (F,B)→Cmaj7 (E,B)
**Grenze/Ausnahme:** Exact voicing/phrase may differ.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0035 · Minor iv color
**Aussage:** Borrowed minor iv often supports tonic approach in major-key styles.
**Illustration:** F–Fm–C in C
**Grenze/Ausnahme:** May be interpreted as mixture or chromatic voice-leading.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0036 · Chromatic predominant augmented sixth
**Aussage:** Aug6 span commonly expands to dominant scale degree 5 in common-practice tonal context.
**Illustration:** Ab–F#→G in C
**Grenze/Ausnahme:** Voicings, doubling, style, enharmonics matter.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0037 · Circle motion
**Aussage:** Descending fifth roots are frequent in some tonal and jazz sequences.
**Illustration:** E7–A7–Dm7–G7–C
**Grenze/Ausnahme:** Not necessarily normative in modal, rock or gamelan.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0038 · Blues dominant seventh tonic
**Aussage:** I7 often functions tonically in blues-derived repertoires.
**Illustration:** C7 as bar1 in C blues
**Grenze/Ausnahme:** Do not force every I7 into V/IV.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0039 · Modal center stability
**Aussage:** Modal vamp can establish center through bass, duration, melody without V–I.
**Illustration:** Dm7–G around D Dorian
**Grenze/Ausnahme:** Tonic inference uncertain without musical evidence.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0040 · Popular loop closure
**Aussage:** Repeated pop loop may have rhetorical closure at rotation boundary independent of cadential V–I.
**Illustration:** Am–F–C–G
**Grenze/Ausnahme:** Context and listener interpretation vary.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0041 · Cadence strength context
**Aussage:** A larger formal closure requires more than a chord-pair identity.
**Illustration:** G7–C at phrase ending
**Grenze/Ausnahme:** No universal scalar cadence metric.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0042 · Melody-harmony compatibility
**Aussage:** Strong melody notes are often chord tones or contextually managed tensions.
**Illustration:** E over Cmaj7 or Dm9
**Grenze/Ausnahme:** Non-chord tones can be compositionally valid.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0043 · Strong-beat harmonic rhythm
**Aussage:** New harmonies often coincide with metrically salient positions in some idioms.
**Illustration:** Chord change each downbeat
**Grenze/Ausnahme:** Anticipations, syncopation, rubato exist.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0044 · Voice leading common tones
**Aussage:** Holding common tones can reduce motion cost under fixed matching.
**Illustration:** C major→A minor shares C,E
**Grenze/Ausnahme:** Smoothness is not universal superiority.
**Status:** editorial_draft_not_automatically_executed.

## transformation

### RULE-V3-0045 · Tritone substitution of V7
**Aussage:** Replace dominant seventh with tritone-related seventh directed to same goal.
**Illustration:** G7→C replaced with Db7→C
**Grenze/Ausnahme:** Jazz idiom; voice-leading and spelling review.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0046 · Relative triad substitution
**Aussage:** Move triad to relative mode preserving two notes.
**Illustration:** C→Am
**Grenze/Ausnahme:** Changes tonic/functional interpretation.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0047 · Parallel mode switch
**Aussage:** Switch major/minor third of chord with same root/fifth.
**Illustration:** C→Cm
**Grenze/Ausnahme:** Modal borrowing may change context.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0048 · Inversion change
**Aussage:** Change bass to chord tone without changing chord's pitch-class set.
**Illustration:** C→C/E
**Grenze/Ausnahme:** Actual bass movement differs.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0049 · Voicing redistribution
**Aussage:** Revoice same chord tones across register while preserving harmony label.
**Illustration:** C4-E4-G4→C3-G3-E4
**Grenze/Ausnahme:** Doubled notes or omitted fifth may affect sound.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0050 · Motivic rhythmic augmentation
**Aussage:** Multiply note durations by positive constant without changing order.
**Illustration:** e e q→q q h
**Grenze/Ausnahme:** Tempo change different operation.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0051 · Motivic rhythmic diminution
**Aussage:** Divide durations by constant.
**Illustration:** q q h→e e q
**Grenze/Ausnahme:** Meter/bar count may change.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0052 · Melodic retrograde
**Aussage:** Reverse pitch event order, with rhythm handling explicit.
**Illustration:** C D E→E D C
**Grenze/Ausnahme:** Not full retrograde if durations unchanged.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0053 · Melodic inversion
**Aussage:** Invert directed melodic intervals around specified axis.
**Illustration:** +2,+3→-2,-3
**Grenze/Ausnahme:** Diatonic/chromatic model requires specification.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0054 · Motivic sequence
**Aussage:** Repeat melodic/rhythmic shape at shifted pitch level.
**Illustration:** C D E→D E F
**Grenze/Ausnahme:** Diatonic spelling vs exact transposition.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0055 · Borrowed chord insertion
**Aussage:** Replace selected diatonic chord with parallel-mode-derived chord.
**Illustration:** C–F–G→C–Fm–G
**Grenze/Ausnahme:** Can clash with melody pitch A over Fm.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0056 · Applied dominant insertion
**Aussage:** Precede target with dominant of that target.
**Illustration:** C–Dm→C–A7–Dm
**Grenze/Ausnahme:** Chord durations and voice leading need replanning.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0057 · Reharmonize fixed melody
**Aussage:** Hold melody notes and seek alternative harmony retaining explicit tension policy.
**Illustration:** E melody over Cmaj7 / Am9 / Fmaj7
**Grenze/Ausnahme:** Need temporal alignment to avoid false compatibility.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0058 · Arrangement recast
**Aussage:** Preserve essential pitch/harmonic plan while reallocating voices to instruments.
**Illustration:** Piano chords→string texture
**Grenze/Ausnahme:** Cannot assume equal idiomatic range.
**Status:** editorial_draft_not_automatically_executed.

## interpretation

### RULE-V3-0059 · Roman numeral lens
**Aussage:** Interpret pitches relative to selected key/mode and local tonicization.
**Illustration:** Am=vi in C, i in A minor
**Grenze/Ausnahme:** Competing centers may be reasonable.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0060 · Functional lens
**Aussage:** Classify context as tonic/predominant/dominant roles.
**Illustration:** G7 in C has dominant behavior
**Grenze/Ausnahme:** Roles are style- and phrase-dependent.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0061 · Modal lens
**Aussage:** Identify characteristic mode and supporting degrees.
**Illustration:** Dm7–G with D focus = Dorian
**Grenze/Ausnahme:** Same notes as C major.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0062 · Pop multi-tonic lens
**Aussage:** Allow relative major/minor focus to coexist.
**Illustration:** Am–F–C–G in A minor/C major
**Grenze/Ausnahme:** Need melody/meter/section evidence.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0063 · Neo-Riemannian triadic lens
**Aussage:** Describe triad changes with P/L/R relationships where defined.
**Illustration:** C→Am R
**Grenze/Ausnahme:** Not a full tonal function theory.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0064 · Chromatic mediant lens
**Aussage:** Describe non-diatonic third-related sonorities and voice-leading.
**Illustration:** C→Ab
**Grenze/Ausnahme:** Historical labels don't yield universal function.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0065 · Blues-specific function
**Aussage:** Treat dominant quality on I/IV as tonic/subdominant in relevant repertoire.
**Illustration:** C7–F7
**Grenze/Ausnahme:** Not same as classical V7/IV.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0066 · Six-based minor notation
**Aussage:** Represent relative-minor tonic as scale degree vi under declared pop notation convention.
**Illustration:** Am in C collection = vi
**Grenze/Ausnahme:** Not necessarily the actual tonal center.
**Status:** editorial_draft_not_automatically_executed.

## heuristic

### RULE-V3-0067 · Voice leading displacement
**Aussage:** Rank voiced chords by total semitone motion under explicit matching rules.
**Illustration:** C-E-G→C-E-Ab costs1 semitone
**Grenze/Ausnahme:** Register/matching/voice crossing policies matter.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0068 · Melody chord-tone preference
**Aussage:** Prefer candidates containing emphasized melody tones when requested.
**Illustration:** E over Am/C/Fmaj7, different roles
**Grenze/Ausnahme:** Tensions and nonchord notes allowed.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0069 · Style-conditional recommendation
**Aussage:** Filter chord candidates by selected analysis lens and style.
**Illustration:** Blues I7 vs classical Imaj
**Grenze/Ausnahme:** Style labels cannot guarantee a unique grammar.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0070 · Complexity ladder
**Aussage:** Provide conservative, colored, advanced and exploratory variants.
**Illustration:** Triads→7ths→mixture→chromatic
**Grenze/Ausnahme:** Pedagogy needs learning-precondition model.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0071 · Composition contour preservation
**Aussage:** When developing motif, preserve selected invariant (contour/rhythm/interval).
**Illustration:** C-D-E→D-E-F retains + +
**Grenze/Ausnahme:** Other qualities may be intentionally transformed.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0072 · Formal contrast budget
**Aussage:** Vary one or more of register/texture/harmony/motif to differentiate sections.
**Illustration:** Verse low-register → chorus high
**Grenze/Ausnahme:** No fixed formula guarantees listener perception.
**Status:** editorial_draft_not_automatically_executed.

## empirical_observation

### RULE-V3-0073 · Corpus dependence of chord frequency
**Aussage:** A chord transition rate has meaning only relative to a named corpus, style, counting grain and sample.
**Illustration:** I–V share varies by rock/classical corpus
**Grenze/Ausnahme:** Never invent numeric probabilities.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0074 · Tonal ambiguity in axis loops
**Aussage:** Published pop research identifies multiple tonal readings of common axis rotations.
**Illustration:** Am–F–C–G
**Grenze/Ausnahme:** Not every performance is ambiguous.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0075 · Plateau loop / hybrid tonic
**Aussage:** Research documents pop loops where IV/V/vi and melodic tonic evidence need nuanced analysis.
**Illustration:** F–G–Am with C melodic center
**Grenze/Ausnahme:** Specific repertoire/time/context required.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0076 · Music expectation is learned
**Aussage:** Perceived tension and expectation depend on learned schemas and context.
**Illustration:** Cadential expectancy in specific listeners
**Grenze/Ausnahme:** Not universal emotion mapping.
**Status:** editorial_draft_not_automatically_executed.

### RULE-V3-0077 · Genre labels are heterogenous
**Aussage:** A 'jazz' or 'popular' pattern label does not uniquely identify a harmonic rule set.
**Illustration:** Dm–G–C appears across contexts
**Grenze/Ausnahme:** Test with representative annotated corpora.
**Status:** editorial_draft_not_automatically_executed.
