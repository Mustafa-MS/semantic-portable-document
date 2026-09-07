# Dependency decisions

Versions below are pinned by `Cargo.lock`.

| Dependency | Version | Purpose / standard | License / status | Decision and alternatives |
|---|---:|---|---|---|
| clap | 4.6.6 | CLI | MIT/Apache-2.0; active | typed CLI; preferred to hand parsing |
| zip | 4.6.1 | bounded ZIP/Deflate access | MIT; active | safe Rust; preferred to extraction/system unzip |
| roxmltree | 0.20.0 | bounded read-only XML/XHTML DOM | MIT/Apache-2.0; maintained | small immutable DOM; quick-xml considered |
| serde / serde_json | 1.0.229 / 1.0.151 | JSON/report model | MIT/Apache-2.0; active | ecosystem baseline; strict duplicate visitor added |
| jsonschema | 0.33.0 | JSON Schema 2020-12 | MIT; active | local embedded schemas; procedural-only validation rejected |
| serde_json_canonicalizer | 0.3.2 | RFC 8785 JCS | MIT/Apache-2.0; maintained | uses ryu-js; hand-written number serialization rejected |
| sha2 / hex | 0.10.9 / 0.4.3 | SHA-256 serialization | MIT/Apache-2.0; RustCrypto active | maintained crypto rather than custom SHA-256 |
| unicode-normalization | 0.1.25 | path NFC | MIT/Apache-2.0; maintained | standard Unicode tables rather than custom normalization |
| regex | 1.13.1 | bounded security token checks | MIT/Apache-2.0; active | linear-time engine; full CSS parser remains future hardening |
| wait-timeout | 0.2.1 | external-tool timeout | MIT/Apache-2.0 | avoids shell/platform polling |
| tempfile | 3.27.0 | isolated adapter support | MIT/Apache-2.0; active | safe lifecycle if adapters need temporary evidence |
| thiserror | 2.0.20 | structured errors | MIT/Apache-2.0; active | avoids unstructured string-only public errors |
| proptest / walkdir | 1.11.0 / 2.5.0 | tests only | MIT/Apache-2.0; active | property generation and deterministic corpus traversal |

EPUBCheck 5.3.0 is an operator-supplied external tool, pinned for regression;
Validator A does not redistribute or download it during validation.
