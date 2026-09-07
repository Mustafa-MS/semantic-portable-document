use serde_json::Value;
use spd_validator::{Outcome, ValidationOptions, validate_reader};
use std::{collections::BTreeSet, fs::File, path::PathBuf};

fn repo() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .unwrap()
        .to_path_buf()
}

#[test]
fn corpus_normalized_classification() {
    let manifest: Value = serde_json::from_reader(
        File::open(repo().join("tests/corpus-0.1-rc1/manifest.json")).unwrap(),
    )
    .unwrap();
    for fixture in manifest["fixtures"].as_array().unwrap() {
        let expected: Value = serde_json::from_reader(
            File::open(repo().join(fixture["expectedResult"].as_str().unwrap())).unwrap(),
        )
        .unwrap();
        let report = validate_reader(
            File::open(repo().join(fixture["package"].as_str().unwrap())).unwrap(),
            &ValidationOptions::default(),
        );
        let actual: BTreeSet<_> = report.violation_ids().into_iter().collect();
        let wanted: BTreeSet<_> = expected["nativeViolationRequirementIds"]
            .as_array()
            .unwrap()
            .iter()
            .map(|v| v.as_str().unwrap().to_owned())
            .collect();
        assert_eq!(actual, wanted, "{}", fixture["id"]);
        assert_eq!(
            serde_json::to_value(report.base).unwrap(),
            expected["nativeBase"],
            "{}",
            fixture["id"]
        );
    }
}

#[test]
fn unavailable_epubcheck_is_incomplete_not_pass_or_document_failure() {
    let report = spd_validator::validate_path(
        repo().join("tests/corpus-0.1-rc1/valid/minimal-base/document.epub"),
        &ValidationOptions::default(),
    );
    assert_eq!(report.base, Outcome::NotTested);
    assert_eq!(
        report.operational_status,
        spd_validator::OperationalStatus::ToolUnavailable
    );
    assert!(
        report
            .findings
            .iter()
            .all(|finding| finding.outcome != Outcome::Fail)
    );
}

#[test]
fn production_report_matches_implementation_schema() {
    let report = validate_reader(
        File::open(repo().join("tests/corpus-0.1-rc1/valid/minimal-base/document.epub")).unwrap(),
        &ValidationOptions::default(),
    );
    let instance = serde_json::to_value(report).unwrap();
    let schema: Value =
        serde_json::from_str(include_str!("../schemas/validator-report.schema.json")).unwrap();
    let validator = jsonschema::options()
        .with_draft(jsonschema::Draft::Draft202012)
        .build(&schema)
        .unwrap();
    let errors: Vec<_> = validator
        .iter_errors(&instance)
        .map(|e| e.to_string())
        .collect();
    assert!(errors.is_empty(), "{errors:?}");
}

#[test]
fn all_requirements_have_coverage_registration() {
    let coverage: Value = serde_json::from_reader(
        File::open(repo().join("validator-a/requirements-coverage.json")).unwrap(),
    )
    .unwrap();
    let entries = coverage.as_object().unwrap();
    assert_eq!(entries.len(), 118);
    assert_eq!(
        entries
            .values()
            .filter(|v| v["status"] == "implemented-automatic")
            .count(),
        74
    );
    assert!(
        entries
            .values()
            .all(|v| v.get("stage").is_some() && v.get("module").is_some())
    );
}

#[test]
fn frozen_differential_oracle_is_complete() {
    let frozen: Value = serde_json::from_reader(
        File::open(repo().join("validator-a/reports/golden/validator-a-0.1.0-draft.1.json"))
            .unwrap(),
    )
    .unwrap();
    assert_eq!(frozen["validator"], "Validator A 0.1.0-draft.1");
    assert_eq!(frozen["fixtureCount"], 69);
    assert_eq!(frozen["results"].as_array().unwrap().len(), 69);
    assert!(
        frozen["results"]
            .as_array()
            .unwrap()
            .iter()
            .all(|r| r["operationalStatus"] == "COMPLETE")
    );

    let epub: Value = serde_json::from_reader(
        File::open(repo().join("validator-a/reports/epubcheck-corpus-results.json")).unwrap(),
    )
    .unwrap();
    assert_eq!(epub["version"], "5.3.0");
    assert_eq!(epub["applicableCount"], 31);
    assert!(
        epub["results"]
            .as_array()
            .unwrap()
            .iter()
            .all(|r| { r["exitCode"] == 0 && r["normalizedResult"] == "PASS" })
    );
}
