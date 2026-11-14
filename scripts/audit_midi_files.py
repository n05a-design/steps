"""Read-only SMF envelope validation and independent Mido event decoding."""

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import struct

ROOT=Path(__file__).resolve().parents[1]


def envelope(data):
    if len(data)<14 or data[:4]!=b'MThd':raise ValueError('Missing SMF header')
    length=struct.unpack('>I',data[4:8])[0]
    if length<6 or 8+length>len(data):raise ValueError('Truncated SMF header')
    format_,tracks,division=struct.unpack('>HHH',data[8:14])
    if format_ not in (0,1,2) or not tracks or (format_==0 and tracks!=1) or division==0:
        raise ValueError('Invalid SMF format/track count/division')
    if division&0x8000:
        rate=(division>>8)-256
        if rate not in (-24,-25,-29,-30) or division&255==0:raise ValueError('Invalid SMPTE division')
    offset=8+length;found=0
    while offset<len(data):
        if offset+8>len(data):raise ValueError('Truncated chunk header')
        kind=data[offset:offset+4];size=struct.unpack('>I',data[offset+4:offset+8])[0]
        offset+=8
        if offset+size>len(data):raise ValueError('Truncated chunk payload')
        if kind==b'MTrk':found+=1
        offset+=size
    if found!=tracks:raise ValueError('Track count differs from MThd')
    return {'format':format_,'tracks':tracks,'division':division}


def inspect(path):
    import mido
    data=path.read_bytes();header=envelope(data);mid=mido.MidiFile(path,clip=False)
    if mid.type!=header['format'] or len(mid.tracks)!=header['tracks']:raise ValueError('Independent reader disagrees with envelope')
    events=0;notes=0;ticks=[];warnings=[]
    for number,track in enumerate(mid.tracks):
        if not track or track[-1].type!='end_of_track':warnings.append(f'track {number}: missing terminal EOT in decoded stream')
        end_count=sum(msg.type=='end_of_track' for msg in track)
        if end_count!=1:raise ValueError('Unexpected EOT count')
        tick=0
        for msg in track:
            if type(msg.time) is not int or msg.time<0:raise ValueError('Invalid delta time')
            tick+=msg.time;events+=1;notes+=msg.type=='note_on' and msg.velocity>0
            if msg.type=='set_tempo' and msg.tempo<=0:raise ValueError('Nonpositive tempo')
        ticks.append(tick)
    return {**header,'events':events,'note_ons':notes,'track_end_ticks':ticks,'warnings':warnings,
            'independent_reader':'mido 1.3.3','rights_status':'OPEN_NOT_A_DISTRIBUTION_APPROVAL','musical_review':'AUSSTEHEND'}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--json-out',type=Path,required=True)
    args=parser.parse_args()
    import importlib.metadata
    if importlib.metadata.version('mido')!='1.3.3':raise SystemExit('Use audit reader mido==1.3.3')
    rows=[]
    for path in sorted((ROOT/'research').rglob('*')):
        if path.suffix.lower() not in {'.mid','.midi'}:continue
        row={'path':path.relative_to(ROOT).as_posix(),'bytes':path.stat().st_size,'sha256':sha256(path.read_bytes()).hexdigest()}
        try:row.update(status='TECHNICAL_PASS',**inspect(path))
        except (ValueError,OSError,EOFError,KeyError) as error:row.update(status='TECHNICAL_FAIL',error=str(error))
        rows.append(row)
    args.json_out.write_text(json.dumps({'reader':'mido==1.3.3','files':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'files':len(rows),'status':dict(Counter(r['status'] for r in rows)), 'musical_approvals':0}))
    if any(row['status']!='TECHNICAL_PASS' for row in rows):raise SystemExit(1)


if __name__=='__main__':main()
