#!/usr/bin/env python3
"""Compose a scene of The Claylings from the game's own sprites.

    python3 tools/claylings_scene.py ../the-claylings && python3 tools/dither.py tools/raw/claylings.png

Day side on the left (fields, storage, forge, workers), the Crystal in the
middle, and on the right the spearmen holding the line against the spiders.
Writes tools/raw/claylings.png at 288x180, the size dither.py outputs.
"""
import random
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance

GAME = Path(sys.argv[1] if len(sys.argv) > 1 else "../the-claylings") / "Art"
OUT = Path(__file__).resolve().parent / "raw" / "claylings.png"
W, H = 288, 180
random.seed(7)


def sheet(name):
    return Image.open(GAME / name).convert("RGBA")


def frame(img, x, y, w, h):
    return img.crop((x, y, x + w, y + h))


scene = Image.new("RGBA", (W, H))

# ground: the game's tiles, a few variants scattered
ground = sheet("GroundTileSet.png")
tiles = [frame(ground, x, 0, 16, 16) for x in (0, 16, 32, 48)]
for ty in range(0, H, 16):
    for tx in range(0, W, 16):
        scene.alpha_composite(random.choice(tiles), (tx, ty))

items = []  # (y for depth sorting, image, x)
def put(img, x, y):
    items.append((y + img.height, img, x, y))

trees = sheet("Trees.png")
for x, y, kind in [(4, 2, 32), (20, -6, 16), (38, 4, 32), (-4, 30, 16), (60, -10, 32), (250, -12, 32), (270, 4, 16)]:
    put(frame(trees, kind, 0, 16, 48), x, y)

storage = sheet("Buildings/Storage.png")
put(frame(storage, 144, 0, 48, 48), 70, 30)
put(frame(sheet("Buildings/Furnace.png"), 32, 0, 32, 32), 28, 66)
put(sheet("Buildings/Forge.png"), 58, 76)
put(sheet("Buildings/Workbench.png"), 92, 82)

crops = sheet("Crops.png")
for i in range(5):
    for j in range(3):
        put(frame(crops, 16 * ((i + j) % 4), 0, 16, 16), 6 + i * 15, 118 + j * 14)

rocks = sheet("Rocks and ores.png")
put(frame(rocks, 0, 32, 16, 16), 226, 150)
put(frame(rocks, 16, 64, 16, 16), 100, 150)

idle = sheet("Claylings/Villagers/idle.png")
chop = sheet("Claylings/Villagers/woodcutting.png")
haul = sheet("Claylings/Villagers/hauling.png")
put(frame(chop, 16 * 2, 0, 16, 16), 26, 40)
put(frame(chop, 16 * 6, 0, 16, 16), 50, 50)
put(frame(haul, 16, 0, 16, 16), 96, 70)
put(frame(haul, 48, 16, 16, 16), 116, 110)
put(frame(idle, 0, 0, 16, 16), 82, 106)
put(frame(idle, 32, 16, 16, 16), 40, 100)

chick = sheet("Animals/Chicken.png")
put(frame(chick, 0, 0, 16, 16), 118, 150)
put(frame(chick, 32, 0, 16, 16), 132, 160)

spear = sheet("Claylings/Spearmen/spearman_idle.png")
for i, (x, y) in enumerate([(178, 44), (186, 70), (180, 96), (188, 122)]):
    put(frame(spear, 16 * (i * 3 % 12), 0, 16, 32), x, y)

# the spiders are dark blue on a dark ground: lift them so they survive the dithering
spider = ImageEnhance.Brightness(sheet("Enemies/BlueSpider.png")).enhance(2.6)
for x, y, fx in [(236, 50, 0), (254, 82, 64), (232, 108, 128), (262, 124, 32)]:
    put(frame(spider, fx, 32, 32, 32), x, y)

# the Crystal (its sprite is not in the repository: drawn here in the same pixel style)
crystal = Image.new("RGBA", (16, 32))
d = ImageDraw.Draw(crystal)
d.polygon([(8, 1), (14, 13), (8, 29), (2, 13)], fill=(150, 215, 255, 255), outline=(40, 70, 120, 255))
d.polygon([(8, 1), (14, 13), (8, 29)], fill=(90, 170, 240, 255))
d.line([(5, 9), (7, 5)], fill=(240, 250, 255, 255))
put(crystal, 140, 62)

for _, img, x, y in sorted(items, key=lambda t: t[0]):
    scene.alpha_composite(img, (x, y))

# night falling from the right, and the Crystal's light
g = np.asarray(scene.convert("L"), dtype=np.float32)
yy, xx = np.mgrid[0:H, 0:W]
light = np.clip(1 - np.hypot(xx - 148, (yy - 78) * 1.3) / 70, 0, 1) ** 1.5
night = np.clip((xx - 120) / 170, 0, 1)
g = g * (1.15 - 0.55 * night) + 120 * light
Image.fromarray(np.clip(g, 0, 255).astype(np.uint8)).save(OUT)
print(f"{OUT}")
