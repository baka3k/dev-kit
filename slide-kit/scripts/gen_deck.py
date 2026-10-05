#!/usr/bin/env python3
"""Generate a .pptx deck in the navy/teal corporate style from a JSON spec.

Usage:
    python3 gen_deck.py spec.json -o deck.pptx

Brand-neutral by design: no logos are placed on any slide.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Length, Pt

# ---------------------------------------------------------------- constants

SLIDE_W, SLIDE_H = 960.0, 540.0          # pt (16:9)
BAND_H = 60.0                            # header band height on content slides
BODY_TOP, BODY_BOTTOM = 72.0, 520.0      # usable body area on content slides
GAP = 10.0                               # vertical gap between body blocks

ASSETS = Path(__file__).resolve().parent.parent / "assets"

INK = "29333A"        # body text
WHITE = "FFFFFF"
TEAL = "32B2C1"       # table headers, accents
TEAL_DARK = "0F4950"
TINT_L = "E8F2F4"     # zebra row light
TINT_M = "CDE4E9"     # zebra row dark
GREEN = "00B050"      # positive / done
GREEN_L = "92D050"    # legend "phase 1"
BLUE_L = "73B5FF"     # legend "phase 2"
CHIP_G = "A7FFCF"     # sitemap chip green
CHIP_B = "C9DCFF"     # sitemap chip blue
ORANGE = "F88728"     # accent / update
PEACH = "FDE0C0"      # update highlight fill
RED = "E02020"        # warnings / "tobe update"
GRAY = "7F7F7F"       # page numbers
BORDER = "BFBFBF"     # card borders
LEGEND_BG = "D9D9D9"  # legend band
NAVY_LINE = "2E6FBE"  # agenda pill outline
LINK = "1155CC"       # link-style text

CODE_TEXT = "3B4249"
CODE_KEY = "E06C75"
CODE_STR = "98C379"
CODE_COM = "7F848E"
CODE_NUM = "D19A66"
CODE_BORDER = "2E75B6"

F_MAIN = "Calibri"
F_CODE = "Menlo"
F_DATE = "Segoe UI"

MARKUP_RE = re.compile(r"(\*\*.+?\*\*|\[\[[a-z]+\|.+?\]\])", re.S)
NAMED_COLORS = {
    "red": RED, "green": GREEN, "orange": ORANGE, "teal": TEAL,
    "tealdark": TEAL_DARK, "blue": LINK, "gray": GRAY, "white": WHITE, "ink": INK,
}

warnings: list[str] = []

SPEC_DIR = Path.cwd()  # set in main(); relative asset paths resolve against it


def warn(msg: str) -> None:
    warnings.append(msg)
    print(f"[warn] {msg}", file=sys.stderr)


# ---------------------------------------------------------------- primitives

def _rgb(hexstr: str) -> RGBColor:
    return RGBColor.from_string(hexstr.upper().lstrip("#"))


def add_picture(slide, path: str, x: float, y: float, w: float, h: float):
    return slide.shapes.add_picture(str(path), Pt(x), Pt(y), Pt(w), Pt(h))


def add_rect(slide, x, y, w, h, fill=None, line=None, line_w=1.0, rounded=False,
             radius=0.5, dash=None):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    sp = slide.shapes.add_shape(shape_type, Pt(x), Pt(y), Pt(w), Pt(h))
    if rounded:
        try:
            sp.adjustments[0] = radius
        except Exception:
            pass
    sp.shadow.inherit = False
    if fill is None:
        sp.fill.background()
    else:
        sp.fill.solid()
        sp.fill.fore_color.rgb = _rgb(fill)
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = _rgb(line)
        sp.line.width = Pt(line_w)
        if dash:
            ln = sp.line._get_or_add_ln()
            d = ln.makeelement(qn("a:prstDash"), {"val": dash})
            ln.append(d)
    return sp


def _set_fill_alpha(shape, alpha_pct: float):
    """alpha_pct: 0..100 opacity of the solid fill."""
    solid = shape.fill._xPr.find(qn("a:solidFill"))
    clr = solid.find(qn("a:srgbClr"))
    a = clr.makeelement(qn("a:alpha"), {"val": str(int(alpha_pct * 1000))})
    clr.append(a)


def _set_line_alpha(shape, alpha_pct: float):
    ln = shape.line._get_or_add_ln()
    solid = ln.find(qn("a:solidFill"))
    if solid is None:
        return
    clr = solid.find(qn("a:srgbClr"))
    if clr is not None:
        a = clr.makeelement(qn("a:alpha"), {"val": str(int(alpha_pct * 1000))})
        clr.append(a)


def parse_markup(text: str):
    """'**bold**' and '[[color|text]]' -> [(text, bold, color_or_None)]"""
    out, pos = [], 0
    for m in MARKUP_RE.finditer(text):
        if m.start() > pos:
            out.append((text[pos:m.start()], False, None))
        tok = m.group(0)
        if tok.startswith("**"):
            out.append((tok[2:-2], True, None))
        else:
            inner = tok[2:-2]
            name, _, val = inner.partition("|")
            out.append((val, False, NAMED_COLORS.get(name, None)))
        pos = m.end()
    if pos < len(text):
        out.append((text[pos:], False, None))
    return out or [(text, False, None)]


def add_text(slide, x, y, w, h, content, size=10, color=INK, bold=False, italic=False,
             font=F_MAIN, align="left", anchor="top", line_spacing=None,
             space_after=0, wrap=True, shrink=False):
    """content: str (markup allowed) or list[str] paragraphs."""
    tb = slide.shapes.add_textbox(Pt(x), Pt(y), Pt(w), Pt(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {
        "top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE, "bottom": MSO_ANCHOR.BOTTOM,
    }[anchor]
    paras = content if isinstance(content, list) else [content]
    for i, ptext in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {
            "left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER,
            "right": PP_ALIGN.RIGHT, "justify": PP_ALIGN.JUSTIFY,
        }[align]
        if line_spacing:
            p.line_spacing = line_spacing
        if space_after:
            p.space_after = Pt(space_after)
        for txt, b, c in parse_markup(str(ptext)):
            r = p.add_run()
            r.text = txt
            r.font.size = Pt(size)
            r.font.name = font
            r.font.bold = bold or b
            r.font.italic = italic
            r.font.color.rgb = _rgb(c or color)
    return tb


def set_bullet(par, char: str, color=INK, font="Arial", indent_pt=10):
    """Attach a real bullet character to a paragraph."""
    pPr = par._p.get_or_add_pPr()
    pPr.set("marL", str(int(indent_pt * 12700)))
    pPr.set("indent", str(-int(indent_pt * 12700)))
    buClr = pPr.makeelement(qn("a:buClr"), {})
    srgb = buClr.makeelement(qn("a:srgbClr"), {"val": color})
    buClr.append(srgb)
    buFont = pPr.makeelement(qn("a:buFont"), {"typeface": font})
    buChar = pPr.makeelement(qn("a:buChar"), {"char": char})
    for el in (buClr, buFont, buChar):
        pPr.append(el)


def est_lines(text: str, width_pt: float, size: float) -> int:
    """Rough wrapped-line estimate for Calibri-like text."""
    text = re.sub(r"\*\*|\[\[[a-z]+\||\]\]", "", str(text))
    cpl = max(8, width_pt / (size * 0.48))
    total = 0
    for chunk in text.split("\n"):
        total += max(1, math.ceil(len(chunk) / cpl))
    return total


# ---------------------------------------------------------------- chrome

def add_page_number(slide, n: int):
    add_text(slide, SLIDE_W - 34, SLIDE_H - 26, 24, 18, str(n), size=10,
             color=GRAY, align="right")


def content_chrome(slide, title: str, page_no: int | None):
    add_picture(slide, ASSETS / "header_band.jpg", 0, 0, SLIDE_W, BAND_H)
    add_text(slide, 26, 0, 690, BAND_H, title, size=24, color=WHITE, bold=True,
             anchor="middle")
    if page_no is not None:
        add_page_number(slide, page_no)


# ---------------------------------------------------------------- block renderers

def render_heading(slide, x, y, w, h, block):
    add_text(slide, x, y, w, min(h, 26), block.get("text", ""), size=block.get("size", 16),
             color=block.get("color", INK), bold=True, anchor="middle")


def render_bullets(slide, x, y, w, h, block):
    size = block.get("size", 10)
    items = block["items"]
    tb = slide.shapes.add_textbox(Pt(x), Pt(y), Pt(w), Pt(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    first = True
    for it in items:
        if isinstance(it, str):
            it = {"t": it}
        lvl = int(it.get("lvl", 0))
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_after = Pt(it.get("space_after", 4 if lvl == 0 else 2))
        p.line_spacing = 1.0
        char = {0: "\u25aa", 1: "\u25cb", 2: "\u2013"}.get(lvl, "\u25aa")
        set_bullet(p, char, color=INK, indent_pt=10 + 12 * lvl)
        base_bold = bool(it.get("bold", False))
        for txt, b, c in parse_markup(it.get("t", "")):
            r = p.add_run()
            r.text = txt
            r.font.size = Pt(it.get("size", size))
            r.font.name = F_MAIN
            r.font.bold = base_bold or b
            r.font.color.rgb = _rgb(c or it.get("color", INK))


def fit_table(block, col_w: list[float], h_avail: float | None):
    """Pick a font size that (roughly) fits; returns (size, est_height)."""
    header = block.get("header", [])
    rows = block.get("rows", [])
    fracs = block.get("cols") or [1.0 / len(col_w)] * len(col_w)
    tot = sum(fracs)
    cw = [col_w[j] * fracs[j] / tot for j in range(len(col_w))]
    size = block.get("size")
    if size is not None:
        est = 0.0
        if header:
            est += 26
        for r in rows:
            lines = max(est_lines(c, cw[j] - 10, size) for j, c in enumerate(r))
            est += min(200, lines * size * 1.25 + 8)
        return size, est
    for cand in (10, 9, 8):
        est = 26.0 if header else 0.0
        for r in rows:
            lines = max(est_lines(c, cw[j] - 10, cand) for j, c in enumerate(r))
            est += min(200, lines * cand * 1.25 + 8)
        if h_avail is None or est <= h_avail + 0.5:
            return cand, est
    return 8, est


def table_content_height(block, w: float) -> float:
    ncols = len(block.get("header", [])) or (
        len(block["rows"][0]) if block.get("rows") else 0)
    if ncols == 0:
        return 0.0
    fracs = block.get("cols") or [1.0 / ncols] * ncols
    tot = sum(fracs)
    col_w = [w * f / tot for f in fracs]
    _, est = fit_table(block, col_w, None)
    return est


def render_table(slide, x, y, w, h, block):
    header = block.get("header", [])
    rows = block.get("rows", [])
    ncols = len(header) or (len(rows[0]) if rows else 0)
    if ncols == 0:
        return
    nrows = len(rows) + (1 if header else 0)

    fracs = block.get("cols") or [1.0 / ncols] * ncols
    tot = sum(fracs)
    col_w = [w * f / tot for f in fracs]
    aligns = block.get("align") or ["left"] * ncols
    size, _ = fit_table(block, col_w, h)

    gf = slide.shapes.add_table(nrows, ncols, Pt(x), Pt(y), Pt(w), Pt(h))
    tbl = gf.table
    tbl.first_row = False
    tbl.horz_banding = False
    for j, cw in enumerate(col_w):
        tbl.columns[j].width = Pt(cw)

    def fill_cell(cell, text, size, color, bold, align, fill_hex, anchor_top=True):
        cell.fill.solid()
        cell.fill.fore_color.rgb = _rgb(fill_hex)
        cell.margin_left = cell.margin_right = Pt(4)
        cell.margin_top = cell.margin_bottom = Pt(2)
        cell.vertical_anchor = MSO_ANCHOR.TOP if anchor_top else MSO_ANCHOR.MIDDLE
        tf = cell.text_frame
        tf.word_wrap = True
        lines = str(text).split("\n")
        for i, lntext in enumerate(lines):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER,
                           "right": PP_ALIGN.RIGHT}[align]
            p.line_spacing = 1.0
            stripped = lntext.lstrip()
            bullet = None
            if stripped.startswith(("- ", "* ")):
                bullet, stripped = "\u25aa", stripped[2:]
            elif stripped.startswith("o "):
                bullet, stripped = "\u25cb", stripped[2:]
            if bullet:
                set_bullet(p, bullet, color=color, indent_pt=8)
            for txt, b, c in parse_markup(stripped):
                r = p.add_run()
                r.text = txt
                r.font.size = Pt(size)
                r.font.name = F_MAIN
                r.font.bold = bold or b
                r.font.color.rgb = _rgb(c or color)

    ri = 0
    if header:
        tbl.rows[0].height = Pt(24)
        for j, htxt in enumerate(header):
            fill_cell(tbl.cell(0, j), htxt, size, WHITE, True, "left", TEAL)
        ri = 1
    for i, row in enumerate(rows):
        zebra = TINT_L if i % 2 == 0 else TINT_M
        lines = max(est_lines(c, col_w[j] - 10, size) for j, c in enumerate(row))
        tbl.rows[ri + i].height = Pt(min(200, lines * size * 1.25 + 8))
        for j, ctxt in enumerate(row):
            if str(ctxt).strip() == "^":     # spanned cell – keep empty, merged later
                continue
            fill_cell(tbl.cell(ri + i, j), ctxt, size, INK, False,
                      aligns[j] if j < len(aligns) else "left", zebra)

    # vertical merge: '^' merges the cell above with all consecutive '^' cells below
    if any("^" in str(c) for row in rows for c in row):
        for j in range(ncols):
            start = None
            for i in range(len(rows) + 1):
                is_caret = (i < len(rows) and j < len(rows[i])
                            and str(rows[i][j]).strip() == "^")
                if is_caret and start is None:
                    start = i - 1
                elif not is_caret and start is not None:
                    r0 = start + (1 if header else 0)
                    r1 = (i - 1) + (1 if header else 0)
                    if r1 > r0:
                        try:
                            origin = tbl.cell(r0, j)
                            origin.merge(tbl.cell(r1, j))
                            origin.vertical_anchor = MSO_ANCHOR.MIDDLE
                        except Exception:
                            warn(f"merge failed at col {j} rows {r0}-{r1}")
                    start = None


def render_image(slide, x, y, w, h, block):
    path = Path(block["path"])
    if not path.is_absolute():
        path = SPEC_DIR / path
    if not path.is_file():
        warn(f"image not found: {path}")
        return
    with Image.open(path) as im:
        iw, ih = im.size
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    add_picture(slide, str(path), x + (w - dw) / 2, y + (h - dh) / 2, dw, dh)


CODE_TOKEN_RE = re.compile(
    r'"(?:[^"\\]|\\.)*"\s*:|"(?:[^"\\]|\\.)*"|\btrue\b|\bfalse\b|\bnull\b|'
    r"\b\d+(?:\.\d+)?\b|[A-Za-z_][\w.]*|\s+|.")


def _code_line_runs(line: str):
    runs = []
    comment = None
    ci = line.find("//")
    if ci >= 0:
        code_part, comment = line[:ci], line[ci:]
    else:
        code_part = line
    for m in CODE_TOKEN_RE.finditer(code_part):
        tok = m.group(0)
        if tok.startswith('"') and tok.rstrip().endswith(":"):
            runs.append((tok, CODE_KEY))
        elif tok.startswith('"'):
            runs.append((tok, CODE_STR))
        elif tok in ("true", "false", "null") or tok.replace(".", "").isdigit():
            runs.append((tok, CODE_NUM))
        else:
            runs.append((tok, CODE_TEXT))
    if comment:
        runs.append((comment, CODE_COM))
    return runs


def render_code(slide, x, y, w, h, block):
    panels = block.get("panels") or [block]
    n = len(panels)
    gap = 12.0
    pw = (w - gap * (n - 1)) / n
    size = block.get("size", 8)
    for k, panel in enumerate(panels):
        px = x + k * (pw + gap)
        card = add_rect(slide, px, y, pw, h, fill=WHITE, line=CODE_BORDER,
                        line_w=1.2, rounded=True, radius=0.055)
        card.text_frame.text = ""
        ty = y + 6
        if panel.get("title"):
            add_text(slide, px + 10, ty, pw - 20, 14, panel["title"], size=8.5,
                     color=INK, bold=True)
            ty += 16
        body = panel.get("code", "")
        tb = slide.shapes.add_textbox(Pt(px + 10), Pt(ty), Pt(pw - 20), Pt(y + h - ty - 6))
        tf = tb.text_frame
        tf.word_wrap = block.get("wrap", True)
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        lines = body.split("\n")
        line_h = size * 1.32
        needed = len(lines) * line_h
        if needed > y + h - ty - 6:
            warn(f"code panel '{panel.get('title', k)}' overflows: needs {needed:.0f}pt, has {y + h - ty - 6:.0f}pt")
        first = True
        for lntext in lines:
            p = tf.paragraphs[0] if first else tf.add_paragraph()
            first = False
            p.line_spacing = Pt(line_h)
            p.space_after = Pt(0)
            if not lntext:
                r = p.add_run(); r.text = " "; r.font.size = Pt(size); r.font.name = F_CODE
                continue
            for txt, colr in _code_line_runs(lntext):
                r = p.add_run()
                r.text = txt
                r.font.size = Pt(size)
                r.font.name = F_CODE
                r.font.color.rgb = _rgb(colr)


def render_cards(slide, x, y, w, h, block):
    groups = block.get("groups") or []
    legend = block.get("legend")
    n = len(groups)
    if n == 0:
        return
    gap = 10.0
    cw = (w - gap * (n - 1)) / n

    # pre-compute chip layout per group so cards hug their content
    layouts = []
    for g in groups:
        title = g.get("title", "")
        tlines = est_lines(title, cw - 12, 8.5) if title else 0
        cy = 8 + (12 * tlines + 6 if title else 0)
        chips = []
        for chip in g.get("chips", []):
            if isinstance(chip, str):
                chip = {"t": chip}
            lvl = int(chip.get("lvl", 0))
            if chip.get("link"):
                ch = 13
            else:
                ch = max(16, est_lines(chip["t"], cw - 16 - lvl * 10 - 12, 8) * 10.2 + 7)
            chips.append((chip, ch, lvl))
            cy += ch + 5
        layouts.append((g, title, tlines, chips, cy))
    card_h = min(h - (34 if legend else 0), max(cy for *_, cy in layouts))

    for k, (g, title, tlines, chips, content_h) in enumerate(layouts):
        gx = x + k * (cw + gap)
        add_rect(slide, gx, y, cw, card_h, fill=WHITE, line=BORDER,
                 line_w=0.75, rounded=True, radius=0.05)
        cy = y + 8
        if title:
            add_text(slide, gx + 6, cy, cw - 12, 12 * tlines, title, size=8.5,
                     color=INK, bold=True, align="center")
            cy += 12 * tlines + 6
        for chip, ch, lvl in chips:
            ix = gx + 8 + lvl * 10
            iw = cw - 16 - lvl * 10
            if chip.get("link"):
                tb = add_text(slide, ix, cy, iw, ch, chip["t"], size=8,
                              color=LINK, bold=False, font=F_MAIN)
                for r in tb.text_frame.paragraphs[0].runs:
                    r.font.underline = True
            else:
                fill_hex = {"green": CHIP_G, "blue": CHIP_B, "peach": PEACH}.get(
                    chip.get("tone", "green"), CHIP_G)
                add_rect(slide, ix, cy, iw, ch, fill=fill_hex, rounded=True, radius=0.28)
                add_text(slide, ix + 6, cy, iw - 12, ch, chip["t"], size=8,
                         color=INK, anchor="middle")
            cy += ch + 5
        if cy > y + card_h + 1:
            warn(f"card group '{title[:24]}' overflows card by {cy - (y + card_h):.0f}pt")

    if legend:
        ly = y + card_h + 8
        if ly + 26 > y + h:
            ly = y + h - 26
        add_rect(slide, x, ly, w, 26, fill=LEGEND_BG, rounded=True, radius=0.16)
        add_text(slide, x + 10, ly, 120, 26, legend.get("label", "Color key"),
                 size=10, color=INK, bold=True, anchor="middle")
        lx = x + w * 0.32
        for sw in legend.get("swatches", []):
            hexc, label = sw
            add_rect(slide, lx, ly + 7, 42, 12, fill=hexc)
            add_text(slide, lx + 50, ly, 130, 26, label, size=10, color=INK,
                     anchor="middle")
            lx += 195


def render_columns(slide, x, y, w, h, block):
    """Side-by-side child blocks, e.g. table left + diagram right."""
    cols = block.get("cols") or []
    weights = block.get("weights") or [1.0] * len(cols)
    tot = sum(weights)
    gap = block.get("gap", 14.0)
    fracs = [wt / tot for wt in weights]
    cx = x
    for col, fr in zip(cols, fracs):
        cwid = (w - gap * (len(cols) - 1)) * fr
        kind = col.get("type", "bullets")
        fn = BLOCK_RENDERERS.get(kind)
        if fn is None:
            warn(f"unknown column block type '{kind}' skipped")
        else:
            ch = float(col["h"]) if col.get("h") else h
            cy = y
            if not col.get("h"):               # center content-sized blocks in column
                nat = content_height(col, cwid)
                if nat is not None and nat < h:
                    cy = y + (h - nat) / 2
            fn(slide, cx, cy, cwid, ch, col)
        cx += cwid + gap


BLOCK_RENDERERS = {
    "heading": render_heading,
    "bullets": render_bullets,
    "table": render_table,
    "image": render_image,
    "code": render_code,
    "cards": render_cards,
    "columns": render_columns,
}


def bullets_content_height(block, w: float) -> float:
    size = block.get("size", 10)
    total = 0.0
    for it in block.get("items", []):
        if isinstance(it, str):
            it = {"t": it}
        lvl = int(it.get("lvl", 0))
        s = it.get("size", size)
        total += est_lines(it.get("t", ""), w - 24 - 12 * lvl, s) * s * 1.32
        total += it.get("space_after", 4 if lvl == 0 else 2)
    return total


def code_content_height(block, w: float) -> float:
    panels = block.get("panels") or [block]
    size = block.get("size", 8)
    line_h = size * 1.32
    max_lines = max(len(p.get("code", "").split("\n")) for p in panels)
    return 12 + (16 if any(p.get("title") for p in panels) else 0) + max_lines * line_h + 4


def cards_content_height(block, w: float) -> float:
    groups = block.get("groups") or []
    n = max(1, len(groups))
    cw = (w - 10.0 * (n - 1)) / n
    best = 0.0
    for g in groups:
        title = g.get("title", "")
        cy = 8 + (12 * est_lines(title, cw - 12, 8.5) + 6 if title else 0)
        for chip in g.get("chips", []):
            if isinstance(chip, str):
                chip = {"t": chip}
            lvl = int(chip.get("lvl", 0))
            if chip.get("link"):
                ch = 13
            else:
                ch = max(16, est_lines(chip["t"], cw - 16 - lvl * 10 - 12, 8) * 10.2 + 7)
            cy += ch + 5
        best = max(best, cy)
    return best + (34 if block.get("legend") else 0)


def content_height(block, w: float) -> float | None:
    """Natural content height of a block, or None when it should fill the space."""
    t = block.get("type", "bullets")
    if t == "heading":
        return 26.0
    if t == "bullets":
        return bullets_content_height(block, w)
    if t == "table":
        return table_content_height(block, w)
    if t == "code":
        return code_content_height(block, w)
    if t == "cards":
        return cards_content_height(block, w)
    return None  # image / columns / unknown → fill allocated space


def render_body(slide, body, w_body=908.0, x0=26.0):
    blocks = body if isinstance(body, list) else [body]
    blocks = [b for b in blocks if b]
    if not blocks:
        return
    avail = BODY_BOTTOM - BODY_TOP
    gaps = GAP * (len(blocks) - 1)

    heights: list[float | None] = []
    known_total = 0.0
    for b in blocks:
        if b.get("h"):
            hh = float(b["h"])
            heights.append(hh)
            known_total += hh
            continue
        ch = content_height(b, w_body)
        if ch is not None and ch < avail * 0.9:
            heights.append(ch)
            known_total += ch
        else:
            heights.append(None)

    unknown = [i for i, hh in enumerate(heights) if hh is None]
    if unknown:
        share = max(60.0, (avail - gaps - known_total) / len(unknown))
        for i in unknown:
            heights[i] = share
    total = sum(hh for hh in heights) + gaps

    y = BODY_TOP
    if total < avail:                      # center an under-filled stack vertically
        y += (avail - total) / 2
    for b, bh in zip(blocks, heights):
        kind = b.get("type", "bullets")
        fn = BLOCK_RENDERERS.get(kind)
        if fn is None:
            warn(f"unknown block type '{kind}' skipped")
        else:
            fn(slide, x0, y, w_body, bh, b)
        y += bh + GAP


# ---------------------------------------------------------------- slide layouts

def slide_cover(prs, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_picture(slide, ASSETS / "bg_cover.jpg", 0, 0, SLIDE_W, SLIDE_H)
    title = spec.get("title", "Deck title")
    size = spec.get("size", 48)
    add_text(slide, 70, spec.get("title_y", 200), 830, 80, title, size=size,
             color=WHITE, bold=True, anchor="middle")
    sub = spec.get("subtitle")
    if sub:
        add_text(slide, 72, spec.get("title_y", 200) + 62, 700, 24, sub, size=16,
                 color=WHITE)
    date = spec.get("date")
    if date:
        pill = add_rect(slide, 72, 472, 172, 38, fill=WHITE, line=WHITE,
                        line_w=1.0, rounded=True, radius=0.5)
        _set_fill_alpha(pill, 14.5)
        _set_line_alpha(pill, 25.1)
        add_text(slide, 72, 472, 172, 38, date, size=16, color=WHITE,
                 font=F_DATE, align="center", anchor="middle")
    if spec.get("notes"):
        slide.notes_slide.notes_text_frame.text = spec["notes"]
    return slide


def slide_agenda(prs, spec, page_no):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_picture(slide, ASSETS / "bg_agenda.jpg", 0, 0, SLIDE_W, SLIDE_H)
    items = spec["items"]
    n = len(items)
    top = 24.0
    step = min(46.6, (500.0 - top) / max(1, n))
    for i, it in enumerate(items):
        if isinstance(it, dict):
            label, num = it.get("t", ""), it.get("n", i + 1)
        else:
            label, num = str(it), i + 1
        y = top + i * step
        num_txt = f"{int(num):02d}"
        # number + glowing ring
        add_text(slide, 55, y, 46, 30, num_txt, size=14, color=WHITE, bold=True,
                 align="center", anchor="middle")
        ring = slide.shapes.add_shape(MSO_SHAPE.OVAL, Pt(57), Pt(y), Pt(42), Pt(30))
        ring.shadow.inherit = False
        ring.fill.background()
        ring.line.color.rgb = _rgb(NAVY_LINE)
        ring.line.width = Pt(1.0)
        # pill
        add_rect(slide, 98, y, 347, 30, fill=None, line=NAVY_LINE, line_w=1.25,
                 rounded=True, radius=0.5)
        add_text(slide, 114, y, 320, 30, label, size=14, color=WHITE, bold=True,
                 anchor="middle")
    add_page_number(slide, page_no)
    if spec.get("notes"):
        slide.notes_slide.notes_text_frame.text = spec["notes"]
    return slide


def slide_content(prs, spec, page_no):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, fill=WHITE)
    content_chrome(slide, spec.get("title", ""), page_no)
    body = spec.get("body")
    if body:
        render_body(slide, body)
    note = spec.get("note")
    if note:  # small annotation bottom-left (e.g. red remarks)
        add_text(slide, 26, SLIDE_H - 26, 700, 18, note, size=spec.get("note_size", 10),
                 color=spec.get("note_color", RED), bold=spec.get("note_bold", False))
    if spec.get("notes"):
        slide.notes_slide.notes_text_frame.text = spec["notes"]
    return slide


def slide_thanks(prs, spec, page_no):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_picture(slide, ASSETS / "bg_thanks.jpg", 0, 0, SLIDE_W, SLIDE_H)
    add_text(slide, 0, spec.get("title_y", 222), SLIDE_W, 90,
             spec.get("title", "THANK YOU"), size=spec.get("size", 54), color=WHITE,
             bold=True, align="center", anchor="middle")
    sub = spec.get("subtitle")
    if sub:
        add_text(slide, 0, spec.get("title_y", 222) + 78, SLIDE_W, 26, sub, size=16,
                 color="D6E4F5", align="center")
    add_page_number(slide, page_no)
    if spec.get("notes"):
        slide.notes_slide.notes_text_frame.text = spec["notes"]
    return slide


# ---------------------------------------------------------------- main

def build(spec: dict, out_path: Path):
    prs = Presentation()
    prs.slide_width = Pt(SLIDE_W)
    prs.slide_height = Pt(SLIDE_H)

    page_no = 0
    for i, s in enumerate(spec.get("slides", [])):
        layout = s.get("layout", "content")
        if layout == "cover":
            slide_cover(prs, s)
        elif layout == "agenda":
            page_no += 1
            slide_agenda(prs, s, page_no)
        elif layout == "content":
            page_no += 1
            slide_content(prs, s, page_no)
        elif layout == "thanks":
            page_no += 1
            slide_thanks(prs, s, page_no)
        else:
            warn(f"slide {i + 1}: unknown layout '{layout}' skipped")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(out_path))
    print(f"saved {out_path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("spec", type=Path, help="deck spec JSON")
    ap.add_argument("-o", "--output", type=Path, help="output .pptx path")
    args = ap.parse_args()

    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    global SPEC_DIR
    SPEC_DIR = args.spec.resolve().parent
    out = args.output or Path(spec.get("output") or args.spec.with_suffix(".pptx").name)
    build(spec, out)
    if warnings:
        print(f"completed with {len(warnings)} warning(s)", file=sys.stderr)


if __name__ == "__main__":
    main()
