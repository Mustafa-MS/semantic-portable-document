# Proposed Architecture Changes — Phase 1C

These are evidence-supported proposals only. AD-013's approved Phase 1B clarification was incorporated separately; no other accepted decision is changed here.

## P1C-01 — Fixed PDF status

Choose **C. PDF should remain the prototype/reference fixed rendition, but not yet become normative.**

The compiler proves exact visual preservation and large conformance gains, but T09 logical text is not interoperable across PDF.js, pypdf, pdfplumber, and MuPDF. A normative profile must not depend on a validator pass while common consumers disagree.

## P1C-02 — Restricted semantic compiler profile

Retain a candidate profile requiring authoritative XHTML, the revision/rendition-bound forward map, renderer-emitted MCIDs or an equivalent association channel, XHTML-derived PDF 2.0 structure, exact dual-raster visual preservation, and explicit PF/CF tests. Do not require a particular implementation mechanism.

## P1C-03 — Accessibility model

For Format 0.1 Base/Fixed, adopt **Model 1**: authoritative semantic XHTML is the accessibility source; fixed PDF is the visual canonical snapshot. Offer **Model 2** only through an Accessibility/Tagged-PDF capability with independent PDF/UA/WTPDF claims and synchronization checks.

Model 1 reduces duplicated accessibility state and works across non-PDF fixed renditions, but PDF-only export users may lose accessibility. Model 2 better matches user and legal expectations for standalone PDF exports, yet duplicates semantics and presently exposes consumer disagreement. Therefore a sealed package may rely on Model 1, while exported PDFs claiming accessibility must satisfy Model 2.

## P1C-04 — Archive scope

Require PDF/A-4 only for an **Archive capability**, not every sealed Fixed rendition. Ordinary Fixed documents should not inherit archival color/output-intent and metadata policy unless the archive claim is requested.
