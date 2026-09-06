import io
# -*- coding: utf-8 -*-
"""Filled media blocks: a real capture paired with one of camera.css's machines.

Separate from case_blocks.py on purpose. That module holds the blocks a page is
assembled from while its media is still a brief; this one holds what replaces them
once the capture exists. Keeping them apart means the plate briefs stay readable as
a to-do list rather than getting mixed in with what has already been shot.

Every block renders into the same 799x391 box that plate() describes, so a brief
becoming a figure changes nothing about the page around it, and every one takes a
caption. A figure without a caption is an assertion; the caption is where a picture
is told what it is being used to prove.

`root` exists because these are used from work/ and projects/ pages, which reach
assets through "../", and from the home page, which does not.
"""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _fig(inner, caption):
    return ('      <figure class="cs-figure">\n'
            '%s'
            '        <figcaption class="cs-caption">%s</figcaption>\n'
            '      </figure>\n' % (inner, esc(caption)))


def clip(name, alt, caption, root="../../"):
    """A walkthrough video. Plays itself, silently, forever.

    The poster is the clip's own opening frame, which is also the frame it dissolves
    back to at the loop, so a clip that has not started and a clip mid-cycle are the
    same picture rather than two different ones.

    preload="metadata" rather than "auto": a case-study page can carry three of
    these, and a visitor who scrolls past them should not have paid for them.

    Muted is not a preference. It is the only state a browser will autoplay, and
    these are assembled from state captures with no audio to lose.
    """
    return _fig(
        '        <div class="cs-media cam cam-clip">\n'
        '          <video src="%sassets/video/%s.mp4" '
        'poster="%sassets/video/%s-poster.jpg" '
        'autoplay muted loop playsinline preload="metadata" '
        'aria-label="%s"></video>\n'
        '        </div>\n' % (root, name, root, name, esc(alt)), caption)


def push(src, alt, caption, z=1.4, fx="50%", fy="50%", dur="13s", root="../../"):
    """A still, framed whole and then pushed in on one part of itself.

    fx/fy name the point worth looking at, as percentages of the image, so the push
    frames the callout rather than the middle.
    """
    return _fig(
        '        <div class="cs-media cam cam-push" '
        'style="--z:%s;--fx:%s;--fy:%s;--dur:%s">\n'
        '          <img src="%sassets/%s" alt="%s" loading="lazy">\n'
        '        </div>\n' % (z, fx, fy, dur, root, src, esc(alt)), caption)


def strip(src, alt, caption, travel, dur="17s", root="../../"):
    """A tall still scrolling behind a fixed frame.

    travel is a PERCENTAGE OF THE IMAGE'S OWN HEIGHT, never a pixel count. See the
    note in camera.css for why that distinction has its own paragraph.
    """
    return _fig(
        '        <div class="cs-media cam cam-strip" style="--travel:%s;--dur:%s">\n'
        '          <img src="%sassets/%s" alt="%s" loading="lazy">\n'
        '        </div>\n' % (travel, dur, root, src, esc(alt)), caption)


def wipe(before_src, after_src, alt, caption,
         before="Explored", after="Shipped", dur="11s", root="../../"):
    """Two stills under a travelling seam, labelled inside the frame.

    The labels sit in the picture rather than in the caption because the whole
    figure is a comparison, and a reader who has to look away to find out which half
    is which is doing the work the figure was meant to do for them.
    """
    return _fig(
        '        <div class="cs-media cam cam-wipe" style="--dur:%s">\n'
        '          <img src="%sassets/%s" alt="%s" loading="lazy">\n'
        '          <img src="%sassets/%s" alt="" aria-hidden="true" loading="lazy">\n'
        '          <span class="seam"></span>\n'
        '          <span class="tag b">%s</span><span class="tag a">%s</span>\n'
        '        </div>\n' % (dur, root, before_src, esc(alt), root, after_src,
                              esc(before), esc(after)), caption)


def deal(srcs, alt, caption, dur="14s", root="../../"):
    """N stills at identical framing, cross-fading. The first is the resting state.

    Which means the first entry should be the frame worth leaving on screen, since
    it is what reduced motion and a paused page both get.
    """
    o = ['        <div class="cs-media cam cam-deal" style="--dur:%s;--n:%d">\n'
         % (dur, len(srcs))]
    for i, src in enumerate(srcs):
        o.append('          <img style="--i:%d" src="%sassets/%s" alt="%s"%s '
                 'loading="lazy">\n'
                 % (i, root, src, esc(alt) if i == 0 else "",
                    "" if i == 0 else ' aria-hidden="true"'))
    o.append('        </div>\n')
    return _fig("".join(o), caption)


def flat(src, alt, caption, root="../../"):
    """A drawn figure, held still.

    The SVG animates itself from its own <style>, so there is no camera machine
    over the top of it: a machine here would be a second thing moving, out of
    phase with the first. The slot just holds it at its authored size.
    """
    return _fig(
        '        <div class="cs-media">\n'
        '          <img class="cs-flat" src="%sassets/%s" alt="%s" loading="lazy">\n'
        '        </div>\n' % (root, src, esc(alt)), caption)


def annotated(src, alt, caption, notes, root="../../"):
    """A still with leader-line labels that push the picture in on what they name.

    notes is a list of (key, label, description, x, y, zoom, top), where x/y are the
    point to frame as percentages of the image, zoom is how far in to go, and top is
    where the label sits down the right-hand margin.

    The capture brief for these asks for about 120px left clear on the right for
    exactly this, so the labels sit over ground rather than over the interface.
    """
    o = ['        <div class="cs-media cam ann">\n']
    for key, label, desc, x, y, z, top in notes:
        o.append('          <div class="ann-group" data-k="%s" '
                 'style="--t:%s;--x:%s;--y:%s;--z:%s">\n'
                 '            <div class="ann-row"><span class="ann-line"></span>'
                 '<span class="ann-note">%s</span></div>\n'
                 '            <p class="ann-desc">%s</p>\n'
                 '          </div>\n'
                 % (key, top, x, y, z, esc(label), esc(desc)))
    o.append('          <div class="ann-view">'
             '<img src="%sassets/%s" alt="%s" loading="lazy"></div>\n'
             '        </div>\n' % (root, src, esc(alt)))
    return _fig("".join(o), caption)


# ---------------------------------------------------------------------------
# The stage: a capture as an object on a surface, with a camera over it.
#
# The slot's real size, from case-study.css. This machine works in pixels rather
# than percentages, so the numbers are stated rather than implied -- the whole
# point of it is that its numbers live in the same space as the thing they
# describe.
SLOT_W, SLOT_H = 799.0, 391.0

# Air around the plate at its resting framing. Enough that the capture reads as an
# object on a surface rather than as something that failed to fill the box.
REST_PAD = 46.0

# Air around a detail framing. Tighter: by then the reader has seen the whole
# thing and the point is to be close to one part of it.
LOOK_PAD = 20.0

# Room held back for a label beside the region it names.
CALL_W, CALL_GAP = 166.0, 22.0

# The detail camera never goes past 1:1. The plates are authored at 1440x810 and
# the assets are 2x that, so scale 1 is where a capture is pixel-exact on a
# retina screen. Past it there is nothing left to reveal and the softness starts.
MAX_K = 1.0


def _plate_size(src, given=None):
    """The delivered size of a plate, from the index gen/plates.py writes.

    The look rectangles are read off the delivered file, so they have to be in the
    delivered file's coordinates -- and that is NOT the size of the capture that
    went in, because plates.py resizes to a fixed delivery width. Passing the
    source size instead puts every rect out by that ratio, which is silent, and
    looks exactly like a badly chosen framing.
    """
    if given:
        return given
    try:
        import json
        idx = json.load(io.open("plate-index.json", encoding="utf-8"))
    except Exception:
        return (1440, 810)
    name = src.split("/")[-1].rsplit(".", 1)[0]
    e = idx.get(name)
    return (e["w"], e["h"]) if e else (1440, 810)


def _fit(pw, ph, pad, vw=SLOT_W):
    """Largest scale fitting pw x ph in the view with pad around it, and the
    translate that centres it there. Returns (x, y, k) in view pixels.

    Against the VIEW rather than the card, because a figure carrying a label has a
    narrower view -- and a resting framing measured against the card would have
    its right-hand edge clipped off by the very window that makes room for the
    label."""
    k = min((vw - pad * 2) / float(pw), (SLOT_H - pad * 2) / float(ph))
    return ((vw - pw * k) / 2.0, (SLOT_H - ph * k) / 2.0, k)


def _clamp(x, y, pw, ph, k, vx=0.0, vw=SLOT_W):
    """Keep the plate covering the viewport, so the surface never shows through
    behind a pushed-in camera.

    `vx`/`vw` are the part of the card the plate is allowed to occupy. It is the
    whole card most of the time, and everything left of the label when there is
    one -- which is what stops a callout being drawn on top of the screenshot it
    is describing. The surface beside it is not a gap; it is the label's ground.
    """
    x = vx + (vw - pw * k) / 2.0 if pw * k < vw else min(vx, max(vx + vw - pw * k, x))
    y = (SLOT_H - ph * k) / 2.0 if ph * k < SLOT_H else min(0.0, max(SLOT_H - ph * k, y))
    return x, y


def _look(rect, pw, ph, k, reserve=0.0):
    """Translate that brings `rect` -- in the PLATE's own pixels -- into the card
    at scale k.

    This is the point of the machine. Every other still here is aimed with a
    percentage of the slot, which is a different space from the one the capture is
    measured in, and the two agree only when the aspects happen to match. A
    rectangle read off the capture cannot drift out of frame, because the framing
    is computed from it rather than the other way round.
    """
    rx, ry, rw, rh = [float(v) for v in rect]
    vx, vw = LOOK_PAD, SLOT_W - reserve - LOOK_PAD * 2
    x = vx + vw / 2.0 - (rx + rw / 2.0) * k
    y = SLOT_H / 2.0 - (ry + rh / 2.0) * k
    return _clamp(x, y, pw, ph, k, vx, vw)


def _look_scale(rects, reserve=0.0):
    """One scale for every detail stop, so a pan between them is a pan and not a
    second zoom. The tightest rect decides it."""
    avail_w = SLOT_W - LOOK_PAD * 2 - reserve
    avail_h = SLOT_H - LOOK_PAD * 2
    k = min(min(avail_w / float(r[2]), avail_h / float(r[3])) for r in rects)
    return min(k, MAX_K)


def stage(shots, alt, caption, look=None, call=None, rest=None,
          plate=None, dur="13s", radius=7, root="../../"):
    """A capture as an object on a surface, with a camera over it.

    shots  one src, or several. Several stack IN REGISTER at the plate's own size
           and cross-fade: states of one screen, not different screens.
    look   the region worth going to, in the PLATE's pixels, read off the capture
           at its authored size. One (x,y,w,h) rect for a push; two for a push and
           then a pan between them at a fixed scale. Omit it and the figure holds
           the whole plate still, which is right more often than the habit of
           always moving suggests.
    call   (label, description) for what `look` lands on. Drawn beside the region,
           arriving as the camera does. Needs `look`: a label with nothing to point
           at is a caption, and captions go underneath.
    rest   index of the shot to hold when nothing is moving. Defaults to the first,
           but for a sequence that ends somewhere the state worth leaving on screen
           is usually the one it ends in.
    plate  the capture's authored size. 1440x810 is the house 16:9; pass real
           numbers for anything else and the arithmetic follows them.
    """
    if isinstance(shots, str):
        shots = [shots]
    if look and isinstance(look[0], (int, float)):
        look = [look]
    pw, ph = _plate_size(shots[0], plate)
    n = max(len(shots), 1)
    rest_i = n - 1 if rest is None and n > 1 else (rest or 0)

    reserve = (CALL_W + CALL_GAP + LOOK_PAD) if (call and look) else 0.0
    view_w = SLOT_W - reserve
    x0, y0, k0 = _fit(pw, ph, REST_PAD, view_w)
    cls = "cs-media cam cam-stage"
    var = ('--pw:%dpx;--ph:%dpx;--plate-r:%dpx;--dur:%s;--n:%d;'
           '--x0:%.1fpx;--y0:%.1fpx;--k0:%.4f'
           % (pw, ph, radius, dur, n, x0, y0, k0))
    if reserve:
        var += ';--vx:0px;--vw:%.1fpx' % view_w

    call_html = ""
    if look:
        k1 = _look_scale(look, reserve)
        cls += " moves"
        for i, rect in enumerate(look[:2]):
            lx, ly = _look(rect, pw, ph, k1, reserve)
            var += ';--x%d:%.1fpx;--y%d:%.1fpx' % (i + 1, lx, i + 1, ly)
        var += ';--k1:%.4f' % k1
        if len(look) > 1:
            cls += " pans"
        if call:
            label, desc = call
            rx, ry, rw, rh = [float(v) for v in look[0]]
            ax, ay = _look(look[0], pw, ph, k1, reserve)
            mid = ay + (ry + rh / 2.0) * k1
            # The column the view gave up is where it goes; nothing to solve.
            side, cx = "", view_w + CALL_GAP
            cx = min(cx, SLOT_W - LOOK_PAD - CALL_W)
            cy = max(LOOK_PAD, min(mid - 26.0, SLOT_H - LOOK_PAD - 74.0))
            call_html = (
                '          <div class="call%s" style="--cx:%.1fpx;--cy:%.1fpx;'
                '--cw:%dpx">\n'
                '            <div class="call-row"><span class="call-line"></span>'
                '<span class="call-note">%s</span></div>\n'
                '            <p class="call-desc">%s</p>\n'
                '          </div>\n'
                % (side, cx, cy, int(CALL_W), esc(label), esc(desc)))

    o = ['        <div class="%s" style="%s">\n' % (cls, var),
         '          <div class="view">\n',
         '            <div class="plate">\n']
    for i, src in enumerate(shots):
        o.append('              <img class="%s" style="--i:%d" src="%sassets/%s" '
                 'alt="%s"%s loading="lazy">\n'
                 % ("rest" if i == rest_i else "", i, root, src,
                    esc(alt) if i == rest_i else "",
                    "" if i == rest_i else ' aria-hidden="true"'))
    o.append('            </div>\n          </div>\n')
    o.append(call_html)
    o.append('        </div>\n')
    return _fig("".join(o), caption)
