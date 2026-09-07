# Format 0.1 RC1 identifier and namespace registry

Status: normative identifier registry for Semantic Portable Document Format 0.1 RC1.

These identifiers are UUID URNs assigned by the SPD project. They are globally unique IRIs, require no DNS authority, make no IANA-registration claim, and are permanent: an identifier in this registry MUST NOT be reassigned to another meaning. The values were generated deterministically with UUIDv5, namespace UUID `6ba7b811-9dad-11d1-80b4-00c04fd430c8` (`uuid.NAMESPACE_URL`), and the case-sensitive name `spd-format-0.1:<registry-key>` shown below.

## Canonical schema identifiers

| Registry key | Artifact | `$id` |
|---|---|---|
| `schema:document-state` | `document-state.schema.json` | `urn:uuid:7a79bc52-a9b9-5953-a2d8-9b0082badbaf` |
| `schema:resource-inventory` | `resource-inventory.schema.json` | `urn:uuid:bbaefa13-a4ff-54bc-9a86-c5c4f586405c` |
| `schema:lifecycle-state` | `state.schema.json` | `urn:uuid:fc155430-2fef-58e3-ba0b-145530cede27` |
| `schema:mapping` | `mapping.schema.json` | `urn:uuid:d08ac0d1-ca22-5518-82d9-a9a2dd6347a0` |
| `schema:annotation-extension` | `annotation-extension.schema.json` | `urn:uuid:74c10ac8-8e41-5db2-ac5f-7fadba53dbc9` |
| `schema:conformance-result` | `conformance-result.schema.json` | `urn:uuid:c4ea11c4-ebca-52e6-9768-17c830f15f42` |

The Validator A report schema is a publication-support artifact, not a canonical document schema. Its stable `$id` is `urn:uuid:40d0f937-3ec9-5b43-9a53-28544b0596ff` (registry key `schema:validator-report`).

## OCF discovery relationship IRIs

| Registry key | Relationship | IRI |
|---|---|---|
| `rel:document-state` | document/revision/capability descriptor | `urn:uuid:0f55d1fb-e1b0-50bb-8a92-53d09c9aa7fc` |
| `rel:resource-inventory` | normative resource inventory | `urn:uuid:08f2982f-d258-5482-abdc-cd6e2b86d990` |
| `rel:lifecycle-state` | lifecycle/integrity state descriptor | `urn:uuid:ec3f5340-bab9-5d57-8c81-77e08906aa4c` |

Each relationship IRI is used as the exact `rel` value of one OCF `container.xml` link. The link media type remains `application/json`.

## Capability IRIs

| Registry key | Short descriptor name | `dcterms:conformsTo` IRI | Status |
|---|---|---|---|
| `capability:Base:0.1` | `Base` | `urn:uuid:bc7ad5f0-9b06-5b01-af4e-7b24ebe724aa` | normative |
| `capability:Mapping:0.1` | `Mapping` | `urn:uuid:7e37d29a-41ac-5151-b843-5bca73555514` | normative when claimed |
| `capability:Accessible:0.1` | `Accessible` | `urn:uuid:ab0f83fe-b584-5726-b289-4892bd823bcb` | normative when claimed |
| `capability:Fixed-Experimental:0.1` | `Fixed-Experimental` | `urn:uuid:92e65973-5fbe-5e41-b604-fcfc88aabcb5` | experimental |
| `capability:Archive-Experimental:0.1` | `Archive-Experimental` | `urn:uuid:f8ff21ff-6200-5cf2-9ca1-3c1935fbf329` | experimental |

The document-state descriptor retains the short name and version `0.1`; EPUB discovery metadata uses the corresponding IRI. This is a serialization mapping, not two capability systems.

## Annotation-extension IRIs

| Registry key | Compact term | IRI |
|---|---|---|
| `vocabulary:StableNodeSelector` | `StableNodeSelector` | `urn:uuid:95d3b3f6-45bb-50fd-9aa5-8bba8186649f` |
| `vocabulary:documentId` | `documentId` | `urn:uuid:1d0a1b23-ca7c-50e8-ada9-febb6ca31d4f` |
| `vocabulary:nodeId` | `nodeId` | `urn:uuid:43ed2328-efe8-54d7-8912-cf6ad018299d` |
| `vocabulary:scope` | `scope` | `urn:uuid:c290e7cc-cdf3-588c-9b07-66accd949405` |
| `vocabulary:revisionId` | `revisionId` | `urn:uuid:eff2bf04-0e80-52a8-8b43-d6c2ec8b16cb` |
| `vocabulary:refinement` | `refinement` | `urn:uuid:bebb56cc-7e6f-5f6d-82bd-02cac1edff94` |

The selector `type` uses its full IRI. Annotation documents map compact extension properties with the inline JSON-LD context in the RC1 annotation profile. Processors MUST NOT fetch a remote project context to interpret these terms.

## Media types and filename extensions

- The OCF container marker remains the registered `application/epub+zip` media type required by EPUB 3.3.
- Descriptor discovery links use `application/json`; Web Annotation resources use an applicable registered type such as `application/ld+json`.
- Format 0.1 RC1 assigns no SPD-specific media type and no mandatory filename extension.
- Values that resemble an unregistered media type, including `application/spd+zip`, `application/vnd.spd+zip`, and equivalents, are not Format 0.1 identifiers.

## Replacement policy

The frozen Draft values under `https://example.invalid/spd/` are historical placeholders and are not accepted as RC1 public identifiers. Future identifiers require an additive registry revision; existing identifiers remain bound to their meanings.
