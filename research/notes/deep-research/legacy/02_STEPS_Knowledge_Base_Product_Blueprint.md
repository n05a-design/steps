# Deep Research: Knowledge Base and Product Blueprint for “Steps”

## Strategic direction

Your current concept is strong enough to justify treating **Steps** as more than a chord-generator app. The most promising positioning is an **open-source harmony laboratory**: a tool that sits between a music-theory tutor, a chord-progression explorer, a composition assistant, and a lightweight symbolic-music workstation.

The project statement you proposed — **“Steps – An independent, open-source chord progression app for exploring harmony & learning music theory.”** — is a good foundation because it avoids competing directly with full DAWs while leaving room for deep theory, experimentation, playback, MIDI, analysis, and educational features.

Your current `SKILL.md` is already pointed in the right direction. It distinguishes analysis, generation, reharmonization, voice leading, teaching, notation and MIDI; it also explicitly warns against conflating classical functional theory, jazz chord-scale theory and popular-music practice. That separation is crucial because the same chord sequence can receive very different explanations depending on repertoire and analytical framework. [Quellenreferenz: turn0file1] Open Music Theory likewise treats voice-leading, harmony, form, chromatic harmony, popular music and jazz as related but distinct areas rather than one universal rule system. [Quellenreferenz: turn523589search0, turn523589search2]

I would therefore build the project around four conceptual engines rather than one giant “music theory engine”: **Theory**, **Harmony**, **Generation**, and **Pedagogy**. The GUI can expose them as one experience, but internally the distinction will make the application much easier to reason about, test and extend.

The important architectural decision is to avoid putting the entire accumulated knowledge directly into `SKILL.md`. Modern Agent Skills are explicitly designed around progressive disclosure: a compact `SKILL.md` defines when and how the skill should operate, while deeper references, scripts and assets are loaded only when needed. OpenAI's current Skills documentation describes exactly this structure, and the open Agent Skills specification supports `references/`, `scripts/`, and `assets/` alongside the required `SKILL.md`. [Quellenreferenz: turn178970search1, turn178970search2, turn178970search0]

A good end-state is therefore:

```text
Steps
├── App
│   ├── Harmony engine
│   ├── Progression engine
│   ├── Voice-leading engine
│   ├── Rhythm/groove engine
│   ├── Playback engine
│   └── UI
│
└── Music-theory skill
    ├── SKILL.md
    ├── references/
    ├── schemas/
    ├── datasets/
    ├── scripts/
    └── evals/
```

The crucial idea is that **the theory knowledge should not live only in natural-language prose**. Whenever possible, concepts should also be represented as structured data that the application itself can consume.

## What your existing collection already covers

The screenshot shows that you have already accumulated material across several unusually useful domains: general theory, harmony, computational music theory, mathematics and music, popular-music analysis, ModeWheel, the Chord Wheel, Chord Files, scale tools and reharmonization. That is a better starting collection than a pile of conventional harmony textbooks because Steps needs both **theoretical authority** and **interaction/product inspiration**.

Your existing skill draft covers the core analytical workflow particularly well: identify tonal center, decompose chord symbols, assign Roman numerals, detect secondary dominants/modal interchange/substitutions only when justified, and explain voice leading. [Quellenreferenz: turn0file1] That should remain the analytical backbone.

There are, however, several knowledge areas that I would deliberately add because they are likely to become important once you begin generating progressions rather than merely labeling them.

| Knowledge area | Why Steps needs it |
|---|---|
| Pitch spelling and enharmonic logic | `F#–A#–C#` and `Gb–Bb–Db` are acoustically equivalent in equal temperament but analytically different in many contexts. |
| Chord-symbol grammar | You need deterministic parsing of `Cmaj7#11/G`, `Fø7`, `Bb7sus4`, `V7/ii`, etc. |
| Tonal hierarchy | Helps rank “next chord” choices instead of merely enumerating all possible chords. |
| Phrase and cadence models | Progressions become musically useful when they express beginning, continuation, dominant preparation and closure. |
| Voice-leading cost | Allows Steps to distinguish harmonic plausibility from physically/smoothly playable realizations. |
| Harmonic rhythm | A progression is not only a sequence of chord labels; timing matters enormously. |
| Modal harmony | Required for Dorian, Mixolydian, Phrygian, modal vamp and modern soundtrack applications. |
| Pop/rock loop theory | Four-chord loops often resist classical dominant–tonic interpretations. |
| Blues harmony | Dominant-seventh tonic/subdominant behavior cannot be treated as conventional classical dominants. |
| Jazz harmony | Extensions, alterations, ii–V structures, tritone substitution, backdoor dominants and chord-scale relationships need their own representation. |
| Neo-Riemannian transformations | Very useful for chromatic mediants, cinematic progressions and parsimonious triadic movement. |
| Chromatic voice-leading | Often explains progressions more convincingly than functional harmony alone. |
| Negative/axis harmony | Useful as an exploratory transformation, but should not be presented as a universal explanatory theory. |
| Harmonic ambiguity | The engine should be able to return several plausible analyses rather than pretend every sequence has one canonical answer. |
| Meter and groove | Necessary once progression playback and drums become part of Steps. |
| Instrument-aware voicing | Piano, guitar, strings and synth pads require different register, spacing and duplication rules. |
| Melody–harmony interaction | Eventually enables chord recommendations conditioned on a melody. |

Open Music Theory is especially valuable as a freely usable conceptual reference because its curriculum spans fundamentals, voice leading, harmonic function, chromatic harmony, modulation, jazz and popular music; the Pressbooks edition is released under Creative Commons Attribution-ShareAlike. [Quellenreferenz: turn523589search0, turn523589search8]

For the skill, I would avoid collapsing these into one `music-theory.md`. A better reference library would look closer to:

```text
references/
  notation/
  pitch-and-intervals/
  scales-and-modes/
  chord-construction/
  chord-symbols/
  tonal-harmony/
  chromatic-harmony/
  modal-harmony/
  popular-harmony/
  jazz-harmony/
  blues-harmony/
  neo-riemannian/
  voice-leading/
  counterpoint/
  cadences-and-form/
  modulation/
  reharmonization/
  melody-harmony/
  harmonic-rhythm/
  rhythm-and-meter/
  drums-and-groove/
  orchestration-and-register/
  pedagogy/
```

That modular design also aligns well with the way current Agent Skills are discovered and loaded: metadata first, then `SKILL.md`, then references/scripts only when required. [Quellenreferenz: turn178970search6, turn178970search9]

## High-value corpora, datasets and open references

This is the area where I would expand your library most aggressively. Books explain theory; **corpora allow Steps to learn what musicians actually do**.

The strongest foundation I found is **ChoCo**, the Chord Corpus. ChoCo integrates more than 20,000 human-created harmonic annotations from 18 heterogeneous datasets and normalizes several representations including Harte-style chord symbols, lead-sheet notation and Roman numerals using JAMS. Its explicit goal is interoperability between previously disconnected harmony datasets. [Quellenreferenz: turn558318search2] This is almost tailor-made for a project such as Steps because it gives you a research-grade bridge between symbolic chord labels and real repertoire.

A second exceptional source is **When in Rome**, which aggregates more than 2,000 functional-harmony analyses covering roughly 1,500 distinct works. Its authors specifically identify automatic analysis, composition, classification and corpus-scale harmonic study as intended uses. [Quellenreferenz: turn558318search1] This corpus could power statistics such as “common destinations after V/V in common-practice repertoire” or provide evaluation examples for your analyzer.

For classical tonal harmony, the **Annotated Beethoven Corpus** provides expert analyses of all Beethoven string quartets using the DCML harmonic-annotation standard and represents key, root, inversion, extensions, suspensions and related properties in machine-readable form. [Quellenreferenz: turn558318search0] The DCML standard itself is worth adopting as one of Steps' internal interchange representations because it supports harmonic labels, local keys, secondary relationships, chord alterations, phrase boundaries and cadence labels. [Quellenreferenz: turn523589search5]

A related corpus of 264 nineteenth-century piano works includes Roman-numeral harmony, phrase boundaries and cadence annotations produced and reviewed by trained theorists. [Quellenreferenz: turn558318search10] This is especially useful because Steps should eventually understand that progression grammar operates at multiple levels: chord → phrase → cadence → section.

For popular music, Hooktheory is useful as product inspiration even if its commercial song database should not simply be copied. Its interface represents harmony key-agnostically with Roman numerals and uses empirical song data to generate “Magic Chord” recommendations based on how chords have appeared in existing songs. [Quellenreferenz: turn558318search8, turn671206search4] The underlying product insight is important: **theory rules and corpus probabilities should be separate recommendation signals**.

For drum functionality, the **Groove MIDI Dataset** is an excellent starting point. It contains 1,150 MIDI drum performances, more than 22,000 measures and about 13.6 hours of human-played material, with genre and tempo metadata; Google distributes it under CC BY 4.0. [Quellenreferenz: turn558318search3] The Expanded Groove MIDI Dataset extends this material to 444 hours of audio rendered across 43 drum kits while retaining MIDI annotations. [Quellenreferenz: turn558318search4] For Steps, you likely do not need the huge audio set initially; the original MIDI dataset is much more relevant for extracting reusable groove abstractions.

A useful drum representation would therefore not store recordings as your primary artifact but something like:

```yaml
genre: funk
meter: 4/4
tempo_range: [90, 115]
length_bars: 1
resolution: 16
kick:  [1,0,0,0, 0,0,1,0, 1,0,0,0, 0,1,0,0]
snare: [0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0]
hihat: [...]
velocity_profile: [...]
swing: 0.08
tags: [syncopated, medium-density]
```

This makes the rhythm engine independent from any specific drum sample pack.

For symbolic formats, **MusicXML** should be your notation interchange target; the W3C maintains MusicXML as an open digital sheet-music interchange format. [Quellenreferenz: turn449471search12, turn449471search19] MIDI should remain your real-time/playback and DAW interchange format.

For Python, **music21** is particularly attractive because it directly models Roman-numeral harmony and keys, while **pretty_midi** provides simple MIDI parsing, creation, manipulation and synthesis and uses the permissive MIT license. [Quellenreferenz: turn523589search4, turn449471search0] Partitura is another useful symbolic-music toolkit and includes analysis functions such as key estimation, tonal tension and voice separation. [Quellenreferenz: turn449471search24, turn449471search32]

These sources suggest a practical raw-data library for Steps:

```text
data/
  corpora/
    choco/
    when-in-rome/
    dcml/
    groove-midi/
  theory/
    open-music-theory/
    book-notes/
  normalized/
    chords/
    progressions/
    cadences/
    modulations/
    grooves/
  schemas/
    chord.schema.json
    progression.schema.json
    voicing.schema.json
    groove.schema.json
    analysis.schema.json
```

Before putting any corpus into your public repository, check the license of each individual source rather than assuming that the license of an aggregator automatically permits every downstream use. The Beethoven corpus, for example, explicitly uses CC BY-NC-SA 4.0. [Quellenreferenz: turn558318search0]

## Competitive landscape and what to borrow

Your Chord Files inspiration is well chosen. The site describes itself as a tool that exposes harmonic possibilities rather than composing for the user, which is philosophically close to what Steps could become. [Quellenreferenz: turn0file4] Its separate progression-example material also indicates that examples and guided exploration are part of the product rather than merely documentation. [Quellenreferenz: turn0file5]

ModeWheel occupies a different niche: its stated purpose is to identify, display, hear and practice modes/scales interactively. [Quellenreferenz: turn0file2] That makes it good inspiration for the **visual relationship layer** of Steps rather than the progression engine itself.

There are several additional products worth studying because each solves a different part of the problem.

| Product | Particularly useful idea for Steps |
|---|---|
| **Hookpad / Hooktheory** | Roman-numeral-first composition; melody/chord visualization; chord suggestions based on a large song corpus; borrowed/secondary chords; integrated bass/drums. [Quellenreferenz: turn671206search4, turn671206search5] |
| **Scaler 3** | Chord discovery outside a fixed scale, modulation paths, automatic voice leading, chord substitutions, multiple progression comparison, MIDI/audio detection and separated chord/melody/bass lanes. [Quellenreferenz: turn671206search0] |
| **Tonaly** | Circle-of-fifths-centered songwriting; Roman/Nashville-number views; many modes and instrument visualizations; MIDI/PDF export. [Quellenreferenz: turn671206search2, turn671206search3] |
| **ChordChord** | Fast generation plus genre-matched arrangements, drums/melodies, chord detection, DAW export and deliberately low theory barrier. [Quellenreferenz: turn523589search6] |
| **ChordJam** | Guided randomization of chord type, voicing, rhythm and progressions instead of deterministic “best chord” recommendation. [Quellenreferenz: turn671206search6] |
| **Ripchord** | One-note chord triggering, user-created preset ecosystems and importing chord content from MIDI. [Quellenreferenz: turn558318search7] |
| **ChordLens** | Loopable progressions, optional voice leading, metronome and SoundFont playback in an open-style desktop workflow. [Quellenreferenz: turn558318search6] |
| **Chord Progression Helper** | Particularly relevant precedent because it is open source and already combines progression writing, drums, strumming, melody and song sections. [Quellenreferenz: turn558318search5] |

Scaler 3 is probably the most important commercial benchmark for the long term. It already spans chord suggestions, automatic voice leading, modulation, circle-of-fifths relationships, non-diatonic exploration, bass/melody generation, arrangement scenes and multi-lane composition. [Quellenreferenz: turn671206search0] Trying to duplicate Scaler feature-for-feature would be a poor open-source strategy. Steps should differentiate itself by making the **reasoning transparent**.

For example, instead of:

> Suggested next chord: Fm

Steps could expose:

```text
Fm
Confidence / compatibility: 0.83

Possible interpretations:
• iv borrowed from C minor
• chromatic predominant
• common-tone connection with C major
• A♭ creates chromatic descent G → A♭ → G or A

Voice-leading score: excellent
Corpus frequency: moderate
Tonal distance: low
Color: darker
```

That would combine the analytical transparency of a theory textbook with the immediacy of a progression tool.

Scaler's own documentation illustrates why this matters: its “Tonal” suggestion mode explicitly allows chords outside the selected scale and can justify a relationship such as C major → F minor through modal interchange, minor-subdominant behavior or shared scales. [Quellenreferenz: turn671206search8] Steps can go further by showing **which interpretation the current context supports** instead of only listing relationships.

A major opportunity is therefore a **multi-theory explanation system**:

```text
C – Ab – Eb – Bb

Classical functional view:
limited explanatory fit

Modal/rock view:
I – bVI – bIII – bVII

Voice-leading view:
strong common tones + stepwise connections

Transformational view:
chromatic-mediant relationships

Corpus view:
common family of major-mode rock progressions
```

The system should sometimes explicitly say that no single functional explanation is preferable. Open Music Theory similarly emphasizes that harmonic analysis is interpretive and depends on phrase and broader musical context, not merely chord labeling. [Quellenreferenz: turn523589search3]

## A much larger knowledge-library design

The library you build before condensation should be deliberately redundant. At the collection stage, your goal should be **coverage, provenance and disagreement preservation**, not elegance.

I would represent every concept as a structured knowledge object with fields such as:

```yaml
id: modal-interchange
names:
  - modal interchange
  - modal mixture
category: chromatic-harmony

definition:
  short: ...
  extended: ...

contexts:
  classical: ...
  jazz: ...
  pop-rock: ...

rules:
  - ...

common_examples:
  - key: C
    progression: [C, Fm, C]
    roman: [I, iv, I]

voice_leading:
  - E -> F
  - A♭ -> G

related:
  - borrowed-chords
  - minor-subdominant
  - chromatic-mediants

ambiguities:
  - ...

sources:
  - type: book
    citation: ...
  - type: corpus
    dataset: ...

app_usage:
  analyzer: true
  generator: true
  tutor: true
```

The same schema should exist for **progression archetypes**:

```yaml
id: pop-axis-family
degrees: [I, V, vi, IV]
mode: major
rotation_equivalent: true

variants:
  - [vi, IV, I, V]
  - [IV, I, V, vi]

properties:
  tonic_stability: medium
  dominant_pressure: low-to-medium
  loopability: high

contexts:
  - pop
  - rock
  - electronic

generation_tags:
  - familiar
  - stable
  - loop
```

And for **transformation rules**:

```yaml
operation: secondary-dominant
input:
  target_degree: ii

output:
  chord: V7/ii

conditions:
  target_should_be_tonicizable: true

example:
  key: C
  before: [C, Dm, G, C]
  after:  [C, A7, Dm, G7]
```

This gives you something much more powerful than a conventional theory database because the same knowledge can drive the tutor, analyzer and generator.

The most important conceptual change I would make to your current Skill is to turn it into a **router and quality-control layer**, rather than the place where theory knowledge accumulates. Your existing draft already contains the right core behavioral rules. [Quellenreferenz: turn0file1]

A mature Skill might therefore contain only:

```text
SKILL.md
  task classification
  source selection
  notation policy
  analysis procedure
  generation procedure
  ambiguity policy
  citation/provenance rules
  output contracts
  validation checklist
```

Everything else belongs in references or code.

This is precisely how OpenAI currently describes Skills: reusable instructions plus optional references, scripts, templates and assets; OpenAI also recommends evaluating skills systematically rather than assuming prompt quality from inspection alone. [Quellenreferenz: turn178970search1, turn178970search4]

## Product concepts that could make Steps distinctive

The most interesting feature direction is a **Harmonic Explorer**, rather than a conventional “Generate Progression” button. Selecting a chord would open multiple possible destinations arranged by relationship:

```text
DIATONIC
ii   iii   IV   V   vi   vii°

BORROWED
iv   bIII   bVI   bVII

DOMINANT PATHS
V/V   V/ii   V/vi

CHROMATIC
bII   III   VI

TRANSFORMATIONS
parallel
relative
chromatic-mediant
tritone-sub

VOICE-LEADING
closest voicing
common-tone
chromatic-motion
```

Each relationship could be displayed on a **harmonic map**, with optional views for circle of fifths, scale degrees, chromatic distance and voice-leading distance. ModeWheel and Tonaly demonstrate the usefulness of circular visualization for relationships among scales and chords, while Scaler demonstrates the value of allowing users to move outside a fixed diatonic universe. [Quellenreferenz: turn0file2] [Quellenreferenz: turn671206search2, turn671206search0]

A second highly differentiating concept would be a **Why does this work?** button. Given any progression, Steps could return layered explanations:

```text
Harmony
Voice leading
Bass motion
Cadence/form
Modal interpretation
Jazz interpretation
Pop/rock interpretation
Corpus similarity
Alternative interpretations
```

A third feature should be **Progression DNA**: normalize chords to Roman numerals so progressions become transposable structures. Hooktheory already demonstrates the educational power of key-agnostic Roman-numeral notation. [Quellenreferenz: turn558318search8] Steps could extend this by treating rotations, substitutions, inversions and reharmonizations as related objects.

A fourth concept is **harmonic distance control**. Instead of mood labels alone, the generator could expose actual parameters:

```text
Diatonicity        ███████░░░
Tonal tension      █████░░░░░
Chromaticism       ███░░░░░░░
Voice movement     ██░░░░░░░░
Jazz complexity    ████░░░░░░
Loopability        ████████░░
Cadential strength ███░░░░░░░
```

Mood labels such as *dark*, *dreamy*, *cinematic* or *nostalgic* can remain as presets, but the underlying engine should operate on musical variables. Scaler already categorizes exploratory harmony partly by concepts such as brighter/darker/compatible/adventurous; exposing the underlying theory would give Steps a clearer educational identity. [Quellenreferenz: turn671206search0]

A fifth feature could be **Reharmonization Ladder**. Your existing “7 levels of reharmonising Eleanor Rigby” material points directly toward this idea. Given a progression, Steps might offer:

```text
Level A – inversions only
Level B – seventh/extensions
Level C – secondary dominants
Level D – modal mixture
Level E – tritone/backdoor substitutions
Level F – chromatic-mediant / transformational
Level G – free reharmonization
```

That would be pedagogically much stronger than presenting eight unrelated alternatives.

The drum module should initially stay modest. Rather than becoming a beat-making DAW, give the user 20–50 high-quality abstract groove families across rock, pop, funk, soul, jazz, blues, hip-hop, house, techno, drum & bass, reggae, Latin, Afrobeat and cinematic styles, with tempo-sensitive variation and fills. The Groove MIDI Dataset provides genre-tagged human performances that can inform such abstractions. [Quellenreferenz: turn558318search3]

## Recommended build order

The project will be easier to execute if you resist adding generative AI too early. The core of Steps can be deterministic and explainable; an AI Skill should sit above that engine rather than substitute for it.

A high-value development sequence would be:

1. **Create the canonical theory model.** Define pitch, interval, scale, mode, chord, extension, inversion, key, Roman numeral, harmonic function, cadence, modulation, progression and voicing as data structures. Adopt explicit parsing/serialization rules and test enharmonic spelling thoroughly. music21's RomanNumeral implementation and the DCML annotation standard are useful reference points. [Quellenreferenz: turn523589search4, turn523589search5]

2. **Build the progression object and playback loop.** A progression should already support key, mode, chord duration, inversion, voicing, BPM, meter and section. MIDI export can be implemented with `pretty_midi`; MusicXML can follow once notation export becomes important. [Quellenreferenz: turn449471search0, turn449471search12]

3. **Build the deterministic harmony analyzer.** Implement diatonic analysis first, followed by inversions, seventh chords, secondary dominants, modal mixture, tonicization and modulation. Allow multiple analyses with confidence rather than returning one absolute answer.

4. **Build a voice-leading engine.** Treat voicing as a separate optimization problem. Scaler's “minimize movement” feature illustrates the usefulness of separating harmonic recommendation from voicing movement. [Quellenreferenz: turn671206search8]

5. **Add progression-generation strategies.** Start with rule-based strategies: functional, modal, loop-based, cadence-based, sequence-based and voice-leading-based. Then add corpus-derived transition probabilities from appropriately licensed datasets such as ChoCo/When in Rome. [Quellenreferenz: turn558318search2, turn558318search1]

6. **Add theory explanations.** This is where your Skill becomes central. The application can pass a fully structured analysis object to the Skill; the Skill translates it into useful explanations, exercises, alternative interpretations and compositional suggestions.

7. **Add groove and rhythm.** Begin with abstract MIDI patterns and genre metadata rather than audio. GMD is suitable source material for learning realistic timing, velocity, beat and fill behavior. [Quellenreferenz: turn558318search3]

8. **Add melody-aware harmony later.** Once chords, voice leading and rhythm are reliable, introduce melody notes and make chord ranking conditional on melody compatibility. Hookpad demonstrates how powerful this combination can become. [Quellenreferenz: turn671206search4]

The resulting project would occupy a useful space that current products only partially cover: **Chord Files' exploratory spirit + ModeWheel's visual theory + Hookpad's data-informed songwriting + Scaler's harmonic depth + an open, explainable theory engine**. Your existing material already covers the first conceptual layer; the highest-value next collection phase is now **machine-readable harmony corpora, formal annotation standards, voice-leading/form theory, genre-specific harmonic grammars, and structured groove data** rather than simply accumulating more general music-theory books. [Quellenreferenz: turn0file4] [Quellenreferenz: turn0file2] [Quellenreferenz: turn671206search4, turn671206search0, turn558318search2]
