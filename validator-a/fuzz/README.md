# Fuzzing

Install `cargo-fuzz`, then run `cargo fuzz run package`. The package target drives
the ZIP gate and, for reachable inputs, container XML, strict JSON, inventory,
mapping, and XHTML parsers under small resource ceilings. Crashes are validator
defects, not document-conformance rules.
