"""Preferred asynchronous Swing chart/drum components, not performed-harmony proof."""
import argparse
from collections import Counter
import csv
from hashlib import sha256
import io
import json
import math
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.steps.theory import parse_spelling
from scripts.audit_rwc_joint import bounded_count,windows
from scripts.audit_billboard_components import targets

OUTPUT=ROOT/'docs/audit/fable-5.2/KORPUS_JAZZSAMBA_SWING_2026-11-14.json'
CATALOG_SHA='92fe14ee3fc41bc8a6f8d6a91b127e51bc99f4a325b654e0a466773735dd89f5'
SELECTION_SHA='459a5c78713ca1924c9f604fa5547aac85b5e77c9849e94045c8b73540691a20'
EXTENSIONS=('has_6','has_9','has_11','has_13','has_add9')
ALTERATIONS=('alt_b5','alt_sharp5','alt_b9','alt_sharp9','alt_sharp11','alt_b11','is_sus2','is_sus4')


def chart_shape(row,mode):
    if mode not in ('exact','triad_projection'):raise ValueError('Explicit chart scope required')
    if row['is_no_chord']!='False' or row['triad'] not in ('maj','min'):return None
    if any(row[k]!='False' for k in ALTERATIONS):return None
    root=int(parse_spelling(row['root'],'INT').pitch_class)
    if mode=='triad_projection':return root,row['triad']
    if row['is_slash']!='False' or any(row[k]!='False' for k in EXTENSIONS):return None
    quality={('maj','none'):'maj',('min','none'):'min',('min','min'):'min7',('maj','dom'):'7',('maj','maj'):'maj7'}.get((row['triad'],row['seventh']))
    return (root,quality) if quality else None


def chart_segments(rows,mode):
    runs=[];run=[];previous_end=None;excluded=0
    def flush():
        nonlocal run
        if run:runs.append(run);run=[]
    for index,row in enumerate(rows):
        start,end=float(row['start_time']),float(row['end_time'])
        if math.isfinite(start) and start>=0 and start==end and index==len(rows)-1:
            flush();excluded+=1;continue
        if not math.isfinite(start) or not math.isfinite(end) or not 0<=start<end:raise ValueError('Invalid timed chart interval')
        if previous_end is not None:
            if start<previous_end-1e-6:raise ValueError('Overlapping chart intervals')
            if start-previous_end>0.02:flush()
        previous_end=end;chord=chart_shape(row,mode)
        if chord is None:flush();excluded+=1;continue
        if run and run[-1]['chord']==chord:run[-1]['end']=end
        else:run.append({'chord':chord,'start':start,'end':end})
    flush();return runs,excluded


def drum_times(raw):
    import mido
    elapsed=0.;out=[];channels=Counter();notes=Counter()
    for msg in mido.MidiFile(file=io.BytesIO(raw)):
        elapsed+=msg.time
        if msg.type=='note_on' and msg.velocity>0:
            out.append(elapsed);channels[str(msg.channel)]+=1;notes[str(msg.note)]+=1
    return out,dict(channels),dict(notes)


def check_bar_grid(chords,bars):
    grid={int(b['bar']):(float(b['start_time']),float(b['end_time'])) for b in bars}
    if not grid or len(grid)!=len(bars) or any(not math.isfinite(a) or not math.isfinite(b) or not 0<=a<b for a,b in grid.values()):
        raise ValueError('Invalid bar-grid identity or timing')
    maximum=0.;last=max(grid)
    for row in chords:
        for side in ('start','end'):
            idx=int(row[side+'_bar']);fraction=float(row[side+'_fraction']);actual=float(row[side+'_time'])
            if not math.isfinite(actual) or not math.isfinite(fraction) or not 0<=fraction<=1:raise ValueError('Invalid chart coordinate')
            if idx in grid:
                a,b=grid[idx];expected=a+fraction*(b-a)
            elif idx==last+1 and fraction==0:expected=grid[last][1]
            else:raise ValueError('Chart coordinate outside supplied bar grid')
            error=abs(actual-expected)
            if error>0.002:raise ValueError('Chart seconds differ from bar-and-fraction axis')
            maximum=max(maximum,error)
    return maximum


def measure(manifest):
    data=json.loads(Path(manifest).read_text(encoding='utf8'));records=[]
    if data['source_record']!='10.5281/zenodo.22943963' or data['catalog_sha256']!=CATALOG_SHA or len(data['records'])!=18:
        raise ValueError('Incomplete or mismatched Swing selection')
    for source in data['records']:
        if source['genre']!='swing' or source['is_swung'] is not True or source['synchronous'] is not False or source['time_signature']!='4/4':
            raise ValueError('Selection must stay preferred asynchronous4/4 Swing')
        blobs={};members={}
        for kind,info in source['members'].items():
            expected='async/songs/'+source['basename']+'/preferred/'+('drums.mid' if kind=='drums' else 'annotations/'+kind+'.csv')
            if info['member']!=expected:raise ValueError('Derived, alternate or mismatched source lane')
            raw=Path(info['local_file']).read_bytes()
            if sha256(raw).hexdigest()!=info['sha256']:raise ValueError('Local source hash changed')
            blobs[kind]=raw;members[kind]={k:v for k,v in info.items() if k!='local_file'}
        chords=list(csv.DictReader(io.StringIO(blobs['chords'].decode('utf8'))));bars=list(csv.DictReader(io.StringIO(blobs['bars'].decode('utf8'))))
        grid_error=check_bar_grid(chords,bars);events,channels,notes=drum_times(blobs['drums']);results={}
        for mode in ('exact','triad_projection'):
            runs,excluded=chart_segments(chords,mode);intervals=windows(runs,targets()['PROG-003'],mode)
            hits=[{'start_seconds':a,'end_seconds':b,'drum_note_onsets':bounded_count(events,a,b)} for a,b in intervals]
            results[mode]={'excluded_chart_rows':excluded,'windows':hits}
        terminal_zero=sum(float(x['start_time'])==float(x['end_time']) for x in chords[-1:])
        records.append({'song_id':source['song_id'],'basename':source['basename'],'source_members':members,
                        'genre':'swing','is_swung':True,'synchronous':False,'take':'preferred','time_signature':'4/4',
                        'drum_note_onsets':len(events),'drum_channels':channels,'note_number_histogram':notes,
                        'excluded_terminal_zero_duration_rows':terminal_zero,'bar_grid_max_error_seconds':grid_error,'patterns':results})
    summary={mode:{'chart_windows':sum(len(r['patterns'][mode]['windows']) for r in records),
                   'windows_with_drum_onsets':sum(w['drum_note_onsets']>0 for r in records for w in r['patterns'][mode]['windows']),
                   'songs_with_both':sum(any(w['drum_note_onsets']>0 for w in r['patterns'][mode]['windows']) for r in records)} for mode in ('exact','triad_projection')}
    return {'schema_version':1,'source_record':'10.5281/zenodo.22943963','catalog_sha256':CATALOG_SHA,
            'selected_songs':18,'source_archive_published_md5':data['archive_published_md5'],'source_archive_full_md5_verified':False,
            'retrieval':'Bounded public HTTP206 ranges, ZIP-member CRC checked, individual SHA256 recorded; no audio or10.8GB archive downloaded.',
            'chart_origin':'TIMED_LEAD_SHEET_NOT_PERFORMED_HARMONY_TRANSCRIPTION','drum_origin':'PREFERRED_ASYNC_DRUM_MIDI_PER_DATASET_NOT_AMT',
            'exact_ride_pedal_pattern_verified':False,'human_approval':'AUSSTEHEND','historical_assertion_closed':False,
            'rights':'Catalog permission notice covers contributed original recordings, MIDI and annotations; underlying standard composition copyrights are separately listed. Raw files remain local; no universal rights/CSS release inferred.',
            'attribution':'Phillip Long and contributors, JazzSAMBA v1.0.0, Zenodo10.5281/zenodo.22943963 and arXiv2609.34931v1.',
            'limits':'Chosen gig-book repertoire and18 preferred asynchronous takes are not a representative Swing population. Chart matching plus onsets proves neither performed ii–V–I nor ride/pedal identity or exact style. Native note numbers are not automatically GM instrument roles.',
            'summary':summary,'records':records}


def validate(d):
    if (d['schema_version']!=1 or d['source_record']!='10.5281/zenodo.22943963' or d['catalog_sha256']!=CATALOG_SHA
            or d['selected_songs']!=18 or len(d['records'])!=18 or len({r['song_id'] for r in d['records']})!=18
            or sha256(json.dumps(sorted(r['song_id'] for r in d['records'])).encode()).hexdigest()!=SELECTION_SHA
            or d['chart_origin']!='TIMED_LEAD_SHEET_NOT_PERFORMED_HARMONY_TRANSCRIPTION'
            or d['drum_origin']!='PREFERRED_ASYNC_DRUM_MIDI_PER_DATASET_NOT_AMT'
            or d['source_archive_full_md5_verified'] is not False or d['exact_ride_pedal_pattern_verified'] is not False
            or d['human_approval']!='AUSSTEHEND' or d['historical_assertion_closed'] is not False):raise ValueError('Invalid source distinction or premature acceptance')
    for r in d['records']:
        if r['genre']!='swing' or r['is_swung'] is not True or r['synchronous'] is not False or r['take']!='preferred' or r['time_signature']!='4/4':raise ValueError('Source selection changed')
        for k,v in r['source_members'].items():
            expected='async/songs/'+r['basename']+'/preferred/'+('drums.mid' if k=='drums' else 'annotations/'+k+'.csv')
            if v['member']!=expected or len(v['sha256'])!=64:raise ValueError('Invalid original source lane')
        if set(r['source_members'])!={'bars','chords','drums'}:raise ValueError('Missing source lane')
        if not 0<=r['bar_grid_max_error_seconds']<=.002 or r['excluded_terminal_zero_duration_rows'] not in (0,1):raise ValueError('Invalid coordinate countercheck')
    for mode in ('exact','triad_projection'):
        expected={'chart_windows':sum(len(r['patterns'][mode]['windows']) for r in d['records']),
                  'windows_with_drum_onsets':sum(w['drum_note_onsets']>0 for r in d['records'] for w in r['patterns'][mode]['windows']),
                  'songs_with_both':sum(any(w['drum_note_onsets']>0 for w in r['patterns'][mode]['windows']) for r in d['records'])}
        if d['summary'][mode]!=expected:raise ValueError('Chart/drum denominator mismatch')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--selection-manifest',type=Path);p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args()
    d=measure(a.selection_manifest) if a.selection_manifest else json.loads(OUTPUT.read_text(encoding='utf8'));validate(d)
    if a.write:OUTPUT.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    if a.check and d!=json.loads(OUTPUT.read_text(encoding='utf8')):raise SystemExit('Jazz component observation stale')
    print(json.dumps({'selected_songs':18,'summary':d['summary'],'exact_pattern_verified':False,'performed_harmony_verified':False}))


if __name__=='__main__':main()
