"""Build 0.1.2 fixture bytes and a predicate-authored oracle, never from A/B output."""
import copy
import hashlib
import io
import json
import re
import struct
import zipfile
from pathlib import Path
import rfc8785

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports/pre_rc_passive_security'
DEST = ROOT / 'tests/corpus-0.1.2'
PARTIAL = {'SPD-PASS-001', 'SPD-PASS-002', 'SPD-PASS-003', 'SPD-RS-001', 'SPD-RS-002'}

def sha(b): return hashlib.sha256(b).hexdigest()
def tagged(b): return 'sha256:' + sha(b)
def encoded(x): return (json.dumps(x, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode()

def resources(fixture='minimal-base'):
    with zipfile.ZipFile(ROOT / f'tests/valid/{fixture}/document.epub') as z:
        return {n: z.read(n) for n in z.namelist()}

def rebind(r, addition_order=None):
    ip, dp, sp = ['META-INF/spd/' + n for n in ['inventory.json', 'document-state.json', 'state.json']]
    inv, doc, state = [json.loads(r[n]) for n in [ip, dp, sp]]
    known = {x['path'] for x in inv['resources']}
    types = {'.css':'text/css','.svg':'image/svg+xml','.png':'image/png','.mp3':'audio/mpeg','.vtt':'text/vtt','.ttf':'font/ttf','.txt':'text/plain'}
    missing = r.keys() - known - {ip, sp}
    ordered = addition_order if addition_order is not None else sorted(missing)
    assert set(ordered) == missing
    for path in ordered:
        ext = Path(path).suffix
        inv['resources'].append({'path':path,'mediaType':types.get(ext,'application/octet-stream'),'byteLength':len(r[path]),'sha256':tagged(r[path]),'affects':['rendering'] if ext in types and ext != '.txt' else [], 'role':'authoritative' if ext in types and ext != '.txt' else 'non-normative'})
    for rec in inv['resources']:
        if rec['path'] in r:
            rec.update(byteLength=len(r[rec['path']]),sha256=tagged(r[rec['path']]))
    for field, effects in [('semanticStateDigest',{'semantic'}),('renditionInputDigest',{'semantic','rendering'})]:
        selected = sorted((x for x in inv['resources'] if effects.intersection(x['affects'])),key=lambda x:x['path'].encode())
        digest = tagged(b''.join((x['path']+'\0'+str(x['byteLength'])+'\0'+x['sha256']+'\n').encode() for x in selected))
        doc[field] = state[field] = digest
    r[dp] = encoded(doc)
    for rec in inv['resources']:
        if rec['path']==dp: rec.update(byteLength=len(r[dp]),sha256=tagged(r[dp]))
    r[ip] = encoded(inv)
    state['inventory']['sha256'] = tagged(r[ip])
    state['descriptorDigest'] = tagged(rfc8785.dumps({k:v for k,v in state.items() if k!='descriptorDigest'}))
    r[sp] = encoded(state)

def package(r, modes=None, addition_order=None):
    rebind(r, addition_order)
    out=io.BytesIO()
    with zipfile.ZipFile(out,'w') as z:
        for name,data in r.items():
            info=zipfile.ZipInfo(name,(2026,9,4,0,0,0))
            info.compress_type=zipfile.ZIP_STORED if name=='mimetype' else zipfile.ZIP_DEFLATED
            if modes and name in modes: info.create_system=3; info.external_attr=modes[name]<<16
            z.writestr(info,data)
    return out.getvalue()

def body(r, text):
    r['EPUB/content.xhtml']=r['EPUB/content.xhtml'].replace(b'</body>',text.encode()+b'</body>')

def head(r,text):
    r['EPUB/content.xhtml']=r['EPUB/content.xhtml'].replace(b'</head>',text.encode()+b'</head>')

def asset(r,path,data,media,properties=''):
    r[path]=data if isinstance(data,bytes) else data.encode()
    opf=next(p for p in r if p.endswith('.opf'))
    item=f'<item id="asset{len(r)}" href="{path.removeprefix("EPUB/")}" media-type="{media}"'+(f' properties="{properties}"' if properties else '')+'/>'
    r[opf]=r[opf].replace(b'</manifest>',item.encode()+b'</manifest>')

def properties(r, value):
    opf=next(p for p in r if p.endswith('.opf'))
    text=r[opf].decode()
    text=re.sub(r'<item\b[^>]*href="content.xhtml"[^>]*/>',lambda m:m[0][:-2] + f' properties="{value}"/>',text)
    r[opf]=text.encode()

CASES=[]
def case(label,name,mutate,ids=(),notes='',source='minimal-base',operation='COMPLETE'):
    CASES.append((label,name,mutate,list(ids),notes,source,operation))

def setup():
    remote_image=['SPD-SEC-003','SPD-SEC-006','SPD-SEC-008']
    remote_css=['SPD-SEC-003','SPD-SEC-005','SPD-SEC-008']
    case('S01','optional-remote-image',lambda r:body(r,'<img src="https://example.invalid/pixel.png" alt=""/>'),remote_image,'Decorative alt-empty image; no network is performed.')
    case('S02','escaped-remote-import',lambda r:head(r,'<style>@import "h\\74tps://example.invalid/style.css";</style>'),remote_css)
    case('S03','inline-remote-style',lambda r:body(r,'<div style="background:url(https://example.invalid/a.png)">Static text</div>'),remote_image)
    case('S04','custom-property-resource',lambda r:head(r,'<style>:root {--art:url(https://example.invalid/a.png)} body {background-image:var(--art)}</style>'),remote_image)
    def svg_asset(r,contents):
        asset(r,'EPUB/picture.svg','<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">'+contents+'</svg>','image/svg+xml')
        body(r,'<img src="picture.svg" alt="Static diagram"/>')
    case('S05','nested-svg-remote',lambda r:svg_asset(r,'<image href="https://example.invalid/a.png" width="10" height="10"/>'),remote_image+['SPD-SEC-007'])
    case('S06','inline-foreignobject',lambda r:(properties(r,'svg'),body(r,'<svg xmlns="http://www.w3.org/2000/svg"><foreignObject width="20" height="20"><div xmlns="http://www.w3.org/1999/xhtml">Text</div></foreignObject></svg>')),['SPD-SEC-007','SPD-PASS-002'])
    case('S07','prefixed-svg-script',lambda r:(properties(r,'svg scripted'),body(r,'<s:svg xmlns:s="http://www.w3.org/2000/svg"><s:script>void(0)</s:script></s:svg>')),['SPD-SEC-001','SPD-SEC-007'])
    case('S08','encoded-executable-link',lambda r:(properties(r,'scripted'),body(r,'<a href="java&#x73;cript:void(0)">Example</a>')),['SPD-SEC-001','SPD-SEC-008'])
    case('S09','iframe-srcdoc',lambda r:(properties(r,'scripted'),body(r,'<iframe srcdoc="&lt;p&gt;Frame&lt;/p&gt;"></iframe>')),['SPD-SEC-002','SPD-PASS-002'])
    case('S10','object-embed',lambda r:(properties(r,'scripted'),body(r,'<object></object><embed/>')),['SPD-SEC-002','SPD-PASS-002'])
    case('S11','active-form',lambda r:(properties(r,'scripted'),body(r,'<form><button id="n_submit" type="submit">Submit</button></form>')),['SPD-PASS-002'])
    case('S12','meta-refresh',lambda r:head(r,'<meta http-equiv="refresh" content="0;url=https://example.invalid/"/>'),['SPD-PASS-002','SPD-SEC-003'])
    case('S13','base-overrides',lambda r:(head(r,'<base href="./"/>'),body(r,'<div xml:base="./">Static</div>')),['SPD-PASS-002'])
    case('S14','network-hints',lambda r:(head(r,'<link rel="prefetch" href="https://example.invalid/a"/><link rel="preconnect" href="https://example.invalid/"/>'),body(r,'<a href="https://example.invalid/" ping="https://example.invalid/ping">Link</a>')),['SPD-SEC-003','SPD-SEC-008'])
    def local_css(r):
        asset(r,'EPUB/assets/sample.png',(ROOT/'corpus/sources/assets/sample.png').read_bytes(),'image/png')
        asset(r,'EPUB/font.ttf',(ROOT/'tests/corpus-0.1.2/source-assets/font.ttf').read_bytes(),'font/ttf')
        asset(r,'EPUB/import.css','body {color:#123} .art {background-image:url(assets/sample.png)}','text/css')
        head(r,'<style>@import "import.css" screen; @font-face {font-family:Packaged;src:url(font.ttf)} body {--tone:#123; color:var(--tone);font-family:Packaged} @media print { body {transform:translate(0,0)} }</style>')
    case('S15','local-css-font-image',local_css,source='figure-svg')
    def cycle(r):
        asset(r,'EPUB/one.css','@import "two.css";','text/css'); asset(r,'EPUB/two.css','@import "one.css";','text/css'); head(r,'<link rel="stylesheet" href="one.css"/>')
    case('S16','local-import-cycle',cycle,['SPD-SEC-008'])
    case('S17','static-svg-local',lambda r:svg_asset(r,'<defs><linearGradient id="g"><stop offset="0" stop-color="blue"/></linearGradient><clipPath id="c"><rect width="100" height="100"/></clipPath><mask id="m"><rect width="100" height="100" fill="white"/></mask><symbol id="s"><rect width="20" height="20"/></symbol></defs><use href="#s"/><rect width="20" height="20" fill="url(#g)" clip-path="url(#c)" mask="url(#m)"/>'))
    case('S18','inert-controls',lambda r:body(r,'<label for="n_input">Value</label><input id="n_input" type="text" disabled="disabled" value="Preserved"/><button id="n_button" type="button" disabled="disabled">Preserved action</button>'))
    # Tiny MP3 asset from existing repository if present; generated silent MPEG frame otherwise.
    def media(r,autoplay=False):
        asset(r,'EPUB/silence.mp3',b'\xff\xfb\x90\x64'+bytes(413),'audio/mpeg')
        body(r,'<audio controls="controls"'+(' autoplay="autoplay"' if autoplay else '')+' src="silence.mp3">Silent audio.</audio><div>Transcript: silence; no document meaning relies on playback.</div>')
    case('S19','local-media',media)
    case('S20','media-autoplay',lambda r:media(r,True),['SPD-PASS-003'])
    case('S21','static-animation-declaration',lambda r:head(r,'<style>body {color:black; transition:color 1s} @keyframes decorative {from{opacity:1} to{opacity:1}}</style>'),notes='File declarations retained. Human static completeness and processor suppression remain NOT_TESTED.')
    case('S22','mathml-local-glyph',lambda r:(asset(r,'EPUB/assets/sample.png',(ROOT/'corpus/sources/assets/sample.png').read_bytes(),'image/png'),properties(r,'mathml'),body(r,'<math xmlns="http://www.w3.org/1998/Math/MathML" id="n_math"><mrow href="https://example.invalid/"><mi>x</mi><mtext><mglyph src="assets/sample.png" alt="dot"/></mtext></mrow></math>')),source='figure-svg')
    case('S23','mathml-remote-glyph',lambda r:(properties(r,'mathml'),body(r,'<math xmlns="http://www.w3.org/1998/Math/MathML" id="n_math"><mtext><mglyph src="https://example.invalid/a.png" alt="dot"/></mtext></math>')),remote_image)
    case('S24','inert-hostile-metadata',lambda r:head(r,'<meta name="description" content="&lt;script&gt;alert(1)&lt;/script&gt; https://example.invalid/context"/>'),notes='Metadata text is data, not a resource request.',source='annotations')
    case('S25','zip-special-modes',lambda r:None,['SPD-BASE-002'],notes='Existing regular CSS/image resources are marked symlink/device; content bytes retained.',source='figure-svg')
    def collision(r):
        r['EPUB/collision.txt']=b'one'; r['EPUB/%63ollision.txt']=b'two'
    case('S26','decoded-path-collision',collision,['SPD-BASE-002','SPD-RES-002'])
    case('S27','zip-header-mismatch',lambda r:None,notes='Local header filename differs from central directory; MALFORMED_INPUT, no fabricated native violation.',operation='MALFORMED_INPUT')
    def bomb(r): r['META-INF/padding.txt']=bytes(2*1024*1024)
    case('S28','bounded-expansion',bomb,notes='Small on-disk highly compressible data exceeds implementation ratio budget; no universal format maximum.',operation='RESOURCE_LIMIT')
    def title(r):
        opf=next(p for p in r if p.endswith('.opf')); r[opf]=re.sub(rb'<dc:title[^>]*>.*?</dc:title>',b'',r[opf],flags=re.S)
    case('S29','unmapped-epub-title',title,notes='Only required OPF title removed; inventory and state rebound. BASE-002 from inherited EPUB conformance.')
    case('S30','script-data-block',lambda r:head(r,'<script type="application/json">{"data":true}</script>'),['SPD-SEC-001'])
    case('S31','standalone-svg-script',lambda r:svg_asset(r,'<script>void(0)</script>'),['SPD-SEC-001','SPD-SEC-007'])
    case('S32','svg-event-handler',lambda r:svg_asset(r,'<rect width="10" height="10" onclick="void(0)"/>'),['SPD-SEC-001','SPD-SEC-007'])
    case('S33','plain-iframe',lambda r:(properties(r,'scripted'),body(r,'<iframe title="Frame"></iframe>')),['SPD-SEC-002','SPD-PASS-002'])
    case('S34','authoritative-canvas',lambda r:body(r,'<canvas width="50" height="50">Interactive drawing</canvas>'),['SPD-PASS-002'])
    case('S35','ordinary-hyperlink',lambda r:body(r,'<a href="https://example.invalid/">Explicit destination</a>'))
    case('S36','nested-rule-remote',lambda r:head(r,'<style>@media screen {@supports(display:grid) {body {background:url(https://example.invalid/a.png)}}}</style>'),remote_image)
    case('S37','annotation-xml-active',lambda r:(properties(r,'mathml scripted'),body(r,'<math xmlns="http://www.w3.org/1998/Math/MathML" id="n_math"><semantics><mi>x</mi><annotation-xml encoding="application/xhtml+xml"><script xmlns="http://www.w3.org/1999/xhtml">void(0)</script></annotation-xml></semantics></math>')),['SPD-SEC-001'])

def main():
    DEST.mkdir(exist_ok=True)
    manifest=copy.deepcopy(json.loads((ROOT/'tests/corpus-manifest.json').read_text()))
    manifest['corpusVersion']='0.1.2'
    historical=json.loads((ROOT/'validator-convergence/final-0.1.1-a.json').read_text())
    external={x['fixture']:x for x in historical['externalEvaluations']}
    decisions=[]
    for f in manifest['fixtures']:
        expected=json.loads((ROOT/f['expectedResult']).read_text())
        ids={v['requirement'] for v in expected['violations']}
        if external[f['id']].get('outcome')=='FAIL': ids.add('SPD-BASE-002')
        if f['id'] in {'invalid/external-required-css','invalid/external-required-font','invalid/external-required-image'}: ids.update({'SPD-SEC-003','SPD-SEC-008'})
        expected['violations']=[{'requirement':i} for i in sorted(ids)]
        expected['notTestedRequirementIds']=sorted((set(expected['notTestedRequirementIds'])|PARTIAL)-ids)
        expected['corpusVersion']='0.1.2'
        dest=DEST/'historical'/f['id']; dest.mkdir(parents=True,exist_ok=True)
        (dest/'expected.json').write_bytes(encoded(expected))
        f['expectedResult']=(dest/'expected.json').relative_to(ROOT).as_posix()
        f['expectedResultSha256']=sha(encoded(expected))
    setup()
    addition_orders=json.loads((ROOT/'scripts/pre_rc_resource_order.json').read_text())
    for label,name,mutate,ids,notes,source,operation in CASES:
        r=resources(source); mutate(r)
        modes=None
        if label=='S25':
            modes={p:0o120777 if p.endswith('.css') else 0o020666 for p in r if p.endswith(('.css','.svg'))}
        data=package(r,modes,addition_orders[name])
        if label=='S27':
            data=bytearray(data); data[30]=ord('M'); data=bytes(data)
        dest=DEST/name; dest.mkdir(exist_ok=True)
        (dest/'document.epub').write_bytes(data)
        expected=json.loads((ROOT/f'tests/valid/{source}/expected.json').read_text())
        fid='security/'+name
        expected.update(fixture=fid,corpusVersion='0.1.2',base='FAIL' if ids else 'PASS',violations=[{'requirement':i} for i in sorted(ids)],notes=[notes] if notes else [],operationalStatus=operation)
        expected['notTestedRequirementIds']=sorted((set(expected['notTestedRequirementIds'])|PARTIAL)-set(ids))
        if ids:
            for cap in ['Accessible','Mapping']:
                if expected['capabilities'][cap]!='NOT_CLAIMED': expected['capabilities'][cap]='FAIL'
        (dest/'expected.json').write_bytes(encoded(expected))
        manifest['fixtures'].append({'id':fid,'name':name,'category':'security','auditCase':label,'package':(dest/'document.epub').relative_to(ROOT).as_posix(),'packageSha256':sha(data),'expectedResult':(dest/'expected.json').relative_to(ROOT).as_posix(),'expectedResultSha256':sha(encoded(expected)),'primaryRequirements':ids,'notes':[notes] if notes else []})
        decisions.append({'fixture':fid,'auditCase':label,'nativePredicates':sorted(ids),'source':source,'reason':notes,'externalReview':'pending direct EPUBCheck diagnostic review; never derived from A/B'})
    manifest['fixtureCount']=len(manifest['fixtures'])
    manifest['counts']['security']=len(CASES)
    (DEST/'manifest.json').write_bytes(encoded(manifest))
    (OUT/'oracle-native-decisions.json').write_bytes(encoded(decisions))
    print('Built',len(CASES),'new cases;',len(manifest['fixtures']),'total. External oracle review pending.')

if __name__=='__main__': main()
