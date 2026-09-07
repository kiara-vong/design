# Portfolio v2

Thirty-two pages, no framework, no dependencies beyond Pillow.

```bash
python build.py                 # generate everything, then check it
python -m http.server 4321      # then open http://localhost:4321
```

`build.py` is the only entry point you need. It runs the generators in dependency
order, clears the files each one owns so a renamed page cannot survive as a stale
file, and finishes by checking that every link, anchor and asset resolves and that
nothing in `assets/` is unreferenced. It exits non-zero if a link is broken.

```bash
python build.py art             # one section, plus whatever it depends on
python build.py --pages         # HTML only, skip regenerating the artwork
python build.py --check         # build nothing, just run the checks
```

Order matters in exactly one place and `build.py` is what enforces it:
`gen/gallery.py` writes `content/art_index.py`, and `gen/art_pages.py` reads it.
Run them the other way round and the Art pages build silently from the previous
category table -- they come out looking fine and describing the wrong art.

`gen/video.py` is deliberately NOT in the build. It is a twenty-minute ffmpeg run
over 1.2GB of source and its output changes only when a source film does.

| Page | What it is |
| --- | --- |
| `index.html` | Hero, four work cards, "how I work", project tiles, footer |
| `resource-dashboard.html` | Case study 01 |
| `events-timeline.html` | Case study 02 |
| `ui-consistency.html` | Case study 03 |
| `persona-homepage.html` | Case study 04 (upcoming) |
| `p-*.html` | Six project detail pages |
| `about.html` | Two columns on a warm ground; hover the interests, art appears |
| `art.html` | A ticket index of 19 art categories, under a painted title band |
| `art-*.html` | One page per category, built on the case-study chassis |

The Art section is two levels. `art.html` is an index of categories as perforated
tickets, projects first, opening on the same painted ground as About and the home
page. Each `art-<slug>.html` is a case study: the same fixed section rail, section
heads and type as `resource-dashboard.html`, because they are built through the
same template (see **The Art pages are case studies** below).

**One category per folder in `../website/art`**, and the studio half of the index is
grouped into Drawing / Painting / Photography / Design. All of that comes out of
`../website/art/art.js`, which is the old site's own art index: the folder-to-group
mapping, the group order, the category labels (Canvas, Hatching, Yearbook) and each
category's cover image. Piece titles come from `../website/art/<folder>/index.html`
wherever that page carried one.

Take that file as the source of truth for the Art section's structure. Grouping by
medium instead had merged five separate sports into one "Photography" page and put
a card routine inside "Illustration", and several piece titles invented for those
mixed categories described the wrong pictures entirely.

Five categories are projects (Splash, Vortex Rings, Rheoscopic Gear Train,
SandSketch, iPhone Films) and carry context, method and selected results. Three of
those have no gallery: iPhone Films is three films, since a frame grab cannot show
cut rhythm; SandSketch is the full run; and the Gear Train is documentation of one
object rather than a body of work. The fourteen studio categories are a salon hang.
Every hang shows titles only.

## READ THIS BEFORE PUBLISHING

Five things will cause you real problems if they ship as-is.

1. **`assets/hero/hakone.png` is a photograph of the template's author.** It is her
   face, in the postcard on your home page. It came across when the reference
   assets were copied. Replace it with a photo of yours.
2. **The fonts are commercial and unlicensed.** PP Kyoto, ABC Diatype, Apercu
   Mono, P22 Mackinac and Monument Grotesk are in `assets/fonts/` and served from
   the origin, which their licences do not permit. Either buy webfont licences
   or delete the folder; every rule already names an open fallback.
3. **Three of the five art projects are TEAM projects.** Splash, Vortex Rings and
   the Rheoscopic Gear Train were done with Sofia Gilroy, Himanssh Pettie and
   Lucian Sharpe; SandSketch with Christian Labrador and Michael Donoso. Their
   pages credit those teams by name and should keep doing so.
4. **Verify the case-study copy.** Everything in `cases-content.py` traces to your
   own project material. Nothing internal is named: no product name, no internal
   URLs, no repository links, no employer brand hexes. That line is deliberate.

5. **`assets/video/` is 135MB.** SandSketch alone is 62MB for a 7-minute run and
   Torah is 53MB for four minutes. Every player is `preload="none"` behind a poster,
   so a visitor who never presses play downloads none of it, but it is a large
   thing to put on a host with a bandwidth cap. If that matters, cut SandSketch to
   a 60-90 second highlight and re-run `gen-video.py`.

Also: the footer weather ("Sunny, 72°") is decoration, hardcoded in
`site-footer.js`. The clock beside it is real Eastern time. And
`assets/demo/frame-*.png` are ten cropped frames from the internal Resource
Dashboard demo video; nothing references them. They are kept, not deleted, because
publishing employer video is a decision only Kiara can make.

## Generated artwork

Every SVG in `assets/` is emitted by one of these, all seeded so reruns are
byte-identical.

| script | makes |
| --- | --- |
| `gen-frames.py` | perforated ticket and postcard frames |
| `gen-art.py` | botanicals: plant garden, cursors, footer flower sprites |
| `gen-sparkles.py` | the three sparkle layers |
| `gen-work.py` | the four work-card thumbnails, self-animating |
| `gen-cs-figures.py` | the four `cs-*.svg` diagrams on the case studies |
| `gen-archive.py` | archive tile content layers |
| `gen-dorms.py` | the Dorms @ Brown tile, drawn (nothing to screenshot) |
| `gen-process.py` | the three "how I work" panels |
| `gen-persona.py` | persona field wash |
| `gen-polaroids.py` | About-page polaroids, from `../website/art` |
| `gen-gallery.py` | cuts every Art image and writes `gallery-index.py` |
| `gen-video.py` | the four art videos, transcoded from the source .mov files |
| `uikit.py`, `handdrawn.py` | shared drawing vocabularies |

Every page except `index.html` is generated, **edit the generator, not the HTML**.
`build.py` runs them all; the scripts are listed in its `STEPS` table.

## Layout

```
index.html          the one hand-written page
about.html
art/index.html      the ticket index      art/<slug>.html    one per category
work/<slug>.html    the four case studies
projects/<slug>.html the six project pages
build.py            the only entry point
*.css *.js          stylesheets and behaviour
content/            writing
  art_pieces.py       every art category, piece and title (hand-edited)
  art_index.py        generated by gen/gallery.py; do not edit
gen/                generators, run as `python -m gen.<name>`
assets/             everything they emit, plus the photographs
  hero/               the home and About grounds, the cats, the postcard
  cards/              the four work-card thumbnails and their washes
  case/               the case-study diagrams
  art/                every image in the Art section
  tile/               the six project-tile captures
  about/              the About polaroids, and _src/ for the photos behind them
  ui/                 chrome: favicon, tickets, botanicals, footer flowers
  video/              the four transcoded films
  fonts/  doc/  demo/
```

Only `index.html` and `about.html` sit at the root, because those are the two the
nav points at by name and a static host needs the first one to serve `/`. Everything
else is one folder down, which means every stylesheet, script and asset in it is
reached through `../`.

That prefix is a template argument, not something you type. `gen/case_template.py`
takes `root` in its spec and threads it through the page, the pill and the back
link; `gen/art_pages.py` uses a literal `../` because everything it writes lives in
`art/`. If you add a page at a new depth, pass its `root`, do not hand-edit the
output.

Anything under a `_src` folder or starting with `_` is staged INPUT and is never
touched by a build. Everything else under `assets/` is output and is rewritten on
every run, so do not save new artwork there: it will be deleted. Sources go in
`../website/art/`, or in an `_src` folder next to where they are used.

Generators run with the project root as the working directory, which is what
`python -m gen.<name>` gives you. They resolve `assets/` and `../website/` against
that, not against their own location.

## Where the writing lives

`content/art_pieces.py` holds the Art section's content: every category, every
piece, every title. It has no imports and no logic, paths are strings, and the only
thing the file can do is be read.

It is separate from `gen/gallery.py` on purpose, and the reason is not tidiness. The
two were one 480-line file, and a caption buried two hundred lines inside a resize
loop does not get read as a caption. Several titles were wrong for months as a
result: the still lifes are cut-paper flowers and had been captioned as fruit-bowl
drawing practice. Nobody, including the person who wrote them, ever looked at that
file as a page of text. Now it is one.

Titles are Kiara's wherever her old site had one. If you add a piece and cannot tell
what the picture is, open it. Do not invent a title.

`gen-video.py` is separate and slow (about twenty minutes), so it is not part of
that sequence. Run it only when a source film changes. It needs ffmpeg; `pip
install imageio-ffmpeg` supplies one if the system has none. If you edit it, note
the comment about `stderr`: ffmpeg writes a progress line every second, and handing
it a pipe nothing drains deadlocks it once the buffer fills. It looks exactly like
a slow encode -- process alive, output file at 0 bytes, CPU time flat.

`index.html` is hand-written.

### Why the artwork animates itself

Each thumbnail and figure carries its own `<style>` inside the SVG. A browser runs
that even when the file is the `src` of an `<img>`, so the choreography travels
with the artwork instead of living in a stylesheet every page loads, and a redraw
never leaves stale keyframes behind in `index.html`. Reduced-motion handling rides
along in the same block.

Three approaches were tried for these. Real screenshots read as unrelated
rectangles at thumbnail size and lost their detail. Hand-drawn versions held
together as a set but could not carry technical content: a wobbly dependency
graph reads as a doodle. Flat vector with one shared palette is the third answer
and the one that stuck.

## Two numbers that are measured, not chosen

- `WH` in `index.html`'s head script is `#work`'s real height. It sets the body
  height and where the footer band starts. Change the grid, read
  `#work.offsetHeight` at 1440px wide, put the new value there.
- `.mascot-label`'s offsets in `mobile.css` are fractions of the mascot image's own
  geometry. Swap the mascot, re-measure them.

## Layout model

Above 760px, `index.html` and `about.html` are 1440px canvases scaled to fit: the
head script computes the transform before first paint, so nothing snaps into place
on load. Below 760px `mobile.css` takes over and `mobile.js` sets `--card-k`,
which scales the fixed 529px card thumbnails into a phone column.

`art.html` deliberately does **not** scale. It is a list that should reflow, and
freezing a gallery's column count would be the wrong trade. The `art-*.html` pages
do scale, because they are case studies now and scale the way case studies do.

Page-level `<style>` blocks must come **before** the `mobile.css` link. They carry
desktop-canvas geometry, and loading them after the responsive sheet means they
win at phone widths too.

### The nav pill

Every page floats the same pill, from `nav.py`. Two things it needs on any page
built as a normal flowing document rather than a scaled canvas:

- Its wrapper id must be listed in `site-nav.js` (`#hg-center, #ab-navwrap,
  #lb-navwrap, #pg-navwrap, #cs-navwrap`). If it is not, that script bails and the
  pill loses its label colour, its light-ground surface and its stand-down at the
  footer, all silently.
- `.nav`'s base rule hardcodes `position:absolute; top:746px`, meant for the 1440
  canvas it normally lives inside. Both the wrapper **and** `.nav` itself need
  that cancelled, or the pill lands partway down the viewport, or below it.
- It must be scaled by `var(--nav-k)`. The pill is drawn at 1440-canvas size, and
  the home and About pages shrink it along with their hero, so a flow page that
  leaves it at 1:1 shows a visibly larger menu than the page you arrived from
  (74px against 62px at 1280x720). `site-motion.js` publishes `--nav-k` on the
  root from the head, using the same formula as `index.html`'s `C.measure()`.
  Scale it about `bottom center` so the 26px gap holds.

### The Art pages are case studies

`art-<slug>.html` is not styled to resemble `resource-dashboard.html`. It is built
by the same function. `gen-art-pages.py` imports `gen-cases.py` and calls its
`build()`, so the section rail, the scroll-spy, `.cs-sechead` with its green tick
and gold label, `.cs-h2`, `.cs-body`'s measure and leading, the scaled 1440 stage
and the pill all arrive as a consequence rather than as a copy.

Three things differ, and all three are arguments rather than forks: `back`
(art.html, not index.html), `pill` (which nav item lights), and `extra_css` (the
hang, the video plate, the natural-aspect figure). If a fourth difference ever
appears, add a fourth argument. A parallel template would drift within a week --
which is exactly what the first version of these pages did.

Two things a work study has that these needed anyway:

- `.cs-media` is a fixed 391px window, right when every figure is a screenshot at a
  known size and wrong for a painting. `.ac-plate` keeps the artwork's own ratio.
- `.cs-caption` is centred, right for one short line and hard to read at the three
  lines these run to. `.ac-plate .cs-caption` sets it left on a measure.

### The project tiles

Six tiles under the four work cards, each a real capture inside a browser frame the
page draws itself. They move in one of two ways and which one is a property of the
site being shown, not a style choice:

- **Scroll**, for the three that are real pages (Dorms, the Stardew companion, the
  old portfolio). A tall capture travels inside a fixed window, which is how a
  thumbnail shows a page rather than a screenful of one. `--travel` on the `<img>`
  is the capture's height minus the window's, written by hand from the real image.
- **Pan**, for the three that are single-screen apps. A chess board, a maze and a
  generated island each fill the viewport exactly -- captured at 1280x860 from the
  live builds, there is nothing below the fold -- so the frame moves across the
  still instead. Add `pan` to the `.tile-view` and it switches; the image needs
  `object-fit:cover` to fill its window before it can move inside it, which that
  class does. 19s against the scroll's 14s, so a row of six never falls into step.

Giving the second group a scroll would be animating content that does not exist.

## The hero

`index.html`'s hero carries three measured numbers. All three were wrong at some
point because somebody changed the thing they were measured against and not them.

- **`WH`** in the head script is `#work`'s real height. Change the grid, read
  `#work.offsetHeight` at 1440px wide, put the number here.
- **`.mascot`** is sized to the artwork's own ratio, not to a square slot. The
  current drawing is 1080x836.
- **`.mascot-prompt`** is the live prompt typed onto the laptop screen. Its five
  numbers come from a coordinate grid drawn over the artwork, because the laptop is
  in perspective and every edge in it lies. The tilt is CLOCKWISE. Two separate
  attempts assumed otherwise and put the panel through the "Clawed" wordmark. If the
  artwork changes, draw the grid again rather than nudging the numbers.
