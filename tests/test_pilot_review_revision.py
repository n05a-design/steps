"""A vanished merge ref may only fall back to the exact completed merge."""
import subprocess
import unittest
from scripts.resolve_pilot_review_revision import resolve


class PilotReviewRevisionTests(unittest.TestCase):
    base='a'*40
    head='b'*40
    merge='c'*40

    def record(self,**extra):
        return dict(number=60,state='closed',merged=True,base={'sha':self.base},head={'sha':self.head},merge_commit_sha=self.merge,**extra)

    def fetch_missing_ref(self,ref):
        if ref.startswith('refs/'):raise subprocess.CalledProcessError(128,['git','fetch'])
        self.assertEqual(ref,self.merge);return self.merge

    def test_live_merge_ref_uses_no_api_fallback(self):
        def no_api(n):self.fail('Live merge ref must not require completed PR API')
        self.assertEqual(resolve(60,self.base,self.head,lambda ref:self.merge,no_api,lambda rev:[self.base,self.head]),self.merge)

    def test_exact_completed_merge_is_admissible(self):
        self.assertEqual(resolve(60,self.base,self.head,self.fetch_missing_ref,lambda n:self.record(),lambda rev:[self.base,self.head]),self.merge)

    def test_open_or_closed_unmerged_pr_cannot_bypass_gate(self):
        for change in [{'state':'open','merged':False},{'merged':False}]:
            record=self.record();record.update(change)
            with self.assertRaises(ValueError):resolve(60,self.base,self.head,self.fetch_missing_ref,lambda n:record,lambda rev:[self.base,self.head])

    def test_changed_head_base_or_pr_identity_rejected(self):
        for change in [{'head':{'sha':'d'*40}},{'base':{'sha':'d'*40}},{'number':61}]:
            record=self.record();record.update(change)
            with self.assertRaises(ValueError):resolve(60,self.base,self.head,self.fetch_missing_ref,lambda n:record,lambda rev:[self.base,self.head])

    def test_wrong_parent_order_and_squash_commit_rejected(self):
        for parents in [[self.head,self.base],[self.base],['d'*40,self.head]]:
            with self.assertRaises(ValueError):resolve(60,self.base,self.head,lambda ref:self.merge,lambda n:self.record(),lambda rev:parents)

    def test_api_merge_commit_must_match_fetched_object(self):
        def wrong(ref):
            if ref.startswith('refs/'):raise subprocess.CalledProcessError(128,['git','fetch'])
            return 'd'*40
        with self.assertRaises(ValueError):resolve(60,self.base,self.head,wrong,lambda n:self.record(),lambda rev:[self.base,self.head])

    def test_api_and_fetch_failures_are_not_silently_accepted(self):
        def fail_api(n):raise subprocess.CalledProcessError(1,['gh','api'])
        with self.assertRaises(subprocess.CalledProcessError):resolve(60,self.base,self.head,self.fetch_missing_ref,fail_api,lambda rev:[self.base,self.head])

    def test_invalid_identifiers_rejected_before_fetch(self):
        for number,base,head in [(0,self.base,self.head),(True,self.base,self.head),(60,'main',self.head),(60,self.base,'x'*40)]:
            with self.assertRaises(ValueError):resolve(number,base,head,lambda ref:self.merge,lambda n:self.record(),lambda rev:[self.base,self.head])


if __name__=='__main__':unittest.main()
