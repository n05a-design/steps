# STEPS Knowledge Curation

The [runbook](SKILL.md) describes the review workflow for research sources,
musical claims and open work instructions. It applies when a compatible agent
loads it. The helper scripts run independently from the desktop application.

| Helper | Implemented behavior |
|---|---|
| [check_source.py](scripts/check_source.py) | Resolves the path and hashes the bytes. A supplied base directory limits which files may be opened. |
| [detect_duplicates.py](scripts/detect_duplicates.py) | Looks for matching content hashes. Near duplicates and conflicting editions require review. |
| [extract_instructions.py](scripts/extract_instructions.py) | Labels extracted text as untrusted document candidates, including TODO markers. |
| [validate_register.py](scripts/validate_register.py) | Checks identifiers, one status per task and evidence fields for DONE_VERIFIED. Review the referenced commit, checks and acceptance evidence independently. |
| [backup_knowledge.py](scripts/backup_knowledge.py) | Verifies a snapshot against its manifest and saves the current register before an atomic replacement. |

Music-theory validation, MIDI interpretation and rights clearance require
separate review. The scripts do not establish factual correctness or rights.

### Back up or restore the register

Set `STEPS_KNOWLEDGE_REGISTER` to the absolute path of the existing master.
Windows uses `%LOCALAPPDATA%\StepsKnowledge\OFFENE_ARBEITSAUFFORDERUNGEN.md`
when that setting is absent. Commands use the sibling `backups/` directory
by default. Pass `--backup-dir` to select a different trusted directory.

From the repository root:

```sh
python .agents/skills/steps-knowledge-curation/scripts/backup_knowledge.py backup
python .agents/skills/steps-knowledge-curation/scripts/backup_knowledge.py list
python .agents/skills/steps-knowledge-curation/scripts/backup_knowledge.py restore "<absolute backup file path>"
python .agents/skills/steps-knowledge-curation/scripts/validate_register.py
```

Keep the backup and its `.md.json` manifest together in a directory writable
only by trusted operators. The hash detects a mismatch between the two files.
Older backups without a manifest are listed as `UNVERIFIED`. Review those
files independently before recovering them through an isolated register and
creating a new snapshot. Restore validates the snapshot's structure so that
older entries can be recovered. Run the stricter validator afterward to find
any evidence missing from `DONE_VERIFIED` entries.

The restore result includes the path of the pre-restore snapshot when a
register existed. A restore lock prevents another invocation from replacing
the register at the same time. Stop editing the register during recovery. If
an interrupted process leaves a lock, check that the process has ended before
removing the lock.

Run the helper and end-to-end tests from the repository root.

```sh
python -B -m unittest discover -s .agents/skills/steps-knowledge-curation/tests -v
```

[Test scope and macOS temporary paths](../../../tests/README.md)

## Ordner im Skill

| Ordner | Inhalt |
| --- | --- |
| [references](references/README.md) | Taxonomie, Rechte, Dokumenthierarchie und Registerprotokoll. |
| [scripts](scripts/README.md) | Quellenprüfung, Backup, Restore und Registervalidierung. |
| [templates](templates/README.md) | Vorlagen für Quelle, Auftrag und Konflikt. |
| [tests](tests/README.md) | Prüfungen für Werkzeuge und Wiederherstellung. |
