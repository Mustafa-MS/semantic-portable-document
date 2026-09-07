"""Versioned integration and pin refresh; historical evidence is never edited."""
import hashlib
import json
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def edit(name, fn):
    p = ROOT / name
    p.write_text(fn(p.read_text(encoding='utf-8')), encoding='utf-8')

def main():
    p = ROOT / 'validation/REQUIREMENT_ATTRIBUTION_0.1.2.json'
    data = json.loads((ROOT / 'validation/REQUIREMENT_ATTRIBUTION_0.1.1.json').read_text())
    data['version'] = '0.1.2'
    data['wholePublicationUmbrella'] = 'Every completed ERROR/FATAL EPUBCheck conformance result adds SPD-BASE-002; warnings and operational tool failures do not.'
    data['partialAndProcessorRequirements'] = ['SPD-PASS-001', 'SPD-PASS-002', 'SPD-PASS-003', 'SPD-RS-001', 'SPD-RS-002']
    data['packageRollupPolicy'] = 'These five human/processor portions remain NOT_TESTED; their syntactic FAIL findings fail Base. Package PASS is not reader or semantic-completeness certification.'
    p.write_text(json.dumps(data, indent=2) + '\n')
    for name in ['validator-a/src/policy.rs', 'validator-b/spd_validator_b/policy.py', 'validator-b/pyproject.toml']:
        edit(name, lambda s: s.replace('REQUIREMENT_ATTRIBUTION_0.1.1', 'REQUIREMENT_ATTRIBUTION_0.1.2'))
    edit('validator-a/Cargo.toml', lambda s: s.replace('0.1.0-draft.2', '0.1.0-draft.3'))
    edit('validator-a/src/lib.rs', lambda s: s.replace('mod package;', 'mod package;\nmod passive;'))
    edit('validator-a/src/validator.rs', lambda s: s[:s.index('fn validate_security(')] + 'fn validate_security(e: &BTreeMap<String, package::Entry>, findings: &mut Vec<Finding>) {\n    crate::passive::inspect(e, findings);\n}\n\n' + s[s.index('fn validate_annotations('):])
    edit('validator-a/src/policy.rs', lambda s: s.replace('if let Some(found) = diagnostic.captures(line) {', 'if let Some(found) = diagnostic.captures(line) {\n            result.insert("SPD-BASE-002".to_owned());'))
    edit('validator-b/spd_validator_b/policy.py', lambda s: s.replace('if diagnostic:', "if diagnostic:\n            found.add('SPD-BASE-002')"))
    edit('validator-a/src/epubcheck.rs', lambda s: s.replace('json!("0.1.1")', 'json!("0.1.2")').replace('} else if code < 0 {', '} else if code < 0 || !crate::policy::attribute(&output).contains(&"SPD-BASE-002".into()) {'))
    edit('validator-a/src/validator.rs', lambda s: s.replace('findings.push(nt(\n        "SPD-ID-013",', '''for id in ["SPD-PASS-001", "SPD-PASS-002", "SPD-PASS-003", "SPD-RS-001", "SPD-RS-002"] {
        if !findings.iter().any(|f| f.requirement_id == id && f.outcome == Outcome::Fail) {
            findings.push(nt(id, "Base", "human-processor", "human semantic/processor portion not evaluated by package validator"));
        }
    }
    findings.push(nt(
        "SPD-ID-013",'''))
    # Remove B's incomplete security branch, retain semantic/identity logic intact.
    edit('validator-b/spd_validator_b/semantics.py', lambda s: s[:s.index('            if name == "script":')] + s[s.index('            if name == "table":'):s.index('    for item in opf.manifest.values():')] + '    return model\n')
    edit('validator-b/spd_validator_b/validator.py', lambda s: s.replace('from .semantics import', 'from .passive import validate_passive\nfrom .semantics import').replace('"SPD-ID-013", "SPD-ACC-001", "SPD-ACC-004"', '"SPD-ID-013", "SPD-ACC-001", "SPD-ACC-004", "SPD-PASS-001", "SPD-PASS-002", "SPD-PASS-003", "SPD-RS-001", "SPD-RS-002"').replace('        discovery = discover(package, report)', '        validate_passive(package, report)\n        discovery = discover(package, report)').replace('    _roll_up(report, registry, claimed, adapter.command is not None)', '''    for rid in ('SPD-PASS-001', 'SPD-PASS-002', 'SPD-PASS-003', 'SPD-RS-001', 'SPD-RS-002'):
        if rid not in report.violation_requirement_ids:
            report.add(rid, Outcome.NOT_TESTED, 'human semantic/processor portion not evaluated by package validator')
    _roll_up(report, registry, claimed, adapter.command is not None)''').replace('"validatorBVersion": "0.1.1"', '"validatorBVersion": "0.1.2"').replace('"differentialContract": "0.1.1"', '"differentialContract": "0.1.2"'))
    for name in ['validator-b/pyproject.toml', 'validator-b/spd_validator_b/__init__.py']:
        edit(name, lambda s: s.replace('"0.1.1"', '"0.1.2"'))
    edit('validator-b/spd_validator_b/epubcheck.py', lambda s: s.replace('"attributionVersion": "0.1.1"', '"attributionVersion": "0.1.2"').replace('report.operational_status = OperationalStatus.RESOURCE_LIMIT', 'report.operational_status = OperationalStatus.TOOL_UNAVAILABLE').replace('        for requirement in attributed:', '''        if completed.returncode != 0 and 'SPD-BASE-002' not in attributed:
            report.operational_status = OperationalStatus.TOOL_UNAVAILABLE
            report.metadata['epubcheck']['result'] = 'ERROR'
            report.add('SPD-BASE-002', Outcome.NOT_TESTED, 'tool did not establish a completed conformance result')
        for requirement in attributed:'''))
    hashes = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in ['spec/FORMAT_0.1_DRAFT.md', 'spec/requirements.yaml']}
    edit('validator-b/spd_validator_b/constants.py', lambda s: re.sub(r'FORMAT_DRAFT_SHA256 = "[^"]+"', 'FORMAT_DRAFT_SHA256 = "' + hashes['spec/FORMAT_0.1_DRAFT.md'] + '"', re.sub(r'REQUIREMENTS_SHA256 = "[^"]+"', 'REQUIREMENTS_SHA256 = "' + hashes['spec/requirements.yaml'] + '"', s)))
    print(hashes)

if __name__ == '__main__': main()
