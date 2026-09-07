from __future__ import annotations

import re
import unicodedata
import uuid
from collections import defaultdict
from pathlib import Path
from typing import Any

import pdfplumber
from lxml import etree

from harness.util import normalize_text, sha256_file, write_json


ADDRESSABLE = {"article", "section", "main", "nav", "header", "footer", "h1", "h2", "h3", "p", "ul", "ol", "li", "table", "caption", "tr", "th", "td", "figure", "figcaption", "math", "aside", "div"}


def _token(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    return re.sub(r"^[^\w\d]+|[^\w\d.=%]+$", "", value, flags=re.UNICODE)


def _node_text(element: etree._Element) -> str:
    return normalize_text(" ".join(piece for piece in element.itertext()))


def _source_tokens(text: str) -> list[tuple[str, int, int]]:
    result = []
    for match in re.finditer(r"\S+", text):
        value = _token(match.group())
        if value:
            result.append((value, match.start(), match.end()))
    return result


def _find_subsequence(haystack: list[str], needle: list[str], start: int = 0) -> int:
    if not needle:
        return -1
    first = needle[0]
    for i in range(start, len(haystack) - len(needle) + 1):
        if haystack[i] == first and haystack[i:i + len(needle)] == needle:
            return i
    return -1


def generate_mapping(source: Path, pdf: Path, output: Path, renderer: str) -> dict[str, Any]:
    tree = etree.parse(str(source))
    revision = tree.xpath('string(//*[local-name()="meta"][@name="revision-id"]/@content)')
    document_id = tree.xpath('string(//*[local-name()="meta"][@name="document-id"]/@content)')
    words: list[dict[str, Any]] = []
    images_by_page: dict[int, list[dict[str, Any]]] = defaultdict(list)
    page_sizes: dict[int, tuple[float, float]] = {}
    with pdfplumber.open(pdf) as fixed:
        for page_number, page in enumerate(fixed.pages, start=1):
            page_sizes[page_number] = (float(page.width), float(page.height))
            for word in page.extract_words(use_text_flow=True, keep_blank_chars=False):
                token = _token(str(word["text"]))
                # Generated page counters are fixed-scene furniture, not semantic source text.
                # Keeping them in the logical token stream breaks otherwise contiguous nodes at
                # page boundaries (the exact case T02 is designed to expose).
                is_page_counter = token.isdigit() and float(word["top"]) > float(page.height) - 40
                if token and not is_page_counter:
                    words.append({**word, "token": token, "page": page_number})
            for image in page.images:
                images_by_page[page_number].append(image)
    word_tokens = [word["token"] for word in words]
    mappings: list[dict[str, Any]] = []
    unmatched: list[dict[str, str]] = []
    cursor_by_text: dict[str, int] = defaultdict(int)

    for element in tree.xpath('//*[@data-node-id]'):
        local = etree.QName(element).localname
        if local not in ADDRESSABLE:
            continue
        node_id = element.get("data-node-id")
        text = _node_text(element)
        source_tokens = _source_tokens(text)
        needle = [item[0] for item in source_tokens]
        # Very large *ancestor* nodes are not forced into a single exact token match. Large leaf
        # paragraphs are essential: T02 deliberately verifies one semantic node -> many pages.
        addressable_descendants = [child for child in element.xpath('.//*[@data-node-id]') if etree.QName(child).localname in ADDRESSABLE]
        if len(needle) > 350 and addressable_descendants:
            unmatched.append({"node": node_id, "reason": "ancestor text exceeds exact-match experiment limit"})
            continue
        start = _find_subsequence(word_tokens, needle, cursor_by_text[text])
        if start < 0 and local == "figure":
            caption = next((c for c in element.xpath('.//*[local-name()="figcaption"]')), None)
            caption_text = _node_text(caption) if caption is not None else ""
            cap_tokens = [item[0] for item in _source_tokens(caption_text)]
            cap_start = _find_subsequence(word_tokens, cap_tokens)
            if cap_start >= 0:
                page_number = words[cap_start]["page"]
                if images_by_page.get(page_number):
                    image = images_by_page[page_number][0]
                    height = page_sizes[page_number][1]
                    mappings.append({"node": node_id, "kind": "figure", "fragments": [{
                        "page": f"pg_{page_number}", "quad": [float(image["x0"]), height-float(image["y1"]), float(image["x1"]), height-float(image["y1"]), float(image["x1"]), height-float(image["y0"]), float(image["x0"]), height-float(image["y0"])],
                    }]})
                    continue
        if start < 0:
            unmatched.append({"node": node_id, "reason": "logical token sequence not found in extracted PDF words"})
            continue
        cursor_by_text[text] = start + len(needle)
        selected = words[start:start + len(needle)]
        by_page: dict[int, list[tuple[dict[str, Any], tuple[str, int, int]]]] = defaultdict(list)
        for word, source_token in zip(selected, source_tokens):
            by_page[word["page"]].append((word, source_token))
        fragments = []
        for page_number, pairs in by_page.items():
            page_words = [pair[0] for pair in pairs]
            token_ranges = [pair[1] for pair in pairs]
            x0 = min(float(word["x0"]) for word in page_words)
            x1 = max(float(word["x1"]) for word in page_words)
            top = min(float(word["top"]) for word in page_words)
            bottom = max(float(word["bottom"]) for word in page_words)
            fragments.append({
                "page": f"pg_{page_number}",
                "textRange": [min(item[1] for item in token_ranges), max(item[2] for item in token_ranges)],
                "quad": [x0, top, x1, top, x1, bottom, x0, bottom],
            })
        kind = "table-cell" if local in {"td", "th"} else "figure" if local == "figure" else "text" if text else "block"
        mappings.append({"node": node_id, "kind": kind, "fragments": fragments})

    expected = [el.get("data-node-id") for el in tree.xpath('//*[@data-node-id]') if etree.QName(el).localname in ADDRESSABLE]
    result = {
        "schemaVersion": "0.1-experimental",
        "document": document_id,
        "revision": revision,
        "fixedRendition": "f_" + uuid.uuid4().hex,
        "fixedRenditionHash": sha256_file(pdf),
        "renderer": renderer,
        "pages": [{"id": f"pg_{number}", "width": size[0], "height": size[1], "unit": "pt"} for number, size in page_sizes.items()],
        "mappings": mappings,
        "coverage": {"mapped": len({item['node'] for item in mappings}), "expected": len(expected), "ratio": round(len({item['node'] for item in mappings}) / len(expected), 4) if expected else 1.0},
        "unmatched": unmatched,
    }
    write_json(output, result)
    return result
