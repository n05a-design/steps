import json
import unittest
from scripts.audit_gmd_pop_pattern import OUTPUT,components,validate


class PopPatternTests(unittest.TestCase):
    def test_additional_kick_is_not_shifted_replacement(self):
        c=components([0,1,2,3,4],{36:[0,2,2.75]},.04)
        self.assertTrue(c['additional_kick_grid'])
        self.assertFalse(c['shifted_kick_without_beat3'])

    def test_shifted_replacement_is_not_additional_kick(self):
        c=components([0,1,2,3,4],{36:[0,2.75]},.04)
        self.assertTrue(c['shifted_kick_without_beat3'])
        self.assertFalse(c['additional_kick_grid'])

    def test_literal_hat_does_not_silently_accept_edge(self):
        c=components([0,1,2,3,4],{22:[i/2 for i in range(8)]},.04)
        self.assertTrue(c['hat_family42_22'])
        self.assertFalse(c['literal_hat42'])

    def test_snare_rim_is_not_literal_head38(self):
        self.assertFalse(components([0,1,2,3,4],{40:[1,3]},.1)['literal_snare38'])

    def test_complete_literal_additional_candidate(self):
        c=components([0,1,2,3,4],{36:[0,2,2.75],38:[1,3],42:[i/2 for i in range(8)]},.04)
        self.assertTrue(c['additional_joint_literal'])

    def test_changed_member_hash_rejected(self):
        d=json.loads(OUTPUT.read_text(encoding='utf8'));validate(d)
        d['records'][0]['midi_sha256']='0'*64
        with self.assertRaises(ValueError):validate(d)

    def test_human_or_harmony_approval_cannot_be_inferred(self):
        for key,value in [('harmonic_pairing_verified',True),('human_approval','PASS')]:
            d=json.loads(OUTPUT.read_text(encoding='utf8'));d[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):validate(d)

    def test_forbidden_note_makes_shift_nonmonotonic(self):
        notes={36:[0,2.08,2.75]}
        self.assertTrue(components([0,1,2,3,4],notes,.04)['shifted_kick_without_beat3'])
        self.assertFalse(components([0,1,2,3,4],notes,.1)['shifted_kick_without_beat3'])


if __name__=='__main__':unittest.main()
