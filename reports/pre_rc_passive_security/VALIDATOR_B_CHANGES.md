# Validator B 0.1.2

The frozen 0.1.1 sources/wheel and historical evidence are retained. Python independently uses lxml and tinycss2 in spd_validator_b/passive.py. It inspects namespace-qualified nested XHTML/SVG/MathML, style elements/attributes, stylesheet tokens/imports/font roles, custom-property resource tokens, fragments, graph cycles and remote/unsafe references. Existing semantic/identity/integrity/mapping algorithms remain separate and unchanged in meaning. No Rust parser code is reused.

The ZIP scanner adds decoded-name identity checks, symlink/device policy, local/central header comparisons and overlap/bounds checks. Malformed and resource-limited input retain operational status and untested predicates. Whole-publication EPUB errors add BASE-002; XHTML-specific mappings do not attribute OPF title errors to SEM-002. Crashes, partial diagnostics and timeouts are NOT_TESTED/TOOL_UNAVAILABLE. Reader/human portions remain untested.

tests/test_passive.py exercises token obfuscation, inert text, namespace/fragment behavior, dynamic resource uncertainty and property-generated CSS. Existing package/schema/security/property/Unicode/algorithm tests and all 107 native expectations are retained. The versioned wheel bundles attribution data 0.1.2. Runtime authority and semantic completeness require the separate reader/manual plan.
