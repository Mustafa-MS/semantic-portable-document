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

Each capability name maps to the stable project-assigned IRI in the Format 0.1 identifier registry. The authoritative descriptor retains the short name; `dcterms:conformsTo` uses the IRI. These two claim sets MUST agree exactly.


| Capability | Public IRI |
|---|---|
| Base | `urn:uuid:bc7ad5f0-9b06-5b01-af4e-7b24ebe724aa` |
| Mapping | `urn:uuid:7e37d29a-41ac-5151-b843-5bca73555514` |
| Accessible | `urn:uuid:ab0f83fe-b584-5726-b289-4892bd823bcb` |
| Fixed-Experimental | `urn:uuid:92e65973-5fbe-5e41-b604-fcfc88aabcb5` |
| Archive-Experimental | `urn:uuid:f8ff21ff-6200-5cf2-9ca1-3c1935fbf329` |
