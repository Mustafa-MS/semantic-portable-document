# Validator A final validation summary

## Freeze status

Validator A is frozen as `0.1.0-draft.1` against the frozen Format 0.1 Draft.
The former SPEC_BLOCKER-001 is resolved as `CORPUS_EXPECTATION_ERROR`; the Draft
was not changed and there are **0 open specification blockers**.

## Accessibility oracle correction

`tests/valid/accessible` now expects Base PASS, Accessible NOT_TESTED, and no
violations. This preserves the rule that unresolved required human WCAG
evaluation cannot become PASS and does not turn incomplete certification into
FAIL. Validator accessibility roll-up semantics were not weakened.

## Acceptance gates

- Requirements: **74/74 AUTOMATED implemented**, **22/22
  PARTIALLY_AUTOMATED represented**, **6/6 MANUAL represented**, **11/11
  INFORMATIVE represented**, **113/113 total represented**.
- Corpus: **69/69 Base classifications**, **69/69 exact expected violation-ID
  sets**, and **69/69 complete normalized results** agree.
- Valid: **18/18** Base accepted; Accessible correctly remains NOT_TESTED.
- Invalid: **38/38** rejected/classified for the exact expected reason set.
- Edge: **13/13** classified as expected.
- EPUBCheck production adapter: fresh **31/31** applicable valid/edge packages
  PASS using EPUBCheck 5.3.0, each with exit code 0. The acceptance run exercised
  all 69 packages; the required 31-record evidence is frozen separately.
- Missing EPUBCheck regression: TOOL_UNAVAILABLE + Base NOT_TESTED, never false
  PASS and never document FAIL.
- Digests: Rust resource/projection/JCS golden vectors match the independent
  Python implementation and all valid/edge corpus vectors.
- Unicode/mapping/state: scalar range, emoji, combining-mark, Arabic/RTL,
  geometry, status, current/stale, and SEALED regressions pass.
- Security: the full adapter run exposed and drove correction of an output-pipe
  deadlock; output is now continuously drained with a 1 MiB memory capture cap,
  excess discarded, and timed-out children killed and reaped.
- Static/build gates: cargo fmt, strict clippy, debug tests, report-schema tests,
  release build, coverage checks, and existing Python repository tests pass.
- Fuzz/property: property and malformed-input tests pass; fuzz targets remain
  available for sustained campaigns.

## Frozen reproducibility metadata

- Format Draft SHA-256:
  `fe649e74f8ea57b993f3fece4373efdb105ac2013812e74152270fe4666db849`
- Requirements registry SHA-256:
  `a6a6ec7f6a0d1585ed5cc11a9dec3489540117257c3562a758b533b6624d137a`
- Canonical schema bundle SHA-256:
  `63367445ce68e873e0e478e73aa10e5206d070e9f3af5966e3238befb3bc403f`
- Unicode: `unicode-normalization 0.1.25 / Unicode 16 data`
- EPUBCheck: `5.3.0`

The differential oracle is
`reports/golden/validator-a-0.1.0-draft.1.json`; per-fixture EPUBCheck evidence is
`reports/epubcheck-corpus-results.json`.

PROCEED TO INDEPENDENT VALIDATOR B
