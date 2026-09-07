# Format 0.1 terminology registry

This registry supplies precise terms for the Draft. Decisions A-001 through A-023 are incorporated. Entries marked **RC blocker** require stable public identifiers before Release Candidate but do not make Draft processing ambiguous.

| Term | Normative meaning | Approval |
|---|---|---|
| Document | One OCF package claiming Format 0.1 conformance, including its authoritative rendition and conformance metadata. | Candidate-supported |
| Document ID | A globally unique, persistent identifier for one document lineage, serialized as a canonical lowercase RFC 9562 UUID URN. It does not identify a particular state. | Approved |
| Document lineage | The sequence/graph of revisions descended from the same Document ID, including persistent Node identities. | **Required** |
| Revision | One committed, immutable semantic state of a document lineage. | Candidate-supported |
| Revision ID | An opaque canonical lowercase RFC 9562 UUID URN identifying one revision. It MUST NOT encode semantic-state identity. | Approved |
| Node | An independently addressable semantic object in authoritative XHTML. | Candidate-supported |
| Node ID | An XML-ID-compatible persistent identifier `n_<token>`, where the token has 1–128 lowercase ASCII characters from `[a-z0-9._-]`; unique in the current revision and governed by separate lineage rules. | Approved |
| Authoritative semantic rendition | The one ordered XHTML spine declared as the source of primary meaning, reading order, accessibility, and edits. | Candidate-supported |
| Normative resource | A package resource whose bytes affect semantic state, rendering input, conformance, a claimed capability, or a sealed binding. Inventory inclusion is independent of normative role. | Approved |
| Non-normative resource | A listed package resource with role `non-normative` and `affects: []`, such as a cache. It remains inventoried and sealed-state-bound when packaged. | Approved |
| Generated resource | A resource derived from a revision, such as a fixed rendition or mapping. Generated does not mean non-normative. | Candidate-supported |
| Inferred resource | A resource produced by heuristic/import inference rather than asserted source semantics. Its provenance remains explicit. | Candidate-supported |
| Fixed rendition | An immutable generated page appearance bound to a particular Revision ID. No permanent fixed media type is normative in 0.1. | Candidate-supported |
| Fixed Rendition ID | An opaque `f_<token>` identifier using the Node-token grammar; regeneration creates a new ID. | Approved |
| Page ID | An opaque `p_<token>` identifier using the Node-token grammar, unique only within one fixed rendition. | Approved |
| Mapping | A revision- and fixed-rendition-bound correspondence artifact between semantic Node IDs/logical ranges and page geometry. It is not a page-description language. | Candidate-supported |
| Mapping fragment | One page-local geometric occurrence of all or part of a semantic node, optionally paired with a half-open logical range. | **Required** |
| Mapping status | One of `MAPPED`, `PARTIALLY_MAPPED`, `NOT_VISIBLE`, `UNMAPPABLE`, or `UNSUPPORTED`, with meanings fixed by the mapping profile. | Candidate-supported |
| Sealed state | A finalized revision descriptor whose inventory and digests bind the semantic revision and any claimed fixed/mapping artifacts. | Candidate-supported |
| Editable state | A mutable lifecycle state in which semantic XHTML remains authoritative and a fixed rendition may be current, stale, or absent. | Candidate-supported |
| Capability | A document-declared ID/version pair whose normative/experimental status and dependencies are fixed by this specification, never by the document. | Approved |
| Processor | Any implementation that reads, writes, validates, imports, renders, or edits a Format 0.1 document. | **Required** |
| Reader | A processor that exposes authoritative content and supported capabilities without modifying the package. | **Required** |
| Editor | A processor that creates revisions while preserving identity and transaction/lifecycle invariants. | **Required** |
| Renderer | A processor that derives responsive presentation or a fixed rendition; a Mapping-capable renderer emits forward mapping. | **Required** |
| Validator | A processor that evaluates requirements and emits a conformance result without repairing the input. | **Required** |
| Importer | A processor that creates authoritative or inferred semantic resources from another representation while retaining provenance. | **Required** |
| Agent processor | A processor exposing stable semantic structures to automated agents, normally through a transactional companion API. | **Required** |
| Semantic text value | Concatenation of descendant Unicode text nodes in DOM logical order, excluding CSS generated content and text in non-rendered metadata containers. Whitespace is not collapsed for mapping offsets. | **Required** |
| Unicode scalar-value offset | A zero-based count of Unicode scalar values in a semantic text value. Ranges are half-open `[start,end)`. Surrogate code units and grapheme clusters are not offset units. | **Required** |
| Resource effect | An explicit inventory `affects` value identifying semantic impact, rendering impact, both, or neither, independently of provenance role. | Approved |
| Semantic-state digest | SHA-256 over the deterministic inventory projection of resources whose `affects` contains `semantic`; separate from Revision ID. | Approved |
| Rendition-input digest | SHA-256 over the deterministic inventory projection of resources whose `affects` contains `semantic` or `rendering`; bound by a current fixed rendition. | Approved |
| Descriptor digest | SHA-256 over RFC 8785 JCS bytes of the lifecycle state descriptor with `descriptorDigest` omitted. | Approved |
| Descriptor discovery | Exact OCF `container.xml` links that identify document-state, inventory, and lifecycle-state resources without filename guessing. | Approved; provisional relationship IRIs are an **RC blocker** |
