# -*- coding: utf-8 -*-
"""Drawn, self-animating thumbnails for the four work cards.

Two things going on here.

First, drawn instead of screenshotted. The captures looked accurate and read as
four unrelated rectangles at 480px wide -- and half the detail in a 1280px product
screenshot is illegible at that size anyway. A drawing can say what the screen
DOES; a shrunken screenshot only says that a screen exists.

Second, each file animates itself. The reference build drove its card animations
from the page stylesheet, which meant the choreography for four specific images
lived in a sheet every page loaded. An <img> still runs a <style> embedded in the
SVG it points at, so the animation travels with the artwork instead: the card
markup is four identical <img> tags and there is nothing in index.html to keep in
sync with a redraw. Reduced-motion handling rides along in the same block.

Authored in the shared 1200x700 cast, which the card scales to 0.40.
"""
import io
from gen.uikit import (rect, bar, lines, text, esc, W, H, INK, MUT, LINE, PAPER,
                   WASH, ACCENT, GREEN, BLUE, VIOLET)

DARK = "#0F2233"
NAVY = "#123A57"
STEEL = "#2E6B8E"
RED = "#D2503F"
OK = "#4E9E5F"
AMBER = "#E8B84B"
# Not GREEN: it and ACCENT are two greens nobody can tell apart at 480px, and
# telling them apart is the whole job the colour does on the persona card.
RUST = "#B4552F"


def doc(body, css):
    return ('<svg width="%d" height="%d" viewBox="0 0 %d %d" fill="none" '
            'xmlns="http://www.w3.org/2000/svg"><style>%s'
            '@media (prefers-reduced-motion:reduce){*{animation:none!important}}'
            '</style>%s</svg>\n' % (W, H, W, H, css, body))


def save(name, body, css):
    io.open("assets/cards/%s.svg" % name, "w", encoding="utf-8").write(doc(body, css))
    print("  %s.svg" % name)


def chrome(title, accent=ACCENT):
    """The window every thumbnail sits in."""
    o = [rect(0, 0, W, H, PAPER, 16), rect(0, 0, W, 52, WASH, 16),
         rect(0, 36, W, 16, WASH),
         '<line x1="0" y1="52" x2="%d" y2="52" stroke="%s" stroke-width="1.5"/>' % (W, LINE)]
    for i, c in enumerate(("#E6685C", "#E8B84B", "#7DC26B")):
        o.append('<circle cx="%d" cy="26" r="6.5" fill="%s"/>' % (28 + i * 22, c))
    o.append(rect(108, 13, 430, 26, PAPER, 13, LINE))
    o.append(text(126, 31, title, 13, MUT, "'JetBrains Mono',monospace"))
    o.append(rect(W - 96, 13, 62, 26, accent, 13, op=.16))
    return "".join(o)


def sidebar(active=1, accent=BLUE, w=196):
    o = [rect(0, 52, w, H - 52, NAVY),
         '<circle cx="30" cy="86" r="11" fill="%s"/>' % accent]
    o.append(bar(50, 81, 74, 10, "#3E6B8C"))
    for i in range(6):
        yy = 126 + i * 40
        if i == active:
            o.append(rect(12, yy - 4, w - 24, 32, accent, 8, op=.30))
        o.append(rect(26, yy + 5, 13, 13, accent if i == active else "#3E6B8C", 3))
        o.append(bar(50, yy + 7, 62 + (i * 13) % 46, 10,
                     accent if i == active else "#2C4E68"))
    return "".join(o)


# =====================================================================
# 01  Resource Dashboard -- the drill-down, one level at a time
# =====================================================================
def dashboard():
    o = [chrome("resource dashboard", BLUE), sidebar(2, "#5AA9D6")]
    x0 = 236
    o.append(text(x0, 104, "Resources", 26, INK, "'Fraunces',serif", 600))
    # Filter row.
    for i in range(3):
        o.append(rect(x0 + i * 250, 130, 226, 40, PAPER, 8, LINE, 1.5))
        o.append(bar(x0 + 16 + i * 250, 145, 90, 10, MUT))
    o.append(rect(W - 150, 130, 110, 40, BLUE, 8))
    o.append(bar(W - 122, 145, 54, 10, PAPER))
    # Three drill levels stacked in the same place, cross-fading in sequence:
    # environments, then regions, then the resources themselves. This is the one
    # thing the tool does that a still frame cannot show.
    LEVELS = [
        ("environments", [("prod", 6), ("staging", 2)]),
        ("regions", [("us-east-1", 4), ("us-west-2", 2)]),
        ("resources", [("ec2", 3), ("rds", 1), ("s3", 2)]),
    ]
    for li, (label, items) in enumerate(LEVELS):
        g = ['<g class="lv l%d">' % li]
        g.append(text(x0, 214, label, 13, MUT, "'JetBrains Mono',monospace", 500))
        # Breadcrumb: grows a step per level, which is the sense of depth.
        for k in range(li + 1):
            g.append(rect(x0 + k * 108, 228, 92, 22, BLUE, 11, op=.16))
        for i, (nm, n) in enumerate(items):
            cx = x0 + i * 216
            g.append(rect(cx, 274, 190, 150, PAPER, 12, LINE, 2))
            g.append('<path d="M %d 330 l 26 -15 l 26 15 l -26 15 Z" fill="%s"/>'
                     % (cx + 69, "#2E6B8E"))
            g.append('<path d="M %d 348 l 26 -15 l 26 15 l -26 15 Z" fill="%s" '
                     'opacity=".55"/>' % (cx + 69, "#2E6B8E"))
            g.append(text(cx + 95, 396, nm, 14, INK, "'Inter',sans-serif", 700,
                          anchor="middle"))
            g.append('<circle cx="%d" cy="292" r="15" fill="%s"/>' % (cx + 166, BLUE))
            g.append(text(cx + 166, 297, str(n), 13, PAPER,
                          "'Inter',sans-serif", 700, anchor="middle"))
        g.append('</g>')
        o.append("".join(g))
    # A footer bar with the count and the export the case study talks about.
    o.append('<line x1="%d" y1="600" x2="%d" y2="600" stroke="%s" stroke-width="1.5"/>'
             % (x0, W - 40, LINE))
    o.append(bar(x0, 626, 120, 11, MUT))
    o.append(rect(W - 190, 616, 150, 40, BLUE, 8))
    o.append(bar(W - 156, 631, 82, 10, PAPER))
    css = (".lv{opacity:0;animation:lv 12s infinite}"
           "@keyframes lv{0%,2%{opacity:0}6%,28%{opacity:1}32%,100%{opacity:0}}"
           ".l1{animation-delay:4s}.l2{animation-delay:8s}")
    return o, css


# =====================================================================
# 02  Events Timeline -- the track draws itself, then the rows arrive
# =====================================================================
def timeline():
    o = [chrome("resource timeline", GREEN)]
    x0, y0 = 60, 120
    o.append(text(x0, 104, "Resource Timeline", 24, INK, "'Fraunces',serif", 600))
    o.append(rect(W - 240, 82, 200, 32, OK, 16, op=.18))
    o.append(text(W - 222, 103, "compliant since Aug 21", 12, OK,
                  "'JetBrains Mono',monospace"))
    for i in range(3):
        o.append(rect(x0 + i * 300, 140, 274, 42, PAPER, 8, LINE, 1.5))
        o.append(bar(x0 + 16 + i * 300, 156, 96, 10, MUT))
    # The track. Segments are coloured by the state carried forward from the event
    # before them, which is the whole engineering point of the feature, so the
    # animation wipes it in left to right rather than fading it up.
    ty = 250
    SEGS = [(0.00, 0.30, OK), (0.30, 0.46, RED), (0.46, 0.62, OK),
            (0.62, 0.78, RED), (0.78, 1.00, OK)]
    tw = W - 120
    o.append('<g class="track">')
    o.append(rect(x0, ty - 3, tw, 6, LINE, 3))
    for a, b, col in SEGS:
        o.append(rect(x0 + tw * a, ty - 4, tw * (b - a), 8, col, 4))
    o.append('</g>')
    for i, (a, _, col) in enumerate(SEGS + [(1.0, 1.0, OK)]):
        cx = x0 + tw * a
        o.append('<g class="dot d%d"><circle cx="%.0f" cy="%d" r="11" fill="%s"/>'
                 '<circle cx="%.0f" cy="%d" r="11" fill="none" stroke="%s" '
                 'stroke-width="2.5"/></g>' % (i, cx, ty, col, cx, ty, PAPER))
        o.append(text(cx, ty + 42, ["Jul 24", "Aug 2", "Aug 7", "Aug 12", "Aug 16",
                                    "Now"][i], 12, MUT,
                      "'JetBrains Mono',monospace", 400, anchor="middle"))
    # The events table beneath, arriving row by row.
    o.append('<line x1="%d" y1="330" x2="%d" y2="330" stroke="%s" stroke-width="1.5"/>'
             % (x0, W - 60, LINE))
    for i, (col, wid) in enumerate(((OK, 210), (RED, 168), (OK, 232),
                                    (RED, 150), (OK, 196))):
        yy = 360 + i * 58
        o.append('<g class="row r%d">' % i)
        o.append(rect(x0, yy, W - 120, 46, WASH if i % 2 else PAPER, 8))
        o.append('<circle cx="%d" cy="%d" r="8" fill="%s"/>' % (x0 + 26, yy + 23, col))
        o.append(bar(x0 + 50, yy + 18, 120, 10, MUT))
        o.append(bar(x0 + 220, yy + 18, wid, 10, LINE))
        o.append(bar(W - 220, yy + 18, 120, 10, "#9FB4C4"))
        o.append('</g>')
    css = (".track{clip-path:inset(0 100% 0 0);animation:tk 9s ease-out infinite}"
           "@keyframes tk{0%,4%{clip-path:inset(0 100% 0 0)}"
           "34%,92%{clip-path:inset(0 0 0 0)}100%{clip-path:inset(0 100% 0 0)}}"
           ".dot{opacity:0;animation:dt 9s infinite}"
           "@keyframes dt{0%,6%{opacity:0}12%,92%{opacity:1}100%{opacity:0}}"
           + "".join(".d%d{animation-delay:%.2fs}" % (i, i * .45) for i in range(6)) +
           ".row{opacity:0;animation:rw 9s infinite}"
           "@keyframes rw{0%,40%{opacity:0}48%,92%{opacity:1}100%{opacity:0}}"
           + "".join(".r%d{animation-delay:%.2fs}" % (i, i * .12) for i in range(5)))
    return o, css


# =====================================================================
# 04  Persona Homepage -- the blocks reorder
# =====================================================================
def persona():
    """The page's own furniture, in its two shipped arrangements.

    Two arrangements rather than three, and the widgets are the ones that are on
    both defaults. The card is the first thing anyone sees of this project and the
    case study's first decision is that there are TWO personas; a thumbnail cycling
    through three would be arguing with the page it links to.

    Colours are the demo's, not this site's: navy #12395A for the grade card, the
    gold for governance, white for everything else on a light ground. A thumbnail
    in the portfolio's own palette would be prettier and would be a picture of a
    different product.
    """
    PG, CARD, EDGE = "#F2F5F7", "#FFFFFF", "#E2E9EE"
    PNAVY, PGOLD, PRAIL = "#12395A", "#F5C647", "#0C3A5E"
    SLATE, ICE = "#5D7183", "#E3E9EE"

    # x, y, w, h for the three column widths, laid out on a 3-column grid inside
    # the page area. Written once; both arrangements index into it.
    GX, GY, GW, GAP = 150, 220, 1010, 14
    COL = (GW - GAP * 2) / 3.0

    def cell(c, r, span, h, kind, label, grade=None):
        x = GX + c * (COL + GAP)
        y = GY + r
        w = COL * span + GAP * (span - 1)
        fill = PNAVY if kind == "navy" else PGOLD if kind == "gold" else CARD
        ink = "#FFFFFF" if kind == "navy" else "#20344A" if kind == "gold" else INK
        soft = "#7FA3BF" if kind == "navy" else "#B08C1F" if kind == "gold" else LINE
        o = [rect(x, y, w, h, fill, 12,
                  None if kind != "plain" else EDGE, 1.5)]
        o.append(rect(x + 16, y + 15, 20, 20, ink, 6, op=.16))
        o.append(text(x + 46, y + 30, label, 16, ink, "'Inter',sans-serif", 700))
        if grade:
            o.append(text(x + 16, y + h - 22, grade, 68, ink,
                          "'Inter',sans-serif", 800))
        elif h > 76:
            o.append(bar(x + 16, y + 58, min(w - 40, 260), 9, soft))
            o.append(bar(x + 16, y + 80, min(w - 40, 190), 9, soft))
            o.append(bar(x + 16, y + h - 26, min(w - 40, 120), 9, soft, r=4))
        return "".join(o)

    # (col, rowY, span, height, kind, label, grade)
    ARRANGE = [
        [(0, 0, 1, 156, "navy", "Maturity score", "A-"),
         (1, 0, 1, 156, "plain", "Score trend", None),
         (2, 0, 1, 156, "gold", "Governance", None),
         (0, 170, 3, 118, "plain", "Recent notices", None),
         (0, 302, 2, 118, "plain", "Cloud cost", None),
         (2, 302, 1, 118, "plain", "Service health", None)],
        [(0, 0, 1, 156, "gold", "Governance", None),
         (1, 0, 1, 156, "navy", "Maturity score", "B+"),
         (2, 0, 1, 156, "plain", "Divisional rollup", None),
         (0, 170, 2, 118, "plain", "Applications", None),
         (2, 170, 1, 118, "plain", "Change status", None),
         (0, 302, 3, 118, "plain", "Cloud cost", None)],
    ]

    o = [chrome("homepage", VIOLET)]
    o.append(rect(0, 52, W, H - 52, PG))

    # The rail. Narrow, navy, and the only thing on the page that is not a card:
    # it is what tells you at a glance that this is one page inside a product
    # rather than a dashboard someone published on its own.
    o.append(rect(0, 52, 88, H - 52, PRAIL))
    o.append('<circle cx="44" cy="92" r="13" fill="%s"/>' % PGOLD)
    for i in range(6):
        yy = 140 + i * 46
        if i == 1:
            o.append(rect(16, yy - 8, 56, 36, "#FFFFFF", 9, op=.14))
        o.append(rect(35, yy, 18, 18, "#C6D6E1", 4, op=1 if i == 1 else .55))

    o.append(text(150, 130, "Welcome back!", 34, "#1B2B3A",
                  "'Inter',sans-serif", 800))

    # The scope bar, and the chip that moves. The page does not ask who you are,
    # it asks what you are responsible for, so the control that travels is a
    # scope and not a job title.
    o.append(rect(150, 158, 1010, 42, "#EDF1F4", 12))
    o.append(text(166, 185, "PAGE SCOPE", 13, "#7C8B99",
                  "'JetBrains Mono',monospace", 700))
    o.append('<rect class="pill" x="286" y="164" width="188" height="30" rx="15" '
             'fill="#DCE7EF" stroke="%s" stroke-width="2"/>' % PNAVY)
    for i, nm in enumerate(("Account", "Division")):
        o.append(text(380 + i * 200, 185, nm, 15, "#33475B",
                      "'Inter',sans-serif", 700, anchor="middle"))
    o.append(rect(1006, 166, 88, 26, ICE, 13))
    o.append(rect(1102, 166, 44, 26, SLATE, 13))

    # Both arrangements are drawn, stacked, and cross-faded. Animating the real
    # movement would need one element per card carrying two keyframed positions;
    # at 480px wide the read is the same and this is half the markup.
    for ai, cells in enumerate(ARRANGE):
        g = ['<g class="ord o%d">' % ai]
        for c in cells:
            g.append(cell(*c))
        g.append('</g>')
        o.append("".join(g))

    css = (".ord{opacity:0;animation:od 11s infinite}"
           "@keyframes od{0%,1%{opacity:0}5%,46%{opacity:1}50%,100%{opacity:0}}"
           ".o1{animation-delay:5.5s}"
           ".pill{animation:pl 11s infinite}"
           "@keyframes pl{0%,44%{transform:translateX(0)}"
           "50%,94%{transform:translateX(200px)}100%{transform:translateX(0)}}")
    return o, css


print("work thumbnails:")
for name, fn in (("shot-dashboard", dashboard), ("shot-timeline", timeline),
                 ("shot-persona", persona)):
    body, css = fn()
    save(name, "".join(body), css)
