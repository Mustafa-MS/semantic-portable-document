# Forward Mapping Results

**VERIFIED BY TEST** with Paged.js 0.4.3 and system Chromium. Mapping was emitted from propagated
`data-node-id` values and instrumented logical source ranges before PDF generation; it did not use
PDF text extraction.

| Document | Visible mapped | Node coverage | Range characters | Range coverage | Partial | Unmappable |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| T01 | 8/8 | 100.0% | 243/243 | 100.0% | 0 | 0 |
| T02 | 4/4 | 100.0% | 7097/7097 | 100.0% | 0 | 0 |
| T03 | 150/150 | 100.0% | 722/722 | 100.0% | 0 | 0 |
| T04 | 7/7 | 100.0% | 122/122 | 100.0% | 0 | 0 |
| T05 | 6/6 | 100.0% | 95/95 | 100.0% | 0 | 0 |
| T06 | 6/6 | 100.0% | 4642/4642 | 100.0% | 0 | 0 |
| T07 | 10/10 | 100.0% | 3069/3069 | 100.0% | 0 | 0 |
| T08 | 14/14 | 100.0% | 178/178 | 100.0% | 0 | 0 |
| T09 | 5/5 | 100.0% | 181/181 | 100.0% | 0 | 0 |
| T10 | 25/25 | 100.0% | 396/396 | 100.0% | 0 | 0 |
| T11 | 17/17 | 100.0% | 337/337 | 100.0% | 0 | 0 |
| T12 | 19/19 | 100.0% | 177/177 | 100.0% | 0 | 0 |

Macro-average visible-node mapping: **100.0%**. Macro-average logical-range mapping:
**100.0%**. T08/T09 minimums were **100.0%** nodes and **100.0%**
ranges. Ancestors without a stable paginated clone are represented by the union of identified child
fragments with explicit `forward:pagedjs-descendant-union` provenance.

The common 0.1B model records `MAPPED`, `PARTIALLY_MAPPED`, `NOT_VISIBLE`, `UNMAPPABLE`, or
`UNSUPPORTED`, method, deterministic confidence category, logical ranges, page-local quads, and the
CSS-pixel-to-PDF-point transform. Adapters remain non-normative.
