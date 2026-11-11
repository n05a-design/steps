#!/usr/bin/env python3
"""STEPS repository audit and conservative, staged architecture migration.

Execute OUTSIDE the checked-out repository. --audit changes no repo contents.
--apply creates a new branch and moves only selected owned-looking project files;
rights clearance, link repair, and Git history rewrite are separate human gates.
"""
from __future__ import annotations
import argparse
import collections
import csv
import datetime as dt
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

EXPECTED_REPO = 'n05a-design/steps'
EXPECTED_HEAD = 'b42a990681ce5fd12c7756fb2ada962e01474521'
BASE = Path(__file__).resolve().parent
SCAFFOLD = BASE / 'scaffold'
DEFAULT_BRANCH = 'refactor/steps-architecture-preservation'

PREFIX_MOVES = (
    ('01_Projektkonsolidierung/01_Overview/', 'docs/project/overview/'),
    ('01_Projektkonsolidierung/02_Technischer_Anhang/', 'docs/project/technical-appendix/'),
    ('01_Projektkonsolidierung/03_Quellenabdeckung/', 'docs/project/provenance/'),
    ('01_Projektkonsolidierung/04_Originaldokumente/', 'docs/project/originals/'),
    ('00_Arbeitsvorbereitung/Steps_Deep_Research_Gesamtpaket/',
     'research/notes/deep-research/legacy/'),
    ('00_Arbeitsvorbereitung/Erster-Skill-Entwurf – music-harmony-coach/',
     'skills/music-harmony-coach/'),
)
FILE_MOVES = {
    '01_Projektkonsolidierung/README.md': 'docs/project/ARCHIVE_README.md',
    '01_Projektkonsolidierung/SHA256SUMS.txt':
         'docs/project/provenance/HISTORIC_SHA256SUMS.txt',
    '02_Bibliothek/README_STEPS_BIBLIOTHEK.md':
         'knowledge/legacy/STEPS_BIBLIOTHEK_README.md',
}

def git(repo: Path, *args: str, checked: bool = True, binary: bool = False):
    cmd = ['git', '-C', str(repo), *args]
    p = subprocess.run(cmd, capture_output=True, check=False)
    if checked and p.returncode:
        raise RuntimeError(f'Git error {p.returncode}: {cmd!r}\n{p.stderr.decode("utf-8", errors="replace")}')
    return p.stdout if binary else p.stdout.decode('utf-8', errors='replace').strip()

def tracked_files(repo: Path):
    data=git(repo, 'ls-files', '-z', binary=True)
    return sorted(p for p in data.decode('utf-8', errors='surrogateescape').split('\0') if p)

def proposed_target(rel: str) -> str | None:
    if rel in FILE_MOVES: return FILE_MOVES[rel]
    if rel.startswith('02_Bibliothek/create_steps_v6_7') and rel.endswith('.py') and '/' not in rel.split('02_Bibliothek/', 1)[1]:
        return 'tools/legacy/generators/' + rel.rsplit('/',1)[-1]
    for src,dst in PREFIX_MOVES:
        if rel.startswith(src): return dst+rel[len(src):]
    return None

def candidate_target(rel: str) -> str:
    """Non-executable suggestion for every *held* old path; no implicit rights grant."""
    if rel in ('README.md', 'LICENSE', '.gitignore'):
        return rel
    if rel.startswith('00_Arbeitsvorbereitung/Drums Progression/'):
        return 'research/production/drums/legacy/' + rel[len('00_Arbeitsvorbereitung/Drums Progression/'):]
    if rel.startswith('00_Arbeitsvorbereitung/Wettbewerb & Konkurrenz/'):
        return 'research/competitors/legacy/working_set/' + rel.split('Wettbewerb & Konkurrenz/',1)[1]
    if rel.startswith('00_Arbeitsvorbereitung/'):
        return 'private_sources/legacy/' + rel
    library='02_Bibliothek/STEPS_Bibliothek/STEPS_Bibliothek_V6_6_Ableton_Blog_Archiv_und_Tutorials/'
    if rel.startswith(library):
        return 'knowledge/legacy/v6_6/' + rel[len(library):]
    if rel.startswith('02_Bibliothek/'):
        return 'private_sources/legacy/' + rel
    if rel.startswith('03_Konkurrenz/'):
        return 'research/competitors/legacy/' + rel[len('03_Konkurrenz/'):]
    if rel.startswith('20_Grafik_Master/'):
        return 'design/references/legacy/' + rel[len('20_Grafik_Master/'):]
    return 'review_unclassified/' + rel

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def rights_gate(rel: str) -> str:
    low=rel.lower()
    if rel.startswith(('01_Projektkonsolidierung/',)):
        return 'project_document_check'
    if rel.startswith('00_Arbeitsvorbereitung/Erster-Skill-Entwurf'):
        return 'draft_skill_check'
    if rel.startswith('00_Arbeitsvorbereitung/Steps_Deep_Research_Gesamtpaket'):
        return 'research_provenance_check'
    if rel.startswith('20_Grafik_Master/'):
        return 'image_origin_review'
    if rel.startswith('03_Konkurrenz/') or '/Wettbewerb & Konkurrenz/' in rel:
        return 'third_party_competitor_review'
    if low.endswith(('.pdf','.epub','.mobi','.mp3','.wav','.zip','.amxd','.png','.jpg','.jpeg','.webp','.html','.download')) or '/_files/' in low:
        return 'rights_review_required'
    if rel.startswith(('02_Bibliothek/',)):
        return 'legacy_provenance_review'
    return 'unclassified_review'

def audit(repo: Path, out: Path) -> dict:
    out.mkdir(parents=True,exist_ok=True)
    files=tracked_files(repo)
    inventory=[]; digests=collections.defaultdict(list); skipped=[]
    for rel in files:
        p=repo/rel
        if not p.is_file():
            skipped.append(rel)
            continue
        st=p.stat()
        digest=sha256(p)
        move=proposed_target(rel)
        record={'original_path':rel,'proposed_path':move or '', 'review_candidate_path':candidate_target(rel) if not move else '', 'bytes':st.st_size,
                'sha256':digest,'rights_gate':rights_gate(rel),
                'action':'safe_text_move' if move else 'hold_review'}
        inventory.append(record)
        digests[digest].append(record)
    dupls=[g for g in digests.values() if len(g)>1]
    dupls.sort(key=lambda g:-(len(g)-1)*g[0]['bytes'])
    summary={
      'repository':EXPECTED_REPO,'head':git(repo,'rev-parse','HEAD'),
      'inventory_files':len(inventory),'skipped_missing':skipped,
      'logical_bytes':sum(r['bytes'] for r in inventory),
      'duplicate_groups':len(dupls),
      'extra_identical_paths':sum(len(g)-1 for g in dupls),
      'extra_logical_bytes':sum((len(g)-1)*g[0]['bytes'] for g in dupls),
      'planned_file_moves':sum(bool(r['proposed_path']) for r in inventory),
      'blocked_file_count':sum(not r['proposed_path'] for r in inventory),
      'timestamp_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    (out/'inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (out/'migration_plan.csv').open('w',newline='',encoding='utf-8-sig') as f:
        fieldnames=list(inventory[0]) if inventory else ['original_path','proposed_path','bytes','sha256','rights_gate','action']
        wr=csv.DictWriter(f,fieldnames=fieldnames,delimiter=';');wr.writeheader();wr.writerows(inventory)
    with (out/'exact_duplicates.csv').open('w',newline='',encoding='utf-8-sig') as f:
        wr=csv.writer(f,delimiter=';');wr.writerow(['SHA256','number_of_paths','file_size_bytes','original_path','other_identical_path'])
        for group in dupls:
            for entry in group[1:]:
                wr.writerow([group[0]['sha256'],len(group),group[0]['bytes'],group[0]['original_path'],entry['original_path']])
    return summary

def preflight(repo: Path, args, inventory: list):
    if not (repo/'.git').exists():
        raise RuntimeError('Directory does not contain .git; use repository root.')
    remote=git(repo,'remote','get-url','origin')
    expected=('github.com/'+EXPECTED_REPO).lower()
    if expected not in remote.lower() and ('github.com:'+EXPECTED_REPO).lower() not in remote.lower():
        raise RuntimeError(f'Unexpected origin remote: {remote!r}')
    actual_head=git(repo,'rev-parse','HEAD')
    if actual_head!=EXPECTED_HEAD and not args.allow_newer:
        raise RuntimeError(f'Expected {EXPECTED_HEAD}, got {actual_head}. Re-audit and use --allow-newer only after review.')
    if git(repo,'status','--porcelain','--untracked-files=all'):
        raise RuntimeError('Working tree not clean. Commit or back up your changes first.')
    current_branch=git(repo,'branch','--show-current')
    if current_branch!='main' and not args.allow_newer:
        raise RuntimeError('Expected a clean main branch. Switch to main before applying.')
    p=subprocess.run(['git','-C',str(repo),'show-ref','--verify','--quiet',f'refs/heads/{args.branch}'],capture_output=True)
    if p.returncode==0:
        raise RuntimeError(f'Target branch already exists: {args.branch}')
    # All destinations must be free, including scaffold paths (the root README is intentional exception).
    moves=[(r['original_path'],r['proposed_path'],r['sha256']) for r in inventory if r['proposed_path']]
    targets=[d for _,d,_ in moves]
    if len(targets)!=len(set(targets)):
        raise RuntimeError('Source to destination collisions in migration mapping.')
    for src,dst,_ in moves:
        if not (repo/src).is_file() or (repo/dst).exists():
            raise RuntimeError(f'Missing source or destination already exists: {src} => {dst}')
    for p in SCAFFOLD.rglob('*'):
        if p.is_file():
            rel=p.relative_to(SCAFFOLD).as_posix()
            if rel=='README.md':continue
            if (repo/rel).exists() or rel in targets:
                raise RuntimeError('Scaffold conflicts with existing file or planned move: '+rel)

def apply(repo:Path,args,output:Path):
    inventory=json.loads((output/'inventory.json').read_text(encoding='utf-8'))
    preflight(repo,args,inventory)
    orig_readme=(repo/'README.md').read_bytes() if (repo/'README.md').exists() else None
    git(repo,'switch','-c',args.branch)
    moved=[]
    try:
        for item in inventory:
            old,new=item['original_path'],item['proposed_path']
            if not new:continue
            dest=repo/new
            dest.parent.mkdir(parents=True,exist_ok=True)
            git(repo,'mv','--',old,new)
            if sha256(dest)!=item['sha256']:
                raise RuntimeError(f'Integrity mismatch after git mv: {old} => {new}')
            moved.append({'old':old,'new':new,'sha256':item['sha256']})
        backup=repo/'docs/handover/ROOT_README_BEFORE_2026-11-10.md'
        backup.parent.mkdir(parents=True,exist_ok=True)
        if orig_readme is not None: backup.write_bytes(orig_readme)
        for source in sorted(SCAFFOLD.rglob('*')):
            if source.is_file():
                relative=source.relative_to(SCAFFOLD)
                dest=repo/relative
                dest.parent.mkdir(parents=True,exist_ok=True)
                if dest.exists() and relative.as_posix()!='README.md':
                    raise RuntimeError('Unexpected scaffold collision: '+str(relative))
                shutil.copy2(source,dest)
        ig=repo/'.gitignore'
        append='''\n# STEPS: private, unlicensed and generated materials (untracked only)\n/private_sources/\n/knowledge/sources/raw/\n/research/sources/local/\n/data/local/\n/artifacts/\n'''
        old=ig.read_text(encoding='utf-8') if ig.exists() else ''
        if '# STEPS: private, unlicensed' not in old:
            ig.write_text(old.rstrip()+'\n'+append,encoding='utf-8')
        report={'base_sha':EXPECTED_HEAD,'applied_from_sha':git(repo,'rev-parse','HEAD'),
                'branch':args.branch,'file_moves':moved,'scaffold_files':sum(p.is_file() for p in SCAFFOLD.rglob('*')),
                'warning':'History unchanged, protected materials still tracked in historical commits; links must be checked.'}
        (output/'apply_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(f'Applied {len(moved)} controlled renames to branch {args.branch!r}.')
        print('Next: python tools/validation/check_structure.py')
        print('Then: git add -A; git diff --cached --stat; review; commit; push branch; open PR.')
        print('Note: Large binary sources, duplicates and Git history have NOT been removed.')
    except Exception:
        print('ATTENTION: partial work may remain on the new branch. Review git status; do not force-reset without preserving data.',file=sys.stderr)
        raise

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo',required=True,type=Path,help='Existing local STEPS checkout (not the extracted package)')
    mode=p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--audit',action='store_true',help='Read-only audit, reports written beside this script')
    mode.add_argument('--apply',action='store_true',help='Create refactor branch and apply conservative moves')
    p.add_argument('--allow-newer',action='store_true',help='Override strict HEAD/branch check after auditing changes')
    p.add_argument('--branch',default=DEFAULT_BRANCH)
    p.add_argument('--report-dir',type=Path,help='Outside-repository output directory; default: package/reports')
    args=p.parse_args()
    repo=args.repo.expanduser().resolve(strict=True)
    out=(args.report_dir or (BASE/'reports')).expanduser().resolve()
    if out==repo or repo in out.parents:
        raise SystemExit('Report directory must be OUTSIDE the repository to preserve clean-tree checks.')
    print(f'Repo: {repo}')
    summary=audit(repo,out)
    print('AUDIT:',json.dumps(summary,ensure_ascii=False,indent=2))
    print(f'Reports: {out}')
    if args.apply:
        apply(repo,args,out)
    else:
        print('Read-only audit completed; repository unchanged.')
if __name__=='__main__':
    try: main()
    except Exception as exc:
        print('ERROR:',str(exc),file=sys.stderr)
        sys.exit(1)
