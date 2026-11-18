#!/usr/bin/env python3
"""Illustration for The Claylings: the night watch, seen from behind.

    python3 tools/claylings.py && python3 tools/dither.py

Spearmen on the palisade look out at the dark forest, where spiders' eyes shine.
Drawn in code (no game sprites). Writes tools/raw/claylings.png.
"""
import math, random
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUT = Path(__file__).resolve().parent / "raw"
OUT.mkdir(exist_ok=True)
W, H = 320, 200
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)


def radial(cx, cy, r, p=1.6, sy=1.0):
    return np.clip(1 - np.hypot(XX - cx, (YY - cy) * sy) / r, 0, 1) ** p


def img_of(a):
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def add(img, a):
    return img_of(np.asarray(img, np.float32) + a)


def ridge(d, y0, amp, seed, v, freq=0.03):
    r = np.random.default_rng(seed); ph = r.random(3) * 10
    pts = [(x, y0 + amp * (math.sin(x * freq + ph[0]) * 0.6 + math.sin(x * freq * 2.3 + ph[1]) * 0.3 + math.sin(x * freq * 5.1 + ph[2]) * 0.1)) for x in range(0, W + 4, 4)]
    d.polygon(pts + [(W, H), (0, H)], fill=v)


def tree(d, x, y, s, v):
    d.rectangle((x - s * 0.7, y - s * 3, x + s * 0.7, y), fill=int(v * 0.8))
    d.ellipse((x - 3.4 * s, y - 11 * s, x + 3.4 * s, y - 2.5 * s), fill=v)


def pine(d, x, y, s, v):
    d.polygon([(x, y - 12 * s), (x + 4 * s, y), (x - 4 * s, y)], fill=v)


def clay(d, x, y, s=1.0, v=255, f=1, view="side", step=0.0, carry=None, tool=None, bend=0.0):
    """A clayling, feet at (x, y). f = 1 faces right, -1 left. view: side or back."""
    E = lambda cx, cy, rx, ry, fill: d.ellipse((x + cx * s - rx * s, y + cy * s - ry * s, x + cx * s + rx * s, y + cy * s + ry * s), fill=fill)
    sw = math.sin(step) * 2.2
    E(f * sw, -1.2, 2.2, 1.4, v)                       # legs, mid-stride
    E(-f * sw, -1.2, 2.2, 1.4, int(v * 0.85))
    E(f * bend, -6, 4.2, 5.2, v)                       # body
    hx, hy = f * (1.4 + bend * 1.6), -13 + bend * 0.8
    E(hx, hy, 4.3, 3.9, v)                             # head
    if view == "side":
        E(hx + f * 2.2, hy - 0.3, 0.75, 1.1, 0)         # one eye, on the side
    if carry == "log":
        d.rounded_rectangle((x - 9 * s + f * 2 * s, y - 20 * s, x + 9 * s + f * 2 * s, y - 16.5 * s), radius=1.5 * s, fill=int(v * 0.8))
        d.ellipse((x + 7.5 * s + f * 2 * s, y - 20 * s, x + 10.5 * s + f * 2 * s, y - 16.5 * s), fill=v)
    if carry == "sack":
        E(-f * 4.5, -9, 3.6, 4.2, int(v * 0.8))
    if tool == "spear":
        d.line([(x + 3 * s, y - 2 * s), (x + 3 * s, y - 30 * s)], fill=int(v * 0.8), width=max(1, round(s)))
        d.polygon([(x + 1.6 * s, y - 30 * s), (x + 4.4 * s, y - 30 * s), (x + 3 * s, y - 35 * s)], fill=v)
    if tool == "axe_up":                               # axe raised behind the head, mid-swing
        d.line([(x + f * 2 * s, y - 8 * s), (x - f * 6 * s, y - 22 * s)], fill=int(v * 0.8), width=max(1, round(s)))
        d.polygon([(x - f * 4 * s, y - 25 * s), (x - f * 10 * s, y - 24 * s), (x - f * 7 * s, y - 19 * s)], fill=v)
    if tool == "hammer":
        d.line([(x + f * 3 * s, y - 8 * s), (x + f * 8 * s, y - 17 * s)], fill=int(v * 0.8), width=max(1, round(s)))
        d.rectangle((x + f * 6 * s - 2 * s, y - 20 * s, x + f * 6 * s + 3 * s, y - 16 * s), fill=v)


def crystal(d, cx, cy, h, v=255):
    w = h * 0.36
    d.polygon([(cx, cy - h / 2), (cx + w, cy - h * 0.1), (cx, cy + h / 2), (cx - w, cy - h * 0.1)], fill=v)
    d.polygon([(cx, cy - h / 2), (cx + w, cy - h * 0.1), (cx, cy + h / 2)], fill=int(v * 0.75))


def stars(d, n, ymax, seed):
    r = random.Random(seed)
    for _ in range(n):
        d.point((r.randrange(W), r.randrange(ymax)), fill=r.choice([140, 200, 255]))


# C. The night watch, from behind: spearmen on the wall, the dark forest, eyes in it
def watch():
    base = 12 + (1 - YY / H) * 14
    im = img_of(base); d = ImageDraw.Draw(im)
    stars(d, 110, 90, 7)
    d.ellipse((246, 22, 266, 42), fill=220); d.ellipse((252, 18, 272, 38), fill=14)
    r = random.Random(2)
    for i in range(46):
        pine(d, i * 7 + r.uniform(-2, 2), 112 + r.uniform(-4, 6), r.uniform(2.6, 4.2), 40)
    d.rectangle((0, 112, W, 140), fill=26)
    for x, y in [(40, 108), (96, 116), (150, 104), (214, 112), (282, 106), (120, 124)]:
        d.point([(x, y), (x + 3, y)], fill=255)
    im = add(im, radial(160, 220, 190, 1.4, 1.2) * 120); d = ImageDraw.Draw(im)   # Crystal light from behind us
    for i in range(41):                                               # the wall, in front of us
        x = i * 8
        d.polygon([(x, 200), (x + 7, 200), (x + 7, 160), (x + 3.5, 155), (x, 160)], fill=150 + (i % 2) * 20)
    d.rectangle((0, 168, W, 172), fill=110)
    for x, s in [(82, 2.2), (166, 2.4), (246, 2.1)]:
        clay(d, x, 162, s, 255, 1, view="back", tool="spear")
    # inverted (light comes out in ink) with the midtones lifted a little
    a = (np.asarray(im, np.float32) / 255) ** 0.85
    Image.fromarray((255 - a * 255).astype(np.uint8)).save(OUT / "claylings.png")
    print("tools/raw/claylings.png")



watch()
