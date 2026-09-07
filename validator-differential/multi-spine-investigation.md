# Multi-spine investigation — RC_BLOCKER

Primary classification: CORPUS_ORACLE_BUG. Secondary: VALIDATOR_A_BUG.

Frozen results: A Base=PASS, no violations; B Base=FAIL, SPD-ID-006. Both have no claimed normative capability beyond Base. This is the sole Base-verdict disagreement.

## Normative evidence, before implementation evidence

Draft §5 (line 199) makes the OPF spine authoritative for reading order. §8 (lines 307–319) defines one authoritative semantic rendition consisting of one or more ordered XHTML resources. §14 (line 509) states: “Node IDs MUST be unique in the current authoritative semantic revision.” SPD-ID-006 repeats that scope. It does not say “within each resource.” Dividing one revision into multiple XHTML files does not create independent Node-ID namespaces.

The document-state schema /$defs/nodeId defines the n_ token syntax, not a resource-qualified identity. The schema cannot by itself check uniqueness across XHTML files. No schema exception narrows §14.

XML's ID validity constraint is document-scoped; a merely named `id` attribute is not automatically a typed XML ID without the applicable vocabulary/schema. SPD adds the stronger revision-scoped Node-ID constraint. Per-XML-document uniqueness does not permit duplicate SPD identities across this rendition. See [XML 1.0 Fifth Edition, §3.3.1](https://www.w3.org/TR/xml/#id).

## Actual package

`tests/valid/multi-spine/document.epub` contains one OPF rootfile, `EPUB/package.opf`. Manifest c1 and c2 resolve to chapter1.xhtml and chapter2.xhtml; the spine lists c1 then c2. Both belong to Document ID `urn:uuid:11111111-1111-4111-8111-111111111111`, Revision ID `urn:uuid:22222222-2222-4222-8222-222222222222`.

| Authoritative resource | Node IDs, in document order |
|---|---|
| EPUB/chapter1.xhtml | n_article01, n_heading01, n_section01, n_heading02, n_paragraph01, n_list0001, n_listitem01 |
| EPUB/chapter2.xhtml | n_article01, n_section02, n_heading03, n_paragraph02 |

The duplicated ID is **n_article01**:

- `EPUB/chapter1.xhtml:4`, `<body><article id="n_article01">`, XPath `/*/*[2]/*` (html/body/article).
- `EPUB/chapter2.xhtml:4`, `<body><article id="n_article01">`, the same structural XPath in a different resource.

There are 11 occurrences and 10 distinct Node IDs in the authoritative spine. The navigation document is not a spine item. Although it also uses n_article01, it is not necessary to establish the violation and was not included in this comparison's spine index. B is not creating the observed duplicate by combining unrelated navigation or OPF IDs.

Both spine XML documents parse without recovery. Document/inventory/lifecycle schemas pass; recorded inventory bytes and projections match. EPUBCheck passes because this is an SPD cross-resource identity restriction, not a duplicate within either XML document. Exact package hash, source lines and ID occurrences are recorded in fixture-byte-evidence.json.

## Oracle contradiction

`tests/valid/multi-spine/expected.json` expects Base PASS and an empty violation list. The corpus manifest labels it valid. CONFORMANCE_MATRIX.md even lists multi-spine as a positive ID test, including SPD-ID-006 (line 43). Those lower-priority artifacts cannot override §14: the current package is invalid.

## Implementation explanation, inspected last

A's `validator-a/src/validator.rs:938` creates `let mut ids = HashSet::new()` inside the per-spine-XHTML loop. The insertion/duplicate check at lines 940–949 therefore sees only one resource at a time. B's `validator-b/spd_validator_b/semantics.py:179` through 186 inserts spine Node IDs into the shared semantic model and detects the second article occurrence. The normative conclusion was established from Draft/registry/package/schema/XML evidence before this source inspection.

## Proposed repair, not performed

Validator A: use a revision-wide index for authoritative semantic Node IDs; preserve separate XML-local ID validation where relevant.

Corpus: either rename the second article Node ID and consistently recompute affected inventory/state digests to retain a genuinely valid multi-spine test, or relabel the current bytes as a negative cross-spine duplicate test. Prefer retaining both positive and negative cases in the later repair stage. Never weaken the Draft to bless the current fixture. No package, expectation, implementation, or specification was changed here.

CORPUS_WRONG
