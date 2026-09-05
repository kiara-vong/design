# -*- coding: utf-8 -*-
"""Shared drawing vocabulary for every generated mockup on the site.

The original cards showed exported screenshots of shipped mobile product. These
are web tools, so the frame is a browser rather than a phone, and the artwork is
drawn rather than exported: there is no shipped UI to screenshot for the personal
work, and a real internal-tool screenshot could not be published anyway.

Everything is authored in one 1200x700 space so a card can scale a shot into its
529x304 window with a single transform, the way the original scaled its 1440x810
cast. Primitives below are deliberately blunt -- bars for text, rects for panels --
because at 44% scale any real glyph is sub-pixel mush, and suggesting text reads
cleaner than rendering it badly.
"""
import io, math, random

W, H = 1200, 700   # the canvas every full-window mockup is authored in
INK, MUT, LINE = "#423E3D", "#878676", "#E3E1CC"
PAPER, WASH = "#FFFFFF", "#F7F5EA"
ACCENT, GREEN, BLUE, VIOLET = "#5690AE", "#649F25", "#1F597B", "#8460C6"

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def rect(x, y, w, h, fill, r=0, stroke=None, sw=1, op=None):
    s = '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="%s"' % (x, y, w, h, r, fill)
    if stroke: s += ' stroke="%s" stroke-width="%g"' % (stroke, sw)
    if op is not None: s += ' opacity="%.2f"' % op
    return s + '/>'

def bar(x, y, w, h=9, fill=LINE, r=None):
    """A stand-in for a line of text."""
    return rect(x, y, w, h, fill, r if r is not None else h / 2.0)

def lines(x, y, widths, gap=17, h=9, fill=LINE):
    return "".join(bar(x, y + i * gap, w, h, fill) for i, w in enumerate(widths))

def text(x, y, s, size=15, fill=INK, fam="'JetBrains Mono',monospace", w=400, anchor="start"):
    return ('<text x="%.1f" y="%.1f" font-family="%s" font-size="%g" font-weight="%s" '
            'fill="%s" text-anchor="%s">%s</text>' % (x, y, fam, size, w, fill, anchor, esc(s)))

def chrome(title, body, tab_accent=ACCENT):
    """Browser window filling the whole 1200x700 frame."""
    o = [rect(0, 0, W, H, PAPER, 16),
         rect(0, 0, W, 52, WASH, 16),
         rect(0, 36, W, 16, WASH),
         '<line x1="0" y1="52" x2="%d" y2="52" stroke="%s" stroke-width="1.5"/>' % (W, LINE)]
    for i, c in enumerate(("#E6685C", "#E8B84B", "#7DC26B")):
        o.append('<circle cx="%d" cy="26" r="6.5" fill="%s"/>' % (28 + i * 22, c))
    o.append(rect(108, 13, 430, 26, PAPER, 13, LINE))
    o.append('<circle cx="126" cy="26" r="5" fill="none" stroke="%s" stroke-width="1.6"/>' % MUT)
    o.append(text(140, 31, title, 13, MUT))
    o.append(rect(W - 96, 13, 62, 26, tab_accent, 13, op=.16))
    return "".join(o) + body

def save(name, body, w=W, h=H):
    # Routed by name, not by argument. Every caller already names its file for what
    # it is -- shot-*, field-* and cs-* -- and those prefixes are exactly the folder
    # split, so asking each call site to repeat it would only be a chance to disagree.
    folder = "case" if name.startswith("cs-") else "cards"
    io.open("assets/%s/%s.svg" % (folder, name), "w", encoding="utf-8").write(
        '<svg width="%d" height="%d" viewBox="0 0 %d %d" fill="none" '
        'xmlns="http://www.w3.org/2000/svg">%s</svg>\n' % (w, h, w, h, body))

def sidebar(x=0, y=52, w=196, items=6, active=1, accent=ACCENT):
    o = [rect(x, y, w, H - y, WASH),
         '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.5"/>' % (x + w, y, x + w, H, LINE)]
    o.append('<circle cx="%d" cy="%d" r="11" fill="%s"/>' % (x + 30, y + 34, accent))
    o.append(bar(x + 50, y + 29, 74, 10, MUT))
    for i in range(items):
        yy = y + 74 + i * 40
        if i == active:
            o.append(rect(x + 12, yy - 4, w - 24, 32, accent, 8, op=.13))
            o.append(rect(x + 12, yy - 4, 3, 32, accent, 1.5))
        o.append(rect(x + 26, yy + 5, 13, 13, accent if i == active else MUT, 3,
                      op=1 if i == active else .5))
        o.append(bar(x + 50, yy + 7, 62 + (i * 13) % 46, 10,
                     accent if i == active else LINE))
    return "".join(o)

