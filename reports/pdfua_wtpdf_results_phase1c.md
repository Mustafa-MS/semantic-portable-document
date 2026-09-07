# PDF/UA-2 and WTPDF results — Phase 1C

| Fixture | Candidate | Profile | Result | Failed rules | Failed checks |
|---|---|---:|---:|---:|---:|
| T03 | compiled | ua2 | PASS | 0 | 0 |
| T04 | compiled | ua2 | PASS | 0 | 0 |
| T08 | compiled | ua2 | PASS | 0 | 0 |
| T08 | compiled | wt1a | PASS | 0 | 0 |
| T08 | compiled | wt1r | PASS | 0 | 0 |
| T09 | compiled | ua2 | PASS | 0 | 0 |
| T09 | compiled | wt1a | PASS | 0 | 0 |
| T09 | compiled | wt1r | PASS | 0 | 0 |
| T10 | compiled | 4 | FAIL | 4 | 50 |
| T10 | compiled | ua2 | PASS | 0 | 0 |
| T10 | compiled | wt1a | PASS | 0 | 0 |
| T10 | compiled | wt1r | PASS | 0 | 0 |
| T12 | compiled | ua2 | PASS | 0 | 0 |
| T12 | compiled | wt1a | PASS | 0 | 0 |
| T12 | compiled | wt1r | PASS | 0 | 0 |
| T08 | fop | ua1 | PASS | 0 | 0 |
| T08 | fop | ua2 | FAIL | 3 | 3 |
| T09 | fop | ua1 | PASS | 0 | 0 |
| T09 | fop | ua2 | FAIL | 3 | 3 |
| T10 | fop | ua1 | PASS | 0 | 0 |
| T10 | fop | ua2 | FAIL | 5 | 5 |
| T12 | fop | ua1 | PASS | 0 | 0 |
| T12 | fop | ua2 | FAIL | 5 | 5 |

## Interpretation

Compiled PDFs declare PDF/UA-2 through XMP only for the experiment and are labelled conformant only where veraPDF passes. WTPDF reuse and accessibility are separate claims. A clean automated report does not resolve human checks or the demonstrated T09 extractor behavior.

## Exact residual diagnostics

### fop T08 — ua2

- `ISO 14289-2:2024` 8.2.5.2/2: 1 failed checks — The structure tree root shall contain a single Document structure element as its only child. The namespace for that element shall be specified as the PDF 2.0 namespace

- `ISO 14289-2:2024` 5/2: 1 failed checks — The value of "pdfuaid:part" shall be the part number of the International Standard to which the file conforms

- `ISO 14289-2:2024` 5/5: 1 failed checks — The value of "pdfuaid:rev" shall be "2024"

### fop T09 — ua2

- `ISO 14289-2:2024` 5/5: 1 failed checks — The value of "pdfuaid:rev" shall be "2024"

- `ISO 14289-2:2024` 5/2: 1 failed checks — The value of "pdfuaid:part" shall be the part number of the International Standard to which the file conforms

- `ISO 14289-2:2024` 8.2.5.2/2: 1 failed checks — The structure tree root shall contain a single Document structure element as its only child. The namespace for that element shall be specified as the PDF 2.0 namespace

### fop T10 — ua2

- `ISO 14289-2:2024` 8.2.5.25/1: 1 failed checks — If Lbl structure elements are present, the ListNumbering attribute shall be present on the respective L structure element; in such cases the value None shall not be used

- `ISO 14289-2:2024` 5/5: 1 failed checks — The value of "pdfuaid:rev" shall be "2024"

- `ISO 32005:2023` Table 5. Lbl-P/1: 1 failed checks — <Lbl> shall not contain <P>

- `ISO 14289-2:2024` 8.2.5.2/2: 1 failed checks — The structure tree root shall contain a single Document structure element as its only child. The namespace for that element shall be specified as the PDF 2.0 namespace

- `ISO 14289-2:2024` 5/2: 1 failed checks — The value of "pdfuaid:part" shall be the part number of the International Standard to which the file conforms

### fop T12 — ua2

- `ISO 32005:2023` Table 5. Lbl-P/1: 1 failed checks — <Lbl> shall not contain <P>

- `ISO 14289-2:2024` 5/5: 1 failed checks — The value of "pdfuaid:rev" shall be "2024"

- `ISO 14289-2:2024` 5/2: 1 failed checks — The value of "pdfuaid:part" shall be the part number of the International Standard to which the file conforms

- `ISO 14289-2:2024` 8.2.5.25/1: 1 failed checks — If Lbl structure elements are present, the ListNumbering attribute shall be present on the respective L structure element; in such cases the value None shall not be used

- `ISO 14289-2:2024` 8.2.5.2/2: 1 failed checks — The structure tree root shall contain a single Document structure element as its only child. The namespace for that element shall be specified as the PDF 2.0 namespace
