"""Version-separated descriptive genre/tempo metadata, never audio or groove approval."""
import argparse
from collections import Counter
from hashlib import sha256
import io
import json
import math
from pathlib import Path
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'docs/audit/fable-5.2/KORPUS_GIANTSTEPS_TEMPO_2026-11-14.json'
COMMIT='d51ab2422e76abacfaa86616a57054bc222ec9fd'
ARCHIVE_SHA='05b908c799be0e616e0632d7019228fc0e424c106c1873c822fa12957d7f0a87'
HOUSE={'house','deep-house','progressive-house','tech-house','electro-house'}


def tempo_band(value):
    if not math.isfinite(value) or value<0:raise ValueError('Invalid tempo')
    if value==0:return 'MISSING'
    return 'IN_120_128' if 120<=value<=128 else 'OUTSIDE_120_128'


def summarize(records,genres):
    rows=[r for r in records if r['genre'] in genres]
    return {version:dict(sorted(Counter(r['bands'][version] for r in rows).items())) for version in ('v1','v2')}


def measure(archive):
    payload=Path(archive).read_bytes()
    if sha256(payload).hexdigest()!=ARCHIVE_SHA:raise ValueError('Unexpected repository archive identity')
    z=zipfile.ZipFile(io.BytesIO(payload));prefix='giantsteps-tempo-dataset-'+COMMIT+'/'
    genres=sorted(n for n in z.namelist() if n.startswith(prefix+'annotations/genre/') and n.endswith('.genre'))
    if len(genres)!=664:raise ValueError('Unexpected genre annotation count')
    records=[]
    for member in genres:
        ident=Path(member).name.removesuffix('.genre');raw=z.read(member);genre=raw.decode().strip()
        values={};digests={'genre':sha256(raw).hexdigest()}
        for version,path in [('v1','annotations/tempo/'),('v2','annotations_v2/tempo/')]:
            b=z.read(prefix+path+ident+'.bpm');values[version]=tempo_band(float(b.decode().strip()));digests[version]=sha256(b).hexdigest()
        records.append({'recording_id':ident,'genre':genre,'bands':values,'annotation_sha256':digests})
    return {'schema_version':1,'repository_commit':COMMIT,'archive_sha256':ARCHIVE_SHA,'records':records,
            'genre_counts':dict(sorted(Counter(r['genre'] for r in records).items())),
            'exact_house':summarize(records,{'house'}),'house_label_family':summarize(records,HOUSE),
            'house_label_family_definition':sorted(HOUSE),
            'method':'Join genre and tempo metadata by the same recording filename; v1 and v2 stay separate. Fixed inclusive120–128 BPM band, zero is missing. No automatic octave-tempo normalization.',
            'source_url':'https://github.com/GiantSteps/giantsteps-tempo-dataset/tree/'+COMMIT,
            'attribution':'Knees et al. ISMIR2015; tempo v2 Schreiber and Müller ISMIR2018. Genre data described as Beatport metadata by project README.',
            'rights':'No general repository licence located in top-level tree; raw archive, scripts, annotations and audio are not republished. Own descriptive classifications, identities and hashes only; no audio downloaded.',
            'limits':'Correction-oriented sample of previews; no representative House population, kick/hat transcription, harmonic sequence or human half/double-tempo validation.',
            'human_approval':'AUSSTEHEND','historical_assertion_closed':False,'joint_drum_harmony_verified':False}


def validate(d):
    if (d['schema_version']!=1 or d['repository_commit']!=COMMIT or d['archive_sha256']!=ARCHIVE_SHA
            or len(d['records'])!=664 or len({r['recording_id'] for r in d['records']})!=664
            or d['house_label_family_definition']!=sorted(HOUSE) or d['human_approval']!='AUSSTEHEND'
            or d['historical_assertion_closed'] is not False or d['joint_drum_harmony_verified'] is not False):raise ValueError('Invalid partial tempo scope or premature approval')
    for r in d['records']:
        if set(r['bands'])!={'v1','v2'} or any(v not in {'MISSING','IN_120_128','OUTSIDE_120_128'} for v in r['bands'].values()):raise ValueError('Mixed or invalid tempo versions')
    if (d['genre_counts']!=dict(sorted(Counter(r['genre'] for r in d['records']).items()))
            or d['exact_house']!=summarize(d['records'],{'house'}) or d['house_label_family']!=summarize(d['records'],HOUSE)):
        raise ValueError('Genre/tempo denominator mismatch')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--giantsteps-zip',type=Path);p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args()
    d=measure(a.giantsteps_zip) if a.giantsteps_zip else json.loads(OUTPUT.read_text(encoding='utf8'));validate(d)
    if a.write:OUTPUT.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    if a.check and d!=json.loads(OUTPUT.read_text(encoding='utf8')):raise SystemExit('Tempo observation stale')
    print(json.dumps({'records':len(d['records']),'exact_house':d['exact_house'],'house_label_family':d['house_label_family'],'human_approval':'AUSSTEHEND'}))


if __name__=='__main__':main()
