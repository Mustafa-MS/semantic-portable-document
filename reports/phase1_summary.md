# Phase 1 Summary

## 1. Is EPUB OCF Still a Good Container Basis?

**UNCERTAIN.** VERIFIED BY TEST: 12 experimental packages passed the internal
OCF/ZIP/XML profile. NOT VERIFIED: EPUBCheck and two-reader interoperability were not run.

## 2. Is XHTML Still a Good Authoritative Semantic Representation?

**YES for continued experimentation.** VERIFIED BY TEST: all 12 fixtures represented the scoped
semantics, stable IDs, language/direction, and transactional edits without duplicate content stores.

## 3. Can Existing Renderers Produce an Acceptable Fixed Rendition?

- Chromium: **Suitable with post-processing/research limitations** - rendered 12/12, but tagging quality and formal conformance are not proven.
- WeasyPrint: **Unknown** - not installed.
- Vivliostyle/Paged.js class: **Unknown** - not installed.

## 4. Is Tagged PDF Suitable as the Reference Fixed Rendition?

**UNCERTAIN.** Chromium exposed a structure tree in 12/12 PDFs, but a
structure-tree flag alone does not establish useful tags, PDF/UA-2, WTPDF, or PDF/A-4 conformance.

## 5. Is Semantic-to-Fixed Mapping Practically Achievable?

**Partially.** VERIFIED BY TEST: exact extracted-token mapping averaged 62.6% coverage.
Failures remain observable. Geometry derived from PDF extraction is useful but renderer/extractor-dependent.

## 6. Does the Minimal Mapping Model Need Expansion?

**Yes, experimentally.** It needs explicit uncertainty/provenance, parent-child overlap rules,
cluster/bidi-aware text anchors, non-text vector regions, and a way to state “not mapped” without
turning layout into a second source of truth.

## 7. Does Arabic/RTL Work Correctly?

- Semantic source: **verified** for logical Unicode plus `lang`/`dir`.
- Rendering: **observed in Chromium; human visual QA required**.
- PDF extraction: exact logical phrases 0/19.
- Mapping: measured per T08/T09 in `rtl_results.md`.
- Copy/paste: **not verified**.
- Accessibility: structure indicators observed; semantic quality/conformance **not verified**.

## 8. Can Semantic-Fixed Equivalence Be Validated?

**Partially.** Structural presence, normalized text similarity, mapped cell presence, link counts,
hash/revision binding, and limited RTL exact matches are automatable. Visual meaning, complete table
relationships, MathML meaning, alt-text propagation, reading order, and accessibility equivalence
cannot be proven by these checks.

## 9. Does Stable Identity Provide a Measurable Advantage?

**Yes within the fixture.** VERIFIED BY TEST: the Table 4 cell kept its ID across an edit while
its content hash and revision changed, allowing exact targeting and zero unrelated node changes.
Comparative agent trials against B1-B4 remain unrun.

## 10. Does the Transaction Model Prevent Unsafe Stale Edits?

**YES in the minimal API.** Revision and node-hash conflicts were rejected before commit, and the
source bytes remained unchanged.

## 11. Are Conventional EPUB Readers Compatible Enough?

**UNCERTAIN.** No independent reader trials were available.

## 12. Biggest New Technical Risk

Mapping quality depends on extraction order and geometric fidelity, especially for bidi text,
MathML, SVG/vector content, and nested semantic objects. Fixing this could pull the mapping layer
toward renderer-specific complexity.

## 13. Recommended Architecture Changes

Do not change the accepted baseline yet. Add experimental mapping confidence/provenance fields and
define explicit partial/unmappable outcomes before proposing a normative change.

## 14. Proceed / Modify / Stop

**PROCEED**

Proceed only to a broader Phase 1 run with the missing renderers, EPUBCheck/readers, and expert PDF
validators. The local results establish coherence of the narrow harness but are insufficient for a
format specification or superiority claim.
