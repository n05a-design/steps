---
name: steps-knowledge-curation
description: >-
  Curation, validation, and incremental maintenance of the STEPS music theory
  knowledge base, music library research documents, and open work instructions
  (OFFENE_ARBEITSAUFFORDERUNGEN.md). Use whenever new research files, music theory
  books, MIDI corpora, or task specifications are added or audited in STEPS.
---

# STEPS Knowledge Curation Skill

This skill provides verified, reproducible procedures and executable helper scripts to inspect, categorize, and incrementally integrate music theory literature, MIDI files, research documents, and open work instructions into the STEPS project without data loss or unverified claims.

## Core Responsibilities

1. **Source Ingestion & Provenance**: Track every file by exact path, size, and SHA-256 hash. Distinguish between own project files, public open-access sources, and proprietary/copyright-protected third-party assets (P0-1 compliance).
2. **Music Theory Validation**: Enforce the 5 foundational theory axioms from `docs/engineering/MUSIC_DOMAIN_AND_MIDI.md`:
   - Sounding pitch $\neq$ pitch class (0..11) $\neq$ note spelling.
   - Chord identity $\neq$ chord symbol $\neq$ voicing $\neq$ inversion $\neq$ context function.
   - Progression $\neq$ rhythmic events (`MusicTime` ticks) $\neq$ phrasing $\neq$ style context.
   - Deterministic rule $\neq$ corpus statistic $\neq$ creative heuristic.
   - Notation $\neq$ MIDI export $\neq$ audio playback.
3. **Open Work Instructions Maintenance**: Maintain the single canonical master register:
   `%LOCALAPPDATA%\StepsKnowledge\OFFENE_ARBEITSAUFFORDERUNGEN.md`.
   Ensure no duplicate tasks are introduced, and all tasks trace back to explicit source anchors.

---

## Workflow: Incremental Integration of New Documents

When a user adds or updates a music document or specification:

```text
[New/Modified File]
        │
        ▼
1. Run Identification & Hash Check:
   python .agents/skills/steps-knowledge-curation/scripts/check_source.py <file_path>
        │
        ▼
2. Check for Duplicates & Prior Versions:
   python .agents/skills/steps-knowledge-curation/scripts/detect_duplicates.py <file_path>
        │
        ▼
3. Determine Rights & Privacy Scope (P0-1):
   Verify license, copyright markers, and commercial indicators.
   Proprietary/copyrighted files must remain METADATA_ONLY and outside public Git commits.
        │
        ▼
4. Extract Claims & Work Instructions:
   python .agents/skills/steps-knowledge-curation/scripts/extract_instructions.py <file_path>
        │
        ▼
5. Update Canonical Master File:
   Append or update OA-* entries in:
   %LOCALAPPDATA%\StepsKnowledge\OFFENE_ARBEITSAUFFORDERUNGEN.md
```

---

## Detailed References

- [Music Knowledge Taxonomy](./references/music_taxonomy.md)
- [Rights & License Policy](./references/rights_policy.md)
- [Open Work Instructions Protocol](./references/work_instructions_protocol.md)
- [Canonical Documentation Hierarchy](./references/canonical_doc_hierarchy.md)

---

## Verification & Self-Test

Run the automated test suite to ensure the skill and its helpers are working correctly:
```bash
python -m unittest discover -s .agents/skills/steps-knowledge-curation/tests/ -v
```
