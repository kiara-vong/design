# -*- coding: utf-8 -*-
"""Prepare the captured stills for delivery, and compute what each one has to move.

The captures land in assets/tile/_src as full-resolution PNG: 50MB across 46 files,
several of them 3136px wide and one 5436px tall. None of that can be served. A
portfolio that costs someone 50MB to read is a portfolio nobody reads, and the
widest any of these is ever drawn is 799 CSS px.

So this is the same job gen/tiles.py does for the home thumbnails, pointed at the
case-study and project figures instead:

  - one delivery width for everything, WebP rather than PNG, since these are
    screenshots of interfaces where WebP's advantage over JPEG is largest: flat
    fills and hard type edges are exactly what JPEG's chroma subsampling smears;
  - travel computed rather than measured by hand, as a percentage of the image's
    own height, for the tall ones that scroll behind a fixed frame;
  - an index the page generators read, so no travel number is ever typed twice.

WIDTH is 1600 rather than 1598, which would be exactly 2x the slot. The extra two
pixels are meaningless; the round number is there so nobody reads 1598 as a
measurement that has to be kept in sync with something.

The push machine crops in to --z, so a plate it uses is drawn at up to 1.45x the
slot and wants the resolution to survive it. Those are listed in SHARP and get more
width. Everything else is a straight fit.
"""
import io
import json
import os

from PIL import Image

SRC = os.path.join("assets", "tile", "_src")
OUT = os.path.join("assets", "plate")

WIDTH = 1600
SHARP_WIDTH = 2200      # for plates the push machine crops into
QUALITY = 82

# The slot every one of these is drawn in, in CSS pixels. .cs-media, from
# case-study.css, and the number the travel below is computed against.
SLOT_W, SLOT_H = 799.0, 391.0

# A tall capture only becomes a strip if there is enough below the fold to be worth
# moving. Under this much travel the movement reads as drift rather than as scrolling
# and the plate is better held still.
MIN_TRAVEL = 12.0

# Plates the push machine crops into, which want the extra resolution.
SHARP = {
    "dashboard-default-annotated",
    "dashboard-export-scoped",
    "dorms-gallery-letterbox",
    "stardew-villager-abigail",
    "dashboard-timeline-carryforward",
    "dashboard-events-table-explored",
    "dorms-floorplans-multibuilding",
    "dashboard-button-contact-sheet",
    "dorms-reviews",
    "stardew-arcade-row",
}

# Captures that are the home page's thumbnails, prepared by gen/tiles.py from the
# same folder. Preparing them twice would put a second copy of each on disk.
SKIP = {"dorms", "stardew", "uxfolio", "chess", "pacman", "ac",
        # A whole-page capture kept as the source the tile and several
        # plates are cut from, rather than a figure in its own right.
        "stardew-full"}





def main():
    if not os.path.isdir(SRC):
        print("  no %s; nothing to prepare" % SRC)
        return
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    index, total = {}, 0
    for f in sorted(os.listdir(SRC)):
        if not f.lower().endswith((".png", ".jpg", ".jpeg")):
            continue
        name = os.path.splitext(f)[0]
        if name in SKIP:
            continue
        im = Image.open(os.path.join(SRC, f)).convert("RGB")
        w, h = im.size
        target = SHARP_WIDTH if name in SHARP else WIDTH
        if w > target:
            im = im.resize((target, int(round(h * target / float(w)))), Image.LANCZOS)
        w, h = im.size
        dst = os.path.join(OUT, name + ".webp")
        im.save(dst, "WEBP", quality=QUALITY, method=6)
        kb = os.path.getsize(dst) / 1024.0
        total += kb

        # Drawn at the slot's width, how far past its bottom edge does it run?
        drawn = SLOT_W * h / float(w)
        travel = round((1.0 - SLOT_H / drawn) * 100.0, 2) if drawn > SLOT_H else 0.0
        index[name] = dict(w=im.size[0], h=im.size[1],
                           travel=travel if travel >= MIN_TRAVEL else 0.0,
                           kb=int(kb))
        print("  %-44s %-11s %5dKB  %s"
              % (name + ".webp", "%dx%d" % im.size, kb,
                 ("strip %.2f%%" % travel) if travel >= MIN_TRAVEL else "fits"))
    with io.open("plate-index.json", "w", encoding="utf-8") as fh:
        fh.write(json.dumps(index, indent=1, sort_keys=True) + "\n")
    print("%d plates, %.1fMB total" % (len(index), total / 1024.0))


if __name__ == "__main__":
    main()
