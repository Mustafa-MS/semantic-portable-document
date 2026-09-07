# Format 0.1 Draft conformance matrix

118 requirements: 11 existing meanings clarified/strengthened, 5 new groups, 102 existing rows unchanged. Canonical schemas and semantic algorithms unchanged.

| Requirement | Capability | Automation | Subject | Normative requirement |
|---|---|---|---|---|
| SPD-ARCH-001 | Base | AUTOMATED | document | A conforming document has exactly one authoritative semantic representation. |
| SPD-ARCH-002 | Fixed-Experimental | PARTIALLY_AUTOMATED | fixed-rendition | A fixed rendition is not an independently editable source of truth. |
| SPD-ARCH-003 | Base | INFORMATIVE_ONLY | format | Stable existing standards are reused where practical. |
| SPD-BASE-001 | Base | AUTOMATED | package | A Format 0.1 Base document uses the EPUB-Compatible Packaging Profile 0.1 and SHALL satisfy applicable container/publication requirements of EPUB 3.3 Recommendation 13 January 2026 except where SPD explicitly imposes a stricter rule. |
| SPD-BASE-002 | Base | AUTOMATED | package | Whole-publication EPUB conformance is required under the pinned baseline. Every completed EPUBCheck 5.3.0 conformance error or fatal error fails this requirement; specific diagnostic attribution is additive. Warnings alone do not fail it, and tool failure is NOT_TESTED rather than document failure. |
| SPD-BASE-003 | Base | INFORMATIVE_ONLY | package | The format does not define a new ZIP dialect. |
| SPD-BASE-004 | Base | MANUAL | processor | A processor MUST distinguish generic semantic compatibility/readability from SPD lifecycle, currentness, integrity, fixed-rendition, Mapping, authentication and transaction verification. Semantic XHTML remains authoritative even in SEALED documents; ordinary EPUB readers are not SPD processors. |
| SPD-BASE-005 | Base | AUTOMATED | package | A Base package includes navigation, an authoritative XHTML spine, identity metadata, inventory, offline required resources, semantic structure, logical text, and integrity digests. |
| SPD-BASE-006 | Base | AUTOMATED | package | The OCF container contains exactly one rootfile package document, whose spine defines the authoritative semantic reading order. |
| SPD-SEC-001 | Base | AUTOMATED | content | Base MUST NOT contain or depend on executable document code, executable macros, script elements (including inert data blocks), event-handler attributes, executable URLs or document-supplied code paths. |
| SPD-SEC-002 | Base | AUTOMATED | content | Base MUST NOT contain active embedded/application contexts: iframe including srcdoc, object, embed, plugin execution, service-worker dependencies or document-created executable browsing contexts. Host-owned rendering frames are outside document content. |
| SPD-SEC-003 | Base | AUTOMATED | content | Base MUST NOT initiate automatic publication-originated network access or navigation, including fetching, speculative loading, remote preload, prefetch, DNS preconnect, ping and automatic link checking. Explicit host-mediated user hyperlinks are separate. |
| SPD-SEC-004 | Base | AUTOMATED | font | Every automatically loaded font MUST be inventoried and package-local, including optional fonts. Remote font fetching is prohibited; authoritative fonts MUST NOT depend on uncontrolled local() substitution. |
| SPD-SEC-005 | Base | AUTOMATED | stylesheet | Every automatically loaded stylesheet or import MUST be inventoried and package-local, including optional and fallback styling. Remote stylesheet loading is prohibited. |
| SPD-SEC-006 | Base | AUTOMATED | image | Every automatically loaded image or other visual/media resource MUST be inventoried and package-local, including decorative, optional, cursor, mask, filter, tracking and non-authoritative resources. |
| SPD-SEC-007 | Base | AUTOMATED | svg | All SVG contexts, including inline, standalone, image and nested resources, MUST exclude script, events, foreignObject, executable URLs, automatic remote dependencies and active behavior; ordinary static graphics and safe terminating local references remain allowed. |
| SPD-SEC-008 | Base | AUTOMATED | resource | Every automatically resolved rendered dependency MUST transitively terminate in verified inventoried package-local resources or valid local fragments. XHTML, CSS, SVG, MathML and nested embedding modes use the same containment policy; import and resource-expansion cycles are prohibited. |
| SPD-SEM-001 | Base | AUTOMATED | rendition | Exactly one authoritative semantic rendition is identified. |
| SPD-SEM-002 | Base | AUTOMATED | rendition | The authoritative rendition consists of one or more ordered XHTML content documents. |
| SPD-SEM-003 | Base | AUTOMATED | spine | The package spine defines primary reading order. |
| SPD-SEM-004 | Base, Accessible | PARTIALLY_AUTOMATED | xhtml | Native HTML semantics are used where they exist. |
| SPD-SEM-005 | Base, Accessible | PARTIALLY_AUTOMATED | xhtml | Semantic XHTML is preferred to accessibility or custom metadata mechanisms. |
| SPD-SEM-006 | Base, Accessible | PARTIALLY_AUTOMATED | aria | ARIA does not replace correct native semantics. |
| SPD-SEM-007 | Base | PARTIALLY_AUTOMATED | content | Primary textual or structural content is not independently duplicated in another normative resource. |
| SPD-SEM-008 | Base | PARTIALLY_AUTOMATED | supplemental-data | Supplemental structured data does not redefine authoritative textual content. |
| SPD-SEM-009 | Base, Accessible | MANUAL | math | When semantic MathML exists, mathematical meaning is not required to be reconstructed from visual glyph positions. |
| SPD-SEM-010 | Base, Accessible | PARTIALLY_AUTOMATED | figure | Figure, caption, and reference relationships remain semantic. |
| SPD-SEM-011 | Base | AUTOMATED | figure | Fixed coordinates do not define figure-caption-reference relationships. |
| SPD-SEM-012 | Base, Accessible | PARTIALLY_AUTOMATED | table | Tables use semantic table structures. |
| SPD-SEM-013 | Base, Accessible | PARTIALLY_AUTOMATED | table | Table header relationships are represented semantically rather than inferred only from visual position. |
| SPD-SEM-014 | Base | PARTIALLY_AUTOMATED | relationship-graph | A supplemental relationship graph does not unnecessarily duplicate authoritative content. |
| SPD-ID-001 | Base | AUTOMATED | document | Every document has a persistent canonical lowercase RFC 9562 UUID URN Document ID. |
| SPD-ID-002 | Base | AUTOMATED | revision | Every committed semantic state has an opaque canonical lowercase RFC 9562 UUID URN Revision ID. |
| SPD-ID-003 | Base | AUTOMATED | revision | A change to normative semantic content creates a new Revision ID. |
| SPD-ID-004 | Base | AUTOMATED | revision | A change only to non-normative cache data does not create a new semantic Revision ID. |
| SPD-ID-005 | Base | AUTOMATED | node | Every independently addressable semantic object carries a persistent Node ID. |
| SPD-ID-006 | Base | AUTOMATED | node | Node IDs are unique in the current authoritative semantic revision. |
| SPD-ID-007 | Base | PARTIALLY_AUTOMATED | node | Node IDs do not depend on page position, DOM path, visible numbering, or text content. |
| SPD-ID-008 | Base | AUTOMATED | node | A content hash is not used as Node identity. |
| SPD-ID-009 | Base | MANUAL | node | A copied node normally receives a new Node ID. |
| SPD-ID-010 | Base | AUTOMATED | table-cell | Addressable table cells have persistent Node IDs. |
| SPD-ID-011 | Base | PARTIALLY_AUTOMATED | editor | A conforming editor preserves Node identity according to lineage rules when supplied lineage history is available. |
| SPD-ID-012 | Base | PARTIALLY_AUTOMATED | editor | A conforming editor does not knowingly reuse a retired Node ID within supplied lineage history. |
| SPD-ID-013 | Base | AUTOMATED | validator | A standalone validator reports history-dependent persistence and non-reuse checks as NOT_TESTED when lineage history is unavailable; absence of history does not fail Base. |
| SPD-I18N-001 | Base | PARTIALLY_AUTOMATED | text | Semantic text is represented in logical Unicode order. |
| SPD-I18N-002 | Base | PARTIALLY_AUTOMATED | text | Visual placement does not determine semantic ordering. |
| SPD-I18N-003 | Base, Accessible | AUTOMATED | language | The root authoritative XHTML html element has equivalent valid lang and xml:lang values. |
| SPD-I18N-004 | Base, Accessible | PARTIALLY_AUTOMATED | direction | The root authoritative XHTML html element explicitly declares dir ltr or rtl, and nested semantic elements declare direction when it differs from inherited direction. |
| SPD-I18N-005 | Base | AUTOMATED | processor | A processor does not equate visual left-to-right position with logical reading order. |
| SPD-I18N-006 | Mapping | AUTOMATED | api | Mapping and editing APIs operate on logical text ranges. |
| SPD-ANN-001 | Base | INFORMATIVE_ONLY | vocabulary | The StableNodeSelector vocabulary and namespace are registered before final 0.1 publication. |
| SPD-ANN-002 | Base | AUTOMATED | selector | A lineage-scoped StableNodeSelector contains Document ID and Node ID and omits Revision ID. |
| SPD-ANN-003 | Base | AUTOMATED | selector | A revision-scoped StableNodeSelector contains Document ID, Revision ID, and Node ID. |
| SPD-ANN-004 | Base | AUTOMATED | annotation | Changing an in-package annotation does not create a semantic Revision ID but invalidates a sealed state whose inventory binds that annotation; external annotations evolve independently unless incorporated. |
| SPD-STATE-001 | Fixed-Experimental | AUTOMATED | processor | A stale fixed rendition is not presented as the current authoritative fixed representation. |
| SPD-STATE-002 | Base | AUTOMATED | sealed-state | A sealed state binds the semantic Revision ID, normative inventory, any claimed fixed rendition, and any applicable mapping artifact. |
| SPD-STATE-003 | Base | AUTOMATED | sealed-state | Changing normative semantic content invalidates the sealed state. |
| SPD-STATE-004 | Fixed-Experimental | AUTOMATED | fixed-rendition | A fixed rendition bound to a sealed revision is immutable for that revision. |
| SPD-STATE-005 | Fixed-Experimental | AUTOMATED | fixed-rendition | A fixed rendition is current only when revision ID, renditionInputDigest, and resource digest match current verified state; otherwise it is stale. |
| SPD-STATE-006 | Base | AUTOMATED | sealed-state | A semantic-only revision may be SEALED; if fixed is present in SEALED it is current. |
| SPD-STATE-007 | Mapping | AUTOMATED | capability | A Mapping claim requires a current fixed rendition and a bound mapping artifact; current fixed without Mapping is permitted. |
| SPD-RES-001 | Base | AUTOMATED | inventory | A document maintains exactly one normative resource inventory. |
| SPD-RES-002 | Base | AUTOMATED | resource | Each inventory entry has a normalized NFC path, media type, byte length, SHA-256 digest, role, and explicit affects array. |
| SPD-RES-003 | Base | AUTOMATED | inventory | The inventory lists every ZIP entry including non-normative caches except the inventory itself and lifecycle state descriptor. |
| SPD-RES-004 | Base | AUTOMATED | resource | Inventory digests cover the exact decompressed bytes returned for the named ZIP entry. |
| SPD-RES-005 | Base | AUTOMATED | resource | Each resource explicitly declares whether it affects semantic state, rendering input, both, or neither; role alone is not effect classification. |
| SPD-RES-006 | Base | AUTOMATED | package | Any unlisted ZIP entry other than the two self-referential exceptions fails conformance. |
| SPD-INT-001 | Base | AUTOMATED | integrity | The document provides digest-based integrity verification. |
| SPD-INT-002 | Base | AUTOMATED | integrity | SHA-256 is supported. |
| SPD-INT-003 | Base | AUTOMATED | integrity | Integrity detects modification of semantic content, normative styles/assets, mapping, fixed rendition, and state metadata when applicable. |
| SPD-INT-004 | Base | AUTOMATED | digest | semanticStateDigest is computed by the normative UTF-8 inventory projection over resources whose affects contains semantic. |
| SPD-INT-005 | Base | AUTOMATED | digest | renditionInputDigest is computed by the normative projection over resources affecting semantic or rendering; presentation-only change stales fixed without changing Revision ID. |
| SPD-INT-006 | Base | AUTOMATED | state | descriptorDigest is SHA-256 of RFC 8785 JCS state JSON with descriptorDigest omitted, producing a cycle-free digest graph. |
| SPD-FIX-001 | Fixed-Experimental | AUTOMATED | fixed-rendition | A fixed rendition identifies its source Revision ID and renditionInputDigest. |
| SPD-FIX-002 | Fixed-Experimental | MANUAL | processor | A Fixed capability claim is not interpreted as making PDF the permanent normative page model. |
| SPD-FIX-003 | Base, Fixed-Experimental | AUTOMATED | archive | PDF/A-4 is not required for Base or ordinary Fixed conformance. |
| SPD-MAP-001 | Mapping | AUTOMATED | renderer | A processor claiming Mapping emits a mapping artifact during fixed rendering. |
| SPD-MAP-002 | Mapping | AUTOMATED | mapping | A mapping is bound to Document ID, Revision ID, and Fixed Rendition ID plus digest. |
| SPD-MAP-003 | Mapping | MANUAL | mapping | Backward reconstruction is not the required normative mapping-generation method. |
| SPD-MAP-004 | Mapping | PARTIALLY_AUTOMATED | mapping | A mapping does not contain glyph rendering, fonts, drawing operations, line-breaking, or page-layout instructions whose purpose is to recreate layout. |
| SPD-MAP-005 | Mapping | AUTOMATED | mapping | Mapping statuses enforce fragment and reason cardinalities for MAPPED, PARTIALLY_MAPPED, NOT_VISIBLE, UNMAPPABLE, and UNSUPPORTED. |
| SPD-MAP-006 | Mapping | PARTIALLY_AUTOMATED | mapping | A processor does not fabricate geometry to claim full coverage. |
| SPD-MAP-007 | Mapping | AUTOMATED | mapping-record | Each mapping record identifies generation mechanism or evidence class. |
| SPD-MAP-008 | Mapping | AUTOMATED | text-range | Mapping text ranges refer to semantic Unicode order. |
| SPD-MAP-009 | Mapping | AUTOMATED | text-range | Semantic text is not reordered to match page geometry. |
| SPD-MAP-010 | Mapping, Fixed-Experimental | AUTOMATED | report | Visual, mapping, fixed-text, and fixed-profile fidelity are not treated as interchangeable. |
| SPD-MAP-011 | Mapping | AUTOMATED | mapping | A Mapping claim includes valid page identifiers, status, provenance, logical ranges where used, and page-bounded geometry. |
| SPD-MAP-012 | Mapping | AUTOMATED | geometry | Mapping geometry uses finite page-local CSS reference pixels with top-left origin, x right, y down, TL-TR-BR-BL quads, and declared rendition-local page dimensions. |
| SPD-ACC-001 | Base, Accessible | PARTIALLY_AUTOMATED | accessibility | Base accessibility is evaluated against the authoritative semantic XHTML rendition. |
| SPD-ACC-002 | Accessible, Fixed-Experimental | PARTIALLY_AUTOMATED | fixed-export | A standalone fixed export claiming accessibility independently satisfies the accessibility requirements of its fixed format. |
| SPD-ACC-003 | Accessible, Fixed-Experimental | MANUAL | fixed-export | Accessible XHTML is not used to claim that an independently distributed inaccessible PDF is accessible. |
| SPD-ACC-004 | Accessible | PARTIALLY_AUTOMATED | document | An SPD Accessible 0.1 claim satisfies EPUB Accessibility 1.1 and WCAG 2.2 Level AA, including applicable human evaluation. |
| SPD-PROV-001 | Base | AUTOMATED | provenance | Prompt transcripts and chain-of-thought are not required portable provenance. |
| SPD-IMP-001 | Base | AUTOMATED | imported-semantics | Imported semantic information distinguishes asserted source semantics from inferred semantics. |
| SPD-IMP-002 | Base | AUTOMATED | importer | An importer does not silently upgrade inferred structure to asserted structure. |
| SPD-IMP-003 | Base | INFORMATIVE_ONLY | importer | The format does not claim lossless conversion of arbitrary PDF to semantic SPD. |
| SPD-API-001 | Base | PARTIALLY_AUTOMATED | format | The file format exposes stable structures suitable for a companion transactional API. |
| SPD-CAP-001 | Base | AUTOMATED | processor | A processor does not silently misrepresent an unsupported capability. |
| SPD-CAP-002 | Base | AUTOMATED | capability | Documents declare only capability ID and version; normative or experimental status is specification-controlled. |
| SPD-CAP-003 | Base | AUTOMATED | discovery | EPUB discovery metadata and the authoritative document-state capability declaration agree exactly. |
| SPD-DISC-001 | Base | AUTOMATED | discovery | container.xml contains exactly one link for each required SPD document-state, resource-inventory, and lifecycle-state relationship. |
| SPD-DISC-002 | Base | AUTOMATED | discovery | Each SPD descriptor link has the exact provisional relationship token, application/json media type, and a safe path resolving to one existing resource. |
| SPD-DISC-003 | Base | AUTOMATED | processor | Processors do not discover SPD descriptors by filename scanning or guessing. |
| SPD-DISC-004 | Base | INFORMATIVE_ONLY | release | Provisional descriptor, capability, schema, and annotation identifiers are replaced by stable project-controlled identifiers before Release Candidate. |
| SPD-EXT-001 | Base | AUTOMATED | extension | Extensions use globally unique identifiers or namespaces. |
| SPD-EXT-002 | Base | AUTOMATED | extension | Each extension declares whether it is required or optional. |
| SPD-EXT-003 | Base | AUTOMATED | processor | An unknown required extension causes its affected capability to be reported unsupported. |
| SPD-TEST-001 | Base | INFORMATIVE_ONLY | conformance-corpus | Conformance development includes multilingual and structurally difficult fixtures. |
| SPD-TEST-002 | Base | INFORMATIVE_ONLY | conformance-corpus | The normative corpus includes Arabic and mixed-bidirectional text. |
| SPD-GOV-001 | Archive-Experimental | INFORMATIVE_ONLY | archive | Archive rules are developed separately from Base conformance. |
| SPD-GOV-002 | Fixed-Experimental | INFORMATIVE_ONLY | annex | The experimental PDF annex does not alter Base conformance. |
| SPD-GOV-003 | Fixed-Experimental | INFORMATIVE_ONLY | standardization | A fixed media format becomes normative only after the evidence gate in section 67 is met. |
| SPD-GOV-004 | Base | INFORMATIVE_ONLY | standardization | New mechanisms are introduced only for demonstrated architectural gaps. |
| SPD-PASS-001 | Base | PARTIALLY_AUTOMATED | content-and-processor | SPD Base content is untrusted passive document data and SHALL NOT supply executable application behavior. A Base processor SHALL NOT execute document-supplied code or grant publication-originated application authority. |
| SPD-PASS-002 | Base | PARTIALLY_AUTOMATED | content | Base SHALL obey the normative inert-control/embedded-context profiles: no forms, active contexts, automatic navigation, base overrides or authoritative interactive canvas; preserved controls SHALL be disabled, labeled inert representations without capture, form association, submission or activation behavior. |
| SPD-PASS-003 | Base | PARTIALLY_AUTOMATED | content-and-processor | Base meaning SHALL be complete in a stable static presentation without animation, transitions, autoplay or interactive state changes. Processors SHALL suppress their execution. Local media MAY play only after user action with equivalent accessible semantics available without playback. |
| SPD-RS-001 | Base | MANUAL | processor | An SPD reader SHALL deny publication-originated network, filesystem, camera, microphone, location, shared-cookie, persistent Web storage and service-worker authority. External HTTP/HTTPS hyperlinks require intentional user action and host mediation without destination access to the document context. |
| SPD-RS-002 | Base | MANUAL | processor | An SPD processor SHALL distinguish displayed semantic content, declared SEALED, verified SEALED/current state and verified current fixed rendition. Unverified views MUST NOT be represented as verified sealed/fixed or authenticated; hash integrity is not signer or issuer authentication. |
