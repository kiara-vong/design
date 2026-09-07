import io
import json
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
    """A figure, and its caption only if it has one.

    An empty caption used to render as an empty <figcaption>, which is not nothing:
    it keeps the caption's top margin and line box, so a figure with no words under
    it sat further from the next one than a figure with words. Some figures say
    everything they have to say inside the frame -- a callout naming the thing it
    points at is already a sentence -- and those should close at the frame.
    """
    cap = ('        <figcaption class="cs-caption">%s</figcaption>\n'
           % esc(caption)) if caption else ''
    return ('      <figure class="cs-figure">\n%s%s      </figure>\n'
            % (inner, cap))


# The window every figure on this site sits in.
#
# The stage machines draw their own chrome, on a plate that moves inside the card.
# The older machines below do not: they fill the card edge to edge, which made a
# screenshot on this site read as two different kinds of object depending on which
# machine happened to be holding it. It is the same kind of object. It is a screen.
#
# So the chrome is drawn here instead, and the machine's own content goes into
# .win -- a positioned box under the bar. Everything inside keeps working
# unchanged, because inset:0 resolves against the nearest positioned ancestor and
# .win is now that ancestor. The content box goes from 799x391 to 799x365, which
# is why gen/plates.py computes strip travel against 365.
FRAME_BAR = 26


def _win(cls, inner, style=""):
    return ('        <div class="cs-media cam framed %s"%s>\n'
            '          <span class="bar" aria-hidden="true">'
            '<i></i><i></i><i></i><b></b></span>\n'
            '          <div class="win">\n%s'
            '          </div>\n'
            '        </div>\n'
            % (cls, (' style="%s"' % style) if style else "", inner))


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
    return _fig(_win("cam-clip",
        '            <video src="%sassets/video/%s.mp4" '
        'poster="%sassets/video/%s-poster.jpg" '
        'autoplay muted loop playsinline preload="metadata" '
        'aria-label="%s"></video>\n' % (root, name, root, name, esc(alt))), caption)


def push(src, alt, caption, z=1.4, fx="50%", fy="50%", dur="13s", root="../../"):
    """A still, framed whole and then pushed in on one part of itself.

    fx/fy name the point worth looking at, as percentages of the image, so the push
    frames the callout rather than the middle.
    """
    return _fig(_win("cam-push",
        '            <img src="%sassets/%s" alt="%s" loading="lazy">\n'
        % (root, src, esc(alt)),
        "--z:%s;--fx:%s;--fy:%s;--dur:%s" % (z, fx, fy, dur)), caption)


def strip(src, alt, caption, travel, dur="17s", root="../../"):
    """A tall still scrolling behind a fixed frame.

    travel is a PERCENTAGE OF THE IMAGE'S OWN HEIGHT, never a pixel count. See the
    note in camera.css for why that distinction has its own paragraph.
    """
    return _fig(_win("cam-strip",
        '            <img src="%sassets/%s" alt="%s" loading="lazy">\n'
        % (root, src, esc(alt)),
        "--travel:%s;--dur:%s" % (travel, dur)), caption)


def wipe(before_src, after_src, alt, caption,
         before="Explored", after="Shipped", dur="11s", root="../../"):
    """Two stills under a travelling seam, labelled inside the frame.

    The labels sit in the picture rather than in the caption because the whole
    figure is a comparison, and a reader who has to look away to find out which half
    is which is doing the work the figure was meant to do for them.
    """
    return _fig(_win("cam-wipe",
        '            <img src="%sassets/%s" alt="%s" loading="lazy">\n'
        '            <img src="%sassets/%s" alt="" aria-hidden="true" loading="lazy">\n'
        '            <span class="seam"></span>\n'
        '            <span class="tag b">%s</span><span class="tag a">%s</span>\n'
        % (root, before_src, esc(alt), root, after_src, esc(before), esc(after)),
        "--dur:%s" % dur), caption)


def deal(srcs, alt, caption, dur="14s", root="../../"):
    """N stills at identical framing, cross-fading. The first is the resting state.

    Which means the first entry should be the frame worth leaving on screen, since
    it is what reduced motion and a paused page both get.
    """
    o = []
    for i, src in enumerate(srcs):
        o.append('            <img style="--i:%d" src="%sassets/%s" alt="%s"%s '
                 'loading="lazy">\n'
                 % (i, root, src, esc(alt) if i == 0 else "",
                    "" if i == 0 else ' aria-hidden="true"'))
    return _fig(_win("cam-deal", "".join(o),
                     "--dur:%s;--n:%d" % (dur, len(srcs))), caption)


def flat(src, alt, caption, root="../../"):
    """A drawn figure, held still, and deliberately NOT in a browser window.

    Everything else on this site that holds a picture wraps it in chrome, because
    everything else is holding a screen. This is not: it is a diagram, drawn for
    the page, explaining something no screenshot of the product could show. Putting
    a title bar around it would claim it was a screenshot, which is the one thing
    it is not, and the reader would spend a moment looking for the application it
    came from.

    The SVG animates itself from its own <style>, so there is no camera machine
    over the top of it either: a machine here would be a second thing moving, out
    of phase with the first. The slot holds it whole -- contain rather than cover,
    since a diagram cropped at the edges is a diagram missing an edge.
    """
    return _fig(
        '        <div class="cs-media cs-diagram">\n'
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
    # The bar lives inside .ann-view rather than on the figure, because this
    # machine's labels sit in a column beside the picture: chrome across the whole
    # card would be a browser window with a set of annotations inside it, which is
    # not what is being shown.
    o.append('          <div class="ann-view framed">'
             '<span class="bar" aria-hidden="true"><i></i><i></i><i></i><b></b>'
             '</span><div class="win">'
             '<img src="%sassets/%s" alt="%s" loading="lazy"></div></div>\n'
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

# The window chrome, in plate pixels, as a fraction of the plate's width.
# Proportional rather than fixed so it renders at about the same size as
# the home tiles' own title bar whatever the capture's resolution is.
BAR = 0.026

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


def _fig_video(src):
    return src.endswith(".mp4")


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


def page(shots, alt, caption, view=(1280, 600), look=None, scroll=0,
         dur="20s", radius=None, root="../../"):
    """A whole page behind a window, scrolled, with states landing in order.

    stage() above holds a screen: the capture is the size of the window and the
    camera moves over it. That is wrong for a list, because a list's argument is
    its length and its length is the part that does not fit. So here the window is
    fixed and the PAGE moves inside it, which is what a browser is.

    shots  full-page captures, in the order they happen. They are hung from the
           same reel at the window's width, so they may be different HEIGHTS --
           which is the point: a filtered list is a shorter page, and letting it be
           one is the difference between a grid collapsing and three pictures
           cross-fading. Different delivery widths are fine too; they are all drawn
           at the window's width, so only the aspect has to be honest.
    view   the window, in CSS pixels, at the size the captures were taken. Not
           forced to 16:9: the fold is wherever the capture's own viewport put it,
           and moving it would put the page's own layout out of step with itself.
    look   the region the camera closes on at the end, in the WINDOW's pixels at
           the `scroll` position below -- not in the page's. The window is what the
           reader is looking through and the reel is what is behind it, so a
           rectangle in window coordinates is the only one that can be checked by
           looking at the figure.
    scroll how far the page is carried down for that closing look, in page pixels
           at the window's width. The reason this exists: the framing that shows a
           list narrowing and the framing that shows the switches doing it are
           usually not the same framing, and on a long rail the switches are below
           the fold. The camera alone cannot reach them; the reel can bring them.
    """
    if isinstance(shots, str):
        shots = [shots]
    vw, vh = [float(v) for v in view]
    n = max(len(shots), 1)

    bar = round(vw * BAR)
    radius = round(vw * 0.013) if radius is None else radius
    pw, ph = vw, vh + bar           # the window is the viewport plus its chrome

    # How far the first page runs past the fold, from its delivered aspect. Read
    # rather than typed: the plate is resized on delivery, so any travel written by
    # hand is a number that was true of a file that is no longer on disk.
    sw, sh = _plate_size(shots[0])
    sy = max(0.0, sh * (vw / float(sw)) - vh)

    x0, y0, k0 = _fit(pw, ph, REST_PAD)
    cls = "cs-media cam cam-stage page" + (" solo" if n == 1 else "")
    var = ('--pw:%dpx;--ph:%dpx;--bar:%dpx;--plate-r:%dpx;--dur:%s;--n:%d;'
           '--x0:%.1fpx;--y0:%.1fpx;--k0:%.4f;--sy:%.1fpx;--sr:%.1fpx'
           % (pw, ph, bar, radius, dur, n, x0, y0, k0, -sy, -float(scroll)))

    if look:
        rect = (look[0], look[1] + bar, look[2], look[3])
        k1 = _look_scale([rect])
        lx, ly = _look(rect, pw, ph, k1)
        cls += " moves"
        var += ';--x1:%.1fpx;--y1:%.1fpx;--k1:%.4f' % (lx, ly, k1)

    o = ['        <div class="%s" style="%s">\n' % (cls, var),
         '          <div class="view">\n',
         '            <div class="plate">\n',
         '              <span class="bar" aria-hidden="true">'
         '<i></i><i></i><i></i><b></b></span>\n',
         '              <div class="shots">\n',
         '                <div class="reel">\n']
    for i, src in enumerate(shots):
        o.append('                  <img style="--i:%d" src="%sassets/%s" '
                 'alt="%s"%s loading="lazy">\n'
                 % (i, root, src, esc(alt) if i == 0 else "",
                    "" if i == 0 else ' aria-hidden="true"'))
    o.append('                </div>\n              </div>\n'
             '            </div>\n          </div>\n')
    o.append('        </div>\n')
    return _fig("".join(o), caption)


# The patch of page the pressed button sits on, so the crop that shrinks has
# something to shrink against. Sampled from the captures rather than guessed --
# it is the one colour in this file that has to match a file on disk exactly.
PRESS_BG = "#FBF8F4"
PRESS_PAD = 12.0


# The control column beside a stepper. Wider than a callout's, because it holds a
# button rather than a label and a button that wraps mid-word reads as broken.
STEP_W, STEP_GAP = 178.0, 20.0


def stepper(shots, alt, caption, label="Place the next tile", again="Start over",
            note=None, plate=None, radius=None, root="../../"):
    """A run the reader advances themselves, one frame per click.

    Every other machine here plays at the reader. This one waits, and the reason
    is specific to what it is showing: the argument is that the island is not
    drawn but DECIDED, one cell after another, each following from what was
    already settled. A loop makes that something you watch. A click makes it
    something you do, and only the second puts the reader where the algorithm is.

    shots  frames of one run, in order. Captured beforehand and chosen at equal
           increments of filled area, so every click is worth the same amount --
           a stepper with uneven steps reads as a slideshow with a button and
           nobody presses it twice.
    label  what the button says, and `again` what it says at the end, where it
           restarts rather than dead-ending on a finished picture.
    """
    if isinstance(shots, str):
        shots = [shots]
    pw, ph = _plate_size(shots[0], plate)
    n = len(shots)
    bar = round(pw * BAR)
    radius = round(pw * 0.013) if radius is None else radius
    ph += bar

    reserve = STEP_W + STEP_GAP + LOOK_PAD
    view_w = SLOT_W - reserve
    x0, y0, k0 = _fit(pw, ph, REST_PAD, view_w)
    var = ('--pw:%dpx;--ph:%dpx;--bar:%dpx;--plate-r:%dpx;--n:%d;'
           '--x0:%.1fpx;--y0:%.1fpx;--k0:%.4f;--vx:0px;--vw:%.1fpx;'
           '--cx:%.1fpx;--cw:%dpx'
           % (pw, ph, bar, radius, n, x0, y0, k0, view_w,
              view_w + STEP_GAP, int(STEP_W)))

    o = ['        <div class="cs-media cam cam-stage cam-step" style="%s"'
         ' data-label="%s" data-again="%s">\n' % (var, esc(label), esc(again)),
         '          <div class="view">\n',
         '            <div class="plate">\n',
         '              <span class="bar" aria-hidden="true">'
         '<i></i><i></i><i></i><b></b></span>\n',
         '              <div class="shots">\n']
    for i, src in enumerate(shots):
        o.append('                <img style="--i:%d" src="%sassets/%s" '
                 'alt="%s"%s loading="lazy">\n'
                 % (i, root, src, esc(alt) if i == 0 else "",
                    "" if i == 0 else ' aria-hidden="true"'))
    o.append('              </div>\n            </div>\n          </div>\n')
    # No counter and no progress track. Both answer a question the reader was not
    # asking -- how far through a slideshow am I -- and asking it turns a run of
    # the solver into a chore with a known length. What is on screen is how far
    # along it is; that is the only progress indicator this needs.
    o.append('          <div class="step-ui">\n'
             '            <button class="step-go" type="button">%s</button>\n'
             % esc(label))
    if note:
        o.append('            <p class="step-note">%s</p>\n' % esc(note))
    o.append('          </div>\n        </div>\n')
    return _fig("".join(o), caption)


def slider(before, after, alt, caption, tags=("before", "after"),
           start=50, handle="Reveal the after state", plate=None,
           radius=None, root="../../"):
    """Two frames of one run, in register, with a line the reader DRAGS.

    Not to be confused with wipe() above, which is the older machine and does a
    different job: that one runs its own seam back and forth on a timer and is
    right for a comparison the reader should be handed. This one waits for a hand.
    A figure that moves at you is a claim; a figure you move is a check, and which
    of the two you want depends on whether the reader has any reason to doubt you.

    (These were the same name for about an hour, which is long enough for Python
    to quietly hand every caller of the old one the new one instead. The names are
    different now for that reason rather than for a nice one.)

    A before and an after are only a comparison if nothing else changed between
    them. That is a condition on the CAPTURE, not on this code: the run has to be
    recorded with the camera still, so the only difference across the seam is the
    thing being compared. Frames from a turning scene make a glitch, not an
    argument -- the eye reads the jump in the silhouette long before it reads
    either half.

    The handle and its labels are positioned against the window's DRAWN rectangle,
    computed here and handed over as --wx/--wy/--ww/--wh, because the plate is
    scaled to fit and anything drawn inside it is scaled with it: a hairline would
    land at half a pixel and a label would end up under six point. The clip stays
    in the plate's own space, where a percentage means the same thing either side.
    """
    pw, ph = _plate_size(before, plate)
    bar = round(pw * BAR)
    radius = round(pw * 0.013) if radius is None else radius
    ph += bar
    x0, y0, k0 = _fit(pw, ph, REST_PAD)
    barh = bar * k0
    var = ('--pw:%dpx;--ph:%dpx;--bar:%dpx;--plate-r:%dpx;--n:2;'
           '--x0:%.1fpx;--y0:%.1fpx;--k0:%.4f;--s:%d;'
           '--wx:%.1fpx;--wy:%.1fpx;--ww:%.1fpx;--wh:%.1fpx'
           % (pw, ph, bar, radius, x0, y0, k0, int(start),
              x0, y0 + barh, pw * k0, ph * k0 - barh))
    return _fig(
        '        <div class="cs-media cam cam-stage cam-slide" style="%s">\n'
        '          <div class="view">\n'
        '            <div class="plate">\n'
        '              <span class="bar" aria-hidden="true">'
        '<i></i><i></i><i></i><b></b></span>\n'
        '              <div class="shots">\n'
        '                <img src="%sassets/%s" alt="%s" loading="lazy">\n'
        '                <img src="%sassets/%s" alt="" aria-hidden="true" '
        'loading="lazy">\n'
        '              </div>\n            </div>\n          </div>\n'
        '          <span class="slide-tag left">%s</span>\n'
        '          <span class="slide-tag right">%s</span>\n'
        '          <span class="slide-line" aria-hidden="true"><i></i></span>\n'
        '          <input class="slide-range" type="range" min="0" max="100" '
        'value="%d" aria-label="%s">\n'
        '        </div>\n'
        % (var, root, before, esc(alt), root, after,
           esc(tags[0]), esc(tags[1]), int(start), esc(handle)), caption)


def walk(steps, alt, caption, view=(1280, 600), press_bg=None, press_pad=8,
         dur="28s", radius=None, root="../../"):
    """A route through an application, clicked out step by step.

    flow() is this with two screens and one click. A drill-down is neither: it is
    a path, and what a path has to show is that each screen FOLLOWED from the
    last. Four stills in a row cannot say that -- the reader is left working out
    what was pressed between them, which is the one thing the figure exists to
    supply.

    steps  four dicts, in order: {page, press, scroll}. `press` is the thing
           clicked to reach the NEXT screen, so the last step has none. It is a
           rectangle in that screen's own pixels, read off the capture -- there is
           no percentage anywhere in this machine, which is why it can be trusted
           to land on the card it says it lands on.

           The camera does not move. That is a choice: the route is the figure,
           and going in and out of it four times turns a path into a series of
           destinations. What has to read instead is the click, which is why the
           press here squashes harder than flow's and leaves a ring behind it.
    scroll set on the one screen that runs past its window: it is scrolled to its
           foot before the camera goes in, because what gets clicked on it is
           below the fold and cutting to it would skip the part that shows why.

    The choreography is fixed at four screens and three clicks. That is not a
    limit worth generalising away until there is a second route to build: the
    keyframes are a script, and a script written for an unknown number of scenes
    is a script that plays none of them well.
    """
    vw, vh = [float(v) for v in view]
    bar = round(vw * BAR)
    radius = round(vw * 0.013) if radius is None else radius
    pw, ph = vw, vh + bar

    scroll = 0.0
    for st in steps:
        if st.get("scroll"):
            sw, sh = _plate_size(st["page"])
            scroll = max(0.0, sh * (vw / float(sw)) - vh)

    x0, y0, k0 = _fit(pw, ph, REST_PAD)
    var = ('--pw:%dpx;--ph:%dpx;--bar:%dpx;--plate-r:%dpx;--dur:%s;--n:%d;'
           '--press-bg:%s;--x0:%.1fpx;--y0:%.1fpx;--k0:%.4f;--sy3:%.1fpx'
           % (pw, ph, bar, radius, dur, len(steps), press_bg or PRESS_BG,
              x0, y0, k0, -scroll))

    o = ['        <div class="cs-media cam cam-stage page cam-walk" '
         'style="%s">\n' % var,
         '          <div class="view">\n',
         '            <div class="plate">\n',
         '              <span class="bar" aria-hidden="true">'
         '<i></i><i></i><i></i><b></b></span>\n',
         '              <div class="shots">\n',
         '                <div class="reel">\n']
    for i, st in enumerate(steps):
        o.append('                  <img style="--i:%d" src="%sassets/%s" '
                 'alt="%s"%s loading="lazy">\n'
                 % (i, root, st["page"], esc(alt) if i == 0 else "",
                    "" if i == 0 else ' aria-hidden="true"'))
    for i, st in enumerate(steps):
        if not st.get("press"):
            continue
        bx, by, bw, bh = [float(v) for v in st["press"]]
        o.append('                  <span class="press s%d" aria-hidden="true" '
                 'style="left:%.1fpx;top:%.1fpx;width:%.1fpx;height:%.1fpx">'
                 '<i style="left:%.0fpx;top:%.0fpx;width:%.1fpx;height:%.1fpx;'
                 'background-image:url(%sassets/%s);background-size:%dpx auto;'
                 'background-position:%.1fpx %.1fpx"></i></span>\n'
                 % (i + 1, bx - press_pad, by - press_pad,
                    bw + press_pad * 2, bh + press_pad * 2,
                    press_pad, press_pad, bw, bh,
                    root, st["page"], int(vw), -bx, -by))
    o.append('                </div>\n              </div>\n'
             '            </div>\n          </div>\n')
    o.append('        </div>\n')
    return _fig("".join(o), caption)


def flow(pages, alt, caption, view=(1280, 600), press=None, picks=None,
         look=None, still=False, press_pad=None, press_bg=None,
         dur="22s", radius=None, root="../../"):
    """A form, the button, and the page it takes you to.

    page() above scrolls one page and swaps states of it in place. A form is not
    that shape: it has a before and an after, they are two different pages, and
    the moment worth showing is the one where the first becomes the second. So the
    swap here is a cut rather than a dissolve, and the camera goes in for the
    press and comes back out on the load, which is how looking at a form actually
    goes.

    pages  two full-page captures: the form, filled in, and what it returns.
    press  the button, as (x, y, w, h) in the FIRST page's own pixels at the
           window's width. It becomes a crop of that button, laid exactly over
           itself on a patch of page background, and it is the crop that moves --
           so the press needs no second asset and cannot drift out of register.
    picks  the index gen/quiz_picks.py writes: an un-answered pill for each answer
           on the form, and where each one sits. They are laid over the answers
           they hide and taken away one at a time, so the form is filled in on
           camera rather than arriving already filled in -- which is what the
           capture is, and what the figure would otherwise be claiming did not
           need doing.
    look   where the camera goes for the press, in the first page's pixels too.
           Everything about the first page is stated in the first page's
           coordinates; the scroll offsets are worked out here rather than by
           whoever is writing the figure.
    """
    vw, vh = [float(v) for v in view]
    bar = round(vw * BAR)
    radius = round(vw * 0.013) if radius is None else radius
    pw, ph = vw, vh + bar

    def travel(src):
        sw, sh = _plate_size(src)
        return max(0.0, sh * (vw / float(sw)) - vh)

    sy, sy2 = travel(pages[0]), travel(pages[1])
    # A first page that already fits its window has nothing to scroll, and the
    # ordinary timeline spends a third of its loop scrolling it anyway -- which on
    # screen is a third of a loop where nothing happens at all. The still variant
    # gives that time to the two things this version does have: a longer look at
    # the control before it is pressed, and a longer scroll of what the press
    # returns.
    still_first = still or sy <= 0.5

    x0, y0, k0 = _fit(pw, ph, REST_PAD)
    cls = "cs-media cam cam-stage page flow" + (" still" if still_first else "")
    var = ('--pw:%dpx;--ph:%dpx;--bar:%dpx;--plate-r:%dpx;--dur:%s;--n:2;'
           '--press-bg:%s;--x0:%.1fpx;--y0:%.1fpx;--k0:%.4f;'
           '--sy:%.1fpx;--sy2:%.1fpx'
           % (pw, ph, bar, radius, dur, press_bg or PRESS_BG,
              x0, y0, k0, -sy, -sy2))

    if look:
        # Stated against the page; the camera works in the window, and at the
        # press the window is showing the page scrolled to its foot.
        rect = (look[0], look[1] - sy + bar, look[2], look[3])
        k1 = _look_scale([rect])
        lx, ly = _look(rect, pw, ph, k1)
        cls += " moves"
        var += ';--x1:%.1fpx;--y1:%.1fpx;--k1:%.4f' % (lx, ly, k1)

    o = ['        <div class="%s" style="%s">\n' % (cls, var),
         '          <div class="view">\n',
         '            <div class="plate">\n',
         '              <span class="bar" aria-hidden="true">'
         '<i></i><i></i><i></i><b></b></span>\n',
         '              <div class="shots">\n',
         '                <div class="reel">\n']
    for i, src in enumerate(pages):
        o.append('                  <img style="--i:%d" src="%sassets/%s" '
                 'alt="%s"%s loading="lazy">\n'
                 % (i, root, src, esc(alt) if i == 0 else "",
                    "" if i == 0 else ' aria-hidden="true"'))
    if picks:
        idx = json.load(io.open(picks, encoding="utf-8"))
        f = vw / float(idx["src_w"])
        sheet = "%sassets/plate/dorms-quiz-blanks.webp" % root
        for i, (bx, by, bw, bh) in enumerate(idx["picks"]):
            o.append('                  <span class="pick" aria-hidden="true" '
                     'style="left:%.1fpx;top:%.1fpx;width:%.1fpx;height:%.1fpx;'
                     'background-image:url(%s);background-size:%.1fpx auto;'
                     'background-position:0 %.1fpx"></span>\n'
                     % (bx * f, by * f, bw * f, bh * f, sheet,
                        idx["sprite_w"] * f, -i * idx["row"] * f))
    if press:
        # The margin around the pressed crop is per-figure, because what is next to
        # a button varies: a submit button sits alone on a page and can take a
        # generous patch, while half of a segmented control has the other half
        # against it and a generous patch would paint over it.
        pad = PRESS_PAD if press_pad is None else float(press_pad)
        bx, by, bw, bh = [float(v) for v in press]
        o.append('                  <span class="press" aria-hidden="true" '
                 'style="left:%.1fpx;top:%.1fpx;width:%.1fpx;height:%.1fpx">'
                 '<i style="left:%.0fpx;top:%.0fpx;width:%.1fpx;height:%.1fpx;'
                 'background-image:url(%sassets/%s);background-size:%dpx auto;'
                 'background-position:%.1fpx %.1fpx"></i></span>\n'
                 % (bx - pad, by - pad, bw + pad * 2, bh + pad * 2,
                    pad, pad, bw, bh,
                    root, pages[0], int(vw), -bx, -by))
    o.append('                </div>\n              </div>\n'
             '            </div>\n          </div>\n')
    o.append('        </div>\n')
    return _fig("".join(o), caption)


def stage(shots, alt, caption, look=None, call=None,
          plate=None, dur="13s", radius=None, root="../../"):
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
    The FIRST shot is the resting frame and never fades; the rest stack over it
    and arrive with the camera. So order them so the first is the state worth
    leaving on screen, and the later ones are what the figure is going to reveal.
    plate  the capture's authored size. 1440x810 is the house 16:9; pass real
           numbers for anything else and the arithmetic follows them.
    """
    if isinstance(shots, str):
        shots = [shots]
    if look and isinstance(look[0], (int, float)):
        look = [look]
    pw, ph = _plate_size(shots[0], plate)
    n = max(len(shots), 1)

    bar = round(pw * BAR)
    radius = round(pw * 0.013) if radius is None else radius
    ph += bar                       # the window is the capture plus its chrome
    if look:
        look = [(r[0], r[1] + bar, r[2], r[3]) for r in look]
    reserve = (CALL_W + CALL_GAP + LOOK_PAD) if (call and look) else 0.0
    view_w = SLOT_W - reserve
    x0, y0, k0 = _fit(pw, ph, REST_PAD, view_w)
    # Two states cross-fade on one window; three or more is a progression and
    # arrives in order. Different claim, different machine.
    cls = "cs-media cam cam-stage" + (" seq" if n == 2 else " steps" if n > 2 else "")
    var = ('--pw:%dpx;--ph:%dpx;--bar:%dpx;--plate-r:%dpx;--dur:%s;--n:%d;'
           '--x0:%.1fpx;--y0:%.1fpx;--k0:%.4f'
           % (pw, ph, bar, radius, dur, n, x0, y0, k0))
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
         '            <div class="plate">\n',
         '              <span class="bar" aria-hidden="true">'
         '<i></i><i></i><i></i><b></b></span>\n',
         '              <div class="shots">\n']
    for i, src in enumerate(shots):
        if src.endswith(".mp4"):
            # A clip in the window rather than beside it. The rest of this site
            # frames its screenshots and leaves its recordings bare, which reads as
            # two different kinds of evidence when they are the same kind: both are
            # a screen, and a screen on this site has a window around it. The
            # camera still works over it, though a clip that already moves rarely
            # wants one.
            stem = src.rsplit("/", 1)[-1][:-4]
            o.append('                <video style="--i:%d" src="%sassets/%s" '
                     'poster="%sassets/video/%s-poster.jpg" '
                     'aria-label="%s" autoplay muted loop playsinline '
                     'preload="metadata"></video>\n'
                     % (i, root, src, root, stem, esc(alt)))
            continue
        o.append('                <img style="--i:%d" src="%sassets/%s" '
                 'alt="%s"%s loading="lazy">\n'
                 % (i, root, src, esc(alt) if i == 0 else "",
                    "" if i == 0 else ' aria-hidden="true"'))
    o.append('              </div>\n            </div>\n          </div>\n')
    o.append(call_html)
    o.append('        </div>\n')
    return _fig("".join(o), caption)
