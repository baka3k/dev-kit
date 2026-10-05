#!/usr/bin/env python3
"""Render a .pptx to per-slide PNGs + a contact sheet for visual QA.

On macOS with Microsoft PowerPoint installed, exports PDF via AppleScript
(faithful fonts: real Calibri). Falls back to `soffice` if PowerPoint is absent.

Usage:
    python3 render_preview.py deck.pptx --output-dir preview [--dpi 130] [--cols 4]
"""

from __future__ import annotations

import argparse
import math
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def _hfs_path(p: Path) -> str:
    """'/tmp/x.pdf' -> 'Macintosh HD:tmp:x.pdf' (PowerPoint AppleScript wants HFS)."""
    parts = [q for q in p.parts if q not in ("/",)]
    return "Macintosh HD:" + ":".join(parts)


def export_pdf_pptx(pptx: Path, pdf: Path) -> None:
    hfs_pdf = _hfs_path(pdf.resolve())
    script = f'''
tell application "Microsoft PowerPoint"
    open (POSIX file "{pptx.resolve()}")
    delay 1
    set pres to active presentation
    save pres in "{hfs_pdf}" as save as PDF
    close pres saving no
end tell
'''
    res = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if res.returncode or not pdf.is_file():
        raise RuntimeError(
            f"PowerPoint export failed: {res.stderr or res.stdout or 'no PDF produced'}")


def export_pdf_soffice(pptx: Path, pdf: Path) -> None:
    soffice = shutil.which("soffice")
    if not soffice:
        raise SystemExit("Neither Microsoft PowerPoint nor LibreOffice (soffice) available for rendering.")
    res = subprocess.run([soffice, "--headless", "--convert-to", "pdf",
                          "--outdir", str(pdf.parent), str(pptx.resolve())],
                         capture_output=True, text=True)
    if res.returncode or not pdf.is_file():
        raise RuntimeError(f"soffice failed: {res.stderr or res.stdout}")


def contact_sheet(images: list[Path], output: Path, cols: int) -> None:
    thumb_w, thumb_h, label_h, gap = 480, 270, 26, 16
    rows = math.ceil(len(images) / cols)
    canvas = Image.new("RGB", (gap + cols * (thumb_w + gap),
                               gap + rows * (thumb_h + label_h + gap)), "#E8EAED")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()
    for i, p in enumerate(images, 1):
        row, col = divmod(i - 1, cols)
        x = gap + col * (thumb_w + gap)
        y = gap + row * (thumb_h + label_h + gap)
        with Image.open(p) as im:
            thumb = im.convert("RGB")
            thumb.thumbnail((thumb_w, thumb_h))
            canvas.paste(thumb, (x + (thumb_w - thumb.width) // 2,
                                 y + label_h + (thumb_h - thumb.height) // 2))
        draw.text((x, y + 5), f"Slide {i}", fill="#1E293B", font=font)
    canvas.save(output, quality=90)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pptx", type=Path)
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--dpi", type=int, default=120)
    ap.add_argument("--cols", type=int, default=4)
    ap.add_argument("--keep-pdf", action="store_true")
    args = ap.parse_args()

    if not args.pptx.is_file():
        raise SystemExit(f"not found: {args.pptx}")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    pdf = args.output_dir / (args.pptx.stem + ".pdf")
    if pdf.exists():
        pdf.unlink()

    have_ppt = Path("/Applications/Microsoft PowerPoint.app").exists()
    try:
        if have_ppt:
            export_pdf_pptx(args.pptx.resolve(), pdf.resolve())
        else:
            export_pdf_soffice(args.pptx, pdf)
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        return 1

    import pymupdf
    doc = pymupdf.open(str(pdf))
    zoom = args.dpi / 72.0
    mat = pymupdf.Matrix(zoom, zoom)
    images = []
    for i, page in enumerate(doc):
        out = args.output_dir / f"slide-{i + 1:02d}.png"
        page.get_pixmap(matrix=mat).save(str(out))
        images.append(out)
    doc.close()

    sheet = args.output_dir / "contact-sheet.jpg"
    contact_sheet(images, sheet, args.cols)
    print(f"rendered {len(images)} slides -> {args.output_dir}")
    print(f"contact sheet: {sheet}")
    if not args.keep_pdf and pdf.exists():
        pdf.unlink()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
