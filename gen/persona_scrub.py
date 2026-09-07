# -*- coding: utf-8 -*-
"""Neutralise the internal identifiers in the persona-homepage captures.

The four screenshots are of a working demo, and the demo is seeded with the real
thing: a division name, an application identifier, and a colleague's first name in
the greeting. None of that is what the case study is about, and a portfolio is a
public document, so the strings come out before the plates are built.

They are repainted rather than blurred or boxed out. A blur says "something was
here" and invites the reader to wonder what; a plausible placeholder in the same
type says what every other value on the screen says, which is that this is demo
data. The replacements are the same length as what they replace wherever a pill
has to keep its width.

Two details make the repaint invisible rather than obvious:

  - the fill is COPIED from a clean strip of the same background rather than
    flooded with a flat colour, because these cards are painted with a faint dot
    texture and a flat patch reads as a sticker. The offset to copy from is chosen
    by matching against the non-ink pixels of the row being replaced, so the dots
    line up instead of being merely the right colour;
  - the size and colour are measured off the ink that is being removed, not typed.

Everything else in the captures -- the widget names, the numbers, the dates -- is
the demo's own invented data and stays as it is.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SRC = os.path.join("assets", "tile", "_src", "_persona")
OUT = os.path.join("assets", "tile", "_src")

LATO = "/usr/share/fonts/truetype/lato/Lato-%s.ttf"
FONTS = {"regular": LATO % "Regular", "bold": LATO % "Bold",
         "semi": LATO % "Semibold", "black": LATO % "Black"}

# (search rectangle, replacement, weight, keep-width?)
# The rectangle is generous: the ink inside it is found, measured and replaced.
PATCHES = {
    "persona-home-leader": [
        ((165, 40, 700, 125), "Welcome back!", "black", False),
        ((525, 188, 1135, 238), "Cloud Platform Engineering & Operations (CPEO)",
         "bold", True),
        ((1180, 198, 1245, 230), "APP", "bold", True),
        ((252, 446, 860, 482), "Division: Cloud Platform Engineering & Oper…",
         "regular", True),
        ((1046, 523, 1640, 560), "Division: Cloud Platform Engineering & Op…",
         "regular", True),
        ((1836, 446, 2450, 482), "Division: Cloud Platform Engineering & Oper…",
         "regular", True),
    ],
    "persona-home-edit": [
        ((165, 40, 700, 125), "Welcome back!", "black", False),
        ((730, 198, 1030, 232), "APPCLOUDMATURITY", "bold", True),
        ((645, 198, 700, 232), "APP", "bold", True),
        ((252, 446, 560, 482), "App: APPCLOUDMATURITY", "regular", True),
        ((1046, 523, 1355, 560), "App: APPCLOUDMATURITY", "regular", True),
        ((1836, 440, 2145, 478), "App: APPCLOUDMATURITY", "regular", True),
    ],
    "persona-home-contributor": [
        ((252, 180, 560, 218), "App: APPCLOUDMATURITY", "regular", True),
        ((252, 878, 560, 916), "App: APPCLOUDMATURITY", "regular", True),
    ],
    "persona-catalog": [
        ((252, 300, 560, 340), "App: APPCLOUDMATURITY", "regular", True),
    ],
}


def bg_colour(a):
    """The most common colour in a patch, as the background."""
    q = (a.astype(np.int64) // 8).reshape(-1, 3)
    key = q[:, 0] * 65536 + q[:, 1] * 256 + q[:, 2]
    vals, counts = np.unique(key, return_counts=True)
    k = vals[counts.argmax()]
    m = (key == k)
    return a.reshape(-1, 3)[m].mean(axis=0)


def find_ink(a, bg, tol=40):
    d = np.abs(a.astype(int) - bg).sum(axis=2)
    return d > tol


def patch_source(arr, x0, y0, x1, y1, ink):
    """The vertical offset whose clean strip best matches the row's own texture.

    Chosen against the pixels that are NOT ink, so a candidate is scored on the
    background it would have to blend into rather than on the text it is covering.
    """
    h = y1 - y0
    best, bestd = None, 1e18
    keep = ~ink
    if keep.sum() < 20:
        keep = np.ones_like(ink)
    for d in range(6, 140):
        if y0 - d < 0:
            break
        cand = arr[y0 - d:y1 - d, x0:x1].astype(int)
        cur = arr[y0:y1, x0:x1].astype(int)
        err = (np.abs(cand - cur).sum(axis=2) * keep).sum() / max(keep.sum(), 1)
        if err < bestd:
            bestd, best = err, d
    return best


def fit_font(text, weight, target_h, target_w=None):
    """Size whose cap-to-baseline ink matches what is being replaced."""
    lo, hi = 6, 120
    best = None
    for size in range(lo, hi):
        f = ImageFont.truetype(FONTS[weight], size)
        box = f.getbbox(text)
        h = box[3] - box[1]
        if h > target_h:
            break
        best = (size, f, box)
    return best


def run(name, patches, verbose=True):
    im = Image.open(os.path.join(SRC, name + ".png")).convert("RGB")
    arr = np.array(im)
    dr = ImageDraw.Draw(im)
    for (sx0, sy0, sx1, sy1), new, weight, keep_w in patches:
        sub = arr[sy0:sy1, sx0:sx1]
        bg = bg_colour(sub)
        ink = find_ink(sub, bg)
        ys = np.where(ink.any(axis=1))[0]
        xs = np.where(ink.any(axis=0))[0]
        if len(ys) == 0:
            print("  !! no ink in", name, (sx0, sy0, sx1, sy1))
            continue
        x0, y0 = sx0 + xs.min(), sy0 + ys.min()
        x1, y1 = sx0 + xs.max() + 1, sy0 + ys.max() + 1
        col = arr[sy0:sy1, sx0:sx1][ink]
        # the ink's own colour: the pixels furthest from the background
        d = np.abs(col.astype(int) - bg).sum(axis=1)
        colour = tuple(int(v) for v in col[d >= np.percentile(d, 70)].mean(axis=0))
        if verbose:
            print("  %-26s ink %4d,%4d %4dx%-4d bg %s ink %s"
                  % (new[:24], x0, y0, x1 - x0, y1 - y0,
                     tuple(int(v) for v in bg), colour))
        # cover, with a strip of the same background from above
        pad = 3
        cy0, cy1 = max(0, y0 - pad), y1 + pad
        cx0, cx1 = max(0, x0 - pad), x1 + pad
        off = patch_source(arr, cx0, cy0, cx1, cy1,
                           find_ink(arr[cy0:cy1, cx0:cx1], bg))
        im.paste(Image.fromarray(arr[cy0 - off:cy1 - off, cx0:cx1]), (cx0, cy0))
        size, f, box = fit_font(new, weight, y1 - y0)
        dr.text((x0 - box[0], y0 - box[1]), new, font=f, fill=colour)
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    im.save(os.path.join(OUT, name + ".png"))
    print("  wrote", name)


if __name__ == "__main__":
    for n, p in PATCHES.items():
        print(n)
        run(n, p)
