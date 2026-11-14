"""Review examples have concrete notes; rendering never grants human acceptance."""
import tempfile
from pathlib import Path
from hashlib import sha256
import wave
import unittest
from unittest.mock import patch
from scripts import render_graph_followup_examples as render


class GraphReviewStimuliTests(unittest.TestCase):
    def test_explicit_comparison_uses_identical_source_and_distinct_targets(self):
        cases=render.examples()
        self.assertEqual(len(cases),7)
        arp=cases['P07_COMPLETE_ARPEGGIO']['events']
        self.assertEqual(sum(e[3]==0 for e in arp),4)
        self.assertEqual(sum(e[3]==1 for e in arp),32)
        a,b=cases['ORACLE_GLOBAL_MIN'],cases['ORACLE_DROP2_MIN']
        self.assertEqual(a['events'][:4],b['events'][:4])
        self.assertNotEqual(a['events'][4:],b['events'][4:])
        self.assertEqual(sum(abs(x[2]-y[2]) for x,y in zip(a['events'][:4],a['events'][4:])),3)
        self.assertEqual(sum(abs(x[2]-y[2]) for x,y in zip(b['events'][:4],b['events'][4:])),7)

    def test_existing_material_and_invalid_tempo_are_rejected_before_rendering(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'manifest.json';path.write_text('existing human review',encoding='utf-8')
            with self.assertRaises(FileExistsError):render.render(directory)
            self.assertEqual(path.read_text(encoding='utf-8'),'existing human review')
            for tempo in [0,-1,float('nan')]:
                with self.assertRaises(ValueError):render.render(directory,tempo)

    def test_render_saves_source_snapshot_and_keeps_acceptance_open(self):
        case={'probe_ids':['CONTROL'],'ticks':48,'events':[[0,40,60,1]]}
        with tempfile.TemporaryDirectory() as directory,patch.object(render,'examples',return_value={'control':case}):
            result=render.render(directory,120)
            root=Path(directory)
            digest=sha256((root/'source-plan.json').read_bytes().replace(b'\r\n',b'\n')).hexdigest()
            self.assertEqual(digest,result['source_plan_lf_sha256'])
            self.assertEqual(result['human_approvals'],0)
            self.assertFalse(result['examples'][0]['historical_transcription'])
            self.assertEqual(result['examples'][0]['human_listen_play_approval'],'AUSSTEHEND')
            with wave.open(str(root/'control.wav'),'rb') as sound:
                self.assertAlmostEqual(sound.getnframes()/sound.getframerate(),0.05,places=3)
