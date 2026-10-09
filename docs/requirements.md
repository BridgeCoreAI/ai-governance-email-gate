# Control requirements and acceptance criteria

Scope: synthetic single-process email execution gate, version 0.1.0.

| ID | Requirement | Acceptance evidence |
|---|---|---|
| CTRL-01 | Require a trusted approval record from a permitted human approver | Unknown IDs block; unpermitted approver cannot create approval |
| CTRL-02 | Bind the exact sender, To/CC/BCC, subject, body, attachment filenames and content hashes | Any tested field change yields HUMAN_REVIEW and zero receipts |
| CTRL-03 | Check revocation, current approver permissions, expiry and policy content at execution | Revoked/removed authority blocks; expiry/config change requires review |
| CTRL-04 | Enforce recipient allowlist and synthetic-data classification | Even an approved unpermitted recipient blocks; non-synthetic classification blocks |
| CTRL-05 | Consume approval once on successful simulated execution | Repeated use yields no second receipt |
| CTRL-06 | Record linked approval, gate decision and simulated receipt | Identifiers and payload/policy fingerprints correlate |
| CTRL-07 | Invalidate an affected control claim after detected failure | Failure records condition, expected/actual result and affected code hash |
| CTRL-08 | Require matching correction and same-condition retest plus regression | Wrong condition/version is rejected; failed regressions invalidate |
| CTRL-09 | Require simulated designated review and matching deployed hash before restoration | Early restoration, wrong reviewer or wrong deployed hash rejected |

HUMAN_REVIEW is a non-executing outcome. Reassessment and a new approval occur explicitly. Restored assurance is a bounded control claim, not permission to act.

Production requirements outside this exercise include authenticated principals, trusted clocks/classification, hashing actual attachments, durable transactional approval consumption, non-bypassable transport integration, independently protected evidence, and operational review authority.
