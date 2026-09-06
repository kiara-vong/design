# -*- coding: utf-8 -*-
"""Builds the case-study pages from one template.

Generated rather than hand-written for the same reason the artwork is: there are
several of them, they share every structural decision, and the moment they become
separate files they start to drift -- one gains a section the others do not, a
heading level slips, the side nav on page three still lists page two's anchors.
This template is the only place any of that is decided.

Section order follows the reference build exactly: Overview, Context, Key
decisions (as a group of sub-sections), Impact. That order is not arbitrary. It
is the problem, then the two or three choices that were actually hard, then what
changed, which is the order a reviewer reads a case study looking for.

CONTENT AND CONFIDENTIALITY: see the note at the top of gen/cases.py.
"""
import io
import os

# The repeating content blocks (stats callout, rules table, before/after ledger,
# screenshot figure) live in case_blocks.py, next to the CSS they are written
# against. This file owns the page shell those blocks get assembled into.
from gen.case_blocks import stats, rules, figure_raw, before_after, ARROW

# The pill, from the one place that owns it.
from gen import nav as _nv


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def sechead(label, h2):
    return ('      <div class="cs-sechead">\n'
            '        <div class="cs-tag"><span class="cs-line"></span>'
            '<span class="cs-seclabel">%s</span></div>\n'
            '        <h2 class="cs-h2">%s</h2>\n'
            '      </div>\n' % (esc(label), esc(h2)))


def body(paras):
    return ('      <div class="cs-body">\n'
            + "".join('        <p>%s</p>\n' % p for p in paras)
            + '      </div>\n')


def figure(src, alt, caption, root=""):
    """A figure whose media is a drawn SVG from the generators."""
    return ('      <figure class="cs-figure">\n'
            '        <div class="cs-media">\n'
            '          <img class="cs-flat" src="%sassets/%s" alt="%s">\n'
            '        </div>\n'
            '        <figcaption class="cs-caption">%s</figcaption>\n'
            '      </figure>\n' % (root, src, esc(alt), esc(caption)))


def _fig(fig):
    """A figure argument is either a (src, alt, caption) tuple for a drawn SVG or
    an already-built block from case_blocks. Accepting both means a section does not
    have to care which kind of illustration it is carrying."""
    return figure(*fig) if isinstance(fig, tuple) else fig


def section(anchor, label, h2, paras, fig=None, extra=None, after=None):
    o = ['    <section id="%s" class="cs-section">\n' % anchor, sechead(label, h2)]
    if extra:
        o.append(extra)              # a block that belongs ABOVE the prose
    o.append(body(paras))
    if fig:
        o.append(_fig(fig))
    if after:
        o.append(after)              # ...and one that belongs below it
    o.append('    </section>\n\n')
    return "".join(o)


def sub(anchor, label, h2, paras, fig=None, first=False, after=None):
    o = ['      <div class="cs-sub" id="%s">\n' % anchor]
    # Only the first sub-section in a group carries the "Key decisions" label.
    # Repeating it above every one turns a group back into three loose sections.
    if first:
        o.append(sechead(label, h2))
    else:
        o.append('        <h2 class="cs-h2">%s</h2>\n' % esc(h2))
    o.append(body(paras))
    if fig:
        o.append(_fig(fig))
    if after:
        o.append(after)
    o.append('      </div>\n\n')
    return "".join(o)


def meta_cols(cols):
    return "".join('          <div class="col"><span class="lbl">%s</span>'
                   '<span class="val">%s</span></div>\n' % (k, v) for k, v in cols)


def nav_links(items):
    return "".join('    <a %shref="#%s">%s</a>\n'
                   % ('class="sub" ' if is_sub else '', href, esc(label))
                   for href, label, is_sub in items)


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} — Kiara Vong</title>
<meta name="description" content="{intro_short}">
<meta name="theme-color" content="#649F25">
<link rel="icon" href="{root}assets/ui/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{root}assets/ui/favicon.svg">
<!-- Critical: painted before site.css arrives, so a cold load does not flash white. -->
<style>html{{background:#FDFBEF}}</style>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{root}site.css">
<script src="{root}site-motion.js"></script>
<link rel="stylesheet" href="{root}case-study.css">
<link rel="stylesheet" href="{root}camera.css">
<style>
/* The reference build's hero hangs 115x250 phone renders in .hero-float. These
   studies are web work, so the hero is one wide plate at the container's own size
   (799x307, from .cs-hero) instead. It stays INSIDE .hero-stage / .hero-float
   because those are what site-motion.js reveals and parallaxes: .js sets
   .hero-float to opacity 0 and only the entrance animation puts it back, so an
   image outside that wrapper never becomes visible at all. Same reason .cs-flat
   sits inside .cs-media rather than replacing it.

   Declared before mobile.css so the responsive sheet still has the last word on
   a phone, which is the ordering rule the whole site follows. */
.cs-hero .hero-float .cs-heroimg{{position:absolute;inset:0;width:100%;height:100%;
  display:block;object-fit:cover}}
.cs-media .cs-flat{{position:absolute;inset:0;width:100%;height:100%;display:block;
  object-fit:cover}}
/* The pill, fixed over the page the way it is on About. A case study is a long
   scroll and the section list on the left only moves within this page; the pill is
   how you get off it.

   --nav-k is the home page's canvas scale, published by site-motion.js, so the
   pill is the same size here as it is on the page you arrived from. Scaled about
   its bottom edge so the 26px gap survives. */
#cs-navwrap{{position:fixed;left:0;bottom:26px;width:100%;z-index:40;
  display:flex;justify-content:center;pointer-events:none}}
#cs-navwrap .nav{{position:static;left:auto;top:auto;pointer-events:auto;
  transform:scale(var(--nav-k,1));transform-origin:bottom center}}
{extra_css}
</style>
<link rel="stylesheet" href="{root}mobile.css">
</head>
<body>
  <a class="cs-back" href="{back}" aria-label="{back_label}">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5"/><path d="M12 19l-7-7 7-7"/></svg>
  </a>
<nav class="cs-nav">
{nav}  </nav>
<div id="cs-navwrap" aria-hidden="false">
{nav_pill}
</div>

<div id="cs-stage">
 <div class="cs-page">

  <main class="cs-main">

    <!-- Overview -->
    <section id="overview" class="cs-overview">
{hero_block}      <div class="cs-head">
        <div class="cs-titleblock">
          <p class="cs-kicker">{kicker}</p>
          <h1 class="cs-title">{title}</h1>
        </div>
        <div class="cs-headgroup">
        <p class="cs-intro">{intro}</p>
        <div class="cs-meta">
{meta}        </div>
        </div>
      </div>
    </section>

{sections}  </main>

  <div id="site-footer"></div>

 </div>
</div>
<div id="bg-footer"></div>

<script src="{root}site-footer.js"></script>
<script src="{root}site-nav.js"></script>
<script src="{root}case-study.js"></script>
<script src="{root}mobile.js"></script>
</body>
</html>
"""


def build(slug, spec):
    # Sections arrive as a sequence of blocks, one per section. Handing that
    # sequence straight to format() renders its repr -- escapes, quotes, tuple
    # parentheses and all -- onto the page. Join it here rather than asking every
    # call site to remember to.
    secs = spec["sections"]
    if not isinstance(secs, str):
        secs = "".join(secs)
    # A hero is either a drawn SVG or a product screenshot, so the spec carries
    # the whole filename; only a bare stem gets .svg assumed for it.
    #
    # A page can also open without a plate at all, and the Art categories do: their
    # cover was the same image the ticket you arrived from had just shown and the
    # first "Selected" figure showed again a screen later, so it was a picture you
    # had already seen twice before you read a word.
    root = spec.get("root", "")
    hero = spec.get("hero")
    hero_block = ""
    if hero:
        if "." not in hero:
            hero += ".svg"
        hero_block = (
            '      <div class="cs-hero">\n'
            '        <div class="hero-stage">\n'
            '          <div class="hero-float">\n'
            '            <img class="cs-heroimg" src="%sassets/%s" alt="%s">\n'
            '          </div>\n'
            '        </div>\n'
            '      </div>\n' % (root, hero, esc(spec.get("hero_alt", ""))))
    # The spec says where the page goes; the folder is created if it is new.
    out = spec.get("out", slug + ".html")
    d = os.path.dirname(out)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    io.open(out, "w", encoding="utf-8").write(PAGE.format(
        title=esc(spec["title"]), kicker=esc(spec["kicker"]),
        intro=esc(spec["intro"]), intro_short=esc(spec["intro"][:150]),
        hero_block=hero_block,
        nav=nav_links(spec["nav"]), meta=meta_cols(spec["meta"]),
        # Three knobs, all defaulted to what a work case study wants. They exist so
        # the Art category pages can be built through this same template instead of
        # a near-copy of it: those pages needed a different back link, a different
        # section lit in the pill, and their own gallery CSS, and nothing else. A
        # parallel template would have drifted from this one within a week.
        extra_css=spec.get("extra_css", ""),
        back=spec.get("back", root + "index.html"),
        back_label=esc(spec.get("back_label", "Back to home")),
        root=root,
        nav_pill=_nv.nav(spec.get("pill", "index"), "  ", root),
        sections=secs))
    print("wrote", out)


# Root-relative, and the pages that use it are one folder down, so it is a function
# of where the page lives rather than a constant.
def note(root=""):
    return ('If you would like the detail, please <a class="touch" '
            'href="%sindex.html">get in touch</a>' % root)


NOTE = note("../")
