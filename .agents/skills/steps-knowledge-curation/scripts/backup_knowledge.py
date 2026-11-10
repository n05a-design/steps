"""Knowledge base backup, integrity verification, and recovery utility."""
from __future__ import annotations
import sys, os, shutil, hashlib, datetime
from pathlib import Path

DEFAULT_MASTER = os.path.expandvars(r"%LOCALAPPDATA%\StepsKnowledge\OFFENE_ARBEITSAUFFORDERUNGEN.md")
DEFAULT_BACKUP_DIR = os.path.expandvars(r"%LOCALAPPDATA%\StepsKnowledge\backups")

def compute_sha256(path: str | Path) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def backup_master(master_path: str = DEFAULT_MASTER, backup_dir: str = DEFAULT_BACKUP_DIR) -> dict[str, str]:
    """Create a timestamped and SHA-256 verified backup of the canonical master file."""
    src = Path(master_path)
    if not src.exists():
        raise FileNotFoundError(f"Master file not found: {master_path}")
    
    b_dir = Path(backup_dir)
    b_dir.mkdir(parents=True, exist_ok=True)
    
    src_hash = compute_sha256(src)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = b_dir / f"OFFENE_ARBEITSAUFFORDERUNGEN_{timestamp}.md"
    
    shutil.copy2(src, backup_file)
    dst_hash = compute_sha256(backup_file)
    
    if src_hash != dst_hash:
        backup_file.unlink(missing_ok=True)
        raise IOError("Backup integrity failure: SHA-256 mismatch")
        
    return {
        "status": "BACKUP_SUCCESS",
        "source": str(src),
        "backup": str(backup_file),
        "sha256": src_hash,
        "timestamp": timestamp
    }

def restore_master(backup_file: str, target_master: str = DEFAULT_MASTER) -> dict[str, str]:
    """Restore the canonical master file from a verified backup."""
    b_path = Path(backup_file)
    if not b_path.exists():
        raise FileNotFoundError(f"Backup file not found: {backup_file}")
        
    target = Path(target_master)
    target.parent.mkdir(parents=True, exist_ok=True)
    
    b_hash = compute_sha256(b_path)
    shutil.copy2(b_path, target)
    t_hash = compute_sha256(target)
    
    if b_hash != t_hash:
        raise IOError("Restore integrity failure: SHA-256 mismatch")
        
    return {
        "status": "RESTORE_SUCCESS",
        "restored_file": str(target),
        "source_backup": str(b_path),
        "sha256": t_hash
    }

def list_backups(backup_dir: str = DEFAULT_BACKUP_DIR) -> list[dict[str, str]]:
    """List all available backups with timestamps and SHA-256 hashes."""
    b_dir = Path(backup_dir)
    if not b_dir.exists():
        return []
        
    results = []
    for f in sorted(b_dir.glob("OFFENE_ARBEITSAUFFORDERUNGEN_*.md"), reverse=True):
        results.append({
            "filename": f.name,
            "path": str(f),
            "size_bytes": str(f.stat().st_size),
            "sha256": compute_sha256(f)
        })
    return results

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "restore":
        if len(sys.argv) < 3:
            print("Usage: python backup_knowledge.py restore <backup_file> [target]")
            sys.exit(1)
        tgt = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_MASTER
        res = restore_master(sys.argv[2], tgt)
        print(f"Restore result: {res}")
    elif len(sys.argv) > 1 and sys.argv[1] == "list":
        b_list = list_backups()
        print(f"Found {len(b_list)} backups:")
        for b in b_list:
            print(f"  {b['filename']} ({b['size_bytes']} bytes) - {b['sha256'][:16]}...")
    else:
        res = backup_master()
        print(f"Backup result: {res}")
