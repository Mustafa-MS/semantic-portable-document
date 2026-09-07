# Format 0.1 conformance model summary

## 1. Is the Candidate Specification precise enough to implement independently?

**YES AFTER LISTED CLARIFICATIONS.** The architecture is coherent, but independent validators would currently disagree on identity syntax, revision-ID/digest semantics, inventory scope, digest bytes, mapping offsets/geometry/statuses, capability serialization, accessibility target, and annotation vocabulary.

## 2. How many normative requirements exist?

The registry contains **90** uppercase-derived or concretized requirements. Of these, **80** are document/processor conformance requirements and **10** are retained specification-governance requirements classified `INFORMATIVE_ONLY`.

Primary (exclusive) assignment is: Base 68, Mapping 12, Accessible 2, Fixed-Experimental 7, Archive-Experimental 1. Because requirements may apply to multiple capabilities, inclusive counts are: Base 68, Mapping 12, Accessible 12, Fixed-Experimental 11, Archive-Experimental 1. The inclusive counts intentionally overlap.

## 3. What percentage are fully automatable?

**54 of 80 executable requirements (67.5%)** are classified `AUTOMATED`. Against the entire 90-row registry, including governance, the figure is 60.0%. Another 20 are partially automatable, 6 require manual evaluation, and 10 are governance/informative-only.

## 4. What requirements still require human judgment?

Human review remains necessary for semantic intent, native-semantics applicability, meaningful alternative text/captions/labels, reading order and link purpose, general natural-language logical-order assessment, history-dependent copy/persistence behavior without lineage evidence, whether a fixed rendition acts as a second editable source, accessible fixed-export quality, and broad implementation/governance claims. Partial automation may collect evidence but cannot certify these qualities.

## 5. What specification ambiguities were found?

Seventeen ambiguity groups are recorded in `spec/AMBIGUITIES.md`: conformance scope, identity syntax, revision ID versus digest, lineage proof, language/direction applicability, inventory coverage, digest bytes/projection, semantic-only sealing conflict, stale/current serialization, mapping range unit/text extraction, geometry, status meanings, capability declaration, accessibility target, annotation namespace/draft dependency, visual-order Arabic detection, and native semantics applicability.

## 6. Did any ambiguity require an architectural change?

**No.** The one direct conflict is that the Candidate permits a sealed state without a fixed rendition while earlier ADR prose/diagrams imply fixed plus mapping is required. The recommendation follows the Candidate as primary truth and narrows Mapping dependency behavior; this is a clarification of lifecycle serialization, not an architectural reversal.

## 7. Are the proposed schemas sufficient?

**Yes for structural validation and validator implementation planning, not as the entire validator.** Draft 2020-12 schemas cover document/revision metadata, inventory entries, lifecycle binding, mapping shape/statuses, StableNodeSelector, and expected results. Procedural checks remain mandatory for ZIP safety, inventory coverage, hashes, DOM IDs, scalar range bounds, page references/geometry, semantic/accessibility quality, and cross-resource identity bindings.

## 8. Does EPUB 3.3 profiling create unresolved contradictions?

**No unresolved contradiction was found.** Stored/Deflate ZIP behavior, case-sensitive UTF-8 paths, OPF manifest/spine/navigation, XHTML, and local-resource packaging remain compatible. SPD adds stricter offline, active-content, normalized-duplicate, inventory, and lifecycle rules. Security resource limits remain configurable implementation policy rather than universal numeric format limits.

## 9. Is the mapping schema still a small correspondence model?

**Yes.** It contains identity, revision/fixed binding, status/provenance, page dimensions, logical ranges, quadrilaterals, and affine transforms. It excludes glyph commands, fonts, drawing operations, line breaking, and page-layout algorithms.

## 10. Are logical text ranges defined interoperably for Arabic/emoji/complex scripts?

**Yes in the proposed model, pending specification approval.** Ranges are zero-based, half-open Unicode scalar-value offsets over a precisely defined DOM-logical semantic text value. UTF-16 units are rejected as implementation-specific; grapheme clusters are useful UI boundaries but version-sensitive as an interchange unit. Fixtures cover Arabic/bidi, emoji ZWJ and flags, combining marks, Indic sequences, CJK, and vertical writing.

## 11. Is the integrity/state model unambiguous?

**The proposed model is; the Candidate alone is not.** Resource digests cover exact decompressed ZIP-entry bytes. Compression and ZIP timestamps do not affect resource identity. Revision ID is opaque, with a separate semantic-state digest. State binds the inventory and any current mapping/fixed artifacts; a self-excluding descriptor digest detects accidental state-metadata mutation. This is integrity only, not authentication or signature security.

## 12. Is the specification ready for validator implementation?

**READY AFTER SPEC CLARIFICATIONS.** The executable model, 90-row registry, schemas, profile documents, 10 valid fixtures, 27 invalid fixtures, 11 edge fixtures, five mutation classes, matrix, and verification tooling make the remaining decisions explicit. Validator implementation should begin only after the listed serialization/target choices are approved into the specification.

## Verification status

The corpus verifier confirms all valid/edge machine-readable artifacts against their schemas, exact inventory byte lengths and SHA-256 hashes, state-to-inventory bindings, OCF `mimetype` ordering/storage, expected-result schemas, known requirement IDs, and intentional identity-schema failures. EPUBCheck 5.3.0 reports 10/10 valid packages PASS. The production validator itself has not been built.

PROCEED TO FORMAT 0.1 SPEC CLARIFICATION
