#!/usr/bin/env python3
"""Read-only A-F source coverage, historical crosswalk and original fenced examples.

Run on an extracted PRIVATE V4 package:
 python scripts/audit_traceability_v4.py --root <extracted-private-package-dir>
This checks *textual preservation only*, not music, rights, or product correctness.
"""
from pathlib import Path
import argparse,csv,hashlib,re
ORIG={'STEPS Project Export.md':297,'Projekt Overview.md':159,
'Glide Kontext für Fable(2).md':659,'Project Definition & Positioning.md':221,
'Forschungs- und Projektgrundlage.md':900,'Projektstatus- und Projektstartbericht.md':376}
EV='github_ready/docs/project/review/evidence/'

def sha(s):return hashlib.sha256(s.encode('utf-8')).hexdigest()
def fenced(s):
 out=[];active=None;acc=[]
 for line in s.splitlines():
  m=re.match(r'^( *)(`{3,4})([^`]*)$',line)
  if active is None:
   if m and len(m.group(1))<=4:active=(m.group(1),m.group(2));acc=[]
  elif re.match(r'^\s*'+re.escape(active[1])+r'\s*$',line):
   out.append('\n'.join(acc).strip());active=None;acc=[]
  else:acc.append(line[len(active[0]):] if line.startswith(active[0]) else line)
 if active:raise ValueError('Unclosed fence')
 return out

def run(root):
 src=root/'private_sources'
 originals={}
 for k,n in ORIG.items():
  lines=(src/k).read_text(encoding='utf-8-sig').splitlines()
  if len(lines)!=n:raise ValueError('Original line count mismatch '+k)
  originals[k]=lines
 with (root/(EV+'STEPS_V4_89_QUELLENABSCHNITTE.csv')).open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
 if len(rows)!=89:raise ValueError('Expected 89 source ranges')
 covered={k:set() for k in ORIG}
 for row in rows:
  k=row['Originaldatei'];lo=int(row['Zeile_von']);hi=int(row['Zeile_bis']);
  if k not in originals or lo<1 or hi>len(originals[k]) or lo>hi:raise ValueError('Out-of-bound range')
  seg='\n'.join(originals[k][lo-1:hi]);
  if sha(seg)!=row['Abschnitt_sha256']:raise ValueError('Changed source block '+k)
  covered[k].update(range(lo,hi+1))
 if any(len(covered[k])!=len(originals[k]) for k in ORIG):raise ValueError('Not fully covered')
 history=(root/(EV+'STEPS_V4_HISTORISCHE_POSITIONEN.csv'))
 with history.open(encoding='utf-8-sig',newline='') as f:hist=list(csv.DictReader(f))
 overview=(src/'Steps_Projekt_Overview_konsolidiert_2026-11-09.md').read_text(encoding='utf-8-sig').splitlines()
 expected={f'W-{i:02d}' for i in range(1,41)}|{f'G-{i:02d}' for i in range(1,35)}|{f'DEC-{i:03d}' for i in range(1,27)}
 if len(hist)!=100 or {r['id'] for r in hist}!=expected:raise ValueError('100 historical IDs mismatch')
 for row in hist:
  ln=int(row['originalzeile']);text=overview[ln-1]
  if sha(text)!=row['V4_Originalzeile_sha256']:raise ValueError('History text mismatch '+row['id'])
 blocks=[b for name in ORIG for b in fenced('\n'.join(originals[name]))]
 appendix=fenced((src/'Steps_Technischer_Anhang_und_Originalvorlagen_2026-11-09.md').read_text(encoding='utf-8-sig'))
 if len(blocks)!=39 or len(set(blocks))!=39 or len(appendix)!=39 or set(blocks)!=set(appendix):raise ValueError('39 source fences mismatch')
 print('TEXTUAL TRACEABILITY OK: 6 originals, 89 ranges, 2612 lines, 39 original fences, 100 historical anchors')
 print('LIMIT: no scientific, legal, repository-code or MIDI verification')

if __name__=='__main__':
 a=argparse.ArgumentParser(description=__doc__);a.add_argument('--root',type=Path,required=True)
 run(a.parse_args().root)
