# Format 0.1 annotation profile

W3C Web Annotation is the normative base model. Format 0.1 adds only `StableNodeSelector` for persistent semantic identity. EPUB Annotations 1.0 (2026 Working Draft) is monitored and serialization should remain shape-compatible, but it is not a normative 0.1 dependency until stable.

## StableNodeSelector

```json
{
  "type": "urn:uuid:95d3b3f6-45bb-50fd-9aa5-8bba8186649f",
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

The JSON structure is constrained by `schemas/rc1/annotation-extension.schema.json`. The selector type and compact extension terms use the permanent IRIs below (SPD-ANN-001). Annotation documents MUST provide these mappings inline so processing requires no network context fetch.

## Packaging and privacy

Annotations may be embedded as non-primary resources or exchanged separately. Annotation bodies do not become authoritative document content by inclusion. Processors should minimize personal data and must not dereference external bodies automatically.

Changing an annotation alone does not create a semantic Revision ID. Every packaged annotation is nevertheless inventoried; changing it invalidates a sealed state that binds that inventory. External annotation collections evolve independently unless explicitly incorporated into a sealed package. Signed annotation layers are deferred.

## Inline extension context

```json
{
  "StableNodeSelector": "urn:uuid:95d3b3f6-45bb-50fd-9aa5-8bba8186649f",
  "documentId": "urn:uuid:1d0a1b23-ca7c-50e8-ada9-febb6ca31d4f",
  "nodeId": "urn:uuid:43ed2328-efe8-54d7-8912-cf6ad018299d",
  "scope": "urn:uuid:c290e7cc-cdf3-588c-9b07-66accd949405",
  "revisionId": "urn:uuid:eff2bf04-0e80-52a8-8b43-d6c2ec8b16cb",
  "refinement": "urn:uuid:bebb56cc-7e6f-5f6d-82bd-02cac1edff94"
}
```
