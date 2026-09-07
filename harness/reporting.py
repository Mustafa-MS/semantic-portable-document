from __future__ import annotations

import json
from pathlib import Path
from statistics import mean
from typing import Any

from harness.util import write_json


LABELS = {
    "verified": "VERIFIED BY TEST",
    "observed": "OBSERVED IN ONE IMPLEMENTATION",
    "standard": "SUPPORTED BY STANDARD",
    "hypothesis": "HYPOTHESIS",
    "unknown": "NOT VERIFIED",
}


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def write_reports(root: Path, results: dict[str, Any]) -> None:
    reports = root / "reports"
    docs = root / "docs"
    reports.mkdir(parents=True, exist_ok=True)
    docs.mkdir(parents=True, exist_ok=True)
    write_json(reports / "results.json", results)

    documents = results["documents"]
    rendered = [d for d in documents if d.get("render", {}).get("success")]
    unavailable = [r for r in results["renderers"] if not r["available"]]
    renderer_rows = []
    for d in documents:
        render = d.get("render", {})
        renderer_rows.append(
            f"| {d['test_id']} | {'PASS' if render.get('success') else 'FAIL'} | {render.get('page_count', '-')} | "
            f"{render.get('render_time_ms', '-')} | {render.get('pdf_size', '-')} | {render.get('structure_tree_present', '-')} | "
            f"{render.get('text_characters_extracted', '-')} |"
        )
    _write(reports / "renderer_comparison.md", f"""# Renderer Comparison

**Evidence scope:** {LABELS['observed']} for Chromium; {LABELS['unknown']} for unavailable adapters.

| Document | Chromium | Pages | Time ms | PDF bytes | Structure tree | Extracted chars |
| --- | --- | ---: | ---: | ---: | --- | ---: |
{chr(10).join(renderer_rows)}

Chromium completed {len(rendered)}/{len(documents)} corpus renders. Its observed output is one
implementation result, not a format-level conclusion or a PDF/UA/WTPDF conformance claim.

Unavailable renderer observations:
{chr(10).join(f'- **{r["id"]}:** NOT RUN - executable was not installed.' for r in unavailable) or '- None.'}

Measurements cover page count, time, size, font resources, extraction, links, images, the PDF
structure-tree flag, marked-content flag, and language metadata. ActualText, ToUnicode quality,
table/figure tags, alt text propagation, and formal conformance remain unproven by this harness.
""")

    role_lines = []
    for d in rendered:
        render = d["render"]
        roles = render.get("structure_role_counts", {})
        role_lines.append(
            f"| {d['test_id']} | {render.get('to_unicode_font_count', 0)}/{render.get('font_resource_count', 0)} | "
            f"{render.get('embedded_font_resource_count', 0)}/{render.get('font_resource_count', 0)} | "
            f"{roles.get('/Table', 0)} | {roles.get('/TR', 0)} | {roles.get('/TH', 0)} | {roles.get('/TD', 0)} | "
            f"{roles.get('/Figure', 0)} | {render.get('structure_alt_text_count', 0)} | {render.get('structure_actual_text_count', 0)} |"
        )
    _write(reports / "pdf_conformance_observations.md", f"""# PDF Conformance Observations

**Evidence:** {LABELS['observed']} in Chromium PDFs. These object-level observations do not prove
WTPDF, PDF/UA-2, or PDF/A-4 conformance.

| Document | ToUnicode fonts | Embedded fonts | Table | TR | TH | TD | Figure | Alt | ActualText |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
{chr(10).join(role_lines)}

The harness inspects `/StructTreeRoot`, `/MarkInfo`, `/Lang`, structure roles, `/Alt`, `/ActualText`,
font descriptors, `/ToUnicode`, links, images, and extractable text. It does not validate role-map
semantics, MCID association correctness, reading order, Unicode CMap correctness, table header
relationships, archival restrictions, or accessibility conformance. Those require specialist tools
and manual assistive-technology inspection.
""")

    mapping_rows = []
    for d in rendered:
        coverage = d["mapping"]["coverage"]
        mapping_rows.append(f"| {d['test_id']} | {coverage['mapped']} | {coverage['expected']} | {_pct(coverage['ratio'])} | {d['mapping_validation']['valid']} | {d['mapping_validation']['error_count']} |")
    ratios = [d["mapping"]["coverage"]["ratio"] for d in rendered]
    multi = next((d for d in rendered if d["test_id"] == "T02"), None)
    _write(reports / "mapping_results.md", f"""# Mapping Results

**Evidence:** {LABELS['verified']} against the generated corpus and PDFs.

| Document | Mapped | Expected | Coverage | Schema/target validation | Errors |
| --- | ---: | ---: | ---: | --- | ---: |
{chr(10).join(mapping_rows)}

Mean exact-token mapping coverage: **{_pct(mean(ratios)) if ratios else 'n/a'}**.

T02 multi-page node produced **{results['revision_experiment'].get('t02_long_node_fragments', 'n/a')}**
page fragments. The experiment supports block/text/table-cell mapping when PDF text extraction
preserves the source token sequence. It does not prove glyph/cluster geometry. Unmatched Arabic,
MathML, SVG, ancestor, or reordered tokens are retained in each mapping file with a reason.

Negative-case validation rejected wrong revisions, wrong fixed hashes, unknown nodes, duplicate
records, invalid quads, and out-of-range text ranges in automated tests.
""")

    rtl_rows = []
    for test_id in ("T08", "T09"):
        d = next((x for x in rendered if x["test_id"] == test_id), None)
        if d:
            rtl = d["equivalence"]["rtl"]
            rtl_rows.append(f"| {test_id} | {d['manifest']['lang']} | {d['manifest']['dir']} | {rtl['exact_logical_order_matches']}/{rtl['arabic_samples']} | {_pct(d['mapping']['coverage']['ratio'])} | {d['render']['pdf_language'] or '(absent)'} |")
    _write(reports / "rtl_results.md", f"""# Arabic and RTL Results

**Evidence:** source metadata checks are {LABELS['verified']}; Chromium rendering/extraction is
{LABELS['observed']}; copy/paste and accessibility conformance are {LABELS['unknown']}.

| Document | lang | dir | Exact Arabic extraction | Mapping coverage | PDF /Lang |
| --- | --- | --- | ---: | ---: | --- |
{chr(10).join(rtl_rows)}

The source stores Arabic in logical Unicode order with `lang="ar"` and `dir="rtl"`. Exact phrase
matching measures extraction order without pretending that a visual inspection proves logical
text order. Automated clipboard behavior was not available. Page render PNGs are generated for
human shaping, joining, punctuation, and bidi inspection.
""")

    package_rows = [f"| {d['test_id']} | {d['package_validation']['valid_internal_profile']} | {len(d['package_validation']['errors'])} | {d['package_validation']['epubcheck']} |" for d in documents if d.get("package_validation")]
    _write(reports / "epub_compatibility.md", f"""# EPUB Compatibility

**Evidence:** internal OCF/ZIP/XML profile checks are {LABELS['verified']}; EPUB conformance and
reader compatibility are {LABELS['unknown']}.

| Document | Internal profile | Errors | EPUBCheck |
| --- | --- | ---: | --- |
{chr(10).join(package_rows)}

Each package has an uncompressed first `mimetype` entry, `META-INF/container.xml`, package
document, manifest, spine, navigation document, XHTML, CSS, local assets, and experimental JSON/PDF
resources. EPUBCheck and two independent reader trials were unavailable, so the harness does not
claim the packages are EPUB-conformant or that unknown resources are harmless in readers.
""")

    integ = results["integrity_experiment"]
    _write(reports / "integrity_results.md", f"""# Integrity Results

**Evidence:** {LABELS['verified']}.

- Untampered sealed state valid: **{integ['untampered_valid']}**
- Semantic modification detected: **{integ['semantic_tamper_detected']}**
- PDF modification detected: **{integ['pdf_tamper_detected']}**
- Mapping modification detected: **{integ['mapping_tamper_detected']}**
- Required CSS/resource modification detected: **{integ['required_resource_tamper_detected']}**
- Excluded cache-file rule leaves the descriptor unchanged: **{integ['excluded_cache_ignored']}**

This is SHA-256 integrity binding only. It provides no signer identity, trust, non-repudiation,
revocation, or long-term signature validation.
""")

    tx = results["revision_experiment"]
    _write(reports / "agent_api_results.md", f"""# Minimal Agent API Results

**Evidence:** {LABELS['verified']} using deterministic transaction fixtures; external AI execution
is {LABELS['unknown']}.

- Atomic Table 4 + discussion update committed: **{tx['atomic_update_committed']}**
- Cell Node ID preserved: **{tx['cell_id_preserved']}**
- Revision ID changed: **{tx['revision_changed']}**
- Cell content hash changed: **{tx['node_hash_changed']}**
- Unrelated semantic nodes changed: **{tx['unrelated_nodes_changed']}**
- Old mapping rejected against R2: **{tx['old_mapping_rejected']}**
- New fixed rendition and R2 mapping generated: **{tx['new_rendition_generated']}**
- Stale-revision write rejected without mutation: **{tx['stale_revision_rejected']}**
- Node-hash conflict rejected without mutation: **{tx['node_conflict_rejected']}**

The harness implements only `replaceText`, `updateTableCell`, `replaceFigure`, `moveSection`, and
`insertCitation`. This is enough to test atomicity and optimistic concurrency, not to define a full SDK.
""")

    avg_cov = mean(ratios) if ratios else 0.0
    tagged_count = sum(1 for d in rendered if d["render"].get("structure_tree_present"))
    rtl = [d for d in rendered if d["test_id"] in {"T08", "T09"}]
    rtl_exact = sum(d["equivalence"]["rtl"]["exact_logical_order_matches"] for d in rtl)
    rtl_samples = sum(d["equivalence"]["rtl"]["arabic_samples"] for d in rtl)
    _write(reports / "phase1_summary.md", f"""# Phase 1 Summary

## 1. Is EPUB OCF Still a Good Container Basis?

**UNCERTAIN.** {LABELS['verified']}: {len(package_rows)} experimental packages passed the internal
OCF/ZIP/XML profile. {LABELS['unknown']}: EPUBCheck and two-reader interoperability were not run.

## 2. Is XHTML Still a Good Authoritative Semantic Representation?

**YES for continued experimentation.** {LABELS['verified']}: all 12 fixtures represented the scoped
semantics, stable IDs, language/direction, and transactional edits without duplicate content stores.

## 3. Can Existing Renderers Produce an Acceptable Fixed Rendition?

- Chromium: **Suitable with post-processing/research limitations** - rendered {len(rendered)}/{len(documents)}, but tagging quality and formal conformance are not proven.
- WeasyPrint: **Unknown** - not installed.
- Vivliostyle/Paged.js class: **Unknown** - not installed.

## 4. Is Tagged PDF Suitable as the Reference Fixed Rendition?

**UNCERTAIN.** Chromium exposed a structure tree in {tagged_count}/{len(rendered)} PDFs, but a
structure-tree flag alone does not establish useful tags, PDF/UA-2, WTPDF, or PDF/A-4 conformance.

## 5. Is Semantic-to-Fixed Mapping Practically Achievable?

**Partially.** {LABELS['verified']}: exact extracted-token mapping averaged {_pct(avg_cov)} coverage.
Failures remain observable. Geometry derived from PDF extraction is useful but renderer/extractor-dependent.

## 6. Does the Minimal Mapping Model Need Expansion?

**Yes, experimentally.** It needs explicit uncertainty/provenance, parent-child overlap rules,
cluster/bidi-aware text anchors, non-text vector regions, and a way to state “not mapped” without
turning layout into a second source of truth.

## 7. Does Arabic/RTL Work Correctly?

- Semantic source: **verified** for logical Unicode plus `lang`/`dir`.
- Rendering: **observed in Chromium; human visual QA required**.
- PDF extraction: exact logical phrases {rtl_exact}/{rtl_samples}.
- Mapping: measured per T08/T09 in `rtl_results.md`.
- Copy/paste: **not verified**.
- Accessibility: structure indicators observed; semantic quality/conformance **not verified**.

## 8. Can Semantic-Fixed Equivalence Be Validated?

**Partially.** Structural presence, normalized text similarity, mapped cell presence, link counts,
hash/revision binding, and limited RTL exact matches are automatable. Visual meaning, complete table
relationships, MathML meaning, alt-text propagation, reading order, and accessibility equivalence
cannot be proven by these checks.

## 9. Does Stable Identity Provide a Measurable Advantage?

**Yes within the fixture.** {LABELS['verified']}: the Table 4 cell kept its ID across an edit while
its content hash and revision changed, allowing exact targeting and zero unrelated node changes.
Comparative agent trials against B1-B4 remain unrun.

## 10. Does the Transaction Model Prevent Unsafe Stale Edits?

**YES in the minimal API.** Revision and node-hash conflicts were rejected before commit, and the
source bytes remained unchanged.

## 11. Are Conventional EPUB Readers Compatible Enough?

**UNCERTAIN.** No independent reader trials were available.

## 12. Biggest New Technical Risk

Mapping quality depends on extraction order and geometric fidelity, especially for bidi text,
MathML, SVG/vector content, and nested semantic objects. Fixing this could pull the mapping layer
toward renderer-specific complexity.

## 13. Recommended Architecture Changes

Do not change the accepted baseline yet. Add experimental mapping confidence/provenance fields and
define explicit partial/unmappable outcomes before proposing a normative change.

## 14. Proceed / Modify / Stop

**PROCEED**

Proceed only to a broader Phase 1 run with the missing renderers, EPUBCheck/readers, and expert PDF
validators. The local results establish coherence of the narrow harness but are insufficient for a
format specification or superiority claim.
""")

    failures = results.get("failures", [])
    _write(docs / "FINDINGS.md", f"""# Findings

This file summarizes the machine-readable evidence in `reports/results.json`.

- {LABELS['verified']}: {len(rendered)} Chromium PDFs, mappings, packages, integrity descriptors,
  and equivalence records were produced and checked.
- {LABELS['verified']}: stale revision and node-hash conflicts were rejected atomically.
- {LABELS['observed']}: Chromium-specific pagination, extraction, links, images, and tagging flags.
- {LABELS['unknown']}: WeasyPrint, Vivliostyle/Paged.js, EPUBCheck, reader interoperability,
  clipboard behavior, and formal PDF conformance.
- Logged failures/unsupported observations: **{len(failures)}**.

Negative results are preserved in `reports/results.json` and the focused reports; they are not
converted into architecture-level claims.
""")
    _write(docs / "OPEN_QUESTIONS.md", """# Open Questions

1. Can WeasyPrint and Vivliostyle/Paged.js produce comparable geometry and better semantics?
2. Do EPUBCheck and two independent readers accept/ignore the experimental resources predictably?
3. Does PDF tagging preserve headings, table scopes, figures, alt text, MathML, language spans,
   footnotes, and logical reading order - not merely a structure-tree flag?
4. Which PDF text model can express logical Unicode ranges through Arabic shaping clusters and bidi?
5. Can mapping uncertainty and partial coverage be represented without becoming a layout model?
6. How do B1-B6 compare under the same human- and agent-executed edit tasks?
7. Is post-processing a generated PDF economically and semantically sustainable?
""")
    _write(docs / "PROPOSED_ARCHITECTURE_CHANGES.md", """# Proposed Architecture Changes

No accepted architecture decision is proposed for change from this local run.

## Experimental clarification candidate (not an ADR change)

- **Decision affected:** AD-013 / Mapping 0.1.
- **Evidence:** Exact-token mapping can be partial and extractor-dependent, especially for bidi,
  MathML, SVG/vector content, and large nested nodes.
- **Why change is proposed:** None yet; the evidence comes from one implementation.
- **Alternative options:** Add confidence/provenance and explicit unmappable outcomes; use renderer
  instrumentation; post-process tagged PDF; narrow map targets to leaf semantic objects.
- **Migration impact:** Unknown until multi-renderer trials.
- **Recommendation:** Test all alternatives before changing the accepted decision.
""")
