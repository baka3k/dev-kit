#!/usr/bin/env python3
"""Render every PPTX slide to PNG and create a labeled contact sheet."""

from __future__ import annotations

import argparse
import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation


def require_binary(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise SystemExit(f"Required executable not found: {name}")
    return path


def run(command: list[str]) -> None:
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode:
        message = (result.stderr or result.stdout).strip()
        raise SystemExit(f"Command failed: {' '.join(command)}\n{message}")


def build_contact_sheet(images: list[Path], output: Path, cols: int) -> None:
    thumb_w, thumb_h, label_h, gap = 480, 270, 28, 18
    rows = math.ceil(len(images) / cols)
    canvas = Image.new(
        "RGB",
        (
            gap + cols * (thumb_w + gap),
            gap + rows * (thumb_h + label_h + gap),
        ),
        "white",
    )
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()
    for index, image_path in enumerate(images, start=1):
        row, col = divmod(index - 1, cols)
        x = gap + col * (thumb_w + gap)
        y = gap + row * (thumb_h + label_h + gap)
        with Image.open(image_path) as source:
            thumb = source.convert("RGB")
            thumb.thumbnail((thumb_w, thumb_h))
            px = x + (thumb_w - thumb.width) // 2
            py = y + label_h + (thumb_h - thumb.height) // 2
            canvas.paste(thumb, (px, py))
        draw.text((x, y + 6), f"Slide {index}", fill="#1E293B", font=font)
    canvas.save(output, quality=92)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--dpi", type=int, default=144)
    parser.add_argument("--cols", type=int, default=4, choices=range(3, 7))
    parser.add_argument("--keep-pdf", action="store_true")
    args = parser.parse_args()

    if not args.pptx.is_file():
        parser.error(f"File not found: {args.pptx}")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    soffice = require_binary("soffice")
    pdftoppm = require_binary("pdftoppm")
    run(
        [
            soffice,
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(args.output_dir),
            str(args.pptx.resolve()),
        ]
    )
    pdf_path = args.output_dir / f"{args.pptx.stem}.pdf"
    if not pdf_path.is_file():
        raise SystemExit(f"LibreOffice did not create: {pdf_path}")

    prefix = args.output_dir / "slide"
    run([pdftoppm, "-png", "-r", str(args.dpi), str(pdf_path), str(prefix)])
    images = sorted(args.output_dir.glob("slide-*.png"))
    expected = len(Presentation(str(args.pptx)).slides)
    if len(images) != expected:
        raise SystemExit(f"Rendered {len(images)} slides; expected {expected}")

    contact_sheet = args.output_dir / "contact-sheet.jpg"
    build_contact_sheet(images, contact_sheet, args.cols)
    if not args.keep_pdf:
        pdf_path.unlink()
    print(f"Rendered {len(images)} slides")
    print(f"Contact sheet: {contact_sheet}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
