#!/usr/bin/env python3
"""Read-only MIDI/ZIP metadata audit. No audio, no music claims, no file copies.

Usage: python STEPS_TOOLS__audit_midi_library__WERKZEUG__V5_3.py /path/to/source --output /private/report.json
Requires mido. ZIP entries are read in memory with conservative size limits.
"""
import argparse, io, hashlib, json, zipfile
from collections import defaultdict
from pathlib import Path
import mido

MAX_UNPACKED=80_000_000

def digest(data): return hashlib.sha256(data).hexdigest()

def audit_bytes(data,virtual_path):
    result={'path':virtual_path,'sha256':digest(data),'bytes':len(data),'format':None,'ticks_per_beat':None,'tempo_events':[], 'time_signatures':[],'tracks':[],'error':None}
    try:
        mid=mido.MidiFile(file=io.BytesIO(data))
        result['format']=mid.type; result['ticks_per_beat']=mid.ticks_per_beat
        for track_idx,track in enumerate(mid.tracks):
            t=0; notes=defaultdict(list); onsets=0; offs=0; unclosed=[];cc={}
            for msg in track:
                t+=msg.time
                if msg.type=='set_tempo':result['tempo_events'].append({'track':track_idx,'tick':t,'tempo_us':msg.tempo})
                if msg.type=='time_signature':result['time_signatures'].append({'track':track_idx,'tick':t,'numerator':msg.numerator,'denominator':msg.denominator})
                if msg.type=='control_change':cc[str(msg.control)]=cc.get(str(msg.control),0)+1
                if msg.type=='note_on' and msg.velocity>0:
                    notes[(msg.channel,msg.note)].append(t);onsets+=1
                if msg.type=='note_off' or (msg.type=='note_on' and msg.velocity==0):
                    offs+=1
                    if notes[(msg.channel,msg.note)]:notes[(msg.channel,msg.note)].pop(0)
                    else:unclosed.append({'unmatched_off':(msg.channel,msg.note,t)})
            for (ch,n),starts in notes.items():
                unclosed.extend({'unclosed_note':(ch,n,start)} for start in starts)
            result['tracks'].append({'index':track_idx,'duration_ticks':t,'notes_on':onsets,'notes_off':offs,'controller_counts':cc,'note_pair_issues':unclosed})
    except Exception as exc:result['error']=str(exc)
    return result

def audit_tree(root):
    entries=[];errors=[]
    for p in sorted(root.rglob('*')):
        if not p.is_file():continue
        rel=p.relative_to(root).as_posix()
        if p.suffix.lower() in ['.mid','.midi']:
            if p.stat().st_size>MAX_UNPACKED:errors.append({'file':rel,'reason':'size_limit'});continue
            entries.append(audit_bytes(p.read_bytes(),rel))
        elif p.suffix.lower()=='.zip':
            try:
                with zipfile.ZipFile(p) as z:
                    for info in z.infolist():
                        if info.is_dir() or not info.filename.lower().endswith(('.mid','.midi')):continue
                        if info.file_size>MAX_UNPACKED:errors.append({'file':rel+'!'+info.filename,'reason':'size_limit'});continue
                        entries.append(audit_bytes(z.read(info),rel+'!'+info.filename))
            except Exception as exc: errors.append({'file':rel,'reason':str(exc)})
    hashes=defaultdict(list)
    for item in entries:hashes[item['sha256']].append(item['path'])
    return {'status':'metadata_only_no_music_style_verification','scanned_root':str(root),'midi_files':len(entries),'duplicate_groups':[v for v in hashes.values() if len(v)>1], 'entries':entries,'errors':errors}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('--output',required=True);args=ap.parse_args()
    root=Path(args.root).expanduser().resolve();dest=Path(args.output).expanduser().resolve()
    if not root.is_dir():raise SystemExit('root not found')
    if dest.is_relative_to(root):raise SystemExit('Output must be outside scanned root to preserve source')
    result=audit_tree(root);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('MIDI metadata scanned:',result['midi_files'],' errors:',len(result['errors']))
