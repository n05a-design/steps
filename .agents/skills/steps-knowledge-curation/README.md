# STEPS Knowledge Curation

The [runbook](SKILL.md) describes the review workflow for research sources,
musical claims and open work instructions. It applies when a compatible agent
loads it. The helper scripts run independently from the desktop application.

| Helper | Implemented behavior |
|---|---|
| [check_source.py](scripts/check_source.py) | Resolves the path, hashes the bytes and reports whether the resolved file is within the supplied base path. The boundary result is informational. |
| [detect_duplicates.py](scripts/detect_duplicates.py) | Looks for matching content hashes. Near duplicates and conflicting editions require review. |
| [extract_instructions.py](scripts/extract_instructions.py) | Extracts text patterns for possible work instructions. |
| [validate_register.py](scripts/validate_register.py) | Checks register structure and identifiers. Source locators and factual support require separate review. |
| [backup_knowledge.py](scripts/backup_knowledge.py) | Provides snapshot and restore operations. Treat the backup and its metadata as trusted inputs and verify restoration independently before relying on it. |

Music-theory validation, MIDI interpretation and rights clearance require
separate review. The scripts do not establish factual correctness or rights.

Run the helper and end-to-end tests from the repository root.

```sh
python -B -m unittest discover -s .agents/skills/steps-knowledge-curation/tests -v
```

[Test scope and macOS temporary paths](../../../tests/README.md)
