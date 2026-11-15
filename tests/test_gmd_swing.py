import json
import unittest
from scripts.audit_gmd_swing import OUTPUT,components,validate


class GmdSwingTests(unittest.TestCase):
    def test_positive_literal_bow_and_pedal(self):
        result=components([0,1,2,3,4],{51:[0,1,2,3],44:[1,3]},.04)
        self.assertTrue(result['joint_bow_pedal'])

    def test_published_edge_is_family_not_literal_bow(self):
        result=components([0,1,2,3,4],{59:[0,1,2,3],44:[1,3]},.04)
        self.assertTrue(result['joint_family_pedal'])
        self.assertFalse(result['joint_bow_pedal'])

    def test_ride_alone_is_not_joint(self):
        self.assertFalse(components([0,1,2,3,4],{51:[0,1,2,3]},.1)['joint_bow_pedal'])

    def test_next_bar_onset_cannot_fill_current_bar(self):
        self.assertFalse(components([0,1,2,3,4],{51:[0,1,2,4],44:[1,3]},.1)['joint_bow_pedal'])

    def test_unrelated_tom45_is_not_ride(self):
        self.assertFalse(components([0,1,2,3,4],{45:[0,1,2,3],44:[1,3]},.1)['joint_family_pedal'])

    def test_changed_source_hash_rejected(self):
        d=json.loads(OUTPUT.read_text(encoding='utf8'));validate(d)
        d['records'][0]['midi_sha256']='0'*64
        with self.assertRaises(ValueError):validate(d)

    def test_changed_recording_id_rejected(self):
        d=json.loads(OUTPUT.read_text(encoding='utf8'));d['records'][0]['recording_id']='UNRELATED'
        with self.assertRaises(ValueError):validate(d)

    def test_premature_harmony_or_human_acceptance_rejected(self):
        for key,value in [('harmonic_pairing_verified',True),('exact_pat012_verified',True),('human_approval','PASS')]:
            d=json.loads(OUTPUT.read_text(encoding='utf8'));d[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):validate(d)


if __name__=='__main__':unittest.main()
