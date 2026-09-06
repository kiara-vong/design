# -*- coding: utf-8 -*-
"""Original botanical + mascot art, authored to the same palette as site.css.

Nothing here traces the original site's assets. The shapes are built from a
handful of primitives (a stem arc, a leaf teardrop, a five-petal bloom) so the
light and dark variants are the same geometry with a different palette dict
rather than two drawings that have to be kept in sync by hand.
"""
import io, math, random

# Palette keys match the CSS custom properties they stand in for.
# Retuned for the blue accent. The bloom used to be the accent itself, which worked
# when the accent was persimmon: a hot orange flower on parchment. A blue flower on
# cream reads as cold and slightly wrong, because nothing in a garden is that colour.
#
# So the roles swap. The bloom goes to the palette's own warm cream and the accent
# moves to the CORE, where it is a small blue centre inside a pale flower -- which is
# a thing that exists, and which ties the botanicals to the rest of the site without
# asking the eye to accept a blue petal.
# On parchment the bloom cannot be cream: #FFF3D2 on #FDFBEF is a two-value
# difference and the flowers simply disappeared, leaving bare stems. Warm gold reads
# as a flower on that ground, and the blue core is what ties it to the accent.
LIGHT = dict(stem="#6F9A2E", leaf="#8D9934", bloom="#E9C46A", core="#43728A")
DARK  = dict(stem="#E2F085", leaf="#C8D665", bloom="#FFF6D8", core="#7FB0C8")

def svg(w, h, body):
    return ('<svg width="%g" height="%g" viewBox="0 0 %g %g" fill="none" '
            'xmlns="http://www.w3.org/2000/svg">\n%s\n</svg>\n' % (w, h, w, h, body))

def leaf(cx, cy, ln, ang, col, curl=0.45):
    """A teardrop leaf: two mirrored quadratics from the base to the tip.

    `curl` is how far the control points bow off the spine, as a fraction of
    length, so a leaf keeps its shape at any size instead of going needle-thin
    when scaled down.
    """
    a = math.radians(ang)
    tx, ty = cx + ln * math.cos(a), cy + ln * math.sin(a)
    nx, ny = -math.sin(a) * ln * curl, math.cos(a) * ln * curl
    return ('<path d="M %.1f %.1f Q %.1f %.1f %.1f %.1f Q %.1f %.1f %.1f %.1f Z" '
            'fill="%s"/>' % (cx, cy,
                             cx + (tx-cx)*.5 + nx, cy + (ty-cy)*.5 + ny, tx, ty,
                             cx + (tx-cx)*.5 - nx, cy + (ty-cy)*.5 - ny, cx, cy, col))

def bloom(cx, cy, r, p):
    """Five petals on a ring plus a centre disc."""
    out = []
    for i in range(5):
        a = -90 + i * 72
        out.append(leaf(cx, cy, r * 1.5, a, p["bloom"], curl=.62))
    out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx, cy, r*.42, p["core"]))
    return "".join(out)

def sprig(w, h, p, pairs, bloomed=True):
    """A stem rising from the bottom centre with `pairs` of opposed leaves."""
    bx, by, ty = w/2.0, h, h*0.14
    parts = ['<path d="M %.1f %.1f C %.1f %.1f %.1f %.1f %.1f %.1f" stroke="%s" '
             'stroke-width="%.1f" stroke-linecap="round"/>'
             % (bx, by, bx-w*.14, by-h*.34, bx+w*.12, by-h*.62, bx, ty,
                p["stem"], max(2.0, w*0.055))]
    for i in range(pairs):
        t = (i + 1) / float(pairs + 1)
        y = by - (by - ty) * t
        x = bx + math.sin(t * math.pi * 1.6) * w * 0.06
        ll = w * (0.30 - 0.07 * t)
        parts.append(leaf(x, y, ll, 200 - 26 * i, p["leaf"]))
        parts.append(leaf(x, y, ll, -20 + 26 * i, p["leaf"]))
    if bloomed:
        parts.append(bloom(bx, ty, w * 0.115, p))
    return svg(w, h, "".join(parts))

for name, pal in (("", LIGHT), ("-dark", DARK)):
    for size, (w, h, pairs) in (("sm", (34, 52, 2)), ("med", (46, 78, 3)), ("lg", (62, 108, 4))):
        io.open("assets/ui/plant%s-%s.svg" % (name, size), "w", encoding="utf-8").write(
            sprig(w, h, pal, pairs))

# The cursor. 24x32, and the size is a hard constraint rather than a preference:
# Windows silently refuses a CSS cursor larger than 32px in either dimension and
# falls back to the default arrow. This was 28x40, so on a good many machines the
# custom cursor never appeared at all, which is the kind of bug that looks like
# "it works for me".
#
# The hotspot goes in site.css and must be the BASE of the stem, bottom centre,
# because that is where site-footer.js plants the stamp: .plant-stamp img is
# left:0;bottom:0;translate(-50%,0), so the click point is the ground the plant
# grows up from. It was 18 29, which is neither the base nor the tip but a point in
# mid-air to the right of the stem, so every click landed 11px above and 4px left of
# where the cursor appeared to be pointing.
CURSOR_W, CURSOR_H = 24, 32
for name, pal in (("plant-cursor", LIGHT), ("plant-cursor-dark", DARK)):
    io.open("assets/ui/%s.svg" % name, "w", encoding="utf-8").write(
        sprig(CURSOR_W, CURSOR_H, pal, 2))


# The link cursor used to be drawn here: one leaf, tip at the top left, with a halo
# so it read on any ground. It is one of the hand-drawn icons now, the clover from
# the third row of the sheet, cut by gen/icons.py. Same idea, her hand instead of
# this file's primitives.

# The footer flowers used to be generated here as a three-tile sprite plus two
# single-tile variants. They are the hand-drawn ones now: gen/icons.py cuts them out
# of one sheet and assembles a different trio per page.
print("art written")
