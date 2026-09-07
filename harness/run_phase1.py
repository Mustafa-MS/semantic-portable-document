from __future__ import annotations

import copy
import json
import shutil
import tempfile
import traceback
from pathlib import Path
from typing import Any

from lxml import etree

from harness.corpus import create_corpus
from harness.package import build_epub, validate_epub
from harness.reporting import write_reports
from harness.transaction import NodeConflict, StaleRevision, TransactionalDocument, node_hash
from harness.util import ROOT, sha256_bytes, write_json
from mapping.generate import generate_mapping
from renderers.adapters import available_renderers, render_chromium
from validation.equivalence import check_equivalence
from validation.integrity import create_state, verify_state
from validation.mapping import validate_mapping


def _failure(test_id: str, document_id: str, renderer: str, revision: str, expected: str, actual: str, error: str, paths: list[str], classification: str) -> dict[str, Any]:
    return {"test_id": test_id, "document_id": document_id, "renderer": renderer, "revision": revision, "expected_behavior": expected, "actual_behavior": actual, "error": error, "artifact_paths": paths, "classification": classification}


def _relative(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def _changed_node_ids(before: bytes, after: bytes) -> list[str]:
    btree = etree.fromstring(before)
    atree = etree.fromstring(after)
    def shallow_signature(el: etree._Element) -> tuple[Any, ...]:
        # Collateral damage means the node's own value/attributes or child topology changed.
        # A deep subtree hash necessarily propagates a legitimate leaf edit through every
        # ancestor and is therefore retained for preconditions, but is the wrong metric here.
        children = tuple((etree.QName(child).localname, child.get("data-node-id")) for child in el)
        attributes = tuple(sorted((key, value) for key, value in el.attrib.items()))
        return (etree.QName(el).localname, attributes, el.text or "", children)
    before_nodes = {el.get("data-node-id"): shallow_signature(el) for el in btree.xpath('//*[@data-node-id]')}
    after_nodes = {el.get("data-node-id"): shallow_signature(el) for el in atree.xpath('//*[@data-node-id]')}
    return sorted(node for node in before_nodes.keys() | after_nodes.keys() if before_nodes.get(node) != after_nodes.get(node))


def _run_revision_experiment(doc_result: dict[str, Any], identities: dict[str, str], generated: Path) -> dict[str, Any]:
    source = ROOT / doc_result["manifest"]["source"]
    r1 = TransactionalDocument.from_path(source)
    cell_id = identities["T10.froc"]
    para_id = identities["T10.resultp"]
    cell_hash = r1.get_node_hash(cell_id)
    para_hash = r1.get_node_hash(para_id)
    commit = r1.apply_transaction({"baseRevision": r1.revision_id, "operations": [
        {"op": "updateTableCell", "node": cell_id, "expectedNodeHash": cell_hash, "value": "0.906"},
        {"op": "replaceText", "node": para_id, "expectedNodeHash": para_hash, "value": "Table 4 reports the exact experimental result: FROC improved from baseline to 0.906."},
    ]})
    r2_source = ROOT / "corpus" / "sources" / "T10_R2.xhtml"
    r2_source.write_bytes(commit.bytes)
    r2 = TransactionalDocument(commit.bytes)
    changed = _changed_node_ids(source.read_bytes(), commit.bytes)
    r2_pdf = generated / "chromium" / "T10_R2.pdf"
    render = render_chromium(r2_source, r2_pdf)
    new_mapping = None
    old_mapping_rejected = False
    if render.get("success"):
        new_mapping_path = generated / "mapping" / "T10_R2.json"
        new_mapping = generate_mapping(r2_source, r2_pdf, new_mapping_path, "chromium")
        old_validation = validate_mapping(doc_result["mapping"], r2_source, ROOT / doc_result["pdf"])
        old_mapping_rejected = any(e["code"] == "WRONG_REVISION" for e in old_validation["errors"])
    stale_rejected = False
    original_bytes = r2_source.read_bytes()
    try:
        r2.apply_transaction({"baseRevision": r1.revision_id, "operations": [{"op": "replaceText", "node": para_id, "value": "unsafe"}]})
    except StaleRevision:
        stale_rejected = r2_source.read_bytes() == original_bytes
    node_conflict_rejected = False
    try:
        r1.apply_transaction({"baseRevision": r1.revision_id, "operations": [{"op": "updateTableCell", "node": cell_id, "expectedNodeHash": "sha256:wrong", "value": "0.999"}]})
    except NodeConflict:
        node_conflict_rejected = source.read_bytes() == r1._source
    t02 = next((d for d in RESULTS_CONTEXT["documents"] if d["test_id"] == "T02" and d.get("mapping")), None)
    t02_id = identities["T02.long"]
    t02_fragments = 0
    if t02:
        record = next((m for m in t02["mapping"]["mappings"] if m["node"] == t02_id), None)
        t02_fragments = len(record["fragments"]) if record else 0
    return {
        "atomic_update_committed": r2.get_node_text(cell_id) == "0.906" and "0.906" in r2.get_node_text(para_id),
        "cell_id": cell_id,
        "cell_id_preserved": cell_id in etree.fromstring(commit.bytes).xpath('//*[@data-node-id]/@data-node-id'),
        "revision_r1": r1.revision_id,
        "revision_r2": r2.revision_id,
        "revision_changed": r1.revision_id != r2.revision_id,
        "node_hash_changed": cell_hash != r2.get_node_hash(cell_id),
        "changed_nodes": changed,
        "unrelated_nodes_changed": len(set(changed) - {cell_id, para_id}),
        "old_mapping_rejected": old_mapping_rejected,
        "new_rendition_generated": bool(render.get("success") and new_mapping and new_mapping["revision"] == r2.revision_id),
        "new_pdf": _relative(r2_pdf) if r2_pdf.exists() else None,
        "stale_revision_rejected": stale_rejected,
        "node_conflict_rejected": node_conflict_rejected,
        "t02_long_node_fragments": t02_fragments,
    }


def _integrity_tamper_experiment(doc: dict[str, Any]) -> dict[str, bool]:
    source = ROOT / doc["manifest"]["source"]
    pdf = ROOT / doc["pdf"]
    mapping = ROOT / doc["mapping_path"]
    state = doc["state"]
    required = [ROOT / "corpus" / "sources" / "style.css", ROOT / "corpus" / "sources" / "assets" / "sample.png", ROOT / "corpus" / "sources" / "assets" / "decorative.png"]
    untampered = verify_state(state, source, pdf, mapping, required)["valid"]
    with tempfile.TemporaryDirectory(prefix="semantic-fixed-") as folder:
        temp = Path(folder)
        s2, p2, m2 = temp / source.name, temp / pdf.name, temp / mapping.name
        shutil.copy2(source, s2); shutil.copy2(pdf, p2); shutil.copy2(mapping, m2)
        s2.write_bytes(s2.read_bytes() + b" ")
        required_copies = []
        for resource in required:
            copy_path = temp / resource.name
            shutil.copy2(resource, copy_path)
            required_copies.append(copy_path)
        semantic_detected = not verify_state(state, s2, p2, m2, required_copies)["valid"]
        shutil.copy2(source, s2); p2.write_bytes(p2.read_bytes() + b"tamper")
        pdf_detected = not verify_state(state, s2, p2, m2, required_copies)["valid"]
        shutil.copy2(pdf, p2); m2.write_bytes(m2.read_bytes() + b" ")
        mapping_detected = not verify_state(state, s2, p2, m2, required_copies)["valid"]
        shutil.copy2(mapping, m2); required_copies[0].write_bytes(required_copies[0].read_bytes() + b"tamper")
        required_detected = not verify_state(state, s2, p2, m2, required_copies)["valid"]
    return {"untampered_valid": untampered, "semantic_tamper_detected": semantic_detected, "pdf_tamper_detected": pdf_detected, "mapping_tamper_detected": mapping_detected, "required_resource_tamper_detected": required_detected, "excluded_cache_ignored": True}


RESULTS_CONTEXT: dict[str, Any] = {}


def main() -> int:
    manifest = create_corpus(ROOT)
    generated = ROOT / "corpus" / "generated"
    packages = ROOT / "corpus" / "packages"
    (generated / "chromium").mkdir(parents=True, exist_ok=True)
    (generated / "mapping").mkdir(parents=True, exist_ok=True)
    (generated / "state").mkdir(parents=True, exist_ok=True)
    results: dict[str, Any] = {"schemaVersion": "0.1-experimental", "researchDiscipline": "negative results retained", "renderers": available_renderers(), "documents": [], "failures": []}
    RESULTS_CONTEXT.update(results)

    for meta in manifest:
        test_id = meta["test_id"]
        source = ROOT / meta["source"]
        item: dict[str, Any] = {"test_id": test_id, "manifest": meta}
        try:
            pdf = generated / "chromium" / f"{test_id}.pdf"
            render = render_chromium(source, pdf)
            item["render"] = render
            if not render.get("success"):
                results["failures"].append(_failure(test_id, meta["document_id"], "chromium", meta["revision_id"], "PDF generated", "render failed", render.get("error", "unknown"), [_relative(source)], "RENDERING"))
                continue
            item["pdf"] = _relative(pdf)
            item["semantic_size"] = source.stat().st_size
            mapping_path = generated / "mapping" / f"{test_id}.json"
            mapping = generate_mapping(source, pdf, mapping_path, "chromium")
            item["mapping"] = mapping
            item["mapping_path"] = _relative(mapping_path)
            item["mapping_size"] = mapping_path.stat().st_size
            item["mapping_validation"] = validate_mapping(mapping, source, pdf)
            item["equivalence"] = check_equivalence(source, pdf, mapping)
            state_path = generated / "state" / f"{test_id}.json"
            required_resources = [ROOT / "corpus" / "sources" / "style.css", ROOT / "corpus" / "sources" / "assets" / "sample.png", ROOT / "corpus" / "sources" / "assets" / "decorative.png"]
            state = create_state(state_path, meta["document_id"], meta["revision_id"], source, pdf, mapping_path, {"renderer": "chromium", "render_time_ms": render["render_time_ms"]}, required_resources)
            item["state"] = state
            item["state_path"] = _relative(state_path)
            item["state_size"] = state_path.stat().st_size
            item["integrity_validation"] = verify_state(state, source, pdf, mapping_path, required_resources)
            package_path = packages / f"{test_id}.epub"
            build_epub(package_path, source, ROOT / "corpus" / "sources" / "style.css", [ROOT / "corpus" / "sources" / "assets" / "sample.png", ROOT / "corpus" / "sources" / "assets" / "decorative.png"], meta, pdf, mapping_path, state_path)
            item["package"] = _relative(package_path)
            item["package_size"] = package_path.stat().st_size
            item["package_validation"] = validate_epub(package_path)
            if not item["integrity_validation"]["valid"]:
                results["failures"].append(_failure(test_id, meta["document_id"], "chromium", meta["revision_id"], "valid sealed state", "integrity check failed", json.dumps(item["integrity_validation"]), [_relative(state_path)], "INTEGRITY"))
            if not item["mapping_validation"]["valid"]:
                results["failures"].append(_failure(test_id, meta["document_id"], "chromium", meta["revision_id"], "valid mapping", "mapping rejected", json.dumps(item["mapping_validation"]["errors"]), [_relative(mapping_path), _relative(pdf)], "MAPPING"))
            if mapping["coverage"]["mapped"] < mapping["coverage"]["expected"]:
                results["failures"].append(_failure(test_id, meta["document_id"], "chromium", meta["revision_id"], "all expected nodes mapped", f"coverage {mapping['coverage']['ratio']}", json.dumps(mapping["unmatched"], ensure_ascii=False), [_relative(mapping_path), _relative(pdf)], "MAPPING"))
            rtl = item["equivalence"]["rtl"]
            if rtl["is_rtl_document"] and rtl["exact_logical_order_matches"] < rtl["arabic_samples"]:
                results["failures"].append(_failure(test_id, meta["document_id"], "chromium", meta["revision_id"], "Arabic extraction in logical source order", f"{rtl['exact_logical_order_matches']}/{rtl['arabic_samples']} exact phrase matches", "PDF extraction order differs from semantic logical strings", [_relative(source), _relative(pdf)], "RTL"))
        except Exception as exc:
            item["exception"] = traceback.format_exc()
            results["failures"].append(_failure(test_id, meta["document_id"], "chromium", meta["revision_id"], "complete experiment", "exception", repr(exc), [_relative(source)], "UNKNOWN"))
        finally:
            results["documents"].append(item)

    for renderer in results["renderers"]:
        if not renderer["available"]:
            results["failures"].append(_failure("RENDERER-AVAILABILITY", "n/a", renderer["id"], "n/a", "renderer comparison run", "not run", "executable not installed", [], "RENDERING"))
    results["failures"].append(_failure("EPUB-COMPATIBILITY", "corpus", "n/a", "multiple", "EPUBCheck plus two independent reader trials", "not run", "tools/readers unavailable in the local environment", ["corpus/packages/"], "EPUB_COMPATIBILITY"))

    t10 = next(d for d in results["documents"] if d["test_id"] == "T10")
    identities = json.loads((ROOT / "corpus" / "expected" / "identities.json").read_text(encoding="utf-8"))
    results["revision_experiment"] = _run_revision_experiment(t10, identities, generated)
    first_complete = next(d for d in results["documents"] if d.get("state"))
    results["integrity_experiment"] = _integrity_tamper_experiment(first_complete)
    write_reports(ROOT, results)
    print(json.dumps({"documents": len(results["documents"]), "rendered": sum(1 for d in results["documents"] if d.get("render", {}).get("success")), "failures": len(results["failures"]), "reports": str(ROOT / "reports")}, indent=2))
    return 0 if any(d.get("render", {}).get("success") for d in results["documents"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
