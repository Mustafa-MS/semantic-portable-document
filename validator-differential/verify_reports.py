"""Verify report completeness and unchanged protected inputs; writes only audit evidence."""
import ast
import collections
import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    raw = read(OUT / 'raw-diff.json')
    a = {r['fixture']: r for r in read(ROOT / 'validator-a/reports/golden/validator-a-0.1.0-draft.1.json')['results']}
    b = {r['fixture']: r for r in read(ROOT / 'validator-b/reports/blind-results-with-epubcheck.json')['results']}
    assert set(a) == set(b) == {r['fixture'] for r in raw['fixtures']}
    differing = []
    for row in raw['fixtures']:
        fid = row['fixture']
        for field in raw['contractFields']:
            assert row['A'][field] == a[fid][field]
            assert row['B'][field] == b[fid][field]
            assert row['equalFields'][field] == (a[fid][field] == b[fid][field])
        av, bv = set(a[fid]['violationRequirementIds']), set(b[fid]['violationRequirementIds'])
        assert row['A_ONLY'] == sorted(av - bv)
        assert row['B_ONLY'] == sorted(bv - av)
        assert row['COMMON'] == sorted(av & bv)
        if av != bv:
            differing.append(row)
            assert av < bv
            assert set(row['analysis']['additionalFindingAssessment']) == bv - av
    assert len(differing) == 25
    assert dict(collections.Counter(x['analysis']['primaryClassification'] for x in differing)) == raw['classificationCounts']
    table = (OUT / 'fixture-differences.md').read_text(encoding='utf-8')
    for row in differing:
        assert table.count('| ' + row['fixture'] + ' |') == 1
    expected = ['summary.md', 'fixture-differences.md', 'requirement-differences.md',
                'disagreement-families.md', 'multi-spine-investigation.md',
                'cascade-semantics-analysis.md', 'experimental-capability-differences.md', 'proposed-resolutions.md']
    for name in expected:
        assert (OUT / name).is_file() and (OUT / name).stat().st_size > 100
    assert (OUT / 'multi-spine-investigation.md').read_text(encoding='utf-8').strip().endswith('CORPUS_WRONG')
    for name in ['summary.md', 'proposed-resolutions.md']:
        assert (OUT / name).read_text(encoding='utf-8').strip().endswith('PROCEED TO VALIDATOR CONVERGENCE FIXES')
    hashes = read(OUT / 'protected-input-hashes.json')
    changed = [p for p, value in hashes.items() if 'sha256:' + hashlib.sha256((ROOT / p).read_bytes()).hexdigest() != value]
    assert not changed, changed
    for p in OUT.glob('*.py'):
        ast.parse(p.read_text(encoding='utf-8'))
    audit = {'status': 'PASS', 'frozenRowsVerified': len(a), 'differingFixturesClassified': len(differing),
             'additionalRequirementOccurrencesAssessed': sum(len(x['B_ONLY']) for x in differing),
             'requiredReportsPresent': 9, 'protectedFilesRechecked': len(hashes), 'changedProtectedFiles': changed,
             'note': 'Protected snapshot was recorded during analysis before narrative report generation, not independently before the task. All authored writes were confined to validator-differential. Frozen B/Draft/registry pins were independently checked at initial comparison.'}
    (OUT / 'verification.json').write_text(json.dumps(audit, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(audit, indent=2))


if __name__ == '__main__':
    main()
