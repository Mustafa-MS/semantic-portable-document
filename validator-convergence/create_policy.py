"""Build the shared, validator-neutral attribution artifact from reviewed predicates."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    stage = json.loads((ROOT / 'validator-differential/raw-diff.json').read_text(encoding='utf-8'))
    ids = sorted({r for x in stage['fixtures'] if not x['completeSurfaceAgreement'] for r in x['B']['violationRequirementIds']})
    definitions = {}
    for line in (ROOT / 'spec/requirements.yaml').read_text(encoding='utf-8').splitlines():
        m = re.search(r'id: (SPD-[A-Z]+-\d+).*?requirement: "([^"]+)"', line)
        if m:
            definitions[m[1]] = m[2]
    groups = {
        'document': ['SPD-CAP-002', 'SPD-CAP-003', 'SPD-ID-002', 'SPD-INT-004', 'SPD-INT-005'],
        'inventory': ['SPD-RES-001', 'SPD-RES-002', 'SPD-RES-003', 'SPD-RES-004', 'SPD-RES-005', 'SPD-RES-006', 'SPD-INT-003', 'SPD-INT-004', 'SPD-INT-005'],
        'state': ['SPD-INT-006', 'SPD-STATE-002', 'SPD-STATE-003', 'SPD-STATE-006', 'SPD-STATE-007'],
        'semanticIndex': ['SPD-ID-006'],
    }
    rules = []
    for rid in sorted(set(ids) | {r for g in groups.values() for r in g}):
        applicability = 'current document; conditional on the registry capability and required evidence'
        if rid == 'SPD-STATE-001': applicability = 'processor execution evidence only; NOT_APPLICABLE in document-only profile'
        if rid in {'SPD-STATE-002', 'SPD-STATE-003', 'SPD-STATE-006'}: applicability = 'SEALED lifecycle only'
        if rid.startswith('SPD-MAP-') or rid == 'SPD-STATE-007': applicability = 'known explicit Mapping claim'
        prereq = [key for key, value in groups.items() if rid in value]
        overlap = 'Retain every independently established applicable predicate; no primary-error suppression.'
        if rid in {'SPD-RES-003', 'SPD-RES-006'}: overlap = 'Emit both for unlisted non-exempt resources, including caches; no filename/role division.'
        if rid in {'SPD-MAP-011', 'SPD-MAP-012'}: overlap = 'Emit both for readable visible quad outside declared page bounds.'
        rules.append({'requirementId': rid, 'applicability': applicability, 'requiredEvidence': definitions[rid],
                      'prerequisites': prereq, 'predicate': definitions[rid], 'overlapBehavior': overlap,
                      'externalToolAttribution': 'Only guarded entries in externalDiagnostics; otherwise native evidence required.'})
    external = [
        {'code': 'OPF-060', 'pattern': 'Duplicate entry in the ZIP file', 'ids': ['SPD-BASE-002'], 'category': 'OCF'},
        {'code': 'RSC-016', 'pattern': '(?i)(parsing|well.formed|XML)', 'ids': ['SPD-SEM-002'], 'category': 'XHTML/XML'},
        {'code': 'RSC-005', 'pattern': 'Duplicate ID', 'ids': ['SPD-ID-006'], 'category': 'content identity'},
        {'code': 'RSC-005', 'pattern': '(?i)(element .*not allowed|missing required element|bad XML)', 'ids': ['SPD-SEM-002'], 'category': 'XHTML/XML'},
        {'code': 'RSC-006', 'pattern': '(?i)https?://[^ ]+\\.css', 'ids': ['SPD-SEC-005'], 'category': 'offline CSS'},
        {'code': 'RSC-006', 'pattern': '(?i)https?://[^ ]+\\.(png|jpg|jpeg|gif|svg)', 'ids': ['SPD-SEC-006'], 'category': 'offline image'},
        {'code': 'RSC-008', 'pattern': '(?i)https?://[^ ]+\\.(woff2?|ttf|otf)', 'ids': ['SPD-SEC-004'], 'category': 'offline font'},
    ]
    payload = {'version': '0.1.1', 'kind': 'NON-NORMATIVE VALIDATION INFRASTRUCTURE', 'noFormatSemanticsChanged': True,
               'blocked': groups, 'rules': rules, 'externalDiagnostics': external,
               'externalDefault': 'Retain raw evidence; no automatic SPD failure attribution.',
               'experimental': ['physicalFixedRenditionPresent', 'fixedExperimentalCapabilityDeclared', 'fixedExperimentalEvaluationStatus']}
    (ROOT / 'validation/REQUIREMENT_ATTRIBUTION_0.1.1.json').write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
    print('Created policy for', len(rules), 'requirements and', len(external), 'external guards.')


if __name__ == '__main__': main()
