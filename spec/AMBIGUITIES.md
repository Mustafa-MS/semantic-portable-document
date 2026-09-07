# Format 0.1 ambiguity disposition

This file preserves the Candidate-stage analysis. A-001 through A-017 are resolved normatively in `FORMAT_0.1_DRAFT.md` by the approved directions described below. A-018 through A-023, discovered during Draft freeze, are also resolved. No open algorithmic ambiguity remains. Stable public identifiers remain a Release Candidate blocker, not a Draft interpretation ambiguity.

| IDs | Draft disposition |
|---|---|
| A-001–A-017 | APPROVED or APPROVED WITH MODIFICATION as recorded in the Candidate-to-Draft diff. |
| A-018 | OCF `container.xml` links with exact provisional relationship tokens and `application/json`. |
| A-019 | Exactly one rootfile; its spine is authoritative. |
| A-020 | Capability status removed from document control. |
| A-021 | Current fixed does not imply Mapping; Mapping claim cross-requires current fixed plus mapping. |
| A-022 | Complete cycle-free inventory/state/JCS digest graph. |
| A-023 | Packaged annotation edits invalidate seal without creating semantic revision. |

## A-001 — Conformance scope of broad architecture clauses

- **Requirement ID:** SPD-ARCH-003
- **Section:** 1, 4, 68
- **Current wording:** “Existing standards SHALL be reused wherever practical.”
- **Problem:** “Practical” cannot yield a document-level pass/fail result.
- **Interpretation A:** Treat it as a conformance requirement.
- **Interpretation B:** Treat it as project governance and traceability direction.
- **Recommended clarification:** Mark these clauses as specification-development requirements (`INFORMATIVE_ONLY` in the registry).
- **Architecture change:** No.

## A-002 — Identity serialization

- **Requirement IDs:** SPD-ID-001, SPD-ID-002, SPD-ID-005
- **Sections:** 11–14
- **Current wording:** Persistent Document, Revision, and Node IDs are required, but syntax is absent.
- **Problem:** Implementations cannot agree which strings are valid.
- **Interpretation A:** Opaque URI for all identities.
- **Interpretation B:** UUID URNs for document/revision and an XML-compatible `n_` token for nodes.
- **Recommended clarification:** Adopt B for 0.1; allow future URI-based extension through a versioned schema.
- **Architecture change:** Clarification only.

## A-003 — Revision ID versus digest

- **Requirement IDs:** SPD-ID-002, SPD-ID-003, SPD-INT-001
- **Sections:** 12, 29
- **Current wording:** Revision IDs identify immutable state; integrity uses SHA-256.
- **Problem:** It does not say whether the ID is opaque or a digest.
- **Interpretation A:** Revision ID equals a semantic-state digest.
- **Interpretation B:** Opaque Revision ID plus a separate digest.
- **Recommended clarification:** Adopt B. It matches persistent identity separation, permits algorithms to evolve, and avoids inventing canonicalization as identity.
- **Architecture change:** No; it makes an implicit separation explicit.

## A-004 — Node persistence across lineage

- **Requirement IDs:** SPD-ID-005, SPD-ID-006, SPD-ID-009
- **Sections:** 13–15
- **Current wording:** IDs are persistent and unique within a lineage; copy/split/merge rules are mostly advisory.
- **Problem:** A single package normally cannot prove history-wide uniqueness or whether a node was copied.
- **Interpretation A:** Current-package validation is sufficient.
- **Interpretation B:** Editors must validate against retained lineage history; standalone validators report history-dependent rules `NOT_TESTED` when history is unavailable.
- **Recommended clarification:** Adopt B and distinguish document validity from editor behavior conformance.
- **Architecture change:** No.

## A-005 — Required language and direction metadata

- **Requirement IDs:** SPD-I18N-003, SPD-I18N-004
- **Section:** 16
- **Current wording:** Metadata is required “where required/necessary.”
- **Problem:** Applicability is undefined.
- **Interpretation A:** Root `lang`/`xml:lang` and `dir` always required.
- **Interpretation B:** Root language always required; direction required on the root or nearest element when Unicode bidi defaults do not convey intended paragraph direction.
- **Recommended clarification:** Require matching root `lang` and `xml:lang`; require `dir` for RTL base paragraphs and direction changes not inferable from content.
- **Architecture change:** No.

## A-006 — Inventory coverage

- **Requirement IDs:** SPD-RES-001, SPD-RES-003
- **Section:** 28
- **Current wording:** One “normative resource inventory” is required, but it is unclear whether every ZIP entry is listed.
- **Problem:** Validators cannot detect an “unlisted normative resource” consistently.
- **Interpretation A:** Inventory every ZIP entry including container plumbing.
- **Interpretation B:** Inventory every conformance-affecting or authoritatively required resource; permit omitted cache resources and specified OCF plumbing.
- **Recommended clarification:** Adopt B. Explicitly exclude `mimetype`, `META-INF/container.xml`, and resources declared `non-normative`; require all manifest resources and all state/mapping/fixed artifacts.
- **Architecture change:** No.

## A-007 — Digest bytes and semantic-state digest

- **Requirement IDs:** SPD-RES-004, SPD-INT-001–003
- **Sections:** 28–29
- **Current wording:** SHA-256 is required without defining the byte stream.
- **Problem:** ZIP compression and metadata could produce different results for identical resources.
- **Interpretation A:** Hash raw compressed entry records/container bytes.
- **Interpretation B:** Hash exact decompressed resource bytes; compute state digest over a deterministic inventory projection.
- **Recommended clarification:** Adopt B. Do not normalize text or XML. ZIP timestamps/compression do not affect resource digests. Define state digest as UTF-8 over sorted `path\0byteLength\0sha256\n` records for included resources, excluding the descriptor field that contains the digest.
- **Architecture change:** No; matches Phase 1 exact resource-byte experiments.

## A-008 — Sealed state with no fixed rendition

- **Requirement ID:** SPD-STATE-002
- **Section:** 27 versus approved ADR AD-016/017
- **Current wording:** Candidate says fixed rendition is optional; ADR diagrams and prose describe sealing as including fixed, mapping, and provenance.
- **Problem:** This is an actual source conflict.
- **Interpretation A:** Any semantic-only revision can be sealed.
- **Interpretation B:** `SEALED` requires fixed plus mapping.
- **Recommended clarification:** Follow the Candidate (A) as primary truth, but state that claiming Mapping requires a current fixed rendition and mapping. Record the ADR conflict explicitly.
- **Architecture change:** Clarification of the Candidate; earlier ADR wording needs alignment.

## A-009 — Fixed status serialization

- **Requirement ID:** SPD-STATE-001
- **Section:** 26
- **Current wording:** A fixed rendition may be absent or stale, but no serialization exists.
- **Problem:** A reader cannot reliably distinguish current/stale/absent.
- **Interpretation A:** Infer from Revision IDs.
- **Interpretation B:** Declare `status` and also verify revision/digest bindings.
- **Recommended clarification:** Adopt B; an incorrect `current` declaration is a conformance error.
- **Architecture change:** No.

## A-010 — Mapping range unit and node text extraction

- **Requirement IDs:** SPD-MAP-008, SPD-I18N-006
- **Sections:** 17, 36–40
- **Current wording:** “logical Unicode range” has no unit or text-extraction algorithm.
- **Problem:** UTF-8 bytes, UTF-16 units, scalar values, and grapheme clusters disagree for emoji and complex scripts.
- **Interpretation A:** UTF-16 DOM offsets for implementation convenience.
- **Interpretation B:** Half-open Unicode scalar-value offsets over a defined semantic text value.
- **Recommended clarification:** Adopt B. Scalar values are deterministic across languages; grapheme segmentation changes across Unicode versions and UTF-16 is JavaScript-specific. Renderers translate local APIs at boundaries.
- **Architecture change:** No.

## A-011 — Mapping geometry

- **Requirement ID:** SPD-MAP-011
- **Sections:** 36–37, 56
- **Current wording:** Quadrilateral, transform, page ID, and “valid geometry” are not formalized.
- **Problem:** Origin, units, ordering, precision, and bounds are unknown.
- **Interpretation A:** PDF points/bottom-left.
- **Interpretation B:** Page-local CSS reference pixels/top-left, clockwise points, optional affine transform to fixed coordinates.
- **Recommended clarification:** Adopt B because forward renderers emit CSS geometry; require explicit page dimensions and transform. Accept finite decimals; comparison tolerance is validator policy, not validity.
- **Architecture change:** No and not Chromium-specific.

## A-012 — Mapping status distinctions

- **Requirement ID:** SPD-MAP-005
- **Section:** 38
- **Current wording:** Status names are listed without definitions.
- **Problem:** `NOT_VISIBLE`, `UNMAPPABLE`, and `UNSUPPORTED` may be conflated.
- **Interpretation A:** All mean no geometry.
- **Interpretation B:** Distinguish intentional non-visibility, representational impossibility/failure with supported input, and unsupported semantic/layout feature.
- **Recommended clarification:** Adopt the definitions in `profiles/mapping-profile.md` (also summarized in the mapping schema documentation).
- **Architecture change:** No.

## A-013 — Capability declaration location

- **Requirement ID:** SPD-CAP-001
- **Sections:** 54–60
- **Current wording:** Capability names exist but no package serialization or dependency processing is defined.
- **Problem:** Validators cannot detect claims.
- **Interpretation A:** New standalone metadata only.
- **Interpretation B:** EPUB package `meta property="dcterms:conformsTo"` links plus the document-state JSON for machine constraints.
- **Recommended clarification:** Adopt B: reuse EPUB metadata for discovery; make document-state JSON authoritative for version/status/dependencies.
- **Architecture change:** No.

## A-014 — Accessible capability target level

- **Requirement IDs:** SPD-ACC-001–003
- **Sections:** 42–43, 58
- **Current wording:** Accessibility authority is identified, but no WCAG version/level or EPUB Accessibility conformance target is chosen.
- **Problem:** “Accessible” cannot produce a determinate PASS.
- **Interpretation A:** Structural checks only.
- **Interpretation B:** EPUB Accessibility 1.1 plus a declared WCAG 2.2 level, with manual checks retained.
- **Recommended clarification:** Require a declared target; recommend EPUB Accessibility 1.1 and WCAG 2.2 AA for 0.1 after approval.
- **Architecture change:** No.

## A-015 — Annotation namespace and EPUB Annotations dependency

- **Requirement ID:** SPD-ANN-001
- **Sections:** 22–24
- **Current wording:** A namespace will be registered; the Candidate references Web Annotation but predates a stable EPUB Annotations recommendation.
- **Problem:** `StableNodeSelector` has no registered IRI and EPUB Annotations 1.0 is a 2026 Working Draft.
- **Interpretation A:** Normatively depend on the draft.
- **Interpretation B:** Normatively use Web Annotation and define only a provisional extension; monitor EPUB Annotations.
- **Recommended clarification:** Adopt B. Align serialization shapes where possible but do not normatively depend on the draft.
- **Architecture change:** No.

## A-016 — Detecting visual-order Arabic

- **Requirement ID:** SPD-I18N-001
- **Section:** 16–17
- **Current wording:** Logical Unicode order is mandatory.
- **Problem:** Arbitrary natural-language text cannot always be classified as logically versus visually ordered without an oracle.
- **Interpretation A:** Fully automated linguistic detection.
- **Interpretation B:** Automated checks for known fixtures and suspicious bidi controls, plus human/source-reference evaluation for arbitrary prose.
- **Recommended clarification:** Classify general enforcement as partially automated; retain deterministic negative corpus cases.
- **Architecture change:** No.

## A-017 — Native semantics applicability

- **Requirement IDs:** SPD-SEM-004–006, SPD-SEM-012–013
- **Sections:** 8–9, 20
- **Current wording:** Native semantics are required “where those semantics exist.”
- **Problem:** Semantic intent is not always inferable from markup.
- **Interpretation A:** Validator infers author intent.
- **Interpretation B:** Automated anti-pattern rules plus manual review of meaning.
- **Recommended clarification:** Adopt B and keep these `PARTIALLY_AUTOMATED`.
- **Architecture change:** No.
