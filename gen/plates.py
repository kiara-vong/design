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

from PIL import Image, ImageDraw

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

# Plates whose subject runs to both edges of the capture.
#
# The slot draws every plate with object-fit:cover, which crops a wide capture to
# the slot's own 2.04 and throws the sides away. For most captures that is fine --
# the middle is the subject. For these it is not: the thing the caption names lives
# in the strip cover discards, so the figure argued for something it never showed.
# A review's stars sit hard right of an otherwise empty card; the letterboxed photo
# is only legible BECAUSE of the blurred bands at its two edges; the export control
# is at one end of a row and the count it belongs to is at the other.
#
# So these are composited onto a ground at the slot's own aspect instead, which is
# what the reference build does with every screenshot on its case-study pages: the
# capture sits ON a surface with air around it rather than bleeding to the edges.
# Nothing is cropped, the whole frame is legible at rest, and --fx/--fy then land
# where they say they do, because the plate and the slot finally agree on a shape.
FRAMED = {
    "dorms-gallery-letterbox",
    "dashboard-export-scoped",
    # Wide interface captures whose first column or leftmost label is the thing the
    # caption is about. Cover took the timestamps off the event table, the building
    # names off the floor plans, and both end labels off the contact sheet.
    "dashboard-events-table-explored",
    "dorms-floorplans-multibuilding",
    "dashboard-button-contact-sheet",
    # A single review card, laid out full-bleed: blurred author at one end,
    # rating at the other, the words down in a corner. Cover can frame any one
    # of those three and never two.
    "dorms-reviews",
    "stardew-arcade-row",
}

# The ground the framed plates sit on, and the air around them. --dove-ivory from
# site.css, which is the same surface the case-study page itself is painted in, so
# the inset reads as the page showing through rather than as a border drawn on.
GROUND = (245, 242, 229)
STROKE = (227, 225, 204)
INSET = 0.045          # air on the long side, as a fraction of plate width


def frame(im, target):
    """Sit a capture on a ground at the slot's aspect, with air around it.

    Sized so the capture keeps `target` as its LONG side wherever it can: the
    ground grows around it rather than the capture shrinking into a fixed box, so
    a framed plate carries the same detail per pixel as an unframed one.
    """
    iw, ih = im.size
    inset = int(round(target * INSET))
    cw = target - inset * 2                       # capture width inside the frame
    ch = int(round(ih * cw / float(iw)))
    gw = target
    gh = max(int(round(gw / (SLOT_W / SLOT_H))), ch + inset * 2)
    # A capture taller than the slot's aspect allows would be squeezed by the
    # ground rather than framed by it; widen the ground to keep the air even.
    if ch + inset * 2 > gh:
        gh = ch + inset * 2
    out = Image.new("RGB", (gw, gh), GROUND)
    x, y = (gw - cw) // 2, (gh - ch) // 2
    out.paste(im.resize((cw, ch), Image.LANCZOS), (x, y))
    # A hairline so the capture's own white does not dissolve into the ground.
    ImageDraw.Draw(out).rectangle([x - 1, y - 1, x + cw, y + ch],
                                  outline=STROKE, width=1)
    return out


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
        if name in FRAMED:
            im = frame(im, target)
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
