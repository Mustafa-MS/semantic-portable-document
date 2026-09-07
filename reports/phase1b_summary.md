# Phase 1B Summary

## 1. Forward mapping gate

**YES.** VERIFIED BY TEST: visible-node macro coverage 100.0%, logical-range
coverage 100.0%, and T08/T09 minimum node/range coverage 100.0%/100.0%.

## 2. MF versus PF

Forward Arabic mapping passes independently of PDF extraction. Best observed normalized Arabic PDF
phrase recovery was 77.8%. A mapping pass does not erase a PDF text failure.

## 3. Renderer independence

Paged.js provided paginated-DOM identity/range geometry. WeasyPrint 69 provided a substantially
independent fixed-PDF path. Their appearance, pagination, tagging, and extraction are not assumed equal.

## 4. Required architectural question

**Should mapping be an output artifact with implementation-specific generation? YES.**

Proposed wording (not applied to the approved ADR):

> A fixed-rendition processor SHALL emit a revision- and rendition-bound semantic-to-fixed mapping
> as an output of rendering when the mapping profile is claimed. The generation mechanism is
> implementation-specific and non-normative. Reconstruction from the fixed rendition MAY be used
> for independent validation or recovery, but SHALL NOT be the required mapping-generation method.

## 5. Tagged PDF 2.0 reference question

**UNCERTAIN.** veraPDF UA-2/Tagged PDF, WTPDF, and PDF/A-4 observations are reported separately;
structure-tree presence alone was not used. A viable profile must name the generation/validation
requirements that actually passed and retain Arabic PF tests.

## 6. EPUB 3.x OCF question

**YES WITH PROFILE RESTRICTIONS.** EPUBCheck: 12/12 PASS.
Full-corpus independent reader implementations: 2; representative manual reader trials:
calibre E-book viewer 5/5.
Unknown resources remained
inactive, but ordinary readers did not expose sealed/fixed lifecycle state.

## 7. Mapping-size kill criterion

**SMALL CORRESPONDENCE LAYER.** The artifact contains identity/range/page/quad correspondence and transforms,
not glyph drawing commands, line-breaking rules, fonts, or a second scene description.

## 8. T10 R1 to R2 regression

- Document ID preserved: True
- Target IDs and new hashes: True / True
- Revision and fixed rendition changed: True / True
- Old map invalid for R2: True
- Unrelated semantic changes: 0
- Unchanged-node page agreement: 100.0%

## 9. Remaining gates

Clipboard and screen-reader behavior remain NOT VERIFIED. Reader sealed-state UX, any failed formal
profiles, extractor differences, and geometry cross-check deviations must remain explicit.

## Final recommendation

**RUN ANOTHER TARGETED RESEARCH PHASE**
