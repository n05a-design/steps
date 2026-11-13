"""Create and restore integrity-checked snapshots of the canonical register."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import stat
import tempfile
from uuid import uuid4

from register_paths import absolute_path, master_path
from validate_register import validate_content


BACKUP_PREFIX = "OFFENE_ARBEITSAUFFORDERUNGEN_"
BACKUP_NAME = re.compile(rf"{BACKUP_PREFIX}\d{{8}}T\d{{12}}Z_[a-f0-9]{{32}}\.md")


def compute_sha256(path: str | Path) -> str:
    return sha256(Path(path).read_bytes()).hexdigest()


def _regular_file(path: Path) -> None:
    if not stat.S_ISREG(path.lstat().st_mode):
        raise ValueError(f"Expected a regular file, not a link or directory: {path}")


def _master(value: str | Path | None) -> Path:
    path = master_path(value)
    return path.parent.resolve(strict=True) / path.name


def _backup_directory(path: Path) -> Path:
    path = path.parent.resolve(strict=True) / path.name
    if path.is_symlink() or path.resolve() != path:
        raise ValueError(f"Backup directory cannot redirect to another path: {path}")
    if path.exists() and not path.is_dir():
        raise NotADirectoryError(path)
    return path


def _selected_backup_directory(target: Path, value: str | Path | None) -> Path:
    path = absolute_path(value, "Backup directory") if value is not None else target.parent / "backups"
    directory = _backup_directory(path)
    if directory in target.parents:
        raise ValueError("The register must be outside the backup directory.")
    return directory


def _write_exclusive(path: Path, data: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
    except BaseException:
        path.unlink(missing_ok=True)
        raise


def _manifest(backup: Path) -> Path:
    return backup.with_suffix(".md.json")


def _save_snapshot(directory: Path, target: Path, data: bytes) -> dict[str, str]:
    directory.mkdir(exist_ok=True, mode=0o700)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup = directory / f"{BACKUP_PREFIX}{timestamp}_{uuid4().hex}.md"
    digest = sha256(data).hexdigest()
    record = {
        "version": 1, "file": backup.name, "register": target.name,
        "size_bytes": len(data), "sha256": digest,
    }
    _write_exclusive(backup, data)
    try:
        _write_exclusive(_manifest(backup), json.dumps(record).encode("utf-8") + b"\n")
    except BaseException:
        backup.unlink(missing_ok=True)
        raise
    return {
        "status": "BACKUP_SUCCESS", "source": str(target), "backup": str(backup),
        "sha256": digest, "timestamp": timestamp,
    }


def backup_master(
    master_path: str | Path | None = None, backup_dir: str | Path | None = None,
) -> dict[str, str]:
    """Snapshot the current bytes, even if the register needs repair."""
    target = _master(master_path)
    _regular_file(target)
    return _save_snapshot(_selected_backup_directory(target, backup_dir), target, target.read_bytes())


def _read_snapshot(backup: Path) -> tuple[dict, bytes]:
    if not BACKUP_NAME.fullmatch(backup.name):
        raise ValueError(f"Unsupported backup name: {backup.name}")
    metadata = _manifest(backup)
    _regular_file(backup)
    try:
        _regular_file(metadata)
    except FileNotFoundError:
        raise ValueError(f"Backup manifest missing: {metadata.name}") from None
    record = json.loads(metadata.read_text(encoding="utf-8"))
    data = backup.read_bytes()
    if (
        not isinstance(record, dict) or type(record.get("version")) is not int
        or record["version"] != 1 or record.get("file") != backup.name
        or type(record.get("size_bytes")) is not int or record["size_bytes"] != len(data)
        or record.get("sha256") != sha256(data).hexdigest()
    ):
        raise ValueError(f"Backup does not match its manifest: {backup.name}")
    return record, data


@contextmanager
def _restore_lock(target: Path):
    lock = target.with_name(f".{target.name}.restore.lock")
    try:
        _write_exclusive(lock, b"Restore in progress\n")
    except FileExistsError:
        raise ValueError(f"Restore lock already exists: {lock}") from None
    try:
        yield
    finally:
        lock.unlink()


def restore_master(
    backup_file: str | Path, target_master: str | Path | None = None,
    *, backup_dir: str | Path | None = None,
) -> dict[str, str]:
    """Check the selected snapshot and save the target before replacing it."""
    target = _master(target_master)
    directory = _selected_backup_directory(target, backup_dir)
    selected = absolute_path(backup_file, "Backup file")
    if selected.parent.resolve() != directory:
        raise ValueError("The backup must be directly inside the selected backup directory.")

    source = directory / selected.name
    record, data = _read_snapshot(source)
    if record.get("register") != target.name:
        raise ValueError("Backup was created for a different register filename.")
    validation = validate_content(data.decode("utf-8-sig"), require_evidence=False)
    if validation["errors"]:
        raise ValueError("Invalid register in backup: " + "; ".join(validation["errors"]))

    with _restore_lock(target):
        previous = None
        if target.exists() or target.is_symlink():
            _regular_file(target)
            previous = target.read_bytes()

        fd, temporary_name = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
        temporary = Path(temporary_name)
        result = {
            "status": "RESTORE_SUCCESS", "restored_file": str(target),
            "source_backup": str(source), "sha256": record["sha256"],
        }
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            if previous is not None:
                saved = _save_snapshot(directory, target, previous)
                result["previous_backup"] = saved["backup"]
                _regular_file(target)
                if target.read_bytes() != previous:
                    raise ValueError("Register changed during restore. Retry with the latest version.")
            elif target.exists() or target.is_symlink():
                raise ValueError("Register appeared during restore. Retry with the latest version.")
            os.replace(temporary, target)
        finally:
            temporary.unlink(missing_ok=True)
    return result


def list_backups(backup_dir: str | Path | None = None) -> list[dict[str, str]]:
    if backup_dir is None:
        directory = _selected_backup_directory(_master(None), None)
    else:
        directory = _backup_directory(absolute_path(backup_dir, "Backup directory"))
    if not directory.exists():
        return []
    results = []
    for file in sorted(directory.glob(f"{BACKUP_PREFIX}*.md"), reverse=True):
        if file.is_symlink() or not file.is_file():
            continue
        entry = {
            "filename": file.name, "path": str(file),
            "size_bytes": str(file.stat().st_size), "sha256": compute_sha256(file),
            "integrity": "UNVERIFIED",
        }
        if _manifest(file).exists() or _manifest(file).is_symlink():
            try:
                record, _ = _read_snapshot(file)
                entry["sha256"] = record["sha256"]
                entry["integrity"] = "VERIFIED"
            except (OSError, ValueError):
                entry["integrity"] = "INVALID"
        results.append(entry)
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("backup", "list", "restore"), nargs="?", default="backup")
    parser.add_argument("backup_file", nargs="?")
    parser.add_argument("target", nargs="?")
    parser.add_argument("--register", help="Absolute path to the register.")
    parser.add_argument("--backup-dir", help="Absolute path to a trusted backup directory.")
    args = parser.parse_args()
    try:
        if args.command == "restore":
            if not args.backup_file or (args.target and args.register):
                parser.error("restore requires a backup file and accepts one target path")
            result = restore_master(args.backup_file, args.target or args.register, backup_dir=args.backup_dir)
        elif args.backup_file:
            parser.error("positional paths are only accepted by restore")
        elif args.command == "list":
            directory = args.backup_dir
            if args.register and directory is None:
                directory = _selected_backup_directory(_master(args.register), None)
            result = list_backups(directory)
        else:
            result = backup_master(args.register, args.backup_dir)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"{exc}\n")
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
