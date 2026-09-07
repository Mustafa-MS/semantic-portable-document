"""Direct upstream evaluation for independent fixture review (imports no validator)."""
import concurrent.futures
import json
import re
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/pre_rc_passive_security'
JAR=ROOT/'validator-b/tools/official-5.3.0/epubcheck-5.3.0/epubcheck.jar'

def main():
    manifest=json.loads((ROOT/'tests/corpus-0.1.2/manifest.json').read_text())
    fixtures=[f for f in manifest['fixtures'] if f['category']=='security']
    policy=json.loads((ROOT/'validation/REQUIREMENT_ATTRIBUTION_0.1.2.json').read_text())
    def run(f):
        p=subprocess.run(['java','-jar',str(JAR),str(ROOT/f['package'])],capture_output=True,text=True,encoding='utf-8',timeout=120)
        output=p.stdout+'\n'+p.stderr
        errors=[line for line in output.splitlines() if re.search(r'\b(?:ERROR|FATAL)\(',line)]
        ids=set()
        for line in errors:
            ids.add('SPD-BASE-002')
            for rule in policy['externalDiagnostics']:
                if '('+rule['code']+')' in line and re.search(rule['pattern'],line): ids.update(rule['ids'])
        result={'fixture':f['id'],'packageSha256':f['packageSha256'],'exitCode':p.returncode,'errors':errors,'ids':sorted(ids),'stdout':p.stdout,'stderr':p.stderr}
        print(f['id'],p.returncode,sorted(ids),flush=True)
        return result
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: results=list(pool.map(run,fixtures))
    (OUT/'direct-epubcheck-review.json').write_text(json.dumps(results,indent=2)+'\n')

if __name__=='__main__':main()
