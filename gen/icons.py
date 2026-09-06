# -*- coding: utf-8 -*-
"""Cut the hand-drawn flower and cat icons out of one sheet, and build the footer
strips and the link cursor from them.

KEYING. The sheet's ground is a soft colour wash that runs red to green to blue
across its own width, so no colour threshold can separate it: the value that keys the
ground under the red poppies keys the poppies themselves under the blue. What does
separate them is TEXTURE. The wash is low frequency by construction and has no edges
anywhere; the drawings are stippled crayon, which is nothing but edges. Subtracting a
heavy blur from the image leaves near zero on the ground and a great deal on a
drawing, and thresholding that difference finds all 23 sprites cleanly.

Holes are filled from the outside rather than by dilation. A daisy is mostly gaps
between its own stems, and dilating enough to close those would eat the gaps that are
meant to be there. Flood filling the inverse from the crop's border marks only ground
that is connected to the outside, which is the same trick gen/mascot.py uses.

THE FOOTER STRIP GEOMETRY IS NOT NEGOTIABLE. site.css crops three tiles out of one
sprite with object-position 0, -122.504 and -245.007 against a 120 x 110.504 box, so
a strip has to be exactly three tiles on that pitch. A shorter image leaves the second
and third tiles empty, which is the bug the About footer had for months.
"""
import io
import json
import os
from collections import deque

from PIL import Image, ImageChops, ImageFilter

SRC = os.path.join("assets", "ui", "_src", "icon-sheet.png")
OUT = os.path.join("assets", "ui")
ICONS = os.path.join(OUT, "icon")

# Segmentation. K is the factor the mask is found at: fine enough to separate
# neighbours, coarse enough that stipple does not fragment a drawing into pieces.
K, TH, MIN_BLOB = 4, 6, 120
BLUR = 9

# The CUT uses a different key from the segmentation, and it has to.
#
# Each sprite on the sheet sits on a soft light glow. At the wide blur radius that
# finds the sprites reliably, that glow reads as texture and is keyed IN, which put a
# pale fog inside every drawing: most visible between a daisy's stems, and obvious
# against the dark footer band. Raising the threshold does not fix it, because a
# cream petal and a cream glow are equally bright and the petals erode first.
#
# What separates them is FREQUENCY. The glow is a smooth gradient; the drawing is
# crayon stipple. A small blur radius differences out only the finest texture, which
# the drawing has everywhere and the glow has nowhere. Three is where the fog goes
# and the petals stay whole; two leaves haze and four starts biting into them.
CUT_BLUR, CUT_TH, CUT_CLOSE = 3, 5, 3

# Delivery. The tile is 120 x 110.504 in CSS; 2x keeps it sharp on a retina screen.
TILE_W, TILE_H = 240.0, 221.008
PITCH = 245.008
PAD = 0.90            # how much of the tile a drawing may fill, so nothing touches

# Per-page strips. Read as (row, column), 1-based, against the sheet's own layout:
# row 1 has six, row 2 six, row 3 seven, row 4 the four cats.
#
# Each page gets a flower, a cat and a flower, so the cat is framed rather than
# stacked at an end, except the case studies, which get foliage and no cat: those
# pages are the serious ones and a cat in the corner undercuts them.
STRIPS = {
    "foot-home":     [(1, 2), (4, 1), (2, 4)],   # daisies, Lyra the tabby, daisies
    "foot-projects": [(1, 1), (4, 2), (2, 1)],   # poppies, the black cat, yellow tulips
    "foot-art":      [(2, 5), (4, 3), (1, 6)],   # pink cosmos, the calico, purple
    "foot-about":    [(1, 4), (4, 4), (3, 4)],   # forget-me-nots, Goose, lily of the valley
    "foot-work":     [(3, 1), (3, 6), (3, 7)],   # sprig, daisies, bow: foliage only
}

# The link cursor. Third row, second item.
CURSOR_AT = (3, 2)
CURSOR_W, CURSOR_H = 24, 32



def energy(im, blur=None, close=5):
    """Texture, not colour: |image - blur|, closed enough to bridge stipple.

    The radius decides WHICH texture. Wide finds whole sprites against the ground;
    narrow finds only the crayon grain, which is what separates a drawing from the
    soft glow the sheet paints behind it.

    The CLOSING filter is the other half, and it is what put a pale fog between a
    daisy's stems. Dilating the energy bridges gaps in the stipple, which is exactly
    what segmentation wants -- a sprite should come back as one blob. But it also
    bridges the real gaps BETWEEN the stems, which are only a few pixels wide, so the
    whole space between them was marked as drawing and filled with the sheet's own
    glow. Five closes those gaps; three leaves them open and still holds the stipple
    together.
    """
    r = BLUR if blur is None else blur
    d = ImageChops.difference(im, im.filter(ImageFilter.GaussianBlur(r))).convert("L")
    return d.filter(ImageFilter.MaxFilter(close)) if close > 1 else d


def blobs(mask, w, h):
    seen = bytearray(w * h)
    out = []
    for sy in range(h):
        for sx in range(w):
            i = sy * w + sx
            if seen[i] or not mask[i]:
                continue
            q = deque([(sx, sy)]); seen[i] = 1
            x0 = x1 = sx; y0 = y1 = sy; n = 0
            while q:
                x, y = q.popleft(); n += 1
                if x < x0: x0 = x
                if x > x1: x1 = x
                if y < y0: y0 = y
                if y > y1: y1 = y
                for dx, dy in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)):
                    nx, ny = x + dx, y + dy
                    j = ny * w + nx
                    if 0 <= nx < w and 0 <= ny < h and not seen[j] and mask[j]:
                        seen[j] = 1; q.append((nx, ny))
            if n > MIN_BLOB:
                out.append((x0, y0, x1, y1))
    return out


def rows_of(boxes, n_rows=4):
    """Split into n_rows by the largest vertical gaps, then order each left to right.

    Clustering on a tolerance does not work here and the reason is worth stating: the
    sprites are wildly different heights, so a short bow and a tall spray of daisies
    in the same row have centres far enough apart to be called two rows, while the
    cats below them are tall enough to reach back up into the row above. Sorting the
    centres and cutting at the three biggest consecutive gaps uses the one thing that
    IS reliable, which is that the gap between rows is larger than any gap within one.
    """
    boxes = sorted(boxes, key=lambda b: (b[1] + b[3]) / 2.0)
    mid = [(b[1] + b[3]) / 2.0 for b in boxes]
    gaps = sorted(range(1, len(boxes)), key=lambda i: mid[i] - mid[i - 1],
                  reverse=True)[:n_rows - 1]
    cuts = [0] + sorted(gaps) + [len(boxes)]
    return [sorted(boxes[cuts[i]:cuts[i + 1]], key=lambda b: b[0])
            for i in range(len(cuts) - 1)]


def cut(im, box, pad=10):
    """One sprite with a keyed, feathered alpha."""
    W, H = im.size
    x0 = max(0, box[0] - pad); y0 = max(0, box[1] - pad)
    x1 = min(W, box[2] + pad); y1 = min(H, box[3] + pad)
    crop = im.crop((x0, y0, x1, y1))
    e = energy(crop, CUT_BLUR, CUT_CLOSE)
    w, h = crop.size
    m = bytearray(1 if v > CUT_TH else 0 for v in e.getdata())

    # Ground is whatever the border can reach through the holes. Everything the
    # flood cannot reach is inside the drawing and stays opaque, which is what keeps
    # the gaps between a daisy's own stems from being punched out.
    out = bytearray(m)
    seen = bytearray(w * h)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if not m[y*w+x] and not seen[y*w+x]:
                seen[y*w+x] = 1; q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if not m[y*w+x] and not seen[y*w+x]:
                seen[y*w+x] = 1; q.append((x, y))
    while q:
        x, y = q.popleft()
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx, ny = x + dx, y + dy
            j = ny * w + nx
            if 0 <= nx < w and 0 <= ny < h and not seen[j] and not m[j]:
                seen[j] = 1; q.append((nx, ny))
    # Fill only the SMALL enclosed gaps.
    #
    # Filling every region the border cannot reach was wrong for this artwork, and
    # wrong in the most visible way: a spray of daisies encloses big pockets of empty
    # ground between its own stems, ringed by flowers above and leaves at the sides,
    # so the flood could not get in and every one of those pockets was filled solid
    # with the sheet's own wash. On the dark footer band it read as a pale fog inside
    # the drawing, which is exactly the "fill in around the transparent background"
    # that made these look wrong.
    #
    # Small pockets still want filling: a flat patch inside a black cat has no texture
    # for the energy mask to find and would otherwise be punched through. So the test
    # is area. Under a fiftieth of the crop it is a gap in the drawing; over it, it is
    # ground the drawing happens to surround.
    LIMIT = max(60, int(w * h * 0.02))
    filled = bytearray(w * h)
    for sy in range(h):
        for sx in range(w):
            i = sy * w + sx
            if seen[i] or m[i] or filled[i]:
                continue
            q2 = deque([(sx, sy)]); filled[i] = 1; cells = [i]
            while q2:
                x, y = q2.popleft()
                for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx, ny = x + dx, y + dy
                    j = ny * w + nx
                    if (0 <= nx < w and 0 <= ny < h and not seen[j]
                            and not m[j] and not filled[j]):
                        filled[j] = 1; q2.append((nx, ny)); cells.append(j)
            if len(cells) <= LIMIT:
                for j in cells:
                    out[j] = 1

    # Keep only the biggest piece. Each sprite sits close enough to its neighbours
    # that the crop catches a tick or two of the drawing beside it, and a stray mark
    # floating off a flower reads as damage rather than as texture.
    out = _largest(out, w, h)

    # ERODE, do not dilate, and barely feather.
    #
    # The first pass grew the mask a pixel and blurred it over one, which put a soft
    # rim of the sheet's own colour wash around every drawing: a blurry outline that
    # follows the shape and belongs to neither the icon nor the page. Pulling the
    # mask IN by a pixel lands the edge inside the drawing's own ink instead, and
    # half a pixel of blur is enough to keep it from stair-stepping.
    a = Image.frombytes("L", (w, h), bytes(255 if v else 0 for v in out))
    a = a.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.5))
    sprite = crop.convert("RGBA")
    sprite.putalpha(a)
    return sprite.crop(sprite.getbbox() or (0, 0, w, h))


def _largest(m, w, h):
    """Zero everything but the largest connected run of set pixels."""
    seen = bytearray(w * h)
    best, best_n = None, 0
    for sy in range(h):
        for sx in range(w):
            i = sy * w + sx
            if seen[i] or not m[i]:
                continue
            q = deque([(sx, sy)]); seen[i] = 1; cells = [i]
            while q:
                x, y = q.popleft()
                for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx, ny = x + dx, y + dy
                    j = ny * w + nx
                    if 0 <= nx < w and 0 <= ny < h and not seen[j] and m[j]:
                        seen[j] = 1; q.append((nx, ny)); cells.append(j)
            if len(cells) > best_n:
                best, best_n = cells, len(cells)
    keep = bytearray(w * h)
    for i in (best or []):
        keep[i] = 1
    return keep


def bleed(im, rounds=6):
    """Push the drawing's colour outward into its transparent margin.

    This is the halo. A cut sprite still carries the sheet's colour wash in every
    pixel it made transparent, because keying only changes alpha. Nothing shows while
    the image is drawn at its own size, since those pixels have alpha 0. The moment it
    is RESIZED, though, the resampler averages neighbouring pixels channel by channel
    and has no idea some of them are meant to be invisible, so the wash bleeds back in
    along every edge as a coloured fringe. It is drawn twice here, once when the strip
    is assembled and once by the browser scaling 240 into 120, so it compounds.

    Fixing the alpha cannot help; the colour underneath has to change. Each round
    blurs the picture and keeps the blur only where the image is transparent, which
    walks the edge colour outward a pixel at a time. Then a resample finds the
    drawing's own colour on both sides of its edge and has nothing foreign to mix in.
    """
    im = im.convert("RGBA")
    a = im.getchannel("A")
    solid = a.point(lambda v: 255 if v > 0 else 0)
    rgb = im.convert("RGB")
    for _ in range(rounds):
        rgb = Image.composite(rgb, rgb.filter(ImageFilter.BoxBlur(1)), solid)
        solid = solid.filter(ImageFilter.MaxFilter(3))
    out = rgb.convert("RGBA")
    out.putalpha(a)
    return out


def fit(sprite, box_w, box_h):
    """Scale a sprite to sit inside one tile without touching its edges."""
    w, h = sprite.size
    s = min(box_w * PAD / w, box_h * PAD / h)
    return sprite.resize((max(1, int(w * s)), max(1, int(h * s))), Image.LANCZOS)


def main():
    if not os.path.exists(SRC):
        print("  no %s" % SRC)
        return
    for d in (ICONS,):
        if not os.path.isdir(d):
            os.makedirs(d)
    im = Image.open(SRC).convert("RGB")
    W, H = im.size
    sm = energy(im).resize((W // K, H // K), Image.BOX)
    w, h = sm.size
    found = blobs(bytearray(1 if v > TH else 0 for v in sm.getdata()), w, h)
    grid = rows_of([(b[0]*K, b[1]*K, b[2]*K, b[3]*K) for b in found])
    print("  sheet %dx%d -> %d rows: %s"
          % (W, H, len(grid), [len(r) for r in grid]))

    sprites, index = {}, {}
    for ri, row in enumerate(grid, 1):
        for ci, box in enumerate(row, 1):
            s = bleed(cut(im, box))
            sprites[(ri, ci)] = s
            name = "r%dc%d" % (ri, ci)
            s.save(os.path.join(ICONS, name + ".png"))
            index[name] = list(s.size)

    # The three-tile footer strips.
    for name, cells in sorted(STRIPS.items()):
        strip = Image.new("RGBA", (int(TILE_W), int(round(PITCH * 2 + TILE_H))),
                          (0, 0, 0, 0))
        for i, cell in enumerate(cells):
            s = fit(sprites[cell], TILE_W, TILE_H)
            x = int((TILE_W - s.size[0]) / 2)
            y = int(PITCH * i + (TILE_H - s.size[1]) / 2)
            strip.alpha_composite(s, (x, y))
        strip.save(os.path.join(OUT, name + ".png"))
        print("  %-14s %s  %s" % (name + ".png", "%dx%d" % strip.size,
                                  " + ".join("r%dc%d" % c for c in cells)))

    # The cursor. Windows silently ignores anything over 32px in either dimension.
    cur = sprites[CURSOR_AT]
    cw = int(round(CURSOR_H * cur.size[0] / float(cur.size[1])))
    cur = cur.resize((min(CURSOR_W, cw), CURSOR_H), Image.LANCZOS)
    cur.save(os.path.join(OUT, "link-cursor.png"))
    print("  link-cursor.png %dx%d  <- r%dc%d"
          % ((CURSOR_W, CURSOR_H) + CURSOR_AT))

    with io.open("icon-index.json", "w", encoding="utf-8") as fh:
        fh.write(json.dumps(index, indent=1, sort_keys=True) + "\n")
    print("%d icons" % len(index))


if __name__ == "__main__":
    main()
