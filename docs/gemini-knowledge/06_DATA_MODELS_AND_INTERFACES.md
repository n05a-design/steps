# Data Models and Interfaces

**Baseline commit:** `00f4d5b9079575260c9f26d6d0f3305ab15e241a`
**Audit date:** 2026-11-19
**Status:** IMPLEMENTED — project, theory, timeline, storage, MIDI, and port abstractions exist; broad compatibility remains PARTIAL.
**Status key:** IMPLEMENTED = exists; TESTED = automated evidence; PARTIAL = incomplete; PLANNED = future; BLOCKED = decision or dependency; HISTORICAL = dated state; NOT_EVIDENCED = insufficient evidence.

## Data boundaries

- **Project**: user composition and musical context, stored separately from app preferences and research sources.
- **Settings**: UI language and app preferences; must not be confused with note naming or project content.
- **Knowledge/research**: source-bound claims and reviewed learning content; raw source files do not become app content by default.

## Concrete models and contracts

| Model/API area | Path | Status / constraint |
|---|---|---|
| Pitch and notation | `src/steps/theory/pitch.py` | IMPLEMENTED typed pitch classes and spelling; `DE`/`INT` are distinct conventions |
| Chord structures | `src/steps/theory/chord.py`, `triad.py`, `seventh.py` | IMPLEMENTED parser/construction for supported symbols; unsupported forms can be rejected |
| Progression state | `src/steps/progression/session.py` | IMPLEMENTED edits/history and context workflows |
| Timeline | `src/steps/models/timeline.py` | IMPLEMENTED tick-based event timing |
| Project IO | `src/steps/storage/project_io.py`, `atomic.py` | IMPLEMENTED JSON read/write and atomic-storage mechanisms |
| JSON schemas | `schemas/project.schema.json`, `chord.schema.json`, `progression.schema.json`, `analysis.schema.json`, `source.schema.json`, `drum_pattern.schema.json` | Present; schema presence alone does not prove complete semantic coverage |
| Ports | `src/steps/ports/` | Interface definitions for event, storage, MIDI, audio, knowledge |
| MIDI time/export | `src/steps/midi/time.py`, `export_service.py`, `smf.py` | IMPLEMENTED conversion/export services; SMF has intentional information-loss boundaries |

The project-file schema version is independent of `VERSION`, package version, and research-library versions. Compatibility and migration rules belong in `docs/architecture/PROJECT_SCHEMA_MIGRATION.md`.

## Time and serialization

Use integer ticks under a declared PPQ where implemented. Preserve event onset and duration independently; do not infer gaps or overlaps from list order. UI `bar:beat:tick` is a projection; absolute ticks are the stored/exported time truth. MIDI events use format-specific delta-time encoding; project semantics and SMF encoding must not be conflated.

## Open model questions

Not every proposed field or future Drum model is product-delivered. Confirm `schemas/` and Python contracts before implementing; do not assume schema stubs define all domain behavior. Recheck supported chord syntax, migrations, event payloads, and information loss in tests.

## References

- `docs/engineering/DATA_STORAGE_AND_PORTABILITY.md`
- `docs/architecture/DOMAIN_AND_STORAGE_CONTRACTS.md`
- `docs/architecture/PROJECT_SCHEMA_MIGRATION.md`
- `docs/theory/API.md`
- `schemas/README.md`
