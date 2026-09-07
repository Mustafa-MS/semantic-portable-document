use spd_validator::{Outcome, ValidationOptions, validate_reader};
use std::{fs::File, path::PathBuf};

fn fixture(name: &str) -> spd_validator::ValidationReport {
    let root = PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .unwrap()
        .to_path_buf();
    validate_reader(
        File::open(
            root.join("tests/corpus-0.1-rc1")
                .join(name)
                .join("document.epub"),
        )
        .unwrap(),
        &ValidationOptions::default(),
    )
}

#[test]
fn revision_scope_and_duplicate_evidence() {
    assert_eq!(fixture("valid/multi-spine").base, Outcome::Pass);
    let bad = fixture("invalid/cross-spine-duplicate-node-id");
    assert_eq!(bad.base, Outcome::Fail);
    let finding = bad
        .findings
        .iter()
        .find(|f| f.requirement_id == "SPD-ID-006")
        .unwrap();
    assert_eq!(finding.evidence["first"]["resource"], "EPUB/chapter1.xhtml");
    assert_eq!(
        finding.evidence["duplicate"]["resource"],
        "EPUB/chapter2.xhtml"
    );
    assert_eq!(finding.evidence["first"]["line"], 4);
    assert_eq!(finding.evidence["duplicate"]["line"], 4);
}

#[test]
fn security_is_not_an_identity_exemption() {
    let ids = fixture("invalid/event-handler").violation_ids();
    assert!(ids.contains(&"SPD-SEC-001".into()));
    assert!(ids.contains(&"SPD-ID-006".into()));
}

#[test]
fn stale_rules_are_document_not_processor_rules() {
    for name in [
        "stale-fixed-rendition",
        "mapping-with-stale-fixed",
        "mutation-fixed",
    ] {
        let ids = fixture(&format!("invalid/{name}")).violation_ids();
        assert!(ids.contains(&"SPD-STATE-007".into()));
        assert!(!ids.contains(&"SPD-STATE-001".into()));
    }
}

#[test]
fn lifecycle_and_effects_guard_state_predicates() {
    let bad = fixture("invalid/bad-resource-hash").violation_ids();
    assert!(!bad.contains(&"SPD-STATE-002".into()));
    for id in ["SPD-RES-004", "SPD-INT-003", "SPD-INT-004", "SPD-INT-005"] {
        assert!(bad.contains(&id.into()));
    }
    for name in [
        "mutation-css",
        "mutation-fixed",
        "mutation-mapping",
        "sealed-after-annotation-modification",
    ] {
        let ids = fixture(&format!("invalid/{name}")).violation_ids();
        assert!(ids.contains(&"SPD-RES-004".into()));
        assert!(!ids.contains(&"SPD-STATE-003".into()));
    }
}

#[test]
fn unknown_claims_are_not_empty_and_xml_prerequisites_are_explicit() {
    for name in [
        "descriptor-discovery-missing",
        "descriptor-discovery-conflict",
    ] {
        let result = fixture(&format!("invalid/{name}"));
        assert_eq!(result.authoritative_claims_status, "UNKNOWN");
        assert_eq!(result.capabilities["Mapping"], "UNKNOWN");
        assert!(
            result
                .not_tested_requirements
                .contains(&"SPD-CAP-003".into())
        );
        assert!(!result.violation_ids().contains(&"SPD-ARCH-001".into()));
    }
    assert!(
        fixture("invalid/invalid-xhtml")
            .not_tested_requirements
            .contains(&"SPD-ID-006".into())
    );
}

#[test]
fn all_reviewed_overlaps_remain_visible() {
    for name in [
        "unlisted-normative-resource",
        "unlisted-non-normative-resource",
    ] {
        let ids = fixture(&format!("invalid/{name}")).violation_ids();
        for id in ["SPD-RES-003", "SPD-RES-006"] {
            assert!(ids.contains(&id.into()));
        }
    }
    let ids = fixture("invalid/mapping-invalid-geometry").violation_ids();
    for id in ["SPD-MAP-011", "SPD-MAP-012"] {
        assert!(ids.contains(&id.into()));
    }
    for name in ["duplicate-normalized-path", "path-traversal"] {
        assert!(
            fixture(&format!("invalid/{name}"))
                .violation_ids()
                .contains(&"SPD-RES-002".into())
        );
    }
}

#[test]
fn bounded_fuzz_smoke() {
    // Deterministic hostile byte sequences exercise the ZIP gate under strict limits.
    let options = ValidationOptions {
        max_package_bytes: 4096,
        max_entry_bytes: 1024,
        max_entries: 8,
        ..Default::default()
    };
    for seed in 0..128_u32 {
        let bytes: Vec<_> = (0..seed)
            .map(|i| (i.wrapping_mul(73).wrapping_add(seed) % 256) as u8)
            .collect();
        let result = validate_reader(std::io::Cursor::new(bytes), &options);
        assert_ne!(
            result.operational_status,
            spd_validator::OperationalStatus::InternalError
        );
    }
}
