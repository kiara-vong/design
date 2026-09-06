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

# The link and footer cursor. Third row, second item.
CURSOR_AT = (3, 2)
CURSOR_W, CURSOR_H = 24, 32


def energy(im):
    """Texture, not colour: |image - heavy blur|, closed enough to bridge stipple."""
    d = ImageChops.difference(im, im.filter(ImageFilter.GaussianBlur(BLUR)))
    return d.convert("L").filter(ImageFilter.MaxFilter(5))


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
    e = energy(crop)
    w, h = crop.size
    m = bytearray(1 if v > TH else 0 for v in e.getdata())

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
    for i in range(w * h):
        if not seen[i]:
            out[i] = 1

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
            s = cut(im, box)
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
    # A second one for dark grounds. The footer band is a dark painting and a
    # mid-green clover sinks into it, so that copy gets a cream outline: the alpha
    # spread wide behind the drawing, filled with the page's parchment.
    halo = cur.getchannel("A").filter(ImageFilter.MaxFilter(5))
    pale = Image.new("RGBA", cur.size, (0, 0, 0, 0))
    pale.paste(Image.new("RGBA", cur.size, (253, 251, 239, 255)), (0, 0), halo)
    pale.alpha_composite(cur)
    pale.save(os.path.join(OUT, "link-cursor-pale.png"))
    print("  link-cursor.png %dx%d  <- r%dc%d"
          % ((CURSOR_W, CURSOR_H) + CURSOR_AT))

    with io.open("icon-index.json", "w", encoding="utf-8") as fh:
        fh.write(json.dumps(index, indent=1, sort_keys=True) + "\n")
    print("%d icons" % len(index))


if __name__ == "__main__":
    main()
