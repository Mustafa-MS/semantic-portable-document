# Tagged PDF structure results

The compiler rebuilds a single PDF 2.0 namespace `Document` tree in XHTML logical order, creates MCR dictionaries and a new parent tree, classifies unowned page content as artifacts, attaches XHTML node IDs externally and through experimental `/ID`, supplies figure `Alt`, and emits table/list attributes.

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

## Representative structure inventory

- T03 roles: `{'Caption': 1, 'Document': 1, 'H1': 1, 'P': 28, 'Sect': 1, 'TBody': 1, 'TD': 56, 'TH': 32, 'THead': 1, 'TR': 30, 'Table': 1}`
- T08 roles: `{'Caption': 2, 'Document': 1, 'FENote': 1, 'Figure': 1, 'H1': 1, 'P': 1, 'Sect': 1, 'TD': 2, 'TH': 2, 'TR': 2, 'Table': 1}`
- T12 roles: `{'Caption': 2, 'Document': 1, 'Figure': 1, 'H1': 1, 'H2': 1, 'H3': 1, 'L': 1, 'LBody': 1, 'LI': 1, 'Lbl': 1, 'Link': 1, 'P': 1, 'Sect': 3, 'TD': 1, 'TH': 3, 'TR': 2, 'Table': 1}`

Remaining failures, if any, are exact validator findings below rather than generic “tagged/not tagged” claims.

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
