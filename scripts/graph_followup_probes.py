"""Bounded counterexamples, arrangements and an independent optimization oracle."""
import csv
from fractions import Fraction
from itertools import product
from math import log2

from src.steps.theory import parse_chord,parse_spelling
from src.steps.progression import get_progression,optimize_smooth_voice_leading
from scripts.audit_conflict_revisions import ROOT,source_bytes


def midi(note):return parse_spelling(note,'INT').midi_number


def drop2_shape(notes):
    # Inverse of dropping the second-highest closed-position voice an octave.
    if len(notes)!=4 or len({n%12 for n in notes})!=4:return False
    closed=sorted([notes[0]+12]+list(notes[1:]))
    return closed[-1]-closed[0]<12 and closed[-2]==notes[0]+12


def oracle(source,target,bass=None):
    """Independent Cartesian search; no production optimizer helpers used."""
    if len(source)!=4 or len(target)!=4 or any(a>=b for a,b in zip(source,source[1:])):
        raise ValueError('Oracle requires four strictly ascending voices and four pitch classes')
    choices=[[n for n in range(max(0,s-12),min(127,s+12)+1) if n%12 in target]
             for s in source]
    minima={'all':None,'drop2':None};counts={'all':0,'drop2':0}
    for candidate in product(*choices):
        if (any(a>=b for a,b in zip(candidate,candidate[1:])) or {n%12 for n in candidate}!=set(target)
                or (bass is not None and candidate[0]%12!=bass)):continue
        cost=sum(abs(a-b) for a,b in zip(source,candidate))
        for group in ['all']+(['drop2'] if drop2_shape(candidate) else []):
            counts[group]+=1
            if minima[group] is None or cost<minima[group]:minima[group]=cost
    if minima['all'] is None or minima['drop2'] is None:raise ValueError('Empty oracle search space')
    actual=optimize_smooth_voice_leading(source,target,bass_pc=bass)
    core_valid=(len(actual)==4 and all(type(n)is int and 0<=n<=127 for n in actual)
                and all(a<b for a,b in zip(actual,actual[1:])) and {n%12 for n in actual}==set(target)
                and all(abs(a-b)<=12 for a,b in zip(source,actual))
                and (bass is None or actual[0]%12==bass))
    return {'unconstrained_min':minima['all'],'drop2_min':minima['drop2'],
            'core_cost':sum(abs(a-b) for a,b in zip(source,actual)),
            'core_matches_oracle':core_valid and sum(abs(a-b) for a,b in zip(source,actual))==minima['all']}


def error_identities(data):
    historical=source_bytes(data['historical_source']).decode('utf-8')
    current=list(csv.DictReader(source_bytes(data['current_source']).decode('utf-8').splitlines()))
    matches=[row for row in current if list(row.values())[0]=='ERR-026']
    if len(matches)!=1:raise ValueError('Ambiguous current error-register row')
    text=' '.join(matches[0].values())
    return {'same_bare_id':'## ERR-026' in historical and 'ERR-026' in text,
            'historical_bass_first':'"Bass First"' in historical,
            'current_l1':'L1-Stimmführungsdistanz' in text,
            'same_semantics':('Bass First' in text and 'L1-Stimmführungsdistanz' in text)}


def calculate(spec):
    kind,data=spec['input']['operation'],spec['input']['data']
    if kind=='reference_invariance':
        ratios=[round((ref*2**(data['semitones']/12))/ref,9) for ref in data['references']]
        return {'ratios':ratios,'reference_independent':len(set(ratios))==1}
    if kind=='microtonal_interval':
        semitones=data['cents']/100
        return {'semitones':semitones,'integer_semitones':semitones.is_integer(),
                'ratio':round(2**(data['cents']/1200),9)}
    if kind=='slash_bass':
        result=[]
        for symbol in data['symbols']:
            c=parse_chord(symbol,'INT');bass=c.bass or c.root
            result.append({'bass_pc':int(bass.pitch_class),'root_pc':int(c.root.pitch_class),
                           'bass_is_chord_tone':bass.pitch_class in c.pitch_class_set})
        return result
    if kind=='pulse_pitch_independence':
        return [{'hz':data['hz'],'bpm':bpm,'quarter_seconds':round(60/bpm,6)} for bpm in data['bpm']]
    if kind=='subdivision_grids':
        return [[str(Fraction(data['ppq']*i,n)) for i in range(n)] for n in data['divisions']]
    if kind=='shells':
        progression=get_progression(data['progression'])
        if len(data['rh'])!=len(progression.chord_definitions):raise ValueError('Missing shell chords')
        pitches=[]
        for chord,notes in zip(progression.chord_definitions,data['rh']):
            values=[midi(n) for n in notes];root=int(chord.root.pitch_class)
            intervals={(n-root)%12 for n in values}
            if len(values)!=2 or len(intervals & {3,4})!=1 or len(intervals & {10,11})!=1:
                raise ValueError('Shell must explicitly contain one third and one seventh')
            if not {v%12 for v in values}<=chord.pitch_class_set:raise ValueError('Foreign shell pitch')
            pitches.append(values)
        return {'rh_pcs':[[v%12 for v in ns] for ns in pitches],
                'rh_l1':[sum(abs(a-b) for a,b in zip(x,y)) for x,y in zip(pitches,pitches[1:])]}
    if kind=='arrangement':
        chords=get_progression(data['progression']).chord_definitions
        if len(chords)!=len(data['lh']) or len(chords)!=len(data['rh']):raise ValueError('Incomplete arrangement')
        result=[]
        for chord,left,right in zip(chords,data['lh'],data['rh']):
            lh=[midi(n) for n in left];rh=[midi(n) for n in right];notes=lh+rh
            if (not lh or not rh or max(lh)>=min(rh) or any(a>=b for a,b in zip(notes,notes[1:]))
                    or not {n%12 for n in notes}<=chord.pitch_class_set):raise ValueError('Invalid arrangement pitches/order')
            if data.get('require_drop2') and not drop2_shape(notes):raise ValueError('Not a Drop-2 shape')
            root=int(chord.root.pitch_class)
            result.append({'symbol':chord.symbol,'total_root_present':root in {n%12 for n in notes},
                           'rh_root_present':root in {n%12 for n in rh}})
        return result
    if kind=='p12_transposition':
        target=get_progression('PROG-028').chord_definitions[0]
        original=[midi(s) for s in data['original']];shift=data['semitones']
        return {'target_symbol':target.symbol,'untransposed_fits':{n%12 for n in original}<=target.pitch_class_set,
                'transposed_fits':{(n+shift)%12 for n in original}<=target.pitch_class_set,
                'transposed_midi':[n+shift for n in original]}
    if kind=='optimizer_oracle':return oracle(data['source'],data['target_pcs'],data.get('bass_pc'))
    if kind=='error_namespaces':return error_identities(data)
    if kind=='overlay':
        total=data['bars']*data['beats_per_bar']*data['ppq']
        parts=data['parts']
        for notes in parts.values():
            if not notes or notes!=sorted(set(notes)) or any(type(n)is not int or not 0<=n<total for n in notes):
                raise ValueError('Invalid overlay timeline')
        return {'total_ticks':total,'keyboard_kick':sorted(set(parts['keyboard'])&set(parts['kick'])),
                'keyboard_snare':sorted(set(parts['keyboard'])&set(parts['snare']))}
    if kind=='arpeggio_events':
        chords=get_progression(data['progression']).chord_definitions
        if len(chords)!=len(data['rh']) or any(len(ns)!=8 for ns in data['rh']):raise ValueError('Eight eighths per chord required')
        for chord,notes in zip(chords,data['rh']):
            if not {midi(n)%12 for n in notes}<=chord.pitch_class_set:raise ValueError('Foreign arpeggio note')
        return {'events':8*len(chords),'total_ticks':len(chords)*4*data['ppq'],
                'last_onset':(len(chords)*8-1)*data['ppq']//2,'all_chord_tones':True}
    if kind=='source_bounded_swing':
        from scripts.audit_golden_remaining import calculate as bounded
        return bounded('swing_regression',data)
    raise ValueError('Unknown graph follow-up operation: '+kind)
