"""Render NEW audit exercises for human review; never original transcriptions."""
import argparse
from hashlib import sha256
import importlib.util
import json
from math import isfinite
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.render_audit_listening_examples import SAMPLE_RATE,add_tone,write_wave
from src.steps.theory import midi_to_frequency,parse_spelling
from src.steps.progression import get_progression


def examples():
    plan=json.loads((ROOT/'knowledge/relations/GRAPH_AUDIT_PLAN.json').read_text(encoding='utf-8'))
    probes={p['id']:p for p in plan['probes']};result={}
    for ident in ['II_V_I_SHELL_ARRANGEMENT','BACKDOOR_DROP2_ARRANGEMENT','MINOR_CYCLE_HAND_LAYERS','CIRCLE_SOUL_HAND_LAYERS']:
        data=probes[ident]['input']['data'];chords=get_progression(data['progression']).chord_definitions;events=[]
        for bar,(chord,rh) in enumerate(zip(chords,data['rh'])):
            left=data.get('lh',[None]*len(chords))[bar]
            lh=[48+int(chord.root.pitch_class)] if left is None else [parse_spelling(n,'INT').midi_number for n in left]
            for channel,notes in [(0,lh),(1,[parse_spelling(n,'INT').midi_number for n in rh])]:
                events += [[bar*1920,1680,n,channel] for n in notes]
        result[ident]={'probe_ids':[ident],'ticks':1920*len(chords),'events':events}
    data=probes['P07_COMPLETE_ARPEGGIO']['input']['data'];events=[]
    for bar,notes in enumerate(data['rh']):
        events.append([bar*1920,1680,parse_spelling(data['lh'][bar],'INT').midi_number,0])
        events += [[bar*1920+i*240,200,parse_spelling(n,'INT').midi_number,1] for i,n in enumerate(notes)]
    result['P07_COMPLETE_ARPEGGIO']={'probe_ids':['P07_COMPLETE_ARPEGGIO'],'ticks':7680,'events':events}
    for name,target in [('ORACLE_GLOBAL_MIN',[62,65,67,71]),('ORACLE_DROP2_MIN',[59,65,67,74])]:
        result[name]={'probe_ids':['DROP2_ORACLE_FROM_CLOSE'],'ticks':3840,
                      'events':[[bar*1920,1680,n,1] for bar,notes in enumerate([[62,65,69,72],target]) for n in notes]}
    for item in result.values():
        for start,duration,note,channel in item['events']:
            if not 0<=start<start+duration<=item['ticks'] or not 0<=note<=127 or channel not in (0,1):
                raise ValueError('Invalid review exercise')
    return result


def render(output,bpm=100,with_midi=False):
    if not isfinite(bpm) or bpm<=0:raise ValueError('Positive finite quarter-note tempo required')
    if with_midi:
        if importlib.util.find_spec('mido') is None:raise ValueError('Optional audit-only Mido is not installed')
        import mido
    output=Path(output);cases=examples()
    paths=[output/(name+ext) for name in cases for ext in (['.wav','.mid'] if with_midi else ['.wav'])]+[output/'manifest.json',output/'source-plan.json']
    if any(p.exists() or p.is_symlink() for p in paths):raise FileExistsError('Existing review material is never overwritten')
    output.mkdir(parents=True,exist_ok=True);manifest=[]
    for name,item in cases.items():
        unit=60/bpm/480;duration=item['ticks']*unit;samples=[0.0]*round(SAMPLE_RATE*duration)
        for onset,length,note,channel in item['events']:
            add_tone(samples,onset*unit,length*unit,midi_to_frequency(note),0.055,1.3)
        peak=max(map(abs,samples));path=output/(name+'.wav');write_wave(path,samples)
        record={'id':name,'probe_ids':item['probe_ids'],'bpm_quarter':bpm,'ppq':480,
                'ticks':item['ticks'],'events':item['events'],'seconds':duration,'peak':peak,
                'wav_sha256':sha256(path.read_bytes()).hexdigest(),'human_listen_play_approval':'AUSSTEHEND',
                'historical_transcription':False,'synthesis':'sinusoidal pitch control; no acoustic piano or style simulation'}
        if with_midi:
            song=mido.MidiFile(type=0,ticks_per_beat=480);track=mido.MidiTrack();song.tracks.append(track)
            track.append(mido.MetaMessage('set_tempo',tempo=mido.bpm2tempo(bpm),time=0))
            ordered=[]
            for onset,length,note,channel in item['events']:
                ordered.extend([(onset,1,note,channel),(onset+length,0,note,channel)])
            previous=0
            for tick,on,note,channel in sorted(ordered):
                track.append(mido.Message('note_on' if on else 'note_off',note=note,velocity=70 if on else 0,channel=channel,time=tick-previous));previous=tick
            track.append(mido.MetaMessage('end_of_track',time=item['ticks']-previous));midi_path=output/(name+'.mid');song.save(midi_path)
            record['midi_sha256']=sha256(midi_path.read_bytes()).hexdigest()
        manifest.append(record)
    data={'schema_version':1,'source_plan_lf_sha256':sha256((ROOT/'knowledge/relations/GRAPH_AUDIT_PLAN.json').read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
          'source_plan_snapshot':'source-plan.json','human_approvals':0,'historical_transcriptions':0,'examples':manifest}
    with (output/'source-plan.json').open('xb') as target:
        target.write((ROOT/'knowledge/relations/GRAPH_AUDIT_PLAN.json').read_bytes())
    (output/'manifest.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return data


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('output_dir',type=Path)
    parser.add_argument('--bpm',type=float,default=100);parser.add_argument('--midi',action='store_true');args=parser.parse_args()
    report=render(args.output_dir,args.bpm,args.midi)
    print(json.dumps({'new_exercises':len(report['examples']),'human_approvals':0,'historical_transcriptions':0}))
