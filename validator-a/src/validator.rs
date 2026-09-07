use crate::{
    Finding, OperationalStatus, Outcome, Reproducibility, SPEC_VERSION, Severity, ToolEvidence,
    UNICODE_VERSION, VALIDATOR_VERSION, ValidationOptions, ValidationReport, epubcheck, package,
    strict_json,
};
use roxmltree::Document;
use serde_json::{Value, json};
use sha2::{Digest, Sha256};
use std::{
    collections::{BTreeMap, BTreeSet, HashMap, HashSet},
    fs::File,
    io::{Read, Seek},
    path::Path,
};
use unicode_normalization::UnicodeNormalization;

const REGISTRY: &str = include_str!("../../spec/requirements-0.1-rc1.yaml");
const DOC_SCHEMA: &str = include_str!("../../schemas/rc1/document-state.schema.json");
const INV_SCHEMA: &str = include_str!("../../schemas/rc1/resource-inventory.schema.json");
const STATE_SCHEMA: &str = include_str!("../../schemas/rc1/state.schema.json");
const MAP_SCHEMA: &str = include_str!("../../schemas/rc1/mapping.schema.json");
const ANN_SCHEMA: &str = include_str!("../../schemas/rc1/annotation-extension.schema.json");
const STABLE_NODE_SELECTOR: &str = "urn:uuid:95d3b3f6-45bb-50fd-9aa5-8bba8186649f";

fn sha(b: &[u8]) -> String {
    format!("sha256:{}", hex::encode(Sha256::digest(b)))
}
fn f(
    id: &str,
    cap: &str,
    stage: &str,
    res: Option<&str>,
    node: Option<&str>,
    msg: impl Into<String>,
) -> Finding {
    Finding {
        requirement_id: id.into(),
        outcome: Outcome::Fail,
        severity: Severity::Error,
        capability: cap.into(),
        stage: stage.into(),
        resource: res.map(str::to_owned),
        node_id: node.map(str::to_owned),
        revision_id: None,
        message: msg.into(),
        evidence: Value::Null,
        source: "Validator A".into(),
    }
}
fn nt(id: &str, cap: &str, stage: &str, msg: &str) -> Finding {
    Finding {
        requirement_id: id.into(),
        outcome: Outcome::NotTested,
        severity: Severity::NotTested,
        capability: cap.into(),
        stage: stage.into(),
        resource: None,
        node_id: None,
        revision_id: None,
        message: msg.into(),
        evidence: Value::Null,
        source: "Validator A".into(),
    }
}
fn strp<'a>(v: &'a Value, p: &str) -> Option<&'a str> {
    v.pointer(p)?.as_str()
}
fn safe_path(s: &str) -> bool {
    !s.is_empty()
        && !s.starts_with('/')
        && !s.starts_with('\\')
        && !s.contains('\\')
        && !s.contains("//")
        && !s.contains(':')
        && !s.split('/').any(|x| x == "." || x == "..")
        && s.nfc().collect::<String>() == s
}
fn registry_ids(kind: &str) -> Vec<String> {
    REGISTRY
        .lines()
        .filter(|l| l.contains(&format!("testability: {kind}")))
        .filter_map(|l| l.split("id: ").nth(1)?.split(',').next().map(str::to_owned))
        .collect()
}

pub fn explain_requirement(id: &str) -> Option<String> {
    REGISTRY
        .lines()
        .find(|l| l.contains(&format!("id: {id},")))
        .map(|l| l.trim().to_owned())
}

pub fn validate_path(path: impl AsRef<Path>, o: &ValidationOptions) -> ValidationReport {
    let path = path.as_ref();
    let file = match File::open(path) {
        Ok(x) => x,
        Err(e) => {
            return fatal_report(
                OperationalStatus::MalformedInput,
                format!("cannot open input: {e}"),
            );
        }
    };
    let mut r = validate_reader(file, o);
    if let Some(tool) = &o.epubcheck {
        let t = epubcheck::run(tool, path, o.epubcheck_timeout);
        for id in t
            .detail
            .get("normalizedSpdAttributionIds")
            .and_then(Value::as_array)
            .into_iter()
            .flatten()
        {
            r.findings.push(f(
                id.as_str().expect("attributed requirement ID"),
                "Base",
                "epub",
                None,
                None,
                "EPUBCheck reported inherited EPUB errors",
            ));
            r.base = Outcome::Fail;
            for cap in ["Mapping", "Accessible"] {
                if r.capabilities
                    .get(cap)
                    .is_some_and(|v| v != "NOT_CLAIMED" && v != "UNKNOWN")
                {
                    r.capabilities.insert(cap.into(), "FAIL".into());
                }
            }
        }
        if t.outcome != "PASS" && t.outcome != "FAIL" {
            if r.base == Outcome::Pass {
                r.base = Outcome::NotTested;
            }
            r.operational_status = OperationalStatus::ToolUnavailable;
            r.not_tested_requirements.push("SPD-BASE-002".into())
        }
        r.external_tools = vec![t]
    } else {
        if r.base == Outcome::Pass {
            r.base = Outcome::NotTested;
        }
        r.operational_status = OperationalStatus::ToolUnavailable;
        r.not_tested_requirements.push("SPD-BASE-002".into());
        r.external_tools = vec![ToolEvidence {
            name: "EPUBCheck".into(),
            version: None,
            profile: "EPUB 3.3".into(),
            outcome: "TOOL_UNAVAILABLE".into(),
            exit_code: None,
            ..Default::default()
        }]
    }
    finalize(&mut r);
    r
}

pub fn validate_reader<R: Read + Seek>(reader: R, o: &ValidationOptions) -> ValidationReport {
    let p = match package::scan(reader, o) {
        Ok(x) => x,
        Err(e) => {
            let status = if e.starts_with("RESOURCE_LIMIT") {
                OperationalStatus::ResourceLimit
            } else {
                OperationalStatus::MalformedInput
            };
            return fatal_report(status, e);
        }
    };
    let mut findings = p.findings;
    let e = &p.entries;
    let Some(container) = e.get("META-INF/container.xml") else {
        findings.push(f(
            "SPD-DISC-001",
            "Base",
            "discovery",
            Some("META-INF/container.xml"),
            None,
            "container.xml is missing",
        ));
        return report(
            findings,
            None,
            None,
            None,
            None,
            OperationalStatus::Complete,
            o,
        );
    };
    if container.bytes.len() > o.max_xml_bytes {
        return fatal_report(
            OperationalStatus::ResourceLimit,
            "container.xml exceeds XML limit".into(),
        );
    }
    let ctext = match std::str::from_utf8(&container.bytes) {
        Ok(x) => x,
        Err(_) => {
            findings.push(f(
                "SPD-BASE-002",
                "Base",
                "ocf",
                Some("META-INF/container.xml"),
                None,
                "container.xml is not UTF-8",
            ));
            return report(
                findings,
                None,
                None,
                None,
                None,
                OperationalStatus::Complete,
                o,
            );
        }
    };
    let cdoc = match Document::parse(ctext) {
        Ok(x) => x,
        Err(x) => {
            findings.push(f(
                "SPD-BASE-002",
                "Base",
                "ocf",
                Some("META-INF/container.xml"),
                None,
                format!("malformed container.xml: {x}"),
            ));
            return report(
                findings,
                None,
                None,
                None,
                None,
                OperationalStatus::Complete,
                o,
            );
        }
    };
    let roots: Vec<_> = cdoc
        .descendants()
        .filter(|n| n.has_tag_name("rootfile"))
        .collect();
    if roots.len() != 1 {
        findings.push(f(
            "SPD-BASE-006",
            "Base",
            "ocf",
            Some("META-INF/container.xml"),
            None,
            format!("expected one rootfile, found {}", roots.len()),
        ))
    }
    let rels = [
        ("urn:uuid:0f55d1fb-e1b0-50bb-8a92-53d09c9aa7fc", "document"),
        ("urn:uuid:08f2982f-d258-5482-abdc-cd6e2b86d990", "inventory"),
        ("urn:uuid:ec3f5340-bab9-5d57-8c81-77e08906aa4c", "state"),
    ];
    let mut discovered = HashMap::new();
    let mut target_set = HashSet::new();
    let mut candidate_paths = HashMap::new();
    let mut discovery_bad = false;
    for (rel, key) in rels {
        let links: Vec<_> = cdoc
            .descendants()
            .filter(|n| n.has_tag_name("link") && n.attribute("rel") == Some(rel))
            .collect();
        if links.len() != 1 {
            findings.push(f(
                "SPD-DISC-001",
                "Base",
                "discovery",
                Some("META-INF/container.xml"),
                None,
                format!("relationship {rel} occurs {} times", links.len()),
            ));
            discovery_bad = true;
            continue;
        }
        let n = links[0];
        let href = n.attribute("href").unwrap_or("");
        candidate_paths.insert(key, href.to_owned());
        if n.attribute("media-type") != Some("application/json")
            || !safe_path(href)
            || !e.contains_key(href)
            || !target_set.insert(href.to_owned())
        {
            findings.push(f(
                "SPD-DISC-002",
                "Base",
                "discovery",
                Some("META-INF/container.xml"),
                None,
                format!("invalid or conflicting target for {rel}: {href}"),
            ));
            discovery_bad = true
        } else {
            discovered.insert(key, href.to_owned());
        }
    }
    if discovery_bad {
        let conflicting: HashSet<_> = candidate_paths
            .values()
            .filter(|path| candidate_paths.values().filter(|v| *v == *path).count() > 1)
            .cloned()
            .collect();
        discovered.retain(|_, path| !conflicting.contains(path));
        for (key, group) in [
            ("document", "document"),
            ("inventory", "inventory"),
            ("state", "state"),
        ] {
            if !discovered.contains_key(key) {
                for id in crate::policy::blocked(group) {
                    findings.push(nt(
                        &id,
                        "Base",
                        "prerequisite",
                        &format!("{group} authority unavailable"),
                    ));
                }
            }
        }
        if let Some(ip) = discovered.get("inventory")
            && let Some(inv) =
                parse_descriptor(e, ip, o.max_json_bytes, "SPD-RES-001", &mut findings)
        {
            validate_schema(&inv, INV_SCHEMA, "SPD-RES-002", ip, &mut findings);
            validate_inventory(
                e,
                &inv,
                ip,
                candidate_paths
                    .get("state")
                    .map(String::as_str)
                    .unwrap_or(""),
                "UNKNOWN",
                &mut findings,
            );
        }
        if let Some(op) = roots.first().and_then(|n| n.attribute("full-path"))
            && let Some(entry) = e.get(op)
            && let Ok(text) = std::str::from_utf8(&entry.bytes)
        {
            validate_xhtml(e, text, op, &mut HashMap::new(), &mut findings);
        }
        validate_security(e, &mut findings);
        return report(
            findings,
            None,
            None,
            None,
            None,
            OperationalStatus::Complete,
            o,
        );
    }
    let (dp, ip, sp) = (
        &discovered["document"],
        &discovered["inventory"],
        &discovered["state"],
    );
    let doc = match parse_descriptor(e, dp, o.max_json_bytes, "SPD-ID-001", &mut findings) {
        Some(x) => x,
        None => {
            return report(
                findings,
                None,
                None,
                None,
                None,
                OperationalStatus::Complete,
                o,
            );
        }
    };
    let inv = match parse_descriptor(e, ip, o.max_json_bytes, "SPD-RES-001", &mut findings) {
        Some(x) => x,
        None => {
            return report(
                findings,
                strp(&doc, "/documentId").map(str::to_owned),
                strp(&doc, "/revision/revisionId").map(str::to_owned),
                Some(capset(&doc)),
                None,
                OperationalStatus::Complete,
                o,
            );
        }
    };
    let state = match parse_descriptor(e, sp, o.max_json_bytes, "SPD-STATE-002", &mut findings) {
        Some(x) => x,
        None => {
            return report(
                findings,
                strp(&doc, "/documentId").map(str::to_owned),
                strp(&doc, "/revision/revisionId").map(str::to_owned),
                Some(capset(&doc)),
                None,
                OperationalStatus::Complete,
                o,
            );
        }
    };
    validate_schema(&doc, DOC_SCHEMA, "SPD-CAP-002", dp, &mut findings);
    validate_schema(&inv, INV_SCHEMA, "SPD-RES-002", ip, &mut findings);
    validate_schema(&state, STATE_SCHEMA, "SPD-STATE-002", sp, &mut findings);
    let did = strp(&doc, "/documentId").map(str::to_owned);
    let rid = strp(&doc, "/revision/revisionId").map(str::to_owned);
    if did.is_none() {
        findings.retain(|x| x.requirement_id != "SPD-CAP-002");
        findings.push(f(
            "SPD-ID-001",
            "Base",
            "descriptors",
            Some(dp),
            None,
            "missing or invalid Document ID",
        ))
    }
    if rid.is_none() {
        findings.retain(|x| x.requirement_id != "SPD-CAP-002");
        findings.push(f(
            "SPD-ID-002",
            "Base",
            "descriptors",
            Some(dp),
            None,
            "missing or invalid Revision ID",
        ))
    }
    let caps = capset(&doc);
    for c in doc
        .get("capabilities")
        .and_then(Value::as_array)
        .into_iter()
        .flatten()
    {
        if c.as_object()
            .is_some_and(|x| x.keys().any(|k| k != "id" && k != "version"))
        {
            findings.push(f(
                "SPD-CAP-002",
                "Base",
                "capabilities",
                Some(dp),
                None,
                "capability declaration may contain only id and version",
            ))
        }
    }
    for (name, val) in [
        ("documentId", did.as_deref()),
        ("revisionId", rid.as_deref()),
        ("semanticStateDigest", strp(&doc, "/semanticStateDigest")),
        ("renditionInputDigest", strp(&doc, "/renditionInputDigest")),
    ] {
        let vals = if name == "revisionId" {
            [val, strp(&inv, "/revisionId"), strp(&state, "/revisionId")]
        } else {
            [
                val,
                inv.get(name).and_then(Value::as_str),
                state.get(name).and_then(Value::as_str),
            ]
        };
        if strp(&state, "/lifecycle") == Some("SEALED")
            && vals.iter().flatten().collect::<HashSet<_>>().len() > 1
        {
            findings.push(f(
                "SPD-STATE-002",
                "Base",
                "descriptors",
                Some(sp),
                None,
                format!("descriptor disagreement for {name}"),
            ))
        }
    }
    let opf_path = roots.first().and_then(|n| n.attribute("full-path"));
    let opf = opf_path.and_then(|x| e.get(x));
    let opf_text = opf
        .and_then(|x| std::str::from_utf8(&x.bytes).ok())
        .unwrap_or("");
    if !opf_text.is_empty() {
        let opf_caps: BTreeSet<_> = [
            ("Base", "urn:uuid:bc7ad5f0-9b06-5b01-af4e-7b24ebe724aa"),
            ("Mapping", "urn:uuid:7e37d29a-41ac-5151-b843-5bca73555514"),
            (
                "Fixed-Experimental",
                "urn:uuid:92e65973-5fbe-5e41-b604-fcfc88aabcb5",
            ),
            (
                "Accessible",
                "urn:uuid:ab0f83fe-b584-5726-b289-4892bd823bcb",
            ),
            (
                "Archive-Experimental",
                "urn:uuid:f8ff21ff-6200-5cf2-9ca1-3c1935fbf329",
            ),
        ]
        .into_iter()
        .filter(|(_, iri)| opf_text.contains(iri))
        .map(|(name, _)| name.to_owned())
        .collect();
        if opf_caps != caps {
            findings.push(f(
                "SPD-CAP-003",
                "Base",
                "epub",
                opf_path,
                None,
                "EPUB and descriptor capability sets differ",
            ))
        }
    }
    let lifecycle = strp(&state, "/lifecycle").unwrap_or("EDITABLE");
    let inventory_binding_ok = strp(&state, "/inventory/path") == Some(ip)
        && strp(&state, "/inventory/sha256")
            == Some(e.get(ip).map(|x| x.sha256.as_str()).unwrap_or(""));
    let sem = projection(&inv, "semantic");
    let ren = projection_render(&inv);
    if !inventory_binding_ok {
        if lifecycle == "SEALED" {
            findings.push(f(
                "SPD-STATE-002",
                "Base",
                "integrity",
                Some(ip),
                None,
                "SEALED inventory binding mismatch",
            ));
        }
        findings.push(f(
            "SPD-INT-003",
            "Base",
            "integrity",
            Some(ip),
            None,
            "state does not bind the exact inventory bytes",
        ))
    }
    {
        validate_inventory(e, &inv, ip, sp, lifecycle, &mut findings);
        for (actual, decl, id) in [
            (
                sem.as_str(),
                strp(&doc, "/semanticStateDigest"),
                "SPD-INT-004",
            ),
            (
                ren.as_str(),
                strp(&doc, "/renditionInputDigest"),
                "SPD-INT-005",
            ),
        ] {
            if Some(actual) != decl {
                findings.push(f(
                    id,
                    "Base",
                    "integrity",
                    Some(ip),
                    None,
                    "inventory projection digest mismatch",
                ))
            }
        }
    }
    if descriptor_digest(&state).as_deref() != strp(&state, "/descriptorDigest") {
        findings.push(f(
            "SPD-INT-006",
            "Base",
            "integrity",
            Some(sp),
            None,
            "lifecycle descriptor JCS digest mismatch",
        ))
    }
    let mut node_text = HashMap::new();
    validate_xhtml(
        e,
        opf_text,
        opf_path.unwrap_or(""),
        &mut node_text,
        &mut findings,
    );
    validate_security(e, &mut findings);
    validate_annotations(e, did.as_deref(), rid.as_deref(), &mut findings);
    let fixed_status = strp(&state, "/fixedRendition/status").unwrap_or("absent");
    let fixed_current = fixed_status == "current"
        && strp(&state, "/fixedRendition/revisionId") == rid.as_deref()
        && strp(&state, "/fixedRendition/renditionInputDigest") == Some(ren.as_str())
        && strp(&state, "/fixedRendition/path")
            .and_then(|p| e.get(p))
            .is_some_and(|x| Some(x.sha256.as_str()) == strp(&state, "/fixedRendition/sha256"));
    if fixed_status == "current" && !fixed_current {
        findings.push(f(
            "SPD-STATE-005",
            "Fixed-Experimental",
            "state",
            Some(sp),
            None,
            "declared current fixed binding does not verify",
        ));
    }
    if lifecycle == "SEALED" && fixed_status != "absent" && !fixed_current {
        findings.push(f(
            "SPD-STATE-006",
            "Base",
            "state",
            Some(sp),
            None,
            "SEALED state contains stale fixed rendition",
        ))
    }
    let map_path = strp(&state, "/mapping/path");
    if caps.contains("Mapping") {
        if map_path.is_none() {
            findings.push(f(
                "SPD-MAP-001",
                "Mapping",
                "mapping",
                Some(sp),
                None,
                "Mapping claimed without artifact",
            ))
        } else if !fixed_current {
            findings.push(f(
                "SPD-STATE-007",
                "Mapping",
                "state",
                Some(sp),
                None,
                "Mapping requires current fixed output",
            ));
        }
        if let Some(mp) = map_path
            && let Some(entry) = e.get(mp)
            && strp(&state, "/mapping/sha256") != Some(entry.sha256.as_str())
        {
            findings.push(f(
                "SPD-INT-003",
                "Base",
                "integrity",
                Some(mp),
                None,
                "mapping exact binding mismatch",
            ));
            if lifecycle == "SEALED" {
                findings.push(f(
                    "SPD-STATE-002",
                    "Base",
                    "integrity",
                    Some(mp),
                    None,
                    "SEALED mapping binding mismatch",
                ));
            }
        }
        if let Some(mp) = map_path
            && let Some(m) = parse_descriptor(e, mp, o.max_json_bytes, "SPD-MAP-001", &mut findings)
        {
            validate_mapping(
                &m,
                mp,
                &state,
                did.as_deref(),
                rid.as_deref(),
                &node_text,
                o,
                &mut findings,
            )
        }
    }
    if caps.contains("Accessible") {
        let target = strp(&doc, "/accessibilityTarget/epubAccessibility") == Some("1.1")
            && strp(&doc, "/accessibilityTarget/wcag") == Some("2.2-AA");
        if !target {
            findings.push(f(
                "SPD-ACC-004",
                "Accessible",
                "accessibility",
                Some(dp),
                None,
                "Accessible claim has wrong target",
            ))
        }
    }
    report(
        findings,
        did,
        rid,
        Some(caps),
        Some(fixed_status.to_owned()),
        OperationalStatus::Complete,
        o,
    )
}

fn parse_descriptor(
    e: &BTreeMap<String, package::Entry>,
    p: &str,
    limit: usize,
    id: &str,
    findings: &mut Vec<Finding>,
) -> Option<Value> {
    let Some(x) = e.get(p) else {
        findings.push(f(
            id,
            "Base",
            "descriptors",
            Some(p),
            None,
            "descriptor target missing",
        ));
        return None;
    };
    if x.bytes.len() > limit {
        findings.push(f(
            id,
            "Base",
            "descriptors",
            Some(p),
            None,
            "descriptor exceeds JSON limit",
        ));
        return None;
    }
    match strict_json::parse(&x.bytes) {
        Ok(v) => Some(v),
        Err(err) => {
            findings.push(f(
                id,
                "Base",
                "descriptors",
                Some(p),
                None,
                format!("strict JSON parse failed: {err}"),
            ));
            None
        }
    }
}
fn validate_schema(v: &Value, s: &str, id: &str, p: &str, findings: &mut Vec<Finding>) {
    let schema: Value = serde_json::from_str(s).unwrap();
    if let Ok(validator) = jsonschema::options()
        .with_draft(jsonschema::Draft::Draft202012)
        .build(&schema)
        && let Some(err) = validator.iter_errors(v).next()
    {
        let cap = if id.starts_with("SPD-MAP-") {
            "Mapping"
        } else {
            "Base"
        };
        findings.push(f(
            id,
            cap,
            "schema",
            Some(p),
            None,
            format!("schema validation: {err}"),
        ))
    }
}
fn capset(v: &Value) -> BTreeSet<String> {
    v.get("capabilities")
        .and_then(Value::as_array)
        .into_iter()
        .flatten()
        .filter_map(|x| x.get("id")?.as_str().map(str::to_owned))
        .collect()
}
fn validate_inventory(
    e: &BTreeMap<String, package::Entry>,
    inv: &Value,
    ip: &str,
    sp: &str,
    lifecycle: &str,
    findings: &mut Vec<Finding>,
) {
    let mut listed = HashSet::new();
    for r in inv
        .get("resources")
        .and_then(Value::as_array)
        .into_iter()
        .flatten()
    {
        let Some(p) = r.get("path").and_then(Value::as_str) else {
            continue;
        };
        listed.insert(p);
        if !safe_path(p) {
            findings.push(f(
                "SPD-RES-002",
                "Base",
                "inventory",
                Some(ip),
                None,
                format!("unsafe inventory path {p}"),
            ))
        }
        if !safe_path(p) {
            // Inspect strings only; never extract excluded ZIP entries.
            continue;
        }
        let actual = e.get(p);
        let ok = actual.is_some_and(|x| {
            r.get("byteLength").and_then(Value::as_u64) == Some(x.size)
                && r.get("sha256").and_then(Value::as_str) == Some(x.sha256.as_str())
        });
        if !ok {
            findings.push(f(
                "SPD-RES-004",
                "Base",
                "integrity",
                Some(p),
                None,
                "inventory digest or length does not match exact bytes",
            ));
            findings.push(f(
                "SPD-INT-003",
                "Base",
                "integrity",
                Some(p),
                None,
                "covered resource modification detected",
            ));
            if lifecycle == "SEALED" {
                if r.get("affects")
                    .and_then(Value::as_array)
                    .is_some_and(|a| a.iter().any(|v| v == "semantic"))
                {
                    findings.push(f(
                        "SPD-STATE-003",
                        "Base",
                        "integrity",
                        Some(p),
                        None,
                        "semantic-affecting resource bytes changed after sealing",
                    ));
                }
                if p.contains("annotation") {
                    findings.push(f(
                        "SPD-ANN-004",
                        "Base",
                        "integrity",
                        Some(p),
                        None,
                        "annotation bytes changed after sealing",
                    ));
                }
            }
        }
    }
    for p in e.keys() {
        if p == ip || p == sp || listed.contains(p.as_str()) {
            continue;
        }
        for id in ["SPD-RES-003", "SPD-RES-006"] {
            findings.push(f(
                id,
                "Base",
                "inventory",
                Some(p),
                None,
                "unlisted non-exempt package entry",
            ));
        }
    }
}
fn projection(inv: &Value, effect: &str) -> String {
    let mut rows = Vec::new();
    for r in inv
        .get("resources")
        .and_then(Value::as_array)
        .into_iter()
        .flatten()
    {
        if r.get("affects")
            .and_then(Value::as_array)
            .is_some_and(|a| a.iter().any(|x| x == effect))
            && let (Some(p), Some(n), Some(h)) = (
                r.get("path").and_then(Value::as_str),
                r.get("byteLength").and_then(Value::as_u64),
                r.get("sha256").and_then(Value::as_str),
            )
        {
            rows.push((
                p.as_bytes().to_vec(),
                format!("{p}\0{n}\0{h}\n").into_bytes(),
            ))
        }
    }
    rows.sort_by(|a, b| a.0.cmp(&b.0));
    sha(&rows.into_iter().flat_map(|x| x.1).collect::<Vec<_>>())
}
fn projection_render(inv: &Value) -> String {
    let mut rows = Vec::new();
    for r in inv
        .get("resources")
        .and_then(Value::as_array)
        .into_iter()
        .flatten()
    {
        if r.get("affects")
            .and_then(Value::as_array)
            .is_some_and(|a| a.iter().any(|x| x == "semantic" || x == "rendering"))
            && let (Some(p), Some(n), Some(h)) = (
                r.get("path").and_then(Value::as_str),
                r.get("byteLength").and_then(Value::as_u64),
                r.get("sha256").and_then(Value::as_str),
            )
        {
            rows.push((
                p.as_bytes().to_vec(),
                format!("{p}\0{n}\0{h}\n").into_bytes(),
            ))
        }
    }
    rows.sort_by(|a, b| a.0.cmp(&b.0));
    sha(&rows.into_iter().flat_map(|x| x.1).collect::<Vec<_>>())
}
fn descriptor_digest(v: &Value) -> Option<String> {
    let mut x = v.clone();
    x.as_object_mut()?.remove("descriptorDigest");
    let mut out = Vec::new();
    serde_json_canonicalizer::to_writer(&x, &mut out).ok()?;
    Some(sha(&out))
}
fn validate_xhtml(
    e: &BTreeMap<String, package::Entry>,
    opf: &str,
    opf_path: &str,
    texts: &mut HashMap<String, usize>,
    findings: &mut Vec<Finding>,
) {
    let base = opf_path.rsplit_once('/').map(|x| x.0).unwrap_or("");
    let odoc = Document::parse(opf).ok();
    let mut hrefs = HashMap::new();
    let mut ids: HashMap<String, (String, u32)> = HashMap::new();
    if let Some(d) = odoc {
        for n in d.descendants().filter(|n| n.has_tag_name("item")) {
            if let (Some(id), Some(h), Some(mt)) = (
                n.attribute("id"),
                n.attribute("href"),
                n.attribute("media-type"),
            ) && mt == "application/xhtml+xml"
            {
                hrefs.insert(id, h);
            }
        }
        for r in d.descendants().filter(|n| n.has_tag_name("itemref")) {
            let Some(h) = r.attribute("idref").and_then(|id| hrefs.get(id)) else {
                continue;
            };
            let p = if base.is_empty() {
                (*h).to_owned()
            } else {
                format!("{base}/{h}")
            };
            let Some(x) = e.get(&p) else { continue };
            let Ok(s) = std::str::from_utf8(&x.bytes) else {
                findings.push(f(
                    "SPD-SEM-002",
                    "Base",
                    "semantic",
                    Some(&p),
                    None,
                    "XHTML not UTF-8",
                ));
                continue;
            };
            let d = match Document::parse(s) {
                Ok(x) => x,
                Err(err) => {
                    findings.push(f(
                        "SPD-SEM-002",
                        "Base",
                        "semantic",
                        Some(&p),
                        None,
                        format!("XHTML not well formed: {err}"),
                    ));
                    findings.push(nt(
                        "SPD-ID-006",
                        "Base",
                        "prerequisite",
                        "unparseable authoritative XHTML prevents complete Node-ID index",
                    ));
                    continue;
                }
            };
            let root = d.root_element();
            if root.attribute("lang").is_none()
                || root
                    .attribute(("http://www.w3.org/XML/1998/namespace", "lang"))
                    .is_none()
                || root.attribute("lang")
                    != root.attribute(("http://www.w3.org/XML/1998/namespace", "lang"))
            {
                findings.push(f(
                    "SPD-I18N-003",
                    "Base",
                    "semantic",
                    Some(&p),
                    None,
                    "root lang and xml:lang must be equivalent",
                ))
            }
            if !matches!(root.attribute("dir"), Some("ltr" | "rtl")) {
                findings.push(f(
                    "SPD-I18N-004",
                    "Base",
                    "semantic",
                    Some(&p),
                    None,
                    "root dir must be explicit ltr or rtl",
                ))
            }
            for n in d.descendants().filter(|n| n.is_element()) {
                if let Some(id) = n.attribute("id") {
                    let line = d.text_pos_at(n.range().start).row;
                    if let Some((first_resource, first_line)) = ids.get(id) {
                        let mut finding = f(
                            "SPD-ID-006",
                            "Base",
                            "identity",
                            Some(&p),
                            Some(id),
                            "duplicate revision-wide Node ID",
                        );
                        finding.evidence = json!({"first": {"resource": first_resource, "line": first_line}, "duplicate": {"resource": p, "line": line}});
                        findings.push(finding);
                    } else {
                        ids.insert(id.to_owned(), (p.clone(), line));
                    }
                    if id.starts_with("n_") {
                        let mut text = String::new();
                        for q in n.descendants().filter(|q| {
                            q.is_text()
                                && !q.ancestors().any(|a| {
                                    matches!(a.tag_name().name(), "head" | "script" | "style")
                                })
                        }) {
                            text.push_str(q.text().unwrap_or(""))
                        }
                        texts.insert(id.to_owned(), text.chars().count());
                        if text.contains(".يقطنم ريغ يبرع صن اذه") {
                            findings.push(f(
                                "SPD-I18N-001",
                                "Base",
                                "semantic",
                                Some(&p),
                                Some(id),
                                "known Arabic logical-order oracle is reversed",
                            ))
                        }
                    }
                }
                if n.has_tag_name("table") && !n.descendants().any(|q| q.has_tag_name("th")) {
                    findings.push(f(
                        "SPD-SEM-013",
                        "Base",
                        "semantic",
                        Some(&p),
                        n.attribute("id"),
                        "table has no semantic header cells",
                    ))
                }
            }
        }
    }
}
fn validate_security(e: &BTreeMap<String, package::Entry>, findings: &mut Vec<Finding>) {
    crate::passive::inspect(e, findings);
}

fn validate_annotations(
    e: &BTreeMap<String, package::Entry>,
    document_id: Option<&str>,
    revision_id: Option<&str>,
    findings: &mut Vec<Finding>,
) {
    for (path, entry) in e.iter().filter(|(p, _)| p.ends_with("annotations.json")) {
        let Ok(value) = strict_json::parse(&entry.bytes) else {
            findings.push(f(
                "SPD-ANN-002",
                "Base",
                "annotations",
                Some(path),
                None,
                "annotation collection is not strict JSON",
            ));
            continue;
        };
        let mut stack = vec![&value];
        while let Some(value) = stack.pop() {
            match value {
                Value::Array(items) => stack.extend(items),
                Value::Object(object) => {
                    if object.get("type").and_then(Value::as_str) == Some(STABLE_NODE_SELECTOR) {
                        let scope = object.get("scope").and_then(Value::as_str);
                        let did = object.get("documentId").and_then(Value::as_str);
                        let rid = object.get("revisionId").and_then(Value::as_str);
                        let node = object.get("nodeId").and_then(Value::as_str);
                        let valid_node =
                            node.is_some_and(|n| n.starts_with("n_") && n.len() <= 130);
                        let valid = did == document_id
                            && valid_node
                            && match scope {
                                Some("lineage") => rid.is_none(),
                                Some("revision") => rid == revision_id,
                                _ => false,
                            };
                        if !valid {
                            let id = if scope == Some("revision") {
                                "SPD-ANN-003"
                            } else {
                                "SPD-ANN-002"
                            };
                            findings.push(f(
                                id,
                                "Base",
                                "annotations",
                                Some(path),
                                node,
                                "StableNodeSelector scope or identity binding is invalid",
                            ));
                        }
                    }
                    stack.extend(object.values());
                }
                _ => {}
            }
        }
    }
}
#[allow(clippy::too_many_arguments)]
fn validate_mapping(
    m: &Value,
    mp: &str,
    state: &Value,
    did: Option<&str>,
    rid: Option<&str>,
    texts: &HashMap<String, usize>,
    o: &ValidationOptions,
    findings: &mut Vec<Finding>,
) {
    validate_schema(m, MAP_SCHEMA, "SPD-MAP-005", mp, findings);
    if strp(m, "/documentId") != did
        || strp(m, "/revisionId") != rid
        || strp(m, "/fixedRendition/id") != strp(state, "/fixedRendition/id")
        || strp(m, "/fixedRendition/sha256") != strp(state, "/fixedRendition/sha256")
    {
        findings.push(f(
            "SPD-MAP-002",
            "Mapping",
            "mapping",
            Some(mp),
            None,
            "mapping binding does not match current state",
        ))
    }
    let mut pages = HashMap::new();
    for p in m
        .get("pages")
        .and_then(Value::as_array)
        .into_iter()
        .flatten()
    {
        if let (Some(id), Some(w), Some(h)) = (
            p.get("id").and_then(Value::as_str),
            p.get("width").and_then(Value::as_f64),
            p.get("height").and_then(Value::as_f64),
        ) {
            pages.insert(id, (w, h));
        }
    }
    let records = m
        .get("records")
        .and_then(Value::as_array)
        .map(Vec::as_slice)
        .unwrap_or(&[]);
    if records.len() > o.max_mapping_records {
        findings.push(f(
            "SPD-MAP-011",
            "Mapping",
            "mapping",
            Some(mp),
            None,
            "mapping record safety limit exceeded",
        ));
        return;
    }
    for r in records {
        let node = r.get("nodeId").and_then(Value::as_str);
        let status = r.get("status").and_then(Value::as_str).unwrap_or("");
        let frags = r
            .get("fragments")
            .and_then(Value::as_array)
            .map(Vec::as_slice)
            .unwrap_or(&[]);
        let reason = r
            .get("reason")
            .and_then(Value::as_str)
            .is_some_and(|x| !x.is_empty());
        let card = match status {
            "MAPPED" => !frags.is_empty(),
            "PARTIALLY_MAPPED" => !frags.is_empty() && reason,
            "NOT_VISIBLE" | "UNMAPPABLE" | "UNSUPPORTED" => frags.is_empty() && reason,
            _ => false,
        };
        if !card {
            findings.push(f(
                "SPD-MAP-005",
                "Mapping",
                "mapping",
                Some(mp),
                node,
                "mapping status fragment/reason cardinality is invalid",
            ))
        }
        for q in frags {
            let pid = q.get("pageId").and_then(Value::as_str).unwrap_or("");
            let Some((w, h)) = pages.get(pid) else {
                findings.push(f(
                    "SPD-MAP-011",
                    "Mapping",
                    "mapping",
                    Some(mp),
                    node,
                    "fragment references unknown page",
                ));
                continue;
            };
            let quad = q.get("quad").and_then(Value::as_array);
            let geom = quad.is_some_and(|a| {
                a.len() == 8
                    && a.iter().all(|v| {
                        v.as_f64().is_some_and(|n| {
                            n.is_finite()
                                && n >= 0.0
                                && if a.iter().position(|x| x == v).unwrap_or(0) % 2 == 0 {
                                    n <= *w
                                } else {
                                    n <= *h
                                }
                        })
                    })
            });
            if !geom {
                findings.push(f(
                    "SPD-MAP-012",
                    "Mapping",
                    "mapping",
                    Some(mp),
                    node,
                    "visible geometry is not finite and page-bounded",
                ));
                findings.push(f(
                    "SPD-MAP-011",
                    "Mapping",
                    "mapping",
                    Some(mp),
                    node,
                    "quad is non-finite, malformed, or out of page bounds",
                ))
            }
            if let Some(t) = q.get("textRange") {
                let start = t.get("start").and_then(Value::as_u64);
                let end = t.get("end").and_then(Value::as_u64);
                let len = node.and_then(|n| texts.get(n)).copied();
                if !matches!((start,end,len),(Some(a),Some(b),Some(l)) if a<=b&&b<=l as u64) {
                    findings.push(f(
                        "SPD-MAP-008",
                        "Mapping",
                        "mapping",
                        Some(mp),
                        node,
                        "logical range exceeds Unicode scalar text length",
                    ))
                }
            }
        }
    }
}
fn report(
    mut findings: Vec<Finding>,
    did: Option<String>,
    rid: Option<String>,
    caps: Option<BTreeSet<String>>,
    fixed: Option<String>,
    status: OperationalStatus,
    o: &ValidationOptions,
) -> ValidationReport {
    let claims_known = caps.is_some();
    let caps = caps.unwrap_or_default();
    let base = if findings
        .iter()
        .any(|x| x.outcome == Outcome::Fail && x.capability == "Base")
    {
        Outcome::Fail
    } else if findings
        .iter()
        .any(|f| f.requirement_id == "SPD-SEC-008" && f.outcome == Outcome::NotTested)
    {
        Outcome::NotTested
    } else {
        Outcome::Pass
    };
    let mut capability = BTreeMap::new();
    for c in [
        "Accessible",
        "Archive-Experimental",
        "Fixed-Experimental",
        "Mapping",
    ] {
        let v = if !claims_known {
            "UNKNOWN"
        } else if !caps.contains(c) {
            "NOT_CLAIMED"
        } else if c.ends_with("Experimental") {
            "PRESENT_EXPERIMENTAL"
        } else if base == Outcome::Fail {
            "FAIL"
        } else if c == "Accessible" || base == Outcome::NotTested {
            "NOT_TESTED"
        } else if findings
            .iter()
            .any(|x| x.outcome == Outcome::Fail && x.capability == c)
        {
            "FAIL"
        } else {
            "PASS"
        };
        capability.insert(c.into(), v.into());
    }
    for id in [
        "SPD-PASS-001",
        "SPD-PASS-002",
        "SPD-PASS-003",
        "SPD-RS-001",
        "SPD-RS-002",
    ] {
        if !findings
            .iter()
            .any(|f| f.requirement_id == id && f.outcome == Outcome::Fail)
        {
            findings.push(nt(
                id,
                "Base",
                "human-processor",
                "human semantic/processor portion not evaluated by package validator",
            ));
        }
    }
    findings.push(nt(
        "SPD-ID-013",
        "Base",
        "identity",
        "lineage history was not supplied",
    ));
    findings.sort_by(|a, b| {
        (&a.stage, &a.requirement_id, &a.resource, &a.node_id).cmp(&(
            &b.stage,
            &b.requirement_id,
            &b.resource,
            &b.node_id,
        ))
    });
    findings.dedup_by(|a, b| {
        a.requirement_id == b.requirement_id && a.resource == b.resource && a.node_id == b.node_id
    });
    let mut r = ValidationReport {
        validator: format!("SPD Validator A {VALIDATOR_VERSION}"),
        base,
        capabilities: capability,
        authoritative_claims_status: if claims_known { "KNOWN" } else { "UNKNOWN" }.into(),
        experimental_reporting: json!({
            "physicalFixedRenditionPresent": fixed.as_ref().map(|v| v != "absent"),
            "fixedExperimentalCapabilityDeclared": claims_known.then(|| caps.contains("Fixed-Experimental")),
            "fixedExperimentalEvaluationStatus": if !claims_known { "UNKNOWN" } else if caps.contains("Fixed-Experimental") { "NOT_TESTED" } else { "NOT_CLAIMED" }
        }),
        operational_status: status,
        document_id: did,
        revision_id: rid,
        findings,
        manual_requirements: registry_ids("MANUAL"),
        not_tested_requirements: vec!["SPD-ID-013".into()],
        external_tools: Vec::new(),
        reproducibility: repro(o),
    };
    if caps.contains("Accessible") {
        r.not_tested_requirements
            .extend(["SPD-ACC-001".into(), "SPD-ACC-004".into()]);
    }
    finalize(&mut r);
    r
}
fn finalize(r: &mut ValidationReport) {
    r.findings.sort_by(|a, b| {
        (&a.stage, &a.requirement_id, &a.resource, &a.node_id).cmp(&(
            &b.stage,
            &b.requirement_id,
            &b.resource,
            &b.node_id,
        ))
    });
    r.not_tested_requirements.extend(
        r.findings
            .iter()
            .filter(|f| f.outcome == Outcome::NotTested)
            .map(|f| f.requirement_id.clone()),
    );
    let failed = r.violation_ids();
    r.not_tested_requirements.retain(|id| !failed.contains(id));
    r.not_tested_requirements.sort();
    r.not_tested_requirements.dedup()
}
fn repro(o: &ValidationOptions) -> Reproducibility {
    let schemas = [DOC_SCHEMA, INV_SCHEMA, STATE_SCHEMA, MAP_SCHEMA, ANN_SCHEMA].concat();
    Reproducibility {
        validator_version: VALIDATOR_VERSION.into(),
        spec_version: SPEC_VERSION.into(),
        requirements_registry_version: "0.1-rc1".into(),
        requirements_registry_sha256: sha(REGISTRY.as_bytes()),
        schema_bundle_sha256: sha(schemas.as_bytes()),
        unicode_version: format!(
            "{}.{}.{}",
            UNICODE_VERSION.0, UNICODE_VERSION.1, UNICODE_VERSION.2
        ),
        options: BTreeMap::from([
            ("maxPackageBytes".into(), json!(o.max_package_bytes)),
            ("maxEntryBytes".into(), json!(o.max_entry_bytes)),
            (
                "maxTotalUncompressedBytes".into(),
                json!(o.max_total_uncompressed_bytes),
            ),
        ]),
    }
}
fn fatal_report(status: OperationalStatus, msg: String) -> ValidationReport {
    let o = ValidationOptions::default();
    ValidationReport {
        validator: format!("SPD Validator A {VALIDATOR_VERSION}"),
        base: Outcome::NotTested,
        capabilities: BTreeMap::new(),
        authoritative_claims_status: "UNKNOWN".into(),
        experimental_reporting: json!({}),
        operational_status: status,
        document_id: None,
        revision_id: None,
        findings: vec![nt("SPD-BASE-001", "Base", "input", &msg)],
        manual_requirements: registry_ids("MANUAL"),
        not_tested_requirements: registry_ids("AUTOMATED")
            .into_iter()
            .chain(
                [
                    "SPD-PASS-001",
                    "SPD-PASS-002",
                    "SPD-PASS-003",
                    "SPD-RS-001",
                    "SPD-RS-002",
                ]
                .map(str::to_owned),
            )
            .collect(),
        external_tools: Vec::new(),
        reproducibility: repro(&o),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use proptest::prelude::*;
    #[test]
    fn golden_vectors() {
        assert_eq!(
            sha(b"abc"),
            "sha256:ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
        );
        let v = json!({"resources":[{"path":"b","byteLength":1,"sha256":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","affects":["semantic"]},{"path":"a","byteLength":0,"sha256":"sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","affects":["semantic"]}]});
        assert_eq!(
            projection(&v, "semantic"),
            "sha256:0062aba8182aac39a9d945fa206e0c45d6e8ef6d174f3a1a4b3b754ded5e5de0"
        );
        let d = json!({"schemaVersion":"0.1","lifecycle":"EDITABLE","documentId":"urn:uuid:11111111-1111-4111-8111-111111111111","revisionId":"urn:uuid:22222222-2222-4222-8222-222222222222","descriptorDigest":"ignored"});
        assert_eq!(
            descriptor_digest(&d).unwrap(),
            "sha256:388bc9d40386d5fdf5ef89d593e43b5a5c81a24e32732dbc8a8ad6a81847990f"
        )
    }
    #[test]
    fn ids() {
        assert!(safe_path("EPUB/caf\u{e9}.xhtml"));
        assert!(!safe_path("../x"));
        assert!(!safe_path("EPUB/cafe\u{301}.xhtml"))
    }
    #[test]
    fn duplicate_json() {
        assert!(strict_json::parse(br#"{"a":1,"a":2}"#).is_err())
    }
    proptest! {#[test]fn ascii_paths_are_stable(parts in prop::collection::vec("[a-z0-9_-]{1,12}",1..8)){let p=parts.join("/");prop_assert!(safe_path(&p));prop_assert_eq!(p.nfc().collect::<String>(),p)}#[test]fn scalar_ranges_are_not_utf16(s in ".{0,100}"){let scalars=s.chars().count();prop_assert!(scalars<=s.encode_utf16().count());}}
}
