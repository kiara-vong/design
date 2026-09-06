# -*- coding: utf-8 -*-
"""Case-study figures: clean vector, self-animating, authored at .cs-media's size.

Replaces both earlier attempts. The screenshots-on-a-mat looked accurate and
inert, and a 1280px capture shrunk into a 799px frame loses the detail that made
it worth showing. The hand-drawn set held together but could not carry the
technical content -- a wobbly diagram of a dependency graph reads as a doodle,
not as an argument.

These are flat vector at exactly 799x391, so nothing is scaled and a 1px rule is
a 1px rule, and each one animates itself from a <style> the browser runs even when
the file is the src of an <img>. That keeps the choreography with the artwork
rather than in a stylesheet every page has to load.

Each figure is trying to make ONE point. If it needs a caption to explain what it
is showing, it is the wrong figure.
"""
import io

FW, FH = 799, 391      # .cs-media
HW, HH = 799, 307      # .cs-hero

PAPER = "#FFFFFF"
WASH = "#F7F5EA"
IVORY = "#F5F2E5"
INK = "#423E3D"
MUT = "#878676"
LINE = "#E3E1CC"
ACCENT = "#649F25"
GREEN = "#649F25"
BLUE = "#1F597B"
STEEL = "#2E6B8E"
VIOLET = "#8460C6"
GOLD = "#E8B84B"
RED = "#D2503F"
OK = "#4E9E5F"
NAVY = "#123A57"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def r(x, y, w, h, fill, rad=0, op=None, cls=None, stroke=None, sw=1.5, style=""):
    s = '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="%s"' % (
        x, y, w, h, rad, fill)
    if stroke:
        s += ' stroke="%s" stroke-width="%g"' % (stroke, sw)
    if op is not None:
        s += ' opacity="%.2f"' % op
    if cls:
        s += ' class="%s"' % cls
    if style:
        s += ' style="%s"' % style
    return s + '/>'


def c(cx, cy, rad, fill, op=None, cls=None, stroke=None, sw=2, style=""):
    s = '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"' % (cx, cy, rad, fill)
    if stroke:
        s += ' stroke="%s" stroke-width="%g"' % (stroke, sw)
    if op is not None:
        s += ' opacity="%.2f"' % op
    if cls:
        s += ' class="%s"' % cls
    if style:
        s += ' style="%s"' % style
    return s + '/>'


def t(x, y, s, size=13, fill=INK, fam="mono", weight=400, anchor="start", cls=None):
    fams = {"mono": "'ApercuMono','JetBrains Mono',ui-monospace,monospace",
            "sans": "'Diatype','Inter',system-ui,sans-serif",
            "serif": "'Mackinac','Fraunces',Georgia,serif"}
    o = ('<text x="%.1f" y="%.1f" font-family="%s" font-size="%g" font-weight="%s" '
         'fill="%s" text-anchor="%s"' % (x, y, fams[fam], size, weight, fill, anchor))
    if cls:
        o += ' class="%s"' % cls
    return o + '>%s</text>' % esc(s)


def bar(x, y, w, h=9, fill=LINE, cls=None, style=""):
    return r(x, y, w, h, fill, h / 2.0, cls=cls, style=style)


def title(x, y, s):
    return t(x, y, s, 17, INK, "serif", 600)


def sub(x, y, s):
    return t(x, y, s, 12, MUT, "mono")


def save(name, body, css, w=FW, h=FH, ground=PAPER):
    io.open("assets/case/%s.svg" % name, "w", encoding="utf-8").write(
        '<svg width="%d" height="%d" viewBox="0 0 %d %d" fill="none" '
        'xmlns="http://www.w3.org/2000/svg"><style>%s'
        '@media (prefers-reduced-motion:reduce){*{animation:none!important}}'
        '</style><rect width="%d" height="%d" fill="%s"/>%s</svg>\n'
        % (w, h, w, h, css, w, h, ground, body))
    print("  %s.svg" % name)


# =====================================================================
# 01  Resource Dashboard
# =====================================================================
def dash_seams():
    """The problem: three systems, one question, a person doing the joining."""
    o = [title(28, 40, "One question, three systems"),
         sub(28, 62, "the cost was never in any one tool")]
    SYS = [("ownership", BLUE), ("compliance jobs", GOLD), ("inventory", VIOLET)]
    for i, (nm, col) in enumerate(SYS):
        x = 46 + i * 240
        o.append(r(x, 96, 200, 128, WASH, 12, stroke=LINE, sw=2))
        o.append(r(x, 96, 200, 30, col, 12, op=.18))
        o.append(r(x, 112, 200, 14, col, 0, op=.18))
        o.append(t(x + 16, 117, nm, 12, col, "mono", 500))
        for k in range(3):
            o.append(bar(x + 18, 152 + k * 22, 164 - k * 34, 9, LINE))
        # Each one hands a fragment down to the person below.
        o.append('<path class="wire w%d" d="M %d 224 L %d 286" stroke="%s" '
                 'stroke-width="2.5" stroke-dasharray="6 6" fill="none"/>'
                 % (i, x + 100, 399, col))
    o.append(c(399, 306, 22, IVORY, stroke=MUT, sw=2.5))
    o.append(c(399, 300, 8, MUT))
    o.append('<path d="M 381 322 a 18 18 0 0 1 36 0" fill="%s"/>' % MUT)
    o.append(t(399, 364, "someone reconciling it by hand", 13, INK, "sans", 700,
               anchor="middle"))
    o.append(t(399, 384, "every time, forever", 12, MUT, "mono", 400, anchor="middle"))
    css = (".wire{opacity:0;stroke-dashoffset:60;animation:wr 6s ease-out infinite}"
           "@keyframes wr{0%{opacity:0;stroke-dashoffset:60}"
           "18%,88%{opacity:1;stroke-dashoffset:0}100%{opacity:0}}"
           ".w1{animation-delay:.35s}.w2{animation-delay:.7s}")
    return o, css


def tl_carry():
    """The one that matters: state carries across the gap between events."""
    o = [title(28, 40, "State carries across the gaps"),
         sub(28, 62, "the colour between the dots is the answer")]
    x0, tw = 60, FW - 120
    NAIVE_Y, GOOD_Y = 150, 286
    EVENTS = [(0.0, OK), (0.30, RED), (0.62, OK), (0.80, RED), (1.0, OK)]
    o.append(t(60, 118, "drawn naively", 12, MUT, "mono"))
    o.append(r(x0, NAIVE_Y - 2, tw, 4, LINE, 2))
    for a, col in EVENTS:
        o.append(c(x0 + tw * a, NAIVE_Y, 10, col))
    o.append(t(x0 + tw * .46, NAIVE_Y + 42,
               "reads as: nothing was wrong here", 12, MUT, "sans", 400, anchor="middle"))
    o.append(t(60, 254, "carrying state forward", 12, ACCENT, "mono", 500))
    o.append(r(x0, GOOD_Y - 3, tw, 6, LINE, 3))
    o.append('<g class="fill">')
    for i in range(len(EVENTS) - 1):
        a, col = EVENTS[i]
        b = EVENTS[i + 1][0]
        o.append(r(x0 + tw * a, GOOD_Y - 4, tw * (b - a), 8, col, 4,
                   cls="seg s%d" % i, style="animation-delay:%.2fs" % (i * .25)))
    o.append('</g>')
    for a, col in EVENTS:
        o.append(c(x0 + tw * a, GOOD_Y, 10, col))
        o.append(c(x0 + tw * a, GOOD_Y, 10, "none", stroke=PAPER, sw=3))
    o.append(t(x0 + tw * .46, GOOD_Y + 44,
               "reads as: five days in violation", 12, INK, "sans", 700, anchor="middle"))
    css = (".seg{opacity:0;transform-box:fill-box;transform-origin:0 50%;"
           "animation:sg 7s ease-out infinite}"
           "@keyframes sg{0%,8%{opacity:0;transform:scaleX(0)}"
           "24%,90%{opacity:1;transform:scaleX(1)}100%{opacity:0;transform:scaleX(0)}}")
    return o, css


def ui_drift():
    """Twenty-seven variants collapsing into nine components."""
    o = [title(28, 40, "Twenty-seven variants, four components"),
         sub(28, 62, "none of them wrong on their own page")]
    ROWS = [("Button", 9, ACCENT), ("Input", 7, BLUE), ("Modal", 5, VIOLET),
            ("Table", 6, GREEN)]
    y = 92
    import random as _rd
    rr = _rd.Random(11)
    for ri, (nm, n, col) in enumerate(ROWS):
        o.append(r(28, y, FW - 56, 58, WASH, 8))
        o.append(t(44, y + 28, nm, 13, INK, "sans", 700))
        o.append(t(44, y + 46, "%d variants" % n, 10, MUT, "mono"))
        for i in range(n):
            bx = 150 + i * 66
            o.append(r(bx, y + 16, 54 + rr.randint(-7, 7), 26 + rr.randint(-5, 5),
                       col, rr.choice([3, 6, 13]), op=.34 + .06 * (i % 4),
                       cls="v v%d" % ri, style="animation-delay:%.2fs" % (i * .04)))
            # Where each one lands once the system exists.
            o.append(r(150 + i * 66, y + 16, 54, 26, col, 6, op=.9,
                       cls="u u%d" % ri, style="animation-delay:%.2fs" % (i * .04)))
        y += 66
    o.append(r(28, y + 4, FW - 56, 1.5, LINE))
    o.append(t(28, y + 30, "27 variants  ->  9 components  ->  1 token layer",
               13, ACCENT, "mono", 500))
    css = (".v{animation:vv 8s ease-in-out infinite}"
           "@keyframes vv{0%,34%{opacity:.55}46%,90%{opacity:0}100%{opacity:.55}}"
           ".u{opacity:0;animation:uu 8s ease-in-out infinite}"
           "@keyframes uu{0%,34%{opacity:0}46%,90%{opacity:.9}100%{opacity:0}}")
    return o, css


def persona_reorder():
    BLOCKS = [("Tasks due", ACCENT), ("What I own", BLUE), ("Recent activity", GREEN),
              ("Team view", VIOLET), ("Getting started", GOLD)]
    ORDERS = [[0, 1, 2, 3, 4], [1, 3, 0, 2, 4], [4, 0, 1, 2, 3]]
    NAMES = ["Operator", "Owner", "Newcomer"]
    o = [title(28, 40, "The same blocks, ranked differently"),
         sub(28, 62, "colour follows one block across the three")]
    for i, nm in enumerate(NAMES):
        x = 28 + i * 254
        o.append(r(x, 88, 224, 30, VIOLET, 8, op=.12))
        o.append(t(x + 112, 108, nm, 12, VIOLET, "sans", 700, anchor="middle"))
        for rank, idx in enumerate(ORDERS[i]):
            label, col = BLOCKS[idx]
            bh = 44 - rank * 4
            y = 130 + sum(44 - k * 4 + 6 for k in range(rank))
            o.append(r(x, y, 224, bh, col, 7, op=.17,
                       cls="pb b%d" % rank, style="animation-delay:%.2fs" % (rank * .1)))
            o.append(r(x, y, 4, bh, col, 2, cls="pb b%d" % rank,
                       style="animation-delay:%.2fs" % (rank * .1)))
            o.append(t(x + 14, y + 22, label, 10, col, "sans", 700,
                       cls="pb b%d" % rank))
    css = (".pb{opacity:0;animation:pb 7s ease-out infinite}"
           "@keyframes pb{0%{opacity:0;transform:translateY(8px)}"
           "14%,90%{opacity:1;transform:translateY(0)}100%{opacity:0}}")
    return o, css



def pac_targets():
    """Pac-Man's actual argument: one movement system, four target rules.

    Every screenshot of this game shows the same thing -- a maze, some dots, four
    ghosts -- and none of them show the only part worth writing about, which is
    that the four ghosts run identical code against four different target tiles.
    That is not a visible property of any one frame. It is the rule behind all of
    them, so it wants a diagram rather than a capture.

    Four panels rather than one board, and that is the whole design. A single
    board with four leader lines on it was tried first: the lines crossed, the
    ghosts overlapped in the middle where they start, and reading it meant
    tracing four paths through one picture. Four small boards make the comparison
    the layout instead of the reader's job -- same fragment, same player, same
    position, one ghost each, and the only thing that moves between panels is the
    highlighted tile. Which is exactly the claim.
    """
    o = [title(28, 40, "One movement system, four targets"),
         sub(28, 62, "identical code; the ghosts differ only in the tile they aim at")]

    CELL = 25
    COLS = ROWS = 5
    PANEL_W = 178
    BOARD = COLS * CELL                       # 135
    TOP = 92
    BOARD_Y = TOP + 30

    # Same fragment in all four: player mid-board, facing left.
    PC, PR = 2, 2

    GHOSTS = [
        # name, colour, ghost cell, target cell, rule, note
        ("Blinky", "#E4483C", (4, 0), (2, 2), "the player's tile",
         "chases directly"),
        ("Pinky",  "#F2A9CE", (0, 0), (0, 2), "four tiles ahead",
         "cuts you off"),
        ("Inky",   "#5FD4E8", (4, 4), (4, 0), "reflected through Blinky",
         "needs Blinky too"),
        ("Clyde",  "#EFA24B", (2, 4), (0, 4), "his corner, when close",
         "gives up nearby"),
    ]

    for i, (nm, col, (gc, gr), (tc, tr), rule, note) in enumerate(GHOSTS):
        px = 28 + i * PANEL_W
        bx = px + (PANEL_W - BOARD) / 2.0 - 6

        o.append(t(px + 2, TOP + 14, nm, 12, col, "sans", 700))
        o.append(t(px + 2 + len(nm) * 8 + 8, TOP + 14, note, 10, MUT, "mono", 400))

        # the board fragment
        o.append(r(bx - 7, BOARD_Y - 7, BOARD + 14, BOARD + 14, "#0E1017", 9))
        for k in range(COLS + 1):
            o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                     'stroke="#26314A" stroke-width="1"/>'
                     % (bx + k * CELL, BOARD_Y, bx + k * CELL, BOARD_Y + BOARD))
            o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                     'stroke="#26314A" stroke-width="1"/>'
                     % (bx, BOARD_Y + k * CELL, bx + BOARD, BOARD_Y + k * CELL))

        def cx(c, _bx=bx):
            return _bx + c * CELL + CELL / 2.0

        def cy(rr):
            return BOARD_Y + rr * CELL + CELL / 2.0

        # the target tile -- the one thing that differs between panels
        o.append(r(bx + tc * CELL + 2.5, BOARD_Y + tr * CELL + 2.5,
                   CELL - 5, CELL - 5, col, 4, op=.26,
                   cls="tgt p%d" % i))
        o.append(r(bx + tc * CELL + 2.5, BOARD_Y + tr * CELL + 2.5,
                   CELL - 5, CELL - 5, "none", 4, stroke=col, sw=1.6,
                   cls="tgt p%d" % i))

        # ghost -> target
        if (gc, gr) != (tc, tr):
            o.append('<path class="aim p%d" d="M %.1f %.1f L %.1f %.1f" '
                     'stroke="%s" stroke-width="1.8" stroke-dasharray="4 4" '
                     'fill="none"/>'
                     % (i, cx(gc), cy(gr), cx(tc), cy(tr), col))

        # the player, facing left, identical in every panel
        o.append('<path d="M %.1f %.1f L %.1f %.1f A 9 9 0 1 0 %.1f %.1f Z" '
                 'fill="#F2C744"/>'
                 % (cx(PC), cy(PR), cx(PC) - 8.5, cy(PR) - 3.1,
                    cx(PC) - 8.5, cy(PR) + 3.1))

        # the ghost
        o.append('<path class="gh p%d" d="M %.1f %.1f a 8 8 0 0 1 16 0 v 9.5 '
                 'l -2.7 -2.7 l -2.7 2.7 l -2.6 -2.7 l -2.7 2.7 l -2.7 -2.7 '
                 'l -2.6 2.7 z" fill="%s"/>'
                 % (i, cx(gc) - 8, cy(gr), col))

        o.append(t(px + 2, BOARD_Y + BOARD + 26, "aims at", 9, MUT, "mono", 400))
        o.append(t(px + 2, BOARD_Y + BOARD + 42, rule, 11, INK, "sans", 700))

    # the shared rule, stated once, under all four
    y = BOARD_Y + BOARD + 56
    o.append('<line x1="28" y1="%.1f" x2="771" y2="%.1f" stroke="%s" '
             'stroke-width="1"/>' % (y, y, LINE))
    o.append(t(28, y + 22, "At every junction each of them runs the same "
               "comparison: take the exit that most reduces the distance to my "
               "target.", 12, INK, "sans", 400))
    o.append(t(28, y + 40, "Frightened mode does not replace that rule. It flips "
               "the comparison to the exit that INCREASES it.", 11, MUT, "sans", 400))

    css = (
        ".tgt{animation:tgt 8s ease-out infinite}"
        "@keyframes tgt{0%,6%{opacity:.45}18%,80%{opacity:1}94%,100%{opacity:.45}}"
        ".aim{stroke-dashoffset:60;animation:aim 8s ease-out infinite}"
        "@keyframes aim{0%,6%{stroke-dashoffset:60;opacity:.5}"
        "22%,80%{stroke-dashoffset:0;opacity:1}94%,100%{stroke-dashoffset:60;opacity:.5}}"
        ".gh{animation:gh 8s ease-out infinite}"
        "@keyframes gh{0%,6%{opacity:.62}18%,80%{opacity:1}94%,100%{opacity:.62}}"
        ".p1{animation-delay:.3s}.p2{animation-delay:.6s}.p3{animation-delay:.9s}"
    )
    return o, css


print("case-study figures:")
FIGS = [
    ("cs-dash-seams", dash_seams),
    ("cs-tl-carry", tl_carry),
    ("cs-ui-drift", ui_drift),
    ("cs-persona-reorder", persona_reorder),
    ("cs-pac-targets", pac_targets),
]
for name, fn in FIGS:
    body, css = fn()
    save(name, "".join(body), css)
