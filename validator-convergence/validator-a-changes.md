# Validator A convergence changes

Implemented against the frozen Draft, registry, reviewed Stage 2 findings and Contract 0.1.1. No other validator implementation was translated or ported. Exact before/after hashes and full per-file diffs are in `source-changes.json`; the archive contains original bytes.

| Stage 2 finding / repair | Requirement IDs | Old behavior | New behavior | Targeted regression |
| --- | --- | --- | --- | --- |
| Revision scope / event exemption | ID-006, SEC-001 | Per-XHTML index and event-handler exemption | Revision-wide index; both occurrences retain resource/line/node evidence; security failure does not exempt identity | revision_scope_and_duplicate_evidence; security_is_not_an_identity_exemption |
| Stale/current document predicates | STATE-005/006/007; not STATE-001 | Stale Mapping attributed to processor behavior | Document-only currentness attribution and SEALED/Mapping guards | stale_rules_are_document_not_processor_rules |
| Independent integrity/projections | RES-002/003/004/006, INT-003/004/005, STATE-002/003, ANN-004 | Primary failures suppressed readable independent predicates; effects conflated | Safe inventory inspection continues; supplied projections and live bytes remain separate; lifecycle/effects guard state rules | lifecycle_and_effects_guard_state_predicates; all_reviewed_overlaps_remain_visible |
| Geometry overlap | MAP-011/012 | Specific geometry label suppressed second applicable predicate | Both independently false predicates retained | all_reviewed_overlaps_remain_visible |
| Unknown authority and prerequisite model | DISC-001/002, CAP-002/003, ID-006 and shared blocked groups | Incomplete authority did not expose stable unknown/blocked surface | Conflicting candidates quarantined; safe OPF facts retained; UNKNOWN not empty; malformed semantic XML blocks identity | unknown_claims_are_not_empty_and_xml_prerequisites_are_explicit |
| External attribution / report representation | Guarded BASE-002, SEM-002, ID-006, SEC-004/005/006 | Broad aggregate external failure; historical freezer suppressed BASE-002 beside native IDs | Shared guarded policy; every fixture keeps full external evidence; new runner never filters IDs | 70 real EPUBCheck integrations; production_report_matches_implementation_schema; unavailable_epubcheck_is_incomplete_not_pass_or_document_failure |
| Reproducibility and experimental reporting | Non-normative report metadata | Physical fixed presence implied claim; hardcoded Unicode 16 label | Explicit declaration/presence/evaluation separate; actual crate Unicode 17.0.0 recorded | 70 separate experimental comparisons; source-stability and runtime checks |
| Security regression / versioned corpus | Existing package/parser limits and coverage | 69-fixture corpus; no cross-spine negative | 70 fixtures, preserved old golden checks, bounded 128-input fuzz smoke | bounded_fuzz_smoke; corpus_normalized_classification; all_requirements_have_coverage_registration |

## Complete changed/new file inventory

| File | Reason / behavior | Verification |
| --- | --- | --- |
| validator-a/Cargo.lock | Root package version refresh only. | Targeted tests above; full suite and 70-fixture three-way comparison |
| validator-a/Cargo.toml | Version draft.2; no dependency replacement. | Targeted tests above; full suite and 70-fixture three-way comparison |
| validator-a/README.md | Version/shared contract and historical-freezer warning. | Targeted tests above; full suite and 70-fixture three-way comparison |
| validator-a/schemas/validator-report.schema.json | Implementation report schema accepts explicit authority/experimental data; canonical schemas untouched. | Targeted tests above; full suite and 70-fixture three-way comparison |
| validator-a/src/epubcheck.rs | Version check and full execution evidence; retain bounded capture/drain/timeout; shared attribution. | Targeted tests above; full suite and 70-fixture three-way comparison |
| validator-a/src/lib.rs | Wire shared policy module and report actual Unicode data version. | Targeted tests above; full suite and 70-fixture three-way comparison |
| validator-a/src/model.rs | Unknown authority, experimental fields and complete tool-evidence structure. | Targeted tests above; full suite and 70-fixture three-way comparison |
| validator-a/src/policy.rs | Native Rust consumer of shared blocked groups and guarded attribution data. | Targeted tests above; full suite and 70-fixture three-way comparison |
| validator-a/src/validator.rs | All A predicate/roll-up/identity repairs in the rows above. | Targeted tests above; full suite and 70-fixture three-way comparison |
| validator-a/tests/convergence.rs | Seven targeted regressions including bounded 128-input fuzz smoke. | Targeted tests above; full suite and 70-fixture three-way comparison |
| validator-a/tests/corpus.rs | Current manifest count 70; preserve historical oracle count 69 and retained external records 31. | Targeted tests above; full suite and 70-fixture three-way comparison |

No unrelated functional refactor was included. B lint cleanup is mechanical and was necessary for the configured strict checks. The new runner retains raw native/external evidence without deleting IDs. Repository reporting schema selection and safe temporary-directory cleanup are documented in `source-changes.json`.
