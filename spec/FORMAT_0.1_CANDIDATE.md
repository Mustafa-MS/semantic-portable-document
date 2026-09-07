\# Semantic Portable Document Format 0.1



\## Candidate Specification



\*\*Working name:\*\* SPD

\*\*Version:\*\* 0.1

\*\*Status:\*\* Candidate specification

\*\*File extension:\*\* Not yet assigned

\*\*Media type:\*\* Not yet assigned



The working name and identifiers are provisional and do not form part of conformance.



\---



\# 1. Scope



Semantic Portable Document Format 0.1 defines a portable document model in which structured semantic content is authoritative and presentation renditions are derived from that content.



The format is designed for:



\* human reading;

\* structured editing;

\* responsive rendering;

\* accessibility;

\* offline distribution;

\* machine interpretation;

\* AI-agent operations;

\* revision-safe editing;

\* annotations;

\* fixed visual renditions;

\* document integrity.



The format does not attempt to define a new:



\* compression format;

\* markup language;

\* browser engine;

\* font format;

\* vector graphics language;

\* cryptographic algorithm;

\* PDF implementation;

\* accessibility vocabulary.



Existing standards SHALL be reused wherever practical.



\---



\# 2. Conformance Language



The key words:



```text

MUST

MUST NOT

REQUIRED

SHALL

SHALL NOT

SHOULD

SHOULD NOT

MAY

OPTIONAL

```



are normative requirements when written in uppercase.



\---



\# 3. Fundamental Principle



A conforming document SHALL have one authoritative semantic representation.



Presentation shall be derived from that semantic representation.



Conceptually:



```text

&#x20;              Semantic Document

&#x20;                     │

&#x20;             authoritative state

&#x20;                     │

&#x20;         ┌───────────┴───────────┐

&#x20;         │                       │

&#x20;         ▼                       ▼



&#x20;  Responsive Rendering      Fixed Rendition

&#x20;                                 optional/

&#x20;                               experimental

```



A fixed rendition SHALL NOT become a second independently editable source of truth.



\---



\# 4. Normative Technology Baseline



Format 0.1 SHALL reuse stable standards wherever possible.



The initial normative baseline is:



```text

Packaging:

EPUB 3.3 OCF-compatible packaging



Semantic content:

XHTML



Styling:

CSS



Mathematics:

MathML



Vector graphics:

SVG



Text:

Unicode



Annotations:

W3C Web Annotation model



Accessibility:

native HTML semantics

WAI-ARIA where required

DPUB-ARIA where applicable



Integrity:

SHA-256

```



EPUB 3.4 and related draft specifications MAY inform implementations but are not normative dependencies of Format 0.1.



\---



\# 5. Package



A Format 0.1 document SHALL be an OCF-compatible ZIP package.



A package SHALL follow the applicable EPUB 3.3 OCF requirements unless this specification explicitly restricts them further.



The format SHALL NOT redefine ZIP packaging.



\---



\# 6. EPUB Compatibility



A Format 0.1 Base document SHOULD remain usable as an EPUB-compatible publication where practical.



However:



```text

Format 0.1 conformance

≠

ordinary EPUB reader awareness

```



An ordinary EPUB reader is not required to understand:



\* revision state;

\* stable semantic identity rules;

\* mapping artifacts;

\* sealed states;

\* fixed-rendition authority;

\* Agent API semantics.



A Format 0.1 processor MUST NOT assume that an ordinary EPUB reader understands those capabilities.



\---



\# 7. Security Profile



Format 0.1 applies a stricter security profile than unrestricted EPUB/web content.



A conforming Base document MUST NOT require:



\* JavaScript;

\* executable macros;

\* plugins;

\* service workers;

\* automatic network access;

\* remote fonts;

\* remote CSS;

\* remote images required for rendering;

\* executable SVG content.



All resources required to render the authoritative document MUST be available within the package.



External hyperlinks MAY exist.



Following an external hyperlink requires explicit user action.



\---



\# 8. Authoritative Semantic Rendition



Each document SHALL identify exactly one authoritative semantic rendition.



That rendition SHALL consist of one or more ordered XHTML content documents.



The package spine SHALL define their primary reading order.



Semantic content SHALL use native HTML semantics wherever those semantics exist.



Examples include:



```text

article

section

nav



h1-h6



p



ol

ul

li



figure

figcaption



table

thead

tbody

tfoot

tr

th

td



blockquote

cite



code

pre



aside

```



\---



\# 9. Native-Semantics-First Rule



A document SHALL use semantic XHTML before accessibility or custom metadata mechanisms.



Preference order:



```text

1\. Native XHTML semantics

2\. Native XHTML attributes

3\. WAI-ARIA

4\. DPUB-ARIA

5\. supplemental relationship metadata

```



ARIA SHALL NOT be used to replace correct native semantics.



\---



\# 10. Semantic Content Is the Source of Truth



Primary textual or structural content MUST NOT be independently duplicated in another normative resource.



For example, this is invalid:



```text

document.xhtml:



FROC = 0.906





graph.json:



FROC = 0.901

```



Supplemental structured data MAY reference semantic objects.



It MUST NOT redefine their authoritative textual content.



\---



\# 11. Document Identity



Every document SHALL have a persistent:



```text

Document ID

```



The Document ID represents a document lineage rather than a specific revision.



It SHOULD use a globally unique identifier.



UUID-based identities are RECOMMENDED.



\---



\# 12. Revision Identity



Each committed semantic document state SHALL have a:



```text

Revision ID

```



A Revision ID identifies one immutable semantic state.



When normative semantic content changes, a new Revision ID MUST be created.



Changing only non-normative cache data MUST NOT create a new semantic Revision ID.



\---



\# 13. Node Identity



Addressable semantic objects SHALL carry persistent Node IDs.



At minimum, IDs MUST be provided for independently addressable:



\* sections;

\* headings;

\* paragraphs;

\* list items;

\* figures;

\* captions;

\* tables;

\* table rows;

\* table cells;

\* equations;

\* notes;

\* citations;

\* references;

\* preserved form controls.



Implementations MAY assign identities to additional inline structures.



\---



\# 14. Node ID Properties



Node IDs:



\* MUST be unique within a document lineage;

\* MUST NOT depend upon page position;

\* MUST NOT depend upon DOM path;

\* MUST NOT depend upon visible numbering;

\* MUST NOT depend upon text content;

\* MUST NOT use the content hash as identity.



A node that remains logically the same object MAY retain its Node ID after its content changes.



\---



\# 15. Copy, Split, Merge and Deletion



A copied node SHALL normally receive a new Node ID.



A deleted Node ID SHOULD NOT be reused within the same document lineage.



Editors SHOULD preserve lineage information for split and merged objects where practical.



The exact user-interface policy for choosing which node retains identity after split/merge is non-normative.



\---



\# 16. Logical Text



Text in the semantic rendition MUST be represented in logical Unicode order.



Visual placement SHALL NOT determine semantic ordering.



This requirement applies to:



\* Arabic;

\* Hebrew;

\* mixed RTL/LTR text;

\* vertical writing;

\* complex-script content.



Language SHALL be explicitly declared where required for correct interpretation.



Direction SHALL be explicitly declared where necessary.



\---



\# 17. Arabic and Bidirectional Text



Arabic and bidirectional behavior are normative conformance cases.



A compliant processor MUST NOT assume:



```text

visual left-to-right position

=

logical reading order

```



Mapping and editing APIs MUST operate using logical text ranges.



\---



\# 18. Mathematics



Mathematical expressions SHOULD use MathML.



Implementations MUST NOT require mathematical meaning to be reconstructed from visual glyph positions when semantic MathML exists.



A fixed rendition MAY map an equation as one semantic visual region without mapping every mathematical glyph individually.



\---



\# 19. Figures



A semantic figure SHOULD consist of:



```text

figure

asset

figcaption

alternative text where appropriate

```



The relationship between figure, caption and references SHALL remain semantic.



Fixed coordinates SHALL NOT define that relationship.



\---



\# 20. Tables



Tables SHALL use semantic table structures.



Table header relationships SHALL be represented semantically rather than inferred from visual position.



Addressable table cells SHALL have persistent Node IDs.



A cell that spans multiple fixed-page fragments retains one Node ID.



\---



\# 21. Supplemental Relationship Graph



A document MAY contain a supplemental relationship graph.



JSON-LD is the RECOMMENDED representation for Format 0.1.



It MAY describe relationships such as:



```text

paragraph → cites → reference



paragraph → discusses → figure



table → derivedFrom → dataset



claim → supportedBy → citation

```



The graph MUST NOT duplicate authoritative content unnecessarily.



A conforming Base reader is not required to implement a general RDF reasoning engine.



\---



\# 22. Annotations



Annotations SHOULD use the W3C Web Annotation Data Model.



Annotations are normally separate from primary semantic content.



An annotation MAY target:



\* a Node ID;

\* a text range;

\* a figure;

\* a table cell;

\* an equation;

\* a page region in a fixed rendition;

\* another annotation.



\---



\# 23. Stable Node Annotation Selector



Format 0.1 defines a profile for targeting persistent semantic identity.



Conceptually:



```json

{

&#x20; "type": "StableNodeSelector",

&#x20; "document": "...",

&#x20; "revision": "...",

&#x20; "node": "n\_xxxx"

}

```



The final serialized vocabulary and namespace SHALL be registered by the project before final 0.1 publication.



\---



\# 24. Robust Text Annotation



Text annotations SHOULD include both:



```text

stable semantic target

\+

fallback textual selector

```



where practical.



Fallback selectors MAY use mechanisms equivalent to:



\* TextQuoteSelector;

\* TextPositionSelector.



The stable Node ID remains preferable for semantic targeting.



\---



\# 25. Document States



Format 0.1 recognizes at least:



```text

EDITABLE



SEALED

```



\---



\# 26. Editable State



In the EDITABLE state:



\* semantic content is authoritative;

\* the document may be modified;

\* a fixed rendition MAY be absent;

\* an existing fixed rendition MAY be stale.



A processor MUST NOT present a stale fixed rendition as the current authoritative fixed representation.



\---



\# 27. Sealed State



A SEALED document represents a finalized semantic revision.



A sealed state SHALL bind:



```text

semantic Revision ID

\+

normative resource inventory

\+

optional fixed rendition

\+

mapping artifact when applicable

```



Changing normative semantic content invalidates the sealed state.



\---



\# 28. Resource Inventory



A conforming document SHALL maintain one normative resource inventory.



Each normative resource entry SHALL include at least:



```text

normalized package path

media type

byte length

SHA-256 digest

resource role

```



Resources SHOULD be classified where applicable as:



```text

authoritative

generated

inferred

cached

non-normative

```



\---



\# 29. Integrity



Integrity is distinct from digital identity.



Format 0.1 SHALL provide digest-based integrity verification.



At minimum SHA-256 SHALL be supported.



Integrity checks SHALL detect modification to:



\* semantic content;

\* normative styles;

\* normative assets;

\* mapping;

\* fixed rendition;

\* state metadata.



\---



\# 30. Digital Signatures



A normative outer-package digital-signature mechanism is NOT defined by Format 0.1.



Implementations MAY experiment with existing standardized signature systems.



No implementation may claim a Format 0.1 signature profile until such a profile is separately standardized.



\---



\# 31. Fixed Rendition Concept



A document MAY contain a fixed rendition.



A fixed rendition is a generated representation preserving a specific page appearance.



Conceptually:



```text

Semantic Revision R

&#x20;      │

&#x20;      ▼

Renderer

&#x20;      │

&#x20;      ├────────→ Mapping M

&#x20;      │

&#x20;      ▼

Fixed Rendition F

```



A fixed rendition SHALL identify the semantic revision from which it was generated.



\---



\# 32. Fixed Rendition Status in 0.1



Format 0.1 does NOT normatively require one specific fixed-page media format.



PDF 2.0 is the project reference fixed-rendition implementation during Format 0.1.



It remains an experimental profile.



A processor SHALL NOT interpret:



```text

Fixed capability

```



as meaning:



```text

PDF is the permanent normative page model

```



\---



\# 33. Fixed Rendition Immutability



Once a fixed rendition is associated with a sealed semantic revision, it SHALL be treated as immutable for that revision.



Regeneration produces a new fixed-rendition identity.



\---



\# 34. Semantic-to-Fixed Mapping



When a processor claims semantic-to-fixed mapping capability, it SHALL emit a mapping artifact during fixed rendering.



The mapping SHALL be bound to:



```text

Document ID

Revision ID

Fixed Rendition ID or digest

```



\---



\# 35. Mapping Generation



The mechanism used to generate mapping is implementation-specific and non-normative.



A conforming processor MAY use:



\* browser layout information;

\* paginated DOM;

\* layout-engine APIs;

\* another reliable forward-layout mechanism.



Mapping reconstruction from a fixed rendition MAY be used for:



\* validation;

\* recovery;

\* legacy import.



It SHALL NOT be the required normative method of generating mappings.



\---



\# 36. Mapping Model



A mapping consists of semantic correspondence rather than another page-description language.



A mapping MAY contain:



```text

Node ID

logical text range

page ID

quadrilateral

bounding region

transform

status

provenance

```



It SHALL NOT contain information whose purpose is to recreate:



\* glyph rendering;

\* fonts;

\* drawing operations;

\* line breaking;

\* page layout algorithms.



\---



\# 37. Mapping Fragment



A semantic node MAY map to zero, one or multiple page fragments.



Example:



```text

Node n\_123



fragment 1

&#x20;   page p1

&#x20;   logical range 0-74



fragment 2

&#x20;   page p2

&#x20;   logical range 75-161

```



This supports semantic objects crossing page boundaries.



\---



\# 38. Mapping Status



A mapping system SHALL support explicit outcomes equivalent to:



```text

MAPPED

PARTIALLY\_MAPPED

NOT\_VISIBLE

UNMAPPABLE

UNSUPPORTED

```



Processors MUST NOT fabricate geometry merely to claim full mapping coverage.



\---



\# 39. Mapping Provenance



Mapping records SHALL identify the generation mechanism or evidence class.



Examples include:



```text

forward-layout

backward-recovery

inferred

manual

```



The exact registry of values will be defined with the mapping schema.



\---



\# 40. Mapping and Bidirectional Text



Logical text ranges in mappings SHALL refer to semantic Unicode order.



Geometric fragments describe visual location.



These two orders MAY differ.



Processors MUST NOT reorder semantic text solely to match page geometry.



\---



\# 41. Visual Fidelity, Mapping Fidelity and Text Fidelity



Format 0.1 distinguishes:



```text

VF — Visual Fidelity



MF — Mapping Fidelity



PF — fixed-rendition text fidelity



CF — fixed-rendition format/profile conformance

```



These properties SHALL NOT be treated as interchangeable.



For example:



```text

MF = PASS

PF = FAIL

```



is a valid reportable state.



\---



\# 42. Accessibility Authority



For a Format 0.1 Base document, the authoritative semantic XHTML rendition is the primary accessibility representation.



Accessibility SHALL be evaluated against that representation.



A fixed rendition is not automatically required to provide a second independently accessible semantic representation.



\---



\# 43. Accessible Fixed Export



A standalone fixed-format export that claims accessibility MUST satisfy the accessibility requirements of that fixed format independently.



For PDF this may include:



```text

PDF/UA

WTPDF accessibility

```



as appropriate.



Semantic XHTML accessibility SHALL NOT be used to claim that an independently distributed inaccessible PDF is accessible.



\---



\# 44. PDF Reference Rendition



The Format 0.1 reference implementation MAY generate PDF 2.0 fixed renditions.



Such PDFs MAY use:



\* Tagged PDF;

\* PDF/UA;

\* WTPDF;

\* semantic compilation;

\* ActualText;

\* structure trees.



These mechanisms are not required for Base Format 0.1 conformance.



\---



\# 45. PDF Text Interoperability Warning



Format 0.1 does not assume that formal Tagged PDF/PDF-UA/WTPDF conformance guarantees identical logical text extraction across all PDF consumers.



Implementations claiming a high-quality accessible PDF export SHOULD test:



\* search;

\* extraction;

\* copy/paste;

\* Arabic;

\* mixed bidi;

\* independent consumers.



\---



\# 46. Archive Capability



Long-term archival conformance is not part of Base 0.1.



An Archive capability MAY require:



\* sealed state;

\* all normative resources embedded;

\* no active content;

\* preservation metadata;

\* fixed rendition;

\* archival fixed-format profile.



PDF/A-4 is the current reference archival fixed-rendition target.



PDF/A-4 SHALL NOT be required for ordinary Base or Fixed documents.



\---



\# 47. Forms



Format 0.1 does not define a complete interoperable forms/workflow model.



Safe semantic form controls MAY be preserved.



Automatic submission, arbitrary calculations, workflow scripting and executable logic are outside Base 0.1.



\---



\# 48. Revision Provenance



A revision SHOULD record minimal provenance including:



```text

Revision ID

parent Revision ID

timestamp

generator

generator version

```



An implementation MAY record additional provenance.



Prompt transcripts and AI chain-of-thought SHALL NOT form part of required portable provenance.



\---



\# 49. Imported Semantics



Imported semantic information SHALL distinguish authoritative source semantics from inferred semantics.



Examples:



```text

native XHTML heading

→ ASSERTED



AI-inferred PDF heading

→ INFERRED

```



An importer MUST NOT silently upgrade inferred structure to asserted structure.



\---



\# 50. PDF Import



PDF import is inherently potentially lossy.



A PDF importer SHOULD preserve:



\* original source PDF;

\* extraction provenance;

\* inferred Node IDs;

\* confidence/evidence where applicable.



The format SHALL NOT claim that arbitrary PDF can be losslessly converted to semantic Format 0.1.



\---



\# 51. Agent Processing Model



The file format SHALL expose stable document structures suitable for a companion transactional API.



The file specification itself does not define programming-language method names.



The companion API MAY support operations conceptually equivalent to:



```text

query node

replace text

update table cell

move section

replace figure

insert citation

add annotation

validate

render

seal

```



\---



\# 52. Transaction Safety



A companion transactional processor SHOULD support revision preconditions.



Example concept:



```text

baseRevision = R105

```



If the current revision is:



```text

R106

```



the attempted mutation SHOULD fail rather than overwrite newer content.



\---



\# 53. Atomic Multi-Node Changes



Changes that semantically form one edit SHOULD be applied atomically.



For example:



```text

change table result

\+

update paragraph discussing result

```



should either both commit or neither commit.



\---



\# 54. Conformance Capabilities



Format 0.1 defines the following capability model:



```text

Base

Mapping

Fixed-Experimental

Accessible

Archive-Experimental

```



Future versions may define:



```text

Signed

Forms

TrackedChanges

Collaborative

Encrypted

```



\---



\# 55. Base Capability



Base is normative in Format 0.1.



Base requires:



\* valid OCF-compatible package;

\* authoritative XHTML rendition;

\* navigation;

\* resource inventory;

\* offline required resources;

\* secure content restrictions;

\* Document ID;

\* Revision ID;

\* persistent Node IDs;

\* logical Unicode text;

\* semantic structure;

\* integrity digests.



\---



\# 56. Mapping Capability



Mapping is normative in Format 0.1.



Mapping requires:



\* fixed-rendition binding;

\* semantic Node IDs;

\* forward-emitted mapping artifact;

\* page identification;

\* mapping status;

\* provenance;

\* logical text ranges where used;

\* valid page geometry.



\---



\# 57. Fixed-Experimental Capability



Fixed rendering remains experimental in Format 0.1.



The specification defines its lifecycle and binding semantics but does not yet designate a permanent normative fixed-page encoding.



PDF 2.0 is the initial reference implementation.



\---



\# 58. Accessible Capability



Accessible Base conformance applies to the semantic rendition.



An implementation claiming an accessible standalone export MUST also satisfy the accessibility rules of the exported format.



\---



\# 59. Archive-Experimental Capability



Archive remains experimental.



The current reference fixed archival representation is PDF/A-4.



Archive rules SHALL be developed separately from Base conformance.



\---



\# 60. Graceful Degradation



A processor that does not implement an optional capability SHOULD still expose the authoritative semantic content where safe.



A processor MUST NOT silently misrepresent unsupported capabilities.



For example:



```text

Fixed rendition unavailable

```



is preferable to displaying a stale or incorrect fixed state.



\---



\# 61. Extensions



Extensions SHALL use globally unique identifiers or namespaces.



Extensions SHALL declare whether they are:



```text

required

optional

```



Unknown optional extensions SHOULD be preserved.



Unknown required extensions SHALL cause the affected capability to be reported as unsupported.



\---



\# 62. Conformance Reports



Validators SHOULD produce machine-readable conformance reports.



A report SHOULD distinguish at least:



```text

ERROR

WARNING

INFORMATION

NOT\_TESTED

```



It SHOULD identify the relevant:



\* resource;

\* Node ID;

\* revision;

\* capability;

\* rule.



\---



\# 63. Test Corpus



Format 0.1 conformance development SHALL include multilingual and structurally difficult fixtures.



Arabic and mixed bidirectional text SHALL be included in the normative test corpus.



Tests SHOULD include:



\* long multipage text;

\* tables across pages;

\* figures;

\* SVG;

\* MathML;

\* notes;

\* citations;

\* multi-column layout;

\* Arabic;

\* mixed Arabic/Latin;

\* CJK where practical;

\* Indic complex shaping where practical.



\---



\# 64. Explicit Non-Goals



Format 0.1 does not attempt to provide:



\* universal office-suite compatibility;

\* arbitrary scripting;

\* browser applications inside documents;

\* DRM;

\* universal PDF round-trip;

\* universal DOCX round-trip;

\* a spreadsheet calculation engine;

\* a presentation animation engine;

\* a new page renderer;

\* a new cryptographic trust infrastructure.



\---



\# 65. Format 0.1 Success Criterion



The primary technical purpose of Format 0.1 is to standardize:



```text

semantic authoritative content

\+

persistent object identity

\+

immutable revision identity

\+

safe portable packaging

\+

semantic-to-fixed correspondence

\+

integrity binding

\+

machine-safe structured processing

```



while continuing to reuse mature standards for everything else.



\---



\# 66. Experimental Fixed-PDF Annex



The reference implementation SHOULD maintain an experimental PDF fixed-rendition annex documenting:



\* PDF 2.0 generation;

\* Tagged PDF experiments;

\* PDF/UA;

\* WTPDF;

\* ActualText behavior;

\* Arabic and bidi extraction;

\* semantic PDF compilation;

\* visual-scene preservation.



This annex is informative for Format 0.1 and SHALL NOT alter Base conformance.



\---



\# 67. Future Standardization Gate



A fixed-rendition media format SHALL become normative only after evidence demonstrates:



1\. stable fixed appearance;

2\. cross-implementation rendering support;

3\. acceptable international text behavior;

4\. adequate accessibility strategy;

5\. viable long-term maintenance;

6\. independent implementation experience.



Until then, the fixed-rendition abstraction remains intentionally decoupled from one permanent encoding.



\---



\# 68. Governing Principle



Where a mature interoperable standard exists, Format 0.1 SHOULD profile or reuse it.



New mechanisms SHALL be introduced only when they address a demonstrated architectural gap.



The intended innovation is the document lifecycle and correspondence model, not reinvention of existing media technologies.



