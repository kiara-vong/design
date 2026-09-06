# -*- coding: utf-8 -*-
"""Find browser chrome baked into a capture.

The captures were taken in a real browser, and a real browser draws a scrollbar.
Where the page scrolled, that scrollbar is in the file: a narrow, near-uniform,
grey band welded to the right edge or the bottom one, sitting on top of whatever
the capture was actually of.

It is easy to miss by eye. Several of these are on dark grounds where the track
reads as a border, and at least one site draws its own scrollbar in its own accent
colour, which looks deliberate until you notice it is the same 15px on every
capture from that site.

Detecting it by sampling one background point does not work -- it false-positives
on any capture whose content happens to reach the edge, and false-negatives on the
dark ones. So this compares each edge band against the column (or row) just inside
it: a scrollbar is flat ALONG its length and different ACROSS it, and content that
merely reaches the edge is neither.

Reports candidates. It does not crop anything: an in-page scrollbar inside a modal
is a real part of that interface and cropping it would be a lie about the product.
Look at every hit before acting on it.
"""
import os
import sys

from PIL import Image

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
BAND = 20          # how far in from the edge to look
FLAT = 10          # a scrollbar varies less than this along its length
DIFF = 18          # ...and more than this against the content beside it


def col(im, x, ys):
    return [im.getpixel((x, y)) for y in ys]


def row(im, y, xs):
    return [im.getpixel((x, y)) for x in xs]


def spread(px):
    if not px:
        return 0
    return max(max(c) - min(c) for c in zip(*px))


def delta(a, b):
    return max(abs(sum(x) / 3.0 - sum(y) / 3.0) for x, y in zip(a, b))


def check(path):
    try:
        im = Image.open(path).convert("RGB")
    except Exception as e:
        return ["unreadable: %s" % e]
    w, h = im.size
    if w < 80 or h < 80:
        return []
    hits = []
    ys = list(range(int(h * .15), int(h * .85), max(1, h // 40)))
    xs = list(range(int(w * .15), int(w * .85), max(1, w // 40)))

    for d in range(2, BAND):
        edge, inside = col(im, w - d, ys), col(im, w - d - BAND, ys)
        if spread(edge) < FLAT and delta(edge, inside) > DIFF:
            hits.append("right edge: flat band at x=%d (%dpx in)" % (w - d, d))
            break
    for d in range(2, BAND):
        edge, inside = row(im, h - d, xs), row(im, h - d - BAND, xs)
        if spread(edge) < FLAT and delta(edge, inside) > DIFF:
            hits.append("bottom edge: flat band at y=%d (%dpx in)" % (h - d, d))
            break
    return hits


def main():
    roots = [os.path.join(ROOT, "assets", "plate"),
             os.path.join(ROOT, "assets", "video"),
             os.path.join(ROOT, "assets", "tile", "_src")]
    n = flagged = 0
    for r in roots:
        if not os.path.isdir(r):
            continue
        print("\n== %s" % os.path.relpath(r, ROOT))
        for f in sorted(os.listdir(r)):
            if not f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                continue
            n += 1
            hits = check(os.path.join(r, f))
            if hits:
                flagged += 1
                print("  %-46s %s" % (f, "; ".join(hits)))
    print("\n%d files, %d flagged" % (n, flagged))


main()
