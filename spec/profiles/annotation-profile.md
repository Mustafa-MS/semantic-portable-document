# Format 0.1 annotation profile

W3C Web Annotation is the normative base model. Format 0.1 adds only `StableNodeSelector` for persistent semantic identity. EPUB Annotations 1.0 (2026 Working Draft) is monitored and serialization should remain shape-compatible, but it is not a normative 0.1 dependency until stable.

## StableNodeSelector

```json
{
  "type": "StableNodeSelector",
  "documentId": "urn:uuid:11111111-1111-4111-8111-111111111111",
  "nodeId": "n_paragraph01",
  "scope": "lineage"
}
```

- `documentId` and `nodeId` are always required.
- `scope: lineage` follows the logical node across revisions and MUST omit `revisionId`.
- `scope: revision` anchors historical state and MUST include `revisionId`.
- A text annotation SHOULD refine the stable selector with Web Annotation `TextQuoteSelector` and/or a Format-profiled `TextPositionSelector` using Unicode scalar-value offsets.
- If the stable node resolves but a fallback selector disagrees, processors report target drift and do not silently retarget.
- A page-region selector is fixed-rendition-specific and includes the Fixed Rendition ID/digest; it is not a substitute for semantic targeting.

The JSON structure is constrained by `schemas/annotation-extension.schema.json`. The provisional type name must be replaced by a registered IRI/context before final publication (SPD-ANN-001).

## Packaging and privacy

Annotations may be embedded as non-primary resources or exchanged separately. Annotation bodies do not become authoritative document content by inclusion. Processors should minimize personal data and must not dereference external bodies automatically.

Changing an annotation alone does not create a semantic Revision ID. Every packaged annotation is nevertheless inventoried; changing it invalidates a sealed state that binds that inventory. External annotation collections evolve independently unless explicitly incorporated into a sealed package. Signed annotation layers are deferred.
