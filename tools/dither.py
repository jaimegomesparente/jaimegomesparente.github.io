#!/usr/bin/env python3
"""Turn images into two-colour dithered PNGs for the site.

    python3 tools/dither.py                      # every image in tools/raw/ -> img/
    python3 tools/dither.py tools/raw/claylings.png --method atkinson --gamma 0.8

Images are cropped to 16:10, resized to --width (288 by default) and dithered to
the two site colours. The page shows them at exactly 2x with
`image-rendering: pixelated`, so keep the width at 288 unless you change the CSS too.

Requires Pillow and NumPy: pip install pillow numpy
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "tools" / "raw"
OUT = ROOT / "img"

PAPER = (236, 232, 220)  # --paper in style.css
INK = (20, 20, 20)       # --ink in style.css
EXTS = {".png", ".jpg", ".jpeg", ".webp"}

# Settings per image, used when the script runs on the whole of tools/raw/.
# An image named on the command line uses the command-line options instead.
PRESETS = {}


def bayer(n=8):
    m = np.array([[0]])
    while m.shape[0] < n:
        m = np.block([[4 * m, 4 * m + 2], [4 * m + 3, 4 * m + 1]])
    return (m + 0.5) / (n * n)


def ordered(g):
    h, w = g.shape
    b = bayer(8)
    t = np.tile(b, (h // 8 + 1, w // 8 + 1))[:h, :w]
    return g > t


def diffusion(g, kernel):
    g = g.copy()
    h, w = g.shape
    out = np.zeros_like(g, dtype=bool)
    for y in range(h):
        for x in range(w):
            old = g[y, x]
            new = 1.0 if old >= 0.5 else 0.0
            out[y, x] = new == 1.0
            err = old - new
            for dx, dy, k in kernel:
                xx, yy = x + dx, y + dy
                if 0 <= xx < w and 0 <= yy < h:
                    g[yy, xx] += err * k
    return out


ATKINSON = [(1, 0, 1 / 8), (2, 0, 1 / 8), (-1, 1, 1 / 8), (0, 1, 1 / 8), (1, 1, 1 / 8), (0, 2, 1 / 8)]
FLOYD = [(1, 0, 7 / 16), (-1, 1, 3 / 16), (0, 1, 5 / 16), (1, 1, 1 / 16)]


def process(src, dst, width, method, gamma, contrast, invert):
    img = Image.open(src).convert("L")
    height = round(width * 10 / 16)
    img = ImageOps.fit(img, (width, height), Image.LANCZOS)
    if contrast:
        img = ImageOps.autocontrast(img, cutoff=contrast)
    g = np.asarray(img, dtype=np.float32) / 255.0
    g = g ** gamma
    if invert:
        g = 1.0 - g
    if method == "bayer":
        light = ordered(g)
    else:
        light = diffusion(g, ATKINSON if method == "atkinson" else FLOYD)
    out = Image.new("P", (width, height))
    out.putpalette([*INK, *PAPER])
    out.putdata(light.astype(np.uint8).ravel().tolist())
    out.save(dst, optimize=True)
    print(f"{src.name} -> {dst.relative_to(ROOT)} ({dst.stat().st_size // 1024} KB)")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("files", nargs="*", type=Path, help="images to convert (default: all of tools/raw/)")
    p.add_argument("--width", type=int, default=288)
    p.add_argument("--method", choices=["bayer", "atkinson", "floyd"], default="bayer")
    p.add_argument("--gamma", type=float, default=1.0, help="< 1 lightens, > 1 darkens")
    p.add_argument("--contrast", type=float, default=1.0, help="percent clipped at each end (0 = off)")
    p.add_argument("--invert", action="store_true", help="swap ink and paper")
    a = p.parse_args()
    OUT.mkdir(exist_ok=True)
    if a.files:
        for f in a.files:
            process(f, OUT / (f.stem + ".png"), a.width, a.method, a.gamma, a.contrast, a.invert)
        return
    for f in sorted(f for f in RAW.iterdir() if f.suffix.lower() in EXTS):
        o = {"method": a.method, "gamma": a.gamma, "contrast": a.contrast, "invert": a.invert}
        o.update(PRESETS.get(f.stem, {}))
        process(f, OUT / (f.stem + ".png"), a.width, o["method"], o["gamma"], o["contrast"], o["invert"])


if __name__ == "__main__":
    main()
