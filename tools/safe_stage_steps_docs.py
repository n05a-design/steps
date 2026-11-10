#!/usr/bin/env python3
"""Dry-run-first Steps documentation staging (no commits, no data deletion)."""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "publish_overlay"  # reviewed candidate, never raw ZIP contents
# Only originally generated documentation: never transfer user-uploaded code or archives.
INCLUDED_TOP = {"docs", "prompts", "templates", "skills", "design", "research", "decisions", "knowledge", "manifests"}
EXCLUDED = {"skills/music-harmony-coach"}  # unchanged original skill

def run_git(repo, *args):
    p=subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(f"git {' '.join(args)}: {p.stderr.strip()}")
    return p.stdout.strip()

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo",required=True,help="Existing local Steps checkout")
    ap.add_argument("--apply",action="store_true",help="Copy only missing files; never overwrite")
    opt=ap.parse_args()
    if not SOURCE.is_dir():
        raise SystemExit("Missing publish_overlay; run tools/build_public_overlay.py first. No raw archive is eligible.")
    repo=Path(opt.repo).expanduser().resolve()
    if not repo.is_dir() or not (repo/".git").exists():
        raise SystemExit("Expected an existing local Git working tree with .git directory.")
    origin=run_git(repo,"remote","get-url","origin")
    if "github.com/n05a-design/steps" not in origin.replace(":","/"):
        raise SystemExit(f"Unexpected Git origin: {origin}")
    branch=run_git(repo,"branch","--show-current")
    sha=run_git(repo,"rev-parse","HEAD")
    if not branch or branch in {"main","master"}:
        raise SystemExit("Refusing work on detached HEAD or main/master. Create a feature branch first.")
    if opt.apply and run_git(repo,"status","--porcelain"):
        raise SystemExit("Working tree is not clean; refusing apply.")
    srcfiles=[]
    for top in sorted(INCLUDED_TOP):
        subtree=SOURCE/top
        if not subtree.exists(): continue
        for f in sorted(subtree.rglob("*")):
            if f.is_file() and f.suffix.lower() in {".md", ".csv", ".yaml", ".json"}:
                rel=f.relative_to(SOURCE)
                if any(rel.as_posix().startswith(prefix) for prefix in EXCLUDED): continue
                srcfiles.append((f,rel))
    missing=[];same=[];conflicts=[]
    for f,rel in srcfiles:
        target=repo/rel
        if target.is_symlink() or any(parent.is_symlink() for parent in list(target.parents) if parent!=repo and repo in parent.parents):
            conflicts.append((rel,"symlink"));continue
        if target.exists():
            (same if target.is_file() and digest(f)==digest(target) else conflicts).append((rel,"exists"))
        else: missing.append((f,rel))
    print(f"repo={repo}\norigin={origin}\nbranch={branch}\nhead={sha}\nmissing={len(missing)} same={len(same)} collisions={len(conflicts)} apply={opt.apply}")
    if conflicts:
        print("Existing paths left unchanged:")
        for rel,_ in conflicts: print("  SKIP",rel.as_posix())
    for f,rel in missing: print("  NEW",rel.as_posix(),digest(f))
    if opt.apply:
        for f,rel in missing:
            target=repo/rel
            target.parent.mkdir(parents=True,exist_ok=True)
            # Exclusive creation; no TOCTOU overwrite even in a parallel session.
            with target.open('xb') as dst, f.open('rb') as src:
                shutil.copyfileobj(src,dst)
        print("Staged files in working tree only. Review git status/diff; no git add/commit/push occurred.")
    else: print("DRY RUN only. Review paths, then rerun with --apply on the same clean feature branch.")

if __name__=='__main__':
    main()
