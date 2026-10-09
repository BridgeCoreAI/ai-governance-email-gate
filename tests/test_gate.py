from dataclasses import replace
import unittest
from email_gate.core import Email, Gate, digest
class GateTests(unittest.TestCase):
    def setUp(self):
        self.g = Gate()
        self.e = Email('assistant@example.test', ('client@example.test',), 'Update', 'Synthetic draft', (('report.txt', digest('bytes')),))
        self.a = self.g.approve(self.e, 'human-reviewer', 100)
    def check(self, email=None, approval=None, now=101, expected='BLOCK', reason=None, **kwargs):
        result = self.g.execute(email or self.e, approval or self.a, now, **kwargs)
        self.assertEqual(result['decision'], expected)
        if reason:
            self.assertEqual(result['reason'], reason)
        self.assertEqual(len(self.g.receipts), 1 if expected == 'PERMIT' else 0)
        return result
    def test_approved(self):
        r = self.check(expected='PERMIT')
        self.assertEqual(r['payload_hash'], self.g.receipts[0]['payload_hash'])
    def test_missing(self):
        self.check(approval='unknown', reason='MISSING_APPROVAL')
    def test_changed_fields(self):
        for field, value in {'to': ('reviewer@example.test',), 'cc': ('reviewer@example.test',), 'bcc': ('reviewer@example.test',), 'subject': 'Changed', 'body': 'Changed', 'sender': 'other@example.test', 'attachments': (('report.txt', digest('different bytes')),)}.items():
            with self.subTest(field=field):
                self.check(email=replace(self.e, **{field: value}), expected='HUMAN_REVIEW', reason='PAYLOAD_CHANGED')
    def test_revoked(self):
        self.g.revoke(self.a)
        self.check(reason='REVOKED_AUTHORITY')
    def test_config_without_version_change(self):
        self.g.policy = replace(self.g.policy, ttl=10)
        self.check(expected='HUMAN_REVIEW', reason='CONFIGURATION_CHANGED')
    def test_expiry(self):
        self.check(now=400, expected='HUMAN_REVIEW', reason='EXPIRED_APPROVAL')
    def test_recipient_permission(self):
        e = replace(self.e, to=('outsider@example.test',))
        a = self.g.approve(e, 'human-reviewer', 100)
        self.check(email=e, approval=a, reason='RECIPIENT_NOT_PERMITTED')
    def test_data_rule(self):
        self.check(data_class='confidential', reason='DATA_RULE_DENIED')
    def test_approver(self):
        with self.assertRaises(PermissionError):
            self.g.approve(self.e, 'agent', 100)
    def test_removed_approver(self):
        self.g.policy = replace(self.g.policy, approvers=())
        self.check(reason='REVOKED_AUTHORITY')
    def test_replay(self):
        self.g.execute(self.e, self.a, 101)
        r = self.g.execute(self.e, self.a, 102)
        self.assertEqual(r['reason'], 'APPROVAL_ALREADY_USED')
        self.assertEqual(len(self.g.receipts), 1)
    def test_fresh_approval(self):
        e = replace(self.e, body='Revised')
        a = self.g.approve(e, 'human-reviewer', 101)
        self.check(email=e, approval=a, expected='PERMIT')
