# Findings

This file summarizes the machine-readable evidence in `reports/results.json`.

- VERIFIED BY TEST: 12 Chromium PDFs, mappings, packages, integrity descriptors,
  and equivalence records were produced and checked.
- VERIFIED BY TEST: stale revision and node-hash conflicts were rejected atomically.
- OBSERVED IN ONE IMPLEMENTATION: Chromium-specific pagination, extraction, links, images, and tagging flags.
- NOT VERIFIED: WeasyPrint, Vivliostyle/Paged.js, EPUBCheck, reader interoperability,
  clipboard behavior, and formal PDF conformance.
- Logged failures/unsupported observations: **17**.

Negative results are preserved in `reports/results.json` and the focused reports; they are not
converted into architecture-level claims.
