# Format 0.1 integrity and state profile

Integrity detects byte changes; it does not authenticate an author, establish trust, or replace a digital signature.

## Inventory and effect classification

Exactly one inventory is authoritative. It lists every ZIP entry, including `mimetype`, `META-INF/container.xml`, control metadata, non-normative caches, annotations, generated fixed renditions, and mappings, except:

1. the inventory itself, to avoid self-reference; and
2. the lifecycle state descriptor, which is self-digested and binds the inventory.

The paths are discovered, not guessed. Literal corpus paths are not normative; OCF container links are.

Each entry has an explicit `affects` array independent of `role`:

- authoritative XHTML and meaningful figure assets: `["semantic","rendering"]`;
- semantic relationship data: `["semantic"]`;
- CSS and fonts: `["rendering"]`;
- document-state control, annotations, cache, mapping, and fixed output: `[]` unless another specification explicitly assigns effects.

Unknown or unlisted entries fail Base even if described as caches.

## Resource digest

For each listed entry, identify the exact normalized NFC package path, decompress the ZIP entry, and compute byte length plus SHA-256 over its exact decompressed bytes. Serialize the digest as lowercase `sha256:` plus 64 hexadecimal digits. No XML/JSON/CSS canonicalization, Unicode normalization, encoding conversion, BOM removal, or newline conversion occurs. ZIP compression, entry order, timestamp, permissions, and comments do not affect resource digests.

## Inventory projections

For a selected entry, serialize exactly:

```text
UTF8(path) 0x00 ASCII(decimal byteLength) 0x00 ASCII(sha256:lowerhex) 0x0A
```

Sort selected entries by unsigned lexicographic comparison of the UTF-8 bytes of their normalized paths. Concatenate records and SHA-256 the result.

- `semanticStateDigest` selects entries whose `affects` contains `semantic`.
- `renditionInputDigest` selects entries whose `affects` contains `semantic` or `rendering`.

Revision ID is opaque. Two commits may have different Revision IDs and the same semanticStateDigest. A CSS/font-only change leaves semanticStateDigest and Revision ID unchanged, changes renditionInputDigest, and stales any fixed rendition bound to the old rendition input.

## Cycle-free binding graph

```text
resource bytes → resource digests → inventory
                                  ├→ semantic projection → semanticStateDigest
                                  └→ render projection   → renditionInputDigest

exact inventory bytes → inventory digest → lifecycle state descriptor

state descriptor with descriptorDigest omitted
  → RFC 8785 JCS UTF-8 bytes
  → SHA-256
  → descriptorDigest
```

JCS applies only to the small state descriptor. It never canonicalizes XHTML, CSS, inventory resource bytes, or other content. The state schema is an I-JSON-compatible closed shape; NaN, Infinity, duplicate names, and lone surrogates are invalid.

## Lifecycle semantics

In `EDITABLE`, fixed status may be `absent`, `current`, or `stale`. `current` is valid only if its Revision ID equals the current revision, its bound renditionInputDigest equals the current value, and its resource digest verifies. Any mismatch is treated as stale regardless of the declared token.

A semantic-only revision MAY be `SEALED`. If a fixed rendition exists in SEALED it MUST be current. A fixed rendition MAY be current without Mapping. If Mapping is claimed, a current fixed rendition and mapping binding are both required.

Every packaged annotation is inventory-bound in a sealed state even though it has `affects: []`; changing it invalidates the seal without creating a semantic revision. External annotations are outside the binding unless incorporated.

Recomputing all hashes after malicious modification can create another internally consistent package, so this remains integrity, not external authenticity. Outer-package signatures are out of scope.
