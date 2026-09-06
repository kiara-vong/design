# Capture request

Everything the site is still waiting on, in one list. Fifty-five briefs: six
project thumbnails, thirty across the four live sites, nineteen for the dashboard
demo. Three thumbnails are already correct and marked no action, two live-site stills
double as thumbnails, and one plate is a drawing rather than a capture, so it is
forty-nine distinct shoots.

There are five live sites to record, not four. The work case studies used to be
unshowable because they describe an internal tool; there is now a public rebuild of
it with invented data, so Part 3 records like any other site rather than being a list
of things to reconstruct.

The live-site captures are drawn from each project's own README, so the list is the
feature set as each project describes itself, not as the portfolio currently
summarises it. Several of these features are not on the portfolio at all yet. They
are listed anyway, because a capture is the cheapest way to find out whether one
deserves a slot.

Each one names the sentence it has to prove. That is the whole test: if a capture
does not make a specific claim on the page believable, it is decoration and should
be skipped rather than shot badly.

---

## Rules that apply to all of them

**Two sizes, and only two.**

| Where | Record at | Renders at |
| --- | --- | --- |
| Case-study media (`.cs-media`) | 1598 x 782 | 799 x 391 |
| Project thumbnail (`.tile-view`) | 1280 wide, natural height | 776 wide |

**Frame it before recording. Do not crop afterwards.** Launch the target in a clean
Chrome window with no tabs, address bar, bookmarks or extension icons:

    chrome.exe --app=<url> --window-size=1598,860 --user-data-dir=C:\temp\clean

The separate `--user-data-dir` is what removes the profile avatar and every
extension button. It does more for how professional this looks than any editing.

## Record flat. The camera is CSS.

This is the most important instruction here and the easiest to get wrong.

The reference build this site is modelled on does **not** record zooms, pans or
cross-fades. It captures a flat, static asset and then moves a camera over it with
CSS keyframes. `case-study.css` still carries that machinery: `wa-follow` pans and
zooms across a phone screen following a conversation, `tile-scroll` and `tile-pan`
drive the six project thumbnails.

That approach wins on every axis. It stays sharp at any zoom because it is a
transform over a still, not a re-encode of one. It is a fraction of the file size. It
can be retimed later without re-recording. And it never has a cursor drifting or a
frame the encoder smeared.

**So: do not zoom while recording. Do not pan while recording. Do not add motion in
an editor.** Hold the frame still and let the interface be the only thing that moves.
Where a brief wants a camera move, capture the widest state as one flat asset and say
so; the movement is written afterwards as keyframes, and I will write them.

Video is only for something that genuinely animates in the product itself: a game
running, a solver resolving, a state transition, a loading sequence, a keyboard
walkthrough where focus moves. Everything else is a still with a camera over it.
Every brief below says which it is, and Part 4 says which camera each still feeds.

**Video spec where it is needed:** 30fps, muted, H.264 mp4. 8 to 12 seconds unless a
brief says otherwise, which is shorter than it feels while recording. Start and end on
the same frame so it loops without a visible cut; record a few seconds spare at each
end and trim to matching frames.

**Cursor:** straight lines, and pause about half a second before every click. Real
usage is jittery and reads as nervous on replay. Several briefs want the cursor
hidden; each one says so.

**Anything that wants a zoom-in, a push, a reveal or a cross-fade:** capture the
flat states, one PNG each, at the same window size and scroll position. Frames that
do not line up cannot be cross-faded, and that is the single most common reason a
sequence has to be reshot.

**Stills:** PNG at 2x. Add `--force-device-scale-factor=2` for real pixels rather
than an upscale.

**Do Not Disturb on.** One notification sliding in ruins a take.

**Where files go:** raw captures into `assets/video/_src/` (video) or
`assets/tile/_src/` (stills). Nothing under `_src` is touched by the build. Do not
put anything in `assets/video/` or `assets/tile/` directly; those are output and get
overwritten. `gen/video.py` does the crop, trim and encode.

---

# Part 1 -- Project thumbnails

Six tiles on the home page. Each is a still image that the page animates itself: a
tall capture that scrolls inside a drawn browser frame (`tile-scroll`), or a single
screen the frame pans across (`tile-pan`). **No video here.** The CSS mechanism is
smaller, sharper and keeps the drawn frame.

### 1.1 UI/UX Case Studies -- cause found, needs one reshoot

The tile is a flat navy rectangle today, and the reason is now known. The site holds
`#page-wrap` at `opacity: 0` until JavaScript adds `body.loaded`, with a full-screen
`#loader` painted `#1b2e63` on top. Every headless attempt captured the loader.

Two ways past it, both fine:

    document.body.classList.add('loaded');
    document.getElementById('loader').classList.add('is-hidden');

or simply wait about two seconds after load before capturing, which is what a real
browser does anyway.

- Full-page PNG at **1280 wide**, ShareX Scrolling Capture or GoFullPage.
- Landing page, top of page, nothing hovered, loader gone.
- `assets/tile/_src/uxfolio.png`

### 1.2 Stardew Companion

Currently the game's title screen, which shows nothing about the project. The page
claims *"look up any villager's favourite gifts, click around town to learn what each
building is for."* The tile should show that.

- Full-page PNG at 1280 wide with the **villager grid visible**, no popup open.
- If the page runs past about 1100px tall it becomes a scrolling tile, which is
  better than a pan.
- `assets/tile/_src/stardew.png`

### 1.3 Dorms @ Brown -- unblocked

The backend is alive again: `dab-w77u.onrender.com/dorms` returns the real dorm list.
**The first request takes about 23 seconds** because Render's free tier spins the
container down when idle, so load a page once and wait for it before recording
anything. A cold start on camera looks like a broken app.

- Full-page PNG at 1280 wide of a **single dorm's detail page**: photo, floor plan,
  features, reviews. The page claims all four and the tile currently shows the
  landing page.
- `assets/tile/_src/dorms.png`

### 1.4 to 1.6 -- already done, no action

Island Generator, Chess and Pac-Man are current and correct. They pan rather than
scroll because each is a single screen with nothing below the fold.

---

# Part 2 -- The live sites, feature by feature

Four sites, thirty captures, drawn from each project's README. Each names the feature
it exists to show.

---

## 2A. Stardew Companion -- kiara-vong.github.io/stardew

The README describes far more than the portfolio claims. The site says gifts and
buildings; the project also contains four playable arcade games, one of which
synthesises its own music. That gap is the most useful thing in this document.

### 2.1 VIDEO -- villager gift lookup *(8-10s loop, cursor visible)*
The most-used thing in the app and invisible on the site. Type a name into the search,
open the card, let the Loved and Liked lists land. Pick someone with a long list, so
the search bar has a reason to exist.
**Proves:** *"look up any villager's favourite gifts."*

### 2.2 STILL -- one villager card, whole *(PNG @2x, popup only)*
Crop to the card, not the page. Corner-bracketed portrait, birthday split into season
and day boxes, biography panel, and the two gift rows with the real in-game heart
sprites rather than emoji. This is the piece of craft the README is proudest of.
**Feeds:** `push`, which frames the whole card then pushes in on the gift rows.

### 2.3 STILL -- the full villager grid *(full-page PNG, 1280 wide)*
All 34 portraits in one frame. A number in prose is an assertion; 34 faces is
evidence.
**Proves:** *"all 34 villagers are clickable."*

### 2.4 STILL -- the locations section, both tiers *(full-page PNG, 1280 wide)*
The six main buildings as full boxes and the smaller spots as the lighter icon
treatment, in one capture. The tiering only reads as a decision when both tiers are
in shot.
**Proves:** *"so the page doesn't turn into a wall of boxes."*
**Feeds:** `strip`.

### 2.5 STILL -- a location popup *(PNG @2x, popup only)*
One of the six full popups: photo, key NPCs, description. Crop to the popup.
**Feeds:** `push`.

### 2.6 STILL -- Explore the Valley, full height *(tall PNG, popup only)*
Scroll capture the **entire** popup interior, not the visible part. The point is that
the outdoor areas are grouped into one long scrollable panel rather than given a box
each, and only the full height shows that.
**Feeds:** `strip`, scrolling it inside a fixed popup frame.

### 2.7 SEQUENCE -- Did You Know *(3 PNGs @2x, identical frame)*
Three different facts, same crop, same window size, same scroll position. The
smallest and cheapest example of the frames-must-line-up rule.
**Feeds:** `deal`.

### 2.8 STILL -- the arcade cabinet row *(PNG @2x)*
All four cabinets side by side, nothing open. The establishing shot for 2.9 to 2.13.
**Proves:** *"four playable canvas cabinets, no game engine."*

### 2.9 VIDEO -- Junimo Kart *(8-10s loop, cursor hidden)*
Jump a spike, clear a gap, collect stars, score readout in frame. Start and end on a
clean run of ground so it loops.

### 2.10 VIDEO -- Fishing, the catch bar *(10-12s, cursor hidden)*
Cast, bite, then the catch-bar minigame with the bar accelerating and the progress
meter shifting colour. The README says this is a deliberate pixel-for-pixel port at
the source's own 20ms tick rate rather than an approximation, and that is a claim
only motion can support. Show a catch, not a miss.

### 2.11 VIDEO -- Journey of the Prairie King *(8-10s, cursor hidden)*
Move and fire through a wave with several enemies on screen at once. Keyboard only,
so no cursor.

### 2.12 VIDEO -- Junimo Jamboree *(10-12s)* **the one audio exception**
Falling notes in all four lanes with judgments landing. The claim is that the song
and the chart are generated from one source by the Web Audio API, and a muted video
makes exactly half of that invisible.

Record **with audio**. The site will still autoplay it muted, because browsers allow
nothing else, with a small unmute control on the plate. That control is worth
building for this one asset. Capture on Normal, where note density reads best.

### 2.13 STILL -- Jamboree difficulty select *(PNG @2x)*
Three difficulties with per-difficulty best scores visible.
**Proves:** *"difficulty changes note density and timing windows, not the song."*

---

## 2B. Island Generator -- kiara-vong.github.io/animal-crossing

The algorithm is the entire project and the current tile is a finished render, which
shows the output and hides the idea.

### 2.14 VIDEO -- the island building itself *(12-15s, cursor hidden)*
Wave function collapse from an empty grid to a finished island. Hold `space` and let
it run. Start on empty and end on complete: this does **not** need to loop and should
not be forced to. Highest-value capture in this document.
**Proves:** *"built tile by tile... constraint propagation, everywhere after."*

### 2.15 VIDEO -- steering it *(6-8s, cursor visible)*
Click a tile to force a type mid-generation and let the constraint propagate outward
into its neighbours. Pause about half a second before the click so it reads as
deliberate.
**Proves:** *"generation isn't purely automatic, it's steerable."*

### 2.16 STILL -- the finished island, wide *(PNG @2x, 1280 wide)*
Auto-rotate off, camera settled, whole island in frame. `screenshots/scene.png`
exists but is too small for the slot.
**Feeds:** `tile-pan`, which supplies the camera move, so do not orbit while
recording.

### 2.17 SEQUENCE -- four stages of one generation *(4 PNGs @2x, camera locked)*
Empty grid, roughly a quarter filled, roughly three quarters, complete. Same camera
angle in all four, which means not touching the mouse between shots.
**Feeds:** `deal`, and this is also the still fallback for 2.14 under reduced motion.

---

## 2C. UI/UX Case Study Portfolio -- kiara-vong.github.io/portfolio

### 2.18 STILL -- the homepage *(full-page PNG, 1280 wide)*
The same capture as 1.1. Shoot once, use twice.

### 2.19 VIDEO -- the loader and the page transition *(6-8s loop, cursor visible)*
The navy screen that broke the thumbnail is a designed loading sequence, and it has
never been shown anywhere. Land on the homepage through the loader, then click into a
case study so the page transition plays.
**Proves:** that the site has considered motion, which no still can say.

### 2.20 SEQUENCE -- one case study, end to end *(4 PNGs @2x)*
Four frames from a single case study, ideally Fonda Wallet or A/B Testing: the
problem, what was tried, the test or the iteration, what shipped. Same width and
scroll rhythm in all four.
**Proves:** *"each piece walks through the problem, what was tried, and what actually
shipped."* This is the claim the whole project rests on and there is currently no
evidence for it anywhere.
**Feeds:** `deal`.

### 2.21 STILL -- the case-studies index *(PNG @2x)*
The four case studies as a set, so the reader knows the number before clicking.

### 2.22 STILL -- experiments and all-works *(PNG @2x)*
The section below the case studies. Currently unmentioned on the portfolio.

### 2.23 VIDEO -- the mobile menu *(5-6s loop, cursor visible, phone width)*
Record the window at 390 wide. The full-screen overlay slides in on a long cubic
bezier with a layered `::before` and `::after` sweep behind it, which is the most
deliberate piece of interaction design on that site.

---

## 2D. Dorms @ Brown -- kiara-vong.github.io/dab

**Warm the backend first.** Load any dorm page and wait out the roughly 23 second
cold start before recording a single frame.

**Names in reviews:** review authors are real students. Either capture reviews you
wrote yourself, or blur the author line. Do not publish someone else's name and photo
out of a university housing app.

### 2.24 VIDEO -- browse and filter *(10-12s loop, cursor visible)*
Start on the full list, apply two filters (room type, then bathroom style), then type
a name into live search. The list narrowing is the whole feature.
**Proves:** *"browse and filter every dorm on campus... with live search by name."*

### 2.25 STILL -- a dorm detail page, full height *(tall PNG, 1280 wide)*
The same capture as 1.3. Photo gallery, features, floor plans, rating and reviews in
one tall image.
**Feeds:** `strip`.

### 2.26 STILL -- the letterboxed gallery *(PNG @2x)*
Pick a dorm whose gallery holds a **tall phone photo**, so the letterboxing is
visible: the full photo over a blurred, darkened copy of itself filling the rest of
the frame. On a landscape photo this capture shows nothing.
**Proves:** *"rather than hard-cropping tall photos to fit a fixed frame (and cutting
off half a room)."*
**Feeds:** `push`.

### 2.27 STILL -- multi-building floor plans *(PNG @2x)*
Keeney or Grad Center, where the plans render as grouped card grids with one group
per building. A single-building dorm does not show this.
**Proves:** *"floor plans render as grouped card grids, one group per building,
rather than a flat list."*

### 2.28 VIDEO -- the recommendation quiz *(12-15s, cursor visible)*
Answer the questions and land on the ranked shortlist. Let the results settle for two
seconds at the end. The longest video in this list and worth its length.
**Proves:** *"a short quiz that narrows 30 dorms down to a shortlist worth touring."*
**Feeds:** `sheet`, if you would rather assemble it from stills. See Part 4.

### 2.29 STILL -- peer reviews *(PNG @2x)*
One dorm's review list with real text and star ratings visible, authors blurred.
Reviews are named in the intro of every version of this project and shown nowhere.

### 2.30 STILL -- the sign-in gate *(PNG @2x)*
The Google sign-in restricted to `@brown.edu`. **No real account in frame:** no
avatar, no address, no account chooser with a name in it. If it cannot be captured
without one, capture the signed-out state only.
**Proves:** *"gating the dorm-browsing and review features to actual students."*

---

# Part 3 -- The dashboard demo

The three work case studies describe an internal tool, which for a long time meant
they could not be shown at all. That is no longer true. There is a public rebuild:

**kiara-vong.github.io/resource-dashboard**

A from-scratch React and TypeScript recreation of the surface, with every name, ARN,
account ID and owner email invented and no proprietary code in it. It records like
any other live site in Part 2, and four routes cover three of the four case studies.

| Route | What it serves |
| --- | --- |
| `#/resources` | Resource Dashboard: filters, hierarchy and table views, export |
| `#/resources/:id` | Resource Details, the compliance timeline, and the jobs list |
| `#/showcase` | UI Redesign / Consistency: eight before/after sections |
| `#/style-guide` | The design-system reference half of the same case study |

### Two consequences worth stating plainly

**Do not use `assets/demo/`.** Those ten frames are cropped from an internal demo
video of the real tool. They were the only option when nothing else existed. A
scrubbed rebuild exists now, so publishing internal frames is a risk taken for no
gain. Shoot the demo instead, and delete that folder once its slots are filled.

**The old rule still governs anything shot anywhere else:** mock data only, and no
internal product name, no internal URLs, no repository or pull-request links, and no
employer brand hex values anywhere in frame. The demo satisfies all of that by
construction, which is the whole reason it exists.

### Before you record

The demo is a `HashRouter` app served from a static host, and its data comes through
Mock Service Worker, a real service worker intercepting real `fetch` calls. Two
practical consequences:

- **Hard-reload once before recording** (Ctrl+Shift+R). A stale service worker is the
  one thing that makes this app look broken on camera.
- **The loading skeletons are real and so is the latency.** The mock layer adds
  artificial delay on purpose. Do not cut it out; 3.5 exists to show it.

---

## Resource Dashboard, at `#/resources`

### 3.1 DIAGRAM, not a capture -- the three-tool reconciliation
The one plate in this document that cannot be recorded. It shows the workflow
*before* the dashboard existed, spread across three internal tools, and there is
nothing public to point a camera at.

Draw it instead: three browser frames, an identifier travelling between them, and the
count of windows it takes to answer one question. It is a stronger artefact than a
screen recording would have been, because the argument is the number of windows
rather than any one screen. I can draw this as an SVG in the site's own hand; say the
word.

### 3.2 VIDEO -- the hierarchy drill, four levels *(10-12s, cursor visible)*
Environments, then regions, then categories, then the resources themselves. Keep the
breadcrumb visible in every frame; it is what makes four screens read as one
movement. End by clicking the breadcrumb root to spring back, which shows the drill
is navigation rather than four separate pages.
**Proves:** the progressive drill-down, and that each level counts what is beneath it.

### 3.3 SEQUENCE -- the same set, two views *(2 PNGs @2x, identical window)*
Graph view and table view of an identical filtered set, same window size, same scroll
position, with the resource count visible in both. The argument is that these are two
readings of one dataset rather than two features, and it only lands if nothing else
in the frame changes.
**Feeds:** `wipe`, with the seam travelling between them.

### 3.4 ANNOTATED STILL -- the default view *(PNG @2x, no OS chrome)*
One clean capture with four callouts: the Category, Region and Environment filters;
the Table and Graph toggle; the "Resources with Jobs Only" toggle, which is a second
data source joined in rather than a filter over the first; and Export, scoped to
whatever is on screen rather than to everything. **Leave about 120px clear on the
right** for the labels.
**Feeds:** `push`, pushing in on each callout in turn.

### 3.5 VIDEO -- the network boundary *(10-14s, DevTools open)* **new slot**
The feature with the strongest engineering claim and no slot on any page yet. Open
the Network tab, reload, and let it show real `fetch` calls to `/api/resources`,
`/api/resources/:id` and `/api/events`, with the loading skeletons on screen while
they are in flight. Then throw one: MSW's error path gives a retryable banner that
actually recovers.

The point is that this is a genuine request boundary with loading and error states
built against it, not an imported array pretending to be data. A still cannot say
that and prose asking to be believed is worse.
**Needs:** a new plate on the Resource Dashboard case study. Worth adding one.

### 3.6 VIDEO -- filters persist, then reset *(6-8s, cursor visible)*
Apply two filters in table view, switch to graph, show the filters still applied and
the counts agreeing, then hit Reset. Small, and it is the difference between a view
toggle and two separate screens.

### 3.7 STILL -- the export *(PNG @2x)* **optional**
The Export button with the filtered count beside it, and the downloaded CSV open
next to it. Only worth shooting if the case study keeps its claim that export is
scoped to the current filter.

---

## Resource Details and the timeline, at `#/resources/:id`

### 3.8 STILL -- the whole detail page, full height *(tall PNG, 1280 wide)*
One scroll capture of everything: the ARN and its metadata grid, the Organization
and Ownership panel, the five tabs, the Resource Timeline, and the Jobs List. This is
the establishing shot for everything below it, and it is also the best single answer
to "what does this thing actually do".
**Feeds:** `strip`.

### 3.9 SEQUENCE -- the five tabs *(5 PNGs @2x, identical crop)*
Account Details, Configurations, Compliance, Network, Tags. Crop to the tab strip and
the panel under it, not the page. Same crop in all five so they cross-fade cleanly.
**Feeds:** `deal`.

### 3.10 STILL -- the events table alone *(PNG @2x, label EXPLORED)*
Crop to the table, timeline excluded, which is the state the case study is arguing
against. It needs enough rows to make the date arithmetic look tedious, and at least
one violated-then-fixed pair several days apart. The demo's sample data already has
both: the Aug 3 violation resolved Aug 8, and the Aug 18 violation resolved Aug 21.

### 3.11 SEQUENCE -- naive vs carry-forward *(2 PNGs @2x, or a wipe)*
Two tracks stacked. Top: the dots on a plain rule with the gaps uncoloured, which is
the explored version. Bottom: the same dots with compliance state carried across the
gaps, so the connecting line is red between a violation and its fix and green either
side. Identical dates and identical width in both.

The demo renders the shipped half already, including the "Compliant since Aug 21"
badge. The naive half has to be faked, and the honest way to do it is to crop the
shipped one and grey the line rather than to redraw the picture.
**Feeds:** `wipe`.

### 3.12 STILL -- a grouped dot, open *(PNG @2x)*
Adjacent same-day events collapse into one dot with a multi-event popover. Capture
one open, with the dot's own colour still visible behind it.
**Proves:** that the timeline stays readable when a day has four events on it.

### 3.13 VIDEO -- keyboard walkthrough *(10-14s, cursor HIDDEN)*
The whole timeline with no mouse. Tab onto the first dot with the focus ring visible,
Enter to open the popover, Escape to close, Tab to the Timestamp header, Enter to
re-sort. This is the accessibility claim and it cannot be made with a still. The dots
and the sortable header were mouse-only before this work, so the capture is the
evidence that they are not any more.

### 3.14 STILL -- the jobs list *(PNG @2x)* **optional**
Its own Category and Source filters, criticality chips, and a second Export. Worth a
frame if the case study wants to claim the page is more than one table.

---

## UI Redesign / Consistency, at `#/showcase` and `#/style-guide`

### 3.15 STILL -- the showcase, full height *(tall PNG, 1280 wide)*
All eight sections in one scroll capture: MUI Theme Foundation, Tables, Buttons,
Filters and Toolbar, Navigation Sidebar, Tooltips, Page Titles and Typography, Cards
and Charts. Each carries its own Problem and Resolution line, which is the case
study's argument already written down.
**Feeds:** `strip`.

### 3.16 STILL -- one section, before and after *(PNG @2x)*
Tables is the best of the eight: the row-height change is the one difference anybody
can see without being told. Crop to that section alone, both halves in frame, labels
included.
**Feeds:** `wipe`.

### 3.17 STILL -- contact sheet of one component *(PNG @2x)*
Every live variant of one component side by side at the same zoom on a neutral
ground. **Keep their real spacing and radii. Do not tidy them**, the mess is the
argument. Buttons or Filters both work. Caption each with the surface it came from.
**Feeds:** `stagger`, so the variants arrive one at a time and the count lands.

### 3.18 STILL -- the style guide *(tall PNG, 1280 wide)*
Brand colours, typography scale, components and their states. The reference half of
the same case study, and the thing that turns "we made it consistent" into something
checkable.
**Feeds:** `strip`.

---

## Persona Homepage -- nothing to shoot yet

### 3.19 SEQUENCE -- three orderings *(PNGs @2x, or a 3-state loop)*
Operator, Owner and Newcomer at the same window width, with one block tinted
identically in all three so the eye can track it moving. Persona switcher visible and
in its selected state. **Waits for the first build to ship.** It is the one route the
demo does not have.

---

# Part 4 -- The camera plan

**This part is a plan, not built yet.** It is here so that every capture above is shot
in a form the site can actually animate, rather than shot first and fitted afterwards.

The site currently has two camera machines (`tile-scroll` and `tile-pan` on the home
thumbnails) plus one bespoke one (`wa-follow`). The reference build has seven or
eight, and that difference is most of why it feels more alive. The fix is not more
one-off animations; it is a small set of named, reusable machines that any slot can
declare with custom properties.

Proposed home: a new `camera.css`, loaded next to `site.css`. That is a one-line
addition in four templates (`index.html`, `gen/case_template.py`,
`gen/project_pages.py`, `gen/art_pages.py`) and keeps `site.css`, already past 3600
lines, from absorbing another subsystem.

Every machine below follows the same three rules:

1. **The asset is flat and static.** The machine supplies all movement.
2. **The slot configures it with custom properties**, never by editing keyframes.
3. **It has a defined resting state** that is a good still, because
   `prefers-reduced-motion` disables the animation and that resting frame is what
   remains. A machine whose still frame is meaningless is a broken machine.

---

## A. `push` -- frame the whole, then move in

The workhorse, and the direct answer to wanting the recorded zoom-ins the original
appears to have. It never recorded them. It pushed a transform into a still.

```css
.cam-push{position:relative;overflow:hidden}
.cam-push img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
  transform-origin:var(--fx,50%) var(--fy,50%);
  animation:push var(--dur,11s) cubic-bezier(.4,0,.2,1) infinite}
@keyframes push{
  0%,14%   {transform:scale(1)}
  32%,68%  {transform:scale(var(--z,1.45))}
  86%,100% {transform:scale(1)}
}
```

A slot sets `--fx` and `--fy` to the point worth looking at and `--z` to how far in
to go. The long holds at both ends are the whole trick: the pause is what lets
someone read the wide frame before it moves and read the detail once it arrives.
Resting state is scale 1, the full frame, which is exactly the still you would pick.

**Fed by:** 2.2 (in on the gift rows), 2.5, 2.26 (in on the letterboxed edge, where
the blurred backdrop meets the real photo), 3.3 (four pushes, one per callout).

## B. `strip` -- a tall still scrolling behind fixed chrome

Already shipping on the home thumbnails as `tile-scroll`. Generalising it means
lifting it out of `index.html` so popups and detail pages can use it too, and keeping
the hard-won detail: **`--travel` is a percentage of the image's own height, never a
pixel count**, because the same tile renders at 322px on desktop and at whatever a
phone gives it.

```css
.cam-strip{position:relative;overflow:hidden}
.cam-strip img{display:block;width:100%;height:auto;
  animation:strip var(--dur,14s) cubic-bezier(.4,0,.2,1) infinite}
@keyframes strip{
  0%,16%   {transform:translateY(0)}
  46%,62%  {transform:translateY(calc(var(--travel,0%) * -1))}
  92%,100% {transform:translateY(0)}
}
```

`--travel` is `(1 - windowHeight / renderedImageHeight) * 100`, measured in the
browser rather than derived. `gen/tiles.py` already computes this for the thumbnails
and should compute it for every strip slot, so it can never be wrong by hand again.

**Fed by:** 1.1 to 1.3, 2.4, 2.6 (inside a drawn popup frame rather than a browser
frame), 2.25.

## C. `deal` -- N same-framed stills, cross-fading

The machine the site is missing most. Every SEQUENCE brief above produces frames for
it, and right now the site has nowhere to put them.

```css
.cam-deal{position:relative}
.cam-deal img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
  opacity:0;animation:deal var(--dur,12s) linear infinite;
  animation-delay:calc(var(--i) * var(--dur,12s) / var(--n))}
.cam-deal img:first-child{opacity:1}   /* base layer, never fades */
@keyframes deal{
  0%      {opacity:0}
  4%,28%  {opacity:1}
  32%,100%{opacity:0}
}
```

The base layer stays opaque underneath so the loop point dissolves against a screen
rather than against the card, which is the detail the reference build gets right and
naive cross-fades get wrong. Each layer sets `--i`; the container sets `--n`.

Resting state is the first frame, so 2.17 doubles as the still fallback for the
island video and 2.20's first frame stands alone as a case-study opener.

**Fed by:** 2.7, 2.17, 2.20, 3.2, 3.10.

## D. `cursor` -- a pointer that visits the click points

`deal` alone shows screens changing. Paired with `cursor` it shows a person using
something, which is a different and better thing. `case-study.css` already has
`flow-cur`; this generalises it.

A small dot travels between coordinates on the same timing as the `deal` it sits
over, and pulses a ring at each stop just before the frame beneath it changes. The
stops are custom properties, so the same machine serves any sequence.

The half-second pause before each click that the capture rules ask for is the same
pause written into these keyframes. It is the single cheapest thing that makes an
interface sequence read as deliberate rather than nervous.

**Pairs with:** 3.2 (four drill levels), 2.20, 2.7.

## E. `sheet` -- a panel rising over a base screen

For anything where a surface arrives over another surface: the dorms quiz landing on
its results, a modal opening, a bottom sheet. The base screen never moves or fades,
so there is always something solid underneath.

Two layers and two properties: the panel translates up from `100%` to its resting
offset on a decelerating curve, and the base behind it dims slightly at the same
time. That dim is what sells the depth; without it the panel looks pasted on.

**Fed by:** 2.28 if assembled from stills rather than shot as video (capture the quiz
question, the last question, and the results panel, all at the same window size), and
by any Stardew popup that should be shown opening rather than open.

## F. `wipe` -- before and after under a moving seam

For the two before/after comparisons, and better than a cross-fade for them: a
cross-fade between two near-identical tables reads as a rendering glitch, while a
seam travelling across reads as a comparison.

One image over the other, the top one clipped with `clip-path: inset(0 var(--x) 0 0)`
animated across, with a 2px rule drawn at the seam so the eye has something to follow.
Holds at both ends, long enough to read each side.

Resting state is the seam parked at 50%, both halves visible, which is a perfectly
good still.

**Fed by:** 3.5, 3.8. Worth trying on 2.19's loader as well.

## G. `stagger` -- N children arriving in sequence

Not a camera over one still but a reveal across many, and the site already owns half
of it: `site-motion.js` adds `is-in` on scroll, and `char-in` and `rise-in` stagger
type. Extending the same idea to grids of things costs almost nothing.

```css
.cam-stagger > *{animation:rise-in .5s both;
  animation-delay:calc(var(--i) * var(--step,60ms))}
```

The count is the point: 34 villagers arriving one after another says "all 34" more
convincingly than the sentence does, and a contact sheet of component variants
arriving one at a time makes the reader count them without being asked.

**Fed by:** 2.3, 2.8, 3.7, and the art category grid, which currently arrives all at
once.

---

## What this adds up to

Seven machines, roughly 150 lines of CSS, and every capture in Parts 1 to 3 already
lands in one of them. The important consequence is for the recording session, not the
stylesheet: **shoot flat, shoot the widest state, and shoot sequences at identical
framing.** Anything shot that way can be re-timed, re-cropped and re-cameraed later
without going back to the browser. Anything shot with a zoom baked in is finished at
the moment it is recorded.

---

## Priority

**Do these first.** The site is currently wrong or empty without them.

1. **1.1 uxfolio** -- the tile is a flat navy rectangle today, and the cause is now
   known, so this is fifteen minutes
2. **2.14 island generator building itself** -- the algorithm is the whole project
3. **1.2 stardew** -- the tile shows a title screen and nothing else
4. **2.1 stardew gift lookup** -- the app's main claim, never shown
5. **2.28 dorms quiz** -- the backend is finally up, and it may not stay up

**Then the arcade**, 2.8 to 2.13, which is a whole half of the Stardew project that
the portfolio does not currently mention at all.

**Then the dashboard demo**, in this order: 3.8, 3.2, 3.5, 3.13. The full-height
detail page is one capture that fills the most slots; the drill and the network
boundary carry the most argument; the keyboard walkthrough is the one claim a still
cannot make. 3.5 needs a new plate on the page, which I can add.

**Not yet:** 3.19, which waits for the persona homepage to ship.

**Retire:** `assets/demo/`, once its slots are filled from the demo instead.
