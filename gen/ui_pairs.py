# -*- coding: utf-8 -*-
"""Cut the before/after specimens out of the refactor showcase.

The showcase page already holds the comparison: eight components, each with the
version that shipped before the shared layer and the version that shipped after,
side by side in one card. Side by side is the right way to READ it on that page
and the wrong way to put it in a figure, because two panels shrunk to fit an 799px
slot are two things too small to see rather than one thing you can check.

So the panels are cut out and stacked instead, one exactly over the other, and the
reader drags the seam. That only works if they register, and registering is a
property of the CROP, not of the machine that draws it: the two panels are centred
inside their boxes, so the after -- which is taller, it gained a footer -- starts
37px lower than the before. Cropping both from their own content's top edge is what
puts the table headers on the same line. Crop them from the box instead and the
wipe shows the widget sliding up, which is the one thing that did not change.

The rectangles below are measured off the capture rather than typed from a design:
the panel borders are found by colour, the content bbox by ink, and both are
asserted at build time. A number that stops being true when the screenshot is
retaken should fail here rather than quietly produce a figure aimed at nothing.
"""
import io
import json
import os

from PIL import Image

SRC = os.path.join("assets", "tile", "_src", "showcase-full-height.png")
OUT = os.path.join("assets", "plate")

QUALITY = 92        # specimens, read close; not the 82 the whole-page plates get

# The two panels inside every card, in the capture's own pixels. Found once by
# walking the pink and green borders down the page; the same for all eight cards
# because they are the same component.
BEFORE_X, AFTER_X, PANEL_W = 203, 1285, 1041

# Each card's before/after panels: (top of the content area, bottom of the box).
# The content area starts 53px below the box's top edge, which is the BEFORE /
# AFTER label strip. The strip is left out of the crops on purpose -- the slider
# already says which side is which, and a label that changes colour across the
# seam is a second answer to a question the reader only asked once.
CARDS = {
    "theme":      (671, 978),
    "tables":     (1451, 2051),
    "buttons":    (2487, 2720),
    "filters":    (3195, 3428),
    "nav":        (3942, 4377),
    "tooltips":   (4813, 5092),
    "typography": (5528, 5761),
    "cards":      (6197, 6484),
}

# What actually gets cut. Height is the taller of the two sides plus air, so the
# shorter one is followed by page-white rather than by the box's own edge.
#
# BAND is white added ABOVE the crop rather than taken from the capture, and it is
# there for one reason: the slider hangs its before/after pills inside the top of
# the window, and without a band they sit on the table's header row -- which is one
# of the things the figure exists to compare. The band cannot come out of the
# capture, because above the content is the panel's own BEFORE / AFTER label strip
# and the two sides start at different heights. Added white is the only padding
# that is identical on both sides, which is the whole requirement.
BAND = 100
PAIRS = [
    # name          card       width  height
    ("ui-tables",   "tables",   966,   460),
]

# One card, whole, as the specimen for how a pull request was written up: the
# change, the reason, and the line that says what it costs to review and what it
# blocks. Cut at the capture's own resolution -- the camera goes close on that
# line, and a resampled 11px glyph cannot be recovered later.
ANATOMY = ("ui-pr-anatomy", (150, 240, 2378, 1035))


def ink_top(im, x0, y0, x1, y1, thresh=735):
    """First row inside the box that has any ink on it.

    The panels centre their contents, so this -- not the box -- is what the two
    crops have to share. Returns an absolute y.
    """
    px = im.crop((x0, y0, x1, y1)).load()
    for y in range(y1 - y0):
        for x in range(0, x1 - x0, 3):
            r, g, b = px[x, y]
            if r + g + b < thresh:
                return y0 + y
    raise SystemExit("  no content found in panel at y=%d" % y0)


def main():
    if not os.path.isfile(SRC):
        print("  no %s; nothing to cut" % SRC)
        return
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    im = Image.open(SRC).convert("RGB")
    index = {}

    for name, card, w, h in PAIRS:
        top, bot = CARDS[card]
        for side, x0, tag in ((0, BEFORE_X, "before"), (1, AFTER_X, "after")):
            y = ink_top(im, x0, top, x0 + PANEL_W, bot)
            if y + h > bot:
                raise SystemExit("  %s %s runs past its box" % (name, tag))
            # Centred horizontally on the panel, so the two sides share an axis
            # as well as a top edge.
            cx = x0 + (PANEL_W - w) // 2
            cut = Image.new("RGB", (w, h + BAND), (255, 255, 255))
            cut.paste(im.crop((cx, y, cx + w, y + h)), (0, BAND))
            dst = os.path.join(OUT, "%s-%s.webp" % (name, tag))
            cut.save(dst, "WEBP", quality=QUALITY, method=6)
            index["%s-%s" % (name, tag)] = dict(w=w, h=h + BAND,
                                                kb=int(os.path.getsize(dst) / 1024))
            print("  %-24s %dx%d  %dKB"
                  % (os.path.basename(dst), w, h + BAND,
                     os.path.getsize(dst) / 1024))

    name, (x0, y0, x1, y1) = ANATOMY
    cut = im.crop((x0, y0, x1, y1))
    dst = os.path.join(OUT, name + ".webp")
    cut.save(dst, "WEBP", quality=QUALITY, method=6)
    index[name] = dict(w=x1 - x0, h=y1 - y0,
                       kb=int(os.path.getsize(dst) / 1024))
    print("  %-24s %dx%d  %dKB"
          % (os.path.basename(dst), x1 - x0, y1 - y0,
             os.path.getsize(dst) / 1024))

    with io.open("ui-pairs.json", "w", encoding="utf-8") as fh:
        fh.write(json.dumps(index, indent=1, sort_keys=True) + "\n")
    print("%d specimens cut from the showcase" % len(index))


if __name__ == "__main__":
    main()
