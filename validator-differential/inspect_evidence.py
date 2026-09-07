"""Independent package-byte inspection, not a validator and not an oracle repair."""
import hashlib
import json
import unicodedata
import zipfile
from pathlib import Path
from lxml import etree
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'validator-differential'


def sha(data):
    return 'sha256:' + hashlib.sha256(data).hexdigest()


def main():
    diff = json.loads((OUT / 'raw-diff.json').read_text())
    schemas = {k: json.loads((ROOT / 'schemas' / v).read_text()) for k, v in {
        'document': 'document-state.schema.json', 'inventory': 'resource-inventory.schema.json',
        'state': 'state.schema.json', 'mapping': 'mapping.schema.json'}.items()}
    rows = []
    for row in diff['fixtures']:
        path = ROOT / 'tests' / row['fixture'] / 'document.epub'
        with zipfile.ZipFile(path) as z:
            # These explicit diagnostic reads DO NOT constitute normative discovery.
            # In the two discovery failures, undiscovered files are forensic evidence only.
            objs = {k: json.loads(z.read(v)) for k, v in {
                'document': 'META-INF/spd/document-state.json', 'inventory': 'META-INF/spd/inventory.json',
                'state': 'META-INF/spd/state.json'}.items()}
            if 'META-INF/spd/mapping.json' in z.namelist():
                objs['mapping'] = json.loads(z.read('META-INF/spd/mapping.json'))
            d, inv, s = (objs[k] for k in ['document', 'inventory', 'state'])
            bad = []
            for entry in inv['resources']:
                data = z.read(entry['path'])  # no extraction, including traversal fixture
                if sha(data) != entry['sha256'] or len(data) != entry['byteLength']:
                    bad.append({'path': entry['path'], 'affects': entry['affects'],
                                'declaredLength': entry['byteLength'], 'actualLength': len(data),
                                'declaredSha256': entry['sha256'], 'actualSha256': sha(data)})
            projections = {}
            for name, effects in [('semanticStateDigest', {'semantic'}), ('renditionInputDigest', {'semantic', 'rendering'})]:
                selected = sorted((e for e in inv['resources'] if effects.intersection(e['affects'])), key=lambda e: e['path'].encode())
                value = sha(b''.join((e['path'] + '\0' + str(e['byteLength']) + '\0' + e['sha256'] + '\n').encode() for e in selected))
                projections[name] = {'computedFromDeclaredInventory': value, 'documentDeclared': d[name], 'stateDeclared': s[name], 'matchesBoth': value == d[name] == s[name]}
            parser = etree.XMLParser(resolve_entities=False, no_network=True, recover=False)
            container = etree.fromstring(z.read('META-INF/container.xml'), parser)
            links = [dict(x.attrib) for x in container.iter() if etree.QName(x).localname == 'link']
            opf = etree.fromstring(z.read('EPUB/package.opf'), parser)
            ns = {'o': 'http://www.idpf.org/2007/opf'}
            manifest = {x.get('id'): x.get('href') for x in opf.xpath('./o:manifest/o:item', namespaces=ns)}
            spine = ['EPUB/' + manifest[x.get('idref')] for x in opf.xpath('./o:spine/o:itemref', namespaces=ns)]
            ids, parse_errors = [], []
            for resource in spine:
                try:
                    doc = etree.fromstring(z.read(resource), parser)
                except etree.XMLSyntaxError as exc:
                    parse_errors.append({'resource': resource, 'error': str(exc)})
                    continue
                for node in doc.iter():
                    if node.get('id'):
                        ids.append({'id': node.get('id'), 'resource': resource, 'line': node.sourceline, 'xpath': node.getroottree().getpath(node)})
            duplicates = {key: [x for x in ids if x['id'] == key] for key in sorted({x['id'] for x in ids}) if sum(x['id'] == key for x in ids) > 1}
            schema_errors = {k: [{'pointer': '/' + '/'.join(map(str, e.absolute_path)), 'message': e.message} for e in Draft202012Validator(schemas[k]).iter_errors(v)] for k, v in objs.items()}
            candidate_errors = []
            for link in links:
                if link['rel'].endswith('/document-state'):
                    candidate = json.loads(z.read(link['href']))
                    candidate_errors = [e.message for e in Draft202012Validator(schemas['document']).iter_errors(candidate)]
            fixed = s['fixedRendition']
            rows.append({'fixture': row['fixture'], 'packageSha256': sha(path.read_bytes()), 'links': links,
                         'forensicReadWarning': 'Explicit known-path reads are not authority after failed discovery.',
                         'claims': d['capabilities'], 'lifecycle': s['lifecycle'], 'fixed': fixed,
                         'fixedExactHashMatches': sha(z.read(fixed['path'])) == fixed['sha256'] if fixed.get('path') else None,
                         'badResources': bad, 'projections': projections,
                         'inventoryBinding': {'declared': s['inventory']['sha256'], 'actual': sha(z.read('META-INF/spd/inventory.json'))},
                         'unlisted': sorted(set(z.namelist()) - {e['path'] for e in inv['resources']} - {'META-INF/spd/state.json', 'META-INF/spd/inventory.json'}),
                         'nonNfcInventoryPaths': [e['path'] for e in inv['resources'] if unicodedata.normalize('NFC', e['path']) != e['path']],
                         'spine': spine, 'nodeIds': ids, 'duplicateNodeIds': duplicates, 'xmlParseErrors': parse_errors,
                         'schemaErrorsForKnownFiles': schema_errors, 'documentLinkCandidateSchemaErrors': candidate_errors,
                         'mapping': objs.get('mapping'), 'expected': json.loads((path.parent / 'expected.json').read_text())})
    (OUT / 'fixture-byte-evidence.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    protected = {}
    for base in ['spec', 'schemas', 'tests', 'validator-a/src', 'validator-a/docs', 'validator-a/tests', 'validator-b/spd_validator_b', 'validator-b/docs', 'validator-b/tests']:
        for p in (ROOT / base).rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts:
                protected[p.relative_to(ROOT).as_posix()] = sha(p.read_bytes())
    for base in ['validator-a/reports/golden/validator-a-0.1.0-draft.1.json', 'validator-b/reports/blind-results-with-epubcheck.json']:
        protected[base] = sha((ROOT / base).read_bytes())
    (OUT / 'protected-input-hashes.json').write_text(json.dumps(protected, indent=2) + '\n', encoding='utf-8')
    print(f'Inspected {len(rows)} packages; recorded {len(protected)} protected input hashes.')


if __name__ == '__main__':
    main()
