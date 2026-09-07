# Contributing to SPD Format 0.1

SPD Format 0.1 RC1 is experimental and is being published specifically for external review. Focused issues, independent implementation reports, and narrowly scoped pull requests are welcome.

## Useful review feedback

- specification language that permits conflicting interpretations;
- independent validator, reader, or editor implementation experience;
- security and passive-content-profile concerns;
- accessibility gaps or manual evaluation findings;
- EPUB 3.3 packaging and reading-system interoperability results; and
- persistent identity, revision, transaction, annotation, or semantic-to-fixed mapping concerns.

Use the most relevant issue label: `spec`, `validator`, `security`, `accessibility`, `interop`, or `editorial`. For suspected vulnerabilities, follow [SECURITY.md](SECURITY.md) instead of opening a public issue.

## Before opening a pull request

1. Open or reference an issue for any normative change. RC1 cleanup must not silently change requirement meaning, schemas, validator behavior, or corpus expectations.
2. Keep editorial corrections separate from normative proposals.
3. Add or update conformance fixtures when a behavior change is eventually accepted.
4. Run the affected validator tests and the repository test suite.
5. State whether the change is editorial, implementation-only, test-only, or normative.

Small typo and broken-link fixes may be submitted directly. A lightweight contributor workflow is intentional at this stage; no formal governance process is implied.

## Licensing

By contributing, you agree that your contribution is licensed under the repository’s applicable split license described in [LICENSE](LICENSE): Apache-2.0 for software/code and CC BY 4.0 for specification/documentation.
