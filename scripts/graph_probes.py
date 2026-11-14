"""Bounded audit calculations; no authority to approve a musical graph."""

from math import lcm
from xml.etree import ElementTree

from src.steps.theory import parse_chord, parse_spelling, midi_to_frequency, midi_to_pitch_class
from src.steps.progression import resolve_roman_degree, absolute_semitone_distance, detect_parallel_fifths_octaves


def calculate(spec):
    kind, data = spec['kind'], spec['input']
    if kind == 'frequency':
        return [round(midi_to_frequency(value), 6) for value in data['midi']]
    if kind == 'pitch_class':
        return [int(midi_to_pitch_class(value)) for value in data['midi']]
    if kind == 'spellings':
        notes = [parse_spelling(value, data['convention']) for value in data['notes']]
        return [[note.step, note.alteration, int(note.pitch_class)] for note in notes]
    if kind == 'collections':
        return [sorted({int(parse_spelling(note, 'INT').pitch_class) for note in notes}) for notes in data['notes']]
    if kind == 'chords':
        return [sorted(map(int, parse_chord(symbol, 'INT').pitch_class_set)) for symbol in data['symbols']]
    if kind == 'roman':
        return [resolve_roman_degree(value, data['key'], data.get('minor', False), convention='INT').symbol
                for value in data['degrees']]
    if kind == 'voice_cost':
        return absolute_semitone_distance(data['from'], data['to'])
    if kind == 'parallels':
        return bool(detect_parallel_fifths_octaves(data['from'], data['to']))
    if kind == 'swing':
        onset = round(data['ppq'] / 2 * data['percent'] / 100)
        return [onset, onset - data['ppq'] // 4, round((onset-data['ppq']/4)*60000/(data['ppq']*data['bpm']), 6)]
    if kind == 'metric_duality':
        return round(4 * 60 / data['fast_bpm'], 6) == round(2 * 60 / data['slow_bpm'], 6)
    if kind == 'cycle':
        return lcm(*data['periods'])
    if kind == 'clave_timeline':
        if data['ppq']!=480 or len(data['bars'])!=2 or any(not 1<=b<5 for bar in data['bars'] for b in bar):
            raise ValueError('Expected two explicitly transcribed 4/4 bars at 480 PPQ')
        return [round((4*i+beat-1)*data['ppq']) for i,bar in enumerate(data['bars']) for beat in bar]
    if kind == 'xml':
        pitch = ElementTree.fromstring(data['xml'])
        return {child.tag: child.text for child in pitch}
    if kind == 'same_root_shift':
        first, second = [parse_chord(x, 'INT') for x in data['symbols']]
        a, b = first.pitch_class_set, second.pitch_class_set
        return {'root_preserved': first.root.pitch_class == second.root.pitch_class,
                'common': sorted(map(int, a & b)), 'removed': sorted(map(int, a-b)), 'added': sorted(map(int,b-a))}
    if kind == 'bass_ambiguity':
        return [[int(parse_chord(s,'INT').root.pitch_class), int((parse_chord(s,'INT').bass or parse_chord(s,'INT').root).pitch_class)]
                for s in data['symbols']]
    if kind == 'draft_events':
        # A newly authored exercise is not a recovered historical montuno.
        total = data['bars'] * data['beats'] * data['ppq']
        occupied = set()
        if (data['ppq'] != 480 or data['beats'] != 4 or data['bars'] != 4
                or data['clave_onsets'] != [480,960,1920,2640,3360,4320,4800,5760,6480,7200]):
            raise ValueError('Draft requires its explicitly notated 2:3 clave overlay')
        for event in data['events']:
            onset, duration, note, chord = event
            if (type(onset) is not int or type(duration) is not int or duration <= 0 or onset < 0
                    or onset + duration > total or (onset, note) in occupied):
                raise ValueError('Invalid or duplicate draft event')
            if parse_spelling(note,'INT').pitch_class not in parse_chord(chord,'INT').pitch_class_set:
                raise ValueError('Draft note outside stated chord')
            if data['chords'][onset // (data['beats'] * data['ppq'])] != chord:
                raise ValueError('Draft harmony does not match event position')
            occupied.add((onset,note))
        return {'total_ticks': total, 'events': len(data['events']),
                'onsets': [event[0] for event in data['events']],
                'clave_relation': 'SHARED_GRID_ONLY_NOT_HISTORICAL_STYLE_PROOF',
                'historical_transcription': False}
    raise ValueError('Unknown audit probe: '+kind)


def evaluate(spec):
    actual = calculate(spec)
    if actual != spec['expected']:
        raise ValueError(f"Probe {spec['id']} differs: {actual!r}")
    return actual
