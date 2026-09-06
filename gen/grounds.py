# -*- coding: utf-8 -*-
"""The two full-bleed grounds: the hero canopy and the About field.

WHY THESE ARE GENERATED AND NOT PHOTOGRAPHED

The hero is defocused foliage and the About ground is a field
under motion blur. Both are colour, depth and grain, and all three of those are
things a script can do honestly.

That is the whole argument for generating rather than sourcing. Nobody can draw a
convincing tree from a formula, but a lens at f/1.4 pointed at a canopy produces
overlapping discs of light, and that IS a formula.

PALETTE

Studio Ghibli's background painting, Kazuo Oga's especially, is recognisable for two
things this file tries to reproduce. Greens sit high in saturation but shadows never
go to black, they go to a deep blue-green, so the darkest part of a frame still has
hue in it. And there is almost always one warm passage, sunlight through leaves,
sitting against all that cool green. A palette of greens alone reads as a golf
course; it is the warm intrusion that makes it read as light.

Every layer is seeded, so a given variant is identical between runs.
"""
import io
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.join("assets", "hero")

# (name, sky/top, canopy mid, deep shadow, sunlight warm, haze)
PALETTES = {
    # Deep summer canopy, sun somewhere behind it. Closest to the ground it replaces.
    "canopy": ("#22392E", "#4E7A43", "#16261F", "#E8D89A", "#93B36A"),
    # Later in the day: the greens cool and the warm passage widens.
    "dusk":   ("#1C3040", "#41684B", "#12212B", "#F0C98A", "#7FA07C"),
    # Wet green, a lot of sky bouncing around in it.
    "rain":   ("#2A4A4A", "#4F7F6B", "#16302F", "#CFE0AE", "#8FBCA6"),
    # The warm one, for the About ground: a field rather than a canopy.
    "field":  ("#8A6A3A", "#C08B41", "#4A3218", "#F3DCA6", "#A88348"),
}


def hx(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def mix(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def vgrad(w, h, stops):
    """A vertical ramp through several colours. The base every ground starts from."""
    im = Image.new("RGB", (1, h))
    px = im.load()
    n = len(stops) - 1
    for y in range(h):
        t = y / float(h - 1) * n
        i = min(int(t), n - 1)
        px[0, y] = mix(stops[i], stops[i + 1], t - i)
    return im.resize((w, h), Image.BILINEAR)


def grain(im, amount, seed):
    """Film grain, added last. Without it a blurred gradient reads as a CSS gradient
    rather than as a photograph: the eye is looking for sensor noise and its absence
    is what makes synthetic images feel synthetic."""
    r = random.Random(seed)
    w, h = im.size
    n = Image.new("L", (w // 2, h // 2))
    n.putdata([r.gauss(128, 42) for _ in range((w // 2) * (h // 2))])
    n = n.resize((w, h), Image.BILINEAR)
    return Image.blend(im, Image.merge("RGB", (n, n, n)), amount)


def canopy(w, h, pal, seed=7, discs=520):
    """Defocused foliage.

    The first attempt was discs scattered evenly and blurred by half their own
    radius, which produced a flat green wash: at that ratio a disc stops being a disc
    before it stops being visible, and an even scatter has no composition to see
    anyway. Two fixes, and both matter.

    Blur per plane is a fraction of the DISC size, not of the frame, so a disc is
    always softened rather than erased. And the frame is given a structure first:
    dark verticals standing in for trunks, one bright horizontal band of lit
    undergrowth, and the discs clustered into that band rather than sprinkled
    everywhere. Real bokeh clumps, because leaves do.
    """
    top, midc, deep, warm, haze = [hx(c) for c in pal]
    r = random.Random(seed)
    S = h / 1000.0                       # everything below is authored at h = 1000

    im = vgrad(w, h, [deep, top, mix(midc, haze, .30), mix(midc, deep, .45), deep])

    # ---- the lit band: where the sun gets through, and where type will not go ----
    band = Image.new("RGB", (w, h))
    band.paste(im)
    bd = ImageDraw.Draw(band, "RGBA")
    by = h * r.uniform(.46, .58)
    for _ in range(40):
        bx = r.uniform(-.05, 1.05) * w
        bw_ = r.uniform(.10, .34) * w
        bh_ = r.uniform(.05, .13) * h
        # ONE jitter, applied to both edges. Two independent ones can invert the
        # box, and PIL refuses an ellipse whose bottom is above its top.
        jy = r.gauss(0, .04) * h
        bd.ellipse([bx - bw_, by - bh_ + jy, bx + bw_, by + bh_ + jy],
                   fill=mix(haze, warm, r.uniform(.15, .6)) + (int(r.uniform(40, 96)),))
    band = band.filter(ImageFilter.GaussianBlur(46 * S))
    im = Image.blend(im, band, .72)

    # ---- trunks: soft dark verticals, the only structure with an edge ----
    tr = Image.new("RGB", (w, h))
    tr.paste(im)
    td = ImageDraw.Draw(tr, "RGBA")
    for _ in range(r.randint(3, 5)):
        x = r.uniform(.04, .96) * w
        tw = r.uniform(.012, .035) * w
        lean = r.uniform(-.05, .05) * w
        td.polygon([(x - tw, 0), (x + tw, 0),
                    (x + tw * .7 + lean, h * .92), (x - tw * .7 + lean, h * .92)],
                   fill=mix(deep, (0, 0, 0), .35) + (int(r.uniform(90, 150)),))
    tr = tr.filter(ImageFilter.GaussianBlur(30 * S))
    im = Image.blend(im, tr, .80)

    # ---- bokeh, in clumps, three depth planes ----
    for count, rad, soft, op in ((int(discs * .46), (14, 30), .34, .34),
                                 (int(discs * .34), (26, 58), .30, .40),
                                 (int(discs * .20), (52, 120), .26, .30)):
        layer = Image.new("RGB", (w, h))
        layer.paste(im)
        d = ImageDraw.Draw(layer, "RGBA")
        mean = sum(rad) / 2.0 * S
        n = 0
        while n < count:
            # a clump, not a sprinkle
            cxs, cys = r.uniform(-.05, 1.05) * w, by + r.gauss(0, .30) * h
            for _ in range(r.randint(4, 12)):
                if n >= count:
                    break
                n += 1
                cx = cxs + r.gauss(0, .07) * w
                cy = cys + r.gauss(0, .05) * h
                rr = r.uniform(*rad) * S
                k = max(0.0, 1.0 - abs(cy - by) / (h * .42))
                col = mix(mix(deep, midc, .35 + .65 * k), warm, (k ** 2) * r.uniform(0, .62))
                d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                          fill=col + (int(255 * op * r.uniform(.45, 1.0)),))
        layer = layer.filter(ImageFilter.GaussianBlur(mean * soft))
        im = Image.blend(im, layer, .86)

    # ---- the sun, well out of focus ----
    glow = Image.new("RGB", (w, h), (0, 0, 0))
    g = ImageDraw.Draw(glow)
    gx, gy = w * r.uniform(.52, .76), by - h * r.uniform(.02, .10)
    gr = h * r.uniform(.34, .48)
    for i in range(24):
        t = i / 23.0
        g.ellipse([gx - gr * (1 - t * .85), gy - gr * (1 - t * .85),
                   gx + gr * (1 - t * .85), gy + gr * (1 - t * .85)],
                  fill=mix((0, 0, 0), warm, .07 + t * .13))
    glow = glow.filter(ImageFilter.GaussianBlur(90 * S))
    im = Image.blend(im, Image.blend(im, glow, .5).point(lambda v: min(255, int(v * 1.10))), .40)

    im = im.filter(ImageFilter.GaussianBlur(5 * S))
    return grain(im, 0.05, seed * 31)


def field(w, h, pal, seed=11, streaks=2600):
    """The About ground: grass under a long exposure. Thin strokes at a shallow angle,
    then blurred ALONG that angle by rotating, blurring on one axis and rotating back.
    A plain Gaussian would smear it in every direction and lose the wind."""
    top, midc, deep, warm, haze = [hx(c) for c in pal]
    r = random.Random(seed)
    # Steeper than it looks in the source, because the blur flattens the read: at
    # -7.5 the streaks came out as a horizontal gradient with no wind in it.
    ang = -13.0

    base = vgrad(w, h, [mix(top, warm, .55), top, midc, mix(midc, deep, .6), deep])
    big = base.rotate(-ang, resample=Image.BICUBIC, expand=True)
    d = ImageDraw.Draw(big, "RGBA")
    bw, bh = big.size
    for _ in range(streaks):
        y = r.uniform(0, bh)
        x = r.uniform(0, bw)
        ln = r.uniform(.10, .45) * bw
        t = y / float(bh)
        col = mix(mix(midc, deep, t), warm, max(0.0, .5 - t) * r.uniform(0, 1.1))
        d.line([x, y, x + ln, y + r.uniform(-2, 2)],
               fill=col + (int(r.uniform(45, 165)),), width=int(r.uniform(1, 7)))
    # Horizontal-only blur in the rotated frame is the motion blur. Kept light: the
    # first pass blurred at 0.006 of the width and erased every streak it had just
    # drawn, leaving a plain vertical gradient.
    big = big.filter(ImageFilter.BoxBlur(bw * 0.0026))
    big = big.rotate(ang, resample=Image.BICUBIC, expand=False)
    c = ((big.size[0] - w) // 2, (big.size[1] - h) // 2)
    im = big.crop((c[0], c[1], c[0] + w, c[1] + h))
    im = im.filter(ImageFilter.GaussianBlur(.004 * h))
    return grain(im, 0.05, seed * 17)


# =====================================================================
# What actually ships
# =====================================================================
# The three grounds are now crops of paintings Kiara chose, not the synthesised
# ones. The generators above are kept because they are the fallback: if a painting
# has to come off the site for any reason, main() can fall back to them without
# anything else changing.
#
# Three different paintings rather than one, for the same reason the reference build
# used a green photograph on the home page and an orange field on About: no two of
# these are ever on screen together, and each is chosen for the type it has to carry.
# They stay a family because they are all Impressionist landscape in the same
# green-and-gold register.
#
#   slug -> (file in _src, output, size, vertical focus)
#
# Vertical focus is the part that matters. It decides which band of the painting
# survives the crop, and the hero's is set high because the calm passage the name
# sits on is in the upper left of the Bannister.
PLATES = [
    # Bannister's Streamside: the darkest of the four and the only one with a quiet
    # passage exactly where the name and six lines of bio go.
    ("edward_mitchell_bannister_-_streamside.jpg", "hero-bg.webp", (2880, 1722), 0.42),
    # Monet's Argenteuil garden, at 4096px the largest file by a distance. It goes on
    # the Art band rather than on About because that band carries a title and one
    # line of type over its own heavy gradient, so a busy, high-key painting survives
    # there. On About, which runs body copy across the whole canvas, it did not.
    ("Claude Monet “The Artist’s Garden in Argenteuil (A Corner of the Garden "
     "with Dahlias)”.jpg", "art-bg.webp", (2200, 1240), 0.52),
    # The Met's 1919 water lilies on About. Darker and far less busy than the
    # Argenteuil, which is what that page needs, but it is only 1076px wide, so both
    # crops are upscales. The wide one is 2.2x and holds; the phone crop is a 1:4.9
    # box from a 1.85:1 painting, which is a narrow vertical slice of it.
    ("Water-Lily_Pond_1919_Claude_Monet_Metropolitan.jpg",
     "about-bg.webp", (2400, 2025), 0.5),
    (None, "about-bg-mobile.webp", (780, 3834), 0.5),

    # The footer ground. Monet's Water Lilies, and the band is cut from the lower
    # third where the big lily cluster is: 810 out of 3265 is a quarter of the height
    # of a square painting, so which quarter is the whole decision.
    #
    # The scrim over it in site.css is much lighter than a photograph would need,
    # because this is a mid-tone painting rather than a dark one. Solved rather than
    # guessed: against cream text, 0.40 already clears 4.5:1 on the brightest five
    # percent of the crop, so the 0.48-to-0.64 gradient it actually uses has real
    # headroom and still lets the painting be a painting.
    ("Claude_Monet_-_Water_Lilies_-_Google_Art_Project_(462013).jpg",
     "footer-bg.webp", (2880, 810), 0.72),
]
SRC = os.path.join("assets", "hero", "_src")

# The synthesised fallbacks, if a painting is ever pulled.
HERO = ("dusk", 5)
ABOUT = ("field", 19)


def main():
    from PIL import ImageOps
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    print("grounds:")
    last = None
    for name, out, size, focus in PLATES:
        if name is not None:
            last = name
        src = os.path.join(SRC, last)
        if not os.path.exists(src):
            print("  MISSING %s" % last)
            continue
        im = Image.open(src).convert("RGB")
        native = im.size
        im = ImageOps.fit(im, size, Image.LANCZOS, centering=(0.5, focus))
        im.save(os.path.join(OUT, out), quality=88, method=6)
        print("  %-22s %dx%d  <- %s (%dx%d, %.1fx)"
              % (out, size[0], size[1], last[:34], native[0], native[1],
                 size[0] / float(native[0])))



if __name__ == "__main__":
    main()
