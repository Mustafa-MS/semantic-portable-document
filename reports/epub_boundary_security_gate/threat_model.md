# Threat model and ZIP/renderer analysis

An attacker controls every byte of an SPD file, including ZIP headers, content, metadata, inventory, claimed digests, annotations and a purported SEALED/fixed state. Assets at risk are device execution integrity, local data, credentials/privacy, availability, and truthful representation of semantic/fixed state. The attacker may also supply links to hostile destinations. The host application, validator binaries and trust UI are separate boundaries, not automatically trusted because the file passes a check.

## Threat/control matrix

| Attacker input or technique | Format mitigation | Validator mitigation | Reader mitigation | Remaining risk |
| --- | --- | --- | --- | --- |
| Malicious ZIP | Existing OCF/SPD path, method, duplicate and inventory rules | Safe scan, unique lookup, bounded decompression | Virtual package filesystem; no unsafe extraction | ZIP library bugs, header/size ambiguity and resource exhaustion |
| Malicious XML/XHTML | XML/EPUB conformance and passive-element rules | Namespace-aware parse, no external entities/network; verify references | No document scripts or active contexts; isolated parser/renderer | Parser bugs, entity/depth handling differences, validation gaps |
| Malicious CSS | Local resources, no primary meaning in generated content | Grammar-aware URL checks across all style contexts | Request-layer denial and layout budgets | Escapes/substitution omissions, selector/paint DoS |
| Malicious SVG | No scripts/events/foreignObject/network; static meaning | Check standalone and inline/nested SVG equally | Constrained processing and local resolver, filter limits | Reference recursion, filters, font/paint/GPU bugs |
| Malicious fonts | Local inventoried resource; no remote authoritative font | Byte integrity and resource/type checks | Sandboxed decoder/shaper and size/work budgets | Byte integrity does not establish font safety |
| Malicious images/media | Local inventoried resource; no autoplay | Resource references/type/size checks | Decode isolation, pixel/frame/time budgets | Codec bugs, animated-image work, misleading visual content |
| Malicious MathML | Existing MathML integration plus shared URL/passive rules | XML/structure and nested content checks | Bounded math layout and shaping | Deep/stretchy math layout, maction/resource handling, parser bugs |
| Resource exhaustion | No universal numeric maximum; honest unsupported/limit semantics | Configurable actual-work ceilings | Process memory/CPU/time limits and cancellation | Valid but expensive files; limit selection trades usability for resilience |
| URI/path confusion | Relative paths, NFC, no ambiguous duplicates, deterministic discovery | Same resolver for inventory, OPF and content; reject ambiguity | Virtual namespace, no OS aliases, no external fallback fetch | Percent-encoding/normalization discrepancies and host extraction aliases |
| Integrity confusion | Complete inventory, exact-byte hashes, cycle-free state binding | Recompute and compare, preserve unknown/blocked results | Render the verified snapshot; trusted status outside content | Attacker can recompute hashes; no author authentication |
| Semantic/fixed mismatch | Frozen currentness/mapping and single semantic authority | Check bindings and stale state; do not infer visual equivalence from hash equality | Separate semantic reading from verified fixed presentation | A malicious producer can bind a visually false fixed rendition; mapping is not proof of semantic equivalence |
| Malicious annotation data | Existing selectors/scope/inventory/seal rules; passive rendering applies when displayed | Strict JSON, scope/identity/range checks; no network contexts | Data-only annotation display, no HTML/URL execution bridge | Deceptive annotation text, injection if host templates are unsafe |
| Misleading link or fake verification badge | No automatic navigation; no document-owned trust claim | Validate role/scheme, not truth of destination/content | Explicit host mediation and trusted verification UI | Phishing and user deception remain possible |

## ZIP/OCF protections: attribution, not assumptions

Sources: [current SPD OCF profile](../../spec/profiles/ocf-profile.md), [Validator A package scanner](../../validator-a/src/package.rs), [Validator B package scanner](../../validator-b/spd_validator_b/package.py), and [EPUB 3.3 OCF §4](https://www.w3.org/TR/2026/REC-epub-33-20260113/#sec-ocf). “Delegated” below is not a claim of comprehensive testing of a ZIP dependency.

| Issue | OCF contribution | Existing SPD addition | A/B implementation evidence and limitation |
| --- | --- | --- | --- |
| Path traversal | Rooted abstract-container/path model | Explicit dot-segment/traversal and decoded-reference rejection | Both scan names; B resolves URL-decoded references. Runtime extraction containment still required. |
| Absolute/drive/UNC paths | Container paths, not arbitrary host filesystem | Explicit absolute/drive/leading-slash prohibition | Both reject major forms; do not trust a filename to be an OS-safe extraction path. |
| Backslashes | OCF naming constraints exclude backslash | Explicit prohibition reinforces it | Both scanners reject backslash. |
| Duplicate ZIP entries | One virtual pathname identifies a resource; external tool reports duplicates | Explicit prohibition even for equal bytes | A HashSet; B raw_seen; convergence includes duplicate/collision evidence. |
| Unicode-normalized collisions | Case-sensitive Unicode path identity; no universal NFC mandate found | Every name already NFC, reject decoded/NFC ambiguous names | Both test raw-name NFC collisions. Neither scan shows the full percent-decoded entry-name collision comparison required by the SPD profile. |
| Compression bombs | Stored/Deflate limits algorithm choices, not expansion cost | Configurable limits recommended; no universal maximum | Both check declared sizes/aggregate/ratio. B bounds actual reads; A read_to_end relies on library/declared-size behavior and checks length afterward. Actual-work enforcement needs review. |
| Entry count | No SPD-style universal security ceiling supplied by OCF | Configurable operational limit | Both implement configurable entry count. |
| Compression ratio | Not a standardized SPD maximum | Configurable operational limit | A integer ratio when compressed size >0; B handles zero compressed size explicitly. These are implementation policies. |
| Encrypted ZIP entries | ZIP encryption prohibited; separate OCF resource encryption exists | Profile also lists encrypted entries as errors | B explicitly checks ZIP flag bit 1. A relies on library opening behavior; no explicit flag check in scanner. Do not equate this with a tested same-attribution guarantee. |
| OCF encryption/font obfuscation | encryption.xml and font obfuscation are different from ZIP encryption | Offline/passive requirements do not alone settle every obfuscation policy | A clear Base policy for encrypted/obfuscated resource processing should be recorded; either may be restricted under A. Hash stored resource bytes and never execute a decryption plugin. |
| Unsupported compression | OCF allows Stored/Deflate only | Reiterated by SPD | Both enforce method 0/8. B does not gain a safer algorithm by renaming the file. |
| Malformed central directory | Must be a conforming ZIP archive | Out-of-archive data prohibited | Parsing delegated to Rust zip/Python zipfile; malformed-input handling exists, comprehensive central/local-header consistency not demonstrated here. |
| Overlapping entries | ZIP validity is not a complete hostile-overlap policy | Outside-archive bounds explicit; no full overlap rule identified in profile prose | No explicit overlap-range gate in either scanner; dependency behavior and cross-implementation tests needed. |
| Symlink/device entries | Abstract files do not authorize host links/devices | Explicitly prohibited by SPD profile | A explicitly checks symlink mode, not every device type; B scanner has no explicit Unix mode/symlink/device check. Neither extracts. No exploit is asserted, but coverage is not established. |
| Nested archives | Can be ordinary uninterpreted resources depending on resource role | Inventory includes them; no blanket recursive archive rule | No recursive unpacking in the reviewed validators. Reader should keep them inert and never recursively process by default. |
| Resource exhaustion generally | Conformance cannot guarantee bounded work on every machine | Configurable limits and honest operational outcomes | ZIP limits are only one layer; XML/JSON/DOM/fonts/images/layout need separate bounds. |

The observed implementation gaps are shared-boundary audit findings, not a reason to change package identity. Current 70-case agreement does not prove behavior for percent-decoded collisions, symlink/device modes, overlapping entries or hostile actual expansion. Record and test those cases before claiming a complete security gate. Do not silently make one implementation's numeric limits normative.

**Option B materially improves none of these protections compared with strict A.** The same restrictions and parser hardening are possible in A, while B would assume responsibility for maintaining the inherited ZIP rules.

## Renderer attack surface with scripting disabled

| Surface | Why passive input can still be hostile | A versus B |
| --- | --- | --- |
| XML/XHTML parser | Malformed nesting, encodings/entities, namespace integration and very large DOMs | Same parser risk with identical content |
| CSS | Expensive selectors, cascading values, cycles, huge layout dimensions, generated content and hidden meaning | Same parser/layout/performance risk |
| SVG | Path count/precision, recursive references, masks, clipping and large filter buffers | Same graphics/DoS/GPU risk |
| MathML | Deep tables/fractions, stretchy operators, font-dependent layout, mixed-markup integration | Same math layout/shaping risk |
| Fonts | Binary font table parsing, decompression, glyph outlines and shaping tables | Same decoder/shaper risk |
| Raster images/media | Compressed dimensions, large frames, malformed formats and animation sequences | Same codec/memory risk |
| Unicode shaping/bidi | Complex clusters and long text, bidi presentation confusion, implementation-version differences | Same shaping risk; preserve logical storage and scalar offsets |
| GPU/raster/compositor | Large surfaces, filters and driver bugs invoked by static graphics | Same underlying engine/driver surface |

These risks originate in content technology and implementation, not the EPUB media label. “No scripts” eliminates an execution route, not all code execution vulnerabilities. A passive reader also needs budgets and isolation. The [reader model](reader_security_model.md) separates those responsibilities from file conformance.

Unicode NFC is for package-name identity, not a license to normalize authoritative prose or hashed resource bytes. UAX #9 addresses display order, not the ability to infer the author's intended text. Existing evidence discloses A Unicode 17.0.0 and B 15.1.0; equality on the corpus does not imply full character-version equivalence. [UAX #15](https://www.unicode.org/reports/tr15/tr15-57.html), [UAX #9](https://www.unicode.org/reports/tr9/tr9-51.html), [convergence summary](../../validator-convergence/summary.md).
