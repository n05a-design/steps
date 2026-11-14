"""Strict, partial Billboard chord-shape observations, never joint groove evidence."""
import argparse
from collections import Counter
from hashlib import sha256
import io
import json
import math
from pathlib import Path
import re
import sys
import tarfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.steps.progression import get_progression
from src.steps.theory import parse_spelling

OUTPUT=ROOT/'docs/audit/fable-5.2/KORPUS_BILLBOARD_KOMPONENTEN_2026-11-14.json'
ARCHIVE_SHA='a22e32bf24c8a18859ce18427c6501a7a72520185cddd6d882ceb3c61d02ec75'
TARGETS=('PROG-001','PROG-002','PROG-003','PROG-007','PROG-017','PROG-023','PROG-025','PROG-028')
QUALITY={'':'maj','m':'min','m7':'min7','7':'7','maj7':'maj7','m9':'min9','9':'9','maj9':'maj9'}
PROJECTION={'maj':'maj','min':'min','7':'maj','maj7':'maj','min7':'min','9':'maj','maj9':'maj','min9':'min'}


def symbol(value):
    m=re.fullmatch(r'([A-G](?:b|#)?):(maj|min|7|maj7|min7|9|maj9|min9)',value)
    return (int(parse_spelling(m[1],'INT').pitch_class),m[2]) if m else None


def chord_segments(text):
    """Accept only one exact chord per complete printed bar; anything else breaks continuity."""
    runs=[];run=[];counts=Counter();last_time=-math.inf
    def flush():
        nonlocal run
        if run:runs.append(run);run=[]
    for line_no,line in enumerate(text.splitlines(),1):
        if not line.strip():continue
        if line.startswith('#'):
            if run:flush();counts['metadata_boundaries']+=1
            continue
        try:time=float(line.split()[0])
        except ValueError:raise ValueError('Phrase timestamp missing') from None
        if not math.isfinite(time) or time<0 or time<last_time:raise ValueError('Phrase times must be finite and ordered')
        last_time=time
        parts=line.split('|')
        if len(parts)<3 or re.search(r'\bZ\s*,',parts[0]):
            flush();counts['non_bar_boundaries']+=1;continue
        for bar_index,bar in enumerate(parts[1:-1],1):
            chord=symbol(bar.strip())
            if chord is None:
                flush();counts['excluded_bars']+=1
            else:
                counts['accepted_bars']+=1
                if not run or run[-1]['chord']!=chord:
                    run.append({'chord':chord,'line':line_no,'bar_index':bar_index})
    flush()
    return runs,dict(counts)


def signature(chords,mode='exact'):
    if mode not in ('exact','triad_projection') or not chords:raise ValueError('Explicit nonempty chord-shape scope required')
    first=chords[0][0]
    return [((root-first)%12,quality if mode=='exact' else PROJECTION[quality]) for root,quality in chords]


def matches(runs,target,mode):
    wanted=signature(target,mode);found=[];windows=0
    for run in runs:
        for i in range(len(run)-len(target)+1):
            window=run[i:i+len(target)];windows+=1
            if signature([x['chord'] for x in window],mode)==wanted:
                found.append({'line':window[0]['line'],'bar_index':window[0]['bar_index'],
                              'relative_roots':[x[0] for x in wanted],'qualities':[x[1] for x in wanted]})
    return found,windows


def targets():
    return {ident:[(int(c.root.pitch_class),QUALITY[c.quality]) for c in get_progression(ident).chord_definitions] for ident in TARGETS}


def measure(archive):
    payload=Path(archive).read_bytes()
    if sha256(payload).hexdigest()!=ARCHIVE_SHA:raise ValueError('Unexpected Billboard delivery identity')
    patterns=targets();rows=[]
    with tarfile.open(fileobj=io.BytesIO(payload),mode='r:gz') as a:
        files=sorted([m for m in a.getmembers() if m.isfile()],key=lambda m:m.name)
        if len(files)!=890 or any(not re.fullmatch(r'McGill-Billboard/\d{4}/salami_chords.txt',m.name) for m in files):
            raise ValueError('Unexpected annotation collection')
        for member in files:
            raw=a.extractfile(member).read();text=raw.decode('utf8');runs,coverage=chord_segments(text)
            metadata={m[1]:m[2].strip() for line in text.splitlines() if (m:=re.match(r'^# (title|artist):\s*(.*)',line))}
            if not all(metadata.get(k) for k in ('title','artist')):raise ValueError('Missing song identity')
            song_key=' | '.join(' '.join(metadata[k].casefold().split()) for k in ('artist','title'))
            found={}
            for ident,target in patterns.items():
                found[ident]={}
                for mode in ('exact','triad_projection'):
                    hits,windows=matches(runs,target,mode)
                    found[ident][mode]={'hits':hits,'eligible_windows':windows}
            rows.append({'slot_id':member.name.split('/')[1],'member':member.name,'sha256':sha256(raw).hexdigest(),
                         'song_key':song_key,'coverage':coverage,'patterns':found})
    summary={}
    for ident in TARGETS:
        summary[ident]={}
        for mode in ('exact','triad_projection'):
            present=[r for r in rows if r['patterns'][ident][mode]['hits']]
            summary[ident][mode]={'matched_slots':len(present),'matched_artist_title_keys':len({r['song_key'] for r in present}),
                                  'matched_windows':sum(len(r['patterns'][ident][mode]['hits']) for r in rows),
                                  'eligible_windows':sum(r['patterns'][ident][mode]['eligible_windows'] for r in rows)}
    return {'schema_version':1,'archive_sha256':ARCHIVE_SHA,'archive_bytes':len(payload),'annotation_slots':len(rows),
            'artist_title_keys':len({r['song_key'] for r in rows}),'targets':{k:[list(x) for x in v] for k,v in patterns.items()},
            'method':'One supported chord per complete bar, adjacent exact duplicates collapsed; unsupported bars, metadata changes and non-bar lines break continuity; no tonal-function, duration or cadence inference.',
            'source_url':'https://ddmal.ca/research/The_McGill_Billboard_Project_(Chord_Analysis_Dataset)/',
            'archive_url':'https://www.dropbox.com/s/2lvny9ves8kns4o/billboard-2.0-salami_chords.tar.gz?dl=1',
            'attribution':'McGill Billboard2.0 annotations, DDMAL, CC0; Burgoyne, Wild and Fujinaga (ISMIR2011); parser-scope reference de Haas and Burgoyne (2012), UU-CS-2012-018.',
            'limits':'Chart slots and artist-title keys are separate units; keys are not independently verified recording identities. Excluded bars are unknown, not negative examples. No audio, drum events, subgenre or statistical population approval.',
            'joint_drum_harmony_verified':False,'human_approval':'AUSSTEHEND','historical_assertion_closed':False,
            'summary':summary,'records':rows}


def validate(d):
    if (d['schema_version']!=1 or d['archive_sha256']!=ARCHIVE_SHA or d['annotation_slots']!=890
            or len(d['records'])!=890 or set(d['summary'])!=set(TARGETS) or d['targets']!={k:[list(x) for x in v] for k,v in targets().items()}
            or d['human_approval']!='AUSSTEHEND' or d['historical_assertion_closed'] is not False
            or d['joint_drum_harmony_verified'] is not False):raise ValueError('Invalid partial observation or premature approval')
    rows=d['records']
    if len({r['slot_id'] for r in rows})!=890 or d['artist_title_keys']!=len({r['song_key'] for r in rows}):raise ValueError('Denominator/duplicate identity error')
    for ident in TARGETS:
        for mode in ('exact','triad_projection'):
            present=[r for r in rows if r['patterns'][ident][mode]['hits']]
            expected={'matched_slots':len(present),'matched_artist_title_keys':len({r['song_key'] for r in present}),
                      'matched_windows':sum(len(r['patterns'][ident][mode]['hits']) for r in rows),
                      'eligible_windows':sum(r['patterns'][ident][mode]['eligible_windows'] for r in rows)}
            if d['summary'][ident][mode]!=expected:raise ValueError('Partial corpus totals differ')
            for r in rows:
                x=r['patterns'][ident][mode]
                if len(x['hits'])>x['eligible_windows'] or len(r['sha256'])!=64:raise ValueError('Invalid observed window')


def render(d):
    head={k:v for k,v in d.items() if k!='records'}
    return (json.dumps(head,ensure_ascii=False,indent=2)[:-2]+',\n  "records": [\n    '
            +',\n    '.join(json.dumps(r,ensure_ascii=False,separators=(',',':')) for r in d['records'])+'\n  ]\n}\n')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--billboard-archive',type=Path);p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args()
    observed=json.loads(OUTPUT.read_text(encoding='utf8')) if not a.billboard_archive else measure(a.billboard_archive)
    validate(observed)
    if a.write:OUTPUT.write_text(render(observed),encoding='utf8')
    if a.check and observed!=json.loads(OUTPUT.read_text(encoding='utf8')):raise SystemExit('Billboard observation stale')
    print(json.dumps({'slots':observed['annotation_slots'],'artist_title_keys':observed['artist_title_keys'],'summary':observed['summary'],'joint_drum_harmony_verified':False}))


if __name__=='__main__':main()
