"""Independent namespace/token-based passive inspection. Never fetch or rewrite."""
from __future__ import annotations

import posixpath
import unicodedata
from urllib.parse import unquote, urlsplit

import tinycss2
from lxml import etree

from .models import Outcome, ResourceLimitExceeded
from .xmlutil import XMLValidationError, parse_xml

SVG = 'http://www.w3.org/2000/svg'
XHTML = 'http://www.w3.org/1999/xhtml'
MATH = 'http://www.w3.org/1998/Math/MathML'


def url_value(value):
    return value.strip(' \t\r\n\f').replace('\t', '').replace('\r', '').replace('\n', '')


class Inspector:
    def __init__(self, package, report):
        self.package, self.report = package, report
        self.xml = {}
        self.edges = {}

    def fail(self, path, *ids, evidence=''):
        for rid in ids:
            self.report.add(rid, Outcome.FAIL, 'passive content/profile violation', resource=path, evidence=evidence)

    def reference(self, path, value, role='other', svg=False, hyperlink=False, source=None):
        value = url_value(value)
        try:
            parts = urlsplit(value)
        except ValueError:
            self.fail(path, 'SPD-SEC-008', evidence=value)
            return
        scheme = parts.scheme.lower()
        if hyperlink and scheme in {'http', 'https'} and parts.netloc:
            return
        ids = set()
        if scheme in {'javascript', 'vbscript'}:
            ids.add('SPD-SEC-001')
        forbidden = bool(scheme or parts.netloc or value.startswith(('/', '\\')))
        if forbidden:
            ids.add('SPD-SEC-008')
            if not hyperlink:
                ids.add('SPD-SEC-003')
                specific = {'font': 'SPD-SEC-004', 'stylesheet': 'SPD-SEC-005', 'image': 'SPD-SEC-006'}.get(role)
                if specific:
                    ids.add(specific)
            if svg:
                ids.add('SPD-SEC-007')
            self.fail(path, *sorted(ids), evidence=value)
            return
        try:
            decoded = unquote(parts.path, errors='strict')
            fragment = unquote(parts.fragment, errors='strict')
        except (ValueError, UnicodeDecodeError):
            self.fail(path, 'SPD-SEC-008', evidence=value)
            return
        target = posixpath.normpath(posixpath.join(posixpath.dirname(path), decoded)) if decoded else path
        unsafe = parts.query or '\\' in decoded or ':' in decoded or decoded.startswith('/') or target.startswith('../') or target == '..' or unicodedata.normalize('NFC', target) != target
        if unsafe or not self.package.exists(target):
            self.fail(path, 'SPD-SEC-008', evidence=value)
            return
        if fragment and (target not in self.xml or not self.xml[target].xpath('//*[@id=$id]', id=fragment)):
            self.fail(path, 'SPD-SEC-008', evidence=value)
        if not hyperlink and source is not None:
            self.edges.setdefault(source, set()).add(target + ('#' + fragment if fragment else ''))

    def css(self, path, text, svg=False):
        # Component-value tokens preserve nested blocks/functions and decode escapes.
        def walk(tokens, role='image', depth=0, strings=False):
            if depth > 128:
                raise ResourceLimitExceeded('CSS nesting inspection budget exceeded')
            import_pending = False
            font_pending = False
            for token in tokens:
                typ = token.type
                if typ in {'whitespace', 'comment'}:
                    continue
                if typ == 'at-keyword':
                    import_pending = token.lower_value == 'import'
                    font_pending = token.lower_value == 'font-face'
                elif typ == 'ident' and token.lower_value in {'behavior', '-moz-binding'}:
                    self.fail(path, 'SPD-SEC-001')
                elif typ == 'url' or typ == 'string' and (import_pending or strings):
                    self.reference(path, token.value, 'stylesheet' if import_pending else role, svg, source=path if import_pending else None)
                    import_pending = False
                elif typ == 'function':
                    name = token.lower_name
                    if strings and name in {'var', 'attr', 'env'}:
                        self.report.add('SPD-SEC-008', Outcome.NOT_TESTED, 'dynamic string resource consumer not resolved', resource=path)
                    if name in {'url', 'src'}:
                        args = [x for x in token.arguments if x.type not in {'whitespace', 'comment'}]
                        if len(args) == 1 and args[0].type in {'string', 'url'}:
                            self.reference(path, args[0].value, 'stylesheet' if import_pending else role, svg, source=path if import_pending else None)
                        else:
                            self.report.add('SPD-SEC-008', Outcome.NOT_TESTED, 'dynamic URL consumer requires unresolved substitution evaluation', resource=path)
                        import_pending = False
                    elif name == 'local' and role == 'font':
                        self.fail(path, 'SPD-SEC-004')
                    elif name == 'expression':
                        self.fail(path, 'SPD-SEC-001')
                    else:
                        walk(token.arguments, role, depth + 1, name in {'image', 'image-set', '-webkit-image-set'})
                elif hasattr(token, 'content'):
                    walk(token.content, 'font' if font_pending else role, depth + 1)
                    font_pending = False
                    import_pending = False
                elif typ == 'error':
                    self.fail(path, 'SPD-SEC-005', evidence=token.message)
                elif typ == 'literal' and token.value == ';':
                    import_pending = False
                    font_pending = False
        walk(tinycss2.parse_component_value_list(text), depth=0)

    def inspect_xml(self, path, root):
        for pi in root.getroottree().xpath('//processing-instruction("xml-stylesheet")'):
            try:
                attrs = etree.fromstring(('<style ' + pi.text + '/>').encode()).attrib
                if attrs.get('href'):
                    self.reference(path, attrs['href'], 'stylesheet')
            except etree.XMLSyntaxError:
                self.fail(path, 'SPD-SEC-005')
        for element in root.iter():
            if not isinstance(element.tag, str):
                continue
            q = etree.QName(element)
            name = q.localname.lower()
            if q.namespace not in {SVG, XHTML, MATH}:
                continue
            svg = q.namespace == SVG or any(etree.QName(a).namespace == SVG for a in element.iterancestors())
            if name == 'script':
                self.fail(path, 'SPD-SEC-001', *(['SPD-SEC-007'] if svg else []))
            if name in {'iframe', 'object', 'embed', 'applet'}:
                self.fail(path, 'SPD-SEC-002', 'SPD-PASS-002')
            if name in {'form', 'base'} or element.get('{http://www.w3.org/XML/1998/namespace}base') is not None:
                self.fail(path, 'SPD-PASS-002')
            if name == 'foreignobject' and svg:
                self.fail(path, 'SPD-SEC-007', 'SPD-PASS-002')
            if name == 'canvas':
                self.fail(path, 'SPD-PASS-002')
            if name in {'input', 'button'}:
                label = element.get('aria-label') or element.get('aria-labelledby') or (''.join(element.itertext()).strip() if name == 'button' else None)
                if not label and element.get('id'):
                    label = root.xpath('//*[local-name()="label"][@for=$id]', id=element.get('id'))
                forbidden = {'form', 'formaction', 'formenctype', 'formmethod', 'formtarget', 'formnovalidate', 'command', 'commandfor', 'popovertarget', 'popovertargetaction'}
                bad = element.get('disabled') is None or not label or bool(forbidden.intersection(element.attrib))
                bad |= element.get('type', '').lower() in {'password', 'file', 'submit', 'image', 'reset'}
                bad |= name == 'button' and element.get('type', 'submit').lower() != 'button'
                bad |= name == 'input' and element.get('value') is None and element.get('type') not in {'checkbox', 'radio'}
                if bad:
                    self.fail(path, 'SPD-PASS-002')
            if name == 'meta' and element.get('http-equiv', '').lower() == 'refresh':
                self.fail(path, 'SPD-SEC-003', 'SPD-PASS-002')
            if 'autoplay' in element.attrib:
                self.fail(path, 'SPD-PASS-003')
            rel = set(element.get('rel', '').lower().split())
            if 'ping' in element.attrib or rel.intersection({'prefetch', 'preconnect', 'dns-prefetch', 'prerender'}):
                self.fail(path, 'SPD-SEC-003')
            if name == 'style':
                self.css(path, ''.join(element.itertext()), svg)
            for attr, value in element.attrib.items():
                local = etree.QName(attr).localname.lower()
                if local.startswith('on'):
                    self.fail(path, 'SPD-SEC-001', *(['SPD-SEC-007'] if svg else []))
                if local == 'style' or (svg and local in {'fill', 'stroke', 'filter', 'clip-path', 'mask', 'cursor', 'marker-start', 'marker-mid', 'marker-end'}):
                    self.css(path, value, svg)
                if local not in {'href', 'src', 'srcset', 'poster', 'data', 'background'}:
                    continue
                if name == 'base':
                    continue  # Prohibited override is not a rendered resource.
                hyperlink = local == 'href' and (name in {'a', 'area'} or (q.namespace == MATH and name != 'mglyph'))
                role = 'stylesheet' if name == 'link' and 'stylesheet' in rel else 'image' if name in {'img', 'image', 'use', 'feimage', 'mglyph', 'audio', 'video', 'source', 'track'} or local in {'poster', 'background'} else 'other'
                if name == 'link' and rel.intersection({'preload', 'modulepreload'}):
                    role = {'font': 'font', 'style': 'stylesheet', 'image': 'image'}.get(element.get('as'), role)
                values = [part.strip().split()[0] for part in value.split(',') if part.strip()] if local == 'srcset' else [value]
                for candidate in values:
                    source = None
                    if svg and not hyperlink:
                        owner = next((a.get('id') for a in [element, *element.iterancestors()] if a.get('id')), None)
                        source = path + ('#' + owner if owner else '')
                    self.reference(path, candidate, role, svg, hyperlink, source)

    def run(self):
        css_paths = set()
        # Parse content by namespace, not filename or embedding assumptions.
        for path in sorted(self.package.paths):
            if path.endswith('.css'):
                css_paths.add(path)
            data = self.package.read(path)
            if not (data.lstrip().startswith(b'<') or data.startswith((b'\xef\xbb\xbf', b'\xff\xfe', b'\xfe\xff', b'\x00<', b'<\x00'))):
                continue
            if len(data) > self.package.limits.max_xml_bytes:
                raise ResourceLimitExceeded('XML inspection byte budget exceeded')
            try:
                root = parse_xml(data, resource=path)
            except XMLValidationError:
                continue  # Existing XML/EPUB rules own malformed documents.
            self.xml[path] = root
            if etree.QName(root).namespace == 'http://www.idpf.org/2007/opf':
                for item in root.xpath('//*[local-name()="item"]'):
                    if item.get('media-type', '').lower() in {'application/javascript', 'text/javascript', 'application/ecmascript', 'text/ecmascript'}:
                        self.fail(path, 'SPD-SEC-001')
                for item in root.xpath('//*[local-name()="item"][@media-type="text/css"]'):
                    href = item.get('href', '')
                    if not urlsplit(href).scheme:
                        css_paths.add(posixpath.normpath(posixpath.join(posixpath.dirname(path), unquote(href))))
        for path, root in self.xml.items():
            self.inspect_xml(path, root)
        for path in sorted(css_paths & self.package.paths):
            try:
                self.css(path, self.package.read(path).decode('utf-8-sig'))
            except UnicodeDecodeError:
                self.fail(path, 'SPD-SEC-005')
        # Iterative graph traversal bounds stack use; hyperlink edges are excluded.
        done = set()
        for root in self.edges:
            pending = [(root, False)]
            active = set()
            while pending:
                node, leave = pending.pop()
                if leave:
                    active.discard(node)
                    done.add(node)
                elif node in active:
                    self.fail(root.split('#')[0], 'SPD-SEC-008', evidence='resource cycle')
                elif node not in done:
                    active.add(node)
                    pending.append((node, True))
                    pending.extend((child, False) for child in self.edges.get(node, ()))


def validate_passive(package, report):
    Inspector(package, report).run()
