# -*- coding: utf-8 -*-
"""The case-study page's repeating content blocks.

These live in their own module rather than inside gen-cases.py because they are
the pieces a page is assembled FROM, while gen-cases.py owns the page shell that
assembles them. Keeping the two apart also means the block markup is somewhere a
person can read it against case-study.css without scrolling past a page template.
"""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def stats(eyebrow, rows, note=None):
    """The Impact callout: an eyebrow rule, three counting numbers, a footnote.

    case-study.js plays this once when it scrolls into view: the rule draws out,
    the stats rise in sequence, and each number counts up to its data-to. That
    attribute carries its own precision, so "4.8" counts to one decimal and "8"
    to none. The visible text is only the starting value.

    rows: (data_to, starting_text, label, definition)
    """
    o = ['      <figure class="cs-figure">\n        <div class="stats">\n',
         '          <p class="stats-eyebrow"><span></span>%s</p>\n' % esc(eyebrow),
         '          <div class="stats-row">\n']
    for to, start, label, detail in rows:
        o.append('            <div class="stat">'
                 '<span class="stat-n" data-to="%s">%s</span>'
                 '<span class="stat-l">%s</span>'
                 '<span class="stat-d">%s</span></div>\n'
                 % (to, esc(start), esc(label), esc(detail)))
    o.append('          </div>\n')
    if note:
        o.append('          <p class="stats-note">%s</p>\n' % note)
    o.append('        </div>\n      </figure>\n')
    return "".join(o)


def rules(items):
    """A short numbered list of constraints, set as a bordered table.

    For things that were decided and written down before the design started.
    Prose buries them; a table is closer to what they actually looked like.
    """
    o = ['      <div class="cs-rules">\n']
    for i, (title, desc) in enumerate(items, 1):
        o.append('        <div class="cs-rule">'
                 '<span class="n">%02d</span>'
                 '<span class="t">%s</span>'
                 '<span class="d">%s</span></div>\n' % (i, esc(title), desc))
    o.append('      </div>\n')
    return "".join(o)


def figure_raw(src, alt, caption):
    """A figure whose media is a raster screenshot rather than a drawn SVG."""
    return ('      <figure class="cs-figure">\n'
            '        <div class="cs-media">\n'
            '          <img class="cs-flat" src="assets/%s" alt="%s">\n'
            '        </div>\n'
            '        <figcaption class="cs-caption">%s</figcaption>\n'
            '      </figure>\n' % (src, esc(alt), esc(caption)))


# Drawn rather than a glyph: an arrow character sits on the text baseline and
# rides whatever the font does, and this one has to sit on the ROW's centre
# whatever the two sides wrap to.
ARROW = ('<svg class="arw" viewBox="0 0 20 12" aria-hidden="true">'
         '<path d="M1 6h16M13 2l4 4-4 4"/></svg>')


def before_after(rows, before="Before", after="After"):
    """A two-column ledger of what changed, as markup rather than an image.

    Markup so the text stays selectable, searchable and translatable, and so it
    reflows on a phone instead of becoming a 799px image someone has to pinch.
    """
    o = ['      <figure class="cs-figure">\n        <div class="cs-ba">\n',
         '          <div class="cs-ba-head"><span>%s</span><span></span>'
         '<span>%s</span></div>\n' % (esc(before), esc(after))]
    for b, a in rows:
        o.append('          <div class="cs-ba-row">'
                 '<p class="b">%s</p>%s<p class="a">%s</p></div>\n'
                 % (esc(b), ARROW, esc(a)))
    o.append('        </div>\n      </figure>\n')
    return "".join(o)


# Media kinds, and the colour each gets on its chip. Kind is the first thing you
# need to know about a brief -- whether you are opening a camera, a screen
# recorder, or a screenshot tool -- so it leads.
KINDS = {
    "still": ("Still", "is-still"),
    "seq": ("Sequence", "is-seq"),
    "video": ("Video / loop", "is-video"),
    "anno": ("Annotated still", "is-still"),
}


def plate(kind, technique, what, why, shots=(), spec=()):
    """A figure slot that has not been filled, describing what belongs in it.

    Rendered at the exact size of the finished asset, so a brief that does not fit
    here is a brief whose asset will not fit either.

    kind      -- which tool you reach for (see KINDS)
    technique -- the presentation device it feeds, in the reference build's terms
    what      -- one line naming the capture
    why       -- what it has to prove
    shots     -- the individual frames or states to grab
    spec      -- (label, value) pairs: size, format, duration
    """
    label, cls = KINDS.get(kind, KINDS["still"])
    o = ['      <figure class="cs-figure">\n        <div class="cs-plate">\n',
         '          <div class="cs-plate-top">'
         '<span class="cs-kind %s">%s</span>'
         '<span class="cs-tech">%s</span></div>\n' % (cls, esc(label), esc(technique)),
         '          <h3>%s</h3>\n' % esc(what),
         '          <p>%s</p>\n' % esc(why)]
    if shots:
        o.append('          <ul>%s</ul>\n'
                 % "".join('<li>%s</li>' % esc(x) for x in shots))
    if spec:
        o.append('          <div class="cs-spec">%s</div>\n'
                 % "".join('<span><b>%s</b> %s</span>' % (esc(k), esc(v))
                           for k, v in spec))
    o.append('        </div>\n      </figure>\n')
    return "".join(o)
