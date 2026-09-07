# Format 0.1 Draft schemas

These Draft 2020-12 schemas use provisional `$id` values under `https://example.invalid/spd/`. Stable project-controlled schema, capability, descriptor-relationship, and annotation identifiers are a mandatory Release Candidate blocker; no production domain is invented in the Draft.

Schemas constrain local structure. Procedural validation remains required for OCF discovery, exact one-rootfile processing, inventory completeness, NFC path normalization, resource hashes, effect projections, RFC 8785 descriptor hashing, cross-descriptor identity/capability agreement, current/stale fixed logic, Mapping dependency closure, Node/range/page references, and geometry bounds.

In particular, `state.schema.json` intentionally permits a current fixed rendition without a mapping. A later validator requires mapping only when the authoritative document-state descriptor claims Mapping.

## Canonical versus historical files

The canonical frozen Draft schema set is exactly:

- `document-state.schema.json`
- `resource-inventory.schema.json`
- `state.schema.json`
- `mapping.schema.json`
- `annotation-extension.schema.json`
- `conformance-result.schema.json` (the normalized corpus expectation shape)

The following are historical Phase 1/1B/1C research artifacts only and MUST NOT
be used for Format 0.1 Draft conformance:

- `mapping-0.1.schema.json`
- `mapping-0.1b.schema.json`
- `state-0.1.schema.json`
- `transaction-0.1.schema.json`
- `failure-record.schema.json`
