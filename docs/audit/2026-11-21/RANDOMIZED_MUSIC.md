# Randomized music checks and peer findings

The audit started from `3a5db64`. Two independent automated reviewers
examined the theory implementation and the written material. No human
review was recorded. The experiment uses supported 12-TET spellings and
explicitly defined harmonic contexts.

| Generated question | Independent reference used for the comparison |
| --- | --- |
| Chord spelling and slash bass | A 14-spelling INT/DE table and explicit triad and seventh recipes derive the letter, pitch class, quality and bass. |
| Seventh inversions | The bass is independently assigned in each of the four inversions of a major, dominant, minor or half-diminished seventh. The upper register and input order vary. Symmetric or otherwise ambiguous root inference needs written context. |
| Diatonic degrees | Major and natural-minor scale offsets and an independent written letter cycle establish the expected root and triad. |
| Degree round trip | For dominant sevenths and ninths on I/IV in major and III/VI in minor, an explicit label and independent chord formula must survive reconstruction. |
| Transposition | A chromatic offset, relative written letters and an unchanged timing pair are checked on a two-chord progression with a slash bass. |
| Voice leading | An exhaustive Cartesian search checks the minimum total movement of the default style for three voices within its allowed windows. |
| MIDI | A separate SMF reader checks Format 0/1, timing, four chord notes including root doubling, and exactly one bass note against reference calculations. |
| Knowledge retrieval | Randomized case, punctuation and topic mixtures test approved pilot aliases and the evidence boundary. Returned claim IDs, source IDs, locators and the grounded explanation are inspected. |

For chord recipes and degree conventions, see the **Triad qualities**,
**Seventh chords** and **Roman numerals** sections of [Open Music Theory](https://open-musictheory.github.io/docs/fundamentals/triads/).
For applied dominants see **Adding tonicization to diatonic progressions** in [Tonicization](https://viva.pressbooks.pub/openmusictheory/chapter/tonicization/).
The MIDI probe uses the [Standard MIDI Files specification](https://midi.org/standard-midi-files).
These are links and locators for the tests.

## Findings verified and corrected

- The independent inversion probe found 109 incorrect results among 192 standard seventh inversions on the base revision. For example, MIDI 47–50–53–55 represents G7/B in first inversion. The old detector returned D as root. After the change, the same 192 cases and their reverse input ordering passed. A declared triad with an added sixth in the bass is reported as a foreign bass. For complete sus2, sus4 and 7sus4 shapes, a suspended bass tone keeps slash notation and is labelled as a suspension.
- `C7/E → I7(65) → Cmaj7/E` changed the original minor seventh to a major seventh. STEPS now emits explicit `dom7` and `dom9` where its resolver otherwise defaults to major quality. Contextual applied-dominant labels retain their existing syntax.
- The documentation review resolved all 116 positions in the 28 catalog sequences and matched the written root, quality and slash bass. Corrections cover the interval and note-membership claims associated with PROG-004, PROG-012, PROG-013, PROG-015, PROG-020, PROG-023 and PROG-026. A valid G → A7/C♯ realization, MIDI `[55, 59, 67, 74] → [49, 55, 69, 76]`, demonstrates that the inversion alone does not prevent parallels. See the **The Counterpoint Line** section of [First-Species Counterpoint](https://viva.pressbooks.pub/openmusictheory/chapter/first-species-counterpoint/).
- The evaluator now rejects a changed grounded or no-evidence explanation and unsupported alternatives even when status and claim IDs remain correct. The 130 BPM Swing question remains open. The cited local [measurement report](../fable-5.2/GMD_RIDE_DYNAMIK_FORTSETZUNG_2026-11-15.md) covers 185 and 215 BPM, so it cannot substantiate the original 130 BPM target.

## Reproduce and interpret

```sh
python -B scripts/audit_randomized_music.py --seed 42 --trials 512 --json-out /tmp/steps-music-audit.json
python -B scripts/audit_randomized_music.py --seed 42 --trials 512 --area inversions
```

Each failure records the generated question, expected value, observed value
and trial number. Replay uses the recorded Python version. The suite checks
these domains within their documented generated inputs. Style judgments,
alternative contextual readings, historical evidence, human listening and
manual DAW interoperability require their existing separate approvals.
