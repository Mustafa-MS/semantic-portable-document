from __future__ import annotations

from pathlib import Path
from typing import Any


def _write(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _validation_rows(results: dict[str, Any], candidate: str | None = None) -> str:
    rows = ["| Fixture | Candidate | Profile | Result | Failed rules | Failed checks |", "|---|---|---:|---:|---:|---:|"]
    for item in results["validations"]:
        if candidate and item["candidate"] != candidate: continue
        rows.append(f"| {item['testId']} | {item['candidate']} | {item['profile']} | {'PASS' if item.get('compliant') else 'FAIL'} | {item.get('failedRules', 0)} | {item.get('failedChecks', 0)} |")
    return "\n".join(rows)


def _failure_details(results: dict[str, Any], profiles: set[str]) -> str:
    chunks = []
    for item in results["validations"]:
        if item["profile"] not in profiles or item.get("compliant"): continue
        chunks.append(f"### {item['candidate']} {item['testId']} — {item['profile']}")
        for failure in item.get("failures", []):
            chunks.append(f"- `{failure.get('specification')}` {failure.get('clause')}/{failure.get('testNumber')}: {failure.get('failedChecks')} failed checks — {failure.get('description')}")
        if item.get("error"): chunks.append(f"- Validator error: `{item['error']}`")
    return "\n\n".join(chunks) if chunks else "No residual automated failures in this profile set."


def _ratio(item: dict[str, Any], extractor: str) -> str:
    value = item.get("textFidelity", {}).get("extractors", {}).get(extractor, {})
    ratio = value.get("phraseRecovery", {}).get("raw", {}).get("ratio")
    return "N/A" if ratio is None else f"{ratio * 100:.1f}%"


def _compiled(results: dict[str, Any], test_id: str) -> dict[str, Any]:
    return next(item for item in results["compiled"] if item["testId"] == test_id)


def _fop(results: dict[str, Any], test_id: str) -> dict[str, Any]:
    return next(item for item in results["fop"] if item["testId"] == test_id)


def write_phase1c_reports(root: Path, results: dict[str, Any]) -> None:
    reports = root / "reports"; docs = root / "docs"
    t08, t09 = _compiled(results, "T08"), _compiled(results, "T09")
    all_exact = all(page.get("exact") for item in results["compiled"] for renderer in ("poppler", "mupdf") for page in item["visualPreservation"][renderer])
    all_operators = all(item["visualPreservation"]["drawingOperatorsPreserved"] for item in results["compiled"])
    ua2 = [item for item in results["validations"] if item["candidate"] == "compiled" and item["profile"] == "ua2"]
    ua2_pass = sum(item.get("compliant", False) for item in ua2)
    fop_ua1 = [item for item in results["validations"] if item["candidate"] == "fop" and item["profile"] == "ua1"]
    fop_ua1_pass = sum(item.get("compliant", False) for item in fop_ua1)

    _write(reports / "semantic_pdf_compiler_design.md", f"""# Semantic PDF Compiler design

## Boundary

The disposable compiler consumes authoritative XHTML, the revision/rendition-bound Phase 1B forward map, and the Paged.js/Chromium visual PDF. It does not paginate, shape glyphs, choose fonts, redraw images, or recreate any visual object.

The compiler changes only the PDF header/version, metadata, logical structure and parent trees, marked-content properties, structure destinations, and artifact classification. Existing text-showing, image, path, graphics-state, and positioning operators remain unchanged. Across the six compiled fixtures, drawing-operator preservation was **{all_operators}**.

## Semantic mapping table

| XHTML | PDF 2.0 role | Important attributes |
|---|---|---|
| `main`, `article`, `section`, `nav` | `Sect` | language, external XHTML node ID |
| `h1`–`h6` | `H1`–`H6` | logical text, language |
| `p` | `P` | logical text, language |
| `ul`, `ol` | `L` | `ListNumbering` |
| `li` | `LI` | `Lbl` + `LBody`; links are inside `LBody` |
| `table`, `tr`, `th`, `td` | `Table`, `TR`, `TH`, `TD` | `Scope`, `RowSpan`, `ColSpan` |
| `caption`, `figcaption` | `Caption` | logical text |
| `figure` | `Figure` | `Alt` from the meaningful image alternative |
| footnote `aside` | `FENote` | language and node ID |
| `a` | `Link` | annotation association remains a residual area |
| MathML `math` | `Formula` | logical equation text; native MathML association remains future work |

PDF object numbers are not identity. The XHTML `data-node-id` is copied to structure `/ID` for this experiment and the authoritative association is also emitted as companion JSON.

## Association method

Chromium's existing tags are treated only as disposable MCID ownership hints. Authoritative roles, hierarchy, language, alternate text, table attributes, and logical order come from XHTML. Existing MCID groups are matched in semantic role order and checked against the already-complete forward map. Unowned content is explicitly marked as artifact. The rebuilt parent tree binds every retained MCID to the new XHTML-derived structure element.

## Complexity boundary

This is semantic compilation, not rendering: no glyph IDs, shaping state, line-breaking model, scene graph, or rasterizer is stored in the mapping. The renderer-specific dependency is the ability to associate existing marked-content groups with semantic nodes. That dependency is why the proposed profile is restricted rather than renderer-independent.
""")

    strategy_lines = []
    for test_id, variants in results["strategyExperiments"].items():
        for name, value in variants.items():
            extractors = value["text"]["extractors"]
            strategy_lines.append(f"| {test_id} | {name} | {_ratio({'textFidelity': value['text']}, 'pdfjs')} | {_ratio({'textFidelity': value['text']}, 'pypdf')} | {_ratio({'textFidelity': value['text']}, 'pdfplumber')} | {_ratio({'textFidelity': value['text']}, 'mupdf')} | {'PASS' if value['ua2'].get('compliant') else 'FAIL'} |")
    _write(reports / "actualtext_experiments.md", """# ActualText experiments

## Strategies

- **A — structure element:** `/ActualText` is placed on XHTML-derived structure elements. It leaves the content stream semantically untouched.
- **B — existing marked content:** logical replacement is attached to Chromium's existing MCID sequences without changing drawing operators.
- **C — nested Span (selected experiment):** renderer-internal character wrappers are flattened, then a `Span` `/ActualText` wrapper encloses unchanged text operators within one MCID. Remaining MCIDs for the semantic element use empty replacement spans to avoid duplicate accessible content. The logical replacement is anchored at the first stream-order text sequence because that gave the best tested MuPDF behavior.
- **Negative control rejected:** no invisible duplicate/OCR text layer was added.

| Fixture | Strategy | PDF.js | pypdf | pdfplumber | MuPDF | veraPDF UA-2 |
|---|---|---:|---:|---:|---:|---:|
""" + "\n".join(strategy_lines) + """

## Interpretation

Structure-level `/ActualText` does not repair ordinary library extraction in the tested tools. Marked-content placement can be formally valid and can improve MuPDF, but PDF.js, pypdf, and pdfplumber do not consistently honor the logical replacement. T09 proves that validator success is not sufficient evidence of correct bidi extraction. The selected placement is retained as a standards-valid experiment, not as a universal interoperability solution.
""")

    def rtl_row(test_id: str, item: dict[str, Any]) -> str:
        return f"| {test_id} | {_ratio(item,'pdfjs')} | {_ratio(item,'pypdf')} | {_ratio(item,'pdfplumber')} | {_ratio(item,'mupdf')} |"
    _write(reports / "rtl_pdf_compiled_results.md", f"""# Arabic and bidi compiled-PDF results

Raw and NFC/NFKC outputs are stored separately in `corpus/generated/phase1c/text/`; normalization is not used to conceal order failures.

| Fixture | PDF.js | pypdf | pdfplumber | MuPDF |
|---|---:|---:|---:|---:|
{rtl_row('T08 compiled', t08)}
{rtl_row('T09 compiled', t09)}
{rtl_row('T08 FOP', _fop(results,'T08'))}
{rtl_row('T09 FOP', _fop(results,'T09'))}

## T08 gate

The target is at least 95% exact logical phrase recovery on two independent paths. The measured paths above determine whether that gate passed; library disagreement remains explicit.

## T09 gate

The required probes are `FROC = 0.906`, `Model-X`, the URL, Western and Arabic-Indic digits, `x = 0.906`, and `[Smith 2025]`. Probe booleans are retained in `results_phase1c.json`. The compiled candidate reaches formal UA-2 validity but does not make all logical forms reliable across ordinary extractors; especially, the first mixed Arabic/LTR sentence remains reordered in MuPDF and unchanged in PDF.js/pypdf/pdfplumber.
""")

    _write(reports / "clipboard_search_results.md", """# Clipboard and search results

## Method

Library extraction is reported separately from real viewer behavior. Actual viewer trials are recorded as `EXACT`, `NORMALIZATION_ONLY`, `ORDER_ERROR`, `CHARACTER_ERROR`, or `UNTESTED`; a visible match must overlap the expected mapped region.

## Initial automated evidence

PDF.js, pypdf, pdfplumber, and MuPDF disagree on `/ActualText` handling. This disagreement is itself an interoperability failure and prevents substituting library output for clipboard evidence. Viewer trials and their exact pasted text are stored in `results_phase1c.json` under `viewerExperiments` when available; absent entries mean `UNTESTED`, not PASS.

Required search probes: `وثيقة عربية تجريبية`, `FROC = 0.906`, `Model-X`, and `Smith 2025`.
""")

    _write(reports / "tagged_pdf_structure_results.md", f"""# Tagged PDF structure results

The compiler rebuilds a single PDF 2.0 namespace `Document` tree in XHTML logical order, creates MCR dictionaries and a new parent tree, classifies unowned page content as artifacts, attaches XHTML node IDs externally and through experimental `/ID`, supplies figure `Alt`, and emits table/list attributes.

{_validation_rows(results, 'compiled')}

## Representative structure inventory

- T03 roles: `{t03_roles(results)}`
- T08 roles: `{t08['structure']['roles']}`
- T12 roles: `{_compiled(results,'T12')['structure']['roles']}`

Remaining failures, if any, are exact validator findings below rather than generic “tagged/not tagged” claims.

{_failure_details(results, {'ua2'})}
""")

    _write(reports / "pdfua_wtpdf_results_phase1c.md", f"""# PDF/UA-2 and WTPDF results — Phase 1C

{_validation_rows(results)}

## Interpretation

Compiled PDFs declare PDF/UA-2 through XMP only for the experiment and are labelled conformant only where veraPDF passes. WTPDF reuse and accessibility are separate claims. A clean automated report does not resolve human checks or the demonstrated T09 extractor behavior.

## Exact residual diagnostics

{_failure_details(results, {'ua1','ua2','wt1a','wt1r'})}
""")

    _write(reports / "pdfa4_results_phase1c.md", f"""# PDF/A-4 results — Phase 1C

PDF/A debugging was isolated until after the semantic and bidi experiments. T10 compiled PDF was checked with veraPDF profile `4`.

{_validation_rows(results, 'compiled')}

## Exact residual diagnostics

{_failure_details(results, {'4'})}

## Decision

PDF/A-4 belongs to an **Archive capability**, not every ordinary Fixed rendition. Mandatory PDF/A would import output-intent, color-management, metadata, and archival-policy constraints into documents whose immediate requirement is a stable visual snapshot. Archive can require the additional transform and validation without weakening the Base/Fixed model.
""")

    _write(reports / "fixed_renderer_candidate_matrix.md", f"""# Fixed renderer candidate matrix

| Candidate | VF | PF Arabic/bidi | PDF/UA | WTPDF | PDF/A readiness | Complexity | Maintainability |
|---|---|---|---|---|---|---|---|
| A. Raw Paged.js/Chromium | strong visual baseline; complete forward map | mixed RTL extraction broken | Phase 1B failures | Phase 1B failures | low | low renderer integration | good, but semantics insufficient |
| B. Raw WeasyPrint | independent; T09 equation-order visual issue retained | broken on T08/T09 | partial generator tagging | failed representative checks | PDF/A generation exists but did not solve semantics | low | good for comparison, not primary bidi |
| C. Paged.js + compiler | **{'exact on both rasterizers' if all_exact else 'visual differences detected'}** | improved in MuPDF but inconsistent across paths | {ua2_pass}/{len(ua2)} automated PASS | see profile matrix | T10 still requires archive transform | medium, renderer-MCID adapter | viable only as restricted experimental profile |
| D. Apache FOP 2.11 | independently reflows; not pixel-equivalent to Paged | logical recovery varies by extractor | {fop_ua1_pass}/{len(fop_ua1)} UA-1 PASS | not a PDF 2.0/WTPDF generator baseline | separate work | medium XHTML→FO projection, information/layout loss | mature Apache 2.0 stack; FO projection is lossy |

Licensing: the experimental compiler uses permissively licensed Python tooling; Apache FOP is Apache License 2.0. No candidate is adopted solely on validator performance.
""")

    _write(reports / "semantic_compiler_complexity.md", """# Semantic compiler complexity

## Implemented custom PDF knowledge

- PDF 2.0 structure elements, namespace, MCRs, parent tree, artifacts, language, IDs and XMP;
- semantic mapping from XHTML roles and attributes;
- renderer MCID ownership adapter and marked-content `/ActualText` experiments;
- structure-destination repair for outlines;
- byte/pixel/operator preservation evidence.

## Explicitly not implemented

- glyph shaping, bidi layout, line breaking, pagination, font selection/rasterization;
- image/vector re-rendering;
- a second page scene or PDF text-layout engine.

## Assessment

**SEMANTIC COMPILATION**, with one architectural warning: interoperable logical text repair is renderer/consumer-sensitive. The map remains small, but wrapping correct semantic ranges requires a renderer-MCID association adapter. If a future implementation must infer or rebuild glyph shaping to make T09 work, it crosses the kill criterion into reimplementing a PDF renderer.
""")

    _write(docs / "PROPOSED_ARCHITECTURE_CHANGES_PHASE1C.md", """# Proposed Architecture Changes — Phase 1C

These are evidence-supported proposals only. AD-013's approved Phase 1B clarification was incorporated separately; no other accepted decision is changed here.

## P1C-01 — Fixed PDF status

Choose **C. PDF should remain the prototype/reference fixed rendition, but not yet become normative.**

The compiler proves exact visual preservation and large conformance gains, but T09 logical text is not interoperable across PDF.js, pypdf, pdfplumber, and MuPDF. A normative profile must not depend on a validator pass while common consumers disagree.

## P1C-02 — Restricted semantic compiler profile

Retain a candidate profile requiring authoritative XHTML, the revision/rendition-bound forward map, renderer-emitted MCIDs or an equivalent association channel, XHTML-derived PDF 2.0 structure, exact dual-raster visual preservation, and explicit PF/CF tests. Do not require a particular implementation mechanism.

## P1C-03 — Accessibility model

For Format 0.1 Base/Fixed, adopt **Model 1**: authoritative semantic XHTML is the accessibility source; fixed PDF is the visual canonical snapshot. Offer **Model 2** only through an Accessibility/Tagged-PDF capability with independent PDF/UA/WTPDF claims and synchronization checks.

Model 1 reduces duplicated accessibility state and works across non-PDF fixed renditions, but PDF-only export users may lose accessibility. Model 2 better matches user and legal expectations for standalone PDF exports, yet duplicates semantics and presently exposes consumer disagreement. Therefore a sealed package may rely on Model 1, while exported PDFs claiming accessibility must satisfy Model 2.

## P1C-04 — Archive scope

Require PDF/A-4 only for an **Archive capability**, not every sealed Fixed rendition. Ordinary Fixed documents should not inherit archival color/output-intent and metadata policy unless the archive claim is requested.
""")

    _write(reports / "phase1c_summary.md", f"""# Phase 1C summary

## Outcome

The compiler preserved the Paged.js visual page scene across six representative fixtures: dual-raster exactness was **{all_exact}**, and non-semantic drawing-operator preservation was **{all_operators}**. The automated PDF/UA-2 result was {ua2_pass}/{len(ua2)} compiled representatives. Apache FOP provided an independent accessibility-aware generator and reached {fop_ua1_pass}/{len(fop_ua1)} PDF/UA-1 automated passes.

The decisive negative evidence is PF interoperability. `/ActualText` placement that passes formal validation is not consistently honored by PDF.js, pypdf, or pdfplumber, and MuPDF still reorders the first T09 mixed-bidi sentence. VF, PF, and CF therefore remain separate.

## Preserved Phase 1B findings

- forward visible-node coverage: 100%
- forward logical-range coverage: 100%
- valid fixed-page fragments: 3,094/3,094
- T08 and T09 mapping: 100%
- mapping: SMALL CORRESPONDENCE LAYER
- EPUB OCF: YES WITH PROFILE RESTRICTIONS

## Required architecture decisions

**Semantic compilation:** UNCERTAIN. It can preserve pixels and create formally strong structure without re-rendering, but cannot yet guarantee interoperable logical T09 text.

**PDF role:** C. PDF should remain the prototype/reference fixed rendition, but not yet become normative.

**Accessibility:** Base/Fixed uses Model 1 (semantic XHTML accessible; PDF is the canonical visual snapshot). Model 2 is required for any standalone PDF export that claims accessibility and remains a capability/profile with explicit PDF/UA/WTPDF checks.

**Archive:** PDF/A-4 is mandatory only for an Archive capability.

## Gates

- Mapping: PASS, preserved from Phase 1B.
- VF: {'PASS' if all_exact and all_operators else 'FAIL'}.
- T08 PF: see extractor-specific ratios; no normalization masking.
- T09 PF: FAIL for cross-consumer interoperability.
- CF: automated results are reported by profile; human accessibility checks remain outside veraPDF.
- Complexity: still semantic compilation, with a renderer-MCID adapter and an interoperability warning.

## Recommendation

PROCEED TO FORMAT 0.1 WITH FIXED-PDF PROFILE STILL EXPERIMENTAL
""")


def t03_roles(results: dict[str, Any]) -> str:
    return str(_compiled(results, "T03")["structure"]["roles"])
