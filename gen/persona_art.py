# -*- coding: utf-8 -*-
"""Artwork for the Persona Homepage card and case study.

This is the one project with nothing to screenshot: it has not shipped. So it is
drawn, and drawn as a DIAGRAM rather than as a fake screen -- three copies of the
same page with the same blocks in a different order, which is the whole idea of
the feature and is not something a single screenshot could show anyway.

Being visibly a diagram is the point. A convincing mockup of an unshipped product
sitting next to three real screenshots would be the one dishonest image on the
site.
"""
import io
from gen.uikit import rect, bar, text, save, W, H, INK, MUT, LINE, PAPER, WASH, ACCENT, BLUE, GREEN

HW, HH = 799, 307      # .cs-hero
FW, FH = 799, 391      # .cs-media

# Each persona gets the same five blocks in a different order and at different
# weights. Colour marks WHICH block, so the eye can follow one across the three
# panels and see it move.
BLOCKS = [("Tasks due", ACCENT), ("What I own", BLUE), ("Recent activity", GREEN),
          ("Team view", "#8460C6"), ("Getting started", "#E8B84B")]
PERSONAS = [("Operator", [0, 1, 2, 3, 4]),
            ("Owner", [1, 3, 0, 2, 4]),
            ("Newcomer", [4, 0, 1, 2, 3])]


def panel(x, y, w, h, name, order, scale=1.0):
    """One persona's homepage: a title bar, then its blocks in its own order."""
    o = [rect(x, y, w, h, PAPER, 10, LINE, 1.5),
         rect(x, y, w, 26 * scale, WASH, 10),
         rect(x, y + 16 * scale, w, 10 * scale, WASH)]
    o.append(text(x + 12, y + 18 * scale, name, 11 * scale, INK,
                  "'Clover',sans-serif", 700))
    # A persona switcher, with this one selected.
    o.append(rect(x + w - 54 * scale, y + 7 * scale, 44 * scale, 13 * scale,
                  MUT, 7 * scale, op=.22))
    yy = y + 36 * scale
    for rank, idx in enumerate(order):
        label, col = BLOCKS[idx]
        # The first block is tallest: rank IS the hierarchy, so the panel has to
        # show weight changing, not just sequence.
        bh = (34 - rank * 4) * scale
        o.append(rect(x + 10 * scale, yy, w - 20 * scale, bh, col, 6, op=.16))
        o.append(rect(x + 10 * scale, yy, 3.5 * scale, bh, col, 2))
        o.append(text(x + 20 * scale, yy + 12 * scale, label, 9 * scale, col,
                      "'Clover',sans-serif", 700))
        if bh > 22 * scale:
            o.append(bar(x + 20 * scale, yy + 18 * scale, (w - 56) * scale,
                         5 * scale, LINE))
        yy += bh + 6 * scale
    return "".join(o)


def fig_reorder():
    o = [rect(0, 0, FW, FH, PAPER)]
    # No caption across the top. This is the cover of a page whose kicker,
    # headline and intro sit two centimetres below it saying the same thing with
    # more room to say it in, and a caption inside a cover image is a caption
    # competing with the headline above it.
    for i, (name, order) in enumerate(PERSONAS):
        o.append(panel(28 + i * 254, 84, 224, 252, name, order, scale=1.02))
    return "".join(o)


def field():
    """The card's ground wash, matching the other three cards' treatment."""
    body = ('<defs><linearGradient id="g" x1="0" y1="0" x2=".3" y2="1">'
            '<stop offset="0" stop-color="#EFECFF"/>'
            '<stop offset="1" stop-color="#DED9F7"/></linearGradient>'
            '<radialGradient id="v" cx=".5" cy=".42" r=".78">'
            '<stop offset=".55" stop-color="#000" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#000" stop-opacity=".13"/></radialGradient></defs>'
            '<rect width="529" height="304" fill="url(#g)"/>')
    for i in range(9):
        for j in range(5):
            body += ('<circle cx="%.0f" cy="%.0f" r="1.8" fill="#8460C6" '
                     'opacity=".22"/>' % (34 + i * 58, 30 + j * 62))
    body += '<rect width="529" height="304" fill="url(#v)"/>'
    # The flat field this used to draw is gone: the four work cards sit on
    # paintings now, cut by gen/card_fields.py.


def card_shot():
    """The home-page thumbnail, authored in the shared 1200x700 cast."""
    o = [rect(0, 0, W, H, "#EFECFF")]
    o.append(text(40, 52, "ONE PAGE, THREE ORDERINGS", 17, "#8460C6",
                  "'Thistle',monospace", 500))
    for i, (name, order) in enumerate(PERSONAS):
        o.append(panel(40 + i * 380, 128, 340, 452, name, order, scale=1.62))
    save("shot-persona", "".join(o), W, H)


save("cs-persona-reorder", fig_reorder(), FW, FH)
field()
card_shot()
print("persona artwork written")
