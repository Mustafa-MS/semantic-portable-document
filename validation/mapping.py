from __future__ import annotations

from pathlib import Path
from typing import Any

from lxml import etree

from harness.util import sha256_file


def validate_mapping(mapping: dict[str, Any], source: Path, pdf: Path) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    tree = etree.parse(str(source))
    revision = tree.xpath('string(//*[local-name()="meta"][@name="revision-id"]/@content)')
    node_ids = set(tree.xpath('//*[@data-node-id]/@data-node-id'))
    pages = {page["id"]: page for page in mapping.get("pages", [])}
    if mapping.get("revision") != revision:
        errors.append({"code": "WRONG_REVISION", "message": "mapping revision does not match semantic source"})
    if mapping.get("fixedRenditionHash") != sha256_file(pdf):
        errors.append({"code": "WRONG_FIXED_HASH", "message": "fixed rendition hash mismatch"})
    seen: set[tuple[str, str, str]] = set()
    for item in mapping.get("mappings", []):
        node = item.get("node")
        if node not in node_ids:
            errors.append({"code": "UNKNOWN_NODE", "message": str(node)})
        element = tree.xpath(f'//*[@data-node-id="{node}"]') if node in node_ids else []
        text_length = len(" ".join(element[0].itertext()).strip()) if element else 0
        for fragment in item.get("fragments", []):
            page_id = fragment.get("page")
            if page_id not in pages:
                errors.append({"code": "UNKNOWN_PAGE", "message": str(page_id)})
                continue
            quad = fragment.get("quad", [])
            signature = (str(node), str(page_id), str(quad))
            if signature in seen:
                errors.append({"code": "DUPLICATE_MAPPING", "message": str(signature)})
            seen.add(signature)
            if len(quad) != 8:
                errors.append({"code": "INVALID_QUAD", "message": str(node)})
            elif min(quad) < 0 or max(quad[0::2]) > pages[page_id]["width"] + 1 or max(quad[1::2]) > pages[page_id]["height"] + 1:
                errors.append({"code": "OUT_OF_BOUNDS", "message": str(node)})
            if "textRange" in fragment:
                start, end = fragment["textRange"]
                if not (0 <= start < end <= text_length):
                    errors.append({"code": "TEXT_RANGE_MISMATCH", "message": str(node)})
    return {"valid": not errors, "errors": errors, "error_count": len(errors)}

