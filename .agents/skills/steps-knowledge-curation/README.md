# STEPS Knowledge Curation

The [runbook](SKILL.md) describes the review workflow for research sources,
musical claims and open work instructions. It applies when a compatible agent
loads it. The helper scripts run independently from the desktop application.

| Helper | Implemented behavior |
|---|---|
| [check_source.py](scripts/check_source.py) | Resolves the path and hashes the bytes. Supply the intake directory. Without one, `within_bounds` is null in the Python result. |
| [detect_duplicates.py](scripts/detect_duplicates.py) | Finds matching hashes and fails on unreadable eligible files. Compare near duplicates and historical editions during review. |
| [extract_instructions.py](scripts/extract_instructions.py) | Produces untrusted candidates from UTF-8 or BOM-marked UTF-16 text. Unsupported formats or invalid text fail with a diagnostic. |
| [validate_register.py](scripts/validate_register.py) | Checks task headings, IDs, statuses and declared evidence. The canonical CLI run also resolves completion SHAs to local Git commit objects. Review the cited checks and acceptance evidence independently. |
| [check_reference_ids.py](scripts/check_reference_ids.py) | Checks baseline-bound identities, the Golden mirror and v3 graph bindings. The canonical baseline, graph files and review records are required. Named historical graph endpoints stay subject to their recorded review. |
| [backup_knowledge.py](scripts/backup_knowledge.py) | Verifies a snapshot against its manifest and saves the current register before an atomic replacement. |

Music-theory validation, MIDI interpretation and rights clearance require
separate review. The scripts report their technical checks. Confirm exact claims and usage permission against their original evidence. Use trusted checkout and intake directories without concurrent edits during validation.

### Back up or restore the register

The canonical register is
`docs/operations/OFFENE_ARBEITSAUFFORDERUNGEN.md`; helper scripts resolve it
relative to the repository, independent of the current directory or OS.
Commands use the sibling `docs/operations/backups/` directory by default;
Git ignores that local backup directory. Pass `--backup-dir` to select a
different trusted directory.

From the repository root:

```sh
python3 .agents/skills/steps-knowledge-curation/scripts/backup_knowledge.py backup
python3 .agents/skills/steps-knowledge-curation/scripts/backup_knowledge.py list
python3 .agents/skills/steps-knowledge-curation/scripts/backup_knowledge.py restore "<absolute backup file path>"
python3 .agents/skills/steps-knowledge-curation/scripts/validate_register.py
```

Keep the backup and its `.md.json` manifest together in a directory writable
only by trusted operators. The hash detects a mismatch between the two files.
Older backups without a manifest are listed as `UNVERIFIED`. Review those
files independently before recovering them through an isolated register and
creating a new snapshot. Restore validates the snapshot's structure so that
older entries can be recovered. Run the stricter validator afterward to find
any evidence missing from `DONE_VERIFIED` entries.
On Windows, replace `python3` with `python` if that is the installed launcher.

The restore result includes the path of the pre-restore snapshot when a
register existed. A restore lock prevents another invocation from replacing
the register at the same time. Stop editing the register during recovery. If
an interrupted process leaves a lock, check that the process has ended before
removing the lock.

Run the helper and end-to-end tests from the repository root.

```sh
python3 -B -m unittest discover -s .agents/skills/steps-knowledge-curation/tests -v
```

[Test scope and macOS temporary paths](../../../tests/README.md)

On Windows, replace `python3` with `python` if that is the installed launcher.

## Ordner im Skill

| Ordner | Inhalt |
| --- | --- |
| [references](references/README.md) | Taxonomie, Rechte, Dokumenthierarchie und Registerprotokoll. |
| [scripts](scripts/README.md) | Quellenprüfung, Backup, Restore und Registervalidierung. |
| [templates](templates/README.md) | Vorlagen für Quelle, Auftrag und Konflikt. |
| [tests](tests/README.md) | Prüfungen für Werkzeuge und Wiederherstellung. |
