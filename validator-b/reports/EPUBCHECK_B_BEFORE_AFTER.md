# Validator B Before/After EPUBCheck

This is a B-only external-dependency comparison. No Validator A results or corpus expected-result files were read.

## Preservation

- Original blind-results SHA-256 remains `c16a844aa04820c06c1f2de3d32dd9ca14679c94b78e2d716f2a087fff45b42c`.
- Re-executing all 69 packages with an explicitly unavailable EPUBCheck JAR reproduces the original normalized JSON **byte-for-byte**, with the same SHA-256.
- The original `BLIND_FREEZE_EVIDENCE.md` remains unchanged (SHA-256 `30b898063dea5ab007e3c704f7fdcda87f81e819d16fe03f1f2810ab74db70d7`).
- Every original SPD-native Python file, original test, normative input, canonical schema, and corpus package retains its pre-stage hash. The sole modified original Python file is `spd_validator_b/epubcheck.py`.
- Detailed native findings, including messages and evidence, are identical before/after on all 69 packages. Only the external adapter's own inherited-EPUB finding is excluded from that detailed comparison.

## Evaluated results

EPUBCheck 5.3.0 executed against **69/69 packages**: **61 PASS, 8 FAIL, 0 ERROR**. Each failure exited 1. All Validator B operational statuses are `COMPLETE`; there are zero internal errors.

| Normalized field | Number changed | Explanation |
|---|---:|---|
| `operationalStatus` | 69 | `TOOL_UNAVAILABLE` became `COMPLETE` |
| `notTestedRequirementIds` | 69 | Inherited EPUB requirement `SPD-BASE-002` was evaluated |
| `base` | 39 | `NOT_TESTED` became `PASS`; the other 30 remain `FAIL` |
| `normativeCapabilities` | 9 | Mapping `NOT_TESTED` became `PASS`; 15 Mapping failures remain |
| `violationRequirementIds` | 7 | EPUBCheck added `SPD-BASE-002`; one additional EPUB-failing package already had that native violation |
| `experimentalCapabilities` | 0 | Unchanged |

Accessible remains `NOT_TESTED` for the one claiming document; EPUBCheck does not supply the required human evaluation.

Every changed result is classified **`EPUBCHECK_NOW_EVALUATED`**. `UNEXPECTED_NON_EPUB_DIFFERENCE` count: **0**.

Machine-readable per-fixture before/after records are in `epubcheck-before-after.json`. Exit codes, diagnostic codes, and raw stdout/stderr are in `epubcheck-fixture-execution.json`.

## EPUBCheck failures observed independently

| Fixture | Exit | Diagnostic codes |
|---|---:|---|
| invalid/duplicate-node-id | 1 | RSC-005 |
| invalid/duplicate-normalized-path | 1 | OPF-060, OPF-074 |
| invalid/event-handler | 1 | OPF-014, RSC-005 |
| invalid/external-required-css | 1 | RSC-006 |
| invalid/external-required-font | 1 | OPF-014, RSC-008 |
| invalid/external-required-image | 1 | OPF-014, RSC-006 |
| invalid/invalid-xhtml | 1 | RSC-005, RSC-016 |
| invalid/javascript | 1 | OPF-014 |

No document logic was changed in response to these outcomes.

