# Contract changes

NO FORMAT SEMANTICS CHANGED. Contract 0.1.1 is shared NON-NORMATIVE VALIDATION INFRASTRUCTURE, outside either validator. The original contract is unchanged. Both implementations consume the same versioned attribution JSON (Rust embeds it; Python loads it and packages it in the wheel).

| Change category | Complete policy change |
| --- | --- |
| comparison precision | Fixture/package identity, explicit KNOWN/UNKNOWN claim authority, exact sorted unique sets, positive-evidence PASS, three-way oracle comparison, individual input/source hashes. Unicode differences are disclosed rather than falsely asserted identical. |
| applicability | Lifecycle/capability guards; processor STATE-001 is outside document-only scope; NOT_APPLICABLE excluded from failed/NOT_TESTED sets. Current-revision Base scope excludes historical ID-013 and Accessible-only manual certification. |
| dependency handling | Unavailable authority stays unknown; explicit blocking groups; retain independent OPF facts; false conjunct establishes FAIL; FAIL takes precedence over blocked NOT_TESTED for the same ID; declared projections are distinct from live integrity. |
| external scope | All 70 safely eligible packages, including native failures; version, digest, execution/skip reason and complete diagnostics retained. Tool failure is operational, not document failure. |
| attribution | Every independently disproved applicable predicate; RES-003/006 and MAP-011/012 overlaps; actual state/effects predicates; code-plus-message guarded external mapping, no blanket BASE-002 or normalization filtering. |
| experimental reporting | Presence, explicit declaration and evaluation are distinct; UNKNOWN/null allowed; normative comparison excludes these fields and measures them separately. |

The section-by-section text below is the exact original-to-new difference; all new clauses fall into the six categories above.

```diff
--- validator-a/docs/DIFFERENTIAL_VALIDATION_CONTRACT.md
+++ validation/DIFFERENTIAL_VALIDATION_CONTRACT_0.1.1.md
@@ -1,28 +1,35 @@
-# Differential validation contract
+# Differential Validation Contract 0.1.1
 
-Independent validators compare the deterministic normalized surface only:
+NON-NORMATIVE VALIDATION INFRASTRUCTURE. NO FORMAT SEMANTICS CHANGED.
 
-1. Base result;
-2. results for claimed normative capabilities;
-3. sorted unique failed requirement IDs;
-4. sorted unique `NOT_TESTED` requirement IDs;
-5. operational status.
+This shared contract supersedes the comparison policy, not Format 0.1 Draft. The original validator-a/docs/DIFFERENTIAL_VALIDATION_CONTRACT.md remains frozen. The companion REQUIREMENT_ATTRIBUTION_0.1.1.json is authoritative for this evaluation profile and is consumed by both implementations.
 
-Experimental presence, richer messages, evidence ordering below the documented
-sort key, performance metrics, and absolute temporary paths are excluded. The
-same Draft, registry/schema digests, options, Unicode data, and EPUBCheck version
-must be used. This contract specifies no Validator B implementation choices.
+## Evidence and attribution
 
-## Normalized capability roll-up
+Every check distinguishes applicability, prerequisite availability and predicate truth. Unknown claims are not empty claims; a missing descriptor is not a descriptor with no capabilities. Invalid/conflicting candidates confer no authority on familiar fields. Independently available OCF/OPF facts and non-conflicting descriptor links remain usable. Candidate structural diagnostics retain candidate provenance; when discovery itself invalidates the candidate, DISC-002 carries the failure and dependent semantic fields remain unknown.
 
-- `PASS`: every applicable normative requirement necessary for the claimed
-  capability has been positively established within the supplied evaluation
-  scope, including required manual evaluation.
-- `FAIL`: at least one applicable normative requirement has been established as
-  failed.
-- `NOT_TESTED`: no established failure exists, but at least one applicable
-  normative requirement required for complete certification was not evaluated.
-- `NOT_CLAIMED`: the document does not claim the capability.
+FAIL requires an independently established applicable counterexample. An established false conjunct suffices even if another conjunct is unavailable. Every independently established applicable failed predicate in the shared scope enters the sorted unique failed-ID set; no primary-error suppression is permitted. An unavailable prerequisite yields NOT_TESTED only where neither a counterexample nor conformance is established, with a blocking reason. Outside-applicability predicates are NOT_APPLICABLE and excluded from failed and NOT_TESTED sets. Missing values must not be replaced by {}, [], 0, false or an empty claim set for semantic comparisons. An omitted/unexecuted check is never implicitly PASS.
 
-Experimental capability presence/status remains separately represented by the
-existing experimental result model.
+Descriptor-dependent blocked-ID groups are specified in the attribution artifact. Some applicability conditions are themselves unknown after discovery failure: these groups represent unevaluated conditional checks, not a finding that a capability was claimed. An explicit failed predicate takes precedence over NOT_TESTED for the same requirement ID. Global lineage evidence is absent in this corpus profile, so ID-013 remains NOT_TESTED without blocking certification of current-revision Base invariants; historical persistence is outside this document-only evaluation scope. Accessible includes manual ACC-001/004 evaluation and cannot automatically PASS.
+
+## Normalized surface
+
+Compare fixture identity and exact package digest, Base, normative capability results, sorted unique violationRequirementIds, sorted unique notTestedRequirementIds, and operationalStatus. Additionally record authoritativeClaimsStatus=KNOWN or UNKNOWN. UNKNOWN claim authority serializes each unresolved capability result as UNKNOWN, not NOT_CLAIMED; this is a versioned report-state extension, not a Format capability. Known unclaimed capabilities serialize NOT_CLAIMED. A known claimed capability FAILs for its own failed predicate or a failed required Base dependency; otherwise required incomplete evaluation is NOT_TESTED. PASS requires positive evidence within the explicitly recorded evaluation scope.
+
+RES-003 and RES-006 both apply to each unlisted non-exempt package resource, including caches. MAP-011 and MAP-012 both apply to readable out-of-bounds visible geometry. Independently readable inventory strings can violate RES-002 despite package rejection; never extract unsafe entries or disable resource limits to inspect them.
+
+Declared-inventory projections consume supplied inventory fields, not reconstructed live resources. Resource byte verification, exact inventory binding, declared projections, verified current state and fixed/mapping bindings retain distinct evidence. Projection mismatches remain testable after an inventory/resource hash failure. Matching declared projections do not certify live resource integrity. STATE-002 is SEALED-only; STATE-003 requires mutation of a semantic-affecting inventoried resource. Non-semantic mutation can invalidate a seal under general integrity rules without STATE-003. STATE-001 requires processor-behavior evidence and is NOT_APPLICABLE to this document-only profile. False declared-current fixed output uses STATE-005; SEALED and Mapping constraints use STATE-006 and STATE-007.
+
+## External scope
+
+Both validators execute official EPUBCheck 5.3.0 for every corpus package, including native failures, within the same bounded timeout and safety scope. Unsafe paths are never extracted by validator code. Operational rejection prevents external execution only when the external-tool safety budget cannot be met; record executed=false and the precise skip reason. Each record includes package SHA-256, version, execution/skip status, exit code, diagnostic codes and attributed IDs. Tool unavailability/failure is not evidence of document invalidity.
+
+Only ERROR/FATAL diagnostics matching the shared diagnostic code plus predicate guard enter SPD results. OCF, OPF, XHTML and other inherited diagnostics remain distinguished. OPF-014 and unrecognized or insufficiently specific diagnostics remain raw external evidence; they are not automatically BASE-002. RSC-005 is refined by message (duplicate ID versus parse failure); no fixture-name tests are permitted. The table is versioned and its hash recorded. Neither normalization nor oracle generation may delete independently established native or externally attributed failures.
+
+## Experimental representation
+
+Outside normative equality, compare physicalFixedRenditionPresent (boolean or null if unknown), fixedExperimentalCapabilityDeclared (boolean or null), and fixedExperimentalEvaluationStatus (NOT_TESTED when declared, NOT_CLAIMED when not, UNKNOWN when authority unknown). Physical presence is determined from a valid fixed-resource binding/path, not merely a Mapping claim. Existing experimentalCapabilities reflects explicit declarations only. Archive-Experimental follows the same declaration distinction. Presence does not certify PDF conformance.
+
+## Reproducibility
+
+Record Draft/registry hashes, individual canonical schema hashes, corpus manifest and fixture hashes, source hashes, contract/attribution hashes, validation options, Unicode data versions, tool version and external scope for both runs. Known Unicode-version differences may be reported without blocking observed convergence, but environments must not be called bit-identical. Freeze new versioned outputs; preserve every prior oracle and differential artifact. Agreement requires A↔B, A↔independently reviewed expected results and B↔expected results, not pairwise imitation.
```
