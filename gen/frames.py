# -*- coding: utf-8 -*-
"""Generates the perforated ticket/postcard frames.

These are the one part of the original layout that is pure geometry: a rounded
panel whose edges are cut into a triangular sawtooth, like a torn raffle stub.
The originals were 12KB Figma exports with every tooth written out as absolute
coordinates. Emitting them from the period and depth instead means the tooth
count re-derives itself whenever a panel changes size, which is what went wrong
the first time the card width moved and the teeth stopped meeting the corners.
"""
import io

def sawtooth(length, period, depth, flip=False):
    """Points for one edge, running 0..length along x with teeth in +y.

    The tooth count is rounded to a whole number and the period rescaled to fit,
    so an edge always begins and ends on a peak no matter what length it is
    handed. A fractional tooth at the corner is what reads as a mistake.
    """
    n = max(1, int(round(length / float(period))))
    step = length / float(n)
    d = -depth if flip else depth
    pts = []
    for i in range(n):
        x0 = i * step
        pts.append((x0 + step * 0.42, d))       # down into the valley
        pts.append((x0 + step * 0.58, d))       # flat valley floor
        pts.append((x0 + step, 0.0))            # back up to the peak
    return pts

# --dove-ivory, not --parchment. The ticket was filled with the exact colour of the
# page it sits on, which meant the only thing separating a ticket from the ground was
# its own 1px sawtooth outline: the body read as a hole rather than as a card. Ivory
# is the next surface up in the palette and is what every other raised element on the
# site uses.
def frame(w, h, period=23.7, depth=12.0, edges="tb", fill="#F5F2E5",
          stroke="#E3E1CC", sw=1.0, radius=0.0):
    """A panel of w x h with sawtooth on the named edges (t/r/b/l)."""
    d = ["M 0 0"]
    if "t" in edges:
        for x, y in sawtooth(w, period, depth):
            d.append("L %.2f %.2f" % (x, y))
    else:
        d.append("L %.2f 0" % w)
    if "r" in edges:
        for y, x in sawtooth(h, period, depth):
            d.append("L %.2f %.2f" % (w - x, y))
    else:
        d.append("L %.2f %.2f" % (w, h))
    if "b" in edges:
        for x, y in sawtooth(w, period, depth):
            d.append("L %.2f %.2f" % (w - x, h - y))
    else:
        d.append("L 0 %.2f" % h)
    if "l" in edges:
        for y, x in sawtooth(h, period, depth):
            d.append("L %.2f %.2f" % (x, h - y))
    d.append("Z")
    return ('<svg width="%g" height="%g" viewBox="0 0 %g %g" fill="none" '
            'xmlns="http://www.w3.org/2000/svg">\n'
            '<path d="%s" fill="%s" stroke="%s" stroke-width="%g" '
            'stroke-linejoin="round"/>\n</svg>\n'
            % (w, h, w, h, " ".join(d), fill, stroke, sw))

io.open("assets/ui/card-ticket.svg", "w", encoding="utf-8").write(
    frame(573, 628, period=23.7, depth=12.0, edges="tb"))
io.open("assets/hero/postcard-top.svg", "w", encoding="utf-8").write(
    frame(300, 644.5, period=12.4, depth=8.5, edges="tb"))
io.open("assets/hero/postcard-bottom.svg", "w", encoding="utf-8").write(
    frame(300, 122, period=12.4, depth=8.5, edges="t"))
print("frames written")

# Mobile variants. Same outline, but preserveAspectRatio="none" so the frame can
# be stretched to whatever height a phone's text block ends up needing. The teeth
# keep their real profile because they are stroked geometry, not a bitmap, and the
# desktop file is left alone: it is used as an <img> where letterboxing is correct.
def stretchy(src, dst):
    s = io.open(src, encoding="utf-8").read()
    s = s.replace('<svg ', '<svg preserveAspectRatio="none" ', 1)
    io.open(dst, "w", encoding="utf-8").write(s)

stretchy("assets/ui/card-ticket.svg", "assets/ui/card-ticket-mobile.svg")
stretchy("assets/ui/card-ticket.svg", "assets/ui/library-ticket-mobile.svg")
print("mobile frames written")
