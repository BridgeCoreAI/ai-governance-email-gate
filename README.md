# AI Governance Email Gate

**Grace Adjeli | BridgeCore AI**

Episode 6: **Engineering AI Governance** — a bounded Python demonstrator of payload-bound approval, execution-time revalidation, and a simulated assurance restoration lifecycle.

## Run

Python 3.10+; standard library only. Run from the repository root:

```bash
python -m unittest discover -s tests -v
python -m email_gate.demo
```

No credentials, paid model API, or real email account are needed. All addresses use `example.test`. Nothing is transmitted.

## What is implemented

- The approval service records the exact sender, To/CC/BCC, subject, body and attachment filename/content hashes, approver, expiration, and policy fingerprint.
- The separate gate checks the trusted approval record at execution. Missing/revoked/replayed approval blocks; payload/configuration changes and expiry require fresh human review. Recipient permissions and synthetic-data rules are independently enforced.
- Only a permit records a simulated execution receipt. Approval, gate decision and receipt share identifiers and fingerprints.
- The recovery exercise records a deliberately defective approval-presence-only fixture permitting an altered recipient. The affected claim is invalidated, the corrected gate's source hash is bound to the same-condition retest, regressions are run, and a simulated designated reviewer restores a bounded claim.

See [requirements and limitations](docs/design.md) and [sample run evidence](docs/sample-evidence.json). The sample was generated locally; run it yourself to reproduce behavior. UUIDs vary.

## Claim limits

18 unit tests passed locally. This establishes tested behavior in a synthetic single-process exercise, not enterprise assurance, message accuracy, delivery, authenticated human approval, or independent certification. The recovery fixture represents a known omitted check, not a historical production incident or deployed patch. Restoration is simulated and never authorizes the next email.

The AI assistant is represented by a proposed email object; a live model is unnecessary to test this boundary.

## License

Apache License 2.0. See LICENSE. BridgeCore AI branding is not licensed by the software license.

**Governance is not what is defined. It is what is enforced at execution.**

Grace Adjeli
