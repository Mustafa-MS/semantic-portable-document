"""Review byte-grounded native predicates plus direct EPUB diagnostics, not A/B votes."""
import hashlib
import json
import re
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/pre_rc_passive_security'
PARTIAL={'SPD-PASS-001','SPD-PASS-002','SPD-PASS-003','SPD-RS-001','SPD-RS-002'}

def encoded(x):return (json.dumps(x,indent=2,sort_keys=True)+'\n').encode()

def main():
    path=ROOT/'tests/corpus-0.1.2/manifest.json';manifest=json.loads(path.read_text())
    direct={r['fixture']:r for r in json.loads((OUT/'direct-epubcheck-review.json').read_text())}
    native={r['fixture']:r for r in json.loads((OUT/'oracle-native-decisions.json').read_text())}
    registry=yaml.safe_load((ROOT/'spec/requirements.yaml').read_text())
    automatic={r['id'] for r in registry['requirements'] if r['testability']=='AUTOMATED'}
    policy=json.loads((ROOT/'validation/REQUIREMENT_ATTRIBUTION_0.1.2.json').read_text())
    results=[]
    for f in manifest['fixtures']:
        p=ROOT/f['expectedResult']; e=json.loads(p.read_text())
        if f['category']=='security':
            n=set(native[f['id']]['nativePredicates']); ids=set(n);r=direct[f['id']]
            assert r['packageSha256']==f['packageSha256'],f['id']+' needs direct EPUB rerun'
            for line in r['errors']:
                ids.add('SPD-BASE-002')
                for rule in policy['externalDiagnostics']:
                    if '('+rule['code']+')' in line and re.search(rule['pattern'],line):ids.update(rule['ids'])
            e['nativeViolationRequirementIds']=sorted(n)
            e['nativeBase']='FAIL' if n else 'PASS'
            if e['operationalStatus'] in {'MALFORMED_INPUT','RESOURCE_LIMIT'}:
                e['nativeBase']='NOT_TESTED'; e['base']='FAIL' if ids else 'NOT_TESTED'
                e['authoritativeClaimsStatus']='UNKNOWN';e['experimentalReporting']={}
                e['capabilities']={c:'UNKNOWN' for c in e['capabilities']}
                e['notTestedRequirementIds']=sorted((automatic|PARTIAL)-ids)
            else:
                e['base']='FAIL' if ids else 'PASS'
                e['notTestedRequirementIds']=sorted((set(e['notTestedRequirementIds'])|PARTIAL)-ids)
                if e['base']=='FAIL':
                    for cap in ['Accessible','Mapping']:
                        if e['capabilities'][cap]!='NOT_CLAIMED':e['capabilities'][cap]='FAIL'
            e['violations']=[{'requirement':i} for i in sorted(ids)]
            e['epubcheckExpected']='PASS' if r['exitCode']==0 else 'FAIL'
            if not n and e['operationalStatus']=='COMPLETE' and f['id']!='security/unmapped-epub-title':
                assert not ids, f['id']+' is an intended valid fixture with EPUB failure'
        else:
            old=json.loads((ROOT/('tests/'+f['id']+'/expected.json')).read_text())
            n={r['requirement'] for r in old['violations']}
            if f['id'] in {'invalid/external-required-css','invalid/external-required-font','invalid/external-required-image'}:n.update({'SPD-SEC-003','SPD-SEC-008'})
            e['nativeViolationRequirementIds']=sorted(n);e['nativeBase']=old['base']
        if f['id']=='security/unmapped-epub-title':
            assert e['violations']==[{'requirement':'SPD-BASE-002'}]
        p.write_bytes(encoded(e));f['expectedResultSha256']=hashlib.sha256(p.read_bytes()).hexdigest()
        results.append(e)
    path.write_bytes(encoded(manifest))
    (OUT/'reviewed-oracle-0.1.2.json').write_bytes(encoded({'version':'0.1.2','source':'Native predicates authored before validator runs; direct EPUBCheck diagnostic review; preserved historical oracle; no implementation is oracle','fixtureCount':len(results),'results':results}))
    (OUT/'manifest-sha256.txt').write_text(hashlib.sha256(path.read_bytes()).hexdigest()+'\n')
    print('Reviewed',len(results),'oracle rows')

if __name__=='__main__':main()
