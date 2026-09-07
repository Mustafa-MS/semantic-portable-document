# Validator B Blind Freeze Evidence

## Identity and normative inputs

- Validator: Validator B
- Version: 0.1.0
- Format: Semantic Portable Document Format 0.1 Draft
- Format Draft SHA-256: `fe649e74f8ea57b993f3fece4373efdb105ac2013812e74152270fe4666db849`
- Requirements registry SHA-256: `a6a6ec7f6a0d1585ed5cc11a9dec3489540117257c3562a758b533b6624d137a`
- Canonical schema manifest: `validator-b/reports/SCHEMA_INPUT_MANIFEST.json`
- Non-normative Validator-B schema-set digest: `8baf64736240b33c043ecf10fbb75a2dd07cf4db90a421dc0a937d16b3f42a45`

The earlier unverifiable supplied bundle hash is classified `RESOLVED_EXPERIMENT_BOOTSTRAP_DEFINITION_ERROR`. It is not a Format ambiguity, Validator defect, or corpus defect.

## Implementation environment

- Freeze date: 2026-09-03 (Asia/Baghdad)
- Repository commit: unavailable; repository has no resolvable `HEAD`
- Python: 3.13.3
- Unicode data: 15.1.0
- Unicode classification: `IMPLEMENTATION_ENVIRONMENT_DIFFERENCE`
- Unicode impact: `NO_OBSERVED_CORPUS_IMPACT`; see `UNICODE_ENVIRONMENT_IMPACT.md`
- EPUBCheck target: 5.3.0
- EPUBCheck status: `TOOL_UNAVAILABLE`

## Completion evidence

- Requirement coverage: 113/113 represented; 74/74 automated requirements have executable coverage
- Canonical schemas: 6/6 independently loaded and Draft 2020-12 meta-validated
- Tests: 37 passed
- Corpus execution: 69/69 fixtures, zero `INTERNAL_ERROR`
- SPEC blocker count: 0
- Blind results: `validator-b/reports/blind-results.json`
- Blind results SHA-256: `c16a844aa04820c06c1f2de3d32dd9ca14679c94b78e2d716f2a087fff45b42c`

## Independence attestation

Before this freeze:

- no `validator-a/src/` file was accessed;
- no `validator-a/tests/` file was accessed;
- no Validator A executable was accessed or invoked;
- no Validator A golden oracle was accessed;
- no Validator A validation summary was accessed;
- no Validator A internal architecture documentation or implementation-specific coverage file was accessed;
- the explicitly permitted `validator-a/docs/DIFFERENTIAL_VALIDATION_CONTRACT.md` was read only for the normalized comparison surface;
- no individual corpus `expected.json` file was read by Validator B or its blind runner;
- Validator B does not import, wrap, invoke, or reuse Validator A code or output.

The blind implementation and result surface are frozen. Differential comparison has not begun.

