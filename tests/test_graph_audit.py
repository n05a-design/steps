"""Counterchecks for complete graph review and separation of evidence boundaries."""

from copy import deepcopy
import json
import unittest

from scripts import audit_graph, graph_probes


class GraphAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan=json.loads((audit_graph.ROOT/audit_graph.PLAN).read_text(encoding='utf-8'))
        cls.relations=audit_graph.read_csv(audit_graph.ROOT/'knowledge/relations/MUSIC_CONCEPT_RELATIONS.csv')

    def test_every_original_has_a_review_but_no_human_approval(self):
        rows,probes=audit_graph.audit()
        self.assertEqual(len(rows),97)
        self.assertEqual({r['relation_id'] for r in rows},{r['relation_id'] for r in self.relations})
        self.assertTrue(all(r['human_review']=='AUSSTEHEND' and not r['production_use_allowed'] for r in rows))
        self.assertEqual(next(r for r in rows if r['relation_id']=='CDR-010')['relation_status'],'FAIL')
        self.assertEqual(len(probes),40)
        self.assertTrue(all(p['status']=='PASS' for p in probes.values()))

    def test_missing_duplicate_changed_edges_and_approval_forgery_fail(self):
        for mutation in ['missing','duplicate','original','approval','source_approval','unknown_claim']:
            altered=deepcopy(self.plan)
            if mutation=='missing':altered['reviews'].pop()
            elif mutation=='duplicate':altered['reviews'][-1]=altered['reviews'][0]
            elif mutation=='original':altered['reviews'][0]['edge']['target_id']='OTHER'
            elif mutation=='approval':altered['reviews'][0]['human_review']='APPROVED'
            elif mutation=='source_approval':altered['reviews'][0]['source_assertion_verified']=True
            else:altered['reviews'][0]['candidate_claim_ids']=['CLAIM-999']
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):
                audit_graph.validate(altered,self.relations)

    def test_wrong_expected_outputs_fail_for_every_probe(self):
        for original in self.plan['probes']:
            altered=deepcopy(original);altered['expected']=None
            with self.subTest(probe=original['id']),self.assertRaises(ValueError):
                graph_probes.evaluate(altered)

    def test_publisher_notation_is_scoped_and_not_human_acceptance(self):
        rows,_=audit_graph.audit()
        row=next(r for r in rows if r['relation_id']=='CDR-018')
        self.assertEqual(row['source_assertion_status'],'CURRENT_PRIMARY_NOTATION_SCOPED_CHECK')
        self.assertEqual(row['human_review'],'AUSSTEHEND')
        altered=deepcopy(self.plan)
        next(r for r in altered['reviews'] if r['relation_id']=='CDR-018')['scoped_source_evidence']['url']=''
        with self.assertRaises(ValueError):audit_graph.validate(altered,self.relations)

    def test_clave_direction_and_meter_are_not_interchangeable(self):
        original=next(p for p in self.plan['probes'] if p['id']=='SON_CLAVE_PUBLISHER_480')
        for bars in [[[2,3],[1,2.5,4]],[[1,2.5,5],[2,3]]]:
            altered=deepcopy(original);altered['input']['bars']=bars
            with self.assertRaises(ValueError):graph_probes.evaluate(altered)

    def test_piano_draft_rejects_foreign_pitch_and_invalid_timeline(self):
        original=next(p for p in self.plan['probes'] if p['id']=='NEW_PIANO_DRAFT')
        for field,value in [(2,'F#4'),(1,-120),(0,99999)]:
            altered=deepcopy(original);altered['input']['events'][0][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):graph_probes.evaluate(altered)

    def test_input_mutations_reach_actual_calculation(self):
        by_id={p['id']:p for p in self.plan['probes']}
        for ident,key,value in [('SAME_ROOT_SHIFT','symbols',['D7','Dm']),('L1','to',[59,61,67]),
                                ('MOD12','midi',[0,12,60,61,126]),('SWING64','percent',63),
                                ('METRIC_DUALITY','slow_bpm',88),('POLYRHYTHM','periods',[3,5])]:
            altered=deepcopy(by_id[ident]);altered['input'][key]=value
            with self.subTest(probe=ident),self.assertRaises(ValueError):graph_probes.evaluate(altered)

    def test_bad_model_probe_cannot_turn_relation_green(self):
        plan=deepcopy(self.plan);probe=next(p for p in plan['probes'] if p['id']=='MOD12')
        probe['expected']=[99]
        rows,_=audit_graph.audit(plan=plan)
        row=next(r for r in rows if r['relation_id']=='CR-003')
        self.assertEqual(row['technical_status'],'FAIL')
        self.assertEqual(row['relation_status'],'OPEN')

    def test_node_proposals_cannot_close_historical_definition_or_approve_production(self):
        original=json.loads((audit_graph.ROOT/'knowledge/relations/NODE_DEFINITION_PROPOSALS.json').read_text(encoding='utf-8'))
        ids={r['historical_node_id'] for r in original['proposals']}
        probes={p['id'] for p in self.plan['probes']}
        for field,value in [('historical_definitions_resolved',True),('production_use_allowed',True),('status','APPROVED')]:
            altered=deepcopy(original);altered[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):
                audit_graph.validate_proposals(altered,self.relations,probes,ids)

    def test_node_proposals_require_all_six_original_ids_and_their_edges(self):
        original=json.loads((audit_graph.ROOT/'knowledge/relations/NODE_DEFINITION_PROPOSALS.json').read_text(encoding='utf-8'))
        ids={r['historical_node_id'] for r in original['proposals']}
        for mutation in ['missing','edge']:
            altered=deepcopy(original)
            if mutation=='missing':altered['proposals'].pop()
            else:altered['proposals'][0]['relation_ids']=['CDR-001']
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):
                audit_graph.validate_proposals(altered,self.relations,{p['id'] for p in self.plan['probes']},ids)
