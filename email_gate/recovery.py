"""Bounded assurance-state exercise; reviewer identity is simulated, not authenticated."""
from dataclasses import dataclass
from .core import digest
@dataclass(frozen=True)
class Retest:
    correction_hash: str
    condition_hash: str
    regression_hash: str
    original_failure_absent: bool
    expected_control_fired: bool
    regressions_passed: bool
class Claim:
    def __init__(self, claim_id, scope):
        self.id, self.scope = claim_id, scope
        self.state = 'UNVERIFIED'
        self.events = []
        self.failure_condition = None
        self.correction = None
        self.report = None
    def fail(self, condition, expected, actual, affected_code_hash):
        self.failure_condition = digest(condition)
        self.state = 'INVALIDATED'
        self.correction = self.report = None
        self.events.append({'state': self.state, 'claim': self.id, 'condition_hash': self.failure_condition,
                            'expected': expected, 'actual': actual, 'code_hash': affected_code_hash})
    def correct(self, code_hash):
        if self.state != 'INVALIDATED':
            raise ValueError('Correction requires an invalidated claim')
        self.correction = code_hash
        self.state = 'CORRECTED_PENDING_RETEST'
        self.events.append({'state': self.state, 'code_hash': code_hash})
    def retest(self, report):
        if self.state != 'CORRECTED_PENDING_RETEST':
            raise ValueError('Retest requires correction')
        if report.correction_hash != self.correction or report.condition_hash != self.failure_condition:
            raise ValueError('Evidence does not match correction and original condition')
        if not all((report.original_failure_absent, report.expected_control_fired, report.regressions_passed)):
            self.state = 'INVALIDATED'
            self.events.append({'state': self.state, 'reason': 'RETEST_FAILED'})
            return
        self.report = report
        self.state = 'PENDING_REVIEW'
        self.events.append({'state': self.state, 'evidence_hash': digest(report.__dict__)})
    def restore(self, reviewer, deployed_hash):
        if reviewer != 'designated-reviewer':
            raise PermissionError('Simulated designated reviewer required')
        if self.state != 'PENDING_REVIEW' or deployed_hash != self.correction:
            raise ValueError('Restoration requires reviewed matching-version evidence')
        self.state = 'RESTORED_BOUNDED'
        self.events.append({'state': self.state, 'reviewer': reviewer, 'simulated': True,
                            'code_hash': deployed_hash, 'scope': self.scope})
