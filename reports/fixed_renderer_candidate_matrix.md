# Fixed renderer candidate matrix

| Candidate | VF | PF Arabic/bidi | PDF/UA | WTPDF | PDF/A readiness | Complexity | Maintainability |
|---|---|---|---|---|---|---|---|
| A. Raw Paged.js/Chromium | strong visual baseline; complete forward map | mixed RTL extraction broken | Phase 1B failures | Phase 1B failures | low | low renderer integration | good, but semantics insufficient |
| B. Raw WeasyPrint | independent; T09 equation-order visual issue retained | broken on T08/T09 | partial generator tagging | failed representative checks | PDF/A generation exists but did not solve semantics | low | good for comparison, not primary bidi |
| C. Paged.js + compiler | **exact on both rasterizers** | improved in MuPDF but inconsistent across paths | 6/6 automated PASS | see profile matrix | T10 still requires archive transform | medium, renderer-MCID adapter | viable only as restricted experimental profile |
| D. Apache FOP 2.11 | independently reflows; not pixel-equivalent to Paged | logical recovery varies by extractor | 4/4 UA-1 PASS | not a PDF 2.0/WTPDF generator baseline | separate work | medium XHTML→FO projection, information/layout loss | mature Apache 2.0 stack; FO projection is lossy |

Licensing: the experimental compiler uses permissively licensed Python tooling; Apache FOP is Apache License 2.0. No candidate is adopted solely on validator performance.
