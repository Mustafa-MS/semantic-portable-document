# Backward vs Forward Mapping Ablation

**VERIFIED BY TEST.** A is the retained `pdfplumber` token matcher. B is explicit Paged.js identity
and logical-range propagation. Both were also run against the same Paged.js PDF where possible.

| Document | Phase 1 backward | A on Paged PDF | B forward nodes | B cells | B MathML | B figures | A mapped nodes | B ms |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| T01 | 75.0% | 75.0% | 100.0% | 100.0% | 100.0% | 100.0% | 6 | 5161.9 |
| T02 | 75.0% | 75.0% | 100.0% | 100.0% | 100.0% | 100.0% | 3 | 10281.2 |
| T03 | 80.0% | 81.3% | 100.0% | 100.0% | 100.0% | 100.0% | 122 | 4368.7 |
| T04 | 71.4% | 71.4% | 100.0% | 100.0% | 100.0% | 100.0% | 5 | 4086.2 |
| T05 | 50.0% | 50.0% | 100.0% | 100.0% | 100.0% | 100.0% | 3 | 4796.9 |
| T06 | 66.7% | 66.7% | 100.0% | 100.0% | 100.0% | 100.0% | 4 | 7719.1 |
| T07 | 70.0% | 70.0% | 100.0% | 100.0% | 100.0% | 100.0% | 7 | 9794.8 |
| T08 | 7.1% | 7.1% | 100.0% | 100.0% | 100.0% | 100.0% | 1 | 5581.5 |
| T09 | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0 | 4282.4 |
| T10 | 84.0% | 84.0% | 100.0% | 100.0% | 100.0% | 100.0% | 21 | 3879.3 |
| T11 | 82.3% | 82.3% | 100.0% | 100.0% | 100.0% | 100.0% | 14 | 5427.8 |
| T12 | 89.5% | 89.5% | 100.0% | 100.0% | 100.0% | 100.0% | 17 | 4810.9 |

Forward mapping materially improves node, Arabic, table-cell, MathML equation, and vector-figure
coverage because it does not require recoverable PDF strings or raster image objects. Its cost is
renderer-specific instrumentation and more range fragments. The output model itself is renderer-
independent. The backward mapper remains valuable as an independent geometry/text cross-check, not
as the normative generation mechanism.
