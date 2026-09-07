# RTL Mapping Fidelity

**VERIFIED BY TEST.** MF is reported independently from PDF text fidelity.

| Document | Visible node MF | Logical-range MF | Evidence | PDF extraction dependency |
| --- | ---: | ---: | --- | --- |
| T08 | 100.0% | 100.0% | EXACT_TEXT_RANGE_LAYOUT | independent of PDF extraction |
| T09 | 100.0% | 100.0% | EXACT_TEXT_RANGE_LAYOUT | independent of PDF extraction |

Arabic, Latin names, URLs, `FROC = 0.906`, Arabic-Indic and European digits, parentheses, citations,
and adjacent MathML are mapped from logical source spans to visual rectangles. Visual x-order is
never used to rewrite or infer logical order. Page geometry was visually inspected separately.
