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
    # No title on this one. It is the page's cover, and the page opens two
    # centimetres below it with a kicker, a title and an intro that say the same
    # thing in better words. A caption inside a cover image is a caption competing
    # with the headline it sits above.
    o = []
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
    """One track, not two: the same events, read the wrong way and then the right
    way, without the reader having to hold two pictures at once.

    It was two tracks stacked, one labelled naive and one labelled carried, which
    is a comparison the reader assembles themselves. A cover has about two seconds
    to make its point, and two seconds is not enough to look twice. So there is
    one timeline now, the dots land on it, and then the colour floods forward out
    of each event into the gap after it -- which is not an illustration of the
    idea, it IS the idea: state carries forward until something changes it.

    No title across the top. This is the cover of a page that opens two
    centimetres below it with a kicker, a headline and an intro, and a caption
    inside a cover image is a caption competing with the headline above it.
    """
    o = []
    # Authored at .cs-hero's own 799x307 rather than the 799x391 the in-page
    # figures use. The hero draws with object-fit:cover, so a 391-tall cover loses
    # 42 pixels off the top and 42 off the bottom -- which the other covers were
    # composed around by accident rather than on purpose. At the real size there
    # is nothing to compose around.
    X0, TW, TY = 70, FW - 140, 85
    # 0.30 to 0.62 of the track is the violated span, and the whole figure is
    # built to put a bracket under exactly that.
    EV = [(0.00, OK), (0.30, RED), (0.62, OK), (0.80, RED), (1.00, OK)]

    o.append(r(X0, TY - 3, TW, 6, LINE, 3))

    # the gaps, flooding forward out of the event on their left
    o.append('<g class="flood">')
    for i in range(len(EV) - 1):
        aa, col = EV[i]
        bb = EV[i + 1][0]
        o.append(r(X0 + TW * aa, TY - 4, TW * (bb - aa), 8, col, 4,
                   cls="seg", style="animation-delay:%.2fs" % (2.3 + i * .34)))
    o.append('</g>')

    # the events themselves, landing left to right
    for i, (aa, col) in enumerate(EV):
        cx = X0 + TW * aa
        o.append(c(cx, TY, 11, col, cls="dot",
                   style="animation-delay:%.2fs" % (i * .2)))
        o.append(c(cx, TY, 11, "none", stroke=PAPER, sw=3, cls="dot",
                   style="animation-delay:%.2fs" % (i * .2)))
        o.append(r(cx - .5, TY + 18, 1, 9, LINE, cls="dot",
                   style="animation-delay:%.2fs" % (i * .2)))

    for aa, lab, anc in ((0.0, "Aug 8", "start"), (0.62, "Aug 23", "middle"),
                         (1.0, "Now", "end")):
        o.append(t(X0 + TW * aa, TY + 46, lab, 11, MUT, "mono", anchor=anc))

    # the bracket under the span the argument is about
    bx0, bx1 = X0 + TW * .30, X0 + TW * .62
    by = TY + 70
    o.append('<g class="span">')
    o.append(r(bx0, by, bx1 - bx0, 2, RED, 1, op=.55))
    o.append(r(bx0, by - 7, 2, 9, RED, 1, op=.55))
    o.append(r(bx1 - 2, by - 7, 2, 9, RED, 1, op=.55))
    o.append(t((bx0 + bx1) / 2.0, by + 26, "five days in violation",
               13, INK, "sans", 700, anchor="middle"))
    o.append('</g>')

    # the two readings, one at a time, in the same place
    o.append(t(FW / 2.0, TY + 120, "five events, and four gaps",
               12, MUT, "mono", anchor="middle", cls="read a"))
    o.append(t(FW / 2.0, TY + 120,
               "the gap is coloured by what happened before it",
               12, ACCENT, "mono", 500, anchor="middle", cls="read b"))

    css = ("""
    .dot{opacity:0;transform-box:fill-box;transform-origin:50% 50%;
         animation:tl-dot 9s ease-out infinite}
    @keyframes tl-dot{0%{opacity:0;transform:scale(.3)}
      6%{opacity:1;transform:scale(1.25)}10%,88%{opacity:1;transform:scale(1)}
      96%,100%{opacity:0;transform:scale(.3)}}
    .seg{transform-box:fill-box;transform-origin:0 50%;transform:scaleX(0);
         animation:tl-seg 9s cubic-bezier(.3,.7,.3,1) infinite}
    @keyframes tl-seg{0%{transform:scaleX(0)}
      7%,86%{transform:scaleX(1)}94%,100%{transform:scaleX(0)}}
    .span{opacity:0;animation:tl-span 9s ease-out infinite}
    @keyframes tl-span{0%,52%{opacity:0}60%,86%{opacity:1}92%,100%{opacity:0}}
    .read{opacity:0;animation:tl-read 9s ease-in-out infinite}
    .read.a{animation-name:tl-read-a}
    .read.b{animation-name:tl-read-b}
    @keyframes tl-read-a{0%,4%{opacity:0}10%,26%{opacity:1}34%,100%{opacity:0}}
    @keyframes tl-read-b{0%,38%{opacity:0}46%,88%{opacity:1}94%,100%{opacity:0}}
    """)
    return o, css


def ui_drift():
    """Twenty-seven variants collapsing into nine components."""
    # No caption across the top: this is a cover, and the page's own kicker,
    # headline and intro sit two centimetres under it saying the same thing with
    # more room to say it in.
    o = []
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
    # No caption across the top: this is a cover, and the page's own kicker,
    # headline and intro sit two centimetres under it saying the same thing with
    # more room to say it in.
    o = []
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




def pac_man(cx, cy, r, mouth=38, facing=180, fill="#F2C744"):
    """A Pac-Man wedge with no arc commands in it.

    mouth  the full opening in degrees, facing  the direction it points (180 is
    left, screen coordinates). The circle is walked in one-degree steps from one
    lip to the other, which at this size is indistinguishable from an arc and
    cannot be drawn inside out.
    """
    import math
    a0 = facing + mouth / 2.0
    a1 = facing + 360.0 - mouth / 2.0
    pts = []
    n = int(a1 - a0)
    for i in range(n + 1):
        a = math.radians(a0 + i)
        pts.append("%.2f %.2f" % (cx + r * math.cos(a), cy + r * math.sin(a)))
    return ('<path d="M %.2f %.2f L %s Z" fill="%s"/>'
            % (cx, cy, " L ".join(pts), fill))


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

        # the player, facing left, identical in every panel.
        #
        # Drawn as a fan of short segments rather than as an SVG arc. The arc
        # version put the wedge's apex at the sphere's centre and then asked for
        # a radius-9 arc between two points 9.05 apart from it -- so the renderer
        # placed the arc's OWN centre wherever it had to, the circle slid off the
        # apex, and what came out was a yellow triangle stuck to the side of a
        # ball. A/@sweep flags are a bad place to be clever at nine pixels wide.
        o.append(pac_man(cx(PC), cy(PR), 9.2, 38))

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



# =====================================================================
# 02b Events Timeline -- four events on one day
# =====================================================================
def tl_collapse():
    """The clustering problem and the answer to it, side by side.

    The section that needs this figure describes three options and picks one, and
    a reader cannot weigh three options they have not seen. Drawn rather than
    captured because the losing two never shipped: there is no screenshot of the
    overlap bug, and there never should be.
    """
    o = []
    CY = 170

    def track(x0, x1, y):
        return [r(x0, y - 2, x1 - x0, 4, LINE, 2)]

    # ---- left: what four events on one day actually look like ----------
    o += [t(46, 58, "drawn where they happened", 12, MUT, "mono", 500),
          t(46, 82, "four events, one day", 15, INK, "sans", 600)]
    o += track(46, 330, CY)
    for i, col in enumerate((RED, GOLD, GOLD, OK)):
        o.append(c(188 + i * 3.5, CY, 11, col, stroke=PAPER, sw=2.5))
    o += [t(188, CY + 44, "one pixel, four dots", 11, MUT, "mono", anchor="middle"),
          t(188, CY + 62, "reads as a rendering fault", 11, MUT, "mono",
            anchor="middle")]
    for x, lab in ((46, "Aug 8"), (330, "Now")):
        o += [r(x, CY + 12, 1, 8, LINE),
              t(x, CY + 34, lab, 11, MUT, "mono",
                anchor="start" if x < 200 else "end")]

    # ---- right: collapsed, with the detail one interaction away --------
    o += [t(452, 58, "collapsed, position kept", 12, ACCENT, "mono", 500),
          t(452, 82, "one dot, four events", 15, INK, "sans", 600)]
    o += track(452, 752, CY)
    o.append(c(594, CY, 13, INK, cls="dot"))
    o.append(t(594, CY + 4.5, "4", 11, PAPER, "mono", 600, "middle"))
    for x, lab in ((452, "Aug 8"), (752, "Now")):
        o += [r(x, CY + 12, 1, 8, LINE),
              t(x, CY + 34, lab, 11, MUT, "mono",
                anchor="start" if x < 600 else "end")]

    # the popover the dot opens
    px, py = 500, 226
    o.append(r(px, py, 188, 112, PAPER, 10, stroke=LINE, sw=1.5, cls="pop"))
    rows = (("Policy Violated", RED), ("Fix Failed", GOLD),
            ("Fix Retried", GOLD), ("Auto Fix Completed", OK))
    for i, (lab, col) in enumerate(rows):
        y = py + 26 + i * 22
        o.append(c(px + 16, y - 4, 4.5, col, cls="pop"))
        o.append(t(px + 30, y, lab, 11, INK, "mono", cls="pop"))
    # No header on the popover. It sat exactly where the axis labels sit and the
    # two collided; the caption underneath says the same thing with more room.

    css = ("""
    .dot{transform-box:fill-box;transform-origin:50% 50%;
         animation:tlc-dot 6s ease-in-out infinite}
    @keyframes tlc-dot{0%,42%{transform:scale(1)}
      50%,88%{transform:scale(1.18)}96%,100%{transform:scale(1)}}
    .pop{opacity:0;animation:tlc-pop 6s ease-in-out infinite}
    @keyframes tlc-pop{0%,44%{opacity:0}54%,86%{opacity:1}94%,100%{opacity:0}}
    """)
    return o, css


print("case-study figures:")
# (name, builder) or (name, builder, width, height). Only the timeline cover is
# authored at the hero's own size so far; the rest are 799x391 and lose a band top
# and bottom to object-fit:cover, which they were composed around.


def sdv_chart():
    """One generated chart, two things reading it, and no file between them.

    The claim in that section is that the beatmap and the music are the same
    object rather than a track with a chart placed on top of it -- so they cannot
    drift, because there is nothing to drift. A screenshot of the game shows
    notes falling, which is the half of that anyone would have assumed. What it
    cannot show is the other consumer: the same sixteen marks are also what
    schedules the oscillators, in one pass at load.

    So both consumers are drawn under one track, driven by one set of delays. If
    the two halves of this picture ever fell out of step it would be because the
    same arithmetic that generates them fell out of step, which is the property
    being described.
    """
    BEATS = 16
    LOOP = 8.0
    STEP = LOOP / BEATS
    LANE = [0, 2, 1, 3, 0, 1, 2, 2, 3, 1, 0, 3, 2, 0, 1, 3]
    COL = ["#649F25", "#1F597B", "#B4552F", "#8460C6"]

    X0, X1 = 62, 738
    TRACK_Y = 86
    SPAN = (X1 - X0) / float(BEATS - 1)

    o = [t(28, 42, "ONE GENERATED CHART", 11, MUT, "mono", 700),
         t(232, 42, "sixteen measures, written at load", 11, MUT, "sans", 400)]

    # the chart itself: one mark per beat, coloured by the lane it belongs to
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" '
             'stroke-width="1.5"/>' % (X0 - 14, TRACK_Y, X1 + 14, TRACK_Y, LINE))
    for i in range(BEATS):
        x = X0 + i * SPAN
        o.append('<rect class="mk" style="animation-delay:%.3fs" x="%.1f" y="%d" '
                 'width="9" height="9" rx="2.5" fill="%s"/>'
                 % (i * STEP, x - 4.5, TRACK_Y - 4.5, COL[LANE[i]]))

    # the two consumers
    PY_, PH = 132, 196
    for px, pw, name, sub_ in ((28, 356, "THE FALLING NOTES", "read every frame"),
                               (416, 356, "THE OSCILLATORS",
                                "scheduled once, at load")):
        o.append(r(px, PY_, pw, PH, "#FFFFFF", 10, stroke=LINE, sw=1.5))
        o.append(t(px + 14, PY_ + 22, name, 10.5, MUT, "mono", 700))
        o.append(t(px + 14, PY_ + 38, sub_, 10.5, MUT, "sans", 400))
        # the fork from the track down into each panel
        cxp = px + pw / 2.0
        o.append('<path d="M%.1f %d C%.1f %d %.1f %d %.1f %d" stroke="%s" '
                 'stroke-width="1.5" fill="none"/>'
                 % (400, TRACK_Y + 12, 400, TRACK_Y + 40, cxp, PY_ - 34,
                    cxp, PY_, LINE))

    # left panel: four lanes, notes falling to a judgment line
    LX, LW = 42, 328
    LANE_W = LW / 4.0
    JUDGE = PY_ + PH - 34
    for k in range(4):
        lx = LX + k * LANE_W
        o.append(r(lx + 6, PY_ + 50, LANE_W - 12, PH - 84, COL[k], 5, op=.07))
    o.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" '
             'stroke-width="2"/>' % (LX + 4, JUDGE, LX + LW - 4, JUDGE, LINE))
    for i in range(BEATS):
        k = LANE[i]
        lx = LX + k * LANE_W + LANE_W / 2.0
        o.append('<circle class="nt" style="animation-delay:%.3fs" cx="%.1f" '
                 'cy="%.1f" r="7" fill="%s"/>'
                 % (i * STEP, lx, PY_ + 56, COL[k]))
    for k in range(4):
        lx = LX + k * LANE_W + LANE_W / 2.0
        o.append('<circle cx="%.1f" cy="%.1f" r="9" fill="none" stroke="%s" '
                 'stroke-width="1.5"/>' % (lx, JUDGE, LINE))

    # right panel: one bar per beat, rising as its mark is reached
    RX, RW = 430, 328
    BW = RW / float(BEATS)
    BASE = PY_ + PH - 30
    for i in range(BEATS):
        h = 16 + (LANE[i] + 1) * 15
        o.append('<rect class="os" style="animation-delay:%.3fs" x="%.1f" '
                 'y="%.1f" width="%.1f" height="%d" rx="2" fill="%s"/>'
                 % (i * STEP, RX + i * BW + 2.5, BASE - h, BW - 5, h,
                    COL[LANE[i]]))
    o.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" '
             'stroke-width="2"/>' % (RX - 2, BASE, RX + RW + 2, BASE, LINE))

    o.append(t(28, 356, "The beatmap and the music are the same object. Difficulty "
               "changes note density and the timing windows, not the song.",
               12, INK, "sans", 400))

    css = (
        ".mk{opacity:.3;transform-box:fill-box;transform-origin:50%% 50%%;"
        "animation:mk %ss linear infinite}"
        "@keyframes mk{0%%,3%%{opacity:1;transform:scale(1.5)}"
        "12%%,100%%{opacity:.3;transform:scale(1)}}"
        ".nt{opacity:0;animation:nt %ss linear infinite}"
        "@keyframes nt{0%%{opacity:0;transform:translateY(-14px)}"
        "6%%{opacity:1}"
        "34%%{opacity:1;transform:translateY(%dpx)}"
        "40%%,100%%{opacity:0;transform:translateY(%dpx)}}"
        ".os{opacity:.12;transform-box:fill-box;transform-origin:50%% 100%%;"
        "animation:os %ss linear infinite}"
        "@keyframes os{0%%{opacity:.12;transform:scaleY(.18)}"
        "4%%{opacity:1;transform:scaleY(1)}"
        "18%%,100%%{opacity:.12;transform:scaleY(.18)}}"
        % (LOOP, LOOP, int(JUDGE - (PY_ + 56)), int(JUDGE - (PY_ + 56)), LOOP))
    return "".join(o), css

FIGS = [
    ("cs-dash-seams", dash_seams),
    ("cs-tl-carry", tl_carry, HW, HH),
    ("cs-tl-collapse", tl_collapse),
    ("cs-ui-drift", ui_drift),
    ("cs-persona-reorder", persona_reorder),
    ("cs-pac-targets", pac_targets),
    ("cs-sdv-chart", sdv_chart),
]
for spec in FIGS:
    name, fn = spec[0], spec[1]
    body, css = fn()
    if len(spec) > 2:
        save(name, "".join(body), css, spec[2], spec[3])
    else:
        save(name, "".join(body), css)
