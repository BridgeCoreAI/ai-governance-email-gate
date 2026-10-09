"""Synthetic single-process email gate. No network transport."""
from dataclasses import dataclass, asdict
from uuid import uuid4
import hashlib
import json
VERSION = '0.1.0'
def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
@dataclass(frozen=True)
class Email:
    sender: str
    to: tuple[str, ...]
    subject: str
    body: str
    attachments: tuple[tuple[str, str], ...] = ()
    cc: tuple[str, ...] = ()
    bcc: tuple[str, ...] = ()
    @property
    def fingerprint(self):
        return digest(asdict(self))
@dataclass(frozen=True)
class Policy:
    version: str = 'policy-1'
    sender: str = 'assistant@example.test'
    recipients: tuple[str, ...] = ('client@example.test', 'reviewer@example.test')
    approvers: tuple[str, ...] = ('human-reviewer',)
    ttl: int = 300
    data_rule: str = 'synthetic-only'
    @property
    def fingerprint(self):
        return digest(asdict(self))
@dataclass(frozen=True)
class Approval:
    id: str
    payload: str
    policy: str
    approver: str
    expires: int
class Gate:
    def __init__(self, policy=None):
        self.policy = policy or Policy()
        self._approvals = {}
        self._revoked = set()
        self._used = set()
        self.events = []
        self.receipts = []
    def approve(self, email, approver, now):
        if approver not in self.policy.approvers:
            raise PermissionError('Approver lacks authority')
        a = Approval(str(uuid4()), email.fingerprint, self.policy.fingerprint, approver, now + self.policy.ttl)
        self._approvals[a.id] = a
        self.events.append({'type': 'approval', **asdict(a)})
        return a.id
    def revoke(self, approval_id):
        self._revoked.add(approval_id)
        self.events.append({'type': 'revocation', 'approval_id': approval_id})
    def execute(self, email, approval_id, now, data_class='synthetic'):
        a = self._approvals.get(approval_id)
        decision, reason = 'PERMIT', 'AUTHORIZED'
        if not a:
            decision, reason = 'BLOCK', 'MISSING_APPROVAL'
        elif approval_id in self._revoked or a.approver not in self.policy.approvers:
            decision, reason = 'BLOCK', 'REVOKED_AUTHORITY'
        elif approval_id in self._used:
            decision, reason = 'BLOCK', 'APPROVAL_ALREADY_USED'
        elif now >= a.expires:
            decision, reason = 'HUMAN_REVIEW', 'EXPIRED_APPROVAL'
        elif a.policy != self.policy.fingerprint:
            decision, reason = 'HUMAN_REVIEW', 'CONFIGURATION_CHANGED'
        elif a.payload != email.fingerprint:
            decision, reason = 'HUMAN_REVIEW', 'PAYLOAD_CHANGED'
        elif email.sender != self.policy.sender or not (email.to or email.cc or email.bcc):
            decision, reason = 'BLOCK', 'SENDER_OR_RECIPIENT_INVALID'
        elif any(r not in self.policy.recipients for r in email.to + email.cc + email.bcc):
            decision, reason = 'BLOCK', 'RECIPIENT_NOT_PERMITTED'
        elif data_class != 'synthetic':
            decision, reason = 'BLOCK', 'DATA_RULE_DENIED'
        e = {'type': 'gate_decision', 'decision': decision, 'reason': reason,
             'approval_id': approval_id, 'payload_hash': email.fingerprint,
             'policy_hash': self.policy.fingerprint, 'policy_version': self.policy.version,
             'code_version': VERSION, 'time': now, 'data_class': data_class}
        self.events.append(e)
        if decision == 'PERMIT':
            self._used.add(approval_id)
            receipt = {**e, 'type': 'simulated_execution', 'outcome': 'SIMULATED_ONLY'}
            self.receipts.append(receipt)
            self.events.append(receipt)
        return e
