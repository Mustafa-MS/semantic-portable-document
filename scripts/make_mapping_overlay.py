from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw


def bbox(quad: list[float]) -> tuple[float, float, float, float]:
    return min(quad[0::2]), min(quad[1::2]), max(quad[0::2]), max(quad[1::2])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mapping", type=Path)
    parser.add_argument("page_png", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--page", type=int, default=1)
    args = parser.parse_args()

    mapping = json.loads(args.mapping.read_text(encoding="utf-8"))
    page_id = f"pg_{args.page}"
    page = next(item for item in mapping["pages"] if item["id"] == page_id)
    image = Image.open(args.page_png).convert("RGBA")
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    sx, sy = image.width / page["width"], image.height / page["height"]
    block_count = range_count = 0
    for record in mapping["records"]:
        for fragment in record["fragments"]:
            if fragment["page"] != page_id:
                continue
            x0, y0, x1, y1 = bbox(fragment["quad"])
            rect = (round(x0 * sx), round(y0 * sy), round(x1 * sx), round(y1 * sy))
            if fragment["type"] == "text-range":
                draw.rectangle(rect, outline=(155, 35, 190, 180), width=1)
                range_count += 1
            else:
                draw.rectangle(rect, outline=(0, 135, 90, 230), width=3)
                block_count += 1
    composed = Image.alpha_composite(image, overlay).convert("RGB")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    composed.save(args.output)
    print(json.dumps({"page": page_id, "blocks": block_count, "textRanges": range_count, "output": str(args.output)}))


if __name__ == "__main__":
    main()
