# -*- coding: utf-8 -*-
"""Cut the hand-drawn flower and cat icons out of one sheet, and build the footer
strips and the link cursor from them.

The sheet arrives with real transparency now, so the cut is the file's own alpha and
nothing more. That is worth saying plainly, because what used to be here was three
hundred lines of keying: the first sheet had every sprite sitting on a soft glow over
a colour wash, and separating a cream petal from a cream glow is not possible with
any filter. Threshold sweeps found no knee, narrowing the blur radius took the petals
with the glow, and a soft alpha ramp made the petals ghostly, because their texture
energy IS the glow's energy. The fix was never going to be a better filter. It was a
better export, and this is it.

What remains is the one thing alpha alone does not solve. Keying only sets alpha, so
a sprite's transparent margin still carries whatever colour was under it, and every
resize -- the strip assembly here, then the browser scaling 240 into 120 -- averages
that back in along the edges as a fringe. bleed() walks the drawing's own colour
outward into that margin so a resample finds the same colour on both sides of an edge
and has nothing foreign to mix.

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

# Segmentation. Components are found on a downsampled alpha: fine enough to keep
# neighbouring sprites apart, coarse enough to be quick. ALPHA_TH is what counts as
# opaque, above the file's own soft edges.
K, ALPHA_TH, MIN_BLOB = 4, 40, 120

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
    "foot-art":      [(1, 3), (4, 3), (1, 6)],   # pink tulips, the calico, purple
    "foot-about":    [(1, 4), (4, 4), (3, 4)],   # forget-me-nots, Goose, lily of the valley
    "foot-work":     [(3, 1), (3, 6), (3, 7)],   # sprig, daisies, bow: foliage only
}

# The link cursor. Third row, second item.
CURSOR_AT = (3, 2)
CURSOR_W, CURSOR_H = 24, 32



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


# NOTE ON THE SPLIT SPRITE. The pink cosmos in row two has a flower head drawn clear
# of its own stem, so alpha finds it as two components and row two comes back with
# seven entries instead of six. Everything after it in that row shifts by one; rows
# one, three and four are unaffected.
#
# Merging by proximity was tried and cannot work: row three's small sprites sit as
# close to each other as the cosmos's two pieces do, so any gap wide enough to rejoin
# the flower also welds the sprig to the clover. The trios below simply avoid that
# one sprite, which costs nothing since there are twenty-three others.


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


def cut(im, box, pad=6):
    """One sprite, carrying the sheet's own alpha."""
    W, H = im.size
    crop = im.crop((max(0, box[0] - pad), max(0, box[1] - pad),
                    min(W, box[2] + pad), min(H, box[3] + pad)))
    return crop.crop(crop.getbbox() or (0, 0) + crop.size)


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
    im = Image.open(SRC).convert("RGBA")
    W, H = im.size
    sm = im.getchannel("A").resize((W // K, H // K), Image.BOX)
    w, h = sm.size
    found = blobs(bytearray(1 if v > ALPHA_TH else 0 for v in sm.getdata()), w, h)
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
