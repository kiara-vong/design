# -*- coding: utf-8 -*-
"""Home-page thumbnails. Drawing primitives live in uikit.py."""
from gen.uikit import *
import io, math, random

# ---------------------------------------------------------------- Card 1
# Design System Overhaul. A long documentation page scrolled inside the window,
# so the card shows the system's *extent* -- tokens, then components, then usage
# docs -- which is the actual claim being made. A single static screen of one
# component grid would show a component grid, not a system.
STRIP_H = 1900
def ds_strip():
    o = [rect(0, 0, W - 196, STRIP_H, PAPER)]
    x0, cw = 40, W - 196 - 80
    o.append(text(x0, 52, "Foundations", 22, INK, "'Laurel',serif", 600))
    o.append(bar(x0, 68, 300, 8, LINE))
    # Colour ramps: the palette of this very site, so the artwork and the page agree.
    for r, base in enumerate(("#649F25", "#649F25", "#1F597B", "#8460C6")):
        for c in range(9):
            o.append(rect(x0 + c * 58, 100 + r * 52, 50, 40, base, 6,
                          op=round(.14 + c * .107, 2)))
        o.append(text(x0 + 9 * 58 + 12, 126 + r * 52, ["persimmon", "leaf", "ink", "iris"][r], 12, MUT))
    y = 330
    o.append(text(x0, y, "Type scale", 22, INK, "'Laurel',serif", 600))
    for i, s in enumerate((34, 27, 22, 17, 14, 11)):
        o.append(bar(x0, y + 26 + i * 34, 120 + s * 9, s * .78, INK if i < 2 else MUT))
        o.append(text(x0 + 640, y + 34 + i * 34, "%d / %d" % (s * 2, int(s * 2 * 1.4)), 12, MUT))
    y = 590
    o.append(text(x0, y, "Components", 22, INK, "'Laurel',serif", 600))
    # 4x3 component tiles, each a different primitive so the grid does not read as wallpaper
    for i in range(12):
        cx, cy = x0 + (i % 4) * (cw / 4.0), y + 26 + (i // 4) * 148
        tw = cw / 4.0 - 18
        o.append(rect(cx, cy, tw, 128, PAPER, 10, LINE, 1.5))
        k = i % 6
        if k == 0:
            o.append(rect(cx + 20, cy + 46, 92, 34, ACCENT, 17))
            o.append(bar(cx + 42, cy + 58, 48, 10, PAPER))
        elif k == 1:
            o.append(rect(cx + 20, cy + 40, tw - 40, 30, WASH, 8, LINE, 1.5))
            o.append(bar(cx + 30, cy + 51, 60, 8, MUT))
            o.append(bar(cx + 20, cy + 82, 74, 8, LINE))
        elif k == 2:
            o.append(rect(cx + 20, cy + 44, 44, 24, GREEN, 12, op=.28))
            o.append('<circle cx="%.1f" cy="%.1f" r="9" fill="%s"/>' % (cx + 52, cy + 56, GREEN))
            o.append(bar(cx + 76, cy + 52, 52, 8, LINE))
        elif k == 3:
            for j in range(3):
                o.append('<circle cx="%.1f" cy="%.1f" r="7" fill="none" stroke="%s" stroke-width="2"/>'
                         % (cx + 28, cy + 40 + j * 26, MUT))
                o.append(bar(cx + 44, cy + 36 + j * 26, 58 - j * 9, 8, LINE))
            o.append('<circle cx="%.1f" cy="%.1f" r="7" fill="%s"/>' % (cx + 28, cy + 40, ACCENT))
        elif k == 4:
            o.append(rect(cx + 20, cy + 34, tw - 40, 1.5, LINE))
            for j in range(3):
                o.append(bar(cx + 20 + j * 46, cy + 48, 34, 8, ACCENT if j == 0 else LINE))
            o.append(rect(cx + 20, cy + 68, tw - 40, 26, WASH, 6))
        else:
            o.append('<circle cx="%.1f" cy="%.1f" r="26" fill="none" stroke="%s" stroke-width="9"/>'
                     % (cx + tw / 2, cy + 64, LINE))
            o.append('<path d="M %.1f %.1f A 26 26 0 0 1 %.1f %.1f" fill="none" stroke="%s" '
                     'stroke-width="9" stroke-linecap="round"/>'
                     % (cx + tw / 2, cy + 38, cx + tw / 2 + 24, cy + 74, ACCENT))
    y = 1200
    o.append(text(x0, y, "Usage", 22, INK, "'Laurel',serif", 600))
    for i in range(2):
        bx = x0 + i * (cw / 2.0)
        o.append(rect(bx, y + 26, cw / 2.0 - 20, 190, PAPER, 10,
                      GREEN if i == 0 else "#E6685C", 2))
        o.append(rect(bx, y + 26, cw / 2.0 - 20, 30, GREEN if i == 0 else "#E6685C", 10, op=.15))
        o.append(text(bx + 14, y + 47, "DO" if i == 0 else "DON'T", 12,
                      GREEN if i == 0 else "#E6685C", w=700))
        o.append(rect(bx + 24, y + 78, 92, 32, ACCENT if i == 0 else MUT, 16, op=1 if i == 0 else .45))
        o.append(lines(bx + 24, y + 130, [cw / 2.0 - 80, cw / 2.0 - 130, cw / 2.0 - 190]))
    o.append(text(x0, 1470, "Migration", 22, INK, "'Laurel',serif", 600))
    for i in range(6):     # the 12,600-line diff, as a review checklist
        yy = 1500 + i * 40
        o.append(rect(x0, yy, cw, 32, WASH if i % 2 else PAPER, 6))
        o.append('<path d="M %.1f %.1f l 5 6 l 10 -13" stroke="%s" stroke-width="3" '
                 'fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
                 % (x0 + 14, yy + 16, GREEN))
        o.append(bar(x0 + 42, yy + 12, 190 + (i * 61) % 260, 9, LINE))
        o.append(bar(x0 + cw - 96, yy + 12, 76, 9, GREEN, r=4.5))
    return "".join(o)

save("shot-ds-strip", ds_strip(), W - 196, STRIP_H)
save("shot-ds-base", chrome("design-system.internal / foundations",
                            sidebar(active=1) + rect(196, 52, W - 196, H - 52, PAPER)))
print("card 1 written")

print("cards written")


# ---------------------------------------------------------------- Fields
# The ground each thumbnail's window sits on. The original used exported
# photographs here, and its stylesheet argues at length that generated textures
# read as foreign next to them. That argument does not transfer: this build has
# no photographs anywhere, so a flat wash with a soft vignette is the consistent
# choice rather than the cheap one. Each is a --tone from :root at low chroma.
def field(name, top, bot, dot):
    body = ('<defs><linearGradient id="g" x1="0" y1="0" x2=".3" y2="1">'
            '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/>'
            '</linearGradient>'
            '<radialGradient id="v" cx=".5" cy=".42" r=".78">'
            '<stop offset=".55" stop-color="#000" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#000" stop-opacity=".13"/></radialGradient></defs>'
            '<rect width="529" height="304" fill="url(#g)"/>' % (top, bot))
    for i in range(9):     # a slack dot grid: enough to catch the light, not a pattern
        for j in range(5):
            body += ('<circle cx="%.0f" cy="%.0f" r="1.8" fill="%s" opacity=".22"/>'
                     % (34 + i * 58, 30 + j * 62, dot))
    body += '<rect width="529" height="304" fill="url(#v)"/>'
    save(name, body, 529, 304)

# The four generated fields are gone. They were flat tinted panels drawn to sit
# quietly behind a screenshot, and they were the last procedural texture on a site
# whose interest comes from photographs, drawings and type. gen/card_fields.py cuts
# paintings for those four slots now, from the same folder the hero, the About
# ground, the footer band and the project thumbnails come from.

