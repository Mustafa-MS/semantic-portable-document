# PDF Conformance Observations

**Evidence:** OBSERVED IN ONE IMPLEMENTATION in Chromium PDFs. These object-level observations do not prove
WTPDF, PDF/UA-2, or PDF/A-4 conformance.

| Document | ToUnicode fonts | Embedded fonts | Table | TR | TH | TD | Figure | Alt | ActualText |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| T01 | 4/4 | 4/4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| T02 | 4/4 | 4/4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| T03 | 7/7 | 7/7 | 1 | 30 | 32 | 56 | 0 | 0 | 0 |
| T04 | 3/3 | 3/3 | 0 | 0 | 0 | 0 | 4 | 2 | 0 |
| T05 | 3/3 | 3/3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| T06 | 3/3 | 3/3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| T07 | 4/4 | 4/4 | 0 | 0 | 0 | 0 | 2 | 1 | 0 |
| T08 | 3/3 | 3/3 | 1 | 2 | 2 | 2 | 2 | 1 | 0 |
| T09 | 3/3 | 3/3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| T10 | 3/3 | 3/3 | 1 | 2 | 2 | 2 | 2 | 1 | 0 |
| T11 | 3/3 | 3/3 | 1 | 2 | 2 | 2 | 0 | 0 | 0 |
| T12 | 3/3 | 3/3 | 1 | 2 | 3 | 1 | 2 | 1 | 0 |

The harness inspects `/StructTreeRoot`, `/MarkInfo`, `/Lang`, structure roles, `/Alt`, `/ActualText`,
font descriptors, `/ToUnicode`, links, images, and extractable text. It does not validate role-map
semantics, MCID association correctness, reading order, Unicode CMap correctness, table header
relationships, archival restrictions, or accessibility conformance. Those require specialist tools
and manual assistive-technology inspection.
