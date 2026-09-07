# Format 0.1 capability declaration profile

The authoritative declaration in the document-state descriptor contains only capability `id` and `version`. Documents MUST NOT set normative or experimental status.

EPUB package metadata uses one `meta property="dcterms:conformsTo"` value per claim for discovery. Its exact claim set MUST equal the authoritative descriptor set; disagreement fails Base.

| Capability | Version | Specification status | Dependencies |
|---|---|---|---|
| Base | 0.1 | normative | none |
| Mapping | 0.1 | normative when claimed | Base + current fixed rendition + mapping artifact |
| Accessible | 0.1 | normative when claimed | Base + EPUB Accessibility 1.1 + WCAG 2.2 AA |
| Fixed-Experimental | 0.1 | experimental | Base |
| Archive-Experimental | 0.1 | experimental | Base + SEALED + current archive-appropriate fixed rendition |

Mapping does not require a `Fixed-Experimental` claim merely because it targets fixed output. Accessibility is independently claimable and is not implied by Archive.

Absence means `NOT_CLAIMED`, not failure. Unknown optional extensions are preserved where safe. An unknown required extension marks each affected capability unsupported and cannot be silently ignored. A processor may still expose safe authoritative Base content.

Provisional capability IRIs under `https://example.invalid/spd/` are Draft identifiers. Stable project-controlled capability, descriptor, schema, and annotation identifiers are a Release Candidate blocker.
