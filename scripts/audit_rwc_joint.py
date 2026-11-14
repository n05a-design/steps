"""Same-ID/time-axis RWC component observations, never exact drum-pattern approval."""
import argparse
from bisect import bisect_left
from collections import Counter
import csv
from hashlib import sha256
import io
import json
import math
from pathlib import Path
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.audit_billboard_components import targets,signature,symbol

COMMIT='0a1a6c31dbe73a7f5d44f7caef8cd0999402a4c2'
ARCHIVE_SHA='27bc4da9c8730b143b2dacb4495c92bb45a00e0cf7d7b385d51203fc6055d534'
OUTPUT=ROOT/'docs/audit/fable-5.2/KORPUS_RWC_GEMEINSAME_ZEITACHSE_2026-11-14.json'


def segments(rows):
    runs=[];run=[];counts=Counter();previous_end=None
    def flush():
        nonlocal run
        if run:runs.append(run);run=[]
    for row in rows:
        start,end=float(row['t_start']),float(row['t_end'])
        if not math.isfinite(start) or not math.isfinite(end) or not 0<=start<end:
            raise ValueError('Invalid chord interval')
        if previous_end is not None:
            if start<previous_end-1e-6:raise ValueError('Overlapping chord intervals')
            if start-previous_end>0.02:flush();counts['gap_boundaries']+=1
        previous_end=end;chord=symbol(row['chord'])
        if chord is None:flush();counts['excluded_segments']+=1;continue
        counts['accepted_segments']+=1
        if run and run[-1]['chord']==chord:run[-1]['end']=end
        else:run.append({'chord':chord,'start':start,'end':end})
    flush();return runs,dict(counts)


def windows(runs,target,mode):
    wanted=signature(target,mode);out=[]
    for run in runs:
        for i in range(len(run)-len(target)+1):
            window=run[i:i+len(target)]
            if signature([x['chord'] for x in window],mode)==wanted:
                out.append((window[0]['start'],window[-1]['end']))
    return out


def bounded_count(times,start,end):
    """Half-open intervals prevent a boundary onset counting in both neighbors."""
    if not 0<=start<end:raise ValueError('Invalid observation interval')
    return bisect_left(times,end)-bisect_left(times,start)


def four_four_bars(beats):
    out=[]
    for i in range(len(beats)-4):
        group=beats[i:i+5]
        if [int(b['beat']) for b in group]!=[1,2,3,4,1]:continue
        times=[float(b['t']) for b in group]
        if all(b>a for a,b in zip(times,times[1:])):out.append(times)
    return out


def role_subset(bar,note_times,tolerance=0.1):
    """Declared note classes and subsets only; GM source mapping is unverified."""
    if len(bar)!=5 or any(b<=a for a,b in zip(bar,bar[1:])) or not 0<=tolerance<0.5:
        raise ValueError('Explicit complete 4/4 grid and bounded tolerance required')
    def near(notes,t,width):
        return any(bounded_count(note_times.get(n,[]),max(0,t-tolerance*width),t+tolerance*width+1e-9)>0 for n in notes)
    widths=[b-a for a,b in zip(bar,bar[1:])]
    kick=all(near((35,36),bar[i],widths[i]) for i in (0,2))
    snare=all(near((38,40),bar[i],widths[i]) for i in (1,3))
    hat=all(near((42,),bar[i]+part*widths[i],widths[i]) for i in range(4) for part in (0,0.5))
    return {'kick_snare_subset':kick and snare,'closed_hat_eighth_subset':hat,'combined_subset':kick and snare and hat}


def midi_events(raw):
    import mido
    m=mido.MidiFile(file=io.BytesIO(raw))
    if m.type not in (0,1) or m.ticks_per_beat<=0:raise ValueError('Metrical SMF required')
    seconds=0.;tempo=500000;percussion=[];note_times={}
    for msg in mido.merge_tracks(m.tracks):
        seconds+=mido.tick2second(msg.time,m.ticks_per_beat,tempo)
        if msg.type=='set_tempo':tempo=msg.tempo
        if msg.type=='note_on' and msg.velocity>0 and msg.channel==9:
            percussion.append(seconds);note_times.setdefault(msg.note,[]).append(seconds)
    return percussion,seconds,note_times


def measure(archive):
    payload=Path(archive).read_bytes()
    if sha256(payload).hexdigest()!=ARCHIVE_SHA:raise ValueError('Unexpected RWC delivery')
    z=zipfile.ZipFile(io.BytesIO(payload));prefix='rwc-annotations-'+COMMIT+'/'
    metadata=list(csv.DictReader(io.StringIO(z.read(prefix+'metadata.csv').decode('utf-8-sig')),delimiter=';'))
    selected=[r for r in metadata if r['CollID']=='P'];patterns=targets();records=[]
    if len(selected)!=100 or len({r['RWCID'] for r in selected})!=100:raise ValueError('RWC-P selection changed')
    for row in selected:
        ident=row['RWCID'];base='01_annotations_preprocessed/'
        paths={'midi':base+'MIDI_aligned/RWC-P/'+ident+'.mid',
               'chords':base+'chords/RWC-P/'+ident+'.csv','beats':base+'beats/RWC-P/'+ident+'.csv'}
        blobs={k:z.read(prefix+path) for k,path in paths.items()}
        chords=list(csv.DictReader(io.StringIO(blobs['chords'].decode()),delimiter=';'))
        beats=list(csv.DictReader(io.StringIO(blobs['beats'].decode()),delimiter=';'))
        beat_times=[float(b['t']) for b in beats]
        if any(not math.isfinite(t) or t<0 for t in beat_times) or any(b<=a for a,b in zip(beat_times,beat_times[1:])):
            raise ValueError('Unordered/invalid beat times')
        runs,coverage=segments(chords);events,midi_end,note_times=midi_events(blobs['midi']);counts={}
        bars=four_four_bars(beats);bar_roles=[(bar,role_subset(bar,note_times)) for bar in bars]
        for ident_pattern,target in patterns.items():
            counts[ident_pattern]={}
            for mode in ('exact','triad_projection'):
                intervals=windows(runs,target,mode)
                observations=[]
                for a,b in intervals:
                    eligible=[roles for bar,roles in bar_roles if bar[0]>=a and bar[-1]<=b]
                    observations.append({'start_seconds':a,'end_seconds':b,
                                         'channel9_onsets':bounded_count(events,a,b),'beats':bounded_count(beat_times,a,b),
                                         'complete_4_4_bars':len(eligible),
                                         'noteclass_subset_bars':{key:sum(v[key] for v in eligible) for key in ('kick_snare_subset','closed_hat_eighth_subset','combined_subset')}})
                counts[ident_pattern][mode]=observations
        records.append({'recording_id':ident,'genre_main':row['GenreMain'],'genre_sub':row['GenreSub'],
                        'drum_metadata':row['DrumInformation'],'member_sha256':{k:sha256(b).hexdigest() for k,b in blobs.items()},
                        'same_id_join':True,'coverage':coverage,'channel9_onsets':len(events),
                        'all_complete_4_4_bars':len(bars),'all_noteclass_subset_bars':{key:sum(v[key] for _,v in bar_roles) for key in ('kick_snare_subset','closed_hat_eighth_subset','combined_subset')},
                        'midi_end_seconds':round(midi_end,6),'last_beat_seconds':beat_times[-1],
                        'audio_duration_metadata_seconds':float(row['duration']),'patterns':counts})
    summary={ident:{mode:{'harmonic_windows':sum(len(r['patterns'][ident][mode]) for r in records),
                           'windows_with_channel9':sum(x['channel9_onsets']>0 for r in records for x in r['patterns'][ident][mode]),
                           'records_with_both':sum(any(x['channel9_onsets']>0 for x in r['patterns'][ident][mode]) for r in records),
                           'records_with_combined_noteclass_subset':sum(any(x['noteclass_subset_bars']['combined_subset']>0 for x in r['patterns'][ident][mode]) for r in records)}
                   for mode in ('exact','triad_projection')} for ident in patterns}
    return {'schema_version':1,'repository_commit':COMMIT,'archive_sha256':ARCHIVE_SHA,'selected_records':100,
            'time_unit':'SECONDS','interval_convention':'[start,end)',
            'source_url':'https://github.com/rwc-music/rwc-annotations/tree/'+COMMIT,
            'attribution':'RWC2.0 annotations: Goto et al.2002/2006; Balke et al.2026, doi:10.5334/tismir.326. Chord annotations traced by source README to Cho and Bello.',
            'rights':'CC BY-NC4.0 per pinned repository LICENSE. Raw MIDI, audio, annotation sequences and third-party code not redistributed. Own audit statistics and hashes only; no commercial or CSS rights approval.',
            'method':'Same RWCID across MIDI/chord/beat members; MIDI tempo-map converted to seconds. Exact supported chord-quality shape or separate triad projection; continuity gaps and unknown symbols break matching.',
            'limits':'Channel9 onset presence is not PAT identity or authenticated instrument mapping. Aligned symbolic annotations are not a new listening test. Overlapping windows are not independent pieces; commissioned Popular/J-pop/Pop selection does not represent the requested subgenres.',
            'exact_drum_pattern_verified':False,'human_approval':'AUSSTEHEND','historical_assertion_closed':False,
            'noteclass_mapping_scope':'GM1_ASSUMPTION_NOT_VERIFIED_FOR_RWC_SOURCE',
            'subset_scope':'Notes35/36 at beats1/3,38/40 at2/4,42 at eighths within annotated complete4/4 bars; ±0.1 local quarter. Extra notes allowed; PAT001 syncopation, tempo, dynamics and exact pattern are not checked.',
            'summary':summary,'records':records}


def validate(d):
    if (d['schema_version']!=1 or d['repository_commit']!=COMMIT or d['archive_sha256']!=ARCHIVE_SHA
            or d['selected_records']!=100 or len(d['records'])!=100 or {r['recording_id'] for r in d['records']}!={f'RWC_P{i:03}' for i in range(1,101)}
            or d['time_unit']!='SECONDS' or d['interval_convention']!='[start,end)'
            or d['human_approval']!='AUSSTEHEND' or d['historical_assertion_closed'] is not False
            or d['exact_drum_pattern_verified'] is not False or set(d['summary'])!=set(targets())
            or d['noteclass_mapping_scope']!='GM1_ASSUMPTION_NOT_VERIFIED_FOR_RWC_SOURCE'):
        raise ValueError('Invalid joint-component scope or premature approval')
    for r in d['records']:
        if r['same_id_join'] is not True or r['genre_main']!='Popular' or set(r['member_sha256'])!={'midi','beats','chords'}:
            raise ValueError('Invalid same-ID source chain')
        subsets=r['all_noteclass_subset_bars']
        if (r['all_complete_4_4_bars']<0 or any(not 0<=n<=r['all_complete_4_4_bars'] for n in subsets.values())
                or subsets['combined_subset']>min(subsets['kick_snare_subset'],subsets['closed_hat_eighth_subset'])):
            raise ValueError('Invalid complete-bar denominator')
        for pattern in targets():
            for mode in ('exact','triad_projection'):
                for x in r['patterns'][pattern][mode]:
                    if (not 0<=x['start_seconds']<x['end_seconds'] or x['channel9_onsets']<0 or x['beats']<0
                            or any(not 0<=n<=x['complete_4_4_bars'] for n in x['noteclass_subset_bars'].values())
                            or x['noteclass_subset_bars']['combined_subset']>min(x['noteclass_subset_bars']['kick_snare_subset'],x['noteclass_subset_bars']['closed_hat_eighth_subset'])):
                        raise ValueError('Invalid observation interval/count')
    for ident in targets():
        for mode in ('exact','triad_projection'):
            expected={'harmonic_windows':sum(len(r['patterns'][ident][mode]) for r in d['records']),
                      'windows_with_channel9':sum(x['channel9_onsets']>0 for r in d['records'] for x in r['patterns'][ident][mode]),
                      'records_with_both':sum(any(x['channel9_onsets']>0 for x in r['patterns'][ident][mode]) for r in d['records']),
                      'records_with_combined_noteclass_subset':sum(any(x['noteclass_subset_bars']['combined_subset']>0 for x in r['patterns'][ident][mode]) for r in d['records'])}
            if d['summary'][ident][mode]!=expected:raise ValueError('Joint-component denominator mismatch')
    proof=json.loads((ROOT/'docs/audit/fable-5.2/KORPUS_RWC_GEGENPRUEFUNG_2026-11-14.json').read_text(encoding='utf8'))
    if (proof['source_archive_sha256']!=ARCHIVE_SHA or proof['human_approval']!='AUSSTEHEND'
            or proof['audio_alignment_independently_verified'] is not False or proof['exact_drum_pattern_verified'] is not False
            or proof['all_complete_4_4_bars']!=sum(r['all_complete_4_4_bars'] for r in d['records'])
            or proof['all_noteclass_subset_bars']!={k:sum(r['all_noteclass_subset_bars'][k] for r in d['records']) for k in ('kick_snare_subset','closed_hat_eighth_subset','combined_subset')}):
        raise ValueError('Countercheck scope or totals differ')


def render(d):
    head={k:v for k,v in d.items() if k!='records'}
    return json.dumps(head,ensure_ascii=False,indent=2)[:-2]+',\n  "records": [\n    '+',\n    '.join(json.dumps(r,ensure_ascii=False,separators=(',',':')) for r in d['records'])+'\n  ]\n}\n'


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--rwc-archive',type=Path);p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args()
    d=measure(a.rwc_archive) if a.rwc_archive else json.loads(OUTPUT.read_text(encoding='utf8'));validate(d)
    if a.write:OUTPUT.write_text(render(d),encoding='utf8')
    if a.check and d!=json.loads(OUTPUT.read_text(encoding='utf8')):raise SystemExit('RWC observations stale')
    print(json.dumps({'records':100,'summary':d['summary'],'exact_drum_pattern_verified':False}))


if __name__=='__main__':main()
