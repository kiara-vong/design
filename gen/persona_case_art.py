# -*- coding: utf-8 -*-
"""The four drawn figures for the Persona Homepage case study.

The artifacts this project actually produced -- a flow diagram, five wireframes, a
widget catalog and a set of mockups -- exist as real documents. They are not what
is on the page, and the reason is not taste: every one of them is a screenshot of
an internal tool, dense with the team's name, its division names and an application
identifier repeated in small type throughout, and a portfolio is a public document.
Repainting all of that is a per-image job with a per-image chance of missing one.

So they are redrawn, with the SUBSTANCE kept and the identifiers left out: the same
flow, the same five personas, the same twenty-four widgets under the same six
headings, the same onboarding modal. A drawing is also the honest register for a
case study whose subject is a decision rather than a screen -- nobody mistakes it
for evidence of a thing that shipped, and the four real captures further down the
page carry that job on their own.

Authored at 799x391, which is .cs-media, and delivered through media.flat(): these
are diagrams and a diagram does not get a title bar. A window around a drawing
sends the reader looking for the application it came from.
"""
import io

from gen.uikit import (rect, bar, text, save, INK, MUT, LINE, PAPER, WASH,
                       ACCENT, BLUE, VIOLET)

FW, FH = 799, 391

AMBER = "#E8B84B"
RUST = "#B4552F"
SANS = "'Clover',sans-serif"
MONO = "'Thistle',monospace"


def label(x, y, s, size=11, fill=INK, w=700, anchor="start", fam=SANS):
    return text(x, y, s, size, fill, fam, w, anchor=anchor)


def box(x, y, w, h, title, sub=None, fill=PAPER, stroke=LINE, accent=None):
    """A node: a rounded card with a title and an optional second line."""
    o = [rect(x, y, w, h, fill, 8, stroke, 1.5)]
    if accent:
        o.append(rect(x, y, 3.5, h, accent, 2))
    o.append(label(x + 12, y + (20 if sub else h / 2 + 4), title, 11.5, INK, 700))
    if sub:
        o.append(label(x + 12, y + 36, sub, 10, MUT, 400))
    return "".join(o)


def arrow(x0, y0, x1, y1, dashed=False, col=MUT):
    """An orthogonal connector with a head, drawn as one path."""
    if abs(y1 - y0) < 1:
        d = "M%.1f %.1f L%.1f %.1f" % (x0, y0, x1 - 7, y1)
    elif abs(x1 - x0) < 1:
        d = "M%.1f %.1f L%.1f %.1f" % (x0, y0, x1, y1 - 7)
    else:
        mid = (y0 + y1) / 2.0
        d = ("M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f"
             % (x0, y0, x0, mid, x1, mid, x1, y1 - 7))
    head = ('<path d="M%.1f %.1f l-4 -6 l8 0 z" fill="%s"/>'
            % (x1, y1, col)) if abs(y1 - y0) > 1 else \
           ('<path d="M%.1f %.1f l-6 -4 l0 8 z" fill="%s"/>' % (x1, y1, col))
    return ('<path d="%s" stroke="%s" stroke-width="1.6" fill="none"%s/>%s'
            % (d, col, ' stroke-dasharray="5 5"' if dashed else "", head))


def diamond(cx, cy, w, h, s):
    return ('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z" fill="%s" '
            'stroke="%s" stroke-width="1.5"/>%s'
            % (cx, cy - h / 2, cx + w / 2, cy, cx, cy + h / 2, cx - w / 2, cy,
               WASH, LINE, label(cx, cy + 4, s, 10.5, INK, 700, "middle")))


# =====================================================================
# 1. the flow: what happens between opening the page and using it
# =====================================================================
def flow():
    o = [rect(0, 0, FW, FH, PAPER)]
    y1, y2, bh = 62, 236, 52
    o.append(box(26, y1, 122, bh, "Opens home", "first visit", accent=BLUE))
    o.append(diamond(232, y1 + bh / 2, 130, 74, "saved layout?"))
    o.append(box(324, y1, 136, bh, "Detect scope", "role, groups, division",
                 accent=ACCENT))
    o.append(box(478, y1, 136, bh, "Confirm it", "the user edits first",
                 accent=ACCENT))
    o.append(box(632, y1, 141, bh, "Five-step tour", "once, then never",
                 accent=ACCENT))

    o.append(box(26, y2, 168, bh, "Render", "skeletons, then widgets",
                 accent=VIOLET))
    o.append(box(224, y2, 168, bh, "Customise", "drag, resize, stack",
                 accent=VIOLET))
    o.append(box(422, y2, 178, bh, "Save a named preset", "server-side, by user",
                 accent=VIOLET))
    o.append(box(630, y2, 143, bh, "Use it", "every day after", accent=BLUE))

    o.append(arrow(148, y1 + bh / 2, 167, y1 + bh / 2))
    o.append(arrow(297, y1 + bh / 2, 324, y1 + bh / 2))
    o.append(arrow(460, y1 + bh / 2, 478, y1 + bh / 2))
    o.append(arrow(614, y1 + bh / 2, 632, y1 + bh / 2))
    o.append(label(305, y1 + bh / 2 - 6, "no", 9.5, MUT, 700, "middle", MONO))
    o.append(label(246, y1 + bh + 34, "yes", 9.5, MUT, 700, "start", MONO))
    # Two ways into Render, drawn at two heights on purpose: the saved-layout
    # shortcut skips the entire onboarding row, and a returning user taking it is
    # the common case rather than the exception. Routed through the same y they
    # would overlap for most of the width and read as one line.
    o.append('<path d="M232 %d L232 %d L110 %d L110 %d" stroke="%s" '
             'stroke-width="1.6" fill="none"/>'
             '<path d="M110 %d l-4 -6 l8 0 z" fill="%s"/>'
             % (y1 + bh / 2 + 37, y2 - 34, y2 - 34, y2, MUT, y2, MUT))
    o.append('<path d="M702 %d L702 %d L134 %d L134 %d" stroke="%s" '
             'stroke-width="1.6" fill="none"/>'
             '<path d="M134 %d l-4 -6 l8 0 z" fill="%s"/>'
             % (y1 + bh, y2 - 66, y2 - 66, y2, MUT, y2, MUT))
    o.append(arrow(194, y2 + bh / 2, 224, y2 + bh / 2))
    o.append(arrow(392, y2 + bh / 2, 422, y2 + bh / 2))
    o.append(arrow(600, y2 + bh / 2, 630, y2 + bh / 2))
    # customising again is the loop, and it is a loop rather than a step
    o.append('<path d="M508 %d L508 %d L308 %d L308 %d" stroke="%s" '
             'stroke-width="1.6" fill="none" stroke-dasharray="5 5"/>'
             '<path d="M308 %d l-4 6 l8 0 z" fill="%s"/>'
             % (y2 + bh, y2 + bh + 34, y2 + bh + 34, y2 + bh + 6, MUT,
                y2 + bh + 6, MUT))
    o.append(label(408, y2 + bh + 48, "every later change writes the same "
                   "preferences row", 10, MUT, 400, "middle"))
    return "".join(o)


# =====================================================================
# 2. five personas, and the two that shipped
# =====================================================================
FIVE = [("Developer", 4, ACCENT), ("Manager", 5, ACCENT),
        ("Director", 6, BLUE), ("Division lead", 6, BLUE),
        ("Executive", 4, BLUE)]


def mini(x, y, w, h, name, blocks, col, scale=1.0):
    """A wireframe at thumbnail size: a header bar and a few content blocks."""
    o = [rect(x, y, w, h, PAPER, 7, LINE, 1.5),
         rect(x, y, w, 13, WASH, 7), rect(x, y + 7, w, 6, WASH)]
    o.append(rect(x + 6, y + 4.5, 22, 4, col, 2, op=.55))
    yy = y + 20
    per = (h - 26) / float(max(blocks, 1))
    for i in range(blocks):
        bh = per - 4
        wide = w - 12 if i % 3 == 0 else (w - 12) * (0.62 if i % 3 == 1 else 0.34)
        o.append(rect(x + 6, yy, wide, bh, col, 3, op=.16))
        if i % 3 != 0:
            o.append(rect(x + 6 + wide + 4, yy, (w - 12) - wide - 4, bh,
                          col, 3, op=.09))
        yy += per
    o.append(label(x + w / 2, y + h + 15, name, 10.5, INK, 700, "middle"))
    return "".join(o)


def five_to_two():
    o = ["<style>.p2-src,.p2-dst{transition:opacity .18s ease}.p2-hit{cursor:pointer}.p2-link{transition:opacity .18s ease,stroke-width .18s ease;animation:p2pulse 9s ease-in-out infinite}.p2-link[data-i=\"1\"]{animation-delay:.5s}.p2-link[data-i=\"2\"]{animation-delay:1s}.p2-link[data-i=\"3\"]{animation-delay:1.5s}.p2-link[data-i=\"4\"]{animation-delay:2s}@keyframes p2pulse{0%,7%{opacity:.55;stroke-width:1.6}2.5%{opacity:1;stroke-width:2.6}12%,100%{opacity:.55;stroke-width:1.6}}svg:has(.p2-src:hover) .p2-link{animation:none;opacity:.12}svg:has(.p2-src:hover) .p2-src:not(:hover){opacity:.32}svg:has(.p2-src:hover) .p2-dst{opacity:.32}svg:has(.p2-src[data-i=\"0\"]:hover) .p2-link[data-i=\"0\"],svg:has(.p2-src[data-i=\"1\"]:hover) .p2-link[data-i=\"1\"],svg:has(.p2-src[data-i=\"2\"]:hover) .p2-link[data-i=\"2\"],svg:has(.p2-src[data-i=\"3\"]:hover) .p2-link[data-i=\"3\"],svg:has(.p2-src[data-i=\"4\"]:hover) .p2-link[data-i=\"4\"]{opacity:1;stroke-width:2.8}svg:has(.p2-src[data-i=\"0\"]:hover) .p2-dst[data-d=\"c\"],svg:has(.p2-src[data-i=\"1\"]:hover) .p2-dst[data-d=\"c\"],svg:has(.p2-src[data-i=\"2\"]:hover) .p2-dst[data-d=\"l\"],svg:has(.p2-src[data-i=\"3\"]:hover) .p2-dst[data-d=\"l\"],svg:has(.p2-src[data-i=\"4\"]:hover) .p2-dst[data-d=\"l\"]{opacity:1}@media (prefers-reduced-motion:reduce){.p2-link,.p2-src,.p2-dst{transition:none;animation:none}}</style>"]
    o.append(rect(0, 0, FW, FH, PAPER))
    o.append(label(26, 26, "PROPOSED", 9.5, MUT, 700, "start", MONO))
    tw, gap = 130, 22
    tx = [26 + i * (tw + gap) for i in range(5)]
    for i, (x, (name, n, col)) in enumerate(zip(tx, FIVE)):
        o.append('<g class="p2-src" data-i="%d">' % i)
        o.append('<rect class="p2-hit" x="%.1f" y="%.1f" width="%.1f" '
                 'height="%.1f" fill="#000" fill-opacity="0" '
                 'pointer-events="all"/>' % (x - 2, 38, tw + 4, 134))
        o.append(mini(x, 40, tw, 116, name, n, col))
        o.append('</g>')

    o.append(label(26, 212, "SHIPPED", 9.5, MUT, 700, "start", MONO))
    bw = 322
    bx = [26, 26 + bw + 27]
    o.append('<g class="p2-dst" data-d="c">%s</g>'
             % mini(bx[0], 226, bw, 116, "Contributor \u00b7 one application",
                    5, ACCENT))
    o.append('<g class="p2-dst" data-d="l">%s</g>'
             % mini(bx[1], 226, bw, 116, "Leader \u00b7 many, or a division",
                    6, BLUE))

    for i, (name, n, col) in enumerate(FIVE):
        x0 = tx[i] + tw / 2.0
        j = 0 if i < 2 else 1
        x1 = bx[j] + bw / 2.0
        y0, y1 = 172, 226
        o.append('<path class="p2-link" data-i="%d" d="M%.1f %.1f '
                 'C%.1f %.1f %.1f %.1f %.1f %.1f" stroke="%s" stroke-width="1.6" '
                 'fill="none" opacity=".55"/>'
                 % (i, x0, y0, x0, y0 + 28, x1, y1 - 28, x1, y1, col))
    return "".join(o)


# =====================================================================
# 3. the catalog, in the categories the picker groups it by
# =====================================================================
CATALOG = [
    ("Maturity & compliance", ACCENT,
     ["Maturity score", "Score (numeric)", "7-day delta", "Score trend",
      "Job breakdown", "Upcoming requirements", "Jobs open", "Job burndown",
      "Jobs"]),
    ("Governance automation", RUST,
     ["Governance automation", "Pipeline events", "Change status",
      "Automated campaigns", "Remediations"]),
    ("Cost", AMBER, ["Cloud cost", "Cost by service"]),
    ("Alerts & health", VIOLET, ["Recent notices", "Service health"]),
    ("Portfolio", BLUE,
     ["Application details", "Applications", "Accounts", "Divisional rollup",
      "Top resources by jobs"]),
    ("Layout", MUT, ["Section title", "Smart stack"]),
]

COLUMNS = [[0], [1, 2], [3, 4, 5]]


def catalog():
    o = ["<style>.cat-grp{transition:opacity .16s ease}.cat-hit{cursor:pointer}.cat-row{transition:opacity .16s ease}svg:has(.cat-grp:hover) .cat-grp:not(:hover){opacity:.28}svg:has(.cat-grp:hover) .cat-grp:hover .cat-row{opacity:1}@media (prefers-reduced-motion:reduce){.cat-grp,.cat-row{transition:none}}</style>"]
    o.append(rect(0, 0, FW, FH, PAPER))
    cw, gap = 237, 22
    for ci, group in enumerate(COLUMNS):
        x = 26 + ci * (cw + gap)
        y = 40
        for gi in group:
            name, col, items = CATALOG[gi]
            g = ['<g class="cat-grp" data-c="%d">' % gi]
            y0 = y - 16
            hh = 12 + len(items) * 23 + 8
            g.append('<rect class="cat-hit" x="%.1f" y="%.1f" width="%.1f" '
                     'height="%.1f" fill="#000" fill-opacity="0" '
                     'pointer-events="all"/>' % (x - 4, y0, cw + 8, hh))
            g.append(rect(x, y - 11, 3.5, 12, col, 2))
            g.append(label(x + 10, y, name.upper(), 9.5, MUT, 700, "start", MONO))
            y += 12
            for it in items:
                g.append('<g class="cat-row">')
                g.append(rect(x, y, cw, 19, col, 4, op=.11))
                g.append(rect(x, y, 2.5, 19, col, 1.5))
                g.append(label(x + 9, y + 13.5, it, 10.5, INK, 500))
                g.append('</g>')
                y += 23
            g.append('</g>')
            o.append("".join(g))
            y += 16
    o.append(label(26, 24, "TWENTY-FOUR WIDGETS, SIX HEADINGS", 9.5, INK,
                   700, "start", MONO))
    o.append(label(FW - 26, 24, "every one of them already existed somewhere",
                   10, MUT, 400, "end"))
    return "".join(o)


# =====================================================================
# 4. the onboarding modal: what the page detected, before it saves anything
# =====================================================================
def onboard():
    o = [rect(0, 0, FW, FH, WASH)]
    mx, my, mw, mh = 96, 30, 607, 331
    o.append(rect(mx, my, mw, mh, PAPER, 12, LINE, 1.5))
    o.append(label(mx + 26, my + 42, "Confirm what we found", 17, INK, 700))
    o.append(label(mx + 26, my + 64,
                   "You can change any of this later from the toolbar.",
                   11, MUT, 400))

    # the auto-detected banner, which is the honest part of the pattern
    o.append(rect(mx + 26, my + 78, mw - 52, 30, ACCENT, 6, op=.12))
    o.append(rect(mx + 34, my + 85, 84, 16, ACCENT, 8, op=.65))
    o.append(label(mx + 76, my + 96, "AUTO-DETECTED", 8, PAPER, 700,
                   "middle", MONO))
    o.append(label(mx + 128, my + 97,
                   "from your role, your groups and your division mapping",
                   10.5, INK, 400))

    rows = [("APPLICATIONS (2)", "detected from your groups",
             [92, 118], ACCENT),
            ("ACCOUNTS (3)", "detected from application membership",
             [80, 80, 80], BLUE),
            ("DIVISIONS (1)", "detected from your primary application",
             [64], VIOLET)]
    yy = my + 126
    for title, sub, chips, col in rows:
        o.append(label(mx + 26, yy, title, 9, MUT, 700, "start", MONO))
        o.append(label(mx + 26 + len(title) * 5.6 + 10, yy, sub, 9.5, MUT, 400))
        yy += 10
        cx = mx + 26
        for w in chips:
            o.append(rect(cx, yy, w, 24, col, 12, op=.13))
            o.append(bar(cx + 12, yy + 10, w - 34, 5, LINE))
            o.append(label(cx + w - 13, yy + 16, "×", 11, MUT, 700, "middle"))
            cx += w + 8
        o.append(rect(cx, yy, 74, 24, PAPER, 12, LINE, 1.2))
        o.append(label(cx + 37, yy + 16, "+ add", 10, MUT, 700, "middle"))
        yy += 44

    o.append(label(mx + 26, my + mh - 36,
                   "Adding a division switches you to the wider layout.",
                   10.5, MUT, 400))
    o.append(rect(mx + mw - 172, my + mh - 54, 146, 32, ACCENT, 16))
    o.append(label(mx + mw - 99, my + mh - 33, "Confirm and continue", 11,
                   PAPER, 700, "middle"))
    return "".join(o)


for name, fn in (("cs-persona-flow", flow),
                 ("cs-persona-five-to-two", five_to_two),
                 ("cs-persona-catalog", catalog),
                 ("cs-persona-onboard", onboard)):
    save(name, fn(), FW, FH)
print("persona case artwork written")
