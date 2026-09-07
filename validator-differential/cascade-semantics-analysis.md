# Cascade semantics

Decision: **C. Both are reasonable document validators, but the differential normalization contract must define dependency/cascade semantics.**

This describes the reporting strategies, not blanket approval of either implementation. Confirmed predicate/applicability mistakes remain bugs. Neither A's particular suppression policy nor B's complete emitted superset is mandated by the frozen rules.

## What the Draft does and does not define

Draft §§26–29 and 70–73 define the actual state, byte-digest and currentness invariants. §§62 and 74 distinguish incomplete evaluation from PASS but do not prescribe a per-requirement dependency graph, redundant-ID closure, or minimal-primary-error normalizer. The frozen differential contract asks for identical unique failed/NOT_TESTED IDs without supplying those policies. Its roll-up requires positive evidence for PASS and an established applicable failure for FAIL.

Document validity remains clear in these cases. Reporting which of several overlapping IDs accompanies an already-established failure is NORMALIZATION_CONTRACT_BUG, not SPEC_AMBIGUITY. An absent operand is not a false operand, and an observed mismatch does not cease to exist merely because a different check failed.

## Dependency model

Arrows below mean the downstream check needs the indicated facts, not that every upstream result must be PASS.

```text
read exact ZIP bytes ───────────────► compare resource length/hash
        │
        └──► parse inventory fields ─► declared-inventory projections
                    │                          │
exact inventory bytes + state binding ─► exact inventory-binding equality
                    │                          │
                    └──► verified semantic/rendering input state
                                      │
fixed bytes + fixed ID/revision/input bindings ─► fixed currentness
                                      │
SEALED applicability ──────────────────┼──► required sealed fixed currentness
Mapping claim + mapping binding ───────┴──► Mapping dependency validity

container rootfile ─► OPF/spine facts (independent of SPD descriptor discovery)
descriptor links ─► unique authorized target ─► parse/typed fields ─► claims
                                                            OPF + claims ─► equality

spine XML bytes ─► strict XML parse ─► authoritative Node-ID occurrences
                                      │
                                      └──► duplicate witness / complete index
```

A hash mismatch is a failed equality, not missing bytes. A malformed XML document, by contrast, does not supply a trustworthy DOM. An inventory projection over supplied fields is testable even if those fields do not accurately describe the resources. That comparison must be labelled as a declared-field consistency check, not certification of verified current content.

## Outcome rules

| Evidence situation | Appropriate treatment |
|---|---|
| An applicable predicate has all needed operands and a counterexample | FAIL, even if another failure caused or preceded it |
| A required operand cannot be obtained through authorized discovery/parse | NOT_TESTED for the dependent check, with prerequisite reason; never synthesize empty values |
| One branch of a conjunction is demonstrably false, another unavailable | FAIL can be established without evaluating every conjunct |
| Known duplicate in two parsed resources, another spine resource unparseable | Uniqueness FAIL is established by the duplicate witness; complete uniqueness PASS is impossible |
| Requirement is outside known lifecycle/claim/processor scope | NOT_APPLICABLE or excluded, not FAIL and not an unavailable-tool error |
| Suppression of an already-established redundant diagnostic | Only a declared normalization policy may omit it; omission is not a test result of PASS |

None of the frozen 25 differences changes the NOT_TESTED ID set. Thus agreement on that set does not demonstrate correct propagation. Proposed future normalization may add blocked IDs; this analysis does not rewrite either frozen result.

## Bad resource hash: all four B-only IDs

The package is EDITABLE with fixed absent. Inventory content.xhtml has the correct length (516) but a zero hash; actual SHA-256 is `51fa731ac4db46fa989874e0d223dcbf3020ebb5b6d786ddc17fa831b6840935`. The inventory file itself no longer matches its lifecycle binding.

RES-004 is directly false. INT-004 and INT-005 are independently false: serialize the declared inventory fields exactly as §70 specifies, including the `sha256:` prefix, NUL separators and LF record terminators. The resulting digests are respectively `d774ef728e31b285e4f10985af261ed70550723d3401f6ad65f722587dd13aa3` and `f2d76f12b5ef7cda3db25403375d4a7419dedcf1b176e7d41968b2b5940594ec`, neither matching the corresponding descriptor declaration. No inference about unavailable original bytes is required. These should not become NOT_TESTED solely because the inventory binding is wrong.

STATE-002 is different: the inventory-binding equality is indeed false, but that registered rule is explicitly about **sealed state**. The package is EDITABLE. General integrity failure is established, while a sealed-state violation is not applicable. B's integrity.py:129–134 applies that ID without checking lifecycle. A's validator.rs:456–497 reports the inventory binding failure as INT-003 and skips inventory/projection diagnostics. The three extra equality findings expose suppression differences; the fourth exposes a B attribution bug.

## Descriptor discovery

Missing fixture: container.xml has no SPD links. Its rootfile still authorizes reading OPF and the authoritative XHTML spine. None of the three descriptor authorities exists; a file with a plausible name is forensic evidence only.

Conflict fixture: both document-state and lifecycle links name `META-INF/spd/state.json`. Reading that explicit target establishes that it fails the document-state schema: it lacks nested revision and capabilities and contains lifecycle-only fields. Candidate-schema diagnostics can describe that fact. They cannot turn the candidate's absent capability array into an authoritative empty claim set. Its flat revisionId also cannot be compared with a fabricated missing revision as though both were independently authorized semantic identities.

B does **not** scan filenames in these paths. epub.py:80–104 records the conflicting targets but retains them; descriptors.py:39–64 loads discovered candidates even after schema errors. validator.py:26–50 substitutes `{}`/empty claims and derives ARCH-001, CAP-002 and CAP-003. ARCH-001 is particularly unsupported: a missing Base declaration does not prove that exactly-one-authoritative-representation is false. CAP-003 equality is blocked when the authoritative declaration is unavailable. A returns on discovery_bad at validator.rs:296–308. Proposed policy should retain independent OPF checks, quarantine invalid descriptor authority, and distinguish candidate-schema failures from downstream semantic claims.

## XHTML and external-tool scope

The event-handler document is well-formed XML with **two n_heading01 occurrences at content.xhtml:4**, one on an h1 carrying onclick. No rule exempts event-handler elements from SPD-ID-006. A's event_ids filter at validator.rs:929–941 suppresses that real duplicate. B's ID finding is not a parser artifact. The duplicate-node-id fixture similarly has two n_paragraph01 occurrences at lines 6 and 7.

invalid-xhtml cannot yield a valid DOM; native SEM-002 and external malformed-content failures can still be established from parsing itself. B does not emit an ID-006 finding for this malformed fixture. JavaScript and the three external-resource fixtures are parseable; their explicit script/event/resource references and OPF declarations can be checked independently.

The external diagnostics corroborate these defects: duplicate-node-id RSC-005; event-handler OPF-014/RSC-005; external CSS RSC-006; external font OPF-014/RSC-008; external image OPF-014/RSC-006; invalid XHTML RSC-005/RSC-016; JavaScript OPF-014. EPUB requires the relevant manifest properties when applicable; see [EPUB 3.3 resource properties](https://www.w3.org/TR/epub-33/#sec-item-resource-properties). This supports the independent EPUB failures; it does not automatically choose an SPD requirement ID for every EPUB diagnostic.

Both adapters map a failed EPUBCheck run to BASE-002 (A validator.rs:104–116; B epubcheck.py:92–94). Therefore **EXTERNAL_TOOL_DIFFERENCE = 0 for differing versions or diagnostic parsing/mapping between A and B**. However, **seven fixture ID differences are associated with unequal external evaluation scope**: A's freeze and external report cover 31 valid/edge fixtures, all PASS; B records 69 runs, 61 PASS and 8 FAIL. The eighth failure, duplicate-normalized-path, already has native BASE-002 in A, so does not add that differential ID. No A external logs exist here for the seven invalid fixtures: do not claim paired-run agreement for them.

A's production validate_path would run the adapter even after native failures. Its corpus test uses validate_reader, and the frozen golden surface does not incorporate the additional invalid-fixture external outcomes. This is an oracle/evaluation-scope normalization problem, not evidence that EPUBCheck itself produced different results. A future common run must define full EPUB versus OCF coverage and a shared diagnostic-to-SPD rule table: BASE-002's registry text specifically mentions OCF, while OPF/content failures are broader. Do not equate a convenient aggregate adapter label with normative proof of that exact OCF predicate.

## Inventory cross-failures

The duplicate-normalized-path inventory contains decomposed `EPUB/cafe\u0301.txt` alongside `EPUB/caf\u00e9.txt`. The former violates NFC independently of the ZIP-name collision. path-traversal inventories `../escape.txt`, rejected by the canonical path schema. No unsafe entry was extracted during analysis; bytes were read directly from ZIP members.

Unlisted `EPUB/extra.css` and `EPUB/cache.bin` are outside both self-reference exceptions. RES-003 explicitly includes non-normative caches, and RES-006 forbids every unlisted non-exempt entry. Both apply. A's OPF-filename heuristic at validator.rs:752–766 chooses only one; B's integrity.py:109–117 reports both. The Draft does not prescribe that ID-selection heuristic. Absence of a duplicate diagnostic is a contract-convergence issue, not by itself a conformance bug.

## State cases

Every extra state-family ID is assessed individually in fixture-differences.md and requirement-differences.md. Key distinctions:

- All mutation resource bytes are readable, so RES-004 and INT-003 are established; most declared-inventory projections still match because the inventory was not updated. Do not falsely add INT-004/005 merely because live resource bytes changed.
- SEALED semantic-affecting XHTML/SVG mutations invalidate the semantic integrity binding. A comment-only change is still an exact-byte change in an inventoried semantic-affecting resource; no claim of changed visible meaning is necessary.
- CSS has affects=[rendering]; fixed, mapping and annotations have affects=[]. Their mutations invalidate SEALED under §27, but do not establish the narrower semantic-content-specific STATE-003 predicate. B integrity.py:162–164 conflates any covered seal failure with that ID.
- Mutation-fixed directly disproves its own current hash, establishing STATE-005, SEALED currentness STATE-006, and Mapping dependency STATE-007. These are failed conjunctions, not unevaluable comparisons. Processor-behavior STATE-001 is not proven by a document alone; a false current declaration has its own STATE-005 predicate.
- Mutation-mapping has a directly failed SEALED mapping binding (STATE-002) even though its extra byte does not prevent parsing JSON. Integrity operates on exact bytes.
- Both stale fixtures declare status=stale in EDITABLE and claim Mapping. STATE-007 is established. A Mapping claim does not demonstrate that a reader actually exposed stale content as current (STATE-001). In stale-fixed-rendition the numerical bindings happen to match; a declared stale token still cannot satisfy a required-current claim. A chooses STATE-001 instead of STATE-007; B emits both. The shared STATE-001 is unsupported, including in the corpus oracle.

## Geometry

mapping-invalid-geometry passes the canonical mapping schema. Page p_1 is 816×1056; its ordered finite quad reaches x=-1/900 and y=1200. Both its structure and dimensions remain usable for checking bounds. §36 explicitly bounds visible fragments and §56 requires page-bounded Mapping geometry. MAP-011 directly names bounds; MAP-012 points to the §36 geometry model, with shorter registry wording. Retaining both is defensible, but the contract must explicitly settle overlapping requirement-ID attribution. It is not a need for NOT_TESTED or a change to document validity.

## Limits

This is a differential investigation, not proof of total validator correctness. Shared omissions outside these fixtures may exist. In particular, neither a matching frozen verdict nor identical NOT_TESTED arrays certifies that every required manual or downstream check was performed. No implementation was executed or repaired to manufacture agreement.
