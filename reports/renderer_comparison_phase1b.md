# Renderer Comparison - Phase 1B

**OBSERVED IN IMPLEMENTATIONS.** Paged.js uses Chromium layout with explicit paginated-DOM access;
WeasyPrint 69.0 is a substantially independent Python/Pango/CSS renderer and generated PDF/UA-2 candidates.

| Document | Path | Pages | Render/paginate ms | Structure tree | Lang | Mapping feasibility |
| --- | --- | ---: | ---: | --- | --- | --- |
| T01 | Chromium baseline | 2 | 2280.64 | True | en | backward PDF tokens |
| T01 | Paged.js | 2 | 221 | True | en | forward DOM |
| T01 | WeasyPrint 69 | 2 | 10611.5 | True | en | layout API not exposed by portable build |
| T02 | Chromium baseline | 3 | 2330.46 | True | en | backward PDF tokens |
| T02 | Paged.js | 3 | 5126 | True | en | forward DOM |
| T02 | WeasyPrint 69 | 3 | 8735.46 | True | en | layout API not exposed by portable build |
| T03 | Chromium baseline | 3 | 2485.42 | True | en | backward PDF tokens |
| T03 | Paged.js | 3 | 186 | True | en | forward DOM |
| T03 | WeasyPrint 69 | 3 | 11732.99 | True | en | layout API not exposed by portable build |
| T04 | Chromium baseline | 1 | 2919.18 | True | en | backward PDF tokens |
| T04 | Paged.js | 1 | 213 | True | en | forward DOM |
| T04 | WeasyPrint 69 | 1 | 8413.92 | True | en | layout API not exposed by portable build |
| T05 | Chromium baseline | 1 | 2614.73 | True | en | backward PDF tokens |
| T05 | Paged.js | 1 | 99 | True | en | forward DOM |
| T05 | WeasyPrint 69 | 1 | 8532.88 | True | en | layout API not exposed by portable build |
| T06 | Chromium baseline | 2 | 3051.89 | True | en | backward PDF tokens |
| T06 | Paged.js | 2 | 3500 | True | en | forward DOM |
| T06 | WeasyPrint 69 | 2 | 9334.11 | True | en | layout API not exposed by portable build |
| T07 | Chromium baseline | 2 | 3236.32 | True | en | backward PDF tokens |
| T07 | Paged.js | 2 | 4566 | True | en | forward DOM |
| T07 | WeasyPrint 69 | 2 | 9239.95 | True | en | layout API not exposed by portable build |
| T08 | Chromium baseline | 1 | 2375.47 | True | ar | backward PDF tokens |
| T08 | Paged.js | 1 | 215 | True | ar | forward DOM |
| T08 | WeasyPrint 69 | 1 | 8019.81 | True | ar | layout API not exposed by portable build |
| T09 | Chromium baseline | 1 | 2978.26 | True | ar | backward PDF tokens |
| T09 | Paged.js | 1 | 247 | True | ar | forward DOM |
| T09 | WeasyPrint 69 | 1 | 10055.12 | True | ar | layout API not exposed by portable build |
| T10 | Chromium baseline | 1 | 2343.12 | True | en | backward PDF tokens |
| T10 | Paged.js | 1 | 98 | True | en | forward DOM |
| T10 | WeasyPrint 69 | 1 | 10073.61 | True | en | layout API not exposed by portable build |
| T11 | Chromium baseline | 2 | 2130.07 | True | en | backward PDF tokens |
| T11 | Paged.js | 2 | 114 | True | en | forward DOM |
| T11 | WeasyPrint 69 | 2 | 9880.53 | True | en | layout API not exposed by portable build |
| T12 | Chromium baseline | 1 | 2056.03 | True | en | backward PDF tokens |
| T12 | Paged.js | 1 | 137 | True | en | forward DOM |
| T12 | WeasyPrint 69 | 1 | 9039.93 | True | en | layout API not exposed by portable build |

The corpus comparison includes pagination, tables, columns, MathML, SVG/raster figures, notes,
Arabic shaping, bidi, links, fonts, tagging, extraction, and mapping feasibility. Detailed object and
text results remain in `results_phase1b.json`; appearance was checked from rendered PNGs.

| Capability | Chromium baseline | Paged.js | WeasyPrint 69 |
| --- | --- | --- | --- |
| Pagination / page CSS | successful baseline | successful; paginated DOM observable | successful; independent CSS engine |
| Tables / split content | rendered | T03 three pages; forward cells mapped | T03 three pages |
| Multi-column | rendered | T07 two columns plus continuation | T07 two columns plus continuation |
| Foot/endnotes | rendered as authored | rendered as authored | rendered as authored |
| SVG / raster | rendered | T04 both figures | T04 both figures |
| MathML | browser MathML | structured fraction/superscript | **limitation:** flattened T05 fraction/superscript |
| Arabic shaping / bidi | visually reasonable; PF failed | visually legible; MF passed, PF failed | visually legible; MF unavailable, PF below gate |
| Fonts / links | embedded / annotations observed | embedded / annotations observed | embedded / annotations observed |
| Tagging / metadata | structure present, formal profiles fail | structure present, formal profiles fail | UA-2 candidate structure present, formal profiles fail |
| Mapping feasibility | backward baseline only | exact identity/range geometry exposed | portable CLI exposes no layout geometry adapter |

Visual-QA classifications: Paged.js **PASS**;
WeasyPrint **PASS_WITH_LIMITATION**.
