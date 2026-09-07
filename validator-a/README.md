# SPD Validator A

Validator A 0.1.0-rc1 is the Rust reference conformance validator for SPD Format 0.1 RC1. It evaluates the versioned RC1 specification, 118-requirement registry, canonical schemas, and 107-fixture corpus. It is read-only, accepts an explicit package path regardless of extension, and never downloads tools or validation resources at runtime.

## Build and use

From `validator-a/`:

```powershell
cargo build --release
cargo run --bin spd-validator -- validate ..\tests\corpus-0.1-rc1\valid\minimal-base\document.epub --format text --epubcheck C:\tools\epubcheck-5.3.0\epubcheck.jar
cargo run --bin spd-validator -- validate document.epub --format json
cargo run --bin spd-validator -- explain SPD-MAP-008
```

Exit codes are `0` for conformance in the evaluated scope, `1` for conformance failure, `2` for incomplete evaluation or unavailable required tooling, `3` for an operational resource limit, `4` for an internal validator error, and `5` for CLI or unknown-requirement errors. Omitting EPUBCheck never produces a false Base `PASS`: an otherwise conforming input becomes `NOT_TESTED` with `TOOL_UNAVAILABLE`.

The reusable API is `validate_path(path, options) -> ValidationReport` or `validate_reader(reader, options) -> ValidationReport`. The CLI uses the same library. Default safety ceilings are operator controls, not SPD format limits.

Run `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, and `cargo test --all-targets` before submitting validator changes. The qualifying RC1 aggregate is summarized in [`../reports/format-0.1-rc1/RC1_VALIDATION_REPORT.md`](../reports/format-0.1-rc1/RC1_VALIDATION_REPORT.md).
