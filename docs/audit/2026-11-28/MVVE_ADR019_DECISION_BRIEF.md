# ADR-019 decision brief for multiple MIDI inputs

**Status** Proposed. ADR-007 and ADR-019 govern the current product. Current single-source output remains the production contract. [ADR-007](../../../decisions/ADR-007-audio-nur-dateiexport-v01.md) · [ADR-019](../../../decisions/ADR-019-live-audio-preview-and-midi-input.md)

| Option | State boundary | Consequences |
| --- | --- | --- |
| Endpoint-keyed reducer | One deterministic reducer owns note state keyed by source, device generation, channel and note number. Mouse and computer key events have local source identities. | An immutable input envelope gives exact replay, channel-local controllers and deterministic teardown. All consumers need a projection of sounding notes and separate selected notes. |
| Per-device input adapters | Each adapter owns its channel state and sends ordered updates to a merger. Local keyboard owns its own adapter. | Device failure is isolated. The merger must define ordering, snapshots and source generation identifiers before display consumers can replay mixed inputs. |
| Keep the approved single-source contract | The existing reducer and port remain the production route. | Physical multi-device input stays a proposed capability. The headless test model can continue to exercise candidate behavior. |

For either multi-source option, note-on velocity zero behaves as note-off. Decide duplicate handling by input type. The draft treats repeated local key-down as idempotent. Specify FIFO or retrigger behavior for incoming MIDI duplicates before adoption. Sustain and CC120, CC121 and CC123 address an endpoint channel, focus loss only the local source, unplug only the disconnected device generation, and panic all transient sources. Focus or device cleanup preserves selected notes. Adapter threads enqueue immutable events. One owner processes them in order and discards queued events from a disconnected generation.

Approval requires traces with identical notes from two devices and channels, independent pedals, controller reset while a note is held, repeated key events, reordered delivery, blocked UI thread, unplug/replug and late events after disconnect. Demonstrate no stuck notes and no unrelated release. Use native target hardware for device identity and lifecycle acceptance. The 35 interleavings and fixed endpoint snapshots are headless evidence for the draft. [Stateful tests](../../../tests/test_music_audit_stateful.py) · [MIDI message summary](https://midi.org/summary-of-midi-1-0-messages)
