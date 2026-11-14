"""Written chart, original/derived lanes and remote-archive evidence stay separate."""
from copy import deepcopy
import json
import unittest
from scripts import audit_jazzsamba_components as j


class JazzComponentTests(unittest.TestCase):
    def row(self,**changes):
        row={k:'False' for k in j.EXTENSIONS+j.ALTERATIONS}
        row.update(is_no_chord='False',root='D',triad='min',seventh='min',is_slash='False',start_time='0',end_time='1')
        row.update(changes);return row

    def test_structured_seventh_quality_is_preserved(self):
        self.assertEqual(j.chart_shape(self.row(),'exact'),(2,'min7'))
        self.assertEqual(j.chart_shape(self.row(root='G',triad='maj',seventh='dom'),'exact'),(7,'7'))

    def test_extensions_are_only_ignored_in_explicit_projection(self):
        row=self.row(has_9='True')
        self.assertIsNone(j.chart_shape(row,'exact'))
        self.assertEqual(j.chart_shape(row,'triad_projection'),(2,'min'))

    def test_altered_triads_are_not_plain_major_minor(self):
        self.assertIsNone(j.chart_shape(self.row(alt_b5='True'),'triad_projection'))
        self.assertIsNone(j.chart_shape(self.row(is_no_chord='True'),'exact'))

    def test_terminal_zero_duration_is_explicitly_excluded(self):
        runs,excluded=j.chart_segments([self.row(),self.row(start_time='1',end_time='1')],'exact')
        self.assertEqual(excluded,1);self.assertEqual(len(runs),1)

    def test_nonterminal_zero_and_overlap_are_not_repaired(self):
        for rows in [[self.row(end_time='0'),self.row()], [self.row(end_time='2'),self.row(start_time='1',end_time='3')]]:
            with self.assertRaises(ValueError):j.chart_segments(rows,'exact')

    def test_bar_fraction_and_seconds_share_one_axis(self):
        bars=[{'bar':'0','start_time':'0','end_time':'4'}]
        row={'start_bar':'0','end_bar':'1','start_fraction':'.5','end_fraction':'0','start_time':'2','end_time':'4'}
        self.assertEqual(j.check_bar_grid([row],bars),0)

    def test_unrelated_time_axis_and_unknown_bar_rejected(self):
        bars=[{'bar':'0','start_time':'0','end_time':'4'}]
        for row in [{'start_bar':'0','end_bar':'0','start_fraction':'0','end_fraction':'.5','start_time':'1','end_time':'2'},
                    {'start_bar':'3','end_bar':'3','start_fraction':'0','end_fraction':'.5','start_time':'0','end_time':'2'}]:
            with self.assertRaises(ValueError):j.check_bar_grid([row],bars)

    def test_chart_and_pattern_are_not_performed_harmony_acceptance(self):
        d=json.loads(j.OUTPUT.read_text(encoding='utf8'));j.validate(d)
        self.assertEqual(d['selected_songs'],18)
        self.assertEqual(d['chart_origin'],'TIMED_LEAD_SHEET_NOT_PERFORMED_HARMONY_TRANSCRIPTION')
        self.assertFalse(d['exact_ride_pedal_pattern_verified'])

    def test_faked_full_archive_or_human_approval_rejected(self):
        for change in [{'source_archive_full_md5_verified':True},{'human_approval':'PASS'},{'historical_assertion_closed':True}]:
            d=json.loads(j.OUTPUT.read_text(encoding='utf8'));d.update(change)
            with self.assertRaises(ValueError):j.validate(d)

    def test_automatic_transcription_cannot_be_renamed_original_lane(self):
        d=json.loads(j.OUTPUT.read_text(encoding='utf8'));d['records'][0]['source_members']['drums']['member']='async-derived/songs/x/preferred/drums.mid'
        with self.assertRaises(ValueError):j.validate(d)

    def test_copied_alternate_annotations_are_not_preferred_performance(self):
        d=json.loads(j.OUTPUT.read_text(encoding='utf8'));d['records'][0]['take']='alternate'
        with self.assertRaises(ValueError):j.validate(d)

    def test_wrong_selection_or_denominator_is_rejected(self):
        d=json.loads(j.OUTPUT.read_text(encoding='utf8'));d['records'][0]['song_id']='999'
        with self.assertRaises(ValueError):j.validate(d)
        d=json.loads(j.OUTPUT.read_text(encoding='utf8'));d['summary']['exact']['songs_with_both']+=1
        with self.assertRaises(ValueError):j.validate(d)


if __name__=='__main__':unittest.main()
