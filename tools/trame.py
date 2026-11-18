#!/usr/bin/env python3
"""Print the 16 dither masks used by the "trame" animation in style.css, as data URIs.

    python3 tools/trame.py

Each mask is an 8×8 PNG: a 4×4 Bayer matrix shown at 2×. Frame k lets through
the cells whose threshold is below k, so the element fills in dot by dot.
"""
import base64
import io

from PIL import Image

BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]

for k in range(16):
    im = Image.new("LA", (8, 8), (0, 0))
    for y in range(8):
        for x in range(8):
            if BAYER[y // 2][x // 2] < k:
                im.putpixel((x, y), (0, 255))
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    uri = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    pct = round(k / 16 * 100, 2)
    print(f"  {pct}% {{ -webkit-mask-image: url({uri}); mask-image: url({uri}); }}")
print("  100% { -webkit-mask-image: none; mask-image: none; }")
