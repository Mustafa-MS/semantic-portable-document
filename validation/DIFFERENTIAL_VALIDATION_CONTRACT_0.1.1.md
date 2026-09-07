# Differential Validation Contract 0.1.1

NON-NORMATIVE VALIDATION INFRASTRUCTURE. NO FORMAT SEMANTICS CHANGED.

This shared contract supersedes the comparison policy, not Format 0.1 Draft. The original validator-a/docs/DIFFERENTIAL_VALIDATION_CONTRACT.md remains frozen. The companion REQUIREMENT_ATTRIBUTION_0.1.1.json is authoritative for this evaluation profile and is consumed by both implementations.

## Evidence and attribution

Every check distinguishes applicability, prerequisite availability and predicate truth. Unknown claims are not empty claims; a missing descriptor is not a descriptor with no capabilities. Invalid/conflicting candidates confer no authority on familiar fields. Independently available OCF/OPF facts and non-conflicting descriptor links remain usable. Candidate structural diagnostics retain candidate provenance; when discovery itself invalidates the candidate, DISC-002 carries the failure and dependent semantic fields remain unknown.

FAIL requires an independently established applicable counterexample. An established false conjunct suffices even if another conjunct is unavailable. Every independently established applicable failed predicate in the shared scope enters the sorted unique failed-ID set; no primary-error suppression is permitted. An unavailable prerequisite yields NOT_TESTED only where neither a counterexample nor conformance is established, with a blocking reason. Outside-applicability predicates are NOT_APPLICABLE and excluded from failed and NOT_TESTED sets. Missing values must not be replaced by {}, [], 0, false or an empty claim set for semantic comparisons. An omitted/unexecuted check is never implicitly PASS.

Descriptor-dependent blocked-ID groups are specified in the attribution artifact. Some applicability conditions are themselves unknown after discovery failure: these groups represent unevaluated conditional checks, not a finding that a capability was claimed. An explicit failed predicate takes precedence over NOT_TESTED for the same requirement ID. Global lineage evidence is absent in this corpus profile, so ID-013 remains NOT_TESTED without blocking certification of current-revision Base invariants; historical persistence is outside this document-only evaluation scope. Accessible includes manual ACC-001/004 evaluation and cannot automatically PASS.

## Normalized surface

Compare fixture identity and exact package digest, Base, normative capability results, sorted unique violationRequirementIds, sorted unique notTestedRequirementIds, and operationalStatus. Additionally record authoritativeClaimsStatus=KNOWN or UNKNOWN. UNKNOWN claim authority serializes each unresolved capability result as UNKNOWN, not NOT_CLAIMED; this is a versioned report-state extension, not a Format capability. Known unclaimed capabilities serialize NOT_CLAIMED. A known claimed capability FAILs for its own failed predicate or a failed required Base dependency; otherwise required incomplete evaluation is NOT_TESTED. PASS requires positive evidence within the explicitly recorded evaluation scope.

RES-003 and RES-006 both apply to each unlisted non-exempt package resource, including caches. MAP-011 and MAP-012 both apply to readable out-of-bounds visible geometry. Independently readable inventory strings can violate RES-002 despite package rejection; never extract unsafe entries or disable resource limits to inspect them.

Declared-inventory projections consume supplied inventory fields, not reconstructed live resources. Resource byte verification, exact inventory binding, declared projections, verified current state and fixed/mapping bindings retain distinct evidence. Projection mismatches remain testable after an inventory/resource hash failure. Matching declared projections do not certify live resource integrity. STATE-002 is SEALED-only; STATE-003 requires mutation of a semantic-affecting inventoried resource. Non-semantic mutation can invalidate a seal under general integrity rules without STATE-003. STATE-001 requires processor-behavior evidence and is NOT_APPLICABLE to this document-only profile. False declared-current fixed output uses STATE-005; SEALED and Mapping constraints use STATE-006 and STATE-007.

## External scope

Both validators execute official EPUBCheck 5.3.0 for every corpus package, including native failures, within the same bounded timeout and safety scope. Unsafe paths are never extracted by validator code. Operational rejection prevents external execution only when the external-tool safety budget cannot be met; record executed=false and the precise skip reason. Each record includes package SHA-256, version, execution/skip status, exit code, diagnostic codes and attributed IDs. Tool unavailability/failure is not evidence of document invalidity.

Only ERROR/FATAL diagnostics matching the shared diagnostic code plus predicate guard enter SPD results. OCF, OPF, XHTML and other inherited diagnostics remain distinguished. OPF-014 and unrecognized or insufficiently specific diagnostics remain raw external evidence; they are not automatically BASE-002. RSC-005 is refined by message (duplicate ID versus parse failure); no fixture-name tests are permitted. The table is versioned and its hash recorded. Neither normalization nor oracle generation may delete independently established native or externally attributed failures.

## Experimental representation

Outside normative equality, compare physicalFixedRenditionPresent (boolean or null if unknown), fixedExperimentalCapabilityDeclared (boolean or null), and fixedExperimentalEvaluationStatus (NOT_TESTED when declared, NOT_CLAIMED when not, UNKNOWN when authority unknown). Physical presence is determined from a valid fixed-resource binding/path, not merely a Mapping claim. Existing experimentalCapabilities reflects explicit declarations only. Archive-Experimental follows the same declaration distinction. Presence does not certify PDF conformance.

## Reproducibility

Record Draft/registry hashes, individual canonical schema hashes, corpus manifest and fixture hashes, source hashes, contract/attribution hashes, validation options, Unicode data versions, tool version and external scope for both runs. Known Unicode-version differences may be reported without blocking observed convergence, but environments must not be called bit-identical. Freeze new versioned outputs; preserve every prior oracle and differential artifact. Agreement requires A↔B, A↔independently reviewed expected results and B↔expected results, not pairwise imitation.
