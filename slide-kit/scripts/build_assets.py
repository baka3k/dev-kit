#!/usr/bin/env python3
"""Rebuild brand-neutral navy backgrounds (cover + agenda) for the skill.

Generates the glowing node-constellation + arc rings artwork from scratch
(no extracted brand shapes) and composes it over the navy gradient.

Usage:  python3 build_assets.py            # writes assets/bg_cover.jpg, assets/bg_agenda.jpg
"""

from __future__ import annotations

import math
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ASSETS = Path(__file__).resolve().parent.parent / "assets"
W, H = 1920, 1080
C1, C2 = (0, 56, 119), (2, 39, 96)   # navy gradient endpoints
STOP = 0.42


def gradient() -> np.ndarray:
    xs = np.linspace(0, 1, W)
    t = np.clip(xs / STOP, 0, 1)[None, :, None]
    a = np.array(C1, dtype=float)[None, None, :]
    b = np.array(C2, dtype=float)[None, None, :]
    row = np.clip(a * (1 - t) + b * t, 0, 255).astype(np.uint8)
    return np.repeat(row, H, axis=0)


def glow_compose(base: np.ndarray, light: Image.Image, k_direct=0.9, k_soft=0.35, k_wide=0.28):
    light_a = np.array(light, dtype=float)
    soft = np.array(light.filter(ImageFilter.GaussianBlur(4)), dtype=float)
    wide = np.array(light.filter(ImageFilter.GaussianBlur(16)), dtype=float)
    out = base.astype(float) + light_a * k_direct + soft * k_soft + wide * k_wide
    return np.clip(out, 0, 255).astype(np.uint8)


def draw_rings(d: ImageDraw.ImageDraw, cx, cy, radii, color, width=3, partial=0.35, rot=0.0):
    for i, r in enumerate(radii):
        bbox = (cx - r, cy - r * 0.92, cx + r, cy + r * 0.92)
        if partial and i % 2 == 1:
            start = rot * 360 + i * 47
            d.arc(bbox, start, start + 360 * (1 - partial), fill=color, width=width)
        else:
            d.ellipse(bbox, outline=color, width=width)


def constellation(rng: random.Random, box, n_nodes, link_dist, seed_color=(90, 165, 255)):
    """Returns (light_image) with glowing node-link mesh inside box=(x0,y0,x1,y1)."""
    light = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(light)
    x0, y0, x1, y1 = box
    pts = [(rng.uniform(x0, x1), rng.uniform(y0, y1)) for _ in range(n_nodes)]
    for i, p in enumerate(pts):
        for q in pts[i + 1:]:
            dist = math.hypot(p[0] - q[0], p[1] - q[1])
            if dist < link_dist:
                fade = 1.0 - dist / link_dist
                col = tuple(int(c * (0.35 + 0.45 * fade)) for c in seed_color)
                d.line([p, q], fill=col, width=2)
    for p in pts:
        r = rng.uniform(2.5, 6.0)
        col = tuple(int(c * rng.uniform(0.75, 1.0)) for c in seed_color)
        x, y = p
        d.ellipse((x - r, y - r, x + r, y + r), fill=col)
    return light


def scatter_dots(rng: random.Random, n, region, color=(80, 150, 240)):
    light = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(light)
    x0, y0, x1, y1 = region
    for _ in range(n):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        r = rng.uniform(1.0, 3.0)
        col = tuple(int(c * rng.uniform(0.4, 1.0)) for c in color)
        d.ellipse((x - r, y - r, x + r, y + r), fill=col)
    return light


def add(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.clip(a.astype(float) + b.astype(float), 0, 255).astype(np.uint8)


def build_cover():
    rng = random.Random(42)
    base = gradient()
    light = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(light)
    # circuit rings anchored bottom-right, partially off-canvas like the reference
    draw_rings(d, 1620, 1010, [150, 235, 330, 430, 540], (52, 130, 235), width=3,
               partial=0.3, rot=0.13)
    base = add(base, np.array(light, dtype=float) * 0.55)
    base = add(base, np.array(light.filter(ImageFilter.GaussianBlur(10)), dtype=float) * 0.5)

    mesh = constellation(rng, (1150, 90, 1840, 780), n_nodes=16, link_dist=270)
    base = glow_compose(base, mesh, k_direct=0.75, k_soft=0.3, k_wide=0.22)

    dots = scatter_dots(rng, 70, (1000, 60, 1900, 1000))
    base = glow_compose(base, dots, k_direct=0.8, k_soft=0.5, k_wide=0.3)

    Image.fromarray(base).save(ASSETS / "bg_cover.jpg", quality=88, optimize=True)
    print("bg_cover.jpg rebuilt")


def build_agenda():
    rng = random.Random(7)
    base = gradient()
    mesh = constellation(rng, (1180, 90, 1850, 980), n_nodes=15, link_dist=280)
    base = glow_compose(base, mesh, k_direct=0.85, k_soft=0.35, k_wide=0.25)

    rings = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(rings)
    draw_rings(d, 1810, 1080, [120, 200, 290, 390], (46, 118, 225), width=3,
               partial=0.25, rot=0.2)
    base = add(base, np.array(rings, dtype=float) * 0.5)
    base = add(base, np.array(rings.filter(ImageFilter.GaussianBlur(8)), dtype=float) * 0.45)

    dots = scatter_dots(rng, 55, (1100, 60, 1900, 1020))
    base = glow_compose(base, dots, k_direct=0.75, k_soft=0.45, k_wide=0.3)

    Image.fromarray(base).save(ASSETS / "bg_agenda.jpg", quality=88, optimize=True)
    print("bg_agenda.jpg rebuilt")


def build_example_diagram():
    """Draw a brand-neutral sample architecture diagram (examples/example_diagram.png)."""
    out = ASSETS.parent / "examples" / "example_diagram.png"
    font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
    try:
        from PIL import ImageFont
        f_box = ImageFont.truetype(font_path, 30)
        f_small = ImageFont.truetype(font_path, 22)
    except Exception:
        f_box = f_small = ImageFont.load_default()

    CW, CH = 1300, 1060
    img = Image.new("RGB", (CW, CH), (255, 255, 255))
    d = ImageDraw.Draw(img)

    INK = (41, 51, 58)
    TEAL = (50, 178, 193)
    TINT_L = (232, 242, 244)
    TINT_M = (205, 228, 233)
    MINT = (167, 255, 207)
    GRAY = (127, 132, 142)
    BORDER = (191, 191, 191)

    def center_text(cx, cy, text, font, fill):
        bb = d.textbbox((0, 0), text, font=font)
        d.text((cx - (bb[2] - bb[0]) / 2, cy - (bb[3] - bb[1]) / 2 - bb[1]), text,
               font=font, fill=fill)

    def rbox(x, y, w, h, fill, outline, label, tcolor=INK, radius=14, width=2):
        d.rounded_rectangle((x, y, x + w, y + h), radius=radius, fill=fill,
                            outline=outline, width=width)
        center_text(x + w / 2, y + h / 2, label, f_box, tcolor)

    def arrow(x0, y0, x1, y1, color=GRAY, width=3):
        d.line((x0, y0, x1, y1), fill=color, width=width)
        ang = math.atan2(y1 - y0, x1 - x0)
        for s in (-1, 1):
            wx = x1 - 14 * math.cos(ang) + 7 * s * math.sin(ang)
            wy = y1 - 14 * math.sin(ang) - 7 * s * math.cos(ang)
            d.polygon([(x1, y1), (wx, wy)], fill=color)

    def row_label(x, y, text):
        d.text((x, y), text, font=f_small, fill=GRAY)

    # layer labels
    row_label(36, 40, "Channels")
    row_label(36, 212, "Ingress")
    row_label(36, 402, "Services")
    row_label(36, 622, "Platform")
    row_label(36, 812, "Data")

    # channels
    rbox(300, 62, 260, 78, TINT_L, BORDER, "Web App")
    rbox(740, 62, 260, 78, TINT_L, BORDER, "Mobile App")
    arrow(430, 140, 590, 236)
    arrow(870, 140, 710, 236)

    # ingress
    rbox(460, 236, 380, 78, TEAL, TEAL, "API Gateway", tcolor=(255, 255, 255))
    arrow(650, 314, 650, 416)
    arrow(430, 275, 300, 275, color=(210, 210, 210), width=2)
    arrow(870, 275, 1000, 275, color=(210, 210, 210), width=2)
    d.text((238, 262), "...", font=f_box, fill=GRAY)
    d.text((1006, 262), "...", font=f_box, fill=GRAY)

    # services
    rbox(160, 416, 280, 88, MINT, MINT, "Content API")
    rbox(510, 416, 280, 88, MINT, MINT, "Search API")
    rbox(860, 416, 280, 88, MINT, MINT, "Media API")
    arrow(300, 504, 430, 646)
    arrow(700, 504, 830, 646)
    arrow(1000, 504, 870, 646)

    # platform
    rbox(300, 646, 260, 78, TINT_M, BORDER, "Cache")
    rbox(740, 646, 260, 78, TINT_M, BORDER, "Queue")
    arrow(430, 724, 560, 838)
    arrow(870, 724, 740, 838)

    # data
    rbox(430, 838, 200, 84, (255, 255, 255), INK, "Primary DB")
    rbox(690, 838, 200, 84, (255, 255, 255), INK, "Index Store")

    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, optimize=True)
    print(f"example_diagram.png rebuilt ({CW}x{CH})")


if __name__ == "__main__":
    build_cover()
    build_agenda()
    build_example_diagram()