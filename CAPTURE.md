# Capture request

Everything the site is still waiting on, in one list. Twenty-three captures across
six project pages and four case studies.

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
zooms across a phone screen following a conversation, `ds-scroll` runs a tall
documentation strip behind fixed chrome, `tile-scroll` and `tile-pan` drive the six
project thumbnails.

That approach wins on every axis. It stays sharp at any zoom because it is a
transform over a still, not a re-encode of one. It is a fraction of the file size. It
can be retimed later without re-recording. And it never has a cursor drifting or a
frame the encoder smeared.

**So: do not zoom while recording. Do not pan while recording. Do not add motion in
an editor.** Hold the frame still and let the interface be the only thing that moves.
Where a brief wants a camera move, capture the widest state as one flat asset and say
so; the movement is written afterwards as keyframes, and I will write them.

Two cases genuinely need video rather than a still with a camera over it: something
animating in the product itself (a state transition, a loading sequence), or a
keyboard walkthrough where focus moves. Those are 2.1 and 2.6, and they are marked.

**Video spec where it is needed:** 30fps, muted, H.264 mp4. 8 to 12 seconds unless a
brief says otherwise, which is shorter than it feels while recording. Start and end on
the same frame so it loops without a visible cut; record a few seconds spare at each
end and trim to matching frames.

**Cursor:** straight lines, and pause about half a second before every click. Real
usage is jittery and reads as nervous on replay. Two briefs want the cursor hidden;
they say so.

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

**CONFIDENTIALITY, for the four case studies.** These are captures of an internal
Capital One tool and the line already drawn on this site holds: mock data only, and
no internal product name, no internal URLs, no repository or pull-request links, and
no employer brand hex values anywhere in frame. Crop past the nav rail if a product
logo lives there. If a capture cannot be taken without one of those in shot, skip it
and say so.

---

# Part 1 — Project thumbnails

Six tiles on the home page. Each is a still image the page animates itself: a tall
capture that scrolls inside a browser frame, or a single screen that pans. **No
video here.** The CSS mechanism is smaller, sharper and keeps the drawn frame.

### 1.1 UI/UX Case Studies — BLOCKED, needed first

`kiara-vong.github.io/portfolio/` renders nothing in headless Chrome, so the current
tile is a flat navy rectangle. This is the one capture that must come from a real
browser.

- Full-page PNG at **1280 wide**, using ShareX's Scrolling Capture or the GoFullPage
  Chrome extension.
- Landing page, top of page, nothing hovered.
- Save as `assets/tile/_src/uxfolio.png`.

### 1.2 Stardew Companion — replace

Currently the game's title screen, which shows nothing about the project. The page
claims *"look up any villager's favourite gifts, click around town to learn what
each building is for."* The tile should show that.

- Full-page PNG at 1280 wide with the **villager list open**, gifts visible.
- If the page is tall enough to scroll (over ~1100px), it becomes a scrolling tile,
  which is better than a pan.
- `assets/tile/_src/stardew.png`

### 1.3 Dorms @ Brown — replace once the backend is up

Currently the landing page only, because the backend is down (see 3.2). The page
claims *"photos, plans, features and peer reviews."* The landing page shows none of
them.

- Full-page PNG at 1280 wide of a **single dorm's detail page**: photo, floor plan,
  features, reviews.
- `assets/tile/_src/dorms.png`

### 1.4 to 1.6 — already done, no action

Island Generator, Chess Engine and Pac-Man are current and correct. They pan rather
than scroll because each is a single-screen app with nothing below the fold.

---

# Part 2 — Case studies

Ten slots, already written into the pages as briefs with their sizes. Each renders at
the exact size of the finished asset, so anything that does not fit the slot on the
page will not fit when it is filled.

## Resource Dashboard

### 2.1 VIDEO — the three-tool reconciliation *(8-12s loop, cursor visible)*
The workflow before the dashboard existed. Proves the claim that the cost was in the
seams between tools, rather than asserting it.
1. Window 1: ownership lookup, paste an identifier
2. Window 2: the compliance job list, find the same resource
3. Window 3: the inventory, confirm what it actually is
4. End on all three open at once

**`assets/demo/` already holds ten cropped frames from your internal demo video.** If
they cover this sequence, this plate can be assembled from them without recording
anything. Ask before publishing employer video.

### 2.2 SEQUENCE — drilling four levels *(4 PNGs @2x, or one cross-fading loop)*
Environment, then region, then type, then the resource. Keep the breadcrumb visible
in every frame; it is what makes four images read as one movement. Same window size
and scroll position throughout.

### 2.3 ANNOTATED STILL — the default view *(PNG @2x, no OS chrome)*
One clean capture with four callouts: the urgency sort and why it is the default,
the view toggle, filters that persist across both views, and the export scoped to
what is on screen. **Leave ~120px clear on the right** for the labels.

## Events Timeline

### 2.4 STILL — the table alone *(PNG @2x, label EXPLORED)*
Before the timeline sat above it. Needs enough rows to make the date arithmetic look
tedious, and at least one violated-then-fixed pair several days apart.

### 2.5 SEQUENCE — naive vs carry-forward *(PNGs @2x, or a wipe)*
Two tracks stacked. Top: dots on a plain rule, gaps uncoloured (EXPLORED). Bottom:
the same dots with state carried across the gaps (SHIPPED). Identical dates and width
in both, so they read as one comparison rather than two pictures.

### 2.6 VIDEO — keyboard walkthrough *(10-14s, cursor HIDDEN)*
The whole timeline with no mouse. Tab onto the first dot with the focus ring visible,
Enter to open the popover, Escape to close, Tab to the Timestamp header, Enter to
re-sort. This is the accessibility claim; it cannot be made with a still.

## UI Redesign / Consistency

### 2.7 STILL — contact sheet of one component *(PNG @2x)*
Every live variant side by side, each cropped at the same zoom on a neutral ground.
**Keep their real spacing and radii. Do not tidy them** — the mess is the argument.
Caption each with the surface it came from. Component chrome only, no data.

### 2.8 STILL — before and after *(two PNGs @2x, or a slider)*
One table, identical data, identical window width, identical scroll position, so only
the styling differs. The 72px to 52px row height should be obvious. Label BEFORE and
AFTER rather than old and new.

### 2.9 STILL — filter chip, four states *(PNG @2x, 2x2 grid)*
One chip selected at full width; overflow showing the +N chip; dropdown open
mid-selection; typing with chips hidden. **Crop tight to the control**, not the page.

## Persona Homepage — after the first build ships

### 2.10 SEQUENCE — three orderings *(PNGs @2x, or a 3-state loop)*
Operator, Owner and Newcomer at the same window width, with one block tinted
identically in all three so the eye can track it moving. Persona switcher visible and
in its selected state.

---

# Part 3 — Features the site claims but never shows

These are not in the pages yet. Each one exists because a project page makes a claim
that currently has no picture behind it. Worth more than polishing what is already
covered.

### 3.1 VIDEO — Stardew: gift lookup *(8-10s loop)*
Page: *"look up any villager's favourite gifts."* Search a villager, open them, show
the gift list. The single most-used thing in the app and it is invisible on the site.

### 3.2 VIDEO — Dorms: the shortlist quiz *(10-12s loop)*
Page: *"a quiz that narrows thirty dorms to a shortlist worth touring."* Take the
quiz and land on the results. **Blocked on the backend** — `dab-w77u.onrender.com`
returns 404, so this needs a local run against a working instance, or the service
redeployed.

### 3.3 STILL or VIDEO — Dorms: peer reviews *(PNG @2x, or 6-8s)*
Page: *"photos, plans, features and peer reviews."* Reviews are named in the intro
and shown nowhere. One dorm's detail page with real review text visible. Same backend
blocker.

### 3.4 STILL — Stardew: the town map *(PNG @2x)*
Page: *"click around town to learn what each building is for."* The map with one
building selected and its description open.

### 3.5 SEQUENCE — UI/UX portfolio: one case study, end to end *(3-4 PNGs @2x)*
Page: *"each piece walks through the problem, what was tried, and what actually
shipped."* Three or four frames from a single case study showing that arc. This is
the claim the whole project rests on and there is currently no evidence for it.

### 3.6 VIDEO — Pac-Man: the frightened state *(6-8s loop)*
Page: *"the frightened state that briefly reverses all of it."* Eat a power pellet,
show all four ghosts reverse. Proves the ghost-behaviour claim in a way a static
maze cannot.

### 3.7 VIDEO — Island Generator: the island building itself *(8-12s loop)*
Page: *"built tile by tile... constraint propagation, everywhere after."* Wave
function collapse resolving from empty to finished. The algorithm is the project and
the current tile is a finished render, which shows the output and not the idea.

### 3.8 VIDEO — Chess: the engine thinking *(8-10s loop)*
Page: *"move generation, alpha-beta search."* A few moves played against the engine,
ideally with any depth or evaluation readout visible.

---

## Priority

**Do these first.** The site is currently wrong or empty without them.

1. **1.1 uxfolio** — the tile is a flat navy rectangle today
2. **3.7 island generator** — the algorithm is the whole project
3. **1.2 stardew** — the tile shows a title screen and nothing else
4. **3.6 pac-man frightened state** — cheap, and it is the page's main claim

**Then the case studies**, in this order: 2.1, 2.3, 2.6. Those three carry the most
argument. The remaining stills are useful but the pages hold without them.

**Blocked on the backend:** 1.3, 3.2, 3.3. Do not attempt until Dorms has a working
instance.

**Not yet:** 2.10, which waits for the persona homepage to ship.
