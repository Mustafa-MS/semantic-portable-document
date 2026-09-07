from __future__ import annotations

import html
import json
import uuid
from dataclasses import dataclass
from pathlib import Path

from harness.util import ROOT, normalize_text, write_json


@dataclass(frozen=True)
class CorpusDocument:
    test_id: str
    title: str
    purpose: str
    lang: str
    direction: str
    body: str


class IdentityRegistry:
    """Persists randomly assigned opaque IDs; IDs are never computed from content or position."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}

    def node(self, fixture_key: str) -> str:
        if fixture_key not in self.data:
            self.data[fixture_key] = "n_" + uuid.uuid4().hex
        return self.data[fixture_key]

    def document(self, fixture_key: str) -> str:
        key = "document:" + fixture_key
        if key not in self.data:
            self.data[key] = "d_" + uuid.uuid4().hex
        return self.data[key]

    def save(self) -> None:
        write_json(self.path, self.data)


def _node(reg: IdentityRegistry, key: str, tag: str, text: str, attrs: str = "") -> str:
    return f'<{tag} data-node-id="{reg.node(key)}" {attrs}>{text}</{tag}>'


def _p(reg: IdentityRegistry, key: str, text: str, attrs: str = "") -> str:
    return _node(reg, key, "p", html.escape(text), attrs)


def _long_text(seed: str, repeats: int = 18) -> str:
    sentence = (
        f"{seed} preserves logical reading order while pagination creates several visible fragments. "
        "Stable identity must remain attached to this paragraph when lines and pages change. "
    )
    return sentence * repeats


def build_documents(reg: IdentityRegistry) -> list[CorpusDocument]:
    n = reg.node

    t01 = f"""
<section data-node-id="{n('T01.section')}"><h1 data-node-id="{n('T01.h1')}">Baseline semantic document</h1>
{_p(reg, 'T01.p1', 'This baseline checks headings, paragraphs, emphasis, links, lists, and explicit page breaks.')}
<p data-node-id="{n('T01.p2')}">A <em>semantic source</em> remains authoritative; visit <a href="https://example.org">the example reference</a>.</p>
<ul data-node-id="{n('T01.list')}"><li data-node-id="{n('T01.li1')}">Persistent identity</li><li data-node-id="{n('T01.li2')}">Logical text order</li></ul>
<div class="page-break"></div>{_p(reg, 'T01.p3', 'This paragraph follows an intentional page break.')}</section>"""

    t02 = f"""<section data-node-id="{n('T02.section')}"><h1 data-node-id="{n('T02.h1')}">Multipage paragraph</h1>
{_p(reg, 'T02.long', _long_text('The long-node experiment', 42))}
{_p(reg, 'T02.tail', 'The preceding single semantic node should map to more than one page fragment.')}</section>"""

    rows = []
    for i in range(1, 29):
        rows.append(
            f'<tr data-node-id="{n(f"T03.r{i}")}"><th data-node-id="{n(f"T03.rh{i}")}" scope="row">R{i}</th>'
            f'<td data-node-id="{n(f"T03.c{i}a")}"><p data-node-id="{n(f"T03.cp{i}")}">Measurement row {i}</p></td>'
            f'<td data-node-id="{n(f"T03.c{i}b")}">{0.800 + i/1000:.3f}</td></tr>'
        )
    t03 = f"""<section data-node-id="{n('T03.section')}"><h1 data-node-id="{n('T03.h1')}">Complex multipage table</h1>
<table data-node-id="{n('T03.table')}"><caption data-node-id="{n('T03.caption')}">Measurements by cohort</caption>
<thead><tr data-node-id="{n('T03.hr')}"><th data-node-id="{n('T03.h1c')}" rowspan="2">Cohort</th><th data-node-id="{n('T03.h2c')}" colspan="2">Result</th></tr>
<tr data-node-id="{n('T03.hr2')}"><th data-node-id="{n('T03.h3c')}">Description</th><th data-node-id="{n('T03.h4c')}">FROC</th></tr></thead><tbody>{''.join(rows)}</tbody></table></section>"""

    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 160" role="img" aria-labelledby="svg-title"><title id="svg-title">Rising three-point trend</title><rect width="400" height="160" fill="#eef4f8"/><polyline points="30,125 170,85 360,30" fill="none" stroke="#176b87" stroke-width="8"/><circle cx="30" cy="125" r="9"/><circle cx="170" cy="85" r="9"/><circle cx="360" cy="30" r="9"/></svg>"""
    t04 = f"""<section data-node-id="{n('T04.section')}"><h1 data-node-id="{n('T04.h1')}">Figures and captions</h1>
{_p(reg, 'T04.p1', 'Figure 1 shows a rising trend and must retain its cross-reference.')}
<figure data-node-id="{n('T04.fig1')}"><img src="assets/sample.png" alt="Three colored bars increasing from left to right"/><figcaption data-node-id="{n('T04.cap1')}">Figure 1. Raster trend summary.</figcaption></figure>
<figure data-node-id="{n('T04.fig2')}">{svg}<figcaption data-node-id="{n('T04.cap2')}">Figure 2. SVG trend line.</figcaption></figure></section>"""

    t05 = f"""<section data-node-id="{n('T05.section')}"><h1 data-node-id="{n('T05.h1')}">Mathematics</h1>
<p data-node-id="{n('T05.p1')}">Inline energy <math xmlns="http://www.w3.org/1998/Math/MathML" data-node-id="{n('T05.eq1')}"><mi>E</mi><mo>=</mo><mi>m</mi><msup><mi>c</mi><mn>2</mn></msup></math> appears in text.</p>
<div class="equation" data-node-id="{n('T05.eq2')}"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><mi>FROC</mi><mo>=</mo><mfrac><mn>906</mn><mn>1000</mn></mfrac></mrow></math><span>(1)</span></div>
{_p(reg, 'T05.p2', 'Equation 1 defines the reported FROC result.')}</section>"""

    t06 = f"""<section data-node-id="{n('T06.section')}"><h1 data-node-id="{n('T06.h1')}">Footnotes and endnotes</h1>
<p data-node-id="{n('T06.p1')}">The first claim<a role="doc-noteref" href="#note-a">1</a> is referenced twice<a role="doc-noteref" href="#note-a">1</a>; another claim has a long note<a role="doc-noteref" href="#note-b">2</a>.</p>
{_p(reg, 'T06.fill', _long_text('Body material separates references from their physical notes', 16))}
<aside id="note-a" role="doc-footnote" data-node-id="{n('T06.note1')}">1. A short repeated footnote.</aside>
<aside id="note-b" role="doc-footnote" data-node-id="{n('T06.note2')}">2. {_long_text('This long note tests placement', 8)}</aside></section>"""

    t07 = f"""<section data-node-id="{n('T07.section')}"><h1 data-node-id="{n('T07.h1')}">Logical order across columns</h1>
{_p(reg, 'T07.intro', 'This introduction is single-column and precedes the two-column section.')}
<div class="columns" data-node-id="{n('T07.columns')}">{_p(reg, 'T07.c1', _long_text('Column content A', 9))}{_p(reg, 'T07.c2', _long_text('Column content B', 9))}
<figure class="span-columns" data-node-id="{n('T07.fig')}"><img src="assets/sample.png" alt="Three rising bars"/><figcaption data-node-id="{n('T07.cap')}">Figure spanning both columns.</figcaption></figure>
{_p(reg, 'T07.c3', 'The logical source order remains independent of column geometry.')}</div>
{_p(reg, 'T07.end', 'This conclusion returns to a single column.')}</section>"""

    t08 = f"""<section data-node-id="{n('T08.section')}"><h1 data-node-id="{n('T08.h1')}">وثيقة عربية تجريبية</h1>
{_p(reg, 'T08.p1', 'هذه وثيقة عربية لاختبار ترتيب يونيكود المنطقي، واتصال الحروف، وعلامات الترقيم العربية؛ والنتيجة ٠٫٩٠٦.')}
<table data-node-id="{n('T08.table')}"><caption data-node-id="{n('T08.cap')}">جدول النتائج</caption><tr data-node-id="{n('T08.r1')}"><th data-node-id="{n('T08.c1')}">المقياس</th><th data-node-id="{n('T08.c2')}">القيمة</th></tr><tr data-node-id="{n('T08.r2')}"><td data-node-id="{n('T08.c3')}">الدقة</td><td data-node-id="{n('T08.c4')}">٩٠٫٦٪</td></tr></table>
<figure data-node-id="{n('T08.fig')}"><img src="assets/sample.png" alt="ثلاثة أعمدة متزايدة"/><figcaption data-node-id="{n('T08.fcap')}">الشكل ١. اتجاه تصاعدي.</figcaption></figure>
<aside role="doc-footnote" data-node-id="{n('T08.note')}">١. ملاحظة عربية قصيرة.</aside></section>"""

    t09 = f"""<section data-node-id="{n('T09.section')}"><h1 data-node-id="{n('T09.h1')}">نص عربي وإنجليزي Mixed RTL/LTR</h1>
{_p(reg, 'T09.p1', 'هذه النتيجة FROC = 0.906 مقارنة بالطريقة السابقة.')}
{_p(reg, 'T09.p2', 'شغّل النموذج Model-X (v2.1) على https://example.org/run?id=42، ثم قارن ١٢٣ مع 123.')}
<p data-node-id="{n('T09.p3')}">المعادلة <math xmlns="http://www.w3.org/1998/Math/MathML"><mi>x</mi><mo>=</mo><mn>0.906</mn></math> مذكورة في المرجع [Smith 2025].</p></section>"""

    t10 = f"""<article data-node-id="{n('T10.article')}"><h1 data-node-id="{n('T10.h1')}">A compact academic paper</h1>
<section data-node-id="{n('T10.abstract')}"><h2 data-node-id="{n('T10.ah')}">Abstract</h2>{_p(reg, 'T10.ap', 'We evaluate a semantic-first document architecture using fixed-rendition mapping.')}</section>
<section data-node-id="{n('T10.methods')}"><h2 data-node-id="{n('T10.mh')}">Methods</h2>{_p(reg, 'T10.mp', 'Stable node identities were preserved during a targeted result update [1].')}</section>
<section data-node-id="{n('T10.results')}"><h2 data-node-id="{n('T10.rh')}">Results</h2>
<p data-node-id="{n('T10.resultp')}">Table 4 reports the exact experimental result: FROC improved from baseline to 0.901.</p>
<table data-node-id="{n('T10.table4')}"><caption data-node-id="{n('T10.tcap')}">Table 4. Primary result.</caption><tr data-node-id="{n('T10.trh')}"><th data-node-id="{n('T10.th1')}">Measure</th><th data-node-id="{n('T10.th2')}">Value</th></tr><tr data-node-id="{n('T10.tr1')}"><td data-node-id="{n('T10.tc1')}">FROC</td><td data-node-id="{n('T10.froc')}">0.901</td></tr></table>
<figure data-node-id="{n('T10.fig')}"><img src="assets/sample.png" alt="Primary result bars"/><figcaption data-node-id="{n('T10.fcap')}">Figure 1. Primary result visualization.</figcaption></figure></section>
<section data-node-id="{n('T10.refs')}"><h2 data-node-id="{n('T10.bh')}">References</h2><ol data-node-id="{n('T10.bib')}"><li data-node-id="{n('T10.cite1')}">[1] Example Research Group. Semantic document experiments. 2025.</li></ol></section></article>"""

    t11 = f"""<article data-node-id="{n('T11.article')}"><header data-node-id="{n('T11.header')}">EXPERIMENTAL AGREEMENT - PAGE HEADER</header><h1 data-node-id="{n('T11.h1')}">Research Services Agreement</h1>
<ol class="clauses" data-node-id="{n('T11.clauses')}"><li data-node-id="{n('T11.c1')}">Definitions.<ol><li data-node-id="{n('T11.c1a')}">“Document” means the semantic source and bound rendition.</li><li data-node-id="{n('T11.c1b')}">“Revision” means one immutable semantic state.</li></ol></li><li data-node-id="{n('T11.c2')}">Obligations. Each party shall preserve identifiers.</li></ol>
<table data-node-id="{n('T11.table')}"><tr data-node-id="{n('T11.r1')}"><th data-node-id="{n('T11.a')}">Party A</th><th data-node-id="{n('T11.b')}">Party B</th></tr><tr data-node-id="{n('T11.r2')}"><td data-node-id="{n('T11.sig1')}">Signature: __________</td><td data-node-id="{n('T11.sig2')}">Signature: __________</td></tr></table>
<div class="page-break"></div>{_p(reg, 'T11.final', 'This clause begins on a fixed new page and tests page-oriented use.')}
<footer data-node-id="{n('T11.footer')}">CONFIDENTIAL - PAGE FOOTER</footer></article>"""

    t12 = f"""<main data-node-id="{n('T12.main')}"><h1 data-node-id="{n('T12.h1')}">Accessibility stress document</h1>
<nav aria-label="Document topics" data-node-id="{n('T12.nav')}"><ul data-node-id="{n('T12.list')}"><li data-node-id="{n('T12.li1')}"><a href="#topic">Topic</a></li></ul></nav>
<section id="topic" data-node-id="{n('T12.s1')}"><h2 data-node-id="{n('T12.h2')}">Structured topic</h2><h3 data-node-id="{n('T12.h3')}">Detailed finding</h3>
<p data-node-id="{n('T12.p1')}">The <abbr title="free-response receiver operating characteristic">FROC</abbr> metric is explained <span lang="fr">en français</span> and in English.</p>
<img class="decorative" src="assets/decorative.png" alt=""/><figure data-node-id="{n('T12.fig')}"><img src="assets/sample.png" alt="Three bars showing an increasing result"/><figcaption data-node-id="{n('T12.cap')}">Meaningful result figure.</figcaption></figure>
<table data-node-id="{n('T12.table')}"><caption data-node-id="{n('T12.tcap')}">Accessible comparison</caption><tr data-node-id="{n('T12.r1')}"><th data-node-id="{n('T12.th1')}" scope="col">System</th><th data-node-id="{n('T12.th2')}" scope="col">Score</th></tr><tr data-node-id="{n('T12.r2')}"><th data-node-id="{n('T12.rh')}" scope="row">Prototype</th><td data-node-id="{n('T12.td')}">0.906</td></tr></table></section></main>"""

    return [
        CorpusDocument("T01", "Basic Semantic Document", "Baseline semantic/render/mapping behavior", "en", "ltr", t01),
        CorpusDocument("T02", "Long Multipage Paragraphs", "One node to multiple fixed fragments", "en", "ltr", t02),
        CorpusDocument("T03", "Complex Tables", "Persistent table/cell identity and fragmentation", "en", "ltr", t03),
        CorpusDocument("T04", "Figures and Captions", "Figure identity and cross-reference preservation", "en", "ltr", t04),
        CorpusDocument("T05", "Mathematics", "MathML rendering and equation identity", "en", "ltr", t05),
        CorpusDocument("T06", "Footnotes and Endnotes", "Logical relationships versus physical placement", "en", "ltr", t06),
        CorpusDocument("T07", "Multi-column Layout", "Logical order versus column geometry", "en", "ltr", t07),
        CorpusDocument("T08", "Arabic Document", "RTL as a first-class baseline", "ar", "rtl", t08),
        CorpusDocument("T09", "Mixed Arabic/English", "Mixed-direction logical/visual mapping", "ar", "rtl", t09),
        CorpusDocument("T10", "Academic Paper", "Realistic research structure and revision fixture", "en", "ltr", t10),
        CorpusDocument("T11", "Business/Legal Document", "Exact page-oriented structure", "en", "ltr", t11),
        CorpusDocument("T12", "Accessibility Stress", "Semantic versus fixed accessibility", "en", "ltr", t12),
    ]


CSS = r"""
@page { size: A4; margin: 18mm 17mm 20mm; }
@page { @bottom-center { content: counter(page); font-size: 9pt; color: #555; } }
html { font-family: "Noto Sans Arabic", "Segoe UI", Arial, sans-serif; color: #17242b; line-height: 1.48; }
body { margin: 0; font-size: 11pt; }
h1 { color: #174d62; font-size: 24pt; border-bottom: 2px solid #7cb8c9; padding-bottom: 5mm; }
h2 { color: #215f72; break-after: avoid; }
h3 { color: #37788a; break-after: avoid; }
p { widows: 3; orphans: 3; }
a { color: #075d9c; }
table { border-collapse: collapse; width: 100%; margin: 7mm 0; }
thead { display: table-header-group; }
th, td { border: 0.5pt solid #617984; padding: 2.5mm; vertical-align: top; }
th { background: #dfeef2; }
figure { margin: 7mm auto; break-inside: avoid; text-align: center; }
figure img, figure svg { max-width: 80%; max-height: 75mm; }
figcaption, caption { font-weight: 600; margin-top: 2mm; }
.page-break { break-before: page; }
.columns { column-count: 2; column-gap: 12mm; }
.span-columns { column-span: all; }
.equation { display: flex; justify-content: center; gap: 10mm; align-items: center; }
aside[role="doc-footnote"] { border-top: 0.5pt solid #81939a; margin-top: 5mm; padding-top: 2mm; font-size: 9pt; }
header, footer { color: #60717a; font-size: 8pt; letter-spacing: .08em; }
[dir="rtl"] { text-align: start; }
"""


def _xhtml(doc: CorpusDocument, document_id: str, revision_id: str) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="{doc.lang}" xml:lang="{doc.lang}" dir="{doc.direction}">
<head>
  <meta charset="utf-8" />
  <meta name="document-id" content="{document_id}" />
  <meta name="revision-id" content="{revision_id}" />
  <title>{html.escape(doc.title)}</title>
  <link rel="stylesheet" type="text/css" href="style.css" />
</head>
<body>{doc.body}</body>
</html>
'''


def create_corpus(root: Path = ROOT) -> list[dict[str, str]]:
    sources = root / "corpus" / "sources"
    expected = root / "corpus" / "expected"
    assets = sources / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    expected.mkdir(parents=True, exist_ok=True)
    reg = IdentityRegistry(expected / "identities.json")
    revision_registry_path = expected / "revisions.json"
    revisions = json.loads(revision_registry_path.read_text(encoding="utf-8")) if revision_registry_path.exists() else {}

    # Generated locally to avoid external assets and network-dependent experiments.
    from PIL import Image, ImageDraw

    sample = Image.new("RGB", (900, 420), "#eef4f8")
    draw = ImageDraw.Draw(sample)
    for x, height, color in [(130, 120, "#81b29a"), (360, 230, "#3d8c9f"), (590, 330, "#174d62")]:
        draw.rectangle((x, 370 - height, x + 150, 370), fill=color)
    sample.save(assets / "sample.png")
    decorative = Image.new("RGBA", (500, 20), (124, 184, 201, 255))
    decorative.save(assets / "decorative.png")
    (sources / "style.css").write_text(CSS, encoding="utf-8")

    manifest: list[dict[str, str]] = []
    for doc in build_documents(reg):
        revisions.setdefault(doc.test_id, "r_" + uuid.uuid4().hex)
        document_id = reg.document(doc.test_id)
        source_path = sources / f"{doc.test_id}.xhtml"
        source_path.write_text(_xhtml(doc, document_id, revisions[doc.test_id]), encoding="utf-8")
        manifest.append({
            "test_id": doc.test_id,
            "title": doc.title,
            "purpose": doc.purpose,
            "source": str(source_path.relative_to(root)).replace("\\", "/"),
            "document_id": document_id,
            "revision_id": revisions[doc.test_id],
            "lang": doc.lang,
            "dir": doc.direction,
        })
    reg.save()
    write_json(revision_registry_path, revisions)
    write_json(expected / "corpus_manifest.json", manifest)
    return manifest

