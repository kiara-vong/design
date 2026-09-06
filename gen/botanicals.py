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

# The cursor. Kept small and with its hotspot at the top-left of the artwork,
# because CSS cursor hotspots default there and a tall sprig would otherwise
# point from empty space well above the stem.
for name, pal in (("plant-cursor", LIGHT), ("plant-cursor-dark", DARK)):
    io.open("assets/ui/%s.svg" % name, "w", encoding="utf-8").write(sprig(28, 40, pal, 2))

# Footer flowers. site.css cuts these with object-fit:none and three
# object-position offsets (0, -122.504px, -245.007px) out of a 120px-wide column,
# so the file has to be a SPRITE of three distinct 120x110.5 tiles stacked, not one
# picture. The first pass shipped a single 230x150 cluster: tile 1 rendered a crop of
# it and tiles 2 and 3 landed past the bottom edge and came back empty, which is why
# the footer showed a few loose stems. The About and Library variants are read with
# object-fit:contain instead and want a single tile, so they get one.
TILE_W, TILE_H, TILE_GAP = 120.0, 110.504, 122.504

def posy(w, h, p, seed, n=5):
    """One compact bouquet, sized to fill a 120x110 tile."""
    rr = random.Random(seed)
    parts, base = [], h - 4
    for i in range(n):
        t = (i + .5) / float(n)
        x = w * (0.13 + 0.74 * t)
        top = h * (0.50 - 0.34 * math.sin(t * math.pi)) + rr.uniform(-5, 5)
        lean = (x - w / 2.0) * 0.20
        parts.append('<path d="M %.1f %.1f Q %.1f %.1f %.1f %.1f" stroke="%s" '
                     'stroke-width="4.2" stroke-linecap="round" fill="none"/>'
                     % (x, base, x - lean, (base + top) * .55, x, top, p["stem"]))
        ly = base - (base - top) * .42
        parts.append(leaf(x, ly, w * .125, 202, p["leaf"]))
        parts.append(leaf(x, ly, w * .125, -22, p["leaf"]))
        parts.append(bloom(x, top, w * 0.078, p))
    return "".join(parts)

# Each footer variant paints a different ground, so each needs its own palette
# rather than the generic LIGHT/DARK pair: the first pass drew accent-coloured blooms on
# the accent footer and they simply were not there. The rule for all three is the
# same -- stem and leaf in a green that holds against the ground, blooms in the
# palette's lightest value, and the bloom core in the GROUND colour, so the middle
# of each flower reads as a hole punched back through to the footer.
# On the deep blue band. The core was the accent itself, which was legible on
# orange and vanishes on blue, so it takes the new-leaf green instead; stem and
# leaf lift a step because the ground under them is darker than it was.
ON_ACCENT = dict(stem="#CBDA79", leaf="#A8B44E", bloom="#FFF6D8", core="#E4F56F")
ON_PEAR      = dict(stem="#749F25", leaf="#8D9934", bloom="#FDFBEF", core="#E2F085")
ON_INK       = dict(stem="#8DA85E", leaf="#6E8548", bloom="#E2F085", core="#1F597B")

sprite = []
for k in range(3):
    sprite.append('<g transform="translate(0,%.3f)">%s</g>'
                  % (k * TILE_GAP, posy(TILE_W, TILE_H, ON_ACCENT, 31 + k, 4 + k)))
io.open("assets/ui/footer-flowers.svg", "w", encoding="utf-8").write(
    svg(TILE_W, TILE_GAP * 2 + TILE_H, "".join(sprite)))

# Single tiles: these two are read with object-fit:contain, not as a sprite.
io.open("assets/ui/foot-flower-about.svg", "w", encoding="utf-8").write(
    svg(TILE_W, TILE_H, posy(TILE_W, TILE_H, ON_PEAR, 31, 5)))
io.open("assets/ui/foot-flower-alt.svg", "w", encoding="utf-8").write(
    svg(TILE_W, TILE_H, posy(TILE_W, TILE_H, ON_INK, 32, 5)))
print("art written")
