# STEPS Reference Identity Baseline Provenance Report (Phase 4.16)

**Date**: 2026-11-11  
**Phase**: STEPS Phase 4.16  
**Document**: Provenance, Chronology, and Non-Circularity Verification of `REFERENCE_IDENTITY_BASELINE.json`  
**Status**: **VERIFIED AUTHORITATIVE**

---

## 1. Provenance Integrity & Anti-Circularity Guarantee

A critical vulnerability in baseline-driven testing is circularity: generating a baseline from already corrupted or drifted repository files, thereby crystallizing errors as normative truths.

In STEPS Phase 4.16, every entity in `knowledge/research/REFERENCE_IDENTITY_BASELINE.json` is traced back to its historical point of entry in the Git commit record, verified against primary musicological literature, and locked against unrecorded regeneration.

---

## 2. Chronological Provenance by Entity Corpus

### 2.1 Chord Progressions (`PROG-001` .. `PROG-027`)
- **PROG-001 to PROG-010 (Phase 4.1 - Commit `7ca4bf1`)**:
  - Foundational Western diatonic progressions: Pop Four Chords (`I-V-vi-IV`), Andalusian Cadence (`i-bVII-bVI-V`), 50s Doo-Wop (`I-vi-IV-V`), Jazz ii-V-I (`ii7-V7-Imaj7`), Pachelbel Canon (`I-V-vi-iii-IV-I-IV-V`), 12-Bar Blues, Blues Minor, Folk Modal (`i-bVII-v-i`), Epic Hero (`i-bVI-III-bVII`), Royal Road (`IVmaj7-V7-iii7-vi`).
  - Primary Sources: Walter Piston (*Harmony*, 1987), Stefan Kostka (*Tonal Harmony*, 2013).
- **PROG-011 to PROG-023 (Phase 4.9 - Commit `61cb95a`)**:
  - Advanced functional and non-functional idioms: Lydian Chromatic Cadence, Backdoor Turnaround (`iv7-bVII7-Imaj7`), SubV7 Tritone Substitution, Chromatic Mediants, Neo-Soul minor modal cycles (`Dm9-Gm9-Bbmaj9-A7b9`), Picardy Third, Dorian Vamp, Mixolydian Rock vamp.
  - Primary Sources: Mark Levine (*The Jazz Theory Book*, 1995), Nicole Biamonte (*Triadic Modal and Pentatonic Patterns in Rock Music*, 2010).
- **PROG-024 to PROG-027 (Phase 4.11 / 4.14 - Commit `a14c3f3` & `d7d7f1e`)**:
  - Extended modulatory cycles: Coltrane Matrix (`Cmaj7-Eb7-Abmaj7-B7-Emaj7-G7-Cmaj7`), Lydian Major Vamp (`Cmaj7(#11) - D/C`), Extended Phrygian Cadence (`Fm - Gbmaj7 - E°7 - Fm`).
  - Primary Sources: Dmitri Tymoczko (*A Geometry of Music*, 2011), John Coltrane (*Giant Steps*, 1960).

### 2.2 Drum Patterns (`PAT-001` .. `PAT-031`)
- **PAT-001 to PAT-010 (Phase 4.1)**:
  - Standard acoustic and electronic rhythm staples: Pop/Rock Straight, Classic House 4-on-the-Floor, Boom-Bap Hip-Hop with MPC swing ($\rho \approx 1{,}28$), UK Garage 2-Step, Berlin Peak Techno 909, Trap Halftime with rolling 32nd hats, Motown Stomp, Amen Drum & Bass break, Funk "The One", Reggae One Drop.
- **PAT-011 to PAT-020 (Phase 4.7)**:
  - Extended world and regional styles: Afrobeat Talking Drum feel, Bebop fast ride comping ($\rho \approx 1{,}85$), Linear Funk ghost notes, Soul Ballad 12/8 compound meter, Reggae Steppers & Rockers, Liquid D&B, Neurofunk gated drums, Authentic UKG 2-Step.
- **PAT-021 to PAT-031 (Phase 4.10 / 4.14 / 4.15)**:
  - Contemporary electronic and polyrhythmic expansions: Jungle Amen Chopped, Jump-Up Minimal Bouncer, Drill Sliding Bass pattern, Footwork/Juke 160 BPM syncopated patterns, Berlin Peak Techno variants, Afrobeat 12/8 polyrhythm (PAT-031).

### 2.3 Piano Practice Modules (`P01` .. `P19`)
- **P01 to P10 (Phase 4.3 / 4.7)**:
  - Elementary keyboard topography and foundational voice leading: Stamm-Dreiklänge & Topografie, Umkehrungen & Topografisches Greifen, Guide-Tone Jazz Voicings (3-7), Pop Comping Arpeggio Patterns, Neo-Soul Extended 9th Voicings, Blues Comping & Charleston Rhythms, Voice Leading Parallelen-Vermeidung, Ear Training Voicing Decoders.
- **P11 to P17 (Phase 4.8 / 4.12)**:
  - Intermediate and advanced accompaniment techniques: Inversion Code decoding, Two-Handed Rootless Voicings (LH Bass + RH Upper Extension Triads), Reharmonization in Practice (Modal Interchange & Picardy Thirds), Bossa Nova & Latin Piano Comping, Voice Leading with Chromatic Mediants, Upper Structure Triads over Dominant 7ths, Contemporary Syncopated Gospel Comping.
- **P18 to P19 (Phase 4.13 / 4.14 / 4.15)**:
  - Refined voice-leading modules: Backdoor Guide-Tone Voicings ($iv^7 \to \flat VII^7 \to I^{\text{maj}7}$, with semitone resolution of 7th $Ab \to G$ and whole-tone step of 3rd $D \to E$), Chromatic Bass Lines for Secondary Dominants in 1st Inversion ($V^7/V(6/5)$).

### 2.4 Concept Relations (`CR-001` .. `CR-094`)
- 94 Authoritative relational edges connecting harmonic progressions, drum styles, piano modules, and theoretical axioms across domains M01 to M12 in `knowledge/relations/MUSIC_CONCEPT_RELATIONS.csv`.

### 2.5 Golden Reference Cases (`REF-0001` .. `REF-0198`)
- **REF-0001 to REF-0094 (Historical Suite - Phase 4.1 to Phase 4.13)**:
  - Originally designated as test verification cases T01..T16 in `MUSICAL_REFERENCE_VALIDATION.csv`. Reconstructed in Phase 4.15 to permanently prevent identity collision.
- **REF-0095 to REF-0100 (Historical Integration Cases - Phase 4.13)**:
  - Cross-domain integration cases linking Coltrane cycles, drum grooves, and piano voicings.
- **REF-0101 to REF-0198 (Migrated Suite - Phase 4.14 / 4.15)**:
  - Algorithmic and acoustic evaluation test cases introduced in Phase 4.14. Formerly collided with REF-0001..REF-0098, migrated in Phase 4.15 to clean non-colliding IDs `REF-0101`..`REF-0198`.

---

## 3. Anti-Drift Guarantee

1. No automatic baseline regeneration is executed on test failures.
2. Any modification of identity-defining fields without an entry in `REFERENCE_ID_MIGRATION_REGISTER.csv` triggers fail-closed execution error 1.
3. Every baseline update is tracked in version control with git commit signatures and audit reports.
