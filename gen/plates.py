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
# 365 rather than 391 because the figures sit in a browser window now: the card is
# still 799x391, but 26px of it is the title bar and the image gets what is left.
# A travel percentage measured against a frame the image no longer sits in is a
# number that looks right and scrolls the picture clean past its own end.
SLOT_W, SLOT_H = 799.0, 365.0

# A tall capture only becomes a strip if there is enough below the fold to be worth
# moving. Under this much travel the movement reads as drift rather than as scrolling
# and the plate is better held still.
MIN_TRAVEL = 12.0

# Plates the push machine crops into, which want the extra resolution.
SHARP = {
    # Two whole pages the window scrolls AND the camera closes on. The look
    # lands on 11px token labels, so the delivery has to hold up at the far
    # end of the move rather than only at the resting framing.
    "showcase-full-height",
    "style-guide-full",
    "persona-home-leader",
    "persona-home-edit",
    "persona-catalog",
    "persona-home-contributor",
    "dashboard-default-annotated",
    "dashboard-export-scoped",
    "dorms-gallery-letterbox",
    "stardew-villager-abigail",
    "dashboard-timeline-carryforward",
    "dashboard-timeline-naive",
    "dashboard-events-table-explored",
    "dorms-floorplans-multibuilding",
    "dashboard-button-contact-sheet",
    "dorms-reviews",
    "stardew-arcade-row",
    "dorms-quiz-asked",
    "dorms-quiz-answered",
    "dorms-list",
    "dorms-filter-3",
    "dorms-detail",
    "dorms-quiz-page",
    "island-generator-tiles",
    "dashboard-graph-page",
    "dashboard-drill-1-envs",
    "dashboard-drill-2-regions",
    "dashboard-drill-3-categories",
    "dashboard-drill-4-resource",
}

# Whole pages, kept at the width they were captured. These are not figures cut to
# fit a slot: they are a page sitting behind a window, and the window scrolls them.
# Being a page says nothing about resolution: a page the camera only ever sees
# whole is a normal-width plate, and only the state the camera goes INTO needs to
# be listed in SHARP as well. Marking all four sharp would cost a megabyte to make
# three images that are never seen closer than half size look better at half size.
NATIVE = {
    "resource-detail-full",
    "dashboard-export-scoped",
}

PAGE = {
    "showcase-full-height",
    "style-guide-full",
    "dashboard-drill-1-envs",
    "dashboard-drill-2-regions",
    "dashboard-drill-3-categories",
    "dashboard-drill-4-resource",
    "dashboard-graph-page",
    "dashboard-table-page",
    "dorms-detail",
    "dorms-quiz-page",
    "dorms-quiz-results",
    "dorms-filter-0",
    "dorms-filter-1",
    "dorms-filter-2",
    "dorms-filter-3",
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
        # Two plates the camera goes all the way to 1:1 on, and where 2200 would
        # be an upscale at exactly the framing that matters. Delivered at the
        # capture's own width instead: the point of those two figures is reading
        # an ARN and a line of CSV, and a resampled glyph is the one thing that
        # cannot be recovered later.
        target = (w if name in NATIVE else
                  SHARP_WIDTH if name in SHARP else WIDTH)
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
        if name in PAGE:
            # A page is scrolled by its own machine, from its own numbers. A strip
            # percentage computed against a slot it never sits in would be a number
            # that looks usable and is not.
            travel = 0.0
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
