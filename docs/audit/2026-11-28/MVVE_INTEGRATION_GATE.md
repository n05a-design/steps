# MVVE V2.2 integration gate

This checkpoint follows the [V2.2 completion matrix](MVVE_V22.md). Its initial evidence is bound to commit 822dae6. The exact published SHA, complete sharing inventory, test artifacts and subsequent GitHub job outcomes are recorded separately.

| Gate | Evidence and outstanding decision |
| --- | --- |
| Public history | Review the union of objects reachable from the candidate and absent from observed remote heads and tags. The local report records every commit, tree and blob with its digest, secret classifications and historical path disposition. Input assets, holdout keys and raw transcripts stay local. |
| Both SMF readers | Shared independent bytes cover framing, malformed length, data bytes, terminal events and VLQ limits. The editable reader preserves original event and tempo bytes, SysEx, equal-tick ordering and terminal silence. Explicit tempo metadata is validated by both readers. [Standard MIDI Files](https://midi.org/standard-midi-files) · [Shared fixtures](../../../tests/test_music_audit_stateful.py) |
| Serialization scope | The canonical format 0 and 1 examples round-trip byte for byte. Running status and delta encoding can be normalized without changing musical events. Ancillary chunks and extended header bytes are deliberately not copied. The analysis reader exposes exact tempo metadata separately from the rounded BPM convenience view. Both readers accept a missing End of Track for historical compatibility and reject a malformed explicit marker. Format 2 and SMPTE division remain unsupported. |
| Native CI | The Ubuntu Python matrix still runs the complete suite. Native Windows and macOS join Linux for storage, process lock, parser and installed-wheel checks. The Windows exact-byte job materializes LF with a per-command checkout option. The separate Windows CRLF job runs the three existing assertions with no change to their outcomes or exit codes. [Workflow](../../../.github/workflows/python-tests.yml) · [Shell-owner handoff](MVVE_SHELL_OWNER_HANDOFF.md) |
| Knowledge and skills | The 27 pending cases are assigned by evidence owner, and the A/B/C/D experiment remains available for a separately authorized run. [Review assignment](MVVE_KNOWLEDGE_VALIDATION.md) |
| External integration | An explicitly authorized checkpoint push and draft review are separate from merge. Check real feature/PR runs against the exact head. Default-branch scheduling is a post-merge evidence phase. [GitHub scheduled workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule) |
| Musical release | The enforced gate and independent reviews remain required. The Shell ownership decision, suspended-chord priority, platform/device validation and 27 knowledge cases are still open for their respective areas. [Musical acceptance workflow](../../governance/MUSICAL_RELEASE_ACCEPTANCE.md) |

## Frozen mutation classifications

The 56 original sites report 40 assertion failures, twelve exceptions observed on previously passing witnesses, one initialization failure, and three survivors. These are separate observations from the 21 curated detections. No conventional mutation score is inferred.

| Contract probed by formerly reported execution failures | Product effect |
| --- | --- |
| Interval minor/major branches (129), written unison (229), chromatic transposition (220) | A defined diminished/major-family interval is rejected, or a supported unison or transposition raises a missing table key. |
| SMF header field (139), chunk length tuple (166), channel event width (287), VLQ lower bound (17) | Valid reference files fail to decode, or a valid zero delta fails to encode. |
| Independent reviewer predicate (200) | A syntactically and procedurally valid synthetic independent review is rejected. The check concerns the gate predicate and confers no real approval. |
| Default source registry (21), two-chord claim (177), known catalog version (190), current UTC date (241) | Ordinary checked-in catalog loading fails, or supported synthetic publication data is rejected. These are source/procedure contract violations. |
| German spelling initializer (268) | The modified lookup cannot initialize. This is a separate module-load regression, distinct from a completed behavioral assertion. |

The three survivors remain visible as REVIEW_REQUIRED. Recognition equivalence follows the stable partition and was checked for all 24,576 nonempty pitch-class-set/bass combinations with omissions enabled under the default context. This evidence covers ordered status, symbols, candidate kinds and bass roles in that configuration. Changing elapsed-time rounding from three to four decimals is outside acceptance. A flat sus2 and E flat sus4 can describe the same sounding set. The reading and resulting figure change between 5/3 and slash in the witness. The root-priority decision is open.
