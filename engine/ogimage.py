#!/usr/bin/env python3
"""Generate branded 1200x630 og:image PNGs for every page at build time."""
import textwrap
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    Image = None

ROOT = Path(__file__).parent.parent
OUT = ROOT / "docs" / "og"

BG = "#1c1917"
ACCENT = "#0e7490"
FG = "#fafaf9"
MUTED = "#a8a29e"

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",   # CI (ubuntu)
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/System/Library/Fonts/Helvetica.ttc",                    # macOS local
    "/System/Library/Fonts/SFNSText.ttf",
]


def load_font(size):
    for p in FONT_CANDIDATES:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def render(title: str, name: str):
    if Image is None:
        return None
    img = Image.new("RGB", (1200, 630), BG)
    d = ImageDraw.Draw(img)

    # accent bar
    d.rectangle([0, 0, 1200, 12], fill=ACCENT)

    # site name
    f_small = load_font(30)
    d.text((70, 70), "AI VISIBILITY INDEX", font=f_small, fill=ACCENT)

    # title (wrapped, auto-shrinking)
    size = 76 if len(title) <= 45 else 60 if len(title) <= 70 else 48
    f_title = load_font(size)
    wrapped = textwrap.fill(title, width=max(18, int(1050 / (size * 0.52))))
    lines = wrapped.split("\n")[:4]
    y = 170
    for line in lines:
        d.text((70, y), line, font=f_title, fill=FG)
        y += int(size * 1.25)

    # footer
    f_foot = load_font(28)
    d.text((70, 540), "Free data on who AI search recommends", font=f_foot, fill=MUTED)
    d.text((1200 - 70 - d.textlength("aicantfindme.com", font=f_foot), 540),
           "aicantfindme.com", font=f_foot, fill=ACCENT)

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{name}.png"
    img.save(path, "PNG")
    return path
