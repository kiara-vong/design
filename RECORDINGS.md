# Recordings to capture

Everything below is a thing the pages already claim and cannot currently show. It
is ordered by how much each one is carrying: the first section is footage that is
standing in for itself right now, the second is footage that exists but is framed
wrong, the third is what would make the pages better rather than merely honest.

---

## The capture spec

One shape for everything, because the figures are built around it.

| | |
|---|---|
| **Aspect** | 16:9, always |
| **Record at** | 2880 × 1620 (a 1440 × 810 window on a 2× display) |
| **Frame rate** | 30fps is plenty; 60 if the tool offers it free |
| **Length** | 8–12 seconds. A loop nobody watches to the end proves nothing |
| **Cursor** | visible for anything where a click or a hover is the point |
| **Chrome** | none. No browser scrollbar in frame — hide it before recording |
| **Stills** | same window, same 2880 × 1620, PNG |

Two notes that have cost real work:

**The scrollbar.** Eleven captures had one baked into an edge, including three
videos, and on the dark ones it read as a border rather than as a mistake. Before
recording, run this in the console once:

```js
document.head.appendChild(Object.assign(document.createElement('style'),
  {textContent:'::-webkit-scrollbar{display:none}html{scrollbar-width:none}'}))
```

**Why 16:9 specifically.** The figures now hold the capture at its authored size
and move a camera over it, rather than cropping it to fit. The detail framing is
exactly 1:1, so a 2× capture is pixel-perfect at the closest the camera ever gets.
Off-spec captures still work — the maths follows whatever size you give it — but
they cannot be as sharp, and the resting framing gets more letterboxing the
further from 16:9 they are.

---

## 1. Standing in for itself

Seven clips on the site are not recordings. They are sparse screenshot states
cross-dissolved together, built deliberately as an honest placeholder, and three
of the captions **say so on the page**:

> "Four states standing in for the run until this one gets a real recording."
> "three states where the actual note timing belongs once there's a real capture"
> "The counter and the health both move considerably faster than this in the actual game."

These are games and solvers. Motion is the subject, so a dissolve between stills
cannot stand in for it — you can see the frames.

### Stardew — the four arcade cabinets

Live at `kiara-vong.github.io/stardew`, Arcade section.

| Clip | Record | Must be in frame |
|---|---|---|
| `stardew-junimo-kart` | One run: start line, a cleared jump, a spike hit, the score screen | The score screen resetting. The page says "the score screen it resets from" |
| `stardew-prairie-king` | Two waves: spawn, wave cleared, a hit taken, counter climbing | The wave counter and the health, at real speed — the caption currently apologises for the pace |
| `stardew-junimo-jamboree` | Difficulty select, then notes falling in four lanes, then a cleared song | Actual note timing against the music. This is the whole claim |
| `stardew-fishing` | Cast, bite, the catch bar, a landed fish | The catch bar moving. Page says its physics were ported to the original tick rate — that is a claim about *motion* |

If Jamboree only gets one take, make it **Hard** — note density is what differs
between difficulties, and the difficulty select still is already on the page.

### Chess

`kiara-vong.github.io/site/projects/chess/`

| Clip | Record | Must be in frame |
|---|---|---|
| `chess-autoplay` | Both sides on the site's own AI, no human moves, ~20 moves in | The board going from a sane opening to a mess. The argument is that the engine is bad, so let it be bad on camera |

### Pac-Man

`kiara-vong.github.io/site/projects/pacman/`

| Clip | Record | Must be in frame |
|---|---|---|
| `pacman-gameplay` | A round: countdown, a clean run, a cornering, a death, the restart | **Frightened mode.** Eat a power pellet and let the ghosts turn blue |

Frightened mode is the one thing worth having and the current footage never
reaches it. The page argues that the state everyone remembers is four lines of
code because the movement system inverts rather than branches — and there is no
frame of blue ghosts anywhere on the site.

Heads-up: the game hangs on a "Loading…" screen because `pacman.js` fetches five
`.ogg` files from an unrelated GitHub repo and waits for a load event that never
fires. It also runs at ~1fps in an automated tab. Recording it by hand in a normal
foreground tab avoids both. If it hangs, this in the console before it loads gets
past it:

```js
const p = HTMLMediaElement.prototype, orig = p.addEventListener;
p.addEventListener = function (t, fn, o) {
  if (/canplay|loadeddata/.test(t)) return setTimeout(() => fn.call(this, new Event(t)), 40);
  return orig.call(this, t, fn, o);
};
```

### Animal Crossing — the solver

`kiara-vong.github.io/animal-crossing`

| Clip | Record | Must be in frame |
|---|---|---|
| `island-generator-building` | Hold space and let it fill from empty to finished | The *rate*. The claim is "the most constrained cell that was left" — the pace of collapse is the evidence |

---

## 2. Framed wrong

Footage that exists and is fine, but was captured in a shape that fights the
figure.

### ~~Dorms — the review card~~ · done

Your full-page shot of the Wellness page solved this. The figure now carries the
rating summary, the write-a-review form and a real review, and no student name
appears anywhere — so the caption no longer has to promise blurring.

### ~~Dorms — the quiz~~ · done

Your two shots — the quiz with its answers chosen, and the ranked shortlist —
register as two states of one page, so the figure cross-fades between them in a
single framing: preferences in, three dorms out. That reads better than the clip
did, so the old `dorms-quiz.mp4` is now unused. **Nothing to re-record here.**

---

## 3. Worth having

Nothing here is broken. These are the gaps where the page makes an argument in
prose that a figure would make better.

### Resource Dashboard

| Clip | Record | Why |
|---|---|---|
| `dashboard-graph-view` | The graph view being explored — a node opened, the layout settling | The page shows the table view twice and the graph view once, statically. The toggle is a headline claim |

### Events Timeline

| Clip | Record | Why |
|---|---|---|
| `timeline-hover-gap` | Hovering a coloured gap between two events so the popover names the state | "The colour between the dots is the answer." A still shows the colour; only motion shows that it is *readable* |

### UI Consistency

| Still | Shoot | Why |
|---|---|---|
| `theme-switch` | The same screen before and after the ThemeProvider, same window, same scroll | There is a before/after for tables but not for the theme foundation, which is section 1 of the showcase |

### Stardew

| Clip | Record | Why |
|---|---|---|
| `stardew-explore-valley` | Opening Explore the Valley and scrolling the panel | The page argues the outdoor areas are one long panel rather than a box each. That is a scrolling behaviour shown as a still |

---

## Where to put them

Videos → `assets/video/<name>.mp4`, and a poster frame is generated for you.
Stills → `assets/tile/_src/<name>.png`.

The names in the tables are the existing asset names; keeping them means the
figures pick the new footage up with no code change. Anything new can be named
freely — tell me the name and what it shows and I'll wire it in.

## What I'll do when they land

Re-time each clip to the 8–12 second band, cut the browser chrome if any survives,
generate posters, and set each figure's camera from the new capture — the framing
is a rectangle read off the footage now, so it goes where you say rather than
where a percentage happens to land.
