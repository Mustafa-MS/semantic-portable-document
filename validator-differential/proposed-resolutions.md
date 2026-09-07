# Proposed resolutions — review required; no fixes applied

## Required decisions

- Genuine Format 0.1 normative ambiguity revealed: **NO**. The investigated validity/currentness/identity rules are sufficiently clear. Diagnostic ID attribution and evaluation scope need a stronger comparison contract, not altered Format semantics.
- Frozen fixture/expected-oracle contradiction: **YES**. `valid/multi-spine` contains a revision-wide duplicate but expects PASS. Additionally, `invalid/stale-fixed-rendition/expected.json` attributes the Mapping failure to processor-behavior STATE-001 without processor evidence; its Mapping FAIL verdict is correct, its exact expected ID is not. Other sparse expected-ID lists are normalization issues, not automatically wrong conformance verdicts.
- Multi-spine decision: **CORPUS_WRONG**, with confirmed A uniqueness defect.
- Cascade decision: **C**. The two reporting strategies are reasonable in principle; actual false predicates and misattributed IDs are not excused.
- Exact convergence today: **NO**, only 44/69 full-surface matches.

## Confirmed Validator A defects

1. Revision-wide Node-ID uniqueness is implemented with a per-XHTML HashSet. This misses n_article01 across multi-spine and causes the lone wrong PASS. Target: validator.rs:938–949.
2. Event-handler IDs are explicitly exempted from duplicate reporting, despite no normative exception. event-handler contains two n_heading01 occurrences in a well-formed DOM. Target: validator.rs:929–941. This is a false check exemption, not simply a choice to report fewer redundant messages.
3. stale-fixed-rendition routes a Mapping-currentness failure to STATE-001, a processor-behavior rule, instead of STATE-007. Target: validator.rs:543–567. The corpus expectation shares this exact-ID error; the invalid Mapping verdict itself is correct.

The current external acceptance workflow is also insufficient for a paired all-fixture external comparison: only 31 valid/edge runs are recorded. This is not a demonstrated defect in A's production adapter, which invokes EPUBCheck whenever configured. Do not label ordinary primary-error suppression or missing duplicate ID labels as confirmed A conformance defects without the agreed normalization policy.

## Confirmed Validator B defects

1. Missing/invalid authoritative descriptor data is coerced to empty claims. CAP-003 is then compared against an invented set, and missing Base declaration is misused to assert ARCH-001. The independently discovered OPF has one authoritative spine. Target: validator.py:26–50, coordinated with descriptor authority tracking. No filename scanning was found in this path.
2. STATE-002 is emitted for the bad-resource-hash EDITABLE package, without sealed-state applicability. The underlying inventory mismatch is real, but the requirement ID is wrong. Target: integrity.py:129–134.
3. Any covered SEALED integrity failure is labelled STATE-003, including rendering-only CSS and non-semantic fixed/mapping/annotation changes. All invalidate the seal, but they do not establish the semantic-content-specific rule. Target: integrity.py:162–164.
4. A stale fixed token plus Mapping claim is treated as proof a processor presents stale content as current. The document establishes STATE-007, not reader behavior. A false current token in mutation-fixed establishes STATE-005, likewise not an observed reader action. Target: mapping.py:44–49 and integrity.py:154–156. The stale-fixed-rendition shared STATE-001 should be corrected on both sides.

These are diagnostic/predicate defects on already-invalid fixtures, not additional frozen PASS/FAIL differences. Review scope guards before reusing those predicates in future capability roll-up.

## Proposed exact contract text

The following is proposed wording only. It was not inserted into the frozen contract.

> A normalized run MUST record the exact fixture digest, normative input digests, schema-file digest manifest, options, Unicode data version, external-tool version and per-fixture external evaluation scope. A comparison with different prerequisites MUST retain its mechanical results but MUST be labelled environment- or scope-divergent; it MUST NOT be described as a controlled same-input convergence result.
>
> Every normalized requirement result MUST distinguish applicability, availability of prerequisite evidence, and the truth of its predicate. A required value unavailable through authorized discovery or parsing MUST NOT be replaced with an empty object, empty claim set, zero, or other default for semantic comparison. A failed candidate-schema check MAY be retained with candidate provenance, but MUST NOT confer authority on that candidate's missing or invalid fields.
>
> An applicable requirement is FAIL when available evidence establishes a counterexample to its predicate. A failed conjunction MAY be established by one false conjunct even when another conjunct cannot be evaluated. Failure of another requirement MUST NOT suppress an independently established failure. An unavailable prerequisite is NOT_TESTED when it prevents establishing either conformance or a counterexample; include the blocking requirement or evidence reason. NOT_APPLICABLE requirements are excluded from both failed and NOT_TESTED sets. No unexecuted or suppressed check is implicitly PASS.
>
> The failed requirement-ID set MUST include every independently established applicable failed predicate in the agreed evaluation scope, using a shared predicate-to-requirement attribution table. Multiple IDs for one fact are included only when their defined predicates each cover that fact; the table MUST explicitly define overlaps such as RES-003/RES-006 and MAP-011/MAP-012. Candidate-schema errors MUST be attributed to the field/structure actually disproved, not inferred semantic facts. Processor-behavior requirements require processor evidence and MUST NOT be inferred solely from a document's capability claim. Lifecycle-specific predicates MUST be evaluated only in their stated lifecycle.
>
> A declared-inventory projection comparison consumes the supplied inventory fields and does not require their resource hashes to pass first. Its result MUST be distinguished from certification of verified live semantic/rendering input state. Exact resource bytes, exact inventory bytes, declared projections, fixed-currentness bindings, and Mapping dependencies MUST retain separate evidence. Missing parse/discovery evidence blocks only the predicates that consume it.
>
> For an EPUBCheck-complete comparison, EPUBCheck 5.3.0 MUST be invoked for every fixture safely eligible for execution, including fixtures already rejected by native checks. Skipped runs MUST record their safety or scope reason. Both validators MUST use the same accepted severity and diagnostic-to-SPD-requirement mapping table, distinguishing OCF requirements from other inherited EPUB requirements. Aggregate external labels MUST NOT silently broaden a registry predicate. Raw log wording is excluded from equality.
>
> Experimental report data MUST distinguish physical rendition presence, explicit capability declaration, and evaluation status. Physical presence of a fixed rendition or a normative Mapping dependency MUST NOT create an explicit Fixed-Experimental claim. Experimental presence/status fields remain outside the normative differential surface. The shared attribution table MUST separately identify the applicability of experimental requirement IDs that appear in the failed-ID array; excluding a status field does not automatically exclude an ID.
>
> Capability FAIL takes precedence when an applicable failed requirement or a failed required capability dependency is established. Otherwise a required unevaluated predicate yields NOT_TESTED. PASS requires positive evidence for all applicable predicates necessary for complete certification. Unknown authoritative claims MUST be represented as unknown evaluation state, not asserted as a known NOT_CLAIMED fact; any serialization extension needed to represent this is versioned with the contract.

Proposed overlap decisions: include both RES-003 and RES-006 for an unlisted non-exempt ZIP resource, including caches; include MAP-011 and the §36-linked MAP-012 for out-of-bounds visible geometry; retain resource and declared-projection failures when their operands are readable. Do not use STATE-002 for EDITABLE binding mismatches or STATE-003 as a generic label for non-semantic seal invalidity. These decisions stabilize reporting; they do not change the underlying document rules.

## Repair sequence for the next authorized stage

1. Review these decisions and approve the versioned contract/attribution table, including scope/environment controls.
2. Correct the multi-spine corpus case and add a distinct negative cross-spine duplicate case; correct the stale-fixed expected-ID attribution. Recompute affected package bindings when package bytes change.
3. Correct the confirmed A and B defects independently against the Draft and targeted tests. Do not copy A's golden IDs into B.
4. Align external evaluation scope and normalization policy. Preserve both existing frozen reports as historical evidence.
5. Produce new versioned validator freezes and rerun the differential. Require all mechanical fields to converge under the approved contract; keep experimental comparisons separate.

Recommended targets: Validator A, Validator B, Corpus, Differential contract and A oracle-generation workflow. No normative Format Draft change is required by the investigated differences. No target was modified in this stage.

PROCEED TO VALIDATOR CONVERGENCE FIXES
