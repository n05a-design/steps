"""Bounded note-number pattern observations; no authenticated instrument or genre claim."""
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

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_rwc_joint import ARCHIVE_SHA, COMMIT, four_four_bars
from scripts.audit_jazzsamba_components import CATALOG_SHA, SELECTION_SHA

OUTPUT = ROOT / 'docs/audit/fable-5.2/REL_PATTERN_KOMPONENTEN_2026-11-14.json'


def events(raw):
    import mido
    midi = mido.MidiFile(file=io.BytesIO(raw))
    if midi.type not in (0, 1) or midi.ticks_per_beat <= 0:
        raise ValueError('Metrical type0/1 MIDI required')
    elapsed = 0.; tempo = 500000; out = {}
    for msg in mido.merge_tracks(midi.tracks):
        elapsed += mido.tick2second(msg.time, midi.ticks_per_beat, tempo)
        if msg.type == 'set_tempo': tempo = msg.tempo
        if msg.type == 'note_on' and msg.velocity > 0 and msg.channel == 9:
            out.setdefault(msg.note, []).append(elapsed)
    return out


def grid_match(bar, note_times, expected, tolerance=.1):
    """One-to-one matching within [bar_start,bar_end), no reused or adjacent-bar hits."""
    if len(bar) != 5 or any(not math.isfinite(t) or t < 0 for t in bar) or any(b <= a for a, b in zip(bar, bar[1:])):
        raise ValueError('Complete ordered quarter grid required')
    if not 0 <= tolerance < .25 or not expected or any(not 0 <= x < 4 for x in expected) or len(set(expected)) != len(expected):
        raise ValueError('Unique bounded target phases required')
    if any(not math.isfinite(t) or t < 0 for t in note_times) or any(b < a for a, b in zip(note_times, note_times[1:])):
        raise ValueError('Ordered finite note times required')
    times = note_times[bisect_left(note_times, bar[0]):bisect_left(note_times, bar[-1])]
    remaining = list(times); hits = 0
    for phase in sorted(expected):
        beat = int(phase); width = bar[beat+1] - bar[beat]
        wanted = bar[beat] + (phase-beat)*width
        candidates = [(abs(t-wanted), i) for i,t in enumerate(remaining) if abs(t-wanted) <= tolerance*width + 1e-9]
        if candidates:
            _, index = min(candidates); remaining.pop(index); hits += 1
    return {'required': len(expected), 'matched': hits, 'observed': len(times),
            'subset': hits == len(expected), 'same_note_grid': hits == len(expected) and len(times) == len(expected)}


def roles(bar, note_times, relation):
    if relation == 'REL-001':
        spec = {'kick_core_35_36': ((35,36), (0,2)), 'snare_38': ((38,), (1,3)),
                'hat_42': ((42,), tuple(i/2 for i in range(8)))}
    elif relation == 'REL-005':
        spec = {'ride_quarters_51': ((51,), (0,1,2,3)), 'pedal_44': ((44,), (1,3)),
                'ride_triplet_skip_51_proposal': ((51,), (0,1,1+2/3,2,3,3+2/3))}
    else: raise ValueError('Unsupported relation')
    return {key: grid_match(bar, sorted(t for note in notes for t in note_times.get(note, [])), phases)
            for key, (notes, phases) in spec.items()}


def aggregate(bars, note_times, intervals, relation):
    selected = [bar for bar in bars if any(a <= bar[0] and bar[-1] <= b for a,b in intervals)]
    # A bar belongs to the union, never once per overlapping harmony window.
    counts = Counter(); tempo = []
    for bar in selected:
        result = roles(bar, note_times, relation)
        for key, value in result.items():
            for level in ('subset','same_note_grid'):
                counts[key+'_'+level] += int(value[level])
        keys = ('kick_core_35_36','snare_38','hat_42') if relation == 'REL-001' else ('ride_quarters_51','pedal_44')
        counts['joint_core_subset'] += int(all(result[k]['subset'] for k in keys))
        tempo.append(240/(bar[-1]-bar[0]))
    return {'unique_complete_bars_in_harmony_windows':len(selected), 'counts':dict(counts),
            'bar_average_bpm_min':min(tempo) if tempo else None, 'bar_average_bpm_max':max(tempo) if tempo else None}


def measure(rwc_archive, jazz_manifest):
    raw = Path(rwc_archive).read_bytes()
    if sha256(raw).hexdigest() != ARCHIVE_SHA: raise ValueError('Unexpected RWC archive')
    z = zipfile.ZipFile(io.BytesIO(raw)); prefix = 'rwc-annotations-'+COMMIT+'/'
    rwc = json.loads((ROOT/'docs/audit/fable-5.2/KORPUS_RWC_GEMEINSAME_ZEITACHSE_2026-11-14.json').read_text(encoding='utf8'))
    manifest = json.loads(Path(jazz_manifest).read_text(encoding='utf8'))
    if manifest['catalog_sha256'] != CATALOG_SHA or manifest['source_record'] != '10.5281/zenodo.22943963': raise ValueError('Unexpected Jazz catalog')
    if sha256(json.dumps(sorted(r['song_id'] for r in manifest['records'])).encode()).hexdigest() != SELECTION_SHA: raise ValueError('Unexpected selection')
    jazz = json.loads((ROOT/'docs/audit/fable-5.2/KORPUS_JAZZSAMBA_SWING_2026-11-14.json').read_text(encoding='utf8'))
    rows = []
    for record in rwc['records']:
        ident = record['recording_id']; base = prefix+'01_annotations_preprocessed/'
        midi = z.read(base+'MIDI_aligned/RWC-P/'+ident+'.mid'); beats_raw = z.read(base+'beats/RWC-P/'+ident+'.csv')
        if sha256(midi).hexdigest() != record['member_sha256']['midi'] or sha256(beats_raw).hexdigest() != record['member_sha256']['beats']: raise ValueError('RWC member mismatch')
        bars = four_four_bars(list(csv.DictReader(io.StringIO(beats_raw.decode()), delimiter=';')))
        intervals = [(w['start_seconds'],w['end_seconds']) for w in record['patterns']['PROG-001']['exact']]
        if intervals:
            rows.append({'relation_id':'REL-001','record_id':ident,'source_sha256':sha256(midi).hexdigest(),
                         'observation':aggregate(bars, events(midi), intervals, 'REL-001')})
    for source in manifest['records']:
        blobs = {}
        for kind in ('drums','bars'):
            member = source['members'][kind]
            expected = 'async/songs/'+source['basename']+'/preferred/'+('drums.mid' if kind == 'drums' else 'annotations/bars.csv')
            if member['member'] != expected: raise ValueError('Unexpected take or derived lane')
            blobs[kind] = Path(member['local_file']).read_bytes()
            if sha256(blobs[kind]).hexdigest() != member['sha256']: raise ValueError('Jazz member mismatch')
        record = next(r for r in jazz['records'] if r['song_id'] == source['song_id'])
        bars = []
        for row in csv.DictReader(io.StringIO(blobs['bars'].decode())):
            a,b = float(row['start_time']),float(row['end_time'])
            bars.append([a+(b-a)*i/4 for i in range(5)])
        intervals = [(w['start_seconds'],w['end_seconds']) for w in record['patterns']['exact']['windows']]
        rows.append({'relation_id':'REL-005','record_id':source['song_id'],'source_sha256':sha256(blobs['drums']).hexdigest(),
                     'observation':aggregate(bars, events(blobs['drums']), intervals, 'REL-005')})
    return {'schema_version':1,'base_commit':'cda6cb99bf3d4c6bc1bde29c4ffef1405a117c0f',
            'source_archive_sha256':ARCHIVE_SHA,'jazz_catalog_sha256':CATALOG_SHA,
            'human_approval':'AUSSTEHEND','historical_assertion_closed':False,'instrument_mapping_verified':False,
            'exact_pattern_verified':False,'sampling_prevalence_verified':False,
            'method':'Channel9 positive note-ons; half-open complete bars in union of strict harmony-shape windows; one-to-one within0.1 local quarter. RWC measured beat grid; Jazz quarter positions interpolated from annotated bar endpoints, not independently measured beat times.',
            'limits':'Note numbers are hypotheses, not instrument authentication. REL001 core excludes unresolved 3e+ syncopation and exact115BPM. REL005 triplet skip is a separate proposal, not a unique Friberg ratio; dynamics/feathering, performed harmony, audio alignment and130BPM identity are unverified. Subset permits extra events; same_note_grid applies only to each specified note group, never whole pattern.',
            'rows':rows}


def validate(d):
    for key in ('historical_assertion_closed','instrument_mapping_verified','exact_pattern_verified','sampling_prevalence_verified'):
        if d[key] is not False: raise ValueError('Premature acceptance')
    if d['human_approval'] != 'AUSSTEHEND' or d['source_archive_sha256'] != ARCHIVE_SHA or d['jazz_catalog_sha256'] != CATALOG_SHA: raise ValueError('Evidence identity changed')
    pairs = [(r['relation_id'],r['record_id']) for r in d['rows']]
    rwc = json.loads((ROOT/'docs/audit/fable-5.2/KORPUS_RWC_GEMEINSAME_ZEITACHSE_2026-11-14.json').read_text(encoding='utf8'))
    jazz = json.loads((ROOT/'docs/audit/fable-5.2/KORPUS_JAZZSAMBA_SWING_2026-11-14.json').read_text(encoding='utf8'))
    if rwc['archive_sha256'] != ARCHIVE_SHA or jazz['catalog_sha256'] != CATALOG_SHA:
        raise ValueError('Component source identity changed')
    expected = {('REL-001',r['recording_id']):r['member_sha256']['midi'] for r in rwc['records'] if r['patterns']['PROG-001']['exact']}
    expected.update({('REL-005',r['song_id']):r['source_members']['drums']['sha256'] for r in jazz['records']})
    if len(pairs) != len(set(pairs)) or set(pairs) != set(expected): raise ValueError('Selection identity mismatch')
    for row in d['rows']:
        if row['source_sha256'] != expected[(row['relation_id'],row['record_id'])]: raise ValueError('Pattern MIDI source hash changed')
        obs = row['observation']; n = obs['unique_complete_bars_in_harmony_windows']
        if type(n) is not int or n < 0 or any(type(v) is not int or not 0 <= v <= n for v in obs['counts'].values()): raise ValueError('Invalid denominator')
        if not n and (obs['counts'] or obs['bar_average_bpm_min'] is not None or obs['bar_average_bpm_max'] is not None):
            raise ValueError('Empty observation must have no counts or tempo')
        keys = ('kick_core_35_36','snare_38','hat_42') if row['relation_id'] == 'REL-001' else ('ride_quarters_51','pedal_44','ride_triplet_skip_51_proposal')
        if n and set(obs['counts']) != {key+'_'+level for key in keys for level in ('subset','same_note_grid')} | {'joint_core_subset'}:
            raise ValueError('Missing or unexpected role counts')
        for key in keys:
            if n and obs['counts'][key+'_same_note_grid'] > obs['counts'][key+'_subset']: raise ValueError('Exact subset hierarchy invalid')
        if n and obs['counts']['joint_core_subset'] > min(obs['counts'][k+'_subset'] for k in keys[:3 if row['relation_id']=='REL-001' else 2]):
            raise ValueError('Joint count exceeds component')
        if n and not 0 < obs['bar_average_bpm_min'] <= obs['bar_average_bpm_max'] < math.inf: raise ValueError('Invalid tempo bounds')


def main():
    p = argparse.ArgumentParser(); p.add_argument('--rwc-archive'); p.add_argument('--jazz-manifest'); p.add_argument('--check',action='store_true'); p.add_argument('--write',action='store_true'); a=p.parse_args()
    if bool(a.rwc_archive) != bool(a.jazz_manifest): p.error('Both local source arguments required')
    if a.write and not a.rwc_archive: p.error('Writing requires source measurement')
    d = measure(a.rwc_archive,a.jazz_manifest) if a.rwc_archive else json.loads(OUTPUT.read_text(encoding='utf8'))
    validate(d)
    if a.write: OUTPUT.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    if a.check and d != json.loads(OUTPUT.read_text(encoding='utf8')): raise SystemExit('Pattern observations stale')
    print(json.dumps({'records':len(d['rows']),'exact_pattern_verified':False,'historical_assertion_closed':False}))


if __name__ == '__main__': main()
