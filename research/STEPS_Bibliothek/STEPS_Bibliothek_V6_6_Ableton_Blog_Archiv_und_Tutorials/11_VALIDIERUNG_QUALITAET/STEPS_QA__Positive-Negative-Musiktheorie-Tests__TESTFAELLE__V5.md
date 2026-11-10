# Konzeptionelle Positiv-/Negativfälle für Codex V5

Diese Fälle sind **testbare Anforderungen an künftige Analyseantworten**, derzeit kein ausgeführter Algorithmustest. Erwartungsstatements stehen neben bewusst verbotenen Überbehauptungen. Der Bezug auf eine Quelle bedeutet thematische Forschungsbasis, nicht zwingend geprüfter Seitenbeleg für die exakte Formulierung.

### V5-CASE-001 – F#4 / Gb4

- **Akzeptieren:** equal sounding pc 6 in 12TET
- **Nicht behaupten:** same spelled note
- **Forschungsanker:** V5-001 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-002 – C to E / C to Fb

- **Akzeptieren:** major third vs diminished fourth despite equal 12TET span
- **Nicht behaupten:** same interval quality
- **Forschungsanker:** V5-001 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-003 – German H vs international B

- **Akzeptieren:** both represent pitch class 11 in common 12TET naming
- **Nicht behaupten:** German B is B natural
- **Forschungsanker:** V5-001 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-004 – German B vs international Bb

- **Akzeptieren:** both represent pitch class 10 in common 12TET naming
- **Nicht behaupten:** German B is identical to English B natural
- **Forschungsanker:** V5-001 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-005 – C7(b9)

- **Akzeptieren:** C E G Bb Db are canonical spelled chord tones
- **Nicht behaupten:** C# is the canonical flat ninth
- **Forschungsanker:** V5-026 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-006 – Cmaj9 / C9

- **Akzeptieren:** maj9 includes B, dominant 9 includes Bb
- **Nicht behaupten:** both imply same seventh
- **Forschungsanker:** V5-026 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-007 – Csus4

- **Akzeptieren:** suspension replaces third in basic chord symbol
- **Nicht behaupten:** E is obligatory in basic Csus4
- **Forschungsanker:** V5-026 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-008 – Cadd9

- **Akzeptieren:** D added to C major; seventh not implied
- **Nicht behaupten:** Bb always present
- **Forschungsanker:** V5-026 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-009 – Gb major scale

- **Akzeptieren:** Gb Ab Bb Cb Db Eb F
- **Nicht behaupten:** Gb Ab Bb B Db Eb F is correctly spelled diatonic
- **Forschungsanker:** V5-001 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-010 – F# major scale

- **Akzeptieren:** F# G# A# B C# D# E#
- **Nicht behaupten:** F# G# A# B C# D# F is correctly spelled diatonic
- **Forschungsanker:** V5-001 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-011 – C# major scale

- **Akzeptieren:** C# D# E# F# G# A# B#
- **Nicht behaupten:** C# D# F F# G# A# C is canonical spelling
- **Forschungsanker:** V5-001 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-012 – C/E vs V/ii

- **Akzeptieren:** slash bass syntax vs applied Roman numeral syntax
- **Nicht behaupten:** treat slash as one grammar
- **Forschungsanker:** V5-010 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-013 – Dm7 G7 Dm7 with D pedal

- **Akzeptieren:** D-Dorian is plausible
- **Nicht behaupten:** must be ii-V in C
- **Forschungsanker:** V5-001 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-014 – Dm7 G7 C major cadence

- **Akzeptieren:** ii V I in C is plausible
- **Nicht behaupten:** must be D-Dorian
- **Forschungsanker:** V5-001 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-015 – Em F Em with E tonic

- **Akzeptieren:** Phrygian-context bII color plausible
- **Nicht behaupten:** must be a functional cadence in C
- **Forschungsanker:** V5-001 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-016 – C Bb F C

- **Akzeptieren:** Mixolydian-oriented I bVII IV I plausible
- **Nicht behaupten:** must be in F major
- **Forschungsanker:** V5-001 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-017 – Am Dm E7 Am

- **Akzeptieren:** G# in E7 is common minor dominant practice
- **Nicht behaupten:** A natural minor forbids G#
- **Forschungsanker:** V5-001 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-018 – Am G F Em

- **Akzeptieren:** E minor v is plausible in modal/pop minor
- **Nicht behaupten:** the v is automatically wrong
- **Forschungsanker:** V5-001 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-019 – C D E F G A B

- **Akzeptieren:** pitch collection cannot prove tonic
- **Nicht behaupten:** pitch collection necessarily C-Ionian
- **Forschungsanker:** V5-001 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-020 – D E F G A B C

- **Akzeptieren:** pitch collection cannot prove D-Dorian
- **Nicht behaupten:** every sample using these notes is D-Dorian
- **Forschungsanker:** V5-001 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-021 – G7 C recurring vamp

- **Akzeptieren:** chord pair alone does not prove cadence
- **Nicht behaupten:** every G7-C is perfect authentic cadence
- **Forschungsanker:** V5-007 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-022 – Fmaj7 Fm6 C

- **Akzeptieren:** iv mixture context possible
- **Nicht behaupten:** F minor chord always sad
- **Forschungsanker:** V5-001 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-023 – C A7 Dm

- **Akzeptieren:** A7 is V7/ii in common C major reading
- **Nicht behaupten:** A7 entails modulation to D minor
- **Forschungsanker:** V5-010 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-024 – C E7 Am

- **Akzeptieren:** E7 is V7/vi in common C-major reading
- **Nicht behaupten:** E7 must mean E major is new tonic
- **Forschungsanker:** V5-010 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-025 – C G7 Am

- **Akzeptieren:** deceptive move is context dependent
- **Nicht behaupten:** V7-vi always marks end of phrase
- **Forschungsanker:** V5-001 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-026 – G7 Db7 to C

- **Akzeptieren:** tritone substitution is a possible jazz lens
- **Nicht behaupten:** Db7 is sounding-identical to G7
- **Forschungsanker:** V5-026 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-027 – Db7 guides

- **Akzeptieren:** Db7 contains F and Cb (enharmonic B)
- **Nicht behaupten:** Db7 is written F and B in standard tertian spelling
- **Forschungsanker:** V5-026 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-028 – Cmaj7 Am7

- **Akzeptieren:** C E G common tones in suitable voicing
- **Nicht behaupten:** exact same voiceleading regardless register
- **Forschungsanker:** V5-015 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-029 – C E Ab C

- **Akzeptieren:** chromatic-mediant explanation can be relevant
- **Nicht behaupten:** must be I V/vi bVI I in all contexts
- **Forschungsanker:** V5-015 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-030 – C7 in 12-bar blues

- **Akzeptieren:** I7 as tonic color is valid
- **Nicht behaupten:** C7 must be V7/IV
- **Forschungsanker:** V5-007 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-031 – F7 in C blues

- **Akzeptieren:** IV7 is blues-conventional
- **Nicht behaupten:** F7 is illegal in C blues
- **Forschungsanker:** V5-007 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-032 – Am F C G

- **Akzeptieren:** C-major vi IV I V and A-minor i VI III VII possible
- **Nicht behaupten:** key can be established without other context
- **Forschungsanker:** V5-005 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-033 – Am F G G leading to C chorus

- **Akzeptieren:** emergent tonic hypothesis possible
- **Nicht behaupten:** if C is absent in verse no C-center can be heard
- **Forschungsanker:** V5-005 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-034 – Cmaj7 Fm6 C/E

- **Akzeptieren:** potential A-Ab-G line if voiced
- **Nicht behaupten:** A-Ab-G automatically occurs in every voicing
- **Forschungsanker:** V5-015 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-035 – C E7 Am

- **Akzeptieren:** G# in E7 is leading tone to A
- **Nicht behaupten:** E7 has G natural in default spelling
- **Forschungsanker:** V5-026 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-036 – Cmaj7 #11

- **Akzeptieren:** F# can be extension #11
- **Nicht behaupten:** Gb is the canonical spelled #11
- **Forschungsanker:** V5-026 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-037 – 8 bars unspecified

- **Akzeptieren:** eight bars alone do not establish sentence form
- **Nicht behaupten:** always sentence
- **Forschungsanker:** V5-002 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-038 – 4+4 with weak/strong endings

- **Akzeptieren:** antecedent/consequent period hypothesis possible
- **Nicht behaupten:** all 4+4 blocks are periods
- **Forschungsanker:** V5-002 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-039 – motif C D E augmentation

- **Akzeptieren:** rhythmic durations scale while pitch order preserved
- **Nicht behaupten:** always invert pitch too
- **Forschungsanker:** V5-001 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-040 – motif C D E chromatic inversion around C

- **Akzeptieren:** C Bb Ab is one possible chromatic mirror
- **Nicht behaupten:** inversion is always unique without pivot
- **Forschungsanker:** V5-001 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-041 – retrograde

- **Akzeptieren:** reverses chosen ordered dimension
- **Nicht behaupten:** all retrogrades must reverse pitch and timing identically
- **Forschungsanker:** V5-001 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-042 – theme and variation

- **Akzeptieren:** motivic relation requires specified invariant/operation
- **Nicht behaupten:** different chords alone prove thematic variation
- **Forschungsanker:** V5-002 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-043 – form Verse Prechorus Chorus

- **Akzeptieren:** harmonic trajectory may culminate on chorus entrance
- **Nicht behaupten:** cadence must be last bar of chorus
- **Forschungsanker:** V5-003 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-044 – no tonic until chorus

- **Akzeptieren:** emergent tonic is one analytic hypothesis
- **Nicht behaupten:** tonic must sound each verse
- **Forschungsanker:** V5-005 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-045 – new orchestration same harmony

- **Akzeptieren:** timbral density and register matter for perception
- **Nicht behaupten:** same chords implies identical impression
- **Forschungsanker:** V5-019 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-046 – cantus firmus species check

- **Akzeptieren:** species rules apply under specified strict framework
- **Nicht behaupten:** species rules govern all musical styles
- **Forschungsanker:** V5-001 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-047 – MIDI imported score

- **Akzeptieren:** MIDI note PCs cannot recover unique enharmonic spelling
- **Nicht behaupten:** MIDI pitch 66 always notated F#
- **Forschungsanker:** V5-024 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-048 – 32-bar piece without phrase metadata

- **Akzeptieren:** bar count does not determine form
- **Nicht behaupten:** always AABA
- **Forschungsanker:** V5-003 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-049 – maqam pitch collection

- **Akzeptieren:** maqam includes melodic course sayr and jins-related practice
- **Nicht behaupten:** maqam equals western scale rotation
- **Forschungsanker:** V5-020 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-050 – Hindustani raga

- **Akzeptieren:** raga includes performative and aesthetic aspects
- **Nicht behaupten:** raga equals chord progression
- **Forschungsanker:** V5-021 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-051 – African rhythm generic label

- **Akzeptieren:** avoid treating diverse practices as uniform
- **Nicht behaupten:** all African music has one rhythmic system
- **Forschungsanker:** V5-022 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-052 – Rock corpus historical bias

- **Akzeptieren:** genre sample and era distributions affect claims
- **Nicht behaupten:** all observed percentages are universal
- **Forschungsanker:** V5-007 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-053 – ChoCo JAAH/CASD/Mozart subset

- **Akzeptieren:** specific subsets have CC BY-NC-SA exception
- **Nicht behaupten:** all ChoCo CC BY 4.0 unrestricted
- **Forschungsanker:** V5-011 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-054 – When in Rome converted analysis

- **Akzeptieren:** derived analyses may retain original license
- **Nicht behaupten:** all source analysis files share one new license
- **Forschungsanker:** V5-012 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-055 – music21 code corpus

- **Akzeptieren:** BSD code does not imply unrestricted corpus
- **Nicht behaupten:** all encoded scores are BSD
- **Forschungsanker:** V5-013 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-056 – publisher abstract source

- **Akzeptieren:** metadata landing page is not full book review
- **Nicht behaupten:** can cite nonexistent page as read
- **Forschungsanker:** V5-015 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-057 – DCML applied chord

- **Akzeptieren:** relative slash relates to local context
- **Nicht behaupten:** every slash means a bass inversion
- **Forschungsanker:** V5-010 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-058 – MIDI 2.0

- **Akzeptieren:** extension to MIDI 1.0
- **Nicht behaupten:** MIDI 1.0 is universally obsolete
- **Forschungsanker:** V5-025 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-059 – MusicXML 4.0

- **Akzeptieren:** symbolic score exchange format
- **Nicht behaupten:** guarantees identical audio across apps
- **Forschungsanker:** V5-024 (Status im Quellenregister).
- **Fachreview:** offen.

### V5-CASE-060 – style-specific valid example

- **Akzeptieren:** explain musical scope and alternate traditions
- **Nicht behaupten:** style categories are rigid universal correctness constraints
- **Forschungsanker:** V5-022 (Status im Quellenregister).
- **Fachreview:** offen.

