# Canonical Documentation Hierarchy

To eliminate duplicate authorities and contradictory guidelines:

1. **Governance & Developer Rules**: `AGENTS.md` (root) is the sole authority for agent contracts.
2. **Architecture & Engineering Contracts**:
   - `docs/engineering/SHELL_EXTRACTION_DEEP_SPEC.md`: Shell extraction & Tkinter isolation.
   - `docs/engineering/MUSIC_DOMAIN_AND_MIDI.md`: Music domain data models & MIDI.
   - `docs/engineering/DATA_STORAGE_AND_PORTABILITY.md`: Persistence, atomicity, and schema versioning.
3. **Decisions**: `decisions/DECISION_REGISTER.md` + individual `ADR-*.md` files.
4. **Knowledge Base (Curated)**: `knowledge/sources/registry.yaml` and `knowledge/concepts/`.
5. **Raw Research (Uncurated Archive)**: `research/` (kept read-only for provenance).
6. **Master Open Tasks**: `%LOCALAPPDATA%\StepsKnowledge\OFFENE_ARBEITSAUFFORDERUNGEN.md`.
