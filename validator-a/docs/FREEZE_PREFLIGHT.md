# Freeze preflight

- Draft/registry: the 113 IDs remain stable. Registry metadata now names
  `0.1-draft` and `spec/FORMAT_0.1_DRAFT.md`.
- Archive dependency metadata now requires Base, SEALED, and a current
  archive-appropriate fixed rendition; no separate Fixed-Experimental claim.
- Canonical schemas: `document-state`, `resource-inventory`, `state`, `mapping`,
  `annotation-extension`, and `conformance-result`.
- Historical Phase 1 schemas are explicitly excluded in `schemas/README.md`.
- Corpus: 69/69 fixtures are deterministically indexed (18 valid, 38 invalid,
  13 edge); every package and expected-result path resolves.
- Requirements: 113 unique IDs; 74 automated, 22 partially automated, 6 manual,
  11 informative.

## Resolved corpus issue

Independent review classified the former Accessible disagreement as a
`CORPUS_EXPECTATION_ERROR`, not a specification blocker. The fixture now expects
`Accessible: NOT_TESTED`, matching Draft sections 58 and 74. No human-evidence
format was invented, validator accessibility semantics were not weakened, and no
normative file was changed. Open specification blockers: **0**.
