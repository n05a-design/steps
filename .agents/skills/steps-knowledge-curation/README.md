# STEPS Knowledge Curation

The [runbook](SKILL.md) describes the review workflow for research sources,
musical claims and open work instructions. It applies when a compatible agent
loads it. The helper scripts run independently from the desktop application.

| Helper | Implemented behavior |
|---|---|
| [check_source.py](scripts/check_source.py) | Resolves the path and hashes the bytes. Supply the intake directory. Without one, `within_bounds` is null in the Python result. |
| [detect_duplicates.py](scripts/detect_duplicates.py) | Finds matching hashes and fails on unreadable eligible files. Compare near duplicates and historical editions during review. |
| [extract_instructions.py](scripts/extract_instructions.py) | Produces untrusted candidates from UTF-8 or BOM-marked UTF-16 text. Unsupported formats or invalid text fail with a diagnostic. Reports bind the path and SHA-256 to the bytes used for extraction. |
| [validate_register.py](scripts/validate_register.py) | Checks task headings, IDs, statuses and declared evidence. The canonical CLI run also resolves completion SHAs to local Git commit objects. Review the cited checks and acceptance evidence independently. |
| [check_reference_ids.py](scripts/check_reference_ids.py) | Checks baseline-bound identities, the Golden mirror, v3 graph bindings and row-wise evidence fingerprints. The canonical baseline, graph files and review records are required. Named historical graph endpoints stay subject to their recorded review. |
| [backup_knowledge.py](scripts/backup_knowledge.py) | Verifies a snapshot against its manifest and saves the current register before an atomic replacement. |

Music-theory validation, MIDI interpretation and rights clearance require
separate review. The scripts report their technical checks. Use `--json` for source, duplicate and register output in automated callers. Confirm exact claims and usage permission against their original evidence. Use trusted checkout and intake directories without concurrent edits during validation.

### Review a proposed evidence change

The [versioned fingerprints](../../../knowledge/research/CURATION_EVIDENCE_FINGERPRINTS.json)
cover the three catalog tables, Golden test and source metadata, v3 graph
audit and review records, the historical reference inventory, and domain
readiness rows. The initial fingerprints record the input from STEPS
`539b6d7107d5d10e8501c123307910690e4c1850`. They preserve the recorded
values and gaps, including evidence still pending review.

For an independently reviewed correction, inspect the proposed fingerprints
using the command below. It writes to stdout. Compare the data, scope and
evidence changes in the pull request before updating the versioned file.
Use the historical migration register as well when changing a protected
identity. Changes to the fingerprints require human review. Keep exactly one
`ACTIVE` controlled correction per ID. Preserve the replaced entry as
`SUPERSEDED` and record the exact approved identity SHA-256. The verifier
currently handles baseline schema `1.3.0`.

```sh
python3 -B .agents/skills/steps-knowledge-curation/scripts/check_reference_ids.py --print-evidence-snapshot
```

### Back up or restore the register

The canonical register is
`docs/operations/OFFENE_ARBEITSAUFFORDERUNGEN.md`; helper scripts resolve it
relative to the repository, independent of the current directory or OS.
Canonical register validation needs Git history containing the declared evidence commits. Fetch the history before running this check in a shallow checkout.

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
only by trusted operators. The hash detects a mismatch between the two files. Version 3 snapshots bind
the original absolute register path to a local identity. The identity is
stored in the worktree's private Git directory or, for a standalone register,
in its default backup directory. Keep the identity with the original local
checkout. Regular destinations retain their POSIX mode on restore.

The `list` report separates manifest integrity, destination binding
(`restore_scope`), and completion evidence fields (`completion_evidence`).
Pass `--register` when inspecting a shared backup directory. Versions 1 and 2
lack the local identity and are listed as `UNBOUND`. Review the origin and
target before invoking `restore --allow-other-register` for an unbound snapshot
or a moved checkout. A matching register filename and valid structure are
required. Historical copies without a manifest need separate review in an
isolated register before they can be snapshotted.

Recovery with missing completion fields requires `--allow-incomplete-evidence`.
Use that option for a reviewed repair. The restore result reports incomplete
fields explicitly. Run the canonical validator afterward to resolve completion
commits in local Git, and confirm the supporting evidence before accepting any
`DONE_VERIFIED` claim.
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
