# Reader security scenarios

Eight processor scenarios, NOT ordinary package-validator fixtures. All remain NOT_TESTED until a reader exists; package PASS supplies no runtime evidence.

- **R1: No automatic publication-originated network.** Observe DNS/HTTP/WebSocket and speculative traffic from before import through preview and reading; exercise CSS imports/fonts/SVG/media/ping/prefetch and annotation contexts. Zero external requests.
- **R2: No filesystem, device or Web storage authority.** Probe file/UNC/drive paths, camera, microphone, location, cookies, localStorage/IndexedDB and service workers. No document authority or permission prompt; host preferences remain separate.
- **R3: Explicit external hyperlink mediation.** Before activation, zero contact. After intentional activation, trusted host shows interpreted HTTP/HTTPS destination and opens isolated context without opener, credentials or package-data access.
- **R4: Truthful SEALED and fixed verification.** Evaluate declared SEALED/current fixed, stale fixed, semantic-only SEALED, failed and unsupported verification. Semantic display is not verified SEALED; stale/unverified fixed is not verified current; no hash-only authentication.
- **R5: Bounded hostile declarative processing.** Exercise ZIP/XML/DOM/CSS/SVG/MathML work budgets and cancel operations. RESOURCE_LIMIT and effective worker cancellation; no invented universal format maximum.
- **R6: Complete static presentation and local media.** Animations/transitions/autoplay suppressed; controls inert and labeled; meaningful static state and accessible equivalents manually assessed; local playback only after user action.
- **R7: Font/image/media decoder containment.** Use malformed decoder inputs and nested SVG. Observe isolated failure and bounded work with no privilege escalation or fabricated successful content.
- **R8: Untrusted annotations and stable source identity.** Render hostile-looking annotations/metadata as data; no trusted UI injection or context fetch. Detect source mutation and ambiguous paths; no sanitized SEALED view represented as verified original.

Machine-readable source: tests/reader-security/scenarios.json. R1–R8 retain the approved audit groups; R2 explicitly covers all device/storage boundaries and R4 both generic and stale-fixed representations.
