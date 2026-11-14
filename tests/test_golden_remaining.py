"""Guard original identity, bounded models, source bytes and unresolved decisions."""
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from scripts import audit_golden_remaining as audit


class RemainingGoldenTests(unittest.TestCase):
    def setUp(self):
        self.plan=json.loads((audit.ROOT/audit.PLAN).read_text(encoding='utf-8'))
        self.cases=json.loads((audit.ROOT/'knowledge/research/golden_cases/golden_reference_cases.json').read_text(encoding='utf-8'))

    def test_complete_64_case_matrix_reproduces_without_original_acceptance(self):
        rows=audit.audit(self.plan,self.cases)
        self.assertEqual(len(rows),64)
        self.assertFalse(any(r['model_status']=='FAIL' for r in rows))
        self.assertTrue(all(r['human_review']=='AUSSTEHEND' and not r['production_use_allowed'] for r in rows))
        self.assertEqual(audit.render(rows),(audit.ROOT/audit.MATRIX).read_text(encoding='utf-8'))

    def test_missing_case_and_changed_original_are_rejected(self):
        self.plan['reviews'].pop()
        with self.assertRaises(ValueError):audit.validate(self.plan,self.cases)
        self.setUp()
        next(c for c in self.cases if c['case_id']=='REF-0017')['expected_output']='G -> C'
        with self.assertRaises(ValueError):audit.validate(self.plan,self.cases)

    def test_original_contradiction_cannot_hide_behind_model_pass(self):
        row=next(r for r in self.plan['reviews'] if r['case_id']=='REF-0017')
        self.assertEqual(audit.calculate(row['model']['kind'],row['model']['input']),['G','C'])
        row['original_assessment']='SUPPORTED_BY_ORIGINAL_INPUT'
        with self.assertRaises(ValueError):audit.validate(self.plan,self.cases)

    def test_fabricated_human_or_production_acceptance_rejected(self):
        for field,value in [('human_review','APPROVED'),('production_use_allowed',True)]:
            altered=copy.deepcopy(self.plan);altered['reviews'][0][field]=value
            with self.assertRaises(ValueError):audit.validate(altered,self.cases)

    def test_wrong_expected_model_is_a_failure(self):
        self.plan['reviews'][0]['model']['expected']['same_spelling']=True
        self.assertEqual(audit.audit(self.plan,self.cases)[0]['model_status'],'FAIL')

    def test_diatonic_spelling_and_sounding_class_are_distinct(self):
        self.assertEqual(audit.calculate('diatonic',{'note':'Db4','scale':['D4','E4','F#4','G4','A4','B4','C#5']}),
                         {'written_degree':None,'pc_present':True})

    def test_same_sounding_notes_do_not_allow_wrong_xml_spelling(self):
        with self.assertRaises(ValueError):
            audit.calculate('xml',{'names':['C#4','Db4'],'pitches':[
                '<pitch><step>C</step><alter>1</alter><octave>4</octave></pitch>',
                '<pitch><step>C</step><alter>1</alter><octave>4</octave></pitch>']})

    def test_named_upper_structures_reject_conflicting_pitch_lists(self):
        row=next(r for r in self.plan['reviews'] if r['case_id']=='REF-0152')
        data=copy.deepcopy(row['model']['input']);data['declared_upper']=[2,5,9]
        with self.assertRaises(ValueError):audit.calculate('upper_structure',data)

    def test_negative_swing_and_invalid_family_are_rejected(self):
        with self.assertRaises(ValueError):audit.calculate('swing_regression',{'slope':0.01,'intercept':1,'bpm':[100]})
        with self.assertRaises(ValueError):audit.calculate('families',{'families':[[2,2,2,2,2,2,2]]})

    def test_source_original_bytes_are_not_repaired_in_place(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            shutil.copytree(audit.ROOT/audit.ARCHIVE.parent,root/audit.ARCHIVE.parent)
            manifest=json.loads((root/audit.ARCHIVE).read_text(encoding='utf-8'))
            path=root/manifest['records'][0]['archive_path']
            path.write_bytes(path.read_bytes()+b'\nchanged')
            with self.assertRaises(ValueError):audit.verify_archives(root)

    def test_source_path_cannot_escape_preserved_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            shutil.copytree(audit.ROOT/audit.ARCHIVE.parent,root/audit.ARCHIVE.parent)
            manifest=json.loads((root/audit.ARCHIVE).read_text(encoding='utf-8'))
            manifest['records'][0]['archive_path']='outside.md'
            (root/audit.ARCHIVE).write_text(json.dumps(manifest),encoding='utf-8')
            with self.assertRaises(ValueError):audit.verify_archives(root)
