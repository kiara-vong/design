# -*- coding: utf-8 -*-
"""A drawn content layer for Dorms @ Brown, the one archive project with no capture.

The app needs a backend and a Firebase project to run, so there is nothing to
screenshot locally. It is recreated instead -- and recreated faithfully rather
than abstractly, because it sits next to five real captures and an obviously
diagrammatic tile would be the odd one out.

Everything drawn here is in the README: filter chips for room type, bathroom and
class year, a live search field, dorm cards carrying a photo, an average star
rating and a room-type line, and the quiz entry that narrows thirty dorms to a
shortlist. The photos are stand-in blocks in Brown's brick and stone tones, which
is the one thing that cannot be recovered from a description.

Emitted at the same 776 width as the captured tiles so it scrolls at the same rate
inside the page's window frame.
"""
import io
import math
import random

W, H = 776, 1180          # tall enough to scroll, like the captured pages

PAPER = "#FFFFFF"
WASH = "#F7F6F2"
INK = "#2B2A28"
MUT = "#8A867E"
LINE = "#E4E1D8"
BROWN = "#8C3A2E"         # the university's brick
SEAL = "#B8352C"
GOLD = "#E8B84B"
STONE = "#C9BEA8"
IVY = "#5E7A4A"
SLATE = "#8FA0AE"


def r(x, y, w, h, fill, rad=0, op=None):
    s = '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="%s"' % (
        x, y, w, h, rad, fill)
    if op is not None:
        s += ' opacity="%.2f"' % op
    return s + '/>'


def t(x, y, s, size=13, fill=INK, fam="sans", weight=400, anchor="start"):
    fams = {"sans": "'Diatype','Inter',system-ui,sans-serif",
            "serif": "'Mackinac','Fraunces',Georgia,serif",
            "mono": "'ApercuMono','JetBrains Mono',ui-monospace,monospace"}
    return ('<text x="%.1f" y="%.1f" font-family="%s" font-size="%g" font-weight="%s" '
            'fill="%s" text-anchor="%s">%s</text>'
            % (x, y, fams[fam], size, weight, fill, anchor,
               s.replace("&", "&amp;").replace("<", "&lt;")))


def stars(x, y, n, of=5, size=9):
    o = []
    for i in range(of):
        pts = []
        for k in range(10):
            ang = -math.pi / 2 + k * math.pi / 5
            rad = size if k % 2 == 0 else size * .44
            pts.append((x + i * (size * 2.6) + rad * math.cos(ang),
                        y + rad * math.sin(ang)))
        o.append('<polygon points="%s" fill="%s"/>'
                 % (" ".join("%.1f %.1f" % p for p in pts),
                    GOLD if i < n else LINE))
    return "".join(o)


o = [r(0, 0, W, H, WASH)]

# ---------------------------------------------------------------- header
o.append(r(0, 0, W, 66, BROWN))
o.append('<circle cx="36" cy="33" r="15" fill="%s"/>' % GOLD)
o.append(t(30, 38, "B", 17, BROWN, "serif", 700))
o.append(t(62, 39, "Dorms @ Brown", 19, "#FFFFFF", "serif", 500))
for i, lbl in enumerate(("Browse", "Quiz", "Reviews")):
    o.append(t(W - 240 + i * 82, 39, lbl, 13, "#F2DCD6", "sans", 400))

# ---------------------------------------------------------------- search + filters
o.append(r(24, 90, W - 48, 42, PAPER, 21))
o.append('<circle cx="52" cy="111" r="7" fill="none" stroke="%s" stroke-width="2"/>' % MUT)
o.append('<path d="M 57 116 l 6 6" stroke="%s" stroke-width="2" stroke-linecap="round"/>' % MUT)
o.append(t(72, 116, "Search by dorm name", 13, MUT))

CHIPS = [("Suite", True), ("Single", False), ("Private bath", True),
         ("Kitchen", False), ("First-year", False), ("Ground floor", True)]
x = 24
for label, on in CHIPS:
    w = 26 + len(label) * 7.4
    o.append(r(x, 148, w, 30, BROWN if on else PAPER, 15, op=1 if on else None))
    if not on:
        o.append('<rect x="%.1f" y="148" width="%.1f" height="30" rx="15" fill="none" '
                 'stroke="%s" stroke-width="1.5"/>' % (x, w, LINE))
    o.append(t(x + w / 2, 168, label, 12, "#FFFFFF" if on else MUT, "sans", 500, "middle"))
    x += w + 10

o.append(t(24, 214, "30 dorms  ·  8 match your filters", 12, MUT, "mono"))

# ---------------------------------------------------------------- dorm cards
DORMS = [
    ("Keeney Quadrangle", "First-year · Double · Hall bath", 3, 4, STONE),
    ("Grad Center A", "Upperclass · Suite · Private bath", 4, 5, "#A79880"),
    ("Young Orchard 4", "Upperclass · Apartment · Kitchen", 5, 5, IVY),
    ("New Pembroke 3", "Upperclass · Single · Hall bath", 4, 4, SLATE),
    ("Barbour Hall", "Upperclass · Suite · Kitchen", 3, 3, "#B8A48C"),
    ("Hope College", "Sophomore · Double · Hall bath", 4, 4, "#9E8C74"),
]
rr = random.Random(6)
y = 236
for i, (name, meta, rating, _n, tone) in enumerate(DORMS):
    o.append(r(24, y, W - 48, 128, PAPER, 12))
    # The photo. Letterboxed over a blurred copy of itself in the real app, which
    # at this size reads as a lighter band top and bottom.
    o.append(r(24, y, 178, 128, tone))
    o.append(r(24, y, 178, 22, tone, op=.55))
    o.append(r(24, y + 106, 178, 22, tone, op=.55))
    # A suggestion of a room: window, bed, desk.
    o.append(r(52, y + 38, 42, 34, "#FFFFFF", 3, op=.55))
    o.append(r(58, y + 44, 12, 22, tone, 1, op=.8))
    o.append(r(78, y + 44, 12, 22, tone, 1, op=.8))
    o.append(r(112, y + 62, 62, 26, "#FFFFFF", 3, op=.4))
    o.append(r(112, y + 92, 40, 8, "#FFFFFF", 2, op=.3))

    o.append(t(220, y + 34, name, 16, INK, "serif", 500))
    o.append(t(220, y + 56, meta, 12, MUT, "sans"))
    o.append(stars(224, y + 78, rating))
    o.append(t(224 + 5 * 23 + 8, y + 82, "%d.%d" % (rating, rr.randint(1, 9)),
               12, MUT, "mono"))
    # Amenity ticks.
    for k, am in enumerate(("Floor plans", "%d reviews" % rr.randint(4, 31))):
        o.append(r(220 + k * 132, y + 96, 118, 22, WASH, 11))
        o.append(t(279 + k * 132, y + 111, am, 11, MUT, "mono", 400, "middle"))
    o.append('<path d="M %d %d l 7 7 l -7 7" stroke="%s" stroke-width="2" fill="none" '
             'stroke-linecap="round" stroke-linejoin="round"/>' % (W - 52, y + 57, MUT))
    y += 140

# ---------------------------------------------------------------- quiz callout
o.append(r(24, y + 8, W - 48, 104, BROWN, 12))
o.append(t(48, y + 46, "Not sure where to start?", 17, "#FFFFFF", "serif", 500))
o.append(t(48, y + 70, "Answer six questions, get a ranked shortlist worth touring.",
           13, "#F2DCD6", "sans"))
o.append(r(W - 196, y + 40, 148, 38, GOLD, 19))
o.append(t(W - 122, y + 64, "Take the quiz", 13, BROWN, "sans", 700, "middle"))

io.open("assets/tile/dorms.jpg".replace(".jpg", ".svg"), "w", encoding="utf-8").write(
    '<svg width="%d" height="%d" viewBox="0 0 %d %d" fill="none" '
    'xmlns="http://www.w3.org/2000/svg">%s</svg>\n' % (W, H, W, H, "".join(o)))
print("assets/tile/dorms.svg  %dx%d" % (W, H))
