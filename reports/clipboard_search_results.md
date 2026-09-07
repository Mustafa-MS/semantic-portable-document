# Clipboard and search results

## Method

Library extraction is reported separately from real viewer behavior. Actual viewer trials are recorded as `EXACT`, `NORMALIZATION_ONLY`, `ORDER_ERROR`, `CHARACTER_ERROR`, or `UNTESTED`; a visible match must overlap the expected mapped region.

## Initial automated evidence

PDF.js, pypdf, pdfplumber, and MuPDF disagree on `/ActualText` handling. This disagreement is itself an interoperability failure and prevents substituting library output for clipboard evidence. Viewer trials and their exact pasted text are stored in `results_phase1c.json` under `viewerExperiments` when available; absent entries mean `UNTESTED`, not PASS.

Required search probes: `وثيقة عربية تجريبية`, `FROC = 0.906`, `Model-X`, and `Smith 2025`.
