use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::{collections::BTreeMap, path::PathBuf, time::Duration};

#[derive(Debug, Clone)]
pub struct ValidationOptions {
    pub epubcheck: Option<PathBuf>,
    pub epubcheck_timeout: Duration,
    pub max_package_bytes: u64,
    pub max_entries: usize,
    pub max_entry_bytes: u64,
    pub max_total_uncompressed_bytes: u64,
    pub max_compression_ratio: u64,
    pub max_xml_bytes: usize,
    pub max_json_bytes: usize,
    pub max_mapping_records: usize,
}

impl Default for ValidationOptions {
    fn default() -> Self {
        Self {
            epubcheck: None,
            epubcheck_timeout: Duration::from_secs(120),
            max_package_bytes: 512 * 1024 * 1024,
            max_entries: 10_000,
            max_entry_bytes: 256 * 1024 * 1024,
            max_total_uncompressed_bytes: 1024 * 1024 * 1024,
            max_compression_ratio: 1_000,
            max_xml_bytes: 32 * 1024 * 1024,
            max_json_bytes: 64 * 1024 * 1024,
            max_mapping_records: 1_000_000,
        }
    }
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq, PartialOrd, Ord)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum Outcome {
    Pass,
    Fail,
    NotTested,
    NotApplicable,
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq, PartialOrd, Ord)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum Severity {
    Error,
    Warning,
    Information,
    NotTested,
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum OperationalStatus {
    Complete,
    ToolUnavailable,
    ToolError,
    ResourceLimit,
    MalformedInput,
    InternalError,
    SpecBlocker,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(rename_all = "camelCase")]
pub struct Finding {
    pub requirement_id: String,
    pub outcome: Outcome,
    pub severity: Severity,
    pub capability: String,
    pub stage: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub resource: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub node_id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub revision_id: Option<String>,
    pub message: String,
    #[serde(default, skip_serializing_if = "Value::is_null")]
    pub evidence: Value,
    pub source: String,
}

#[derive(Debug, Clone, Default, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct ToolEvidence {
    pub name: String,
    pub version: Option<String>,
    pub profile: String,
    pub outcome: String,
    pub exit_code: Option<i32>,
    #[serde(flatten, default)]
    pub detail: BTreeMap<String, Value>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Reproducibility {
    pub validator_version: String,
    pub spec_version: String,
    pub requirements_registry_version: String,
    pub requirements_registry_sha256: String,
    pub schema_bundle_sha256: String,
    pub unicode_version: String,
    pub options: BTreeMap<String, Value>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct ValidationReport {
    pub validator: String,
    pub base: Outcome,
    pub capabilities: BTreeMap<String, String>,
    pub authoritative_claims_status: String,
    pub experimental_reporting: Value,
    pub operational_status: OperationalStatus,
    pub document_id: Option<String>,
    pub revision_id: Option<String>,
    pub findings: Vec<Finding>,
    pub manual_requirements: Vec<String>,
    pub not_tested_requirements: Vec<String>,
    pub external_tools: Vec<ToolEvidence>,
    pub reproducibility: Reproducibility,
}

impl ValidationReport {
    pub fn violation_ids(&self) -> Vec<String> {
        let mut ids: Vec<_> = self
            .findings
            .iter()
            .filter(|f| f.outcome == Outcome::Fail)
            .map(|f| f.requirement_id.clone())
            .collect();
        ids.sort();
        ids.dedup();
        ids
    }
}
