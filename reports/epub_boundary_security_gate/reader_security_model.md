# Reader security model

This is **non-normative implementation guidance**. Candidate interoperable reader obligations are isolated in P4/P5 of [the passive proposal](passive_content_profile.md). Numeric limits and sandbox technology choices below are not new format limits.

## Separate three kinds of requirements

| Layer | Examples | What success means |
| --- | --- | --- |
| File conformance | No scripts/events/remote fetch declarations; unambiguous package names; valid inventories and local references | The input meets stated syntactic/semantic predicates |
| Reader conformance | Deny document network/filesystem/device authority; host-mediated links; truthful verification status | Observed reader behavior honors the processing contract, including for invalid files |
| Implementation hardening | Process isolation, memory/CPU ceilings, patched decoders, timeouts, font/image sandboxing | Limits the impact of malformed input and implementation vulnerabilities |

A PASS from Validator A/B is not an authorization to enable browser privileges. The reader must withstand an entirely malicious package, including files that fail validation, before its first preview is painted. A conforming EPUB input does not require its reader to claim all EPUB optional capabilities. General-purpose EPUB readers remain outside SPD reader conformance unless they implement it.

## Reference-reader boundary

Use a trusted controller for input selection, immutable package snapshots, verification status, link mediation and deliberate export. Parse/decompress in a constrained worker; expose a virtual read-only package filesystem rather than extracting directly into a browser-visible directory. Render in a separate unprivileged process with only a narrow package-resource channel. A document must not inherit application IPC, command dispatch, user cookies, credentials, browser profiles or local server privileges.

Network denial must cover the actual fetch layer: HTTP(S), WebSocket, service workers, speculative requests, CSS/font/image loading, media, redirects, XML external entities, XInclude, remote JSON-LD contexts and helpfully generated previews. Never rely only on the absence of JavaScript or on a CSS sanitizer. If a loopback asset server is used, it still needs per-document authorization, path isolation, no directory listing and no route to other local services. A virtual resource resolver avoids many of those hazards.

Deny filesystem/UNC/drive traversal, camera, microphone, geolocation, notifications and document permission prompts. A host “save as,” file picker, annotation store or reading-position database is allowed only through host-controlled intent and bounded interfaces; it is not Web authority exposed to the document. Use disposable document contexts without cookies/shared localStorage/IndexedDB. A private bounded temporary cache may exist and must not persist as a document application.

Host controls may use JavaScript and host-owned frames internally. They must not turn author bytes into same-origin trusted application content or expose a bridge by attribute/URL injection. Sandboxing headers and CSP can be defense in depth, but their delivery and coverage must be verified; this report does not prescribe an untested CSP string as a complete security model.

## Resource budgets

Apply configurable limits to compressed input bytes, actual expanded bytes, entry count, individual entries, expansion ratio, XML/JSON depth and size, DOM nodes, CSS rule/selector work, SVG reference depth/filter regions, decoded image pixels, font table/glyph sizes, media decode work, mapping records, layout/paint time and total resident memory. Count work during decompression and decoding; declared ZIP/image dimensions are not trustworthy budgets. Cancellation must reach workers and decoders, not merely hide a spinner.

Report **RESOURCE_LIMIT**, **UNSUPPORTED** or malformed-input results as appropriate. Do not label a limit violation as exceeding a universal SPD maximum that does not exist. A file can be format-valid and exceed a particular device's memory budget. Do not invent geometry or silently omit meaning after a timeout.

Fonts, image decoders, Unicode shaping, complex MathML, SVG filters and GPU paths still process hostile input without scripts. Keep those components patched, sandbox decoding/rasterization where feasible, and limit GPU surfaces. Isolating the main browser process alone does not prove a codec or driver cannot be attacked. Software rendering can trade GPU exposure for CPU/DoS costs; it is not universally safer.

## Verification and display

Read a stable input snapshot to prevent validation/rendering time-of-check/time-of-use drift. Hash exact bytes used by the renderer. Use one path resolver and one selected ZIP-entry identity across integrity, extraction and display. NFC comparison must not cause silent stored-name rewriting; Windows case folding, reserved names and trailing-dot aliases must not merge distinct virtual entries during extraction.

Display semantic reading separately from the optional current fixed rendition. A trusted status indicator should say what was actually verified and must be outside author-controlled content. SEALED is an internal consistency state, not identity authentication; signatures remain outside Format 0.1. An attacker can produce a completely self-consistent but false document.

Treat annotation bodies, titles, URLs and metadata as untrusted data. Never interpolate them into privileged HTML. Do not dereference annotation contexts or targets automatically. Keep annotation edits and the existing revision/seal consequences unchanged. If unsafe content is transformed for a convenience view, identify it as a derived unverified view; do not claim unchanged verified appearance.

## Eight proposed runtime scenarios

| ID | Test scenario | Required observation |
| --- | --- | --- |
| R1 | All automatic fetch routes, including CSS/import/font/SVG/media/ping/prefetch/context references | Zero publication-originated external requests, including before validation completes |
| R2 | File/UNC/custom-scheme access, device permissions and storage/cookie probes | No filesystem/device/shared-storage authority; no document-triggered permission dialog |
| R3 | Explicit external link activation | Trusted destination mediation, no automatic contact, no opener/credential/package-data leakage |
| R4 | SEALED R8/F8, stale fixed and semantic-only seal | Trusted UI distinguishes declared/verified/unsupported states and does not invent a fixed canonical view |
| R5 | ZIP/XML/DOM/CSS/SVG/MathML resource exhaustion | Bounded work and effective cancellation; operational result distinct from a format maximum |
| R6 | Optional animations/transitions, inert controls, local media | Complete static Base view, no autoplay or document-driven edits; user-mediated local playback works |
| R7 | Malformed fonts/images/embedded SVG and decoder failures | Worker containment, no privilege escalation path, visible failure rather than fabricated content |
| R8 | Malicious annotations/metadata, duplicate path views and source mutation during display | No trusted-DOM injection, one verified byte/path identity, source changes detected |

These are eight runtime scenarios, not additional claims that existing validators have run them. Package fixtures cannot prove them. The identical scenarios apply to A and B. [EPUB Reading Systems 3.3](https://www.w3.org/TR/2024/REC-epub-rs-33-20241017/) supplies relevant origin/scripting context, but SPD's stronger no-authority policy must be enforced by the actual implementation.
