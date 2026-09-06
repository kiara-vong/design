# -*- coding: utf-8 -*-
"""Project covers, built as the thumbnail rather than beside it.

The cover at the top of a project page used to be the tile image itself, dropped
into a 799x307 box with object-fit:cover. The tiles are tall -- Stardew's is
776x1112 -- so cover threw away four fifths of every one of them and kept a band
from the middle: no title, no browser frame, no painted ground, just a stripe of
whatever happened to be halfway down the page. It did not look like the thumbnail
the reader had clicked, because it was not the same picture in any sense.

So this composes the cover the way index.html composes the thumbnail, from the
same three parts in the same order:

    a painted ground, cut from the same folder the hero and About grounds come from
    a browser window sitting on it, inset so a border of the painting shows
    the capture inside the window, from ITS TOP

That last part matters. The tile scrolls, and the frame a reader sees before they
click is its resting frame, which is the top of the capture. Starting the cover
anywhere else would make the two pictures disagree at the exact moment the reader
is checking whether they arrived where they meant to.

Written at 2x and delivered as WebP, like everything else that carries a
screenshot on this site.
"""
import io
import json
import os

from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.join("assets", "hero")
TILE = os.path.join("assets", "tile")

# .cs-hero, from case-study.css, at 2x.
W, H = 1598, 614

# The window's inset, as a fraction of the cover. Wider than the tile's because a
# 2.6:1 box can afford more ground at the sides than a 1.24:1 one can, and the
# painting is worth showing. It runs off the BOTTOM rather than sitting inside a
# margin, exactly as .tile-win does: a window with air under it reads as a card,
# and a window leaving the frame reads as a page that continues.
INSET_X, INSET_TOP = 0.062, 0.108

BAR = 46                      # chrome height at 2x, matching .tile-bar's 17px
RADIUS = 22
LIGHTS = ((0xE6, 0x68, 0x5C), (0xE8, 0xB8, 0x4B), (0x7D, 0xC2, 0x6B))
IVORY = (245, 242, 229)
STROKE = (227, 225, 204)
PARCH = (253, 251, 239)


def cover(im, w, h):
    """Fill w x h, anchored at the TOP -- the tile's resting frame."""
    sc = max(w / float(im.size[0]), h / float(im.size[1]))
    im = im.resize((max(1, int(round(im.size[0] * sc))),
                    max(1, int(round(im.size[1] * sc)))), Image.LANCZOS)
    x = (im.size[0] - w) // 2
    return im.crop((x, 0, x + w, h))


def build(slug, ground, shot):
    base = cover(Image.open(ground).convert("RGB"), W, H).convert("RGBA")

    x0 = int(round(W * INSET_X))
    y0 = int(round(H * INSET_TOP))
    ww, wh = W - x0 * 2, H - y0          # runs off the bottom edge

    win = Image.new("RGB", (ww, wh), IVORY)
    d = ImageDraw.Draw(win)

    # the chrome: three lights and an address strip, at .tile-bar's proportions
    d.line([(0, BAR), (ww, BAR)], fill=STROKE, width=2)
    r = int(BAR * .145)
    for i, c in enumerate(LIGHTS):
        cx, cy = int(BAR * (.41 + i * .53)) + r, BAR // 2
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
    bx0, bx1 = int(BAR * 2.23), ww - int(BAR * .59)
    by0, by1 = int(BAR * .26), int(BAR * .74)
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=(by1 - by0) // 2,
                        fill=PARCH, outline=STROKE, width=2)

    # the screen: the capture, from its top
    win.paste(cover(Image.open(shot).convert("RGB"), ww, wh - BAR - 2), (0, BAR + 2))

    # The mask has to be built as L. Drawing into RGBA and converting gives
    # luminance rather than alpha, which pastes the window semi-transparent and
    # lets the painting show straight through the screenshot.
    mask = Image.new("L", (ww, wh), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, ww - 1, wh + RADIUS],
                                           radius=RADIUS, fill=255)

    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        [x0 + 2, y0 + 10, x0 + ww + 2, y0 + wh + 10], radius=RADIUS,
        fill=(28, 24, 22, 52))
    base = Image.alpha_composite(base, shadow.filter(ImageFilter.GaussianBlur(16)))
    base.paste(win, (x0, y0), mask)

    out = base.convert("RGB")
    ImageDraw.Draw(out).rounded_rectangle(
        [x0, y0, x0 + ww - 1, y0 + wh + RADIUS], radius=RADIUS,
        outline=STROKE, width=2)

    dst = os.path.join(OUT, "cover-%s.webp" % slug)
    out.save(dst, "WEBP", quality=86, method=6)
    return dst, os.path.getsize(dst) / 1024.0


def main():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    idx = json.load(io.open("tile-index.json", encoding="utf-8"))
    print("project covers:")
    for slug, e in sorted(idx.items()):
        shot = os.path.join(TILE, slug + ".jpg")
        ground = os.path.join(TILE, e.get("ground") or "")
        if not (os.path.exists(shot) and os.path.exists(ground)):
            print("  skip %-9s (no capture or ground yet)" % slug)
            continue
        dst, kb = build(slug, ground, shot)
        print("  %-22s %dx%d %5dKB" % (os.path.basename(dst), W, H, kb))


if __name__ == "__main__":
    main()
