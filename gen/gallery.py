# -*- coding: utf-8 -*-
"""Cuts the Art section's images and writes the category index.

The content it works from -- categories, pieces, titles -- is content/art_pieces.py.
This file is only the machinery: resolve a path, open, transpose, cap the width,
encode, and emit content/art_index.py for the page generators to read.

Third pass, and the change is structural rather than cosmetic. The archive is no
longer a flat list of pieces with a medium attached: it is a set of CATEGORIES,
five of which are real projects with reports behind them and nine of which are
bodies of studio work. The Art page is now an index of those categories, and each
one gets its own page.

The five project categories come from coursework at Brown, and three of them are
team projects. Their pages credit the team by name. That is not a formality: a
lab report with four contributors on the cover is not a solo portfolio piece, and
presenting it as one is the kind of thing that falls apart in an interview.

Covers keep their NATURAL ratio, capped to a width. The category pages are salon
hangs and want real proportions -- a vortex ring photographed in landscape and a
sketchbook page are not the same shape and should not be cropped as if they were.

Sources under assets/art/_src are frames already pulled from video, or figures
already lifted out of a .docx, so they are staged rather than re-extracted here.
Everything in assets/art that does not start with "_" is regenerated each run.
"""
import io
import os
from PIL import Image, ImageOps

# The categories, the pieces and every title live in content/art_pieces.py. This file
# does not know or care what any of them say.
from content.art_pieces import CATEGORIES

OUT = os.path.join("assets", "art")
MAX_W = 760


def fallback(path):
    """Resolve a path, falling back to a sibling if the exact file has moved."""
    if os.path.exists(path):
        return path
    folder = os.path.dirname(path)
    if os.path.isdir(folder):
        for f in sorted(os.listdir(folder)):
            if f.lower().endswith((".jpg", ".jpeg", ".png")):
                return os.path.join(folder, f)
    return None


def _walk(root):
    """Every generated file under assets/art, one level down as well as at the top.

    The cut images live in per-category folders now, so a flat listdir would leave
    every one of them behind on a rebuild and the stale-file guarantee this loop
    exists for would quietly stop holding.
    """
    out = []
    for name in os.listdir(root):
        p = os.path.join(root, name)
        if name.startswith("_"):
            continue
        if os.path.isdir(p):
            out += [os.path.join(p, n) for n in os.listdir(p)]
        else:
            out.append(p)
    return out


if not os.path.isdir(OUT):
    os.makedirs(OUT)
# Clear only generated covers. Anything under _src is a staged source and any
# file starting with "_" is deliberately not ours to delete.
for p in _walk(OUT):
    if os.path.isfile(p) and not os.path.basename(p).startswith("_"):
        os.remove(p)

index = []
total = 0
print("covers:")
for cat in CATEGORIES:
    rows = []
    for slug, path, title, blurb in cat["pieces"]:
        src = fallback(path)
        if not src:
            print("  MISS %-16s %s" % (slug, path))
            continue
        im = ImageOps.exif_transpose(Image.open(src).convert("RGB"))
        if im.size[0] > MAX_W:
            im = im.resize((MAX_W, int(im.size[1] * MAX_W / float(im.size[0]))),
                           Image.LANCZOS)
        # One folder per category, named for it. A hundred and sixty-three files in
        # one directory is a directory nobody can read: the two-letter prefixes that
        # were doing the sorting (ht, gr, yb) are only legible if you already know
        # the categories they stand for.
        d = os.path.join(OUT, cat["slug"])
        if not os.path.isdir(d):
            os.makedirs(d)
        im.save(os.path.join(d, "%s.jpg" % slug), quality=87, optimize=True)
        rows.append((slug, title, blurb, im.size[0], im.size[1]))
        total += 1
    print("  %-13s %2d pieces" % (cat["slug"], len(rows)))
    index.append(dict(slug=cat["slug"], name=cat["name"], kind=cat["kind"],
                      tag=cat["tag"], blurb=cat["blurb"],
                      group=cat.get("group"),
                      cover=cat["cover"],
                      course=cat.get("course"), team=cat.get("team"),
                      lead=cat.get("lead"), pieces=rows))

io.open(os.path.join("content", "art_index.py"), "w", encoding="utf-8").write(
    "# -*- coding: utf-8 -*-\n"
    '"""Written by gen/gallery.py. Do not edit; edit content/art_pieces.py.\n\n'
    'CATEGORIES: list of dicts. `pieces` is (slug, title, blurb, w, h).\n"""\n'
    "CATEGORIES = %r\n" % (index,))
print("%d pieces across %d categories" % (total, len(index)))
