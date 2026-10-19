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

# Brand palette
GREEN_DEEP = (0x0B, 0x3D, 0x2E)
TEAL_DEEP  = (0x0A, 0x6B, 0x66)
GREEN_BRIGHT = (0x22, 0xC5, 0x5E)
LEAF_LIGHT = (0x9B, 0xE7, 0xC9)
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

def draw_leaf(size, fill, vein=WHITE):
    """Single leaf (ellipse + vein) on transparent RGBA."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    leaf = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ld = ImageDraw.Draw(leaf)
    lw, lh = int(size * 0.78), int(size * 0.46)
    lx, ly = (size - lw) // 2, (size - lh) // 2
    ld.ellipse([lx, ly, lx + lw, ly + lh], fill=(*fill, 255))
    leaf = leaf.rotate(-35, resample=Image.BICUBIC, expand=False)
    img.paste(leaf, (0, 0), leaf)
    v = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    vd = ImageDraw.Draw(v)
    vw = max(2, int(size * 0.03))
    vd.line([(size * 0.28, size * 0.72), (size * 0.72, size * 0.28)], fill=(*vein, 230), width=vw)
    v = v.rotate(-35, resample=Image.BICUBIC, expand=False)
    img.paste(v, (0, 0), v)
    return img

def make_logo(size, out_path):
    radius = int(size * 0.22)
    tile = rounded_gradient(size, radius, GREEN_DEEP, TEAL_DEEP)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.paste(tile, (0, 0), tile)
    ls = int(size * 0.62)
    l1 = draw_leaf(ls, GREEN_BRIGHT, vein=WHITE)
    l2 = draw_leaf(int(ls * 0.8), LEAF_LIGHT, vein=WHITE)
    canvas.paste(l1, (int(size * 0.18), int(size * 0.16)), l1)
    canvas.paste(l2, (int(size * 0.34), int(size * 0.40)), l2)
    canvas.save(out_path, "PNG")
    print(f"saved {out_path} ({size}x{size})")

def make_cover(w, h, out_path, logo_size=None):
    bg = dgradient(w, h, GREEN_DEEP, TEAL_DEEP).convert("RGBA")
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
    lm = rounded_gradient(logo_size, int(logo_size * 0.22), GREEN_DEEP, TEAL_DEEP)
    ls = int(logo_size * 0.62)
    l1 = draw_leaf(ls, GREEN_BRIGHT, vein=WHITE)
    l2 = draw_leaf(int(ls * 0.8), LEAF_LIGHT, vein=WHITE)
    lm.paste(l1, (int(logo_size * 0.18), int(logo_size * 0.16)), l1)
    lm.paste(l2, (int(logo_size * 0.34), int(logo_size * 0.40)), l2)
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