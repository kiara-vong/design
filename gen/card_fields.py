# -*- coding: utf-8 -*-
"""Painting grounds for the four work cards.

The cards used to sit on generated SVG fields: flat tinted panels, one per card,
drawn to be inoffensive behind a screenshot. They were the last generated texture on
the site, and site.css already says why that was wrong for the reference build it
came from: this site's interest comes from photographs, drawings and type, and a
procedural fill reads as foreign among them.

So the field is a painting now, from the same folder the hero, the About ground, the
footer band and the six project thumbnails are cut from. That is the whole argument
for it: one set of pictures under everything, rather than each surface reaching for
its own answer.

Only a border of each one is visible. .card-photo is 529x304 and the screenshot on
top of it is 480x280 inset at 24.5 and 12, so what shows is a 24px frame on the
sides and a 12px band top and bottom. A painting behind a screenshot would fight it;
a painting around one reads as a mount, which is the same reason it works on the
thumbnails.

Chosen for tone against the screenshot each one carries, not for subject.
"""
import io
import json
import os

from PIL import Image, ImageOps

SRC = os.path.join("assets", "hero", "_src")
OUT = os.path.join("assets", "cards")

# The .card-photo box, at 2x so it survives a retina screen.
W, H = 1058, 608

# card key -> (substring of the painting's filename, vertical centring)
#
# Matched on a SUBSTRING rather than a filename: half of these files carry an en
# dash or an accented character in their name, and spelling those back out in a
# source file is a way to silently match nothing.
FIELDS = {
    # Resource Dashboard. Monet's Argenteuil garden: the warmest of the set, under
    # the coolest screenshot.
    "plat":    ("Argenteuil", 0.52),
    # Events Timeline. Bannister's Streamside, which is the darkest, and the one
    # already carrying the hero, so the two ends of the page rhyme.
    "gql":     ("bannister", 0.44),
    # UI Consistency. Wisinger-Florian's Meadow: busy, and the screenshot over it is
    # the emptiest of the four.
    "ds":      ("Wisinger-Florian", 0.55),
    # Persona Homepage. Chamaillard's spring, the lightest, under a card that is not
    # built yet and should not look heavier than the three that are.
    "persona": ("Chamaillard", 0.5),
}


def main():
    if not os.path.isdir(SRC):
        print("  no %s" % SRC)
        return
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    names = sorted(os.listdir(SRC))
    index = {}
    for key, (match, focus) in sorted(FIELDS.items()):
        hits = [f for f in names if match.lower() in f.lower()]
        if not hits:
            print("  no painting matched %r for %s" % (match, key))
            continue
        im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, hits[0])))
        im = ImageOps.fit(im.convert("RGB"), (W, H), Image.LANCZOS,
                          centering=(0.5, focus))
        dst = os.path.join(OUT, "field-%s.webp" % key)
        im.save(dst, "WEBP", quality=84, method=6)
        index[key] = hits[0]
        print("  field-%-9s %dx%d  %4dKB  <- %s"
              % (key + ".webp", W, H, os.path.getsize(dst) / 1024, hits[0][:40]))
    with io.open("card-fields.json", "w", encoding="utf-8") as fh:
        fh.write(json.dumps(index, indent=1, sort_keys=True) + "\n")
    print("%d card fields" % len(index))


if __name__ == "__main__":
    main()
