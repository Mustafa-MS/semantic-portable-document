"""Run the independent validators on identical manifest-pinned bytes."""
import argparse
import concurrent.futures
import hashlib
import json
import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/pre_rc_passive_security'
JAR=ROOT/'validator-b/tools/official-5.3.0/epubcheck-5.3.0/epubcheck.jar'

def provenance(side):
    paths=[]
    for directory in ['spec','schemas','validator-a/src' if side=='a' else 'validator-b/spd_validator_b']:
        paths.extend(p for p in (ROOT/directory).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    paths.extend(ROOT/p for p in ['validation/REQUIREMENT_ATTRIBUTION_0.1.2.json','tests/corpus-0.1.2/manifest.json','validator-a/Cargo.lock' if side=='a' else 'validator-b/pyproject.toml'])
    return {p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('side',choices=['a','b']);parser.add_argument('--native',action='store_true');parser.add_argument('--workers',type=int,default=4);parser.add_argument('--retry-operational',action='store_true');parser.add_argument('--refresh-fixtures',default='');args=parser.parse_args()
    manifest=json.loads((ROOT/'tests/corpus-0.1.2/manifest.json').read_text())
    before=provenance(args.side)
    previous=None
    if args.retry_operational or args.refresh_fixtures:
        previous=json.loads((OUT/('candidate-'+args.side+'.json')).read_text())
        source_only=lambda d:{k:v for k,v in d.items() if k!='tests/corpus-0.1.2/manifest.json'}
        assert source_only(previous['sourceSha256'])==source_only(before), 'Cannot reuse results across implementation changes'
        failed={r['normalized']['fixture'] for r in previous['results'] if r['normalized']['operationalStatus']=='TOOL_UNAVAILABLE'}
        failed.update(filter(None,args.refresh_fixtures.split(',')))
        manifest['fixtures']=[f for f in manifest['fixtures'] if f['id'] in failed]
    sys.path.insert(0,str(ROOT/'validator-b'))
    if args.side=='b':
        from spd_validator_b.validator import validate
        from spd_validator_b.models import ValidationOptions,ResourceLimits
        options=ValidationOptions(epubcheck_jar=None if args.native else str(JAR),limits=ResourceLimits(max_package_bytes=536870912,max_entry_bytes=268435456,max_total_decompressed_bytes=1073741824,max_xml_bytes=33554432,max_json_bytes=67108864))
    def one(f):
        path=ROOT/f['package'];assert hashlib.sha256(path.read_bytes()).hexdigest()==f['packageSha256']
        expected=json.loads((ROOT/f['expectedResult']).read_text())
        if args.side=='a':
            cmd=[str(ROOT/'validator-a/target/release/spd-validator.exe'),'validate',str(path),'--format','json']
            if not args.native:cmd+=['--epubcheck',str(JAR)]
            p=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',timeout=200)
            r=json.loads(p.stdout)
            n={'fixture':f['id'],'base':r['base'],'normativeCapabilities':{c:r['capabilities'].get(c,'UNKNOWN') for c in ['Accessible','Mapping']},'experimentalCapabilities':{c:r['capabilities'].get(c,'UNKNOWN') for c in ['Archive-Experimental','Fixed-Experimental']},'violationRequirementIds':sorted({v['requirementId'] for v in r['findings'] if v['outcome']=='FAIL'}),'notTestedRequirementIds':r['notTestedRequirements'],'operationalStatus':r['operationalStatus'],'authoritativeClaimsStatus':r['authoritativeClaimsStatus'],'experimentalReporting':r['experimentalReporting']}
        else:
            result=validate(path,options);r=result.detailed();n=result.normalized(f['id'])
        wanted={'fixture':f['id'],'base':expected['base'],'normativeCapabilities':{c:expected['capabilities'][c] for c in ['Accessible','Mapping']},'experimentalCapabilities':{c:expected['capabilities'][c] for c in ['Archive-Experimental','Fixed-Experimental']},'violationRequirementIds':sorted(v['requirement'] for v in expected['violations']),'notTestedRequirementIds':expected['notTestedRequirementIds'],'operationalStatus':expected['operationalStatus'],'authoritativeClaimsStatus':expected['authoritativeClaimsStatus'],'experimentalReporting':expected['experimentalReporting']}
        keys=['violationRequirementIds'] if args.native else list(wanted)
        if args.native:
            wanted['violationRequirementIds'] = expected['nativeViolationRequirementIds']
        differences={k:{'expected':wanted[k],'actual':n[k]} for k in keys if wanted[k]!=n[k]}
        if differences:print(f['id'],json.dumps(differences),flush=True)
        return {'normalized':n,'report':r,'differences':differences}
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:results=list(pool.map(one,manifest['fixtures']))
    path=OUT/(('native-' if args.native else 'candidate-')+args.side+'.json')
    if previous is not None:
        attempt=OUT/('operational-attempt-'+args.side+'.json')
        index=2
        while attempt.exists():
            attempt=OUT/('operational-attempt-'+args.side+'-'+str(index)+'.json');index+=1
        attempt.write_text(json.dumps(previous,indent=2)+'\n')
        replacements={r['normalized']['fixture']:r for r in results}
        results=[replacements.get(r['normalized']['fixture'],r) for r in previous['results']]
        final_manifest=json.loads((ROOT/'tests/corpus-0.1.2/manifest.json').read_text())
        final_hashes={f['id']:f['packageSha256'] for f in final_manifest['fixtures']}
        for row in results:
            report=row['report'];external=report['externalTools'][0] if args.side=='a' else report['metadata']['epubcheck']
            assert external['fixtureSha256']==final_hashes[row['normalized']['fixture']], 'Cannot reuse a result for different package bytes'
    after=provenance(args.side)
    path.write_text(json.dumps({'validator':args.side,'version':'0.1.0-draft.3' if args.side=='a' else '0.1.2','fixtureCount':len(results),'manifestSha256':hashlib.sha256((ROOT/'tests/corpus-0.1.2/manifest.json').read_bytes()).hexdigest(),'epubcheckJarSha256':hashlib.sha256(JAR.read_bytes()).hexdigest(),'sourceSha256':before,'sourceStableDuringRun':before==after,'results':results},indent=2)+'\n')
    print('Completed',args.side,len(results),'fixtures;',sum(bool(r['differences']) for r in results),'differences',flush=True)

if __name__=='__main__':main()
