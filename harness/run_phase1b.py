from __future__ import annotations

import copy
import json
import statistics
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from lxml import etree

from harness.reporting_phase1b import write_phase1b_reports
from harness.package import make_phase1b_compatible_epub
from harness.transaction import TransactionalDocument, node_hash
from harness.util import ROOT, write_json
from mapping.forward import calibrate_geometry, run_pagedjs_forward
from mapping.generate import generate_mapping
from renderers.adapters import inspect_pdf, render_weasyprint
from validation.pdf_cmap import inspect_tounicode
from validation.pdf_text import extract_pdf_text
from validation.tool_validators import run_epubcheck, run_verapdf


def _relative(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def _summary_text_fidelity(value: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(value)
    for extractor in result.get("extractors", {}).values():
        if isinstance(extractor, dict):
            extractor.pop("outputs", None)
    return result


def _make_r2(source: Path, identities: dict[str, str]) -> tuple[Path, dict[str, Any]]:
    document = TransactionalDocument.from_path(source)
    cell_id, paragraph_id = identities["T10.froc"], identities["T10.resultp"]
    before_cell_hash = document.get_node_hash(cell_id)
    before_paragraph_hash = document.get_node_hash(paragraph_id)
    result = document.apply_transaction({"baseRevision": document.revision_id, "operations": [
        {"op": "updateTableCell", "node": cell_id, "expectedNodeHash": before_cell_hash, "value": "0.906"},
        {"op": "replaceText", "node": paragraph_id, "expectedNodeHash": before_paragraph_hash, "value": "Table 4 reports the exact experimental result: FROC improved from baseline to 0.906."},
    ]})
    output = ROOT / "corpus" / "sources" / "T10_R2_1B.xhtml"
    output.write_bytes(result.bytes)
    updated = TransactionalDocument(result.bytes)

    def shallow(el: etree._Element) -> tuple[Any, ...]:
        return (etree.QName(el).localname, tuple(sorted(el.attrib.items())), el.text or "", tuple((etree.QName(child).localname, child.get("data-node-id")) for child in el))
    before_tree, after_tree = etree.parse(str(source)), etree.parse(str(output))
    before = {el.get("data-node-id"): shallow(el) for el in before_tree.xpath('//*[@data-node-id]')}
    after = {el.get("data-node-id"): shallow(el) for el in after_tree.xpath('//*[@data-node-id]')}
    changed = sorted(key for key in before.keys() | after.keys() if before.get(key) != after.get(key))
    document_id_r1 = before_tree.xpath('string(//*[local-name()="meta"][@name="document-id"]/@content)')
    document_id_r2 = after_tree.xpath('string(//*[local-name()="meta"][@name="document-id"]/@content)')
    return output, {
        "documentIdPreserved": document_id_r1 == document_id_r2,
        "documentId": document_id_r2,
        "revisionR1": document.revision_id, "revisionR2": updated.revision_id,
        "revisionChanged": document.revision_id != updated.revision_id,
        "targetNodeIds": [cell_id, paragraph_id],
        "targetIdsPreserved": all(after_tree.xpath(f'//*[@data-node-id="{node}"]') for node in (cell_id, paragraph_id)),
        "targetHashesChanged": before_cell_hash != updated.get_node_hash(cell_id) and before_paragraph_hash != updated.get_node_hash(paragraph_id),
        "changedNodes": changed, "unrelatedSemanticChanges": len(set(changed) - {cell_id, paragraph_id}),
    }


def _compare_revision_geometry(r1: dict[str, Any], r2: dict[str, Any], changed: set[str]) -> dict[str, Any]:
    def blocks(mapping: dict[str, Any]) -> dict[str, list[tuple[str, tuple[float, ...]]]]:
        result = {}
        for record in mapping["records"]:
            result[record["node"]] = [(fragment["page"], tuple(fragment["quad"])) for fragment in record["fragments"] if fragment["type"] == "block"]
        return result
    a, b = blocks(r1), blocks(r2)
    unchanged = sorted((set(a) & set(b)) - changed)
    same_page = 0; deviations = []
    for node in unchanged:
        if [item[0] for item in a[node]] == [item[0] for item in b[node]]:
            same_page += 1
        if len(a[node]) == len(b[node]):
            for (_, qa), (_, qb) in zip(a[node], b[node]):
                deviations.extend(abs(x-y) for x,y in zip(qa,qb))
    return {"unchangedNodesCompared": len(unchanged), "samePageAssignment": same_page, "samePageRatio": round(same_page/len(unchanged),4) if unchanged else 1.0, "medianCoordinateDeviationPt": round(statistics.median(deviations),3) if deviations else None}


def _run_epubjs(packages: list[Path]) -> dict[str, Any]:
    runtime = Path.home() / ".cache" / "codex-runtimes" / "codex-primary-runtime" / "dependencies" / "node"
    node = runtime / "bin" / "node.exe"
    epubjs = ROOT / ".phase1b" / "deps" / "node" / "node_modules" / "epubjs" / "dist" / "epub.js"
    jszip = ROOT / ".phase1b" / "deps" / "node" / "node_modules" / ".pnpm" / "jszip@3.10.1" / "node_modules" / "jszip" / "dist" / "jszip.min.js"
    output = ROOT / "reports" / "epubjs_reader_results.json"
    screenshots = ROOT / "reports" / "screenshots" / "epubjs"
    env = __import__("os").environ.copy()
    env["NODE_PATH"] = str(ROOT / ".phase1b" / "deps" / "node" / "node_modules") + ";" + str(runtime / "node_modules")
    cmd = [str(node), str(ROOT / "scripts" / "epubjs_reader_test.cjs"), str(ROOT), str(output), str(screenshots), r"C:\Program Files\Google\Chrome\Application\chrome.exe", str(epubjs), str(jszip), *map(str, packages)]
    proc = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True, timeout=240)
    if proc.returncode != 0:
        return {"reader": "epub.js", "version": "0.3.93", "status": "FAILED", "error": proc.stderr[-4000:]}
    return json.loads(output.read_text(encoding="utf-8"))


def _run_foliate(packages: list[Path]) -> dict[str, Any]:
    runtime = Path.home() / ".cache" / "codex-runtimes" / "codex-primary-runtime" / "dependencies" / "node"
    node = runtime / "bin" / "node.exe"
    output = ROOT / "reports" / "foliate_reader_results.json"
    screenshots = ROOT / "reports" / "screenshots" / "foliate"
    env = __import__("os").environ.copy()
    env["NODE_PATH"] = str(runtime / "node_modules")
    cmd = [str(node), str(ROOT / "scripts" / "foliate_reader_test.cjs"), str(ROOT), str(output), str(screenshots), r"C:\Program Files\Google\Chrome\Application\chrome.exe", *map(str, packages)]
    proc = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True, timeout=300)
    if proc.returncode != 0:
        return {"reader": "Foliate JS", "version": "git:78914aef4466eb960965702401634c2cb348e9b1", "status": "FAILED", "error": proc.stderr[-4000:]}
    return json.loads(output.read_text(encoding="utf-8"))


def main() -> int:
    phase1 = json.loads((ROOT / "reports" / "results.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "corpus" / "expected" / "corpus_manifest.json").read_text(encoding="utf-8"))
    identities = json.loads((ROOT / "corpus" / "expected" / "identities.json").read_text(encoding="utf-8"))
    r2_source, revision = _make_r2(ROOT / "corpus" / "sources" / "T10.xhtml", identities)
    entries = [{"test_id": item["test_id"], "source": ROOT / item["source"], "manifest": item} for item in manifest]
    r2_tree = etree.parse(str(r2_source))
    entries.append({"test_id": "T10_R2_1B", "source": r2_source, "manifest": {"test_id": "T10_R2_1B", "title": "Academic Paper R2 Phase 1B", "document_id": revision["documentId"], "revision_id": revision["revisionR2"], "lang": "en", "dir": "ltr", "source": _relative(r2_source)}})
    out = ROOT / "corpus" / "generated" / "phase1b"
    for name in ("pagedjs", "weasyprint", "forward", "backward", "raw", "text"):
        (out / name).mkdir(parents=True, exist_ok=True)
    results: dict[str, Any] = {
        "schemaVersion": "0.1B-experimental", "phase1ResultsPreservedAt": "reports/results.json",
        "tools": {"pagedjs": "0.4.3", "weasyprint": "69.0", "epubcheck": "5.3.0", "verapdf": "1.30.2", "epubjs": "0.3.93", "foliateJs": "git:78914aef4466eb960965702401634c2cb348e9b1", "calibre": "9.14", "pdfjs": "bundled runtime", "chromium": "system Chrome/151"},
        "documents": [], "revisionExperiment": revision, "failures": [],
    }
    phase1_by_id = {item["test_id"]: item for item in phase1["documents"]}

    for index, entry in enumerate(entries, start=1):
        test_id, source = entry["test_id"], entry["source"]
        print(f"[{index}/{len(entries)}] {test_id}: Paged.js forward", flush=True)
        item: dict[str, Any] = {"testId": test_id, "source": _relative(source), "manifest": entry["manifest"]}
        try:
            paged_pdf = out / "pagedjs" / f"{test_id}.pdf"
            forward_path = out / "forward" / f"{test_id}.json"
            raw_path = out / "raw" / f"{test_id}.json"
            forward = run_pagedjs_forward(source, paged_pdf, forward_path, raw_path)
            paged_inspection = inspect_pdf(paged_pdf)
            backward_path = out / "backward" / f"{test_id}-pagedjs.json"
            started = time.perf_counter(); backward = generate_mapping(source, paged_pdf, backward_path, "pagedjs-pdfplumber"); backward_ms = round((time.perf_counter()-started)*1000,2)
            item["pagedjs"] = {"pdf": _relative(paged_pdf), "forwardMapping": _relative(forward_path), "backwardMapping": _relative(backward_path), "forward": forward, "backward": backward, "backwardProcessingTimeMs": backward_ms, "geometryCalibration": calibrate_geometry(forward, backward), "pdfInspection": paged_inspection}
        except Exception as exc:
            item["pagedjs"] = {"success": False, "error": repr(exc)}; results["failures"].append({"testId": test_id, "classification": "FORWARD_MAPPING", "error": repr(exc)})

        print(f"[{index}/{len(entries)}] {test_id}: WeasyPrint PDF/UA-2", flush=True)
        try:
            weasy_pdf = out / "weasyprint" / f"{test_id}.pdf"
            render = render_weasyprint(source, weasy_pdf, "pdf/ua-2")
            if not render.get("success"): raise RuntimeError(render.get("error"))
            backward_path = out / "backward" / f"{test_id}-weasyprint.json"
            started = time.perf_counter(); backward = generate_mapping(source, weasy_pdf, backward_path, "weasyprint-pdfplumber"); backward_ms = round((time.perf_counter()-started)*1000,2)
            item["weasyprint"] = {"pdf": _relative(weasy_pdf), "render": render, "backwardMapping": _relative(backward_path), "backward": backward, "backwardProcessingTimeMs": backward_ms}
        except Exception as exc:
            item["weasyprint"] = {"success": False, "error": repr(exc)}; results["failures"].append({"testId": test_id, "classification": "RENDERING", "renderer": "weasyprint", "error": repr(exc)})

        if test_id in {"T08", "T09"}:
            for renderer, pdf in [("chromium", ROOT / phase1_by_id[test_id]["pdf"]), ("pagedjs", ROOT / item["pagedjs"]["pdf"] if item.get("pagedjs", {}).get("pdf") else None), ("weasyprint", ROOT / item["weasyprint"]["pdf"] if item.get("weasyprint", {}).get("pdf") else None)]:
                if not pdf or not pdf.exists(): continue
                fidelity = extract_pdf_text(pdf, source)
                fidelity_path = out / "text" / f"{test_id}-{renderer}.json"; write_json(fidelity_path, fidelity)
                item.setdefault("pdfTextFidelity", {})[renderer] = {"result": _summary_text_fidelity(fidelity), "rawAndNormalizedOutput": _relative(fidelity_path), "toUnicode": inspect_tounicode(pdf), "actualTextCount": inspect_pdf(pdf).get("structure_actual_text_count",0)}
        if test_id in phase1_by_id:
            item["phase1BackwardCoverage"] = phase1_by_id[test_id]["mapping"]["coverage"]
            item["chromiumBaseline"] = {"pdf": phase1_by_id[test_id]["pdf"], "render": phase1_by_id[test_id]["render"]}
        results["documents"].append(item)

    r1 = next(item for item in results["documents"] if item["testId"] == "T10")
    r2 = next(item for item in results["documents"] if item["testId"] == "T10_R2_1B")
    if r1.get("pagedjs", {}).get("forward") and r2.get("pagedjs", {}).get("forward"):
        revision["oldMappingRejectedForR2"] = r1["pagedjs"]["forward"]["revision"] != r2["pagedjs"]["forward"]["revision"]
        revision["newFixedRendition"] = r1["pagedjs"]["forward"]["fixedRenditionHash"] != r2["pagedjs"]["forward"]["fixedRenditionHash"]
        revision["unchangedGeometry"] = _compare_revision_geometry(r1["pagedjs"]["forward"], r2["pagedjs"]["forward"], set(revision["targetNodeIds"]))

    print("EPUBCheck 5.3.0: 12 packages", flush=True)
    epub_outputs = ROOT / "reports" / "epubcheck-json" / "phase1b"; epub_outputs.mkdir(parents=True, exist_ok=True)
    original_packages = [ROOT / "corpus" / "packages" / f"T{i:02d}.epub" for i in range(1,13)]
    packages = []
    package_updates = []
    for original in original_packages:
        compatible = ROOT / "corpus" / "packages" / "phase1b" / original.name
        update = make_phase1b_compatible_epub(original, compatible)
        update["source"] = _relative(original); update["output"] = _relative(compatible)
        package_updates.append(update)
        packages.append(compatible)
    results["epubPackageUpdates"] = package_updates
    epub_results = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(run_epubcheck, package, epub_outputs / f"{package.stem}.json"): package for package in packages}
        for future in as_completed(futures):
            package = futures[future]
            try: epub_results.append({"testId": package.stem, **future.result()})
            except Exception as exc: epub_results.append({"testId": package.stem, "status": "FAIL", "error": repr(exc)})
    results["epubcheck"] = sorted(epub_results, key=lambda item:item["testId"])

    original_outputs = ROOT / "reports" / "epubcheck-json" / "phase1-original"; original_outputs.mkdir(parents=True, exist_ok=True)
    original_results = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(run_epubcheck, package, original_outputs / f"{package.stem}.json"): package for package in original_packages}
        for future in as_completed(futures):
            package = futures[future]
            try: original_results.append({"testId": package.stem, **future.result()})
            except Exception as exc: original_results.append({"testId": package.stem, "status": "FAIL", "error": repr(exc)})
    results["epubcheckOriginalPhase1Packages"] = sorted(original_results, key=lambda item:item["testId"])

    print("epub.js + Foliate JS readers: 12 packages", flush=True)
    results["epubReaders"] = [_run_epubjs(packages), _run_foliate(packages)]
    calibre_result = ROOT / "reports" / "calibre_reader_results.json"
    if calibre_result.exists():
        results["epubReaders"].append(json.loads(calibre_result.read_text(encoding="utf-8")))

    print("veraPDF 1.30.2: representative profile matrix", flush=True)
    docs = {item["testId"]: item for item in results["documents"]}
    jobs = []
    for test_id in ("T03","T08","T09","T10","T12"):
        for renderer in ("chromium","pagedjs","weasyprint"):
            if renderer == "chromium": pdf = ROOT / phase1_by_id[test_id]["pdf"]
            else:
                value = docs[test_id].get(renderer, {}); pdf = ROOT / value["pdf"] if value.get("pdf") else None
            if pdf and pdf.exists(): jobs.append((test_id,renderer,pdf,"ua2"))
    for test_id in ("T08","T10"):
        for renderer in ("chromium","pagedjs","weasyprint"):
            pdf = ROOT / phase1_by_id[test_id]["pdf"] if renderer=="chromium" else ROOT / docs[test_id][renderer]["pdf"]
            jobs.extend([(test_id,renderer,pdf,"wt1r"),(test_id,renderer,pdf,"wt1a")])
    for renderer in ("chromium","pagedjs","weasyprint"):
        pdf = ROOT / phase1_by_id["T10"]["pdf"] if renderer=="chromium" else ROOT / docs["T10"][renderer]["pdf"]
        jobs.append(("T10",renderer,pdf,"4"))
    validations = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(run_verapdf,pdf,profile):(test_id,renderer,pdf,profile) for test_id,renderer,pdf,profile in jobs}
        for future in as_completed(futures):
            test_id,renderer,pdf,profile=futures[future]
            try: validations.append({"testId":test_id,"renderer":renderer,"pdf":_relative(pdf),**future.result()})
            except Exception as exc: validations.append({"testId":test_id,"renderer":renderer,"profile":profile,"compliant":False,"error":repr(exc)})

    a4_temp = ROOT / ".phase1b" / "tmp" / "T10-weasyprint-pdfa4u.pdf"
    a4_render = render_weasyprint(ROOT / "corpus" / "sources" / "T10.xhtml", a4_temp, "pdf/a-4u")
    results["weasyprintPdfA4uExperiment"] = {"render": a4_render, "validation": run_verapdf(a4_temp,"4") if a4_render.get("success") else None}
    if a4_temp.exists(): a4_temp.unlink()
    results["pdfValidation"] = sorted(validations,key=lambda item:(item["testId"],item["renderer"],item["profile"]))

    visual_qa = ROOT / "reports" / "visual_qa_phase1b.json"
    if visual_qa.exists():
        results["visualQA"] = json.loads(visual_qa.read_text(encoding="utf-8"))

    write_json(ROOT / "reports" / "results_phase1b.json", results)
    write_phase1b_reports(ROOT, results)
    print(json.dumps({"documents":len(results["documents"]),"failures":len(results["failures"]),"phase1bResults":str(ROOT/'reports'/'results_phase1b.json')},indent=2),flush=True)
    return 0 if not any(item.get("classification") == "FORWARD_MAPPING" for item in results["failures"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
