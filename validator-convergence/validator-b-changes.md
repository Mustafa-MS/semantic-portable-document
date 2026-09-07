# Validator B convergence changes

Implemented against the frozen Draft, registry, reviewed Stage 2 findings and Contract 0.1.1. No other validator implementation was translated or ported. Exact before/after hashes and full per-file diffs are in `source-changes.json`; the archive contains original bytes.

| Stage 2 finding / repair | Requirement IDs | Old behavior | New behavior | Targeted regression |
| --- | --- | --- | --- | --- |
| Missing/conflicting discovery | DISC-001/002; CAP-003; ARCH-001 | Unavailable fields coerced to empty and invented architecture/capability failures | Quarantine candidates; unknown claim authority; use only discovered facts, no filename authority fallback | test_unknown_descriptor_facts (2 cases) |
| SEALED applicability | STATE-002; INT-003/004/005; RES-004 | EDITABLE bad-resource-hash received SEALED-only ID | Explicit lifecycle guard; retain all four real integrity/projection failures | test_editable_bad_hash_and_projection_failures |
| Semantic effects | STATE-003; RES-004; INT-003 | Every SEALED byte mutation treated as semantic change | Semantic-specific rule requires semantic-affecting resource; rendering/fixed/mapping/annotation mutations retain general integrity IDs only where appropriate | test_nonsemantic_integrity_is_not_semantic_mutation (4 cases) |
| Stale/current document predicates | STATE-005/006/007; not STATE-001 | Document state used to assert processor mispresentation | No STATE-001 without processor evidence; document currentness uses actual predicates | test_no_document_only_processor_finding (3 cases) |
| Prerequisite/roll-up model | Shared blocked IDs; ACC-001/004; ID-013 | Unknowns/defaults and automatic PASS ledger; transient Accessible Base-scope regression during repair | Unknowns explicit, failed wins blocked; unevaluated ledger entries not falsely PASS; current Base scope excludes history and Accessible manual work | test_accessible_manual_work_does_not_block_current_base_scope; 70-fixture full oracle comparison |
| External attribution / experimental report | Guarded BASE-002, SEM-002, ID-006, SEC-004/005/006; experimental metadata | Blanket external BASE-002; physical presence/claims conflated | Same policy consumed independently; preserve raw unmatched diagnostics; explicit experimental claims | test_shared_external_policy_no_blanket_mapping; 6 adapter tests; 70 real integrations |
| Revision uniqueness / overlap retention | ID-006, SEC-001, RES-003/006, MAP-011/012 | Correct independent B behavior needed retention while other repairs landed | No cross-port from A; regression asserts positive and negative plus all reviewed native ID sets | test_revision_wide_positive_and_negative; test_current_corpus_against_independent_native_oracle |

## Complete changed/new file inventory

| File | Reason / behavior | Verification |
| --- | --- | --- |
| validator-b/pyproject.toml | Version 0.1.1 and shared attribution bundled in wheel. | Targeted tests above; full suite and 70-fixture three-way comparison |
| validator-b/README.md | New reporting contract/version and preserved blind artifacts. | Targeted tests above; full suite and 70-fixture three-way comparison |
| validator-b/spd_validator_b/__init__.py | Version 0.1.1. | Targeted tests above; full suite and 70-fixture three-way comparison |
| validator-b/spd_validator_b/annotations.py | Ruff mechanical import cleanup only; no behavior change. | Targeted tests above; full suite and 70-fixture three-way comparison |
| validator-b/spd_validator_b/cli.py | Version label 0.1.1. | Targeted tests above; full suite and 70-fixture three-way comparison |
| validator-b/spd_validator_b/coverage.py | Ruff mechanical import/type-annotation cleanup only; registration/classification unchanged. | Targeted tests above; full suite and 70-fixture three-way comparison |
| validator-b/spd_validator_b/epub.py | Candidate provenance and quarantine, no fallback authority. | Targeted tests above; full suite and 70-fixture three-way comparison |
| validator-b/spd_validator_b/epubcheck.py | Guarded shared attribution plus complete external record. | Targeted tests above; full suite and 70-fixture three-way comparison |
| validator-b/spd_validator_b/integrity.py | Available-evidence checks, SEALED/effects guards and corrected state attribution. | Targeted tests above; full suite and 70-fixture three-way comparison |
| validator-b/spd_validator_b/mapping.py | Claim/state evidence guards; correct stale STATE-007 and SEALED-only mapping STATE-002. | Targeted tests above; full suite and 70-fixture three-way comparison |
| validator-b/spd_validator_b/models.py | New normalized fields; FAIL wins NOT_TESTED for same ID. | Targeted tests above; full suite and 70-fixture three-way comparison |
| validator-b/spd_validator_b/package.py | Ruff mechanical import cleanup only; security behavior unchanged. | Targeted tests above; full suite and 70-fixture three-way comparison |
| validator-b/spd_validator_b/policy.py | Native Python shared data consumer plus packaged fallback; not copied from A. | Targeted tests above; full suite and 70-fixture three-way comparison |
| validator-b/spd_validator_b/semantics.py | Unavailable authoritative XML blocks revision ID index. | Targeted tests above; full suite and 70-fixture three-way comparison |
| validator-b/spd_validator_b/validator.py | Unknown claims, blocked groups, experimental separation and scoped roll-up; explicit top-level containment lint justification. | Targeted tests above; full suite and 70-fixture three-way comparison |
| validator-b/tests/test_algorithms.py | Ruff mechanical import cleanup only; test behavior unchanged. | Targeted tests above; full suite and 70-fixture three-way comparison |
| validator-b/tests/test_convergence.py | Fourteen targeted cases covering reviewed predicates and independent native oracle. | Targeted tests above; full suite and 70-fixture three-way comparison |
| validator-b/tests/test_corpus_security.py | Manifest count 70; preserve malformed-package/security assertions. | Targeted tests above; full suite and 70-fixture three-way comparison |
| validator-b/tests/test_epubcheck_integration.py | Expected external XML attribution SEM-002 instead of blanket BASE-002. | Targeted tests above; full suite and 70-fixture three-way comparison |

No unrelated functional refactor was included. B lint cleanup is mechanical and was necessary for the configured strict checks. The new runner retains raw native/external evidence without deleting IDs. Repository reporting schema selection and safe temporary-directory cleanup are documented in `source-changes.json`.
