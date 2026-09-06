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
SRC = os.path.join(OUT, "_src")     # captures that arrived through CAPTURE.md
SHOTS = os.path.join(os.environ.get("TEMP", "/tmp"), "shots")
PROJ = ".."

# The window the capture scrolls inside, in the desktop canvas's own pixels, and the
# width the capture is drawn at inside it. Both measured in the browser rather than
# derived: .tile-view is 248 tall and .tile-win is 322 wide. They are here so the
# travel below is computed rather than eyeballed, which is how it went wrong before:
# the values were once measured in the capture's own 776px space and applied against
# a 322px render, so every one of them was about 2.8x too large and the animation ran
# the image clean past its own bottom edge.
VIEW_H, VIEW_W = 248.0, 322.0

# The ground each tile's drawn browser frame sits on. It used to be one flat colour
# per tile, sampled from the capture. It is a painting now, cut from the same folder
# the page grounds come from, so the six tiles are bordered by the same hands the
# hero and the About page are.
#
# Only a border of it is ever visible: .tile-win insets 8.5% either side and 15% at
# the top, so what shows is a frame a few dozen pixels wide. That is the whole reason
# this works at all. A painting behind a screenshot would fight it; a painting AROUND
# one reads as a mount.
#
# Chosen for tone against the capture inside, not for subject: a warm ground under a
# warm page, a cool one under a cool page, and the darkest painting under Pac-Man,
# which is the only capture that is nearly black.
FIELD_W, FIELD_H = 776, 624
# Matched on a SUBSTRING rather than a filename. Half of these files carry an en
# dash or an accented character in their name, and spelling those back out in a
# source file is a way to silently match nothing.
FIELDS = {
    "ac":      ("RENOIR", 0.62),
    "dorms":   ("Chamaillard", 0.45),
    "stardew": ("Ottis-Adams", 0.55),
    "uxfolio": ("Seurat", 0.5),
    "chess":   ("Jacob-Alberts", 0.5),
    "pacman":  ("Wisinger-Florian", 0.72),
}
HERO_SRC = os.path.join("assets", "hero", "_src")

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


def source(slug, fallback):
    """Prefer the staged capture, fall back to whatever built the tile before.

    assets/tile/_src/<slug>.png is where CAPTURE.md tells people to put things, so
    a capture landing there should be picked up without editing this file.
    """
    staged = os.path.join(SRC, slug + ".png")
    return staged if os.path.exists(staged) else fallback


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
    src = source(slug, src)
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
    # How far this capture has to travel, as a PERCENTAGE OF ITS OWN HEIGHT, which
    # is the only form that survives a phone: translateY resolves a percentage
    # against the image, and mobile.css scales card and image together.
    #
    # A capture with nothing below the fold gets no travel and takes the .pan
    # treatment instead, which moves the frame across a still rather than the still
    # through the frame.
    drawn = h * VIEW_W / float(TILE_W)
    travel = round((1.0 - VIEW_H / drawn) * 100.0, 2) if drawn > VIEW_H else None
    # The painting behind the frame, if this tile has one.
    ground = None
    if slug in FIELDS:
        key, focus = FIELDS[slug]
        hits = [f for f in sorted(os.listdir(HERO_SRC)) if key in f]
        fpath = os.path.join(HERO_SRC, hits[0]) if hits else None
        if fpath:
            g = ImageOps.exif_transpose(Image.open(fpath).convert("RGB"))
            g = ImageOps.fit(g, (FIELD_W, FIELD_H), Image.LANCZOS,
                             centering=(0.5, focus))
            g.save(os.path.join(OUT, "field-%s.webp" % slug),
                   "WEBP", quality=84, method=6)
            ground = "field-%s.webp" % slug
        else:
            print("     no painting matched %r for %s" % (key, slug))
    meta[slug] = {"field": field, "h": h, "travel": travel, "ground": ground}
    print("  %-10s %dx%d  field %s  travel %s"
          % (slug + ".jpg", TILE_W, h, field,
             ("%.2f%%" % travel) if travel else "pan"))

io.open("tile-index.json", "w", encoding="utf-8").write(
    json.dumps(meta, indent=2, sort_keys=True))
print("wrote tile-index.json")
