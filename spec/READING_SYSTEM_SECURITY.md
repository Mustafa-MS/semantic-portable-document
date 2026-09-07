# SPD reading-system security

## Normative processor conformance

SPD-PASS-001–003 and SPD-RS-001–002 apply to SPD-aware processors. EPUB Reading Systems 3.3, Recommendation 17 October 2024, supplies explicitly relied-on processing context; publication conformance alone neither proves reader conformance nor imports every EPUB reader recommendation.

Document content is untrusted passive data. Processors SHALL NOT execute document-supplied code or expose application command/IPC authority. They SHALL deny publication-originated network (including speculative requests, contexts and link checking), filesystem/UNC access, camera, microphone, location, shared cookies, persistent Web storage and service-worker state. This boundary applies before validation/preview as well as afterward. Host-owned rendering processes/frames, reading position, preferences, temporary cache and deliberate import/export are separate host operations.

External HTTP/HTTPS hyperlinks require intentional user activation and host mediation. No automatic ping/prefetch/preload/DNS request is authorized; destinations MUST NOT gain access to the document context. Trusted UI SHOULD expose the interpreted destination. Validators never visit links.

Base suppresses animation, transitions, automatic navigation and autoplay. Optional local media playback requires user action and accessible alternatives; inert preserved controls must not acquire submission/activation behavior. Static completeness requires human evaluation.

Processors SHALL distinguish semantic content displayed, declared SEALED, verified SEALED/current state and verified current fixed rendition. Generic/unverified views MUST NOT be labeled verified sealed/fixed or authenticated. Hash integrity is not issuer/signer authentication. Ordinary EPUB readers cannot be required to show SPD UI. Sensitive workflows MAY require SPD-aware viewing or an explicit derivative reading copy. No mandatory embedded warning, new lifecycle state or signature is introduced.

Validation inspects without mutating source. A sanitized/rewritten SEALED source MUST NOT retain a verified-source claim. Existing revision rules govern any repair.

## Non-normative implementation hardening

Use immutable input snapshots, one verified virtual package identity, narrow resource channels, isolated workers and patched XML/CSS/SVG/MathML/font/image/media decoders. Keep author text/annotation bodies out of trusted UI templates. Do not recursively unpack nested archives by default. CSP and process isolation are defense in depth, not proof of safety.

Apply configurable budgets to ZIP input/expanded bytes, compression ratio, entries, actual reads, DOM depth/nodes, CSS complexity, SVG expansion/filter regions, image dimensions, font tables/glyphs, render time and memory. Cancellation should reach workers. No universal numeric ceilings are added to Format 0.1. RESOURCE_LIMIT reports an operational limit, not a fabricated document rule. A conforming file can still exploit a vulnerable decoder.

The [reader conformance plan](../tests/reader-security/scenarios.json) is processor evidence, NOT ordinary package-validator fixtures. It remains NOT_TESTED until an actual reader exists and is evaluated.
