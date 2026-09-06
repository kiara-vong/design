# -*- coding: utf-8 -*-
"""Archive tile artwork: real captures, prepared for a CSS window frame.

Fifth pass, and the reason for it is worth stating: the tiles needed to move.

Every earlier version baked the whole tile -- field, browser chrome, screenshot,
shadow -- into one flat image, which is accurate and coherent and completely
static. The reference build does not do that. Its cards keep the screenshot as its
own layer inside a frame and then MOVE it: card one scrolls a tall capture inside
a device viewport, which is how a thumbnail shows a page rather than a screenful.

So this script no longer draws frames. It only prepares the content layer: each
capture cropped to a fixed width and left as tall as it really is, so the page's
CSS can scroll it inside a window it draws itself. The frame moved to index.html
where it is one rule for all six instead of six baked copies, and the tiles gained
motion for free.

Output width is fixed at TILE_W so every capture scrolls at the same rate for a
given duration; only the height varies, and the page derives the travel from it.
"""
import io
import json
import os
from PIL import Image, ImageOps

OUT = "assets/tile"
TILE_W = 776                  # 2x the .mini-shot slot's width
MIN_H = 500
SHOTS = os.path.join(os.environ.get("TEMP", "/tmp"), "shots")
PROJ = ".."

# (slug, source, field colour, crop-from-top). A page wants its top; a render or a
# game board wants its middle.
TILES = [
    ("ac",       os.path.join(PROJ, "animal-crossing", "img", "sample.png"),
     "#BDE3F0", "trim"),
    ("dorms",    os.path.join(SHOTS, "live2_dorms.png"), "#F0E4DC", "top"),
    ("stardew",  os.path.join(SHOTS, "tall_stardew.png"), "#EEEAD6", "top"),
    ("uxfolio",  os.path.join(SHOTS, "tall_uxfolio.png"), "#D6DBEA", "top"),
    ("chess",    os.path.join(SHOTS, "tall_chess.png"),   "#E8DCC0", "mid"),
    ("pacman",   os.path.join(SHOTS, "pan_pacman.png"),   "#12131A", "mid"),
]


def trim_white(im, tol=12, pad=20):
    from PIL import ImageChops
    bg = Image.new("RGB", im.size, (255, 255, 255))
    box = ImageChops.difference(im, bg).convert("L").point(
        lambda p: 255 if p > tol else 0).getbbox()
    if not box:
        return im
    return im.crop((max(0, box[0] - pad), max(0, box[1] - pad),
                    min(im.size[0], box[2] + pad), min(im.size[1], box[3] + pad)))


if not os.path.isdir(OUT):
    os.makedirs(OUT)

meta = {}
print("tile content layers:")
for slug, src, field, mode in TILES:
    if not src.lower().endswith((".png", ".jpg", ".jpeg")) or not os.path.exists(src):
        print("  skip %-9s (no capture yet)" % slug)
        meta[slug] = {"field": field, "h": None}
        continue
    im = ImageOps.exif_transpose(Image.open(src).convert("RGB"))
    if mode == "trim":
        im = trim_white(im)
    # One width for all six, so a given scroll duration means the same speed
    # everywhere; height is whatever the capture really is.
    h = max(MIN_H, int(im.size[1] * TILE_W / float(im.size[0])))
    im = im.resize((TILE_W, h), Image.LANCZOS)
    im.save(os.path.join(OUT, "%s.jpg" % slug), quality=88, optimize=True)
    meta[slug] = {"field": field, "h": h}
    print("  %-10s %dx%d  field %s" % (slug + ".jpg", TILE_W, h, field))

io.open("tile-index.json", "w", encoding="utf-8").write(
    json.dumps(meta, indent=2, sort_keys=True))
print("wrote tile-index.json")
