# Validator B Blind Summary

Status: `BLIND VALIDATOR B IMPLEMENTATION COMPLETE`

Validator B 0.1.0 independently implements the frozen Semantic Portable Document Format 0.1 Draft in Python. The blind run was frozen before any Validator A result or oracle was inspected.

## Completion gate

- Frozen Draft SHA-256: `fe649e74f8ea57b993f3fece4373efdb105ac2013812e74152270fe4666db849`
- Requirements SHA-256: `a6a6ec7f6a0d1585ed5cc11a9dec3489540117257c3562a758b533b6624d137a`
- Canonical schemas: 6/6 parsed and Draft 2020-12 meta-validated
- Requirements represented: 113/113
- Automated executable coverage: 74/74
- Tests: 37 passed
- Fixtures executed: 69/69
- Internal errors: 0
- SPEC blockers: 0
- Blind results SHA-256: `c16a844aa04820c06c1f2de3d32dd9ca14679c94b78e2d716f2a087fff45b42c`

## Blind result distribution

- Operational: 69 `TOOL_UNAVAILABLE` because EPUBCheck 5.3.0 was not configured.
- Base: 30 `FAIL`, 39 `NOT_TESTED`.
- Mapping: 15 `FAIL`, 9 `NOT_TESTED`, 45 `NOT_CLAIMED`.
- Accessible: 1 `NOT_TESTED`, 68 `NOT_CLAIMED`.

Missing EPUBCheck never becomes document `FAIL`; it contributes `SPD-BASE-002 = NOT_TESTED`. Independently established SPD-native failures remain in each result.

## Independent-interpretation observation

The permitted corpus manifest labels `valid/multi-spine` as valid, but its two authoritative spine documents both use Node ID `n_article01`. Draft sections 13–14 require Node IDs to be unique in the current authoritative semantic revision, so Validator B freezes `SPD-ID-006 = FAIL` for that package. This is recorded as a blind corpus-metadata disagreement for later differential investigation, not optimized away and not classified as a Draft `SPEC_BLOCKER`.

No individual `expected.json` result and no Validator A result was used to change validation behavior.

## Environment

- Python: 3.13.3
- Unicode data: 15.1.0
- Classification: `IMPLEMENTATION_ENVIRONMENT_DIFFERENCE`
- Corpus impact: `NO_OBSERVED_CORPUS_IMPACT`
- EPUBCheck: `TOOL_UNAVAILABLE` (target remains 5.3.0)
- Previous bootstrap stop: `RESOLVED_EXPERIMENT_BOOTSTRAP_DEFINITION_ERROR`

