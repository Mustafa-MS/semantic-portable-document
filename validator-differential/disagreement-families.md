# Disagreement families

Families partition the 25 normative-surface differences. Experimental overlap is listed separately, not added to 25.

## NODE_ID_SCOPE — 1 fixtures

Affected fixtures: valid/multi-spine.

Affected IDs: SPD-ID-006.

Root normative question: Does uniqueness span the authoritative revision?

A interpretation: Per-XHTML ID set.

B interpretation: Shared spine-wide ID index.

Resolved interpretation: Draft §14 is revision-wide. Corpus and A wrong.

Primary classifications: CORPUS_ORACLE_BUG. Per-fixture exceptions and secondary classes are in fixture-differences.md.

## DESCRIPTOR_DISCOVERY_CASCADE — 2 fixtures

Affected fixtures: invalid/descriptor-discovery-conflict, invalid/descriptor-discovery-missing.

Affected IDs: SPD-ARCH-001, SPD-BASE-005, SPD-CAP-002, SPD-CAP-003, SPD-DISC-001, SPD-DISC-002, SPD-ID-002.

Root normative question: Which facts remain knowable after failed descriptor authority?

A interpretation: Early return after discovery failure.

B interpretation: Continue with absent or wrong-type descriptor treated as claim data.

Resolved interpretation: Keep OPF/spine facts; do not substitute empty claims or infer architecture. Candidate schema diagnostics can remain with explicit provenance.

Primary classifications: VALIDATOR_B_BUG. Per-fixture exceptions and secondary classes are in fixture-differences.md.

## XHTML_AND_EXTERNAL_EVALUATION — 7 fixtures

Affected fixtures: invalid/duplicate-node-id, invalid/event-handler, invalid/external-required-css, invalid/external-required-font, invalid/external-required-image, invalid/invalid-xhtml, invalid/javascript.

Affected IDs: SPD-BASE-002, SPD-ID-006, SPD-SEC-001, SPD-SEC-004, SPD-SEC-005, SPD-SEC-006, SPD-SEM-002.

Root normative question: Are extra findings independent and was external scope equal?

A interpretation: Golden/native surface plus 31 successful valid/edge external runs; event-ID exemption.

B interpretation: Run EPUBCheck on all 69 and retain duplicate-ID finding.

Resolved interpretation: Seven extra external aggregate findings are scope/reporting differences; the event duplicate is real and the exemption is a defect.

Primary classifications: NORMALIZATION_CONTRACT_BUG, VALIDATOR_A_BUG. Per-fixture exceptions and secondary classes are in fixture-differences.md.

## RESOURCE_INVENTORY_CASCADE — 4 fixtures

Affected fixtures: invalid/duplicate-normalized-path, invalid/path-traversal, invalid/unlisted-non-normative-resource, invalid/unlisted-normative-resource.

Affected IDs: SPD-BASE-002, SPD-RES-002, SPD-RES-003, SPD-RES-006.

Root normative question: Do ZIP rejection or resource roles suppress inventory rules?

A interpretation: Return on package errors; choose RES-003 or RES-006 by OPF filename presence.

B interpretation: Inspect inventory and report all overlaps.

Resolved interpretation: Unsafe/non-NFC strings are directly testable. Both inventory coverage rules include caches; no role-based division.

Primary classifications: NORMALIZATION_CONTRACT_BUG. Per-fixture exceptions and secondary classes are in fixture-differences.md.

## STATE_INTEGRITY_CASCADE — 10 fixtures

Affected fixtures: invalid/bad-resource-hash, invalid/mapping-with-stale-fixed, invalid/mutation-asset, invalid/mutation-css, invalid/mutation-fixed, invalid/mutation-mapping, invalid/mutation-semantic, invalid/sealed-after-annotation-modification, invalid/sealed-after-semantic-modification, invalid/stale-fixed-rendition.

Affected IDs: SPD-ANN-004, SPD-INT-003, SPD-INT-004, SPD-INT-005, SPD-RES-004, SPD-STATE-001, SPD-STATE-002, SPD-STATE-003, SPD-STATE-005, SPD-STATE-006, SPD-STATE-007.

Root normative question: Which equality failures and lifecycle predicates are established?

A interpretation: Often choose primary integrity or state finding and suppress overlaps.

B interpretation: Emit multiple equalities, plus generic sealed and stale-mapping labels.

Resolved interpretation: Retain measurable independent equalities; honor EDITABLE/SEALED, effects, and processor applicability. Do not infer semantic mutation from arbitrary seal failure.

Primary classifications: NORMALIZATION_CONTRACT_BUG, VALIDATOR_A_BUG, VALIDATOR_B_BUG. Per-fixture exceptions and secondary classes are in fixture-differences.md.

## MAPPING_GEOMETRY — 1 fixtures

Affected fixtures: invalid/mapping-invalid-geometry.

Affected IDs: SPD-MAP-011, SPD-MAP-012.

Root normative question: Can both linked geometry predicates be evaluated?

A interpretation: Bounds failure reported as MAP-011.

B interpretation: Bounds failure reported as MAP-011 and MAP-012.

Resolved interpretation: Valid finite quad shape does not prevent checking bounds; §§36 and 56 overlap. Define stable ID attribution in contract.

Primary classifications: NORMALIZATION_CONTRACT_BUG. Per-fixture exceptions and secondary classes are in fixture-differences.md.

## EXPERIMENTAL_CAPABILITY_REPORTING — 24 fixtures

See experimental-capability-differences.md for the complete fixture list. Affected field: Fixed-Experimental presence/status; no normative requirement-ID difference is attributed to this field. A uses presence, B uses explicit claim. Resolved as a NON_NORMATIVE report-model consistency issue, outside the comparison contract.
