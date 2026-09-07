# Specialist PDF Validation - Phase 1B

**VERIFIED BY TEST** using veraPDF 1.30.2.

| Document | Renderer | Profile | Result | Failed rules | Failed checks |
| --- | --- | --- | --- | ---: | ---: |
| T03 | chromium | ua2 | FAIL | 4 | 6 |
| T03 | pagedjs | ua2 | FAIL | 5 | 13 |
| T03 | weasyprint | ua2 | FAIL | 2 | 4 |
| T08 | chromium | ua2 | FAIL | 6 | 6 |
| T08 | chromium | wt1a | FAIL | 6 | 6 |
| T08 | chromium | wt1r | FAIL | 5 | 5 |
| T08 | pagedjs | ua2 | FAIL | 7 | 9 |
| T08 | pagedjs | wt1a | FAIL | 7 | 9 |
| T08 | pagedjs | wt1r | FAIL | 6 | 8 |
| T08 | weasyprint | ua2 | FAIL | 3 | 3 |
| T08 | weasyprint | wt1a | FAIL | 4 | 4 |
| T08 | weasyprint | wt1r | FAIL | 4 | 4 |
| T09 | chromium | ua2 | FAIL | 3 | 3 |
| T09 | pagedjs | ua2 | FAIL | 4 | 8 |
| T09 | weasyprint | ua2 | FAIL | 1 | 1 |
| T10 | chromium | 4 | FAIL | 6 | 50 |
| T10 | chromium | ua2 | FAIL | 6 | 6 |
| T10 | chromium | wt1a | FAIL | 6 | 6 |
| T10 | chromium | wt1r | FAIL | 5 | 5 |
| T10 | pagedjs | 4 | FAIL | 6 | 50 |
| T10 | pagedjs | ua2 | FAIL | 7 | 13 |
| T10 | pagedjs | wt1a | FAIL | 7 | 13 |
| T10 | pagedjs | wt1r | FAIL | 6 | 12 |
| T10 | weasyprint | 4 | FAIL | 4 | 50 |
| T10 | weasyprint | ua2 | FAIL | 2 | 6 |
| T10 | weasyprint | wt1a | FAIL | 3 | 7 |
| T10 | weasyprint | wt1r | FAIL | 3 | 7 |
| T12 | chromium | ua2 | FAIL | 7 | 8 |
| T12 | pagedjs | ua2 | FAIL | 7 | 13 |
| T12 | weasyprint | ua2 | FAIL | 4 | 7 |

The WeasyPrint PDF/A-4u disposable generation experiment validated against veraPDF profile 4 as
**FAIL**. UA-2 validation includes Tagged
PDF requirements. `wt1r` and `wt1a` are WTPDF reuse/accessibility profiles. A failed profile is
reported as evidence, not repaired or reclassified.

Most frequent exact validator diagnostics:

- 16 result(s): ISO 32005:2023 Table 5. Table-content: <Table> shall not contain content items
- 11 result(s): ISO 14289-2:2024 8.8: All destinations whose target lies within the current document shall be structure destinations
- 10 result(s): ISO 14289-2:2024 8.2.5.2: The structure tree root shall contain a single Document structure element as its only child. The namespace for that element shall be specified as the PDF 2.0 namespace
- 10 result(s): ISO 14289-2:2024 8.2.2: Content that is not considered real shall be an artifact
- 10 result(s): ISO 14289-2:2024 8.11.1: The Catalog dictionary of a conforming file shall contain the Metadata key whose value is a metadata stream as defined in ISO 32000-2:2020, 14.3. The metadata stream dictionary shall contain entry Type with value /Metadata and entry Subtype with value /XML
- 8 result(s): WTPDF1.0 8.2.5.2: The structure tree root shall contain a single Document structure element as its only child. The namespace for that element shall be specified as the PDF 2.0 namespace
- 8 result(s): WTPDF1.0 8.2.2: Content that is not considered real shall be an artifact
- 8 result(s): WTPDF1.0 8.11.1: The Catalog dictionary of a conforming file shall contain the Metadata key whose value is a metadata stream as defined in ISO 32000-2:2020, 14.3. The metadata stream dictionary shall contain entry Type with value /Metadata and entry Subtype with value /XML

Disposable WeasyPrint PDF/A-4u diagnostics:

- ISO 19005-4:2020 6.7.3: A file that does not conform to either PDF/A-4e or PDF/A-4f shall not provide any "pdfaid:conformance"
- ISO 19005-4:2020 6.2.7.1: If an Image dictionary contains the Interpolate key, its value shall be false. For an inline image, the I key, if present, shall have a value of false
