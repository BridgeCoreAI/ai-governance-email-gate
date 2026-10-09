# Evidence guide

Run `python -m unittest discover -s tests -v` and `python -m email_gate.demo` from the root. The demo executes the regression suite and prints JSON containing runtime and assurance events. Sample output is in `sample-evidence.json`.

## Interpret the fields

| Field | Meaning and limit |
|---|---|
| approval ID | Correlates a trusted in-memory approval with decisions; not authentication |
| payload hash | SHA256 of canonical JSON payload representation; not a signature |
| policy hash | Binds complete policy content, not merely its version label |
| code version | Human-readable runtime label; source hash in recovery identifies exact core source |
| correction/code hash | SHA256 of `core.py` used for the recovery retest |
| condition hash | Identifies the recorded original/altered payload, time, expected result and policy condition |
| test source hash | Identifies exact test-source text used in the regression exercise |
| regression result | Local runner count and success result; trusted runner input |
| simulated receipt | Evidence that the demonstrator recorded execution; no email was delivered |
| restoration reviewer | Synthetic role string; not authenticated approval |

## Assess a run

1. Confirm the scenario, expected result, actual gate reason and absence/presence of receipt.
2. Compare approval and executed payload/policy fingerprints.
3. For recovery, inspect invalidation before correction, retest evidence before review, and correction hash matching the simulated deployed hash.
4. Check the original failing condition and regression result, rather than treating another run as sufficient.
5. Bind your conclusion to the recorded condition and source/test versions.

The fixture deliberately omits payload binding; it is not a patched production deployment. The recovery model validates linkage of trusted test results, not the truthfulness of arbitrary submitted reports. No independent auditor or reviewer participated. Logs are mutable in-memory data exported as JSON.

**Conclusion strength must not exceed evidence strength.**

## Download fresh GitHub run evidence

Open **Actions → Control tests → the completed run**. In the summary's **Artifacts** section, download the archive for Python 3.10 or 3.12. Each contains:

- `evidence-run.json`: fresh synthetic demo output.
- `evidence-manifest.json`: tested commit, workflow run and attempt, Python version, and SHA256 of the evidence file.

Artifacts are retained for 30 days and access follows repository permissions. A pull-request run's tested commit can be GitHub's temporary merge commit; the manifest records the actual checkout SHA. Re-running jobs tests that run's existing commit, not automatically the newest branch commit. A rerun generates a new attempt-specific artifact. Hashes help detect changes; they do not certify results independently.
