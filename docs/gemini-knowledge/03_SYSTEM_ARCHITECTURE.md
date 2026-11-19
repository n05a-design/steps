# System Architecture and Data Flow

**Baseline commit:** `00f4d5b9079575260c9f26d6d0f3305ab15e241a`
**Audit date:** 2026-11-19
**Status:** IMPLEMENTED — app, domain, storage, MIDI, and knowledge adapter boundaries exist; product-level architecture acceptance is PARTIAL.
**Status key:** IMPLEMENTED = exists; TESTED = automated evidence; PARTIAL = incomplete; PLANNED = future; BLOCKED = decision or dependency; HISTORICAL = dated state; NOT_EVIDENCED = insufficient evidence.

## Runtime shape

```text
app.main (CLI or Tk entry point)
  └─ app.ui / session controller
       ├─ src.steps.progression session and analysis
       │    ├─ src.steps.theory pitch/chord/interval/voicing
       │    ├─ src.steps.models timeline
       │    └─ src.steps.knowledge adapter → reviewed knowledge
       ├─ src.steps.storage JSON read/write/recovery
       └─ src.steps.midi SMF parse/export services

knowledge/ + research/ ── review/curation ──> product-reviewed examples
```

`src/steps/` holds Python domain and service logic; `app/` owns the CLI, desktop UI and integration. `research/` and archive material are not automatically runtime-approved knowledge. Use `docs/architecture/ARCHITECTURE_OVERVIEW.md` and `docs/IMPLEMENTATION.md` for precise implementation boundaries.

## Component map

| Component | Concrete paths | Role/status |
|---|---|---|
| User entry | `app/main.py`, `app/ui/main_window.py` | IMPLEMENTED CLI/Tkinter prototype |
| Application coordination | `app/ui/session_controller.py` | IMPLEMENTED session orchestration |
| Music domain | `src/steps/theory/`, `src/steps/progression/` | IMPLEMENTED pure-ish typed theory/progression modules |
| Timeline and models | `src/steps/models/timeline.py`, `drums.py`, `swing.py` | IMPLEMENTED models; visible drum workflow PLANNED |
| Storage | `src/steps/storage/` | IMPLEMENTED project IO/atomic write/undo services |
| MIDI | `src/steps/midi/` | IMPLEMENTED SMF tools and export service |
| Knowledge boundary | `src/steps/knowledge/adapter.py`, `app/knowledge.py` | IMPLEMENTED adapter for reviewed examples; not a general research search engine |
| External contracts | `src/steps/ports/` | IMPLEMENTED interface abstractions; backend availability varies |

## Data flow and trust boundary

User input enters the UI/controller, is validated through domain APIs, and becomes project/session state. Save serializes a versioned project through storage. MIDI export converts timed project events to SMF, with expected format-specific losses. The knowledge adapter exposes reviewed learning items; a research archive entry, corpus record, or AI output does not become an approved claim by mere presence.

External documents, corpora, MIDI files, and generated text are untrusted data. They cannot authorize commands, change review status, or provide license clearance. See `docs/governance/RIGHTS_SECURITY_AND_RELEASE.md`.

## Important limits

Playback is not part of accepted v0.1 scope. A Python package and Tk window do not prove a supported installer, complete platform acceptance, or robust accessibility. Do not infer use of Glide code from design or architectural similarities; Glide is a separate project and any reuse needs provenance and license review.

## References

- `docs/architecture/ARCHITECTURE_OVERVIEW.md`
- `docs/architecture/DOMAIN_AND_STORAGE_CONTRACTS.md`
- `docs/engineering/DATA_STORAGE_AND_PORTABILITY.md`
- `docs/engineering/MUSIC_DOMAIN_AND_MIDI.md`
- `app/README.md`
