# Renderer Comparison

**Evidence scope:** OBSERVED IN ONE IMPLEMENTATION for Chromium; NOT VERIFIED for unavailable adapters.

| Document | Chromium | Pages | Time ms | PDF bytes | Structure tree | Extracted chars |
| --- | --- | ---: | ---: | ---: | --- | ---: |
| T01 | PASS | 2 | 2280.64 | 34911 | True | 282 |
| T02 | PASS | 3 | 2330.46 | 27591 | True | 8209 |
| T03 | PASS | 3 | 2485.42 | 73190 | True | 939 |
| T04 | PASS | 1 | 2919.18 | 39991 | True | 147 |
| T05 | PASS | 1 | 2614.73 | 35944 | True | 117 |
| T06 | PASS | 2 | 3051.89 | 29595 | True | 5386 |
| T07 | PASS | 2 | 3236.32 | 41899 | True | 3573 |
| T08 | PASS | 1 | 2375.47 | 49588 | True | 211 |
| T09 | PASS | 1 | 2978.26 | 47647 | True | 216 |
| T10 | PASS | 1 | 2343.12 | 46932 | True | 462 |
| T11 | PASS | 2 | 2130.07 | 32178 | True | 405 |
| T12 | PASS | 1 | 2056.03 | 45432 | True | 205 |

Chromium completed 12/12 corpus renders. Its observed output is one
implementation result, not a format-level conclusion or a PDF/UA/WTPDF conformance claim.

Unavailable renderer observations:
- **weasyprint:** NOT RUN - executable was not installed.
- **vivliostyle_or_pagedjs:** NOT RUN - executable was not installed.

Measurements cover page count, time, size, font resources, extraction, links, images, the PDF
structure-tree flag, marked-content flag, and language metadata. ActualText, ToUnicode quality,
table/figure tags, alt text propagation, and formal conformance remain unproven by this harness.
