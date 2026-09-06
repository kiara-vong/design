# -*- coding: utf-8 -*-
"""Polaroids of the site owner's own artwork, for the About page's hover well.

The original About page hangs eight polaroids off a "I also moonlight as" list --
hover a link, the matching photo swings into the well. Those were photographs of
the original author's life. These are photographs of this owner's, taken straight
from the art archive in ../website/art, which is the honest version of the same
idea and the one thing on this site that could not be drawn.

Each plate is composited rather than CSS-framed: a real polaroid has a thick
bottom margin, a slightly warm white, and a caption written by hand, and doing
that in the image means the About page can treat all eight as one interchangeable
asset at one size.

Output is 427x638 to match .ab-art img's box exactly, so nothing is resampled by
the browser.
"""
import io
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageOps

SRC = os.path.join("..", "website", "art")
# Personal photographs, staged rather than pulled from the art folders. They are
# under _src so the build never treats them as its own output and deletes them.
SELF = os.path.join("assets", "about", "_src")
OUT = "assets/about"
W, H = 427, 638
PAD = 26                      # side and top margin
IMG_H = 452                   # the picture window; the rest is the caption skirt
PAPER = (253, 251, 243)
INK = (62, 58, 56)

HAND = r"C:\Windows\Fonts\Inkfree.ttf"
FALLBACK = r"C:\Windows\Fonts\comic.ttf"

# (slug, source file, caption). The captions are the voice of the page, so they
# are written the way someone labels their own snapshot, not the way a gallery
# labels a work.
PLATES = [
    # A source that starts with "@" is one of Kiara's own photographs in _src; the
    # rest are pulled out of her art folders.
    ("painting",  "@artist.jpg",              "not a Bob Ross"),
    ("food",      "@food.jpg",                "worth the queue"),
    ("amc",       "@amc.jpg",                 "A-List, fully used"),
    ("kpop",      "@kpop.jpg",                "reformed, allegedly"),
    ("smiski",    "@smiski.jpg",              "room for one more"),
    ("cats",      "@cat.jpg",                 "she has notes"),
]


def load_font(size):
    for path in (HAND, FALLBACK):
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def find(rel):
    """Resolve a source path, falling back to any sibling in the same folder.

    The archive is somebody's real folder of scans, not a fixture: a name that is
    right today may not be tomorrow. Falling back to a sibling means a renamed
    file changes which picture appears, never whether the page builds.
    """
    if rel.startswith("@"):                      # a personal photograph in _src
        p = os.path.join(SELF, rel[1:])
        return p if os.path.exists(p) else None
    if rel.startswith("!"):                      # a path from the project root
        p = rel[1:]
        return p if os.path.exists(p) else None
    p = os.path.join(SRC, rel)
    if os.path.exists(p):
        return p
    folder = os.path.dirname(p)
    if os.path.isdir(folder):
        for f in sorted(os.listdir(folder)):
            if f.lower().endswith((".jpg", ".jpeg", ".png")):
                return os.path.join(folder, f)
    return None


def plate(slug, rel, caption, seed):
    src = find(rel)
    if not src:
        print("  skip %-12s (no source for %s)" % (slug, rel))
        return False
    r = random.Random(seed)
    card = Image.new("RGB", (W, H), PAPER)

    # Warm the paper unevenly so eight plates are not eight identical rectangles.
    d = ImageDraw.Draw(card)
    for i in range(H):
        k = int(4 * (i / float(H)))
        d.line([(0, i), (W, i)], fill=(PAPER[0] - k, PAPER[1] - k, PAPER[2] - k - 2))

    photo = ImageOps.exif_transpose(Image.open(src))
    if photo.mode in ("RGBA", "LA", "P"):
        photo = photo.convert("RGBA")
        ground = Image.new("RGBA", photo.size, PAPER + (255,))
        photo = Image.alpha_composite(ground, photo)
    photo = photo.convert("RGB")
    box = (W - PAD * 2, IMG_H)
    photo = ImageOps.fit(photo, box, Image.LANCZOS, centering=(0.5, 0.42))
    card.paste(photo, (PAD, PAD))

    # A hairline inside the window: real prints have an edge where the emulsion
    # stops, and without it the photo floats off the card at small sizes.
    d.rectangle([PAD, PAD, PAD + box[0] - 1, PAD + box[1] - 1],
                outline=(226, 220, 202), width=1)

    f = load_font(31)
    tw = d.textbbox((0, 0), caption, font=f)[2]
    # Hand-written captions are never centred and never level.
    tx = int((W - tw) / 2 + r.uniform(-16, 16))
    ty = PAD + IMG_H + 42 + int(r.uniform(-5, 5))
    skirt = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(skirt).text((tx, ty), caption, font=f, fill=INK + (232,))
    skirt = skirt.rotate(r.uniform(-1.6, 1.6), resample=Image.BICUBIC, center=(W / 2, ty))
    card.paste(skirt, (0, 0), skirt)

    card.save(os.path.join(OUT, "pol-%s.jpg" % slug), quality=88, optimize=True)
    print("  pol-%-12s <- %s" % (slug + ".jpg", os.path.relpath(src, SRC)))
    return True


print("polaroids:")
made = [p[0] for i, p in enumerate(PLATES) if plate(p[0], p[1], p[2], 100 + i)]

# The well's resting state: what shows before any link is hovered. A small painted
# sprig rather than a photo, so the empty state reads as decoration and not as a
# ninth thing you failed to hover.
open(os.path.join("assets", "ui", "about-rest.svg"), "w").write(
    '<svg width="120" height="111" viewBox="0 0 120 111" fill="none" '
    'xmlns="http://www.w3.org/2000/svg">'
    '<path d="M60 106 C54 78 50 58 44 40" stroke="#8D9934" stroke-width="4" '
    'stroke-linecap="round" fill="none"/>'
    '<path d="M52 74 C36 70 28 58 26 44 C42 46 52 58 52 74 Z" fill="#749F25"/>'
    '<path d="M56 88 C74 86 84 76 88 62 C70 62 58 72 56 88 Z" fill="#8D9934"/>'
    '<circle cx="44" cy="36" r="13" fill="#649F25"/>'
    '<circle cx="44" cy="36" r="5" fill="#FFEDBC"/>'
    '<circle cx="66" cy="28" r="8" fill="#FFEDBC"/>'
    '<circle cx="28" cy="24" r="6" fill="#C8D665"/>'
    '</svg>\n')
print("about-rest.svg written")
print("%d plates" % len(made))
