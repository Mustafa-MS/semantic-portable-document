# Format 0.1 Release Candidate preparation gate

READY FOR FORMAT 0.1 RELEASE CANDIDATE PREPARATION

This gate authorizes no rename or release. Format remains **Format 0.1 Draft**. RC1 preparation is a separate task.

## Required gates

| Gate | Evidence | Result |
| --- | --- | --- |
| Open normative specification blockers | 0 | PASS |
| A ↔ B normative surface | 70/70 | PASS |
| A ↔ independently reviewed oracle | 70/70 | PASS |
| B ↔ independently reviewed oracle | 70/70 | PASS |
| Fixture identity and exact bytes | 70/70; package and expectation SHA-256 verified | PASS |
| Valid multi-spine | Base PASS in both; no failures; EPUBCheck exit 0 | PASS |
| Cross-spine duplicate | Base FAIL, exactly SPD-ID-006 in both; EPUBCheck exit 0 | PASS |
| Stale Mapping attribution | STATE-007; no STATE-001 anywhere in document profile | PASS |
| Unknown descriptor authority | UNKNOWN, not empty/NOT_CLAIMED; matching blocked sets | PASS |
| Lifecycle/effects guards | No EDITABLE STATE-002; no non-semantic STATE-003 | PASS |
| Reviewed overlap attribution | RES-003+006, MAP-011+012, resource/projection and state bindings exact | PASS |
| Requirement coverage | Each validator: 113/113 represented, 74/74 automated registered/implemented | PASS |
| Full shared EPUBCheck scope | 70/70 each, version 5.3.0, same policy, zero skipped/operational failures | PASS |
| Validator A checks | fmt, strict clippy, 17 tests, release; 128-input fuzz smoke included | PASS |
| Validator B checks | 57 unit/property/security/integration tests, Ruff, wheel build and installed policy smoke | PASS |
| Repository checks | 21 tests, schemas and 70-package integrity audit | PASS |
| Draft and registry freeze | Both pinned SHA-256 values unchanged | PASS |
| Historical evidence and canonical schemas | 71 protected live files; all 350 archived files verify | PASS |
| Source/input stability | Start/end snapshots equal for each run and rechecked at final gate | PASS |
| Experimental reporting (separate) | 70/70 A↔B↔oracle | PASS |

## Final questions A–M

| Question | Answer |
| --- | --- |
| A. Format Draft changed? | NO. Exact pre/post digest unchanged; no Format semantics changed. |
| B. Corpus fixtures? | 70: 18 valid, 39 invalid, 13 edge. |
| C. Valid multi-spine passes? | YES, both validators and EPUBCheck. |
| D. New duplicate fails ID-006? | YES, exactly that failed ID in both. |
| E. Stale STATE-001 removed? | YES; STATE-007 is used; processor behavior is not inferred. |
| F. Unknown facts remain unknown? | YES; explicit UNKNOWN authority/capabilities, matching NOT_TESTED prerequisites. |
| G. Lifecycle rules guarded? | YES; targeted EDITABLE and resource-effects regressions pass. |
| H. Same EPUBCheck scope? | YES, all 70 packages completed in each validator. |
| I. Same external attribution? | YES, shared Contract 0.1.1 guarded code/message table. |
| J. Every normative field agrees? | YES, 70/70 complete exact agreement. |
| K. Both match independent oracle? | YES, 70/70 each, without oracle generation from validator output. |
| L. Open Format blockers? | NO, zero. |
| M. Experimental convergence? | YES, 70/70 separately; physical presence does not imply claim. |

## Frozen normative inputs

- `spec/FORMAT_0.1_DRAFT.md`: `fe649e74f8ea57b993f3fece4373efdb105ac2013812e74152270fe4666db849`
- `spec/requirements.yaml`: `a6a6ec7f6a0d1585ed5cc11a9dec3489540117257c3562a758b533b6624d137a`

## New validator freezes

| Validator | Versioned immutable freeze | SHA-256 |
| --- | --- | --- |
| A | validator-convergence/freezes/validator-a-0.1.0-draft.2-corpus-0.1.1.json | e4e6dd809b0bc8365a303d8b6c5f57fb108fcd0b756302b60f09f16c67fe3538 |
| B | validator-convergence/freezes/validator-b-0.1.1-corpus-0.1.1.json | edc0dcca3506ec75be97d88a8043cf87b8c3e3b01d53bf524b85da3b9a4c8df1 |

Detailed test commands and exit statuses: `checks.json`; complete outputs: the eight named `.log` files. Coverage registration is retained without reclassifying requirements. Document-only runs do not certify historical lineage, processor behavior, Accessible manual work or experimental PDF conformance. Unicode versions differ (A 17.0.0, B 15.1.0); no fixture behavior differs, and environments are not described as bit-identical.

READY FOR FORMAT 0.1 RELEASE CANDIDATE PREPARATION
