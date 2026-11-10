#!/usr/bin/env python3
"""Create a review-only publication overlay from safe documentation files.

No repository, GitHub, user-data or existing output files are modified.
Rewrites package-only relative links to exact GitHub source references or plain
non-links. Run source/rights review before publication.
"""
from __future__ import annotations
import shutil
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'publish_overlay'
INCLUDED={'docs','prompts','templates','skills','design','research','decisions','knowledge'}
MANIFESTS={
 'REQUIREMENTS_TRACE_28.csv', 'INVESTIGATION_COVERAGE_33_V2.csv',
 'GLIDE_94_MODULE_REUSE_AUDIT_V2.csv','GLIDE_25_PACKAGES_AUDIT_V2.csv',
 'DEEP_RESEARCH_REFS.csv','ORIGINAL_CONFLICTS_40.csv',
 'ORIGINAL_GAPS_34.csv','EXTERNAL_PRIMARY_REFERENCES.csv',
 'GLIDE_SHELL_ANCHORS_V2.csv','GLIDE_IMPORT_SIDE_EFFECTS_V2.csv'
}
HEAD='75329fef46878a5ac816cef3690e612a9e8fe52c'
REWRITE_LINKS={
 '../../source_archive/Steps_Projekt_Overview_konsolidiert_2026-11-09.md':
 f'https://github.com/n05a-design/steps/blob/{HEAD}/docs/project/overview/Steps_Projekt_Overview_konsolidiert_2026-11-09.md',
}

def revise(text):
    # Keep source paths as explanatory text, never fabricate a non-existing GitHub link.
    for old,new in REWRITE_LINKS.items():text=text.replace(f']({old})',f']({new})')
    text=text.replace('](../../archive/v1_docs/)', ' (historische Dokumente: nur im vollständigen Audit-ZIP)')
    text=text.replace('](../../source_archive/)', ' (Original-Uploads: nur im vollständigen Audit-ZIP)')
    return text

def build():
 if OUT.exists():raise SystemExit('publish_overlay exists; inspect it, then manually remove before rebuilding')
 count=0
 for top in sorted(INCLUDED):
  for src in sorted((ROOT/top).rglob('*')):
   if not src.is_file() or src.is_symlink() or src.suffix.lower() not in {'.md','.csv','.json','.yaml'}:continue
   rel=src.relative_to(ROOT)
   dest=OUT/rel;dest.parent.mkdir(parents=True,exist_ok=True)
   if src.suffix.lower()=='.md':dest.write_text(revise(src.read_text(encoding='utf-8')),encoding='utf-8')
   else:shutil.copyfile(src,dest)
   count+=1
 for name in sorted(MANIFESTS):
  src=ROOT/'manifests'/name
  if not src.is_file():raise SystemExit(f'Missing manifest {name}')
  dest=OUT/'manifests'/name;dest.parent.mkdir(parents=True,exist_ok=True)
  shutil.copyfile(src,dest);count+=1
 # verify all internal links against overlay; links into pre-existing repo may
 # be intentionally unresolved, but this overlay should need none.
 broken=[]
 for p in OUT.rglob('*.md'):
  text=p.read_text(encoding='utf-8')
  for link in re.findall(r'\]\(([^)]+)\)',text):
   if link.startswith(('http:','https:','mailto:','#')):continue
   target=link.split('#',1)[0].replace('%20',' ')
   if target and not (p.parent/target).exists():broken.append((str(p.relative_to(OUT)),link))
 if broken:
  shutil.rmtree(OUT)
  raise SystemExit(f'Broken staged links {broken[:10]!r}')
 for forbidden in ('source_archive','archive'):
  if (OUT/forbidden).exists():raise SystemExit('Private/legacy archive copied unexpectedly')
 print(f'PUBLIC OVERLAY CANDIDATE: {count} text/manifests, zero broken internal links, zero uploaded originals')
 return count

if __name__=='__main__':build()
