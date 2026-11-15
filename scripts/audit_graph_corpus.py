"""Audit scoped corpus capability and observations; never infer genre acceptance."""
import argparse
from collections import Counter
import csv
from fractions import Fraction
from hashlib import sha256
import io
import json
from pathlib import Path
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
PLAN=ROOT/'knowledge/relations/GRAPH_CORPUS_REVIEW.json'
MATRIX=ROOT/'docs/audit/fable-5.2/GRAPH_KORPUS_14_2026-11-14.csv'
OBS=ROOT/'docs/audit/fable-5.2/GRAPH_KORPUS_GMD_2026-11-14.json'
SCOPE={'CR-029','CR-030','CR-031','CR-032','REL-001','REL-005','REL-006','REL-007',
       'REL-014','REL-015','REL-017','REL-026','REL-032','REL-035'}
GMD_SHA='651cbc524ffb891be1a3e46d89dc82a1cecb09a57c748c7b45b844c4841dcc1e'


def capability_gaps(required,available):
    """A union of annotations from unrelated recordings is not aligned evidence."""
    return sorted(set(required)-set(available))


def beat_coverage(events,ppq,bars,tolerance=0.1):
    if type(ppq)is not int or ppq<=0 or type(bars)is not int or bars<=0 or not 0<=tolerance<0.5:
        raise ValueError('Explicit positive PPQ, complete bars and sub-half-beat tolerance required')
    # Events are (absolute_tick, note_number, velocity); note-on velocity zero is not a hit.
    targets={'kick_1_3':[(b*4+q)*ppq for b in range(bars) for q in (0,2)],
             'snare_2_4':[(b*4+q)*ppq for b in range(bars) for q in (1,3)]}
    notes={'kick_1_3':{36},'snare_2_4':{37,38,40}}
    return {key:{'matched':sum(any(velocity>0 and note in notes[key] and abs(tick-target)<=tolerance*ppq
                                 for tick,note,velocity in events) for target in times),
                 'opportunities':len(times)} for key,times in targets.items()}


def slot_set_coverage(events,ppq,bars,tolerance='0.1'):
    """Separate event-to-slot calculation with exact inclusive tick boundaries."""
    result={}
    for role,notes,parity in [('kick_1_3',{36},0),('snare_2_4',{37,38,40},1)]:
        slots=set()
        for tick,note,velocity in events:
            q=round(Fraction(tick,ppq))
            if (velocity>0 and note in notes and 0<=q<4*bars and q%2==parity
                    and abs(tick-q*ppq)<=Fraction(tolerance)*ppq):slots.add(q)
        result[role]={'matched':len(slots),'opportunities':2*bars}
    return result


def measure_gmd(archive):
    """Optional local reproduction using audit-only Mido; raw MIDI stays outside Git."""
    import mido
    payload=Path(archive).read_bytes()
    if sha256(payload).hexdigest()!=GMD_SHA:raise ValueError('GMD archive differs from publisher hash')
    z=zipfile.ZipFile(io.BytesIO(payload));info=next(n for n in z.namelist() if n.endswith('/info.csv'))
    metadata=list(csv.DictReader(io.StringIO(z.read(info).decode('utf8'))));prefix=info[:-len('info.csv')]
    selected=[r for r in metadata if r['style'].split('/')[0]=='pop' and r['beat_type']=='beat' and r['time_signature']=='4-4']
    if len({r['id'] for r in selected})!=len(selected):raise ValueError('Duplicate recording identity')
    results=[]
    for row in selected:
        raw=z.read(prefix+row['midi_filename']);m=mido.MidiFile(file=io.BytesIO(raw));tick=0;events=[];meters=[]
        for msg in mido.merge_tracks(m.tracks):
            tick+=msg.time
            if msg.type=='time_signature':meters.append((msg.numerator,msg.denominator))
            if msg.type=='note_on' and msg.velocity>0:
                if msg.channel!=9:raise ValueError('Unexpected non-drum channel')
                events.append((tick,msg.note,msg.velocity))
        if not meters or set(meters)!={(4,4)}:raise ValueError('Metadata/meter mismatch')
        bars=tick//(4*m.ticks_per_beat)
        if bars<=0:raise ValueError('No complete bar')
        coverage=beat_coverage(events,m.ticks_per_beat,bars)
        if coverage!=slot_set_coverage(events,m.ticks_per_beat,bars):raise ValueError('Independent timing calculation differs')
        results.append({'recording_id':row['id'],'member':prefix+row['midi_filename'],
                        'sha256':sha256(raw).hexdigest(),'drummer':row['drummer'],'session':row['session'],
                        'style':row['style'],'bpm':int(row['bpm']),'split':row['split'],
                        'ppq':m.ticks_per_beat,'complete_bars':bars,
                        'coverage':coverage})
    totals={k:{field:sum(x['coverage'][k][field] for x in results) for field in ('matched','opportunities')}
            for k in ('kick_1_3','snare_2_4')}
    return {'schema_version':1,'archive_sha256':GMD_SHA,'metadata_rows':len(metadata),
            'metadata_style_counts':dict(sorted(Counter(r['style'].split('/')[0] for r in metadata).items())),
            'selection':'primary style exactly pop; beat_type beat; time_signature 4-4',
            'tolerance_quarter_notes':0.1,'bar_origin':'tick zero; complete bars before SMF end-of-track',
            'kick_notes':[36],'snare_notes':[37,38,40],
            'denominator':'two target opportunities per role per complete bar; pooled hits are not independent songs',
            'selected_recordings':len(results),'selected_drummers':len({x['drummer'] for x in results}),
            'totals':totals,'recordings':results,'population_generalization':False,
            'human_approval':'AUSSTEHEND','relation_status':'OPEN','historical_assertion_closed':False,
            'attribution':'Google LLC, Groove MIDI Dataset v1.0.0, CC BY 4.0; Gillick et al., Learning to Groove with Inverse Sequence Transformations (2019)',
            'source_url':'https://magenta.tensorflow.org/datasets/groove'}


def validate_observation(d):
    if (d['schema_version']!=1 or d['archive_sha256']!=GMD_SHA or d['metadata_rows']!=1150
            or d['population_generalization'] is not False or d['historical_assertion_closed'] is not False
            or d['human_approval']!='AUSSTEHEND' or d['relation_status']!='OPEN'
            or d['selected_recordings']!=len(d['recordings']) or not d['recordings']):
        raise ValueError('Invalid corpus observation or premature acceptance')
    ids=[x['recording_id'] for x in d['recordings']]
    if len(set(ids))!=len(ids) or d['selected_drummers']!=len({x['drummer'] for x in d['recordings']}):
        raise ValueError('Correlated/duplicate recording identity misreported')
    for row in d['recordings']:
        if row['style'].split('/')[0]!='pop' or len(row['sha256'])!=64 or row['complete_bars']<=0:
            raise ValueError('Observation outside selection')
        for role,v in row['coverage'].items():
            if role not in ('kick_1_3','snare_2_4') or not 0<=v['matched']<=v['opportunities'] or v['opportunities']!=2*row['complete_bars']:
                raise ValueError('Invalid event denominator')
    for role in ('kick_1_3','snare_2_4'):
        for field in ('matched','opportunities'):
            if d['totals'][role][field]!=sum(x['coverage'][role][field] for x in d['recordings']):
                raise ValueError('Pooled totals differ')


def audit(document=None):
    d=document if document is not None else json.loads(PLAN.read_text(encoding='utf8'))
    with (ROOT/'knowledge/relations/MUSIC_CONCEPT_RELATIONS.csv').open(encoding='utf8') as f:
        originals={r['relation_id']:r for r in csv.DictReader(f)}
    rows=d['cases'];sources={x['id']:x for x in d['corpus_candidates']}
    if d['schema_version']!=1 or len(rows)!=14 or {x['relation_id'] for x in rows}!=SCOPE or len(sources)!=len(d['corpus_candidates']):
        raise ValueError('Original corpus scope changed')
    out=[]
    for row in rows:
        original=originals[row['relation_id']]
        required={'chords','drum_events','genre','aligned_recording_identity','representative_song_sample'} if row['relation_id'].startswith('REL-') and row['relation_id']!='REL-017' else {
            'CR-029':{'genre','drum_events','representative_song_sample'},
            'CR-030':{'house_subgenre','drum_events','representative_song_sample'},
            'CR-031':{'chords','genre','cadence_labels','representative_song_sample'},
            'CR-032':{'house_subgenre','tempo','drum_events','representative_song_sample'},
            'REL-017':{'jumpup_subgenre','drum_events','bass_events','aligned_recording_identity'}}[row['relation_id']]
        if (row['original_row_sha256']!=sha256(json.dumps(original,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
                or row['original_edge']!={k:original[k] for k in ('source_id','target_id','relation_type')}
                or row['status']!='OPEN' or row['human_approval']!='AUSSTEHEND'
                or row['production_use_allowed'] is not False or row['historical_assertion_closed'] is not False
                or set(row['required_annotations'])!=required or not row['sampling_frame'] or not row['unresolved_claim']
                or not row['next_evidence'] or not row['candidate_ids']):raise ValueError('Unbound or prematurely accepted corpus case')
        checks={ident:capability_gaps(row['required_annotations'],sources[ident]['available_annotations']) for ident in row['candidate_ids']}
        if any(not gaps for gaps in checks.values()):raise ValueError('Candidate now sufficient: perform actual observation review instead of automatic acceptance')
        for a in row['project_anchors']:
            p=ROOT/a['path']
            if p.is_absolute() and not p.resolve().is_relative_to(ROOT):raise ValueError('Source outside repository')
            if sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest()!=a['lf_sha256'] or a['row'] not in p.read_text(encoding='utf8').splitlines():
                raise ValueError('Project catalog anchor changed')
        observation=('GMD_POP_SCOPED' if row['relation_id']=='CR-029' else
                     'GIANTSTEPS_GENRE_TEMPO_ONLY' if row['relation_id'] in {'CR-030','CR-032'} else
                     'BILLBOARD_CHORD_SHAPES_NOT_CADENCES' if row['relation_id']=='CR-031' else
                     'GIANTSTEPS_PARENT_DNB_LABEL_NOT_JUMPUP' if row['relation_id']=='REL-017' else
                     'BILLBOARD_HARMONY_COMPONENT_ONLY')
        if row['relation_id'] in {'CR-029','CR-031'} or (row['relation_id'].startswith('REL-') and row['relation_id']!='REL-017'):
            observation+=';RWC_SAME_ID_SYMBOLIC_COMPONENTS_NOT_EXACT_PATTERN'
        if row['relation_id']=='REL-005':observation+=';JAZZSAMBA_SWING_CHART_ORIGINAL_DRUM_COMPONENTS_ONLY'
        if row['relation_id'] in {'REL-001','REL-005'}:observation+=';BOUNDED_NOTE_GRID_NO_COMPLETE_CORE_MATCH_NOT_GENRE_DISPROOF'
        if row['relation_id']=='REL-001':observation+=';REF0030_1320TICK_SYNCOPATION_SENSITIVITY_NO_JOINT_MATCH'
        if row['relation_id']=='REL-005':observation+=';GMD_SWING_PUBLISHER_MAPPED_DRUM_COMPONENT_NOT_HARMONIC_PAIRING'
        if row['relation_id']=='REL-005':observation+=';ACTUAL_RIDE_IOI_DIAGNOSTIC_NOT_FEATHERING_APPROVAL'
        out.append({'relation_id':row['relation_id'],'original_row_sha256':row['original_row_sha256'],**row['original_edge'],
                    'sampling_frame':row['sampling_frame'],'required_annotations':';'.join(row['required_annotations']),
                    'candidate_gaps':json.dumps(checks,ensure_ascii=False,sort_keys=True),
                    'local_observation':observation,'rwc_scope':row['rwc_scope'],
                    'unresolved_claim':row['unresolved_claim'],'next_evidence':row['next_evidence'],
                    'relation_status':'OPEN','human_approval':'AUSSTEHEND','production_use_allowed':False})
    validate_observation(json.loads(OBS.read_text(encoding='utf8')))
    validate_sources(json.loads((ROOT/'docs/audit/fable-5.2/GRAPH_CDR019_CDR021_QUELLEN_2026-11-14.json').read_text(encoding='utf8')))
    from scripts import audit_billboard_components as billboard, audit_edm_tempo as edm
    billboard.validate(json.loads(billboard.OUTPUT.read_text(encoding='utf8')))
    edm.validate(json.loads(edm.OUTPUT.read_text(encoding='utf8')))
    validate_original_search(json.loads((ROOT/'docs/audit/fable-5.2/CDR019_ORIGINALSUCHE_2026-11-14.json').read_text(encoding='utf8')))
    from scripts import audit_rwc_joint as rwc
    rwc.validate(json.loads(rwc.OUTPUT.read_text(encoding='utf8')))
    from scripts import audit_jazzsamba_components as jazz
    jazz.validate(json.loads(jazz.OUTPUT.read_text(encoding='utf8')))
    from scripts import audit_relation_patterns as patterns
    patterns.validate(json.loads(patterns.OUTPUT.read_text(encoding='utf8')))
    from scripts import audit_pattern_syncopation as syncopation
    syncopation.validate(json.loads(syncopation.OUTPUT.read_text(encoding='utf8')))
    from scripts import audit_gmd_swing as swing
    swing.validate(json.loads(swing.OUTPUT.read_text(encoding='utf8')))
    from scripts import audit_gmd_swing_detail as detail
    detail.validate(json.loads(detail.OUTPUT.read_text(encoding='utf8')))
    validate_garcia_followup(json.loads((ROOT/'docs/audit/fable-5.2/CDR019_GARCIA_2023_QUELLENBEFUND_2026-11-14.json').read_text(encoding='utf8')))
    return out


def validate_garcia_followup(d):
    if (d['schema_version']!=1 or d['relation_id']!='CDR-019' or d['human_approval']!='AUSSTEHEND'
            or d['historical_assertion_closed'] is not False or d['requested_original_fulltexts_verified']!=0
            or d['new_author_article_scoped_checks']!=1 or d['source']['author']!='Walter Garcia'
            or d['source']['journal']!='Iberic@l24,2023'
            or d['source']['sha256']!='5f659a994bcf07c95adbde4fbec83352e56992fc987664325cc09954cee523d7'
            or d['source']['visually_checked_pdf_pages']!=[1,7] or not d['source']['scope'] or not d['source']['rights']):
        raise ValueError('Later author article is not verification of the requested older originals')


def validate_original_search(d):
    expected={'REILY_PUBLISHER','CABRAL_VOLUME2_PREVIEW','REILY_DISCOVERY_MIRRORS','GARCIA_USP_1998','GARCIA_1999_CATALOG','SCHREINER_1993_CATALOG'}
    if (d['schema_version']!=1 or d['relation_id']!='CDR-019' or d['human_approval']!='AUSSTEHEND'
            or d['historical_assertion_closed'] is not False or d['verified_causal_claim'] is not False
            or d['fulltext_originals_verified']!=0 or len(d['records'])!=6 or {r['id'] for r in d['records']}!=expected):
        raise ValueError('Invalid original search scope or premature source acceptance')
    statuses={'REFERENCE_LIST_READ_BODY_ACCESS_REQUIRED','TOC_ONLY','INDEXED_EXCERPT_ONLY','INSTITUTIONAL_CATALOG_ONLY','CATALOG_ONLY'}
    for r in d['records']:
        if r['status'] not in statuses or not all(r[k].strip() for k in ('url','finding','access_result','next_required')):
            raise ValueError('Search result is not an original-page verification')
        if r['id']=='CABRAL_VOLUME2_PREVIEW' and (r['pages']!=4 or r['sha256']!='ed3c09a75b6ef168cfc344d260685ae0da81fbfeeab31cb44627c92905b4ccef' or r['status']!='TOC_ONLY'):
            raise ValueError('Preview misrepresented as full book')


def validate_sources(d):
    expected={'MARCELINO_2010':('CDR-021','9510e9bd804c786522f767832dbca4bff4e32dc6e9e0df101774bee81e34fa4c',[34]),
              'GHEZZI_2009':('CDR-019','abd8b07b100a55a162af4be0e144f0eb96a90d29d0233b92ffed4f37d637c7ff',[9])}
    if (d['schema_version']!=1 or d['human_approval']!='AUSSTEHEND' or d['historical_definitions_resolved'] is not False
            or d['redistribution']!='METADATA_AND_OWN_FINDINGS_ONLY'
            or len(d['sources'])!=3 or {s['id'] for s in d['sources']}!=set(expected)|{'REILY_1996_METADATA'}):
        raise ValueError('Invalid source package or premature acceptance')
    for source in d['sources']:
        if not source['url'].startswith('https://') or not source['locator'] or not source['limits']:
            raise ValueError('Missing source locator or evidence limit')
        if source['id'] in expected:
            relation,digest,pages=expected[source['id']]
            if source['relation_id']!=relation or source['sha256']!=digest or source['visually_checked_pdf_pages']!=pages:
                raise ValueError('Source identity or visually inspected scope changed')


def render(rows):
    f=io.StringIO(newline='');w=csv.DictWriter(f,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows);return f.getvalue()


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('--gmd-zip',type=Path);a=p.parse_args()
    if a.gmd_zip:
        measured=measure_gmd(a.gmd_zip);validate_observation(measured)
        if a.write:OBS.write_text(json.dumps(measured,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        elif measured!=json.loads(OBS.read_text(encoding='utf8')):raise SystemExit('GMD observation stale')
    rows=audit();text=render(rows)
    if a.write:MATRIX.write_text(text,encoding='utf8')
    if a.check and MATRIX.read_text(encoding='utf8')!=text:raise SystemExit('Corpus matrix stale')
    print(json.dumps({'corpus_cases':len(rows),'OPEN':len(rows),'human_approvals':0,'local_gmd_observation':True}))


if __name__=='__main__':main()
