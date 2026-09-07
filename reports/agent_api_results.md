# Minimal Agent API Results

**Evidence:** VERIFIED BY TEST using deterministic transaction fixtures; external AI execution
is NOT VERIFIED.

- Atomic Table 4 + discussion update committed: **True**
- Cell Node ID preserved: **True**
- Revision ID changed: **True**
- Cell content hash changed: **True**
- Unrelated semantic nodes changed: **0**
- Old mapping rejected against R2: **True**
- New fixed rendition and R2 mapping generated: **True**
- Stale-revision write rejected without mutation: **True**
- Node-hash conflict rejected without mutation: **True**

The harness implements only `replaceText`, `updateTableCell`, `replaceFigure`, `moveSection`, and
`insertCitation`. This is enough to test atomicity and optimistic concurrency, not to define a full SDK.
