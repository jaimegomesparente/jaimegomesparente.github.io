#!/usr/bin/env python3
"""Placeholder illustrations for the projects, drawn in code.

    python3 tools/illustrations.py && python3 tools/dither.py

Writes greyscale images to tools/raw/. Replace any of them with a real screenshot
under the same name, then run dither.py again.
"""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from pathlib import Path
OUT = Path(__file__).resolve().parent / "raw"
OUT.mkdir(exist_ok=True)
W, H = 320, 200  # drawing resolution

def save(name, gray):
    # inverted so that the bright parts of the drawing come out in ink
    img = Image.fromarray(255 - np.asarray(gray, dtype=np.uint8))
    img.resize((W * 2, H * 2), Image.LANCZOS).save(OUT / f"{name}.png")
    print(f"tools/raw/{name}.png")


def canvas():
    return Image.new("L", (W, H), 0)

def glow(img, r, k=1.0):
    g = img.filter(ImageFilter.GaussianBlur(r))
    return Image.fromarray(np.clip(np.asarray(img, np.float32) + k * np.asarray(g, np.float32), 0, 255).astype(np.uint8))

def radial(cx, cy, r, inner=255):
    y, x = np.mgrid[0:H, 0:W]
    d = np.sqrt((x - cx) ** 2 + (y - cy) ** 2) / r
    return np.clip(1 - d, 0, 1) ** 1.6 * inner

random.seed(4)

# 1. Gravitational simulation: star, orbits, planets with shaded spheres
def gravity():
    a = radial(120, 100, 150, 120)
    img = Image.fromarray(a.astype(np.uint8))
    d = ImageDraw.Draw(img)
    for _ in range(140):
        x, y = random.randrange(W), random.randrange(H)
        d.point((x, y), fill=random.choice([90, 160, 255]))
    for rx, ry in [(60, 40), (105, 70), (150, 98), (200, 128)]:
        d.ellipse((120 - rx, 100 - ry, 120 + rx, 100 + ry), outline=110)
    img = glow(img, 1.2, 0.3)
    arr = np.asarray(img, np.float32)
    y, x = np.mgrid[0:H, 0:W]
    def sphere(cx, cy, r, lx, ly, base=255):
        dx, dy = (x - cx) / r, (y - cy) / r
        m = dx * dx + dy * dy <= 1
        z = np.sqrt(np.clip(1 - dx * dx - dy * dy, 0, 1))
        shade = np.clip(dx * lx + dy * ly + z * 0.6, 0, 1) * base
        arr[m] = shade[m]
    arr += radial(120, 100, 55, 255)
    sphere(120, 100, 22, -0.1, -0.1)
    for ang, (rx, ry), r in [(0.6, (60, 40), 5), (2.4, (105, 70), 8), (4.0, (150, 98), 11), (5.6, (200, 128), 7)]:
        px, py = 120 + rx * math.cos(ang), 100 + ry * math.sin(ang)
        vx, vy = 120 - px, 100 - py
        n = math.hypot(vx, vy)
        sphere(px, py, r, vx / n, vy / n)
    # ship trajectory
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    pts = [(250 + 40 * math.cos(t / 10) , 40 + t * 1.2 + 10 * math.sin(t / 6)) for t in range(0, 60, 3)]
    for i, p in enumerate(pts[:-1]):
        if i % 2 == 0:
            d.line([p, pts[i + 1]], fill=230)
    d.polygon([(286, 108), (294, 116), (282, 118)], fill=255)
    save("gravity", img)

# 2. The Claylings: crystal with glow, clay blobs around it, night hills
def claylings():
    y, x = np.mgrid[0:H, 0:W]
    arr = (y / H) * 70.0
    arr += radial(160, 92, 130, 150)
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    d.polygon([(0, 160), (60, 140), (130, 150), (200, 138), (260, 148), (320, 136), (320, 200), (0, 200)], fill=40)
    # crystal
    d.polygon([(160, 40), (180, 85), (160, 130), (140, 85)], fill=245)
    d.polygon([(160, 40), (180, 85), (160, 130)], fill=180)
    d.polygon([(160, 130), (172, 140), (148, 140)], fill=120)
    img = glow(img, 3, 0.5)
    d = ImageDraw.Draw(img)
    def blob(cx, cy, s, lit):
        d.ellipse((cx - 7 * s, cy - 12 * s, cx + 7 * s, cy + 6 * s), fill=lit)
        d.ellipse((cx - 5 * s, cy - 6 * s, cx + 5 * s, cy + 8 * s), fill=lit)
        d.ellipse((cx - 3 * s - 1, cy - 7 * s, cx - 3 * s + 2, cy - 4 * s), fill=0)
        d.ellipse((cx + 2 * s - 1, cy - 7 * s, cx + 2 * s + 2, cy - 4 * s), fill=0)
    for cx, cy, s in [(100, 150, 1.4), (125, 160, 1.1), (205, 152, 1.3), (230, 164, 1.0), (70, 170, 1.2), (260, 176, 1.2)]:
        lit = int(max(90, 230 - abs(cx - 160) * 1.2))
        blob(cx, cy, s, lit)
    # spear on one
    d.line([(214, 128), (218, 158)], fill=210)
    save("claylings", img)

# 3. Wooly Caravan: flock of sheep along a mountain path
def wooly():
    y, x = np.mgrid[0:H, 0:W]
    arr = 40 + (1 - y / H) * 60.0
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    d.polygon([(0, 90), (50, 40), (90, 75), (150, 20), (210, 70), (250, 45), (320, 85), (320, 200), (0, 200)], fill=70)
    d.polygon([(150, 20), (165, 34), (150, 32), (138, 32)], fill=200)
    d.polygon([(0, 130), (320, 110), (320, 200), (0, 200)], fill=95)
    path = [(t, 165 - t * 0.12 + 6 * math.sin(t / 30)) for t in range(0, 321, 4)]
    d.line(path, fill=140, width=22)
    random.seed(9)
    for i in range(40):
        t = 40 + i * 5.5 + random.uniform(-4, 4)
        px, py = t, 165 - t * 0.12 + 6 * math.sin(t / 30) + random.uniform(-9, 9)
        for k in range(4):
            ox, oy = random.uniform(-3, 3), random.uniform(-2, 2)
            d.ellipse((px - 4 + ox, py - 3 + oy, px + 4 + ox, py + 3 + oy), fill=235)
        d.ellipse((px + 4, py - 3, px + 7, py + 1), fill=40)
    # shepherd and dog
    d.rectangle((268, 120, 273, 136), fill=250)
    d.ellipse((266, 112, 275, 121), fill=250)
    d.line([(276, 108), (279, 138)], fill=250, width=2)
    d.ellipse((30, 160, 42, 167), fill=200)
    d.ellipse((40, 155, 47, 161), fill=200)
    # eagle shadow + sight
    d.ellipse((150, 60, 162, 72), outline=255)
    d.line([(156, 54), (156, 78)], fill=255)
    d.line([(144, 66), (168, 66)], fill=255)
    save("wooly", img)

# 4. Face Masker: abstract head, mosaic block, tracking box
def facemask():
    y, x = np.mgrid[0:H, 0:W]
    arr = 30 + (x / W) * 40.0
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    d.ellipse((90, 120, 230, 260), fill=110)  # shoulders
    d.ellipse((125, 35, 195, 125), fill=180)
    d.rectangle((150, 115, 170, 135), fill=150)
    arr = np.asarray(img, np.float32).copy()
    # mosaic
    x0, y0, x1, y1 = 118, 28, 202, 132
    random.seed(2)
    for by in range(y0, y1, 10):
        for bx in range(x0, x1, 10):
            arr[by:by + 10, bx:bx + 10] = random.choice([60, 110, 150, 190, 230])
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    d.rectangle((x0 - 4, y0 - 4, x1 + 4, y1 + 4), outline=255, width=2)
    d.rectangle((x0 - 4, y0 - 16, x0 + 26, y0 - 4), fill=255)
    d.text((x0 - 1, y0 - 16), "ID 3", fill=0)
    # second small face, tracked
    d.ellipse((250, 70, 274, 100), fill=140)
    d.rectangle((244, 64, 280, 106), outline=200)
    save("facemask", img)

gravity(); claylings(); wooly(); facemask()
