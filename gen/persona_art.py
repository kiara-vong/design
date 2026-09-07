# -*- coding: utf-8 -*-
"""Artwork for the Persona Homepage case study cover.

The captures on the case-study page show what the two defaults look like. What
they cannot show is the thing the project is actually about, which is that they
are the SAME page: same widget catalog, same page, different opening order. A
screenshot of one ordering is a screenshot of a homepage; two of them side by side
with the blocks joined up is the argument.

So this is drawn, and drawn as a diagram rather than as a fake screen. Colour
marks which widget, and the links across the middle are the same five widgets
finding their new rank. Being visibly a diagram is the point -- a convincing
mockup sitting next to four real screenshots would be the one image on the page a
reader could not tell from evidence.

The home-page thumbnail is NOT here. It lives in gen/work_cards.py with the other
three, because it animates and the animation has to travel inside the file.
"""
import io
from gen.uikit import (rect, bar, text, save, W, H, INK, MUT, LINE, PAPER, WASH,
                       ACCENT, BLUE)

FW, FH = 799, 391      # .cs-media

# Five colours that stay five colours at hero size. ACCENT and GREEN are two
# greens a reader cannot tell apart across a metre of white, and telling them
# apart is the entire job the colour is doing here.
VIOLET, AMBER, RUST = "#8460C6", "#E8B84B", "#B4552F"

# The five widgets that actually exist on both defaults, in the order the leader
# page opens with. Colour marks WHICH widget, so the eye can follow one across
# and watch it move rather than reading two lists.
BLOCKS = [("Maturity score", ACCENT), ("Score trend", BLUE),
          ("Governance", RUST), ("Recent notices", VIOLET),
          ("Cloud cost", AMBER)]

# Two, not three, and not five. The case study explains why; the picture should
# not quietly disagree with it.
PERSONAS = [("Division lead", [0, 1, 2, 3, 4]),
            ("Application owner", [3, 4, 0, 2, 1])]


def panel(x, y, w, h, name, order, scale=1.0):
    """One persona's homepage, and where each of its blocks ended up.

    Returns (svg, {block index: vertical centre}) so the caller can join the two
    panels up. Working the positions out twice, once to draw and once to link, is
    how a diagram ends up with lines that nearly point at things.
    """
    o = [rect(x, y, w, h, PAPER, 10, LINE, 1.5),
         rect(x, y, w, 26 * scale, WASH, 10),
         rect(x, y + 16 * scale, w, 10 * scale, WASH)]
    o.append(text(x + 12, y + 18 * scale, name, 11 * scale, INK,
                  "'Inter',sans-serif", 700))
    # The scope chip that decides the ordering, drawn as a chip rather than a
    # name, because the page infers the persona from scope rather than a title.
    o.append(rect(x + w - 54 * scale, y + 7 * scale, 44 * scale, 13 * scale,
                  MUT, 7 * scale, op=.22))
    mid = {}
    yy = y + 36 * scale
    for rank, idx in enumerate(order):
        label, col = BLOCKS[idx]
        # The first block is tallest: rank IS the hierarchy, so the panel has to
        # show weight changing, not just sequence.
        bh = (46 - rank * 5) * scale
        o.append(rect(x + 10 * scale, yy, w - 20 * scale, bh, col, 6, op=.16))
        o.append(rect(x + 10 * scale, yy, 3.5 * scale, bh, col, 2))
        o.append(text(x + 20 * scale, yy + 12 * scale, label, 9 * scale, col,
                      "'Inter',sans-serif", 700))
        if bh > 22 * scale:
            o.append(bar(x + 20 * scale, yy + 18 * scale, (w - 56) * scale,
                         5 * scale, LINE))
        mid[idx] = yy + bh / 2.0
        yy += bh + 6 * scale
    return "".join(o), mid


def link(x0, y0, x1, y1, col):
    """A flat S-curve from one panel's block to the same block in the other."""
    dx = (x1 - x0) * 0.55
    return ('<path d="M%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f" stroke="%s" '
            'stroke-width="1.6" fill="none" opacity=".5"/>'
            % (x0, y0, x0 + dx, y0, x1 - dx, y1, x1, y1, col))


def fig_reorder():
    # No caption across the top. This is the cover of a page whose kicker,
    # headline and intro sit two centimetres below it saying the same thing with
    # more room to say it in, and a caption inside a cover image is a caption
    # competing with the headline above it.
    o = [rect(0, 0, FW, FH, PAPER)]
    PW, PH, PY = 262, 278, 56
    LX, RX = 46, FW - 46 - PW
    left, lmid = panel(LX, PY, PW, PH, PERSONAS[0][0], PERSONAS[0][1], scale=1.06)
    right, rmid = panel(RX, PY, PW, PH, PERSONAS[1][0], PERSONAS[1][1], scale=1.06)
    # Links first, so the panels sit on top of where the curves meet them.
    for idx, (_, col) in enumerate(BLOCKS):
        o.append(link(LX + PW, lmid[idx], RX, rmid[idx], col))
    o.append(left)
    o.append(right)
    return "".join(o)


def field():
    """The card's ground wash, matching the other three cards' treatment."""
    # The flat field this used to draw is gone: the four work cards sit on
    # paintings now, cut by gen/card_fields.py.
    return None


save("cs-persona-reorder", fig_reorder(), FW, FH)
field()
print("persona artwork written")
