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
