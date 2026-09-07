# -*- coding: utf-8 -*-
"""Neutralise the internal identifiers in the persona-homepage captures.

The four screenshots are of a working demo, and the demo is seeded with the real
thing: a division name, an application identifier, and a first name in the
greeting. None of that is what the case study is about, and a portfolio is a
public document, so the strings come out before the plates are built. The
originals stay in _src/_persona, outside the folder gen/plates.py reads, so this
is reversible and nothing unscrubbed is ever delivered.

They are repainted rather than blurred or boxed out. A blur says "something was
here" and invites the reader to wonder what; a plausible placeholder in the same
type says what every other value on these screens says, which is that this is demo
data. Where a value sits in a pill sized to it, the replacement is chosen to be
the same length, so the pill does not have to be redrawn.

Three details make the repaint invisible rather than obvious:

  - the fill is COPIED from a clean strip of the same background rather than
    flooded with a flat colour, because these cards carry a faint dot texture and
    a flat patch reads as a sticker. The offset it is copied from is chosen by
    matching against the NON-ink pixels of the row being replaced, so the dots
    line up rather than merely being the right colour;
  - the type size is fitted against the ORIGINAL string's own metrics, not against
    the replacement's. Fitting to the replacement makes every patch whose text has
    no descender come out a size too large, which is the tell;
  - short labels are letterspaced to the width they are replacing, because these
    are tracked-out small caps and a tight three letters beside an untouched
    neighbour is visible even when nobody knows what changed.

Everything else in the captures -- the widget names, the numbers, the dates -- is
the demo's own invented data and stays as it is.
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

SRC = os.path.join("assets", "tile", "_src", "_persona")
OUT = os.path.join("assets", "tile", "_src")

LATO = "/usr/share/fonts/truetype/lato/Lato-%s.ttf"
FONTS = {"regular": "Regular", "bold": "Bold", "semi": "Semibold",
         "black": "Black"}

DIV_OLD = "Cloud Operations Resilience Engineering (CORE)"
DIV_NEW = "Cloud Platform Engineering & Operations (CPEO)"
SCOPE_NEW = "Division: Cloud Platform Engineering & Operations"
APP_OLD = "ASV: ASVCLOUDMATURITY"
APP_NEW = "App: APPCLOUDMATURITY"

# (search rect, old string, new string, weight, letterspace-to-width)
# The rect only has to CONTAIN the run and nothing else; the ink inside it is
# found, measured and replaced. Keeping the widget icons out of it is the reason
# the left edges are where they are.
PATCHES = {
    "persona-home-leader": [
        ((165, 45, 700, 125), "Welcome, Michelle!", "Welcome back!", "black", 0),
        ((535, 200, 1122, 232), DIV_OLD, DIV_NEW, "bold", 0),
        ((1214, 200, 1266, 232), "ASV", "APP", "bold", 1),
        ((262, 448, 855, 478),
         "Division: Cloud Operations Resilience Engineering (CO",
         SCOPE_NEW, "regular", 0),
        ((1058, 525, 1640, 558),
         "Division: Cloud Operations Resilience Engineering (C",
         SCOPE_NEW, "regular", 0),
        ((1848, 448, 2450, 478),
         "Division: Cloud Operations Resilience Engineering (CO",
         SCOPE_NEW, "regular", 0),
    ],
    "persona-home-edit": [
        ((165, 45, 700, 125), "Welcome, Michelle!", "Welcome back!", "black", 0),
        ((730, 200, 1006, 232), "ASVCLOUDMATURITY", "APPCLOUDMATURITY", "bold", 0),
        ((677, 200, 729, 232), "ASV", "APP", "bold", 1),
        ((262, 448, 620, 478), APP_OLD, APP_NEW, "regular", 0),
        ((1058, 525, 1420, 558), APP_OLD, APP_NEW, "regular", 0),
        ((1848, 442, 2210, 476), APP_OLD, APP_NEW, "regular", 0),
    ],
    "persona-home-contributor": [
        ((262, 182, 620, 216), APP_OLD, APP_NEW, "regular", 0),
        ((262, 880, 620, 914), APP_OLD, APP_NEW, "regular", 0),
    ],
    "persona-widget-jobs": [
        ((262, 302, 620, 340), APP_OLD, APP_NEW, "regular", 0),
    ],
}


def bg_colour(a):
    """The most common colour in a patch, taken as its background."""
    q = (a.astype(np.int64) // 8).reshape(-1, 3)
    key = q[:, 0] * 65536 + q[:, 1] * 256 + q[:, 2]
    vals, counts = np.unique(key, return_counts=True)
    m = (key == vals[counts.argmax()])
    return a.reshape(-1, 3)[m].mean(axis=0)


def find_ink(a, bg, tol=40):
    return np.abs(a.astype(int) - bg).sum(axis=2) > tol


def clean_patch(arr, x0, y0, x1, y1, ink, bg):
    """A rectangle of pure background to paste over the run being replaced.

    Flat grounds are simply flooded. Textured ones -- these cards carry a faint
    dot grid -- are covered with a strip lifted from ABOVE or BELOW, at whichever
    offset both contains no ink of its own and best matches the pixels of this row
    that are not ink. Skipping the no-ink test is how the first pass ended up
    pasting the tops of the very words it was covering back underneath them.
    """
    h, w = y1 - y0, x1 - x0
    keep = ~ink
    if keep.sum() < 20:
        keep = np.ones_like(ink)
    cur = arr[y0:y1, x0:x1].astype(int)
    # Flat ground: the background is one colour, so say so and stop.
    clean = cur[keep]
    if clean.std(axis=0).max() < 4.0:
        return Image.new("RGB", (w, h), tuple(int(v) for v in bg))
    best, err0 = None, 1e18
    for d in list(range(6, 200)) + [-d for d in range(6, 200)]:
        ty0 = y0 - d
        if ty0 < 0 or ty0 + h > arr.shape[0]:
            continue
        cand = arr[ty0:ty0 + h, x0:x1].astype(int)
        # a source strip that is itself inked is not background
        if find_ink(cand, bg, 60).mean() > 0.02:
            continue
        err = (np.abs(cand - cur).sum(axis=2) * keep).sum() / max(keep.sum(), 1)
        if err < err0:
            err0, best = err, Image.fromarray(arr[ty0:ty0 + h, x0:x1])
    if best is None:
        return Image.new("RGB", (w, h), tuple(int(v) for v in bg))
    return best


def fit(old, weight, ink_h):
    """The size at which the ORIGINAL string's ink is as tall as what was found."""
    chosen = None
    for size in range(6, 140):
        f = ImageFont.truetype(LATO % FONTS[weight], size)
        b = f.getbbox(old)
        if b[3] - b[1] > ink_h:
            break
        chosen = (size, f, b)
    return chosen


def draw_spread(dr, xy, text, font, fill, width):
    """Draw `text` letterspaced to fill `width` exactly."""
    x, y = xy
    if len(text) < 2:
        dr.text((x, y), text, font=font, fill=fill)
        return
    solid = sum(font.getlength(c) for c in text)
    gap = (width - solid) / float(len(text) - 1)
    for c in text:
        dr.text((x, y), c, font=font, fill=fill)
        x += font.getlength(c) + gap


def run(name, patches):
    im = Image.open(os.path.join(SRC, name + ".png")).convert("RGB")
    arr = np.array(im)
    dr = ImageDraw.Draw(im)
    for (sx0, sy0, sx1, sy1), old, new, weight, spread in patches:
        sub = arr[sy0:sy1, sx0:sx1]
        bg = bg_colour(sub)
        ink = find_ink(sub, bg)
        ys, xs = np.where(ink.any(axis=1))[0], np.where(ink.any(axis=0))[0]
        if not len(ys):
            raise SystemExit("  no ink in %s %s" % (name, (sx0, sy0, sx1, sy1)))
        x0, y0 = sx0 + xs.min(), sy0 + ys.min()
        x1, y1 = sx0 + xs.max() + 1, sy0 + ys.max() + 1
        pix = sub[ink]
        d = np.abs(pix.astype(int) - bg).sum(axis=1)
        colour = tuple(int(v) for v in pix[d >= np.percentile(d, 70)].mean(axis=0))

        pad = 3
        cy0, cy1 = max(0, y0 - pad), y1 + pad
        cx0, cx1 = max(0, x0 - pad), x1 + pad
        im.paste(clean_patch(arr, cx0, cy0, cx1, cy1,
                             find_ink(arr[cy0:cy1, cx0:cx1], bg), bg), (cx0, cy0))

        size, f, b = fit(old, weight, y1 - y0)
        # Never wider than what it replaces: these runs sit in pills and cards
        # already sized to them, and the original is itself truncated to fit.
        # Lato is not the font on the screen and sets a little wider at the same
        # cap height, so the first remedy is a point or two smaller rather than a
        # word cut off -- a truncated identifier looks like a bug, and a line set
        # 6% small next to type nobody has the original of does not.
        room = x1 - x0
        while size > 8 and f.getlength(new) > room and \
                f.getlength(new) < room * 1.35:
            size -= 1
            f = ImageFont.truetype(LATO % FONTS[weight], size)
            b = f.getbbox(old)
        txt = new
        while len(txt) > 4 and f.getlength(txt) > room:
            txt = txt[:-1].rstrip(" ,&")
        if txt != new:
            txt += "…"
        if spread:
            draw_spread(dr, (x0 - b[0], y0 - b[1]), txt, f, colour, room)
        else:
            dr.text((x0 - b[0], y0 - b[1]), txt, font=f, fill=colour)
        print("  %-50s %dpx at %d,%d" % (txt, size, x0, y0))
    im.save(os.path.join(OUT, name + ".png"))


def main():
    if not os.path.isdir(SRC):
        print("  no %s; nothing to scrub" % SRC)
        return
    for n in sorted(PATCHES):
        print(n)
        run(n, PATCHES[n])
    print("%d captures scrubbed" % len(PATCHES))


if __name__ == "__main__":
    main()
