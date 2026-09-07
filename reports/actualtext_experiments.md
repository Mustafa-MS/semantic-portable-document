# ActualText experiments

## Strategies

- **A — structure element:** `/ActualText` is placed on XHTML-derived structure elements. It leaves the content stream semantically untouched.
- **B — existing marked content:** logical replacement is attached to Chromium's existing MCID sequences without changing drawing operators.
- **C — nested Span (selected experiment):** renderer-internal character wrappers are flattened, then a `Span` `/ActualText` wrapper encloses unchanged text operators within one MCID. Remaining MCIDs for the semantic element use empty replacement spans to avoid duplicate accessible content. The logical replacement is anchored at the first stream-order text sequence because that gave the best tested MuPDF behavior.
- **Negative control rejected:** no invisible duplicate/OCR text layer was added.

| Fixture | Strategy | PDF.js | pypdf | pdfplumber | MuPDF | veraPDF UA-2 |
|---|---|---:|---:|---:|---:|---:|
| T08 | structure | 11.1% | 0.0% | 0.0% | 33.3% | PASS |
| T08 | marked-content | 11.1% | 0.0% | 0.0% | 0.0% | PASS |
| T09 | structure | 0.0% | 0.0% | 0.0% | 0.0% | PASS |
| T09 | marked-content | 0.0% | 0.0% | 0.0% | 50.0% | PASS |

## Interpretation

Structure-level `/ActualText` does not repair ordinary library extraction in the tested tools. Marked-content placement can be formally valid and can improve MuPDF, but PDF.js, pypdf, and pdfplumber do not consistently honor the logical replacement. T09 proves that validator success is not sufficient evidence of correct bidi extraction. The selected placement is retained as a standards-valid experiment, not as a universal interoperability solution.
