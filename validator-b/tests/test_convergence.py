import json
from pathlib import Path

import pytest

from spd_validator_b.descriptors import Descriptors
from spd_validator_b.policy import external_ids, policy
from spd_validator_b.validator import _claims, validate

ROOT = Path(__file__).resolve().parents[2]


def run(name): return validate(ROOT / 'tests/corpus-0.1-rc1' / name / 'document.epub')


def test_revision_wide_positive_and_negative():
    assert 'SPD-ID-006' not in run('valid/multi-spine').violation_requirement_ids
    assert 'SPD-ID-006' in run('invalid/cross-spine-duplicate-node-id').violation_requirement_ids
    assert {'SPD-SEC-001', 'SPD-ID-006'} <= set(run('invalid/event-handler').violation_requirement_ids)


@pytest.mark.parametrize('name', ['stale-fixed-rendition', 'mapping-with-stale-fixed', 'mutation-fixed'])
def test_no_document_only_processor_finding(name):
    ids = run('invalid/' + name).violation_requirement_ids
    assert 'SPD-STATE-007' in ids
    assert 'SPD-STATE-001' not in ids


@pytest.mark.parametrize('name', ['mutation-css', 'mutation-fixed', 'mutation-mapping', 'sealed-after-annotation-modification'])
def test_nonsemantic_integrity_is_not_semantic_mutation(name):
    ids = run('invalid/' + name).violation_requirement_ids
    assert {'SPD-INT-003', 'SPD-RES-004'} <= set(ids)
    assert 'SPD-STATE-003' not in ids


def test_editable_bad_hash_and_projection_failures():
    assert set(run('invalid/bad-resource-hash').violation_requirement_ids) == {'SPD-INT-003', 'SPD-INT-004', 'SPD-INT-005', 'SPD-RES-004'}


def test_accessible_manual_work_does_not_block_current_base_scope():
    from spd_validator_b.coverage import load_registry
    from spd_validator_b.validator import _roll_up
    report = run('valid/accessible')
    report.findings = [f for f in report.findings if f.requirement_id != 'SPD-BASE-002']
    _roll_up(report, load_registry(ROOT / 'spec/requirements-0.1-rc1.yaml'), {'Base', 'Accessible'}, True)
    assert report.base == 'PASS'
    assert report.normative_capabilities['Accessible'] == 'NOT_TESTED'
    assert run('invalid/bad-resource-hash').requirement_outcomes['SPD-STATE-002'] == 'NOT_APPLICABLE'


@pytest.mark.parametrize('name', ['descriptor-discovery-missing', 'descriptor-discovery-conflict'])
def test_unknown_descriptor_facts(name):
    report = run('invalid/' + name)
    assert report.metadata['authoritativeClaimsStatus'] == 'UNKNOWN'
    assert report.normative_capabilities['Mapping'] == 'UNKNOWN'
    assert 'SPD-CAP-003' in report.not_tested_requirement_ids
    assert 'SPD-ARCH-001' not in report.violation_requirement_ids
    assert _claims(Descriptors()) is None
    assert _claims(Descriptors(document={'capabilities': []})) == set()


def test_shared_external_policy_no_blanket_mapping():
    assert policy()['version'] == '0.1.2'
    assert external_ids('ERROR(OPF-014): scripted missing') == ['SPD-BASE-002']
    assert external_ids('ERROR(RSC-005): Duplicate ID "n_x"') == ['SPD-BASE-002', 'SPD-ID-006']
    assert external_ids('ERROR(OPF-060): Duplicate entry in the ZIP file') == ['SPD-BASE-002']
    assert external_ids('WARNING(RSC-005): Duplicate ID "n_x"') == []


def test_current_corpus_against_independent_native_oracle():
    manifest = json.loads((ROOT / 'tests/corpus-0.1-rc1/manifest.json').read_text(encoding='utf-8'))
    for fixture in manifest['fixtures']:
        expected = json.loads((ROOT / fixture['expectedResult']).read_text(encoding='utf-8'))
        actual = validate(ROOT / fixture['package'])
        assert actual.violation_requirement_ids == expected['nativeViolationRequirementIds'], fixture['id']
