#!/usr/bin/env python3
"""Validate STEPS V6.0 library structural integrity (not musicology). Usage: python 15_TOOLS_SKRIPTE/STEPS_V6_0__audit_library.py [library_root]"""
from pathlib import Path
import sys,json,hashlib,csv
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent
ix=root/'00_NAVIGATION'/'STEPS_V6_0__THEMENREGISTER__DATEN__V6_0.json'
data=json.loads(ix.read_text(encoding='utf-8'))
assert len(data['major_domains'])>=25
ids=[t['id'] for t in data['terms']]
assert len(ids)==len(set(ids))
assert all((root/d['folder']).is_dir() for d in data['major_domains'])
for p in root.rglob('*.json'): json.loads(p.read_text(encoding='utf-8'))
for p in root.rglob('*.csv'):
  with p.open(encoding='utf-8-sig',newline='') as f: next(csv.reader(f),None)
base=json.loads((root/'00_NAVIGATION'/'STEPS_V6_0__SOURCE_BASE_HASHES__MANIFEST__V6_0.json').read_text(encoding='utf-8'))['files']
for rel,digest in base.items(): assert hashlib.sha256((root/rel).read_bytes()).hexdigest()==digest,rel
print(json.dumps({'status':'pass','base_files_verified':len(base),'topic_terms':len(ids),'domain_count':len(data['major_domains']),'note':'structural only'}))
