# Validator convergence and release gate

READY FOR FORMAT 0.1 RELEASE CANDIDATE PREPARATION

Validator A **0.1.0-draft.2**, Validator B **0.1.1**, shared Contract **0.1.1**, Corpus **0.1.1**. All 70 fixtures agree exactly across A, B and the independently reviewed oracle. No Format Draft, requirement meaning/ID/classification, or canonical schema changed. No RC1 rename or release was performed.

## Old versus new

| Measure | Frozen Stage 2 | Convergence |
| --- | --- | --- |
| Fixtures | 69 | 70 |
| Base agreement | 68/69 | 70/70 |
| Normative capabilities | 69/69 | 70/70 |
| Failed-ID sets | 44/69 | 70/70 |
| NOT_TESTED sets | 69/69 | 70/70 |
| Operational status | 69/69 | 70/70 |
| Complete normative surface | 44/69 | 70/70 |
| Experimental reporting (separate) | 45/69 | 70/70 |
| Open normative blockers | 0 | 0 |

The repaired positive multi-spine passes both validators. The new cross-spine negative fails exactly SPD-ID-006 in both while EPUBCheck passes its per-resource XML IDs. Stale Mapping uses STATE-007, not processor STATE-001. Unknown authority stays unknown. SEALED/effects guards and reviewed independent overlaps are retained. Experimental presence, declaration and evaluation agree separately.

## Verification

- A: 17 tests, strict clippy, fmt check, release build; deterministic 128-input fuzz smoke included.
- B: 57 tests including property/security/adapter checks, Ruff, wheel build and installed bundled-policy smoke.
- Repository: 21 tests; 70 package hashes and 70 expected-file hashes/schemas verified; all multi-spine projections and bindings recompute.
- EPUBCheck 5.3.0: 70 completed executions per validator, 140 total; zero skips or operational failures; identical guarded attribution.
- Both: 113/113 requirements represented and 74/74 automated registrations/implementations retained.
- Preservation: 71 protected live files and all 350 archived historical inputs verify; source snapshots remained stable during final runs.

A preliminary B run exposed one Accessible/Base scope reporting regression introduced during repair. It was fixed and regression-tested before the final stable full run. Preliminary `candidate-*` files are not frozen release evidence.

The old A freezer retained only 31 external records but invoked the tool more broadly; it also filtered BASE-002 beside other IDs. The new runner records every execution and filters nothing. A's historical Unicode 16 label was incorrect: the installed crate uses 17.0.0. B uses 15.1.0. This difference is disclosed and did not affect observed fixture convergence; environments are not bit-identical.

## Evidence

[RC gate and answers A–M](RC_GATE.md), [contract changes](contract-changes.md), [attribution table](attribution-table.md), [corpus changes](corpus-changes.md), [A repairs](validator-a-changes.md), [B repairs](validator-b-changes.md), [external evaluation](external-evaluation.md), [fixture matrix](fixture-matrix.md), [machine-readable differential](differential-results.json).

| Validator | Versioned immutable freeze | SHA-256 |
| --- | --- | --- |
| A | validator-convergence/freezes/validator-a-0.1.0-draft.2-corpus-0.1.1.json | e4e6dd809b0bc8365a303d8b6c5f57fb108fcd0b756302b60f09f16c67fe3538 |
| B | validator-convergence/freezes/validator-b-0.1.1-corpus-0.1.1.json | edc0dcca3506ec75be97d88a8043cf87b8c3e3b01d53bf524b85da3b9a4c8df1 |

READY FOR FORMAT 0.1 RELEASE CANDIDATE PREPARATION
