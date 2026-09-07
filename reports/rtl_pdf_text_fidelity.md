# Arabic PDF Text Fidelity

**VERIFIED BY TEST** for pypdf, pdfplumber, and PDF.js. Poppler `pdftotext` is **NOT VERIFIED**
because that executable is absent from the bundled Poppler runtime. Raw, NFC, and NFKC output is
preserved per PDF under `corpus/generated/phase1b/text/`; normalization is never treated as an order fix.

| Doc | Renderer | Extractor | Raw exact phrases | NFKC recovery | Base Arabic CMap | Presentation forms | ActualText |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| T08 | chromium | pdfjs | 0/9 | 0.0% | 24 | 57 | 0 |
| T08 | chromium | pdfplumber | 0/9 | 0.0% | 24 | 57 | 0 |
| T08 | chromium | pypdf | 0/9 | 55.6% | 24 | 57 | 0 |
| T08 | pagedjs | pdfjs | 0/9 | 0.0% | 24 | 57 | 0 |
| T08 | pagedjs | pdfplumber | 0/9 | 0.0% | 24 | 57 | 0 |
| T08 | pagedjs | pypdf | 0/9 | 33.3% | 24 | 57 | 0 |
| T08 | weasyprint | pdfjs | 0/9 | 0.0% | 93 | 0 | 0 |
| T08 | weasyprint | pdfplumber | 0/9 | 0.0% | 93 | 0 | 0 |
| T08 | weasyprint | pypdf | 7/9 | 77.8% | 93 | 0 | 0 |
| T09 | chromium | pdfjs | 0/4 | 0.0% | 9 | 41 | 0 |
| T09 | chromium | pdfplumber | 0/4 | 0.0% | 9 | 41 | 0 |
| T09 | chromium | pypdf | 0/4 | 0.0% | 9 | 41 | 0 |
| T09 | pagedjs | pdfjs | 0/4 | 0.0% | 9 | 41 | 0 |
| T09 | pagedjs | pdfplumber | 0/4 | 0.0% | 9 | 41 | 0 |
| T09 | pagedjs | pypdf | 0/4 | 0.0% | 9 | 41 | 0 |
| T09 | weasyprint | pdfjs | 0/4 | 0.0% | 60 | 0 | 0 |
| T09 | weasyprint | pdfplumber | 0/4 | 0.0% | 60 | 0 | 0 |
| T09 | weasyprint | pypdf | 0/4 | 0.0% | 60 | 0 | 0 |

MF and PF remain separate. A PDF can carry correct forward geometry while exposing strings in visual
bidi order, presentation forms, or extractor-specific order. `/ToUnicode` destination classes and
`/ActualText` counts are observations; they do not alone prove search, clipboard, or AT behavior.
