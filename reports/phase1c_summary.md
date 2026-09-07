# Phase 1C summary

## Outcome

The compiler preserved the Paged.js visual page scene across six representative fixtures: dual-raster exactness was **True**, and non-semantic drawing-operator preservation was **True**. The automated PDF/UA-2 result was 6/6 compiled representatives. Apache FOP provided an independent accessibility-aware generator and reached 4/4 PDF/UA-1 automated passes.

The decisive negative evidence is PF interoperability. `/ActualText` placement that passes formal validation is not consistently honored by PDF.js, pypdf, or pdfplumber, and MuPDF still reorders the first T09 mixed-bidi sentence. VF, PF, and CF therefore remain separate.

## Preserved Phase 1B findings

- forward visible-node coverage: 100%
- forward logical-range coverage: 100%
- valid fixed-page fragments: 3,094/3,094
- T08 and T09 mapping: 100%
- mapping: SMALL CORRESPONDENCE LAYER
- EPUB OCF: YES WITH PROFILE RESTRICTIONS

## Required architecture decisions

**Semantic compilation:** UNCERTAIN. It can preserve pixels and create formally strong structure without re-rendering, but cannot yet guarantee interoperable logical T09 text.

**PDF role:** C. PDF should remain the prototype/reference fixed rendition, but not yet become normative.

**Accessibility:** Base/Fixed uses Model 1 (semantic XHTML accessible; PDF is the canonical visual snapshot). Model 2 is required for any standalone PDF export that claims accessibility and remains a capability/profile with explicit PDF/UA/WTPDF checks.

**Archive:** PDF/A-4 is mandatory only for an Archive capability.

## Gates

- Mapping: PASS, preserved from Phase 1B.
- VF: PASS.
- T08 PF: see extractor-specific ratios; no normalization masking.
- T09 PF: FAIL for cross-consumer interoperability.
- CF: automated results are reported by profile; human accessibility checks remain outside veraPDF.
- Complexity: still semantic compilation, with a renderer-MCID adapter and an interoperability warning.

## Recommendation

PROCEED TO FORMAT 0.1 WITH FIXED-PDF PROFILE STILL EXPERIMENTAL
