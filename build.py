# -*- coding: utf-8 -*-
"""Build the whole site, in order, and check the result.

    python build.py            everything
    python build.py art        just the Art section (and what it depends on)
    python build.py --pages    skip the artwork, rebuild the HTML only
    python build.py --check    build nothing, just run the checks

Two audits live as pages rather than build steps, because they need a real browser
to measure layout. Serve the site and open them:

    _mobile.html   horizontal overflow, every page, phone to tablet widths
    _resize.html   resizes ONE live page down past the 760 breakpoint and back up

_resize.html is the one that matters for the home page. It is a scaled 1440 canvas,
so its geometry is written by script, and the failure it catches is the layout being
correct on load at any width and wrong the moment the window moves.

WHY THIS EXISTS

Twenty generators, and the order between two of them is load-bearing:
gen-gallery.py writes gallery-index.py, and gen-art-pages.py reads it. Run them the
other way round and you get a silent build of the previous category table. That
happened, more than once, and it does not announce itself -- the pages come out
looking fine and describing the wrong art.

The second thing it fixes is staleness. Renaming a category renames its page, and
the old file just sits there: art-acrylic.html and art-editorial.html both outlived
their categories and stayed linked from nothing, valid HTML serving content that no
longer existed anywhere in the source. Each step declares the files it owns, and
those are cleared before it runs, so a page that stops being generated stops
existing.

VIDEO IS NOT IN HERE. gen-video.py is a twenty-minute ffmpeg run over 1.2GB of
source and its output changes only when a source film does. Run it by hand.
"""
import glob
import os
import re
import subprocess
import sys

# Each step: (name, script, owns, needs).
#   owns  -- glob patterns this step is the only writer of. Cleared before it runs,
#            so nothing it stops emitting can survive as a stale file.
#   needs -- steps that must have run first, for a real data dependency only.
STEPS = [
    # ---- artwork: SVGs and cut images, no HTML ----
    # The two full-bleed grounds. Deliberately first: everything else on the site
    # is toned against them.
    ("grounds",   "gen.grounds",    [], []),
    ("frames",    "gen.frames",     [], []),
    ("botanicals", "gen.botanicals",       [], []),
    ("work",      "gen.work_cards",       [], []),
    ("shots",     "gen.card_shots",      [], []),
    ("figures",   "gen.case_figures", [], []),
    ("archive",   "gen.tiles",    [], []),
    ("dorms",     "gen.tile_dorms",      [], []),
    ("persona",   "gen.persona_art",    [], []),
    ("polaroids", "gen.polaroids",  [], []),
    # Writes gallery-index.py, which the Art pages read. This is THE ordering
    # constraint in the build.
    ("gallery",   "gen.gallery",    [], []),

    # ---- pages ----
    ("cases",     "gen.cases",  ["work/*.html"], []),
    ("projects",  "gen.project_pages",   ["projects/*.html"], []),
    ("about",     "gen.about_page",      ["about.html"], []),
    ("art",       "gen.art_pages",  ["art/*.html"], ["gallery"]),
]

PAGE_STEPS = {"cases", "projects", "about", "art"}


def run(step):
    name, script, owns, _ = step
    for pat in owns:
        for f in glob.glob(pat):
            os.remove(f)
    r = subprocess.run([sys.executable, "-m", script], capture_output=True)
    out = (r.stdout + r.stderr).decode("utf-8", "replace")
    if r.returncode:
        sys.stdout.write(out)
        sys.exit("\nFAILED: python -m %s" % script)
    # One line per step. The generators are chatty and twenty of them at full
    # volume buries the one line that matters.
    tail = [l for l in out.strip().splitlines() if l.strip()]
    print("  %-10s %s" % (name, tail[-1].strip() if tail else "ok"))


# ---------------------------------------------------------------- checks
def check():
    """Every link, anchor and asset resolves, and nothing in assets is unreferenced.

    Cheap, and it catches the two failures this site actually produces: a renamed
    page leaving a dead link behind, and an image that stopped being used but is
    still being cut on every build."""
    # Underscore-prefixed pages are scratch (the background picker, for one) and
    # are gitignored, so they are not part of the site and should not be counted
    # or link-checked.
    pages = sorted(f for f in glob.glob("*.html") + glob.glob("*/*.html")
                   if not os.path.basename(f).startswith("_"))
    ids = {f.replace(os.sep, "/"):
           set(re.findall(r'id="([^"]+)"', open(f, encoding="utf-8").read()))
           for f in pages}
    bad = []
    for f in pages:
        for m in re.findall(r'(?:href|src)="([^"]+)"',
                            open(f, encoding="utf-8").read()):
            if m.startswith(("http", "mailto", "data:", "tel:")) or m == "#":
                continue
            if m.startswith("#"):
                if m[1:] not in ids[f.replace(os.sep, '/')]:
                    bad.append("%s -> %s (no such anchor)" % (f, m))
                continue
            path = m.split("#")[0].split("?")[0]
            # Relative to the PAGE, not to the root: half of these live one folder
            # down and every asset in them is reached through "../".
            here = os.path.normpath(os.path.join(os.path.dirname(f), path)) if path else ""
            if path.endswith("/"):
                here = os.path.join(here, "index.html")
            if here and not os.path.exists(here):
                bad.append("%s -> %s (missing)" % (f, m))
            elif "#" in m and here.endswith(".html"):
                key = here.replace(os.sep, "/")
                if m.split("#")[1] not in ids.get(key, set()):
                    bad.append("%s -> %s (no such anchor)" % (f, m))

    used = set()
    for f in pages + glob.glob("*.css") + glob.glob("*.js"):
        used |= set(re.findall(r"assets/([A-Za-z0-9_./-]+)",
                               open(f, encoding="utf-8").read()))
    have = set()
    for root, _, files in os.walk("assets"):
        for x in files:
            have.add(os.path.relpath(os.path.join(root, x), "assets")
                     .replace(os.sep, "/"))
    # _src is staged input and assets/demo is kept deliberately; see the README.
    orphans = sorted(x for x in (have - used)
                     if "/_src/" not in x and not x.startswith("demo/"))

    print("\n%d pages" % len(pages))
    for b in bad:
        print("  BROKEN  " + b)
    for o in orphans:
        print("  ORPHAN  assets/" + o)
    if not bad and not orphans:
        print("  every link, anchor and asset resolves; no orphans")
    return 1 if bad else 0


def main():
    args = [a for a in sys.argv[1:]]
    if "--check" in args:
        sys.exit(check())
    only = set(a for a in args if not a.startswith("-"))
    pages_only = "--pages" in args

    steps = STEPS
    if only:
        # Pull in whatever the named steps depend on, so `build.py art` cannot
        # produce pages from a stale gallery index.
        want, changed = set(only), True
        while changed:
            changed = False
            for name, _, _, needs in STEPS:
                if name in want and not set(needs) <= want:
                    want |= set(needs)
                    changed = True
        steps = [s for s in STEPS if s[0] in want]
    if pages_only:
        steps = [s for s in steps if s[0] in PAGE_STEPS]

    print("building %d step%s" % (len(steps), "" if len(steps) == 1 else "s"))
    for s in steps:
        run(s)
    sys.exit(check())


if __name__ == "__main__":
    main()
