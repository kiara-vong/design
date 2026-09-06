# -*- coding: utf-8 -*-
"""The Art section: a ticket index of categories, then a page for each.

The Art page used to be one very long wall of every piece in the archive. At a
hundred and one pieces that stopped working: nothing could be featured, the
project work sat in the same rhythm as the sketchbook pages, and the five things
with actual reports behind them were indistinguishable from a page of fruit
studies.

So it splits in two:

  art.html          An index. One perforated ticket per category, in the same
                    idiom as the work cards on the home page. Projects first and
                    larger, studio work after.
  art-<slug>.html   The category. A salon hang of everything in it, with mixed
                    framing and wall labels always up.

The five project categories get a written page on top of the hang: context,
method, the named results with what the report says about them, then the full
set. Three of them are TEAM projects and their pages credit the team by name --
a lab report with four contributors on the cover is not a solo portfolio piece,
and presenting it as one is exactly the sort of thing that comes apart when
somebody asks about it.

The nav pill sits at the BOTTOM here, as it does on every other page. The earlier
version of this page put it at the top, which made the Art section the only place
on the site where the menu moved.
"""
import io
import os

from gen import nav as _nav
from gen import case_template as _cs
from content.art_index import CATEGORIES as CATS


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


COLOR = {
    # One feature colour per category, spread across the seven so no two adjacent
    # tickets on the index share one. All seven are the same lightness, so this is a
    # question of hue only.
    "water-drop": "var(--ink-blue)",   "smoke": "var(--feat-leaf)",
    "rheoscopic": "var(--feat-sage)",  "sandsketch": "var(--feat-moss)",
    "films": "var(--feat-bright)",
    "canvas": "var(--feat-leaf)",      "pens": "var(--feat-lime)",
    "sketches": "var(--feat-bright)",  "hatch": "var(--slate)",
    "still-life": "var(--feat-sage)",
    "football": "var(--feat-leaf)",    "cheer": "var(--feat-fern)",
    "powderpuff": "var(--feat-moss)", "swim": "var(--feat-pine)",
    "nature": "var(--feat-lime)",
    "fantasy": "var(--feat-sage)",     "flashcards": "var(--feat-bright)",
    "graphics": "var(--slate)",        "yearbook": "var(--feat-fern)",
}


# =====================================================================
# Shared shell
# =====================================================================
SHELL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>__TITLE__</title>
<meta name="description" content="__DESC__">
<link rel="icon" href="../assets/ui/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="../assets/ui/favicon.svg">
<meta name="theme-color" content="#649F25">
<style>html{background:#FDFBEF}</style>
<link rel="stylesheet" href="../site.css">
<script src="../site-motion.js"></script>
<style>
/* ---- the pill, at the bottom ----
   .nav's base rule hardcodes an absolute position meant for the 1440 canvas it
   normally lives inside, so both the wrapper AND the nav need cancelling on a
   page that is a normal flowing document. Anchored to the bottom because that is
   where it sits on every other page; an earlier version of the Art page put it at
   the top and it was the only place on the site where the menu moved.

   --nav-k is the home page's own canvas scale, published by site-motion.js. The
   pill is authored at 1440 size and the home and About pages shrink it with their
   hero; left at 1:1 here it read as a different, larger menu on half the site.
   Scaled from the bottom edge so the 26px gap holds however it is scaled. */
#pg-navwrap{position:fixed;left:0;bottom:26px;width:100%;z-index:40;
  display:flex;justify-content:center;pointer-events:none}
#pg-navwrap .nav{position:static;left:auto;top:auto;pointer-events:auto;
  transform:scale(var(--nav-k,1));transform-origin:bottom center}
/* The back arrow sits over the painted band at the top and over parchment once you
   scroll past it, so it cannot have one colour. It starts light, which is what it
   needs against a painting, and site-nav.js adds .on-light when the band's bottom
   passes it. Same mechanism the pill already uses, and the same class name. */
.ap-back{position:fixed;left:32px;top:28px;width:28px;height:28px;z-index:40;
  color:var(--parchment);opacity:.85;
  filter:drop-shadow(0 1px 3px rgba(20,26,20,.45));
  transition:color .25s ease,opacity .25s ease,filter .25s ease}
.ap-back.on-light{color:var(--dusty-granite);opacity:.5;filter:none}
.ap-back:hover{opacity:1}
.ap-back svg{display:block;width:28px;height:28px}
/* site.css sets a blanket section{width:1440px} for the scaled-canvas pages. */
body.ap section{position:relative;width:auto}
__CSS__
</style>
<link rel="stylesheet" href="../mobile.css">
</head>
<body class="ap">

<div id="pg-navwrap" aria-hidden="false">
__NAV__
</div>

<a class="ap-back" href="__BACK__" aria-label="__BACKLABEL__">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5"/><path d="M12 19l-7-7 7-7"/></svg>
</a>

__CONTENT__

<div id="site-footer" data-flowers="foot-art.png"></div>

<script src="../site-footer.js"></script>
<script src="../site-nav.js"></script>
<script src="../mobile.js"></script>
</body>
</html>
"""


def shell(out, title, desc, css, content, back="index.html",
          backlabel="Back to the index", root=""):
    d = os.path.dirname(out)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    io.open(out, "w", encoding="utf-8").write(
        SHELL.replace("../", root)
             .replace("__TITLE__", esc(title))
             .replace("__DESC__", esc(desc))
             .replace("__CSS__", css)
             .replace("__NAV__", _nav.nav("art", "  ", root))
             .replace("__BACK__", back)
             .replace("__BACKLABEL__", backlabel)
             .replace("__CONTENT__", content))
    print("  %s" % out)


# =====================================================================
# art.html -- the ticket index
# =====================================================================
CSS_INDEX = """
/* Gutters, matched to About rather than guessed. That page is a 1440 canvas with
   57px of ground either side of a 1326 content block, so its gutter is 3.96% of
   the width; --ai-gut reproduces that proportionally and then stops growing, so a
   wide monitor gets air rather than an ever-widening margin. The floor keeps a
   phone off the edge. */
.ai-shell{--ai-gut:clamp(22px,3.96vw,64px);
  max-width:1368px;margin:0 auto;padding:0 var(--ai-gut) 120px}

/* The title sits on the painted ground the home page and About both open on. It is
   the same file About uses, so the three pages share one surface instead of three
   near-misses, and the section reads as the top of a page rather than as a heading
   that happens to be first.

   Full-bleed: the band ignores the shell's gutter and runs edge to edge, with the
   type inset by that gutter from within. A painted ground that stops short of the
   window looks like a photograph of a painted ground. */
.ai-hero{position:relative;margin:0 calc(var(--ai-gut) * -1) 0;
  background:url("../assets/hero/art-bg.webp") 50% 50% / cover no-repeat,#7A5633;
  /* As tall as the home page's, which is the whole viewport less a little, so the
     ground is something you are standing in rather than a strip you scroll past.
     min-height rather than height: the type sets the floor on a short window and
     the band grows past it on a tall one. */
  min-height:min(78vh,760px);box-sizing:border-box;
  display:flex;flex-direction:column;justify-content:flex-end;
  /* Square bottom, deliberately, where the home page's hero is rounded. The hero
     is a photograph behind a whole viewport of content and the curve reads as that
     panel ending; this is a shorter band under a page of tickets, and any radius on
     it read as a rounded box sitting on the parchment rather than as ground. */
  padding:120px var(--ai-gut) 92px;overflow:hidden}
/* The painting is a CSS background rather than an <img>, which is the one place
   this differs from About. As an absolutely-positioned <img> inside an
   overflow:hidden, border-radiused flex box it reported itself as loaded, visible
   and correctly sized, and then rasterised as nothing -- measured, not guessed: the
   band came back as the ::after wash over bare parchment while the same file
   painted normally on About. A background has no such box to lose.

   Its own ground rather than About's. The Art index and the About page were sharing
   one image, which was fine when both were an abstract wash and wrong once they
   became paintings: two pages opening on the same picture reads as a template.
   art-bg.webp is cut for this band's shape in gen/grounds.py, so it is centred here
   rather than anchored low. */
/* A wash over the painting. The ground is a mid-value brown and the type is set in
   parchment; without this the lightest passages come up under the lede and take
   the contrast with them. */
.ai-hero::after{content:"";position:absolute;inset:0;z-index:1;
  background:linear-gradient(105deg,rgba(38,28,18,.62),rgba(38,28,18,.24) 62%,
    rgba(38,28,18,.50))}
.ai-head{position:relative;z-index:2;max-width:760px}
.ai-kicker{font-family:'ApercuMono','JetBrains Mono',ui-monospace,monospace;font-weight:500;
  font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#F5C9A8}
.ai-title{margin-top:14px;font-family:'Kyoto','Newsreader',Georgia,serif;font-weight:500;
  font-style:italic;font-size:74px;line-height:.98;color:var(--parchment)}
.ai-intro{margin-top:20px;font-family:'Diatype','Inter',system-ui,sans-serif;font-weight:400;
  font-size:17px;line-height:1.65;color:rgba(253,251,239,.86)}
.ai-count{margin-top:16px;font-family:'ApercuMono','JetBrains Mono',ui-monospace,monospace;
  font-weight:500;font-size:13px;color:#E2F085}

.ai-sec{margin-top:66px}
.ai-sechead{display:flex;align-items:baseline;gap:16px;margin-bottom:32px}
.ai-sechead h2{font-family:'Mackinac','Fraunces',Georgia,serif;font-weight:500;font-size:24px;
  color:var(--dusty-granite);white-space:nowrap}
.ai-sechead .n{font-family:'ApercuMono','JetBrains Mono',ui-monospace,monospace;font-size:13px;
  color:var(--antique-gold);white-space:nowrap}
.ai-sechead .dots{flex:1;overflow:hidden;font-family:'Newsreader',serif;font-style:italic;
  font-weight:300;font-size:13px;color:var(--outline-stroke);white-space:nowrap;letter-spacing:1px}

.ai-sub{display:flex;align-items:baseline;gap:14px;margin:44px 0 22px}
.ai-sub:first-of-type{margin-top:0}
.ai-sub h3{font-family:'Mackinac','Fraunces',Georgia,serif;font-weight:500;font-size:17px;
  color:var(--dusty-granite);white-space:nowrap}
.ai-sub .n{font-family:'ApercuMono','JetBrains Mono',ui-monospace,monospace;font-size:11px;
  letter-spacing:.1em;color:var(--antique-gold);white-space:nowrap}
.ai-sub .rule{flex:1;height:1px;background:linear-gradient(90deg,
  rgba(120,105,85,.30),rgba(120,105,85,0))}

/* auto-fill rather than a fixed column count, so the grid reflows continuously
   instead of at breakpoints. Fixed counts overflowed in the gap between the mobile
   breakpoint and the desktop layout: at 768px a hard 3-column studio grid could not
   fit its own tickets and the page scrolled sideways.

   The minmax floor is the real number here. It is the narrowest a ticket can be and
   still hold its serial, its kind and two tag chips on one line. */
.ai-grid{display:grid;gap:34px 30px}
/* A grid item defaults to min-width:auto, which floors its track at the item's own
   min-content width. The perforation row is a long unbroken run of bullets with
   white-space:nowrap, so that floor was 396px and the project tickets stayed 396
   wide at every phone size, hanging off a 335px column and getting clipped. The
   document never overflowed, which is why the overflow audit never saw it.

   overflow:hidden on .ai-perf is not enough on its own; the item has to be allowed
   to shrink past its content in the first place. */
.ai-grid > *{min-width:0}
.ai-grid.big{grid-template-columns:repeat(auto-fill,minmax(min(100%,340px),1fr))}
.ai-grid.small{grid-template-columns:repeat(auto-fill,minmax(min(100%,228px),1fr))}

/* The ticket. Same stretchable sawtooth frame the mobile work cards use, so the
   edge profile is identical to the index's tickets rather than a near-match. */
.ai-ticket{position:relative;display:block;padding:26px 24px 22px;text-decoration:none;
  color:inherit;background:url("../assets/ui/card-ticket-mobile.svg") 0 0 / 100% 100% no-repeat;
  transform-origin:50% 100%;
  transition:transform .35s cubic-bezier(.34,1.3,.5,1),filter .35s ease}
.ai-ticket:hover{transform:translateY(-8px) rotate(-1.2deg);
  filter:drop-shadow(0 16px 26px rgba(52,46,42,.20))}
.ai-ticket:nth-child(even):hover{transform:translateY(-8px) rotate(1.2deg)}
.ai-top{display:flex;align-items:baseline;justify-content:space-between;gap:12px}
.ai-serial{font-family:'ApercuMono','JetBrains Mono',ui-monospace,monospace;font-weight:500;
  font-size:14px;color:var(--accent)}
.ai-kind{font-family:'ApercuMono','JetBrains Mono',ui-monospace,monospace;font-weight:500;
  font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--sw)}
.ai-win{margin-top:12px;border-radius:7px;overflow:hidden;background:var(--dove-ivory);
  border:1px solid var(--outline-stroke)}
.ai-grid.big .ai-win{aspect-ratio:16/10}
.ai-grid.small .ai-win{aspect-ratio:4/3}
.ai-win img{display:block;width:100%;height:100%;object-fit:cover;
  transition:transform .5s cubic-bezier(.4,0,.2,1)}
.ai-ticket:hover .ai-win img{transform:scale(1.045)}
.ai-perf{margin:16px -8px 14px;font-family:'Newsreader',serif;font-style:italic;
  font-weight:300;font-size:12px;line-height:1;color:var(--antique-gold);
  white-space:nowrap;overflow:hidden;letter-spacing:1px}
.ai-stub{display:flex;align-items:flex-start;gap:14px}
.ai-admit{font-family:'ApercuMono','JetBrains Mono',ui-monospace,monospace;font-weight:500;
  font-size:9.5px;letter-spacing:.16em;color:var(--sw);writing-mode:vertical-rl;
  transform:rotate(180deg);flex:none;padding-top:2px}
.ai-meta{flex:1;min-width:0}
.ai-name{font-family:'Mackinac','Fraunces',Georgia,serif;font-weight:500;line-height:1.24;
  color:var(--dusty-granite)}
.ai-grid.big .ai-name{font-size:26px}
.ai-grid.small .ai-name{font-size:19px}
.ai-note{margin-top:8px;font-family:'Diatype','Inter',system-ui,sans-serif;font-weight:400;
  font-size:14px;line-height:1.55;color:var(--muted)}
.ai-tags{margin-top:12px;display:flex;flex-wrap:wrap;gap:7px}
.ai-tag{background:var(--cream);border:1px solid var(--outline-stroke);border-radius:10px;
  padding:5px 10px;font-family:'ApercuMono','JetBrains Mono',ui-monospace,monospace;
  font-weight:500;font-size:11px;color:var(--sw)}
.ai-tag.mut{color:var(--muted)}
@media (prefers-reduced-motion:reduce){
  .ai-ticket,.ai-win img{transition:none}
  .ai-ticket:hover{transform:none}
}
@media (max-width:1080px){.ai-grid.small{grid-template-columns:repeat(2,1fr)}}
@media (max-width:760px){
  /* The pill STAYS a fixed bar at the bottom, as it is on every other page and at
     every other width. It used to go position:static here, and because #pg-navwrap is
     the first element in <body> that dropped it into the flow at the very top of the
     page, at its full 1440-canvas width. That is the "jumps to the top and resizes
     weirdly" -- it was two bugs wearing one coat.

     Scaled to .84 about its bottom edge, which is what mobile.css does for the other
     two wrappers, so all three bars are the same size on a phone. */
  #pg-navwrap{position:fixed;left:0;right:0;bottom:0;top:auto;
    width:100%;height:auto;margin:0;transform:none;z-index:60}
  #pg-navwrap .nav{transform:scale(var(--nav-k,.84));transform-origin:bottom center;
    margin-bottom:24px;width:max-content}
  /* The arrow leaves the corner and joins the flow, since a fixed arrow over a
     full-bleed band on a 375px screen sits on the title. */
  /* The arrow stays OVER the band on a phone rather than sitting above it.
  
     Dropping it into the flow was giving it 16px of margin and 28px of height, and
     with the shell's own 24px of padding that was 68px of bare parchment above the
     painting: a white bar across the top of the one page whose whole opening move is
     a full-bleed painted ground. About does not have it, because its ground starts
     at the top of the document and the arrow sits on top of the ground.
  
     So the arrow goes back to being fixed, the shell loses its top padding, and the
     band takes that space as its own padding instead, which keeps the type clear of
     the arrow without putting anything above the picture. */
  .ap-back{position:fixed;left:16px;top:14px;margin:0}
  .ai-shell{padding:0 20px 96px}         /* 96 is room for the fixed bar */
  .ai-hero{min-height:auto;padding:84px 20px 44px}
  .ai-title{font-size:44px}
  .ai-grid.big,.ai-grid.small{grid-template-columns:1fr}
  .ai-intro{font-size:15.5px}
}
"""


def ticket(cat, serial, big):
    sw = COLOR.get(cat["slug"], "var(--accent)")
    kind = "Project" if cat["kind"] == "project" else "Studio"
    # No dates on the tickets. A range like "2019-2024" on a studio category was
    # doing nothing except inviting arithmetic about how long ago the early work was.
    pr = PROSE.get(cat["slug"]) or {}
    if pr.get("videos"):
        count = "%d films" % len(pr["videos"])
    elif pr.get("hang", True) is False:
        # No hang, so the ticket must not advertise a gallery. It says what the page
        # is instead of counting images the page never shows.
        count = "Project"
    else:
        count = "%d pieces" % len(cat["pieces"])
    tags = ['<span class="ai-tag">%s</span>' % esc(cat["tag"]),
            '<span class="ai-tag mut">%s</span>' % esc(count)]
    return ('    <a class="ai-ticket" href="%s/" style="--sw:%s">\n'
            '      <div class="ai-top"><span class="ai-serial">No. %02d</span>'
            '<span class="ai-kind">%s</span></div>\n'
            '      <div class="ai-win"><img src="../assets/art/%s/%s.jpg" alt="%s" loading="lazy"></div>\n'
            '      <p class="ai-perf">%s</p>\n'
            '      <div class="ai-stub">\n'
            '        <span class="ai-admit">ADMIT ONE</span>\n'
            '        <div class="ai-meta">\n'
            '          <p class="ai-name">%s</p>\n'
            '          <p class="ai-note">%s</p>\n'
            '          <div class="ai-tags">%s</div>\n'
            '        </div>\n'
            '      </div>\n'
            '    </a>\n'
            % (cat["slug"], sw, serial, kind, cat["slug"], cat["cover"],
               esc(cat["name"]),
               "&bull;" * (70 if big else 54), esc(cat["name"]), esc(cat["blurb"]),
               "".join(tags)))


# The order her own filter chips are in, not alphabetical.
GROUPS = ["Drawing", "Painting", "Photography", "Design"]


def build_index():
    projects = [c for c in CATS if c["kind"] == "project"]
    studio = [c for c in CATS if c["kind"] != "project"]
    total = sum(len(c["pieces"]) for c in CATS)
    o = ['<div class="ai-shell">\n',
         '  <div class="ai-hero">\n',
         '    <div class="ai-head">\n',
         '      <p class="ai-kicker">Admit one</p>\n',
         '      <h1 class="ai-title">Art</h1>\n',
         '      <p class="ai-intro">Paint, ink, a camera, four years of a high school\n'
         '      yearbook, and five projects where the art was the point of the\n'
         '      engineering. Each ticket opens a room.</p>\n',
         '      <p class="ai-count">%d pieces &middot; %d categories</p>\n' % (total, len(CATS)),
         '    </div>\n  </div>\n\n',
         '  <section class="ai-sec">\n',
         '    <div class="ai-sechead"><h2>Projects</h2>'
         '<span class="n">%02d</span><span class="dots">%s</span></div>\n'
         % (len(projects), "&bull;" * 90),
         '    <div class="ai-grid big">\n']
    n = 0
    for c in projects:
        n += 1
        o.append(ticket(c, n, True))
    o.append('    </div>\n  </section>\n\n')

    # Studio splits four ways, and the split is hers: art/art.js on the old site
    # filters these same folders by Drawing / Painting / Photography / Design. It
    # matters most for Photography, which is eight of the fourteen -- ungrouped,
    # the sports ran into the plumeria and the whole second half read as one
    # undifferentiated block of tickets.
    o.append('  <section class="ai-sec">\n')
    o.append('    <div class="ai-sechead"><h2>Studio</h2>'
             '<span class="n">%02d</span><span class="dots">%s</span></div>\n'
             % (len(studio), "&bull;" * 90))
    for grp in GROUPS:
        rows = [c for c in studio if c.get("group") == grp]
        if not rows:
            continue
        o.append('    <div class="ai-sub"><h3>%s</h3><span class="n">%02d</span>'
                 '<span class="rule"></span></div>\n' % (esc(grp), len(rows)))
        o.append('    <div class="ai-grid small">\n')
        for c in rows:
            n += 1
            o.append(ticket(c, n, False))
        o.append('    </div>\n')
    o.append('  </section>\n</div>\n')
    shell("art/index.html", "Art · Kiara Vong",
          "Paintings, drawings, photography, editorial design and fluid-mechanics "
          "project work by Kiara Vong.",
          CSS_INDEX, "".join(o), back="../",
          backlabel="Back to the index", root="../")


# =====================================================================
# art-<slug>.html -- the category page
# =====================================================================
PROSE = {
 "water-drop": dict(
   picks=["dark-matter", "mycology", "cerulean"],
   sections=[
     ("Context", [
       "A Worthington-Edgerton splash is a single droplet hitting still liquid, "
       "photographed at the instant the crown forms. The whole event is over in a "
       "few milliseconds, which means there is no version of it you can see with "
       "your eyes and no version you can catch by reacting to it.",
       "The camera does not freeze it either. A shutter is far too slow. What "
       "freezes it is the flash: the room is dark, the shutter is already open, "
       "and the only light in the entire exposure is one burst a few hundred "
       "microseconds wide."]),
     ("Method", [
       "An Arduino holds the timing. It pulses a peristaltic pump to release a "
       "drop, waits a set delay, then fires the flash, and the shutter closes "
       "around it. Change that delay and you get a different moment in the same "
       "event: the impact, the crater, the jet rising back out of it, the crown, "
       "or a second drop landing on the jet before it falls.",
       "Everything else was varied by hand between shots: fluid mixture, surface, "
       "backdrop, colour. Glow-stick fluid, glycerol, water, cream. The "
       "viscoelastic mixtures are the ones that produce filaments, which is why "
       "several of these have visible threads connecting the fragments."]),
   ]),
 "smoke": dict(
   picks=["ring-of-fire", "inferno", "chains"],
   sections=[
     ("Context", [
       "A vortex ring is a torus of rotating fluid. Its inner edge travels faster "
       "than its outer edge, and that difference is what sustains the rotation and "
       "carries the whole ring forward through still air.",
       "Every laminar flow is unstable eventually. Past a critical Reynolds number "
       "the viscous forces stop holding against the flow's own inertia, the ring "
       "loses coherence, and the motion turns turbulent. The photographs worth "
       "keeping are almost all at that transition, because a fully stable ring is "
       "just a smoke ring and a fully broken one is just a cloud."]),
     ("Method", [
       "A box with one flexible face and a plexiglass orifice, filled from a smoke "
       "machine. Striking the flexible face ejects a ring. Lighting is a flood or "
       "a laser sheet against black, which is what lets the internal structure "
       "survive the exposure rather than reading as one flat silhouette.",
       "The orifice shape was the main variable. It sets how the ring forms and "
       "how soon it destabilises, so most of the range across these images comes "
       "from changing that rather than from changing the light."]),
   ]),
 "rheoscopic": dict(
   # All eight figures, since with no hang this section IS the page.
   picks=["rh-final", "rh-detail", "rh-gears", "rh-cad", "rh-cad2", "rh-flow",
          "rh-flow2", "rh-bench"],
   sections=[
     ("Context", [
       "Rheoscopic fluid is water with microscopic mica flakes suspended in it. "
       "The flakes are flat and reflective and they orient along the flow "
       "direction, the way logs do going down a river, so internal currents become "
       "visible without introducing any dye or tracer.",
       "The brief was a lasting, self-sustaining piece, after Paul Matisse's "
       "Kalliroscope. Rather than photograph a flow once, build something that "
       "keeps producing one."]),
     ("Method", [
       "Rheoscopic fluid sealed into rotating cylinders, driven by a 3D-printed "
       "gear train. CAD first, then printing, then tuning the gear ratio against "
       "the flow it produced, since the rotation rate is what decides whether what "
       "you see reads as laminar or as turbulent.",
       "The no-slip boundary condition is the actual subject. Fluid touching the "
       "wall moves with the wall, fluid at the centre lags behind, and the shear "
       "between the two is what the flakes draw for you. The patterns it settles "
       "into look a great deal like the banding in the atmosphere of a gas giant, "
       "for the same reason."]),
   ],
   # No hang. The figures on this page are CAD, a gear housing and two flow studies
   # -- documentation of one object, not a set of works, and presenting eight of
   # them as a salon wall claimed a body of work that does not exist.
   hang=False),
 "sandsketch": dict(
   picks=["ss-3", "ss-1", "ss-4"],
   # The count in the credit strip should say what the page holds, and for these two
   # that is figures from a report rather than pieces of art.
   noun="figures",
   sections=[
     ("Context", [
       "A robo-zen garden: a quadrotor carrying a pencil attachment, drawing "
       "geometric patterns into a table of sand from the air. The piece is "
       "impermanent by design, since the next pass erases the last one.",
       "My part of the team was the pattern code: working out trajectories that go "
       "beyond parametric curves while still being something a drone can actually "
       "fly and the medium can actually hold."]),
     ("Method", [
       "A sand table lit from beneath through tempered glass, a CAD nib "
       "attachment, and a guard around it to stop rotor downwash erasing the line "
       "as fast as it is drawn. Downwash shaped everything: it sets how long the "
       "nib has to be, which sets the payload, which sets the flight time.",
       "The other constraint is that intricate patterns need slow movement, and "
       "slow movement costs battery. How complex a pattern can get is therefore a "
       "flight-time question rather than a code question, which is not the "
       "trade-off any of us expected going in."]),
   ],
   # The hang went in favour of the run itself. Five stills of a drone over a sand
   # table describe the rig; they cannot show the thing the project is actually
   # about, which is whether the line survives the downwash while it is being drawn.
   hang=False,
   film=dict(src="sandsketch", poster="ss-3", dur="6:58",
             title="The full run",
             cap="One uninterrupted pass, from an empty table to a finished pattern. "
                 "The nib guard and the flight time are both easier to see here than "
                 "in any still: the line has to be laid faster than the downwash can "
                 "sweep it away, and the battery decides how intricate the pattern "
                 "is allowed to get."),
 ),
 "films": dict(
   picks=["fm-goose-1", "fm-grocery-1", "fm-torah-1"],
   # Films, so the selections ARE the films. A screenshot of a short film is a
   # still of somebody else's decision about where to pause it, and cut rhythm --
   # which is what carries all three of these -- is the one thing a frame cannot
   # show. The hang went for the same reason: it was six frames from three films.
   hang=False,
   videos={"fm-goose-1": ("fm-goose", "0:50"),
           "fm-grocery-1": ("fm-grocery", "0:18"),
           "fm-torah-1": ("fm-torah", "4:05")},
   sections=[
     ("Context", [
       "Three short films shot and cut entirely on a phone. No rig, no second "
       "unit, no colourist, and in most cases no second take.",
       "The constraint is the point. A phone is always the camera you have, which "
       "leaves only three real decisions: where to stand, when to start, and when "
       "to cut. Everything a bigger production would solve with equipment has to "
       "be solved with those instead."]),
   ]),
}


# ============================================================================
# art-<slug>.html -- built on the case-study chassis
#
# These pages used to have a layout of their own: their own headings, their own
# type sizes, their own idea of what a section looked like. They were the only
# written pages on the site that were not case studies, and they read as somebody
# else's pages.
#
# So they are now built through gen-cases.py's own template. That is not a shared
# stylesheet, it is the same file: the fixed section rail, .cs-sechead with its
# green tick and gold label, .cs-h2, .cs-body's measure and leading, the scaled
# 1440 stage, the pill, the scroll-spy -- all of it arrives because these pages
# ARE case studies as far as that template is concerned. Only three things differ
# and all three are passed in: the back link goes to art.html, the pill lights Art
# rather than Work, and the CSS below adds the gallery vocabulary the work studies
# have no use for.
#
# What is left here is only what a case study genuinely does not have: a hang, a
# video plate, and a natural-aspect figure. A case study's .cs-media is a fixed
# 391px window because every figure in one is a screenshot at a known size. A
# painting is whatever shape the painting is.
# ============================================================================
CSS_CAT = """
/* A figure that keeps its own proportions. Everything else about it -- the gap to
   its caption, the caption's face and colour -- is .cs-figure and .cs-caption,
   unchanged. */
.ac-plate img,.ac-plate video{display:block;width:100%;height:auto;border-radius:12px;
  border:1px solid var(--outline-stroke)}
.ac-plate video{background:#26221F;border-color:transparent}
/* .cs-caption is centred, which is right for a work study where every caption is
   one short line under a screenshot. These run to three lines describing a piece,
   and centred ragged type at that length is genuinely harder to read -- so left,
   on a measure, with real leading. */
.ac-plate .cs-caption{text-align:left;max-width:660px;line-height:1.65}
.cs-caption .t{font-family:'Mackinac','Fraunces',Georgia,serif;font-weight:500;
  font-size:17px;color:var(--dusty-granite)}
.cs-caption .d{color:var(--antique-gold)}
/* controls, but no autoplay and no loop: these have sound and a running time, and
   a portfolio that starts making noise at you is a portfolio you close. */
.ac-plate .runs{font-family:'ApercuMono','JetBrains Mono',ui-monospace,monospace;
  color:var(--antique-gold)}

/* Where a piece has been published, that goes on the piece. It is the one claim on
   these pages that an outside party has already made for her. */
.ac-award{display:inline-flex;align-items:center;gap:7px;margin-top:10px;
  padding:5px 11px 5px 9px;border-radius:999px;
  background:rgba(226,240,133,.34);border:1px solid rgba(140,150,70,.42);
  font-family:'ApercuMono','JetBrains Mono',ui-monospace,monospace;font-weight:500;
  font-size:11px;letter-spacing:.06em;color:#5C6326;white-space:nowrap}
.ac-award::before{content:"";width:6px;height:6px;border-radius:50%;
  background:#8C9646;flex:none}
.cs-caption .ac-award{margin-top:0;margin-left:10px;vertical-align:middle}

/* The hang. Two columns inside the study's own 799px measure rather than three
   across a wider page: the whole point of moving these onto this chassis was that
   the column does not change width partway down. */
.ac-hang{column-count:2;column-gap:40px;width:100%}
.ac-work{break-inside:avoid;margin-bottom:46px;display:block}
.ac-frame{position:relative;transition:transform .4s cubic-bezier(.34,1.2,.5,1),
  box-shadow .4s ease}
.ac-work:hover .ac-frame{transform:translateY(-4px)}
.ac-frame img{display:block;width:100%;height:auto}
/* Three treatments, by position. A salon hang is mixed by definition; one frame
   repeated a hundred times is a grid wearing a costume. */
.f-mat .ac-frame{background:var(--parchment);padding:18px;
  border:1px solid rgba(90,78,62,.32);box-shadow:0 10px 24px rgba(70,60,48,.15)}
.f-mat:hover .ac-frame{box-shadow:0 18px 34px rgba(70,60,48,.23)}
.f-thin .ac-frame{padding:6px;background:#2E2A26;box-shadow:0 10px 22px rgba(70,60,48,.19)}
.f-thin:hover .ac-frame{box-shadow:0 18px 32px rgba(70,60,48,.27)}

/* Taped to the wall. Both strips hang from the TOP corners, angled inward, each
   straddling its corner so roughly half the strip lies over the picture.

   That overlap is the whole thing, and it is what the first version got wrong. It
   put one strip diagonally out past the top-left corner and the other out past the
   bottom-right, at -15px and -8px on a frame with no padding -- so neither touched
   the picture at any point. They read as two loose beige rectangles in the gutter,
   most obviously on the last piece in a column, where one is left sitting on its own
   under the bottom of the hang with nothing beside it.

   Tape hangs from the top because that is how anybody actually tapes a photograph
   to a wall, and because a strip at the bottom of a column has nothing above it to
   look like it is holding.

   Slightly translucent, with a soft edge shadow, so the picture reads faintly
   through it and it sits ON the print rather than beside it. */
.f-tape .ac-frame{box-shadow:0 8px 18px rgba(70,60,48,.16)}
.f-tape:hover .ac-frame{box-shadow:0 16px 28px rgba(70,60,48,.24)}
.f-tape .ac-frame::before,.f-tape .ac-frame::after{content:"";position:absolute;
  width:62px;height:19px;top:8px;z-index:2;
  background:linear-gradient(105deg,rgba(232,223,198,.90),rgba(240,233,212,.80));
  border-left:1px solid rgba(160,145,118,.30);
  border-right:1px solid rgba(160,145,118,.30);
  box-shadow:0 2px 5px rgba(70,60,48,.20)}
.f-tape .ac-frame::before{left:-22px;transform:rotate(-42deg)}
.f-tape .ac-frame::after{right:-22px;transform:rotate(42deg)}
.ac-label{margin-top:14px;padding-left:12px;border-left:2px solid #C8D665}
.ac-label .t{display:block;font-family:'Mackinac','Fraunces',Georgia,serif;font-weight:500;
  font-size:15px;line-height:1.3;color:var(--dusty-granite)}
.ac-label .b{display:block;margin-top:7px;font-family:'Diatype','Inter',system-ui,sans-serif;
  font-weight:400;font-size:13px;line-height:1.55;color:var(--muted)}
@media (prefers-reduced-motion:reduce){
  .ac-frame{transition:none}.ac-work:hover .ac-frame{transform:none}
}
@media (max-width:760px){
  .ac-hang{column-count:1}
}
"""

# Where a piece has been published. Kept as data rather than written into a blurb
# so the same fact can appear on the piece, in the page's credit strip and in the
# category's own summary without being retyped in three voices.
AWARDS = {
    "mycology": "Featured in Physics Today",
    "yb-element3": "Featured in the Jostens Look Book",
}
# ...and the category-level version of the same fact, for the credit strip.
FEATURED = {
    "water-drop": ("Featured in", "Physics Today"),
    "yearbook": ("Featured in", "Jostens Look Book"),
}

FRAMES = ["f-mat", "f-thin", "f-tape"]


def award(key, cls=""):
    a = AWARDS.get(key)
    return '<span class="ac-award%s">%s</span>' % (cls, esc(a)) if a else ""


def plain_section(anchor, label, h2, inner):
    """A section that is a heading and a block, with no prose between them.

    _cs.section always writes a .cs-body, which on a gallery section would be an
    empty paragraph box holding open 32px of the flex gap for nothing."""
    return ('    <section id="%s" class="cs-section">\n%s%s    </section>\n\n'
            % (anchor, _cs.sechead(label, h2), inner))


def plate(media, title, blurb, key, extra=""):
    """A figure and its caption. A falsy blurb gives the title alone.

    Title-only is what the studio galleries already do, for the reason written above
    them: a paragraph under every picture turns a wall into a reading exercise, and
    the writing that matters is already above it in Context and Method. The films
    were the last place still carrying a runtime and a description under each entry,
    and there was no reason for them to be the exception.
    """
    tail = (' · %s' % (extra + esc(blurb))) if blurb else ""
    return ('      <figure class="cs-figure ac-plate">\n%s'
            '        <figcaption class="cs-caption"><span class="t">%s</span>%s'
            '%s</figcaption>\n'
            '      </figure>\n'
            % (media, esc(title), award(key), tail))


def build_category(cat):
    slug = cat["slug"]
    by = {p[0]: p for p in cat["pieces"]}
    prose = PROSE.get(slug)
    vids = (prose or {}).get("videos") or {}
    hang = (prose or {}).get("hang", True)
    film = (prose or {}).get("film")

    nav = [("overview", "Overview", False)]
    secs = []

    if prose:
        for h2, paras in prose["sections"]:
            anchor = h2.lower().replace(" ", "-")
            nav.append((anchor, h2, False))
            secs.append(_cs.section(anchor, cat["tag"], h2, [esc(p) for p in paras]))

        plates = []
        for i, key in enumerate(prose["picks"]):
            if key not in by:
                continue
            pslug, title, blurb, w, h = by[key]
            if key in vids:
                stem, dur = vids[key]
                # preload="none" so three films on one page cost nothing until one
                # is played, and the poster is the still this entry used to be, so
                # the page looks the same before anyone presses anything.
                media = ('        <video controls preload="none" playsinline '
                         'poster="../../assets/art/%s/%s.jpg" width="%d" height="%d">\n'
                         '          <source src="../../assets/video/%s.mp4" type="video/mp4">\n'
                         '          Your browser cannot play this film. '
                         '<a href="../../assets/video/%s.mp4">Download it instead.</a>\n'
                         '        </video>\n' % (slug, pslug, w, h, stem, stem))
                # Title only, like every other gallery on the site. dur is still
                # read, because carrying a runtime is what marks this entry as a
                # film rather than a still.
                extra, blurb = "", None
            else:
                media = ('        <img src="../../assets/art/%s/%s.jpg" alt="%s" '
                         'loading="lazy" width="%d" height="%d">\n'
                         % (slug, pslug, esc(title), w, h))
                extra = ""
            plates.append(plate(media, title, blurb, key, extra))
        if plates:
            lbl = "Films" if vids else "Selected"
            nav.append(("selected", lbl, False))
            secs.append(plain_section(
                "selected", cat["tag"],
                "The films" if vids else "Selected results", "".join(plates)))

    if film:
        p = by.get(film["poster"])
        w, h = (p[3], p[4]) if p else (760, 427)
        nav.append(("run", film["title"], False))
        media = ('        <video controls preload="none" playsinline '
                 'poster="../../assets/art/%s/%s.jpg" width="%d" height="%d">\n'
                 '          <source src="../../assets/video/%s.mp4" type="video/mp4">\n'
                 '          Your browser cannot play this film. '
                 '<a href="../../assets/video/%s.mp4">Download it instead.</a>\n'
                 '        </video>\n'
                 % (slug, film["poster"], w, h, film["src"], film["src"]))
        secs.append(plain_section(
            "run", cat["tag"], film["title"],
            plate(media, film["title"], film["cap"], None,
                  '<span class="runs">%s</span> &middot; ' % esc(film["dur"]))))

    if hang:
        # A title and nothing else, on every category. A paragraph under every
        # picture turns a wall into a reading exercise, and the writing that
        # matters is already above it, in Context and Method.
        works = ['      <div class="ac-hang">\n']
        for i, (pslug, title, blurb, w, h) in enumerate(cat["pieces"]):
            works.append(
                '        <div class="ac-work %s">\n'
                '          <div class="ac-frame"><img src="../../assets/art/%s/%s.jpg" alt="%s" '
                'loading="lazy" width="%d" height="%d"></div>\n'
                '          <div class="ac-label"><span class="t">%s</span>%s</div>\n'
                '        </div>\n'
                % (FRAMES[i % len(FRAMES)], slug, pslug, esc(title), w, h,
                   esc(title),
                   award(pslug)))
        works.append('      </div>\n')
        title = "The full set" if prose else "The work"
        nav.append(("works", title, False))
        secs.append(plain_section("works", cat["tag"], title, "".join(works)))

    # The credit strip, in the case study's own meta box. On a team project this is
    # not decoration: it is what keeps the page honest about who did what.
    meta = []
    if cat.get("course"):
        meta.append(("Course", esc(cat["course"])))
    if cat.get("team"):
        meta.append(("Team", esc(cat["team"])))
    if cat.get("lead"):
        meta.append(("Advised by", esc(cat["lead"])))
    if slug in FEATURED:
        meta.append(tuple(esc(x) for x in FEATURED[slug]))
    # Count what the page actually shows, and name it correctly. Three of these
    # pages have no hang: "8 pieces" over a page holding five figures from a report
    # was both the wrong number and the wrong word.
    if vids:
        meta.append(("Films", "%d" % len(vids)))
    elif not hang:
        meta.append(("Figures", "%d" % len(prose["picks"])))
    else:
        meta.append(("Pieces", "%d" % len(cat["pieces"])))
    # No opening plate. The cover is the image the ticket you arrived from has just
    # shown you, and on the project pages the first Selected figure shows it again a
    # screen later; a page that opens on its own thumbnail starts by repeating
    # itself.
    _cs.build("art-" + slug, dict(
        out="art/%s/index.html" % slug, root="../../",
        title=cat["name"], kicker=cat["tag"], intro=cat["blurb"], hero=None,
        nav=nav, meta=meta, sections=secs,
        extra_css=CSS_CAT, back="../", back_label="Back to Art",
        pill="art"))


print("art section:")
build_index()
for _c in CATS:
    build_category(_c)
