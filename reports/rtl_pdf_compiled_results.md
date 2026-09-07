# Arabic and bidi compiled-PDF results

Raw and NFC/NFKC outputs are stored separately in `corpus/generated/phase1c/text/`; normalization is not used to conceal order failures.

| Fixture | PDF.js | pypdf | pdfplumber | MuPDF |
|---|---:|---:|---:|---:|
| T08 compiled | 11.1% | 0.0% | 0.0% | 0.0% |
| T09 compiled | 0.0% | 0.0% | 0.0% | 50.0% |
| T08 FOP | 0.0% | 0.0% | 0.0% | 0.0% |
| T09 FOP | 0.0% | 0.0% | 0.0% | 0.0% |

## T08 gate

The target is at least 95% exact logical phrase recovery on two independent paths. The measured paths above determine whether that gate passed; library disagreement remains explicit.

## T09 gate

The required probes are `FROC = 0.906`, `Model-X`, the URL, Western and Arabic-Indic digits, `x = 0.906`, and `[Smith 2025]`. Probe booleans are retained in `results_phase1c.json`. The compiled candidate reaches formal UA-2 validity but does not make all logical forms reliable across ordinary extractors; especially, the first mixed Arabic/LTR sentence remains reordered in MuPDF and unchanged in PDF.js/pypdf/pdfplumber.
