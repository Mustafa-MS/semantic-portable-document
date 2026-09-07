//! Shared Contract 0.1.1 data; native validation is implemented in Rust.
use serde_json::Value;
use std::{collections::BTreeSet, sync::OnceLock};

pub fn data() -> &'static Value {
    static POLICY: OnceLock<Value> = OnceLock::new();
    POLICY.get_or_init(|| {
        serde_json::from_str(include_str!(
            "../../validation/REQUIREMENT_ATTRIBUTION_0.1.2.json"
        ))
        .expect("versioned attribution data")
    })
}

pub fn blocked(group: &str) -> Vec<String> {
    data()["blocked"][group]
        .as_array()
        .expect("known evidence group")
        .iter()
        .map(|v| v.as_str().unwrap().to_owned())
        .collect()
}

pub fn attribute(output: &str) -> Vec<String> {
    let diagnostic = regex::Regex::new(r"\b(?:ERROR|FATAL)\(([A-Z]+-\d+[a-z]?)\)").unwrap();
    let mut result = BTreeSet::new();
    for line in output.lines() {
        if let Some(found) = diagnostic.captures(line) {
            result.insert("SPD-BASE-002".to_owned());
            for rule in data()["externalDiagnostics"].as_array().unwrap() {
                if rule["code"].as_str() == Some(&found[1])
                    && regex::Regex::new(rule["pattern"].as_str().unwrap())
                        .unwrap()
                        .is_match(line)
                {
                    for id in rule["ids"].as_array().unwrap() {
                        result.insert(id.as_str().unwrap().to_owned());
                    }
                }
            }
        }
    }
    result.into_iter().collect()
}
