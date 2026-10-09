from dataclasses import replace
import json
from pathlib import Path
import unittest
from .core import Email, Gate, digest
from .recovery import Claim, Retest

def main():
    email = Email('assistant@example.test', ('client@example.test',), 'Update', 'Synthetic draft')
    gate = Gate()
    approval = gate.approve(email, 'human-reviewer', 100)
    altered = replace(email, to=('reviewer@example.test',))
    condition = {'original': email.fingerprint, 'altered': altered.fingerprint, 'time': 101,
                 'policy_hash': gate.policy.fingerprint, 'expected': 'HUMAN_REVIEW'}
    # Deliberately defective fixture: tests approval presence only, omitting payload binding.
    def defective_fixture(approval_present):
        return 'PERMIT' if approval_present else 'BLOCK'
    actual = defective_fixture(True)
    claim = Claim('CTRL-PAYLOAD-01', 'Altered recipient under recorded synthetic condition')
    claim.fail(condition, 'HUMAN_REVIEW', actual, digest('approval-presence-only fixture'))
    corrected_hash = digest(Path(__file__).with_name('core.py').read_text())
    claim.correct(corrected_hash)
    result = gate.execute(altered, approval, 101)
    suite = unittest.defaultTestLoader.discover('tests')
    regression = unittest.TextTestRunner(verbosity=0).run(suite)
    # Hash exact test sources; stdout records suite result, not independent certification.
    regression_hash = digest({p.name: p.read_text() for p in sorted(Path('tests').glob('test_*.py'))})
    claim.retest(Retest(corrected_hash, digest(condition), regression_hash,
                        result['decision'] != actual, result['decision'] == 'HUMAN_REVIEW', regression.wasSuccessful()))
    claim.restore('designated-reviewer', corrected_hash)
    gate.execute(email, approval, 102)
    print(json.dumps({'scope': 'Synthetic single-process exercise; reviewer simulated',
                      'regression': {'tests_run': regression.testsRun, 'passed': regression.wasSuccessful(),
                                     'test_source_hash': regression_hash},
                      'assurance_events': claim.events, 'runtime_events': gate.events}, indent=2))
if __name__ == '__main__':
    main()
