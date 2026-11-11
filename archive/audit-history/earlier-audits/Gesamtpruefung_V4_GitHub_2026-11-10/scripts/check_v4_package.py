#!/usr/bin/env python3
"""Read-only audit of a V4 ZIP. Verifies internal consistency, not authenticity.

Stdlib-only; does not extract, execute, alter Git, or install any files.
Authenticity requires comparing the ZIP to a trusted, separately delivered digest.
"""
import argparse
import hashlib
import io
from pathlib import PurePosixPath
import zipfile

MANIFEST='MANIFEST_SHA256SUMS.txt'
REQUIRED={'INTEGRATION_UND_QA.md','github_ready/docs/project/review/STEPS_KRITISCHE_GESAMTPRUEFUNG_V4.md',
 'github_ready/docs/project/review/evidence/STEPS_V4_89_QUELLENABSCHNITTE.csv',
 'github_ready/docs/project/review/evidence/STEPS_V4_HISTORISCHE_POSITIONEN.csv',
 'github_ready/docs/project/review/evidence/STEPS_V4_NEUE_BEFUNDE.csv',
 'github_ready/docs/project/review/evidence/STEPS_V4_PRUEFPROTOKOLL.json'}

def sha(b):return hashlib.sha256(b).hexdigest()
def verify(path):
 with zipfile.ZipFile(path) as z:
  members=z.namelist()
  if len(members)!=len(set(members)):
   raise ValueError('Duplicate ZIP entries')
  for name in members:
   p=PurePosixPath(name)
   if p.is_absolute() or '..' in p.parts or '\\' in name or not name or name.startswith('/') or name.endswith('/'):
    raise ValueError('Unsafe/non-file ZIP path: '+name)
   inf=z.getinfo(name)
   if (inf.external_attr >> 16) & 0o170000 == 0o120000:
    raise ValueError('Symlink ZIP entry: '+name)
  if MANIFEST not in members:
   raise ValueError('Missing manifest')
  records={}
  for line in z.read(MANIFEST).decode('utf-8').splitlines():
   h,sep,n=line.partition('  ')
   if not sep or len(h)!=64 or any(x not in '0123456789abcdef' for x in h) or n in records:
    raise ValueError('Invalid manifest row')
   records[n]=h
  if set(members)-{MANIFEST}!=set(records):
   raise ValueError('Manifest names mismatch')
  for name,h in records.items():
   if sha(z.read(name))!=h:
    raise ValueError('Wrong digest '+name)
  if not REQUIRED.issubset(records):
   raise ValueError('Required V4 files missing')
  if z.testzip() is not None:
   raise ValueError('ZIP CRC failure')
  print('INTERNAL OK:',len(records),'manifested members in',path)
  print('LIMIT: Not a source signature or legal/content verification')
  return len(records)

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('archive')
 args=ap.parse_args();verify(args.archive)
