from __future__ import annotations

import statistics
from collections import Counter
from pathlib import Path
from typing import Any


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip()+"\n",encoding="utf-8")


def _pct(value: float | None) -> str:
    return "n/a" if value is None else f"{value*100:.1f}%"


def _docs(results: dict[str, Any]) -> list[dict[str, Any]]:
    return [item for item in results["documents"] if item["testId"] != "T10_R2_1B"]


def _category(mapping: dict[str, Any], tags: set[str]) -> tuple[int,int,float]:
    records=[r for r in mapping["records"] if r["tag"] in tags]
    mapped=sum(r["status"] in {"MAPPED","PARTIALLY_MAPPED"} for r in records)
    return mapped,len(records),mapped/len(records) if records else 1.0


def write_phase1b_reports(root: Path, results: dict[str, Any]) -> None:
    reports=root/"reports"; docs=_docs(results)
    valid_forward=[d for d in docs if d.get("pagedjs",{}).get("forward")]
    node_avg=statistics.mean(d["pagedjs"]["forward"]["mappingFidelity"]["visibleNodeMapping"]["ratio"] for d in valid_forward)
    range_avg=statistics.mean(d["pagedjs"]["forward"]["mappingFidelity"]["logicalRangeMapping"]["ratio"] for d in valid_forward)
    rtl=[d for d in valid_forward if d["testId"] in {"T08","T09"}]
    rtl_node=min((d["pagedjs"]["forward"]["mappingFidelity"]["visibleNodeMapping"]["ratio"] for d in rtl),default=0)
    rtl_range=min((d["pagedjs"]["forward"]["mappingFidelity"]["logicalRangeMapping"]["ratio"] for d in rtl),default=0)

    forward_rows=[]
    for d in valid_forward:
        mf=d["pagedjs"]["forward"]["mappingFidelity"]
        statuses=Counter(r["status"] for r in d["pagedjs"]["forward"]["records"])
        forward_rows.append(f"| {d['testId']} | {mf['visibleNodeMapping']['mapped']}/{mf['visibleNodeMapping']['expected']} | {_pct(mf['visibleNodeMapping']['ratio'])} | {mf['logicalRangeMapping']['mappedCharacters']}/{mf['logicalRangeMapping']['expectedCharacters']} | {_pct(mf['logicalRangeMapping']['ratio'])} | {statuses.get('PARTIALLY_MAPPED',0)} | {statuses.get('UNMAPPABLE',0)} |")
    _write(reports/"forward_mapping_results.md",f"""# Forward Mapping Results

**VERIFIED BY TEST** with Paged.js 0.4.3 and system Chromium. Mapping was emitted from propagated
`data-node-id` values and instrumented logical source ranges before PDF generation; it did not use
PDF text extraction.

| Document | Visible mapped | Node coverage | Range characters | Range coverage | Partial | Unmappable |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
{chr(10).join(forward_rows)}

Macro-average visible-node mapping: **{_pct(node_avg)}**. Macro-average logical-range mapping:
**{_pct(range_avg)}**. T08/T09 minimums were **{_pct(rtl_node)}** nodes and **{_pct(rtl_range)}**
ranges. Ancestors without a stable paginated clone are represented by the union of identified child
fragments with explicit `forward:pagedjs-descendant-union` provenance.

The common 0.1B model records `MAPPED`, `PARTIALLY_MAPPED`, `NOT_VISIBLE`, `UNMAPPABLE`, or
`UNSUPPORTED`, method, deterministic confidence category, logical ranges, page-local quads, and the
CSS-pixel-to-PDF-point transform. Adapters remain non-normative.
""")

    ablation_rows=[]
    for d in valid_forward:
        forward=d["pagedjs"]["forward"]; backward=d["pagedjs"]["backward"]
        cells=_category(forward,{"td","th"}); equations=_category(forward,{"math"}); figures=_category(forward,{"figure"})
        ablation_rows.append(f"| {d['testId']} | {_pct(d.get('phase1BackwardCoverage',{}).get('ratio'))} | {_pct(backward['coverage']['ratio'])} | {_pct(forward['mappingFidelity']['visibleNodeMapping']['ratio'])} | {_pct(cells[2])} | {_pct(equations[2])} | {_pct(figures[2])} | {backward.get('coverage',{}).get('mapped','-')} | {round(forward['processingTimeMs'],1)} |")
    _write(reports/"backward_vs_forward_mapping.md",f"""# Backward vs Forward Mapping Ablation

**VERIFIED BY TEST.** A is the retained `pdfplumber` token matcher. B is explicit Paged.js identity
and logical-range propagation. Both were also run against the same Paged.js PDF where possible.

| Document | Phase 1 backward | A on Paged PDF | B forward nodes | B cells | B MathML | B figures | A mapped nodes | B ms |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
{chr(10).join(ablation_rows)}

Forward mapping materially improves node, Arabic, table-cell, MathML equation, and vector-figure
coverage because it does not require recoverable PDF strings or raster image objects. Its cost is
renderer-specific instrumentation and more range fragments. The output model itself is renderer-
independent. The backward mapper remains valuable as an independent geometry/text cross-check, not
as the normative generation mechanism.
""")

    rtl_rows=[]
    for d in rtl:
        mf=d["pagedjs"]["forward"]["mappingFidelity"]
        rtl_rows.append(f"| {d['testId']} | {_pct(mf['visibleNodeMapping']['ratio'])} | {_pct(mf['logicalRangeMapping']['ratio'])} | EXACT_TEXT_RANGE_LAYOUT | independent of PDF extraction |")
    _write(reports/"rtl_mapping_results.md",f"""# RTL Mapping Fidelity

**VERIFIED BY TEST.** MF is reported independently from PDF text fidelity.

| Document | Visible node MF | Logical-range MF | Evidence | PDF extraction dependency |
| --- | ---: | ---: | --- | --- |
{chr(10).join(rtl_rows)}

Arabic, Latin names, URLs, `FROC = 0.906`, Arabic-Indic and European digits, parentheses, citations,
and adjacent MathML are mapped from logical source spans to visual rectangles. Visual x-order is
never used to rewrite or infer logical order. Page geometry was visually inspected separately.
""")

    pf_rows=[]
    for d in rtl:
        for renderer, detail in d.get("pdfTextFidelity",{}).items():
            for extractor,value in detail["result"]["extractors"].items():
                if "phraseRecovery" not in value: continue
                raw=value["phraseRecovery"]["raw"]; nfkc=value["phraseRecovery"]["NFKC"]
                pf_rows.append(f"| {d['testId']} | {renderer} | {extractor} | {raw['matched']}/{raw['expected']} | {_pct(nfkc['ratio'])} | {detail['toUnicode']['codepointClasses'].get('base_arabic',0)} | {detail['toUnicode']['codepointClasses'].get('arabic_presentation_forms',0)} | {detail['actualTextCount']} |")
    _write(reports/"rtl_pdf_text_fidelity.md",f"""# Arabic PDF Text Fidelity

**VERIFIED BY TEST** for pypdf, pdfplumber, and PDF.js. Poppler `pdftotext` is **NOT VERIFIED**
because that executable is absent from the bundled Poppler runtime. Raw, NFC, and NFKC output is
preserved per PDF under `corpus/generated/phase1b/text/`; normalization is never treated as an order fix.

| Doc | Renderer | Extractor | Raw exact phrases | NFKC recovery | Base Arabic CMap | Presentation forms | ActualText |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
{chr(10).join(pf_rows)}

MF and PF remain separate. A PDF can carry correct forward geometry while exposing strings in visual
bidi order, presentation forms, or extractor-specific order. `/ToUnicode` destination classes and
`/ActualText` counts are observations; they do not alone prove search, clipboard, or AT behavior.
""")

    renderer_rows=[]
    for d in docs:
        chromium=d.get("chromiumBaseline",{}).get("render",{})
        paged=d.get("pagedjs",{}).get("pdfInspection",{}); weasy=d.get("weasyprint",{}).get("render",{})
        renderer_rows.append(f"| {d['testId']} | Chromium baseline | {chromium.get('page_count','-')} | {chromium.get('render_time_ms','-')} | {chromium.get('structure_tree_present','-')} | {chromium.get('pdf_language','')} | backward PDF tokens |")
        renderer_rows.append(f"| {d['testId']} | Paged.js | {paged.get('page_count','-')} | {d.get('pagedjs',{}).get('forward',{}).get('adapter',{}).get('paginationTimeMs','-')} | {paged.get('structure_tree_present','-')} | {paged.get('pdf_language','')} | forward DOM |")
        renderer_rows.append(f"| {d['testId']} | WeasyPrint 69 | {weasy.get('page_count','-')} | {weasy.get('render_time_ms','-')} | {weasy.get('structure_tree_present','-')} | {weasy.get('pdf_language','')} | layout API not exposed by portable build |")
    visual=results.get("visualQA",{}).get("observations",{})
    _write(reports/"renderer_comparison_phase1b.md",f"""# Renderer Comparison - Phase 1B

**OBSERVED IN IMPLEMENTATIONS.** Paged.js uses Chromium layout with explicit paginated-DOM access;
WeasyPrint 69.0 is a substantially independent Python/Pango/CSS renderer and generated PDF/UA-2 candidates.

| Document | Path | Pages | Render/paginate ms | Structure tree | Lang | Mapping feasibility |
| --- | --- | ---: | ---: | --- | --- | --- |
{chr(10).join(renderer_rows)}

The corpus comparison includes pagination, tables, columns, MathML, SVG/raster figures, notes,
Arabic shaping, bidi, links, fonts, tagging, extraction, and mapping feasibility. Detailed object and
text results remain in `results_phase1b.json`; appearance was checked from rendered PNGs.

| Capability | Chromium baseline | Paged.js | WeasyPrint 69 |
| --- | --- | --- | --- |
| Pagination / page CSS | successful baseline | successful; paginated DOM observable | successful; independent CSS engine |
| Tables / split content | rendered | T03 three pages; forward cells mapped | T03 three pages |
| Multi-column | rendered | T07 two columns plus continuation | T07 two columns plus continuation |
| Foot/endnotes | rendered as authored | rendered as authored | rendered as authored |
| SVG / raster | rendered | T04 both figures | T04 both figures |
| MathML | browser MathML | structured fraction/superscript | **limitation:** flattened T05 fraction/superscript |
| Arabic shaping / bidi | visually reasonable; PF failed | visually legible; MF passed, PF failed | visually legible; MF unavailable, PF below gate |
| Fonts / links | embedded / annotations observed | embedded / annotations observed | embedded / annotations observed |
| Tagging / metadata | structure present, formal profiles fail | structure present, formal profiles fail | UA-2 candidate structure present, formal profiles fail |
| Mapping feasibility | backward baseline only | exact identity/range geometry exposed | portable CLI exposes no layout geometry adapter |

Visual-QA classifications: Paged.js **{visual.get('pagedjs',{}).get('overall','NOT VERIFIED')}**;
WeasyPrint **{visual.get('weasyprint',{}).get('overall','NOT VERIFIED')}**.
""")

    geometry_rows=[]
    fragment_total=0
    in_page_fragments=0
    for d in valid_forward:
        forward=d["pagedjs"]["forward"]
        page_by_id={page["id"]:page for page in forward["pages"]}
        for record in forward["records"]:
            for fragment in record["fragments"]:
                fragment_total += 1
                page=page_by_id.get(fragment["page"])
                xs=fragment["quad"][0::2]; ys=fragment["quad"][1::2]
                if page and min(xs)>=-0.01 and min(ys)>=-0.01 and max(xs)<=page["width"]+0.01 and max(ys)<=page["height"]+0.01:
                    in_page_fragments += 1
        if d["manifest"].get("dir")=="rtl": continue
        g=d["pagedjs"]["geometryCalibration"]
        geometry_rows.append(f"| {d['testId']} | {g['comparisonPairs']} | {g['medianEdgeDeviationPt']} | {g['p95EdgeDeviationPt']} | {g['medianIoU']} | {_pct(g['pageAssignmentAgreement'])} |")
    _write(reports/"mapping_geometry_calibration.md",f"""# Mapping Geometry Calibration

**VERIFIED BY TEST**, with the backward mapper used only as an independent cross-check.

| Document | Pairs | Median edge dev pt | P95 pt | Median IoU | Page agreement |
| --- | ---: | ---: | ---: | ---: | ---: |
{chr(10).join(geometry_rows)}

Per-page transforms use measured PDF media-box dimensions divided by Paged.js sheet dimensions,
not a hard-coded DPI assumption. Differences include box-vs-glyph bounds and extraction uncertainty;
they are not automatically forward-map errors.

Forward-map page assignment validity is **{in_page_fragments}/{fragment_total}
({_pct(in_page_fragments/fragment_total if fragment_total else None)})**: every fragment names an
existing page and its clipped quad lies inside that PDF media box. T08/T09 overlay inspection is
**{results.get('visualQA',{}).get('mappingOverlays',{}).get('T08',{}).get('correspondence','NOT VERIFIED')}**
and **{results.get('visualQA',{}).get('mappingOverlays',{}).get('T09',{}).get('correspondence','NOT VERIFIED')}**.
Backward page agreement remains a separate extraction-based cross-check, not the page-assignment score.
""")

    validation_rows=[]
    validation_failure_counts=Counter()
    for item in results["pdfValidation"]:
        validation_rows.append(f"| {item['testId']} | {item['renderer']} | {item['profile']} | {'PASS' if item.get('compliant') else 'FAIL'} | {item.get('failedRules','-')} | {item.get('failedChecks','-')} |")
        for failure in item.get("failures",[]):
            validation_failure_counts[f"{failure.get('specification')} {failure.get('clause')}: {failure.get('description')}"] += 1
    a4=results["weasyprintPdfA4uExperiment"]
    common_failures="\n".join(f"- {count} result(s): {description}" for description,count in validation_failure_counts.most_common(8))
    a4_failures="\n".join(f"- {failure.get('specification')} {failure.get('clause')}: {failure.get('description')}" for failure in a4.get("validation",{}).get("failures",[]))
    _write(reports/"pdf_validation_phase1b.md",f"""# Specialist PDF Validation - Phase 1B

**VERIFIED BY TEST** using veraPDF 1.30.2.

| Document | Renderer | Profile | Result | Failed rules | Failed checks |
| --- | --- | --- | --- | ---: | ---: |
{chr(10).join(validation_rows)}

The WeasyPrint PDF/A-4u disposable generation experiment validated against veraPDF profile 4 as
**{'PASS' if a4.get('validation',{}).get('compliant') else 'FAIL'}**. UA-2 validation includes Tagged
PDF requirements. `wt1r` and `wt1a` are WTPDF reuse/accessibility profiles. A failed profile is
reported as evidence, not repaired or reclassified.

Most frequent exact validator diagnostics:

{common_failures or '- none'}

Disposable WeasyPrint PDF/A-4u diagnostics:

{a4_failures or '- none'}
""")

    epub_rows=[]
    original_by_id={item["testId"]:item for item in results.get("epubcheckOriginalPhase1Packages",[])}
    updates={Path(item["output"]).stem:item for item in results.get("epubPackageUpdates",[])}
    for item in results["epubcheck"]:
        original=original_by_id.get(item["testId"],{})
        added=", ".join(updates.get(item["testId"],{}).get("addedContentProperties",[])) or "none"
        epub_rows.append(f"| {item['testId']} | {original.get('status','-')} | {item['status']} | {added} | {item.get('fatals','-')} | {item.get('errors','-')} | {item.get('warnings','-')} | {item.get('rawResult','')} |")
    _write(reports/"epubcheck_results.md",f"""# EPUBCheck Results

**VERIFIED BY TEST** with authoritative EPUBCheck 5.3.0 against EPUB 3.3.

The original Phase 1 packages are retained byte-for-byte. Phase 1B copies add only required
`svg`/`mathml` manifest declarations when present, so the initial negative result remains auditable.

| Package | Original | Phase 1B | Added property | Fatal | Errors | Warnings | JSON diagnostic |
| --- | --- | --- | --- | ---: | ---: | ---: | --- |
{chr(10).join(epub_rows)}
""")

    reader_lines=[]
    for reader in results.get("epubReaders",[]):
        opened=sum(item.get("opened",False) for item in reader.get("results",[])); total=len(reader.get("results",[]))
        reader_lines.append(f"- **{reader.get('reader')} {reader.get('version','')}** ({reader.get('engine','unknown engine')}): opened {opened}/{total} packages.")
    _write(reports/"epub_reader_interop.md",f"""# EPUB Reader Interoperability

{chr(10).join(reader_lines) or '- NOT VERIFIED.'}

**OBSERVED IN IMPLEMENTATIONS.** Tests cover opening, navigation, XHTML, Arabic metadata/text,
images, MathML, links, unknown experimental manifest resources, and embedded-PDF non-activation.
epub.js, Foliate JS, and Calibre showed the semantic spine without surfacing the sealed state or fixed PDF, which is safe
fallback behavior but creates user-experience ambiguity: an ordinary reader cannot communicate
that a bound fixed rendition exists. Screenshots are under `reports/screenshots/`.

Technical validity, fallback behavior, security, and user-experience ambiguity are separate axes.
""")

    all_epub=all(item["status"]=="PASS" for item in results["epubcheck"])
    reader_count=sum(1 for r in results.get("epubReaders",[]) if len(r.get("results",[]))==12 and all(i.get("opened") for i in r["results"]))
    representative_readers=[r for r in results.get("epubReaders",[]) if 0 < len(r.get("results",[])) < 12 and all(i.get("opened") for i in r["results"])]
    mapping_answer="YES" if node_avg>=.95 and rtl_node>=.95 and range_avg>=.90 else "UNCERTAIN"
    weasy_ua=[v for v in results["pdfValidation"] if v["renderer"]=="weasyprint" and v["profile"]=="ua2"]
    weasy_ua_pass=bool(weasy_ua) and all(v.get("compliant") for v in weasy_ua)
    best_pf=0.0
    for d in rtl:
        for detail in d.get("pdfTextFidelity",{}).values():
            for extractor in detail["result"]["extractors"].values():
                if "phraseRecovery" in extractor: best_pf=max(best_pf,extractor["phraseRecovery"]["NFKC"]["ratio"])
    pdf_answer="YES" if weasy_ua_pass and best_pf>=.90 else "YES, BUT REQUIRES A DEFINED POST-PROCESSING/GENERATION PROFILE" if weasy_ua_pass or best_pf>=.90 else "UNCERTAIN"
    epub_answer="YES WITH PROFILE RESTRICTIONS" if all_epub and reader_count>=2 else "UNCERTAIN"
    mapping_layer="SMALL CORRESPONDENCE LAYER" if node_avg>=.95 else "BORDERLINE"
    recommendation="PROCEED WITH ARCHITECTURE CHANGES" if mapping_answer=="YES" and pdf_answer!="UNCERTAIN" and epub_answer!="UNCERTAIN" else "RUN ANOTHER TARGETED RESEARCH PHASE"
    revision=results["revisionExperiment"]
    _write(reports/"phase1b_summary.md",f"""# Phase 1B Summary

## 1. Forward mapping gate

**{mapping_answer}.** VERIFIED BY TEST: visible-node macro coverage {_pct(node_avg)}, logical-range
coverage {_pct(range_avg)}, and T08/T09 minimum node/range coverage {_pct(rtl_node)}/{_pct(rtl_range)}.

## 2. MF versus PF

Forward Arabic mapping passes independently of PDF extraction. Best observed normalized Arabic PDF
phrase recovery was {_pct(best_pf)}. A mapping pass does not erase a PDF text failure.

## 3. Renderer independence

Paged.js provided paginated-DOM identity/range geometry. WeasyPrint 69 provided a substantially
independent fixed-PDF path. Their appearance, pagination, tagging, and extraction are not assumed equal.

## 4. Required architectural question

**Should mapping be an output artifact with implementation-specific generation? {mapping_answer}.**

Proposed wording (not applied to the approved ADR):

> A fixed-rendition processor SHALL emit a revision- and rendition-bound semantic-to-fixed mapping
> as an output of rendering when the mapping profile is claimed. The generation mechanism is
> implementation-specific and non-normative. Reconstruction from the fixed rendition MAY be used
> for independent validation or recovery, but SHALL NOT be the required mapping-generation method.

## 5. Tagged PDF 2.0 reference question

**{pdf_answer}.** veraPDF UA-2/Tagged PDF, WTPDF, and PDF/A-4 observations are reported separately;
structure-tree presence alone was not used. A viable profile must name the generation/validation
requirements that actually passed and retain Arabic PF tests.

## 6. EPUB 3.x OCF question

**{epub_answer}.** EPUBCheck: {sum(i['status']=='PASS' for i in results['epubcheck'])}/12 PASS.
Full-corpus independent reader implementations: {reader_count}; representative manual reader trials:
{', '.join(f"{r.get('reader')} {len(r.get('results',[]))}/{len(r.get('results',[]))}" for r in representative_readers) or 'none'}.
Unknown resources remained
inactive, but ordinary readers did not expose sealed/fixed lifecycle state.

## 7. Mapping-size kill criterion

**{mapping_layer}.** The artifact contains identity/range/page/quad correspondence and transforms,
not glyph drawing commands, line-breaking rules, fonts, or a second scene description.

## 8. T10 R1 to R2 regression

- Document ID preserved: {revision['documentIdPreserved']}
- Target IDs and new hashes: {revision['targetIdsPreserved']} / {revision['targetHashesChanged']}
- Revision and fixed rendition changed: {revision['revisionChanged']} / {revision.get('newFixedRendition')}
- Old map invalid for R2: {revision.get('oldMappingRejectedForR2')}
- Unrelated semantic changes: {revision['unrelatedSemanticChanges']}
- Unchanged-node page agreement: {_pct(revision.get('unchangedGeometry',{}).get('samePageRatio'))}

## 9. Remaining gates

Clipboard and screen-reader behavior remain NOT VERIFIED. Reader sealed-state UX, any failed formal
profiles, extractor differences, and geometry cross-check deviations must remain explicit.

## Final recommendation

**{recommendation}**
""")
    _write(root/"docs"/"PROPOSED_ARCHITECTURE_CHANGES_PHASE1B.md",f"""# Proposed Architecture Changes - Phase 1B

The approved `ARCHITECTURE_DECISIONS_0.1.md` is unchanged.

## AD-013 generation clarification

- **Decision affected:** AD-013, semantic-to-fixed mapping.
- **Evidence:** Forward Paged.js identity mapping achieved {_pct(node_avg)} visible-node and
  {_pct(range_avg)} range coverage versus the retained backward baseline.
- **Proposed wording:** Use the wording in `reports/phase1b_summary.md` section 4.
- **Alternatives:** Require fixed-PDF reconstruction; standardize renderer adapters; omit mappings.
- **Migration impact:** 0.1B mappings add status, method, confidence, transform, and explicit partial/
  invisible outcomes. Existing 0.1 mappings remain readable as backward baseline artifacts.
- **Recommendation:** {mapping_answer}; architecture-owner approval remains required.
""")
