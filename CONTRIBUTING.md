# Contributing

Use Python 3.10+ with the standard library. Keep fixtures synthetic and addresses under `example.test`. Do not add email credentials, real transport, customer messages, or personal data.

For changes:

1. Work on a branch and describe the concrete requirement or defect.
2. Add meaningful negative-path tests for changed controls.
3. Run `python -m unittest discover -s tests -v`.
4. Run `python -m email_gate.demo` if runtime or recovery behavior changed.
5. Update requirements, sample evidence and documented claim limits when affected.
6. Submit a pull request with validation results and material limitations.

Use `DL-###` for material decision logs. A passing run does not itself justify a broader assurance claim. Public release is a separate decision by Grace Adjeli.
