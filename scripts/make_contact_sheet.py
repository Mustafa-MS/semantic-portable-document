from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--columns", type=int, default=4)
    parser.add_argument("--cell-width", type=int, default=320)
    parser.add_argument("--cell-height", type=int, default=470)
    args = parser.parse_args()
    files = sorted(args.input.glob("*.png"))
    if not files:
        raise SystemExit("no PNGs found")
    label_height = 32
    rows = (len(files) + args.columns - 1) // args.columns
    sheet = Image.new("RGB", (args.columns * args.cell_width, rows * (args.cell_height + label_height)), "#d9e0e3")
    draw = ImageDraw.Draw(sheet)
    for index, path in enumerate(files):
        image = Image.open(path).convert("RGB")
        thumbnail = ImageOps.contain(image, (args.cell_width - 16, args.cell_height - 16))
        column, row = index % args.columns, index // args.columns
        x = column * args.cell_width + (args.cell_width - thumbnail.width) // 2
        y = row * (args.cell_height + label_height) + 8
        sheet.paste(thumbnail, (x, y))
        draw.text((column * args.cell_width + 8, y + args.cell_height), path.stem, fill="#17242b")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output)


if __name__ == "__main__":
    main()

