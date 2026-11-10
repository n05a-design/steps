# STEPS Knowledge Curation – Skill README

## Overview
The `steps-knowledge-curation` skill provides automated and standardized procedures for curating the STEPS project knowledge base, cataloging music theory literature, analyzing MIDI files, and maintaining the central register of open work instructions (`OFFENE_ARBEITSAUFFORDERUNGEN.md`).

## Installation & Activation
This workspace skill resides at:
`.agents/skills/steps-knowledge-curation/`

It activates automatically when interacting with Antigravity agents on tasks involving music theory literature, open tasks, research documents, or rights triage in STEPS.

## Directory Structure
```text
.agents/skills/steps-knowledge-curation/
├── SKILL.md             # Main runbook and activation instructions
├── README.md            # Skill architecture and documentation
├── CHANGELOG.md         # Version history
├── references/          # Detailed documentation and guidelines
│   ├── music_taxonomy.md
│   ├── rights_policy.md
│   ├── work_instructions_protocol.md
│   └── canonical_doc_hierarchy.md
├── scripts/             # Executable utilities
│   ├── check_source.py
│   ├── detect_duplicates.py
│   ├── extract_instructions.py
│   └── validate_register.py
├── templates/           # Reusable templates
│   ├── source_entry.md
│   ├── work_instruction_entry.md
│   └── conflict_entry.md
└── tests/               # Automated unit tests
    └── test_curation_tools.py
```

## Running the Self-Test
```bash
python -m unittest discover -s .agents/skills/steps-knowledge-curation/tests/ -v
```
