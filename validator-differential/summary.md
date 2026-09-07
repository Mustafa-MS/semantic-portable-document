# Frozen differential comparison — Stage 2

The frozen validators do **not** converge. The Draft's conformance meaning is sufficiently clear for the investigated cases: proceed to reviewed validator/report-contract/corpus repairs, without changing normative Format semantics. No repairs were made here.

## Agreement metrics

| Surface | Agreement |
|---|---:|
| Fixture identities | 69/69 |
| Base result | 68/69 |
| Normative capability results | 69/69 |
| Exact violation-ID sets | 44/69 |
| Exact NOT_TESTED-ID sets | 69/69 |
| Operational status | 69/69 |
| Complete normalized differential surface | 44/69 |
| Normative invalid versus not-invalid classification | 68/69 |
| Three-valued VALID / INVALID / UNDETERMINED classification | 68/69 |
| Experimental reporting, excluded from normative metrics | 45/69 |

For the semantic metric, INVALID means Base or a claimed normative capability is FAIL. If no failure exists but a required result is NOT_TESTED, classification is UNDETERMINED, not certified VALID. This avoids mislabelling the Accessible manual-evaluation case as valid. Both semantic metrics differ only on multi-spine.

There are exactly **25** differing violation sets. **A is a strict subset of B in all 25**; A_ONLY is empty throughout. raw-diff.json contains all 69 pairs, every contract field, equal-field flags, COMMON/B_ONLY/A_ONLY sets, and separate experimental values. No failed-ID array was altered to force agreement.

## Primary classifications

| Classification | Fixtures |
|---|---:|
| CORPUS_ORACLE_BUG | 1 |
| VALIDATOR_A_BUG | 2 |
| VALIDATOR_B_BUG | 8 |
| NORMALIZATION_CONTRACT_BUG | 14 |
| SPEC_AMBIGUITY | 0 |
| EXTERNAL_TOOL_DIFFERENCE | 0 |
| PERMITTED_IMPLEMENTATION_VARIATION | 0 |
| UNRESOLVED | 0 |

One primary class per fixture; secondary classes capture compound cases. There is **1 RC_BLOCKER**, multi-spine, and **24 RC_DIAGNOSTIC_CONVERGENCE** cases with identical validity/capability results. Experimental differences affect **24 fixtures**, classified NON_NORMATIVE and counted separately. Predicate/attribution bugs on already-invalid fixtures remain bugs even though their observed severity is diagnostic convergence.

## Required decisions

- Multi-spine: **CORPUS_WRONG**; n_article01 repeats at chapter1.xhtml:4 and chapter2.xhtml:4 in one authoritative revision. A's local ID set misses it. Current fixture bytes cannot legitimately pass SPD-ID-006.
- Cascade semantics: **C**. Independent false predicates may be reported together; unavailable prerequisites must not become fabricated failures. Exact suppression/overlap policy is missing from the contract.
- Genuine normative Format ambiguity: **NO**.
- Corpus/oracle contradiction: **YES**: multi-spine's PASS, plus stale-fixed-rendition's unsupported processor-rule ID attribution (its Mapping FAIL remains correct).
- Confirmed A defects: per-resource rather than per-revision Node-ID scope; event-handler duplicate-ID exemption; stale Mapping failure attributed to STATE-001 rather than STATE-007.
- Confirmed B defects: unknown descriptor claims treated as empty/architecture evidence; sealed-only STATE-002 used in EDITABLE; semantic-change STATE-003 used for non-semantic changes; processor-presentation STATE-001 inferred from document state/claims alone.
- Contract clarification needed: **YES**, for dependencies, redundant IDs, NOT_TESTED/applicability, external evaluation scope and experimental presence versus claims. Exact proposed wording is in proposed-resolutions.md.

## Freeze and comparability evidence

| Input | Verified SHA-256 |
|---|---|
| B EPUBCheck-complete frozen result | af68e0e02182cf6a212c437ba19f6faa8a2d08409b65c3d77aa848e895cc2ed4 |
| Format Draft | fe649e74f8ea57b993f3fece4373efdb105ac2013812e74152270fe4666db849 |
| Requirements registry | a6a6ec7f6a0d1585ed5cc11a9dec3489540117257c3562a758b533b6624d137a |
| A frozen golden result, current observed digest | 68d6ab4b23a70f19937a8539eb6deb63cf9f4e4a3b06dd388ed15e4a295617a4 |

B and normative inputs match the supplied pins exactly. A is the expected golden path/version (0.1.0-draft.1), with matching frozen Draft/registry metadata and a freeze record identifying that path as immutable. **No independent earlier A oracle checksum was supplied**: A verification is artifact/metadata based, with its current digest recorded, not proof of an independently pinned prior digest. No observed frozen-input change triggered DIFFERENTIAL_FREEZE_FAILURE.

Both freezes identify EPUBCheck **5.3.0** and the same official release ZIP digest `6c07e68584b2e2ce2f89fe06e1246dfead3eb36b46b340e7d93524f29dcff6c5`. B's executable JAR digest is `f7f96617c929371821609b88c8484d6dc9f24fe916499863c46094c5fb778a65`.

Comparability caveats are retained, not normalized away:

- A declares Unicode 16 data; B uses Unicode 15.1.0. The Format traceability table allows a processor-declared supported version, but the differential contract requires the same data. No observed difference was traced to Unicode-version behavior; nevertheless this is not a strictly environment-identical experiment.
- A's schema-bundle digest and B's independently defined schema-set digest use different conventions. Canonical schema files were inspected and individually hashed; unequal aggregate conventions are not evidence of changed schema bytes, nor proof of identical aggregate inputs. A's historical per-file schema manifest is not supplied here.
- A records **31** valid/edge external runs, all PASS. B records **69** runs: 61 PASS, 8 FAIL. Seven B-only BASE-002 findings correspond to invalid fixtures omitted from A's recorded external scope. Both adapters map failures alike; no differing-version or diagnostic-parser cause was found, hence EXTERNAL_TOOL_DIFFERENCE=0 in that specific sense. This does **not** mean external evaluation is irrelevant or that all 69 external runs were paired. See cascade-semantics-analysis.md.

The mechanical metrics are exact comparisons of the requested frozen artifacts, not a claim that their environments/scopes satisfied every prerequisite of a controlled convergence run. This limitation does not undermine the directly evidenced multi-spine defect or measured package invariants.

## Deliverables and method

- raw-diff.json: all normalized pairs and reviewed per-fixture classifications.
- fixture-differences.md: required eight-column table for all 25 fixtures, followed by every B-only ID assessment.
- requirement-differences.md: reverse index, exact registry entries and occurrence-level conclusions.
- disagreement-families.md: six grouped normative families, plus the separate experimental family.
- multi-spine-investigation.md: normative evidence, exact ID locations and required verdict.
- cascade-semantics-analysis.md: dependency graph, FAIL/NOT_TESTED/applicability distinctions, state/geometry/external investigations.
- experimental-capability-differences.md: all 24 excluded informational differences.
- proposed-resolutions.md: confirmed defects, exact proposed contract wording and review/repair sequence.

Supporting artifacts: fixture-byte-evidence.json, protected-input-hashes.json and reproducible analysis scripts mechanical.py, inspect_evidence.py, build_reports.py. ZIPs were read without extraction; schemas and exact-byte digests were independently inspected without importing either validator. Source was inspected only after normative/package evidence to explain behavior. No validator, fixture, schema, expectation, registry, Draft or frozen contract was edited. No validator was rerun to generate a replacement oracle.

Final verification (`verify_reports.py`, results in verification.json): all 69 frozen pairs reproduced, all 25 classifications and 48 B-only requirement occurrences covered, all nine required reports present, and all 285 protected files unchanged against the snapshot recorded during analysis. That snapshot is not presented as an independently supplied pre-task freeze.

Reproduction: run mechanical.py, then inspect_evidence.py, then build_reports.py using B's existing Python environment. The first command regenerates mechanical raw-diff.json; the last restores reviewed classifications and generated detail reports. The four narrative reports are authored analysis, not generated oracle output. Reproduction writes only validator-differential/.

PROCEED TO VALIDATOR CONVERGENCE FIXES
