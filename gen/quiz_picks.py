# -*- coding: utf-8 -*-
"""The quiz's answers, un-answered.

The capture is of a form that is already filled in, because that is the only
state worth photographing: an empty form is a picture of nothing. But the figure
argues that you answer it, and an argument that starts at its conclusion is not
an argument. So the six chosen answers have to be shown arriving.

Repainting them was the obvious approach and the wrong one. A pill's label is set
in the site's own type at the site's own size, and a redrawn label is a redrawn
label -- close is worse than absent, because the eye reads the difference as a
rendering fault rather than as a design.

So the labels are not redrawn. They are LIFTED. A selected pill is white type on
crimson, which means the type is already a clean alpha channel: how far a pixel
has travelled from the crimson toward white is exactly how much glyph is in it.
Pull that out, drop it onto an unselected pill drawn in the page's own three
colours, and the result is the same glyphs, the same hinting, the same kerning,
in the colour they would have had if nobody had clicked. Every colour here is
sampled from the capture; none is chosen.

Six of these go into one sprite, and the figure lays them over the answers they
hide. They start opaque and fade out one at a time, so the form fills itself in
and the state it ends in is the unmodified capture rather than anything built
here.
"""
import io
import json
import os

import numpy as np
from PIL import Image, ImageDraw

SRC = os.path.join("assets", "tile", "_src", "dorms-quiz-page.png")
OUT = os.path.join("assets", "plate", "dorms-quiz-blanks.webp")
IDX = "quiz-picks.json"

SS = 4                      # supersample for the pill's own edges
GAP = 4                     # air between sprite rows, so no row bleeds into the next

# A margin of page background around each blank, in capture pixels.
#
# Without it the blank is exactly the size of the pill it covers, which sounds
# right and is not. The capture is delivered at 2200px and drawn at 1280; the
# sprite is delivered at its own width and drawn at another; the two are resampled
# by different amounts and land a fraction of a pixel apart. What that fraction
# looks like is a crimson hairline around a white pill -- the answer showing
# through the thing that is meant to be hiding it, which reads as a rendering
# fault rather than as a form waiting to be filled in.
#
# So the blank over-covers, onto ground the same colour as the page. Three pixels
# is far more than the error and still less than a seventh of the gap between two
# pills, so nothing else is ever touched.
PAD = 3


def _pills(a):
    """The six crimson answers, as full pill rectangles.

    Found by colour and then re-measured against the page background, because the
    crimson run stops a couple of pixels inside the pill's real edge where the
    antialiasing turns. Two pixels is nothing until the blank laid over it is two
    pixels small on every side, and then it is a crimson outline around a white
    pill.
    """
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    m = (r > 120) & (r < 200) & (g < 55) & (b < 70)
    m[:400, :] = False                        # the site header's own crimson
    m[2100:, :] = False                       # the submit button and the footer
    ys = np.nonzero(m.any(axis=1))[0]
    bands, run = [], [ys[0]]
    for y in ys[1:]:
        if y - run[-1] > 12:
            bands.append((run[0], run[-1]))
            run = []
        run.append(y)
    bands.append((run[0], run[-1]))
    bands = [q for q in bands if q[1] - q[0] > 40]

    bg = a[10, 10]
    out = []
    for y0, y1 in bands:
        xs = np.nonzero(m[y0:y1 + 1, :].sum(axis=0) > 20)[0]
        cx0, cx1 = xs.min(), xs.max()
        d = np.abs(a[y0 - 6:y1 + 7, :] - bg).sum(axis=2) > 18
        cols = np.nonzero(d.sum(axis=0) > 3)[0]
        lo = cols[cols <= cx0].max() if (cols <= cx0).any() else cx0
        hi = cols[cols >= cx1].min() if (cols >= cx1).any() else cx1
        while lo - 1 in set(cols.tolist()):
            lo -= 1
        while hi + 1 in set(cols.tolist()):
            hi += 1
        rows = np.nonzero(d.sum(axis=1) > 3)[0] + y0 - 6
        out.append((int(lo), int(rows.min()), int(hi - lo + 1),
                    int(rows.max() - rows.min() + 1)))
    return out


def _blank(a, rect, page, fill, edge, ink, crimson):
    """One unselected pill, carrying the selected one's own glyphs, on a patch of
    page wide enough to cover the answer underneath it whole."""
    x, y, w, h = rect[0] + PAD, rect[1] + PAD, rect[2] - PAD * 2, rect[3] - PAD * 2
    crop = a[y:y + h, x:x + w].astype(float)

    # the pill's own shape, drawn clean rather than traced
    big = Image.new("L", (w * SS, h * SS), 0)
    ImageDraw.Draw(big).rounded_rectangle(
        [0, 0, w * SS - 1, h * SS - 1], radius=h * SS // 2, fill=255)
    shape = big.resize((w, h), Image.LANCZOS)

    pill = Image.new("RGB", (w, h), tuple(fill))
    d = ImageDraw.Draw(pill)
    # the border, drawn at the same supersample and composited, so it keeps the
    # hairline weight it has on the page instead of thickening to a whole pixel
    ring = Image.new("L", (w * SS, h * SS), 0)
    dr = ImageDraw.Draw(ring)
    dr.rounded_rectangle([0, 0, w * SS - 1, h * SS - 1],
                         radius=h * SS // 2, outline=255, width=SS * 2)
    pill.paste(Image.new("RGB", (w, h), tuple(edge)), (0, 0),
               ring.resize((w, h), Image.LANCZOS))

    # the glyphs, as the distance the pixel travelled from crimson toward white
    lo, hi = float(crimson[1]), 255.0
    alpha = np.clip((crop[:, :, 1] - lo) / (hi - lo), 0.0, 1.0)
    inner = np.array(shape.filter(__import__("PIL.ImageFilter",
                     fromlist=["x"]).MinFilter(5))) / 255.0
    alpha = (alpha * inner * 255.0).astype(np.uint8)
    pill.paste(Image.new("RGB", (w, h), tuple(ink)), (0, 0),
               Image.fromarray(alpha, "L"))

    out = Image.new("RGB", (w + PAD * 2, h + PAD * 2), tuple(page))
    out.paste(pill, (PAD, PAD), shape)
    return out


def main():
    im = Image.open(SRC).convert("RGB")
    a = np.array(im).astype(int)
    rects = [(x - PAD, y - PAD, w + PAD * 2, h + PAD * 2)
             for (x, y, w, h) in _pills(a)]

    bg = tuple(int(v) for v in a[10, 10])
    crimson = tuple(int(v) for v in a[rects[0][1] + rects[0][3] // 2,
                                     rects[0][0] + PAD + 4])
    # an unselected neighbour of the first answer, for the three colours a pill
    # has when nobody has clicked it
    x, y, w, h = rects[0]
    # Medians rather than single pixels: a pill is mostly fill with a minority of
    # dark type, so the median IS the fill, while one sample taken at the middle
    # is as likely to land on a glyph as not -- and it did, the first time.
    nb = a[y + 8:y + h - 8, x + w + 26:x + w + 26 + 60]
    fill = tuple(int(v) for v in np.median(nb.reshape(-1, 3), axis=0))
    # The border, found rather than sampled at a guessed point: walk down each
    # column of the neighbour until the page stops being the page. The first
    # thing you meet on the way down is always the top of the stroke, and never a
    # glyph, which sits well below it. A fixed offset gets this wrong near the
    # pill's rounded end, where the top of the stroke is not at the top.
    hits = []
    for cx in range(x + w + 26, x + w + 26 + 140):
        col = a[y - 6:y + h // 2, cx]
        d = np.nonzero(np.abs(col - np.array(bg)).sum(axis=1) > 18)[0]
        if len(d):
            hits.append(col[d[0]])
    edge = tuple(int(v) for v in np.median(np.array(hits), axis=0))
    ink = tuple(int(v) for v in np.percentile(nb.reshape(-1, 3), 1, axis=0))

    sw = max(r[2] for r in rects)
    row = max(r[3] for r in rects) + GAP
    sheet = Image.new("RGB", (sw, row * len(rects)), tuple(bg))
    for i, r in enumerate(rects):
        sheet.paste(_blank(a, r, bg, fill, edge, ink, crimson), (0, i * row))

    if not os.path.isdir(os.path.dirname(OUT)):
        os.makedirs(os.path.dirname(OUT))
    # Lossless: it is six pills of flat fill and hinted type, it is tiny
    # either way, and it is laid over the same type it replaces -- a
    # compression artefact here would read as a rendering fault.
    sheet.save(OUT, "WEBP", lossless=True, method=6)
    json.dump(dict(src_w=im.size[0], sprite_w=sw, row=row,
                   picks=[list(r) for r in rects]),
              io.open(IDX, "w", encoding="utf-8"), indent=1)
    print("quiz picks: %d answers, sheet %dx%d, bg %s fill %s edge %s"
          % (len(rects), sw, row * len(rects), bg, fill, edge))


if __name__ == "__main__":
    main()
