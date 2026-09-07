# PDF/A-4 results — Phase 1C

PDF/A debugging was isolated until after the semantic and bidi experiments. T10 compiled PDF was checked with veraPDF profile `4`.

| Fixture | Candidate | Profile | Result | Failed rules | Failed checks |
|---|---|---:|---:|---:|---:|
| T03 | compiled | ua2 | PASS | 0 | 0 |
| T04 | compiled | ua2 | PASS | 0 | 0 |
| T08 | compiled | ua2 | PASS | 0 | 0 |
| T08 | compiled | wt1a | PASS | 0 | 0 |
| T08 | compiled | wt1r | PASS | 0 | 0 |
| T09 | compiled | ua2 | PASS | 0 | 0 |
| T09 | compiled | wt1a | PASS | 0 | 0 |
| T09 | compiled | wt1r | PASS | 0 | 0 |
| T10 | compiled | 4 | FAIL | 4 | 50 |
| T10 | compiled | ua2 | PASS | 0 | 0 |
| T10 | compiled | wt1a | PASS | 0 | 0 |
| T10 | compiled | wt1r | PASS | 0 | 0 |
| T12 | compiled | ua2 | PASS | 0 | 0 |
| T12 | compiled | wt1a | PASS | 0 | 0 |
| T12 | compiled | wt1r | PASS | 0 | 0 |

## Exact residual diagnostics

### compiled T10 — 4

- `ISO 19005-4:2020` 6.1.3/1: 1 failed checks — File identifiers shall be defined by the ID entry in a PDF file’s trailer dictionary

- `ISO 19005-4:2020` 6.2.4.3/2: 47 failed checks — DeviceRGB shall only be used if a device independent DefaultRGB colour space has been set when the DeviceRGB colour space is used or if the current transparency blending space, when the DeviceRGB colour space is used, is a device independent RGB-based colour space or the current PDF/A OutputIntent, when the DeviceRGB colour space is used, contains an 'RGB ' destination profile

- `ISO 19005-4:2020` 6.1.3/4: 1 failed checks — The Info key shall not be present in the trailer dictionary of PDF/A-4 conforming files unless there exists a PieceInfo entry in the document catalog dictionary

- `ISO 19005-4:2020` 6.1.3/5: 1 failed checks — If a document information dictionary is present, it shall only contain a ModDate entry

## Decision

PDF/A-4 belongs to an **Archive capability**, not every ordinary Fixed rendition. Mandatory PDF/A would import output-intent, color-management, metadata, and archival-policy constraints into documents whose immediate requirement is a stable visual snapshot. Archive can require the additional transform and validation without weakening the Base/Fixed model.
