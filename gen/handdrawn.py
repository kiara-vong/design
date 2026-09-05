# -*- coding: utf-8 -*-
"""A hand-drawn rendering vocabulary: wobbly strokes, gouache dabs, paper grain.

The first pass at this site's artwork drew perfect geometry -- exact rects, true
circles, mathematically straight rules -- and it read as what it was, a drawing
made by a machine that has never held a pen. This module replaces the primitives
with ones that make the same shapes badly on purpose.

The wobble is BAKED INTO THE PATH DATA rather than applied with an SVG filter.
feDisplacementMap gives a convincing wobble in one line, but it is a per-pixel
filter: on a full-viewport hero it costs real frame time, it re-rasterises on
every resize, and it blurs any text caught inside it. Jittering the control
points costs nothing at render time and survives being scaled to any size, which
matters here because these files are scaled by the page's stage transform.

Every jitter is drawn from a SEEDED generator keyed to the shape's own position,
so a given drawing is byte-identical between builds. Hand-drawn should mean "looks
drawn by a hand", not "different every time you rerun the script".

Reference for the look is the site owner's own sketchbook work: gouache and marker
on watercolour paper, foliage built from stippled dabs in two or three greens,
outlines that overshoot the corner, fills that sit slightly off the line.
"""
import math
import random


# ----------------------------------------------------------------- geometry
def rng(seed):
    """A generator keyed to an integer, so every shape's wobble is reproducible."""
    return random.Random(seed if isinstance(seed, int) else hash(seed) & 0xFFFFFF)


def _cat(pts, closed=False, tension=6.0):
    """Catmull-Rom through pts, emitted as cubic beziers.

    Used everywhere instead of polylines: a wobbled polyline reads as a jagged
    machine line, and a wobbled spline reads as a wavering hand. The difference
    is most of the effect.
    """
    n = len(pts)
    if n < 2:
        return ""
    p = list(pts)
    if closed:
        p = [pts[-1]] + list(pts) + [pts[0], pts[1]]
    else:
        p = [pts[0]] + list(pts) + [pts[-1]]
    d = ["M %.2f %.2f" % (p[1][0], p[1][1])]
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / tension, p1[1] + (p2[1] - p0[1]) / tension)
        c2 = (p2[0] - (p3[0] - p1[0]) / tension, p2[1] - (p3[1] - p1[1]) / tension)
        d.append("C %.2f %.2f %.2f %.2f %.2f %.2f"
                 % (c1[0], c1[1], c2[0], c2[1], p2[0], p2[1]))
    if closed:
        d.append("Z")
    return " ".join(d)


def jitter(pts, amp, seed, closed=False):
    """Push each point off the true path by up to amp, perpendicular to the run."""
    r = rng(seed)
    out, n = [], len(pts)
    for i, (x, y) in enumerate(pts):
        a = pts[(i + 1) % n] if (closed or i < n - 1) else pts[i - 1]
        b = pts[i - 1] if (closed or i > 0) else pts[i + 1]
        dx, dy = a[0] - b[0], a[1] - b[1]
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L, dx / L
        k = r.uniform(-amp, amp)
        # A little along-path drift too, so the wobble is not a pure ripple.
        t = r.uniform(-amp, amp) * .45
        out.append((x + nx * k + dx / L * t, y + ny * k + dy / L * t))
    return out


def sample_line(x1, y1, x2, y2, step=26.0):
    L = math.hypot(x2 - x1, y2 - y1)
    n = max(2, int(L / step) + 1)
    return [(x1 + (x2 - x1) * i / (n - 1.0), y1 + (y2 - y1) * i / (n - 1.0))
            for i in range(n)]


def sample_ellipse(cx, cy, rx, ry, n=18, start=0.0, sweep=math.pi * 2):
    return [(cx + rx * math.cos(start + sweep * i / float(n)),
             cy + ry * math.sin(start + sweep * i / float(n))) for i in range(n)]


def sample_rect(x, y, w, h, step=30.0, overshoot=0.0):
    """Rectangle as a point run. overshoot pushes the corners past each other."""
    o = overshoot
    pts = []
    pts += sample_line(x - o, y, x + w + o, y, step)
    pts += sample_line(x + w, y - o, x + w, y + h + o, step)[1:]
    pts += sample_line(x + w + o, y + h, x - o, y + h, step)[1:]
    pts += sample_line(x, y + h + o, x, y - o, step)[1:]
    return pts


def sample_poly(corners, step=14.0, closed=True):
    """Walk a polygon's perimeter, dropping a point every `step`.

    _cat() runs a spline THROUGH the points it is given, so a quadrilateral
    handed over as four corners comes back as a pill -- which is exactly what
    happened to the laptop: lid and base both rendered as rounded blobs and merged
    into one shape under the sticker rim. Sampling along each edge first keeps the
    corners corners, because there are now several collinear points either side of
    each one holding the spline flat.
    """
    pts, n = [], len(corners)
    last = n if closed else n - 1
    for i in range(last):
        a, b = corners[i], corners[(i + 1) % n]
        seg = sample_line(a[0], a[1], b[0], b[1], step)
        pts += seg[:-1] if closed or i < last - 1 else seg
    return pts


# ----------------------------------------------------------------- strokes
def stroke(pts, col, w=3.0, seed=1, amp=1.6, passes=2, closed=False,
           opacity=1.0, cap="round"):
    """A drawn line: two or three passes, each wobbled differently.

    Drawing the same line twice is what a pen actually does when someone is
    sketching rather than drafting, and it is the single cheapest cue that a
    shape was not machine-made. Later passes are thinner and fainter so the
    result reads as one line with a doubled edge, not as two lines.
    """
    out = []
    for k in range(passes):
        p = jitter(pts, amp * (1.0 + .35 * k), seed * 7919 + k * 131, closed)
        out.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.2f" '
                   'stroke-linecap="%s" stroke-linejoin="round" opacity="%.2f"/>'
                   % (_cat(p, closed), col, w * (1.0 - .22 * k), cap,
                      opacity * (1.0 - .32 * k)))
    return "".join(out)


def line(x1, y1, x2, y2, col, w=3.0, seed=1, amp=1.6, passes=2, opacity=1.0):
    return stroke(sample_line(x1, y1, x2, y2), col, w, seed, amp, passes,
                  False, opacity)


def box(x, y, w, h, col, sw=3.0, seed=1, amp=1.6, fill=None, fill_off=(1.5, 1.5),
        passes=2, overshoot=2.5):
    """A drawn rectangle. The fill sits slightly off the outline, on purpose.

    Colouring a hair outside the line is what marker work looks like and what
    every crisp vector rectangle fails to do. fill_off is that offset.
    """
    out = []
    pts = sample_rect(x, y, w, h, 30.0, overshoot)
    if fill:
        fp = jitter(sample_rect(x + fill_off[0], y + fill_off[1], w, h, 34.0),
                    amp * 1.3, seed * 31 + 5, True)
        out.append('<path d="%s" fill="%s"/>' % (_cat(fp, True), fill))
    if col:
        out.append(stroke(pts, col, sw, seed, amp, passes, True))
    return "".join(out)


def circle(cx, cy, r, col=None, sw=3.0, seed=1, amp=1.4, fill=None,
           fill_off=(1.2, 1.2), passes=2, ry=None):
    out = []
    ry = r if ry is None else ry
    if fill:
        fp = jitter(sample_ellipse(cx + fill_off[0], cy + fill_off[1], r, ry, 16),
                    amp * 1.25, seed * 17 + 3, True)
        out.append('<path d="%s" fill="%s"/>' % (_cat(fp, True), fill))
    if col:
        out.append(stroke(sample_ellipse(cx, cy, r, ry, 16), col, sw, seed,
                          amp, passes, True))
    return "".join(out)


def blob(pts, fill, seed=1, amp=2.4, opacity=1.0):
    """A filled organic shape: no outline, just a wobbled silhouette."""
    return ('<path d="%s" fill="%s" opacity="%.2f"/>'
            % (_cat(jitter(pts, amp, seed, True), True), fill, opacity))


# ----------------------------------------------------------------- painting
def dabs(cx, cy, rx, ry, n, cols, seed=1, size=(3.0, 7.0), edge=1.25):
    """Stippled paint dabs filling a soft cluster: the foliage technique.

    Taken straight off the sketchbook trees -- a mass built from separated marks
    in two or three greens rather than one filled shape, with the dabs crowding
    toward the edge so the silhouette reads without being outlined.
    """
    r, out = rng(seed), []
    for i in range(n):
        a = r.uniform(0, math.pi * 2)
        # sqrt keeps the distribution even by area; the exponent above 0.5 pushes
        # marks outward so the cluster has a busy rim and an open middle.
        d = r.random() ** (1.0 / (2.0 * edge))
        x, y = cx + math.cos(a) * rx * d, cy + math.sin(a) * ry * d
        s = r.uniform(*size)
        col = cols[i % len(cols)]
        out.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" '
                   'transform="rotate(%.0f %.1f %.1f)" opacity="%.2f"/>'
                   % (x, y, s, s * r.uniform(.62, .95), col,
                      r.uniform(0, 180), x, y, r.uniform(.78, 1.0)))
    return "".join(out)


def wash(pts, fill, seed=1, layers=3, amp=3.0):
    """A watercolour pool: the same blob stacked with growing wobble.

    Real watercolour dries darker where it pooled at the edge, so the layers go
    from large-and-faint to small-and-stronger and the overlap does the rest.
    """
    out = []
    for k in range(layers):
        out.append('<path d="%s" fill="%s" opacity="%.3f"/>'
                   % (_cat(jitter(pts, amp * (1.0 + k * .5), seed * 53 + k, True),
                           True), fill, .16 + k * .07))
    return "".join(out)


def taper(x1, y1, x2, y2, col, w0, w1, seed=1, bow=0.0):
    """A brush stroke that changes width along its length.

    Built as a filled outline rather than a stroke, because SVG strokes are a
    constant width and a constant width is the thing that reads as a computer.
    """
    r = rng(seed)
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / L, dx / L
    mx, my = (x1 + x2) / 2 + nx * bow, (y1 + y2) / 2 + ny * bow
    wm = (w0 + w1) * .5 * r.uniform(.9, 1.15)
    up = "M %.1f %.1f Q %.1f %.1f %.1f %.1f" % (
        x1 + nx * w0 / 2, y1 + ny * w0 / 2, mx + nx * wm, my + ny * wm,
        x2 + nx * w1 / 2, y2 + ny * w1 / 2)
    dn = "L %.1f %.1f Q %.1f %.1f %.1f %.1f Z" % (
        x2 - nx * w1 / 2, y2 - ny * w1 / 2, mx - nx * wm, my - ny * wm,
        x1 - nx * w0 / 2, y1 - ny * w0 / 2)
    return '<path d="%s %s" fill="%s"/>' % (up, dn, col)


# ----------------------------------------------------------------- texture
def defs_paper(idn="paper", freq=".9", octaves="4"):
    """Grain, for laying over a finished drawing at low opacity."""
    return ('<filter id="%s" x="0" y="0" width="100%%" height="100%%">'
            '<feTurbulence type="fractalNoise" baseFrequency="%s" numOctaves="%s" '
            'stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/>'
            '</filter>' % (idn, freq, octaves))


def paper(w, h, idn="paper", opacity=.10, mode="multiply"):
    return ('<rect width="%g" height="%g" filter="url(#%s)" opacity="%.3f" '
            'style="mix-blend-mode:%s"/>' % (w, h, idn, opacity, mode))


def defs_bleed(idn="bleed", scale="2.6", freq=".035", seed="4"):
    """A gentle edge displacement.

    Kept for the few places where baked wobble cannot reach -- text, and shapes
    that have to stay geometrically exact for layout. Deliberately weak: at any
    real strength it turns type to mush.
    """
    return ('<filter id="%s"><feTurbulence type="fractalNoise" baseFrequency="%s" '
            'numOctaves="2" seed="%s" result="n"/>'
            '<feDisplacementMap in="SourceGraphic" in2="n" scale="%s" '
            'xChannelSelector="R" yChannelSelector="G"/></filter>'
            % (idn, freq, seed, scale))
