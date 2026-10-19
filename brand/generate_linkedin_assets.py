#!/usr/bin/env python3
"""
Generate LinkedIn-ready brand assets for Fluxoniks:
  - linkedin-logo.png    (square, 400x400 — LinkedIn company logo)
  - linkedin-logo@2x.png (square, 800x800 — retina)
  - linkedin-cover.png   (1128x376 — LinkedIn company page cover)
  - linkedin-cover@2x.png (2256x752 — retina)

Uses the same brand palette as the website. Only needs Pillow.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

OUT = os.path.dirname(os.path.abspath(__file__))

# Brand palette (must match favicon.svg exactly)
GREEN_DEEP = (0x0B, 0x3D, 0x2E)   # #0B3D2E — gradient start
TEAL        = (0x0D, 0x94, 0x88)  # #0D9488 — gradient end (favicon)
TEAL_DEEP   = (0x0A, 0x6B, 0x66)  # #0A6B66 — darker accent (kept for reference)
GREEN_BRIGHT = (0x22, 0xC5, 0x5E) # #22C55E — right leaf (95% opacity)
LEAF_LIGHT = (0x9B, 0xE7, 0xC9)   # #9BE7C9 — left leaf
WHITE = (255, 255, 255)

def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))

def dgradient(w, h, c1, c2):
    """Diagonal gradient (top-left c1 -> bottom-right c2)."""
    img = Image.new("RGB", (w, h), c1)
    px = img.load()
    diag = w + h
    for y in range(h):
        for x in range(w):
            t = (x + y) / diag
            px[x, y] = lerp(c1, c2, t)
    return img

def rounded_gradient(size, radius, c1, c2):
    grad = dgradient(size, size, c1, c2).convert("RGBA")
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(grad, (0, 0), mask)
    return out

def load_font(size, bold=True):
    paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNSDisplay.ttf",
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()

# ── Bezier helpers (replicate the exact favicon.svg paths) ─────────────────
# favicon paths (viewBox 64x64):
#   right leaf: M32 50 c0-12 7-20 22-22 -2 14 -8 22 -22 22 Z
#   left  leaf: M32 50 c0-12-7-20-22-22  2 14  8 22  22 22 Z
#   stem      : M32 50 V26  (white, stroke-width 2.4)

def _cubic(p0, p1, p2, p3, t):
    u = 1 - t
    return (
        u*u*u*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t*t*t*p3[0],
        u*u*u*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t*t*t*p3[1],
    )

def _leaf_points(scale, right=True):
    """Sample the two cubic segments of one leaf (in 64-space), scaled to `scale`."""
    if right:
        a0, a1, a2, a3 = (32, 50), (32, 38), (39, 30), (54, 28)
        b0, b1, b2, b3 = (54, 28), (52, 42), (46, 50), (32, 50)
    else:
        a0, a1, a2, a3 = (32, 50), (32, 38), (25, 30), (10, 28)
        b0, b1, b2, b3 = (10, 28), (12, 42), (18, 50), (32, 50)
    pts = []
    n = 48
    for i in range(n + 1):
        t = i / n
        pts.append(_cubic(a0, a1, a2, a3, t))
    for i in range(1, n + 1):
        t = i / n
        pts.append(_cubic(b0, b1, b2, b3, t))
    return [(x * scale, y * scale) for (x, y) in pts]

def draw_sprout(size, with_bg=True):
    """Render the Fluxoniks sprout mark at `size`, matching favicon.svg exactly.
    If with_bg, paint the rounded gradient square first (as in the favicon)."""
    s = size / 64.0  # scale from 64-space
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if with_bg:
        radius = int(15 * s)
        tile = rounded_gradient(size, radius, GREEN_DEEP, TEAL)
        img.paste(tile, (0, 0), tile)
        d = ImageDraw.Draw(img)
    # left leaf (lighter) then right leaf (brighter) on top, matching favicon layer order
    left_fill = (*LEAF_LIGHT, 255)
    right_fill = (*GREEN_BRIGHT, int(255 * 0.95))
    d.polygon(_leaf_points(s, right=False), fill=left_fill)
    d.polygon(_leaf_points(s, right=True), fill=right_fill)
    # stem — white vertical line from (32,50) to (32,26), width 2.4 (85% opacity)
    stem_w = max(2, int(round(2.4 * s)))
    d.line(
        [(32 * s, 50 * s), (32 * s, 26 * s)],
        fill=(*WHITE, int(255 * 0.85)),
        width=stem_w,
    )
    return img

def draw_leaf(size, fill, vein=WHITE):
    """Deprecated single-leaf — kept for compatibility. Not used in new logo."""
    return Image.new("RGBA", (size, size), (0, 0, 0, 0))

def make_logo(size, out_path):
    """Logo = the exact favicon sprout (gradient square + two leaves + stem)."""
    img = draw_sprout(size, with_bg=True)
    img.save(out_path, "PNG")
    print(f"saved {out_path} ({size}x{size})")

def make_cover(w, h, out_path, logo_size=None):
    bg = dgradient(w, h, GREEN_DEEP, TEAL).convert("RGBA")
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    r = int(h * 1.1)
    for i in range(12):
        rr = int(r * (1 - i / 14))
        a = int(18 * (i / 12))
        gd.ellipse([w - rr - 60, -rr // 2, w + rr, rr], fill=(0x22, 0xC5, 0x5E, a))
    glow = glow.filter(ImageFilter.GaussianBlur(40))
    bg.paste(glow, (0, 0), glow)
    if logo_size is None:
        logo_size = int(h * 0.62)
    lm = draw_sprout(logo_size, with_bg=True)
    pad = int(h * 0.18)
    bg.paste(lm, (pad, (h - logo_size) // 2), lm)
    d = ImageDraw.Draw(bg)
    tx = pad + logo_size + int(h * 0.12)
    name_font = load_font(int(h * 0.26), bold=True)
    tag_font = load_font(int(h * 0.085), bold=False)
    d.text((tx, int(h * 0.30)), "Fluxoniks", font=name_font, fill=WHITE)
    d.text((tx, int(h * 0.62)), "GHG & Sustainability Consulting", font=tag_font, fill=LEAF_LIGHT)
    d.text((tx, int(h * 0.74)), "Methodology + Standard + Deliverable", font=tag_font, fill=(0xC7, 0xE6, 0xDC))
    bg.convert("RGB").save(out_path, "PNG")
    print(f"saved {out_path} ({w}x{h})")

if __name__ == "__main__":
    make_logo(400, os.path.join(OUT, "linkedin-logo.png"))
    make_logo(800, os.path.join(OUT, "linkedin-logo@2x.png"))
    make_cover(1128, 376, os.path.join(OUT, "linkedin-cover.png"))
    make_cover(2256, 752, os.path.join(OUT, "linkedin-cover@2x.png"))
    print("\nLinkedIn assets generated.")