import unittest
from email_gate.core import digest
from email_gate.recovery import Claim, Retest
class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.c = Claim('control-1', 'synthetic test')
        self.c.fail({'change': 'recipient'}, 'REVIEW', 'PERMIT', 'old-code')
        self.c.correct('new-code')
        self.report = Retest('new-code', digest({'change': 'recipient'}), 'tests-hash', True, True, True)
    def test_restore_requires_retest(self):
        with self.assertRaises(ValueError):
            self.c.restore('designated-reviewer', 'new-code')
    def test_evidence_wrong_version(self):
        from dataclasses import replace
        with self.assertRaises(ValueError):
            self.c.retest(replace(self.report, correction_hash='other'))
    def test_evidence_wrong_condition(self):
        from dataclasses import replace
        with self.assertRaises(ValueError):
            self.c.retest(replace(self.report, condition_hash='other'))
    def test_failed_regression(self):
        from dataclasses import replace
        self.c.retest(replace(self.report, regressions_passed=False))
        self.assertEqual(self.c.state, 'INVALIDATED')
    def test_restoration_authority(self):
        self.c.retest(self.report)
        with self.assertRaises(PermissionError):
            self.c.restore('agent', 'new-code')
        with self.assertRaises(ValueError):
            self.c.restore('designated-reviewer', 'other-code')
        self.c.restore('designated-reviewer', 'new-code')
        self.assertEqual(self.c.state, 'RESTORED_BOUNDED')
    def test_new_failure_invalidates_restoration(self):
        self.c.retest(self.report)
        self.c.restore('designated-reviewer', 'new-code')
        self.c.fail({'new': 'condition'}, 'BLOCK', 'PERMIT', 'new-code')
        self.assertEqual(self.c.state, 'INVALIDATED')
        self.assertIsNone(self.c.report)
