# Mapping Geometry Calibration

**VERIFIED BY TEST**, with the backward mapper used only as an independent cross-check.

| Document | Pairs | Median edge dev pt | P95 pt | Median IoU | Page agreement |
| --- | ---: | ---: | ---: | ---: | ---: |
| T01 | 5 | 0.148 | 4.072 | 0.7326 | 83.3% |
| T02 | 5 | 0.266 | 4.134 | 0.9354 | 100.0% |
| T03 | 62 | 0.238 | 3.97 | 0.7233 | 68.9% |
| T04 | 3 | 0.255 | 7.919 | 0.7326 | 75.0% |
| T05 | 3 | 0.15 | 7.919 | 0.7436 | 60.0% |
| T06 | 4 | 0.275 | 7.919 | 0.8648 | 80.0% |
| T07 | 6 | 0.195 | 4.121 | 0.8093 | 85.7% |
| T10 | 13 | 0.231 | 97.664 | 0.7326 | 86.7% |
| T11 | 11 | 0.202 | 4.024 | 0.7307 | 91.7% |
| T12 | 9 | 0.235 | 5.553 | 0.7306 | 81.8% |

Per-page transforms use measured PDF media-box dimensions divided by Paged.js sheet dimensions,
not a hard-coded DPI assumption. Differences include box-vs-glyph bounds and extraction uncertainty;
they are not automatically forward-map errors.

Forward-map page assignment validity is **3094/3094
(100.0%)**: every fragment names an
existing page and its clipped quad lies inside that PDF media box. T08/T09 overlay inspection is
**PASS - outlines coincide with Arabic title, paragraph, table text, caption, and note; figure container block coincides with rendered figure**
and **PASS - outlines coincide with Arabic/Latin title, mixed bidi paragraphs, URL, digits, citation, and equation**.
Backward page agreement remains a separate extraction-based cross-check, not the page-assignment score.
