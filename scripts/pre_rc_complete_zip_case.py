"""Complete S25's two-mode audit case; run only after ongoing evaluations finish."""
import hashlib
import importlib.util
import json
import subprocess
import zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/pre_rc_passive_security'

def main():
    # Capture pre-revision evidence before changing this one package.
    path=ROOT/'tests/corpus-0.1.2/zip-special-modes/document.epub'
    previous=path.read_bytes()
    artifact=OUT/'s25-initial-symlink-only.epub'
    if not artifact.exists():artifact.write_bytes(previous)
    spec=importlib.util.spec_from_file_location('builder',ROOT/'scripts/pre_rc_corpus.py')
    b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
    r=b.resources('figure-svg')
    modes={p:0o120777 if p.endswith('.css') else 0o020666 for p in r if p.endswith(('.css','.svg'))}
    order=json.loads((ROOT/'scripts/pre_rc_resource_order.json').read_text())['zip-special-modes']
    data=b.package(r,modes,order);path.write_bytes(data)
    with zipfile.ZipFile(path) as z:
        actual={i.filename:oct((i.external_attr>>16)&0o170000) for i in z.infolist() if i.filename in modes}
        assert set(actual.values())=={'0o120000','0o20000'}
    manifest_path=ROOT/'tests/corpus-0.1.2/manifest.json';m=json.loads(manifest_path.read_text())
    for f in m['fixtures']:
        if f['id']=='security/zip-special-modes':f['packageSha256']=hashlib.sha256(data).hexdigest()
    manifest_path.write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
    jar=ROOT/'validator-b/tools/official-5.3.0/epubcheck-5.3.0/epubcheck.jar'
    result=subprocess.run(['java','-jar',str(jar),str(path)],capture_output=True,text=True,encoding='utf-8',timeout=120)
    assert result.returncode==0,result.stderr
    review_path=OUT/'direct-epubcheck-review.json';review=json.loads(review_path.read_text())
    for row in review:
        if row['fixture']=='security/zip-special-modes':row.update(packageSha256=hashlib.sha256(data).hexdigest(),exitCode=0,errors=[],ids=[],stdout=result.stdout,stderr=result.stderr)
    review_path.write_text(json.dumps(review,indent=2)+'\n')
    js={'reason':'Final byte inspection found S25 initially covered symlink mode only. SVG entry now also exercises device mode; no payload or normative outcome changed. Both validators must re-evaluate these final bytes.','beforeSha256':hashlib.sha256(previous).hexdigest(),'afterSha256':hashlib.sha256(data).hexdigest(),'modes':actual}
    (OUT/'s25-mode-review.json').write_text(json.dumps(js,indent=2)+'\n')
    # Keep the authored recipe and byte-rebuild evidence in sync.
    p=ROOT/'scripts/pre_rc_corpus.py';s=p.read_text().replace("p.endswith(('.css','.png'))", "p.endswith(('.css','.svg'))");p.write_text(s)
    rebuild_path=OUT/'rebuild-verification.json';checks=json.loads(rebuild_path.read_text())
    assert b.package(b.resources('figure-svg'),modes,order)==data
    for row in checks:
        if row['fixture']=='zip-special-modes':row.update(packageSha256=hashlib.sha256(data).hexdigest(),rebuiltSha256=hashlib.sha256(data).hexdigest(),identical=True)
    rebuild_path.write_text(json.dumps(checks,indent=2)+'\n')
    print('S25 now includes both symlink and device modes; direct EPUBCheck PASS')

if __name__=='__main__':main()
