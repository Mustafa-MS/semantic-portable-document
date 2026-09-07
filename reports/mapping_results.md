# Mapping Results

**Evidence:** VERIFIED BY TEST against the generated corpus and PDFs.

| Document | Mapped | Expected | Coverage | Schema/target validation | Errors |
| --- | ---: | ---: | ---: | --- | ---: |
| T01 | 6 | 8 | 75.0% | True | 0 |
| T02 | 3 | 4 | 75.0% | True | 0 |
| T03 | 120 | 150 | 80.0% | True | 0 |
| T04 | 5 | 7 | 71.4% | True | 0 |
| T05 | 3 | 6 | 50.0% | True | 0 |
| T06 | 4 | 6 | 66.7% | True | 0 |
| T07 | 7 | 10 | 70.0% | True | 0 |
| T08 | 1 | 14 | 7.1% | True | 0 |
| T09 | 0 | 5 | 0.0% | True | 0 |
| T10 | 21 | 25 | 84.0% | True | 0 |
| T11 | 14 | 17 | 82.3% | True | 0 |
| T12 | 17 | 19 | 89.5% | True | 0 |

Mean exact-token mapping coverage: **62.6%**.

T02 multi-page node produced **2**
page fragments. The experiment supports block/text/table-cell mapping when PDF text extraction
preserves the source token sequence. It does not prove glyph/cluster geometry. Unmatched Arabic,
MathML, SVG, ancestor, or reordered tokens are retained in each mapping file with a reason.

Negative-case validation rejected wrong revisions, wrong fixed hashes, unknown nodes, duplicate
records, invalid quads, and out-of-range text ranges in automated tests.
