# Arabic and RTL Results

**Evidence:** source metadata checks are VERIFIED BY TEST; Chromium rendering/extraction is
OBSERVED IN ONE IMPLEMENTATION; copy/paste and accessibility conformance are NOT VERIFIED.

| Document | lang | dir | Exact Arabic extraction | Mapping coverage | PDF /Lang |
| --- | --- | --- | ---: | ---: | --- |
| T08 | ar | rtl | 0/14 | 7.1% | ar |
| T09 | ar | rtl | 0/5 | 0.0% | ar |

The source stores Arabic in logical Unicode order with `lang="ar"` and `dir="rtl"`. Exact phrase
matching measures extraction order without pretending that a visual inspection proves logical
text order. Automated clipboard behavior was not available. Page render PNGs are generated for
human shaping, joining, punctuation, and bidi inspection.
