"""Source-scoped MIDI/notation and context counterchecks, never human approval."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from math import lcm,log2
import re
import struct
from xml.etree import ElementTree

from scripts.audit_conflict_revisions import source_bytes
from src.steps.theory import parse_spelling
from src.steps.progression import resolve_roman_degree,get_progression


def integer(value,low,high):
    if type(value)is not int or not low<=value<=high:raise ValueError('Integer out of declared range')
    return value


def xml_midi_index(xml):
    root=ElementTree.fromstring(xml)
    channels=root.findall('midi-channel');notes=root.findall('midi-unpitched')
    if root.tag!='midi-instrument' or len(channels)!=1 or len(notes)!=1:
        raise ValueError('Exactly one explicit channel and unpitched number required')
    channel=integer(int(channels[0].text),1,16)-1;note=integer(int(notes[0].text),1,128)-1
    return {'wire_channel':channel,'note_number':note,'note_on_status':0x90+channel}


def vlq(value):
    value=integer(value,0,0x0fffffff);result=[value&127];value>>=7
    while value:result.insert(0,(value&127)|128);value>>=7
    return bytes(result)


def control_smf(ppq,note,wire_channel):
    """Tiny audit control only; no STEPS product exporter is asserted."""
    ppq=integer(ppq,1,32767);note=integer(note,0,127);channel=integer(wire_channel,0,15)
    track=(b'\x00\xff\x51\x03\x07\xa1\x20'+bytes([0,0x90+channel,note,70])
           +vlq(ppq)+bytes([0x80+channel,note,0])+b'\x00\xff\x2f\x00')
    return b'MThd'+struct.pack('>IHHH',6,0,1,ppq)+b'MTrk'+struct.pack('>I',len(track))+track


def catalog_row(source,ident):
    text=source_bytes(source).decode('utf-8')
    rows=[line for line in text.splitlines() if line.startswith('| `'+ident+'` |')]
    if len(rows)!=1:raise ValueError('Missing or ambiguous versioned catalog row')
    return rows[0]


def calculate(spec):
    operation,data=spec['input']['operation'],spec['input']['data']
    if operation=='octave_reference':
        return {'ratio':data['upper']/data['lower'],'cents':round(1200*log2(data['upper']/data['lower'])),
                'interval_is_tuning_system':False}
    if operation=='spelling_without_staff':
        n=parse_spelling(data['note'],'INT')
        return {'step':n.step,'alter':n.alteration,'pitch_class':int(n.pitch_class),'staff_required_by_parser':False}
    if operation=='contextual_degree':
        out=[]
        for note,scale in zip(data['notes'],data['scales']):
            n=parse_spelling(note,'INT');ss=[parse_spelling(s,'INT') for s in scale]
            matches=[i+1 for i,s in enumerate(ss) if (n.step,n.alteration)==(s.step,s.alteration)]
            if len(matches)!=1:raise ValueError('Written degree not uniquely in declared scale')
            out.append(matches[0])
        return out
    if operation=='primary_triads':
        return [resolve_roman_degree(x,data['key'],convention='INT').symbol for x in data['degrees']]
    if operation=='smf_control':
        blob=control_smf(data['ppq'],data['note'],data['wire_channel'])
        header=struct.unpack('>IHHH',blob[4:14])
        return {'format':header[1],'tracks':header[2],'division':header[3],
                'metrical_ppq':not bool(header[3]&0x8000),'track_length_correct':struct.unpack('>I',blob[18:22])[0]==len(blob)-22,
                'product_exporter_proven':False}
    if operation=='paired_swing':
        pair=integer(data['pair_ticks'],1,32767)
        if not 0<data['percent']<100:raise ValueError('Two positive subdivisions required')
        return {'zero_based_moving_index':1,'onsets':[0,round(pair*data['percent']/100)],'pair_end':pair}
    if operation=='xml_midi_index':return xml_midi_index(data['xml'])
    if operation=='gm_profile':
        channel=integer(data['human_channel'],1,16)
        role=('PERCUSSION' if channel==10 else 'MELODIC') if data['profile']=='GM1' else 'NOT_ASSERTED'
        return {'wire_channel':channel-1,'role':role,'gm1_note_span_count':len(range(35,82)) if data['profile']=='GM1' else None}
    if operation=='drums_without_keyboard':
        events=data['events']
        if not events or any(x['instrument'] not in {'kick','snare','hat'} or not 0<=x['tick']<1920 for x in events):
            raise ValueError('Explicit drum-only bar required')
        return {'drum_events':len(events),'keyboard_events':0,'event_grid_valid':True,'genre_norm_proven':False}
    if operation=='ukg_catalog_swing':
        row=catalog_row(data['source'],'PAT-020');percent=int(re.search(r'(\d+)% MPC-Swing',row)[1])
        return {'bpm':int(re.search(r'(\d+) BPM',row)[1]),'percent':percent,
                'second_sixteenth_tick':round(240*percent/100),'genre_norm_proven':False}
    if operation=='domain_namespaces':
        old=source_bytes(data['historical_source']).decode('utf-8')
        import csv
        modern=list(csv.DictReader(source_bytes(data['later_source']).decode('utf-8').splitlines()))
        old_label=re.search(r'^### M03[^\n]+',old,re.M)[0]
        label=next(r['domain_name'] for r in modern if r['domain_id']=='M03')
        return {'historical_mentions_intervals':'Intervalle' in old_label,
                'later_mentions_modes':'Modi' in label,'same_label':old_label.split('–',1)[-1].strip()==label,
                'readiness_is_expert_approval':False}
    if operation=='scale_triads':
        triads=[]
        for scale in data['scales']:
            pcs=[int(parse_spelling(n,'INT').pitch_class) for n in scale]
            if len(pcs)!=7 or len(set(pcs))!=7:raise ValueError('Seven distinct scale degrees required')
            triads += [tuple(sorted({pcs[i],pcs[(i+2)%7],pcs[(i+4)%7]})) for i in range(7)]
        return {'instances':len(triads),'all_three_tones':all(len(t)==3 for t in triads),'all_instances_unique':len(set(triads))==len(triads)}
    if operation=='bossa_catalog_grid':
        row=catalog_row(data['source'],'PAT-027');m=re.search(r'auf (\d), (\d)\+, (\d) sowie (\d), (\d)\+',row)
        if not m:raise ValueError('Missing explicit source beat positions')
        a,b,c,d,e=map(int,m.groups())
        return {'ticks':[(a-1)*480,(b-1)*480+240,(c-1)*480,1920+(d-1)*480,1920+(e-1)*480+240],
                'cycle_ticks':3840,'universal_guitar_batida_proven':False}
    if operation=='minor_leading_tone':
        tonic=parse_spelling(data['tonic'],'INT')
        gaps=[(tonic.midi_number-parse_spelling(n,'INT').midi_number) for n in data['sevenths']]
        return {'signature_fifths':data['signature_fifths'],'gaps_semitones':gaps,'same_leading_tone_behavior':len(set(gaps))==1}
    if operation=='metric_overlay':
        ppq=integer(data['ppq'],1,32767);chords=len(get_progression(data['progression']).chord_definitions)
        if chords!=data['chords']:raise ValueError('Declared harmonic loop differs from actual catalog progression')
        harmonic=chords*data['quarters_per_chord']*ppq;bell=6*ppq
        joint=lcm(harmonic,bell)
        return {'joint_ticks':joint,'bell_cycles':joint//bell,'harmonic_loops':joint//harmonic,
                'seconds':joint/ppq*60/data['quarter_bpm'],'style_pairing_proven':False}
    if operation=='surdo_role_grid':
        if data['scope']!='FLORIANOPOLIS_2010_MARCELINO_FIG3_4' or data['meter']!='2/4':
            raise ValueError('Source-specific roles required')
        ppq=integer(data['ppq'],1,32767)
        first=data['primeira_ticks'];second=data['segunda_ticks']
        if first!=[ppq,3*ppq] or second!=[0,2*ppq]:raise ValueError('Role onsets differ from source figures')
        return {'primeira_quarter_positions':[x//ppq+1 for x in first],
                'segunda_quarter_positions':[x//ppq+1 for x in second],
                'dynamic_accent_proven':False,'universal_norm_proven':False}
    raise ValueError('Unknown semantic probe operation')
