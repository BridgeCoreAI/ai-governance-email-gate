# Release checklist

Repository stays private while building. Publication requires Grace Adjeli's explicit decision.

## Technical and evidence verification

- [x] Review final source and documentation for scope accuracy.
- [x] Run all tests on the reviewed commit and review CI results.
- [x] Reproduce the synthetic demo in CI and bind the generated evidence to the tested commit.
- [x] Verify the CI evidence-file SHA256 against the generated evidence artifact.
- [x] Review current repository content and commit history for obvious secrets, credentials, real customer messages, or non-synthetic email data.
- [x] Confirm negative-path scenarios and non-execution outcomes.
- [x] Confirm reviewer/authentication and transport simulations are clearly labeled.
- [x] Check LICENSE, authorship, and BridgeCore AI branding language.
- [x] Review README, architecture, evidence guide, requirements, and claim boundaries for consistency.

## Verified baseline

Reviewed baseline before this checklist update:

- Commit: `d502201c615bf3a160f0cd5fb3b9b7d46758accf`
- GitHub Actions run: `38030183211`
- Python 3.10: 18 tests passed
- Python 3.12: 18 tests passed
- Both matrix jobs generated synthetic evidence and uploaded run-specific evidence artifacts.
- Python 3.12 evidence artifact SHA256: `3641ee2192a1aa1cffd8e646b719817dae09f28c2d5ad72fe227b5791df712d8`
- Generated `evidence-run.json` SHA256: `4896bf389aae6d5c0e8425e269376b87da42551c95b22390d59471d677e2d47d`
- The manifest identifies the exact tested commit and explicitly limits scope to a synthetic demonstrator, not independent assurance.
- The generated evidence records 18 passing regression tests, a bounded invalidation-to-restoration sequence, and simulated—not authenticated—review.

## Claim boundary

The verification above establishes reproducible repository behavior for the reviewed synthetic implementation. It does **not** establish production email delivery, authenticated human identity, independent audit assurance, enterprise control effectiveness, legal compliance, or generalized AI-system safety.

A successful control test or restored bounded claim is not permission for a future action; execution still requires a fresh execution-time gate decision.

## Publication decision — intentionally pending

- [ ] Re-run CI after the final documentation freeze and verify the exact final commit.
- [ ] Revisit LinkedIn/Substack claims against the frozen repository and evidence.
- [ ] Decide whether the repository remains private or becomes public.
- [ ] If public release is approved, perform final visibility review and tag the release.

Episode 6 should describe only the implementation and evidence actually present in the reviewed version.
