# EPUBCheck Results

**VERIFIED BY TEST** with authoritative EPUBCheck 5.3.0 against EPUB 3.3.

The original Phase 1 packages are retained byte-for-byte. Phase 1B copies add only required
`svg`/`mathml` manifest declarations when present, so the initial negative result remains auditable.

| Package | Original | Phase 1B | Added property | Fatal | Errors | Warnings | JSON diagnostic |
| --- | --- | --- | --- | ---: | ---: | ---: | --- |
| T01 | PASS | PASS | none | 0 | 0 | 0 | reports/epubcheck-json/phase1b/T01.json |
| T02 | PASS | PASS | none | 0 | 0 | 0 | reports/epubcheck-json/phase1b/T02.json |
| T03 | PASS | PASS | none | 0 | 0 | 0 | reports/epubcheck-json/phase1b/T03.json |
| T04 | FAIL | PASS | svg | 0 | 0 | 0 | reports/epubcheck-json/phase1b/T04.json |
| T05 | FAIL | PASS | mathml | 0 | 0 | 0 | reports/epubcheck-json/phase1b/T05.json |
| T06 | PASS | PASS | none | 0 | 0 | 0 | reports/epubcheck-json/phase1b/T06.json |
| T07 | PASS | PASS | none | 0 | 0 | 0 | reports/epubcheck-json/phase1b/T07.json |
| T08 | PASS | PASS | none | 0 | 0 | 0 | reports/epubcheck-json/phase1b/T08.json |
| T09 | FAIL | PASS | mathml | 0 | 0 | 0 | reports/epubcheck-json/phase1b/T09.json |
| T10 | PASS | PASS | none | 0 | 0 | 0 | reports/epubcheck-json/phase1b/T10.json |
| T11 | PASS | PASS | none | 0 | 0 | 0 | reports/epubcheck-json/phase1b/T11.json |
| T12 | PASS | PASS | none | 0 | 0 | 0 | reports/epubcheck-json/phase1b/T12.json |
