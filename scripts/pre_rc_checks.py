"""Capture acceptance commands; never write historical logs."""
import concurrent.futures
import json
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/pre_rc_passive_security'
PY=str(ROOT/'validator-b/.venv/Scripts/python.exe')

def run(name,cmd,cwd):
    result=subprocess.run(cmd,cwd=ROOT/cwd,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=900)
    (OUT/(name+'.log')).write_text(result.stdout+'\n'+result.stderr,encoding='utf-8')
    print(name,result.returncode,flush=True)
    return {'name':name,'command':cmd,'cwd':cwd,'exitCode':result.returncode}

def a():
    return [run(n,c,'validator-a') for n,c in [('a-fmt',['cargo','fmt','--check']),('a-clippy',['cargo','clippy','--offline','--all-targets','--','-D','warnings']),('a-tests',['cargo','test','--offline']),('a-release',['cargo','build','--release','--offline'])]]

def b():
    return [run(n,c,'validator-b') for n,c in [('b-lint',[PY,'-m','ruff','check','spd_validator_b','tests']),('b-tests',[PY,'-m','pytest','--junitxml=../reports/pre_rc_passive_security/b-tests.xml']),('b-wheel',[PY,'-m','build','--wheel','--no-isolation','--outdir','../reports/pre_rc_passive_security/dist'])]]

if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        fa=pool.submit(a);fb=pool.submit(b);results=fa.result()+fb.result()
    (OUT/'checks.json').write_text(json.dumps(results,indent=2)+'\n')
