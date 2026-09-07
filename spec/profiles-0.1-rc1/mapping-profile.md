# Format 0.1 mapping profile

This profile documents the procedural constraints complementing `schemas/mapping.schema.json`.

## Status registry

| Status | Normative meaning | Geometry |
|---|---|---|
| `MAPPED` | All mappable visible presentation of the node within the claimed scope is represented. | One or more fragments. |
| `PARTIALLY_MAPPED` | Some required visible correspondence is represented but known required visible correspondence remains missing. | One or more fragments and a reason. |
| `NOT_VISIBLE` | The node intentionally has no visible fixed presentation (for example conditional/hidden semantic content). This is not an algorithm failure. | None. |
| `UNMAPPABLE` | The processor supports the feature and attempted mapping, but reliable correspondence cannot be represented for this instance. | None; reason required. |
| `UNSUPPORTED` | The processor does not implement the semantic/layout feature needed to map this node. | None; reason required. |

`NOT_VISIBLE` never means “the mapping algorithm failed.” A processor must not emit invented boxes to turn partial/failure states into `MAPPED`.

## Provenance

- Document level records the generator and dominant method.
- Record level is required and may repeat or override the method: `forward-layout`, `backward-recovery`, `inferred`, or `manual`.
- Fragment-level provenance is omitted in 0.1 to avoid unnecessary complexity. Split records if materially different evidence is needed.
- Mapping claims require `forward-layout` for renderer-produced normative mappings. Other methods are valid for recovery, validation, or explicitly non-normative imported evidence.

## Geometry

- Unit: CSS reference pixel (`1in = 96px`).
- Origin: page top-left; x increases right; y increases down.
- Quad order: top-left, top-right, bottom-right, bottom-left in the fragment's untransformed page space.
- Pages declare positive width/height. Every coordinate is finite and lies within page bounds after clipping.
- Optional six-number affine matrices use `[a,b,c,d,e,f]` with `x' = ax + cy + e`, `y' = bx + dy + f`.
- Geometry numbers are finite JSON numbers. No document-level precision is declared; comparison tolerance is validator/test policy, not validity.

## Logical ranges

Ranges are zero-based, half-open `[start,end)` Unicode scalar-value offsets over the XHTML-profile semantic text value. `0 <= start <= end <= length`. Adjacent page fragments may share a boundary but cannot overlap unless the overlap is explicitly justified as repeated visual presentation. Emoji ZWJ sequences and combining sequences may be split at scalar boundaries syntactically, but renderers SHOULD use grapheme boundaries when a meaningful visual fragment permits it.

## Procedural validation

Schemas validate shape. Procedural checks additionally confirm referenced Node/page IDs, identity bindings and digests, range bounds/order, finite/in-page geometry, status/fragment consistency, and absence of rendering instructions.
