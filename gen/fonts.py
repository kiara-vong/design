# -*- coding: utf-8 -*-
"""Cuts the site's own typefaces, and writes the @font-face block that serves them.

WHY THIS EXISTS. The design this site grew out of used five commercial families:
PP Kyoto, ABC Diatype, Apercu Mono, P22 Mackinac and Monument Grotesk. Every one
of them is licensed per-user and none is licensed for redistribution, which is the
part that matters: serving a font file from a public origin IS redistribution, and
no amount of it being "just a portfolio" changes that. Working locally was fine.
Publishing was not.

So the site gets its own set instead. Four families, cut here from open-licensed
sources, named for this site, and served from this repo:

    Giverny   display italic, for the hero line and the case-study titles
    Laurel    headings, section titles, the big numbers in a stats callout
    Clover    body text, everything you actually read a paragraph of
    Thistle   mono, for labels, kickers, captions and small type

WHAT "OWN" MEANS HERE, precisely, because the honest version is more useful than
the flattering one. The outlines are not drawn from scratch: drawing four families
of Latin by hand is a year of somebody's life, and the result would be worse than
what open licensing already offers. What IS this site's own is the cut. Each face
below is instanced at axis values chosen for the exact size it gets used at, then
subset to the glyphs the site actually sets, then named for the role it plays. A
variable font pinned at opsz 144 for a 100px hero and at opsz 32 for a 28px heading
is two genuinely different drawings of the same letters, and that difference is
the whole reason a display face and a text face are not the same file. The Google
CSS API will not hand you those cuts; this does.

Provenance, in full, with the licence shipped next to the fonts in
assets/fonts/OFL-<source>.txt:

    Giverny  <- Instrument Serif    (Instrument, OFL 1.1)
    Laurel   <- Fraunces            (Undercase Type, OFL 1.1)
    Clover   <- Instrument Sans     (Instrument, OFL 1.1)
    Thistle  <- DM Mono             (Colophon Foundry for Google, OFL 1.1)

None of the four carries a Reserved Font Name, so a renamed derivative is exactly
what the licence contemplates. The original copyright line stays in each file's
name table, untouched, which is the one thing the OFL genuinely requires.

WHAT THIS BUYS BEYOND LEGALITY. The old block loaded five OTF files, which browsers
support but which are two to four times the size of the same face as WOFF2, plus a
Google Fonts stylesheet, which is a render-blocking request to a third party before
a single letter can be drawn. This ships eight WOFF2 files from the same origin as
everything else, and the @import goes away.

RUNNING IT. Needs network the first time, to fetch the sources into
assets/fonts/_src (cached and gitignored after that). Then:

    python -m gen.fonts

It rewrites the block in site.css between the two FONTS: sentinels, so the CSS and
the files on disk cannot drift apart.
"""
import io
import os
import re
import sys

from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools import subset

SRC = os.path.join("assets", "fonts", "_src")
OUT = os.path.join("assets", "fonts")
CSS = "site.css"

RAW = "https://raw.githubusercontent.com/google/fonts/main/ofl/%s"

# Sources, as (directory in the google/fonts repo, filename). The bracketed names
# are how that repo stores a variable font: the axes it carries, in its filename.
SOURCES = {
    "instrumentserif-regular": ("instrumentserif", "InstrumentSerif-Regular.ttf"),
    "instrumentserif-italic":  ("instrumentserif", "InstrumentSerif-Italic.ttf"),
    "fraunces":                ("fraunces", "Fraunces[SOFT,WONK,opsz,wght].ttf"),
    "fraunces-italic":         ("fraunces", "Fraunces-Italic[SOFT,WONK,opsz,wght].ttf"),
    "instrumentsans":          ("instrumentsans", "InstrumentSans[wdth,wght].ttf"),
    "dmmono-regular":          ("dmmono", "DMMono-Regular.ttf"),
    "dmmono-medium":           ("dmmono", "DMMono-Medium.ttf"),
}

# The cuts. Each is (family, css weight, css style, source key, pinned axes, file).
#
# The file is named rather than derived, because two CSS weights can legitimately be
# the same drawing. Giverny is one italic used at 300 in some rules and 500 in others,
# and deriving the filename from the weight would put two identical 21KB files on disk
# and make a page that sets both download it twice. Sharing the name gives the browser
# one request and one cache entry, and the @font-face descriptor is what decides which
# CSS weight resolves to it either way.
#
# The axis values are the part worth reading. opsz is an optical size axis: it is
# the type designer's own answer to "what should this letter look like at 100px
# versus at 14px", and it is not a scale. Large optical sizes have finer hairlines,
# tighter spacing and more contrast, because at 100px you can afford detail that
# would fill in and blur at 14px. Small optical sizes are sturdier and wider for
# the opposite reason. Pinning each cut at the size it is actually used at is the
# single biggest quality difference between this and loading one file for everything.
#
# WONK is Fraunces' own name for its quirk axis: it swaps in the slanted, splayed,
# faintly wobbly alternates the family is known for. On at heading sizes, where it
# reads as character and where the page already has hand-drawn flowers in the
# footer. It would be noise at 14px, and no cut here uses Fraunces at 14px.
CUTS = [
    # Giverny. One drawing, used at 100px on About and 42px on a case-study title.
    # Instrument Serif has no weight axis, which is not a limitation for a display
    # face: it is one drawing done well, and the site only ever wanted one. The two
    # weights below are the same file, declared twice, because the CSS asks for 300
    # in one place and 500 in another and it is not worth chasing every call site to
    # say so.
    ("Giverny", 300, "italic", "instrumentserif-italic",  {}, "giverny-italic.woff2"),
    ("Giverny", 500, "italic", "instrumentserif-italic",  {}, "giverny-italic.woff2"),
    ("Giverny", 500, "normal", "instrumentserif-regular", {}, "giverny.woff2"),

    # Laurel. Headings run 18px to 44px, so opsz 32 sits in the middle of the range
    # rather than at either end. SOFT stays at 0: the softened cut is lovely and it
    # is also visibly rounder, which fights the drawn line work rather than joining it.
    ("Laurel", 400, "normal", "fraunces", {"opsz": 32, "wght": 400, "SOFT": 0, "WONK": 1}, "laurel-400.woff2"),
    ("Laurel", 500, "normal", "fraunces", {"opsz": 32, "wght": 500, "SOFT": 0, "WONK": 1}, "laurel-500.woff2"),
    ("Laurel", 700, "normal", "fraunces", {"opsz": 32, "wght": 700, "SOFT": 0, "WONK": 1}, "laurel-700.woff2"),

    # Clover. Body text, so opsz does not apply (Instrument Sans has no optical axis)
    # and wdth stays at its full 100. The bold is a real 700 master interpolation
    # rather than the browser smearing the regular, which is what a missing bold gets
    # you and what the old stack risked every time a licensed file was absent.
    ("Clover", 400, "normal", "instrumentsans", {"wdth": 100, "wght": 400}, "clover-400.woff2"),
    ("Clover", 500, "normal", "instrumentsans", {"wdth": 100, "wght": 500}, "clover-500.woff2"),
    ("Clover", 700, "normal", "instrumentsans", {"wdth": 100, "wght": 700}, "clover-700.woff2"),

    # Thistle. DM Mono ships as static cuts, so there is nothing to pin.
    ("Thistle", 400, "normal", "dmmono-regular", {}, "thistle-400.woff2"),
    ("Thistle", 500, "normal", "dmmono-medium",  {}, "thistle-500.woff2"),
]

# The fallback stack every family falls through to, so that a font file failing to
# arrive degrades the page instead of breaking it. Deliberately generic now: the old
# stacks named Newsreader, Inter and JetBrains Mono, which meant the fallback was
# itself a request to Google, and a fallback that needs the network is not one.
FALLBACK = {
    "Giverny": "Georgia, 'Times New Roman', serif",
    "Laurel":  "Georgia, 'Times New Roman', serif",
    "Clover":  "system-ui, -apple-system, 'Segoe UI', sans-serif",
    "Thistle": "ui-monospace, 'SFMono-Regular', Consolas, monospace",
}

# What to keep. Basic Latin and the Latin-1 letters, plus the punctuation the site
# actually sets: curly quotes, the ellipsis, the middot in every page title, the
# bullet, and the two arrows. Everything outside this is dropped, which is where
# most of the size saving comes from: a full Fraunces master carries Cyrillic and
# Greek this site will never set a word of.
#
# The en dash is here and the em dash is not, on purpose. The site does not use em
# dashes, and a glyph that is never set is a glyph not worth carrying.
KEEP = (
    "U+0020-007E,"          # ASCII
    "U+00A0-00FF,"          # Latin-1: accented letters, the degree sign, the copyright
    "U+0131,U+0152-0153,"   # dotless i and the oe ligature, which OpenType needs
    "U+2018-201A,U+201C-201E,"   # curly quotes, single and double
    "U+2013,U+2026,U+00B7,U+2022,"   # en dash, ellipsis, middot, bullet
    "U+2190,U+2192,"        # the two arrows
    "U+2122,U+20AC,"        # trademark, euro
    "U+FB01-FB02"           # the fi and fl ligatures
)

# Features to keep. kern and the two standard ligature features are the ones that
# change how a line of English looks; the rest of a font's feature list is for
# scripts and typographic modes this site does not use.
FEATURES = ["kern", "liga", "clig", "calt", "ccmp", "locl", "mark", "mkmk",
            "aalt", "salt", "onum", "lnum", "tnum", "frac"]


def fetch(key):
    """Fetch one source into the cache, or use what is already there.

    The cache is gitignored. Committing 2MB of variable-font masters to serve 200KB
    of cuts would be committing the quarry to ship the countertop.
    """
    folder, name = SOURCES[key]
    dst = os.path.join(SRC, name)
    if os.path.exists(dst):
        return dst
    if not os.path.isdir(SRC):
        os.makedirs(SRC)
    try:
        from urllib.request import urlopen, quote
    except ImportError:                      # pragma: no cover
        from urllib2 import urlopen
        from urllib import quote
    url = RAW % (folder + "/" + quote(name))
    print("  fetching %s" % name)
    data = urlopen(url, timeout=60).read()
    with open(dst, "wb") as fh:
        fh.write(data)
    # The licence travels with the font. Shipped next to the WOFF2 files rather
    # than filed away in a docs folder, because the whole point of the OFL's
    # requirement is that the licence is findable from the font.
    lic = os.path.join(OUT, "OFL-%s.txt" % folder)
    if not os.path.exists(lic):
        with open(lic, "wb") as fh:
            fh.write(urlopen(RAW % (folder + "/OFL.txt"), timeout=60).read())
    return dst


def rename(font, family, weight, style, source):
    """Give the cut this site's name for it, and leave the original credit in place.

    Two naming systems live in a font's name table at once. IDs 1 and 2 are the old
    four-style model, where a family may only have Regular, Bold, Italic and Bold
    Italic, so a family with three weights has to lie and call itself three families.
    IDs 16 and 17 are the modern replacement that can say "Laurel, Medium" honestly.
    Both get written: 16/17 for anything that understands them, and 1/2 arranged so
    that software which only reads the old pair still gets a usable answer.

    ID 0, the copyright, is not touched. That is the OFL's actual requirement, and
    it is also just correct: somebody drew these letters and it was not me.
    """
    nt = font["name"]
    italic = style == "italic"
    # The old model can carry exactly one non-Regular weight per family name, so
    # anything that is not 400 gets the weight folded into the ID 1 family. This is
    # the standard workaround and it is why font menus are full of "Foo Medium".
    label = {400: "Regular", 300: "Light", 500: "Medium", 700: "Bold"}[weight]
    if weight == 400:
        legacy_family, legacy_style = family, ("Italic" if italic else "Regular")
    elif weight == 700:
        legacy_family, legacy_style = family, ("Bold Italic" if italic else "Bold")
    else:
        legacy_family = "%s %s" % (family, label)
        legacy_style = "Italic" if italic else "Regular"
    typo_style = label + (" Italic" if italic else "")
    full = "%s %s" % (family, typo_style)
    ps = "%s-%s" % (family, typo_style.replace(" ", ""))

    for nid, value in ((1, legacy_family), (2, legacy_style), (4, full), (6, ps),
                       (16, family), (17, typo_style),
                       (3, "%s; cut for kiaravong.com from %s" % (ps, source)),
                       (5, "Version 1.000"),
                       (13, "Licensed under the SIL Open Font License, Version 1.1. "
                            "This is a modified cut: instanced, subset and renamed. "
                            "See OFL-*.txt beside this file."),
                       (14, "https://scripts.sil.org/OFL")):
        nt.setName(value, nid, 3, 1, 0x409)     # Windows, Unicode BMP, en-US
        nt.setName(value, nid, 1, 0, 0)         # Macintosh, Roman, English
    # Names 21 and 22 are the WWS pair, which only mean anything when the typographic
    # family in 16 is itself a subfamily of something wider. Nothing here is, and a
    # stale pair left over from the source would contradict 16/17.
    for nid in (21, 22):
        nt.removeNames(nid)

    # The bits, which are what actually decides whether a browser thinks it needs to
    # synthesise an oblique or a fake bold. Getting these wrong is how a page ends up
    # with a slanted upright sitting next to a real italic and nobody able to say why.
    os2 = font["OS/2"]
    os2.usWeightClass = weight
    os2.fsSelection = (os2.fsSelection & ~0b1100001) | (
        0b0000001 if italic else (0b0100000 if weight == 700 else 0b1000000))
    head = font["head"]
    head.macStyle = (head.macStyle & ~0b11) | (0b10 if italic else 0) | (
        0b01 if weight == 700 else 0)


def cut(family, weight, style, key, axes, name):
    font = TTFont(fetch(key))
    if axes:
        # Pinning every axis to a single value turns a variable font into a static
        # one: fvar goes away, the deltas are baked into the outlines, and what is
        # left is one drawing rather than a range of them.
        font = instancer.instantiateVariableFont(font, axes, inplace=True,
                                                 updateFontNames=False)
    rename(font, family, weight, style, SOURCES[key][1])

    opts = subset.Options()
    opts.layout_features = FEATURES
    opts.name_IDs = ["*"]           # keep the name table we just wrote
    opts.name_legacy = True
    opts.notdef_outline = True
    opts.recalc_bounds = True
    opts.drop_tables += ["DSIG"]    # a signature is invalid the moment we subset
    sub = subset.Subsetter(options=opts)
    sub.populate(unicodes=subset.parse_unicodes(KEEP))
    sub.subset(font)

    font.flavor = "woff2"
    dst = os.path.join(OUT, name)
    font.save(dst)
    font.close()
    return os.path.getsize(dst)


def block():
    """The @font-face rules, generated from the same table the files come from.

    font-display is swap everywhere. The alternative, block, hides the text until
    the font arrives, and on a page whose first screen is a 100px line of display
    italic that is the difference between a slow load and an empty one.
    """
    o = ["/* FONTS:BEGIN generated by gen/fonts.py -- do not edit by hand.\n"
         "   Four families cut for this site from open-licensed sources, with the\n"
         "   licence in assets/fonts/OFL-*.txt and the full reasoning in gen/fonts.py.\n"
         "\n"
         "     Giverny  <- Instrument Serif   display italic\n"
         "     Laurel   <- Fraunces           headings\n"
         "     Clover   <- Instrument Sans    body\n"
         "     Thistle  <- DM Mono            labels and captions\n"
         "\n"
         "   Same origin as the rest of the site, so there is no third-party request\n"
         "   in front of the first painted letter. */\n"]
    for family, weight, style, key, axes, name in CUTS:
        o.append("@font-face {\n"
                 "   font-family: '%s';\n"
                 "   src: url('assets/fonts/%s') format('woff2');\n"
                 "   font-weight: %d;\n"
                 "   font-style: %s;\n"
                 "   font-display: swap\n"
                 "}\n\n" % (family, name, weight, style))
    o.append("/* FONTS:END */")
    return "".join(o)


def write_css():
    """Replace the block between the sentinels, or install it if it is not there yet."""
    text = io.open(CSS, encoding="utf-8").read()
    new = block()
    if "/* FONTS:BEGIN" in text:
        text = re.sub(r"/\* FONTS:BEGIN.*?/\* FONTS:END \*/", lambda m: new,
                      text, flags=re.S)
    else:
        raise SystemExit("no FONTS: sentinels in %s; add them once by hand" % CSS)
    io.open(CSS, "w", encoding="utf-8").write(text)
    print("  updated the @font-face block in %s" % CSS)


def main():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    total, done = 0, {}
    for family, weight, style, key, axes, name in CUTS:
        if name in done:
            # A second CSS weight pointing at a drawing already cut. The names inside
            # the file were written for the first of the two; nothing reads them at
            # render time, and the alternative is two copies of the same outlines.
            print("  %-22s %6s     shared with %d" % (name, "", done[name]))
            continue
        size = cut(family, weight, style, key, axes, name)
        done[name] = weight
        total += size
        print("  %-22s %6.1fKB   %s" % (name, size / 1024.0, SOURCES[key][1]))
    print("%d files, %d faces, %.1fKB total"
          % (len(done), len(CUTS), total / 1024.0))
    write_css()


if __name__ == "__main__":
    sys.exit(main())
