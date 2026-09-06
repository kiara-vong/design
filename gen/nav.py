# -*- coding: utf-8 -*-
"""The floating nav pill, in one place.

It appears on every page and every page used to carry its own copy, which is how
the About page ended up with four icons while the index had four different ones.
Built here instead: the caller says which entry is current, and that entry moves
into the labelled slot on the left. That slot is the pill's one piece of state --
it is what tells you where you are without a second indicator.
"""

# Two icons were added for the Art and Resume pages. Both are drawn on the same
# 28x28 grid at the same 2px stroke as the ones inherited from the reference
# build, so the row reads as one set rather than four borrowed marks and two new.
ICONS = {
    "index": ('32', '<path d="M20 28V17.3333C20 16.9797 19.8595 16.6406 19.6095 16.3905C19.3594 16.1405 19.0203 16 18.6667 16H13.3333C12.9797 16 12.6406 16.1405 12.3905 16.3905C12.1405 16.6406 12 16.9797 12 17.3333V28"/>'
              '<path d="M4 13.3333C3.99991 12.9454 4.08445 12.5622 4.24772 12.2103C4.41099 11.8584 4.64906 11.5464 4.94533 11.296L14.2787 3.296C14.76 2.88921 15.3698 2.66603 16 2.66603C16.6302 2.66603 17.24 2.88921 17.7213 3.296L27.0547 11.296C27.3509 11.5464 27.589 11.8584 27.7523 12.2103C27.9156 12.5622 28.0001 12.9454 28 13.3333V25.3333C28 26.0406 27.719 26.7189 27.219 27.2189C26.7189 27.719 26.0406 28 25.3333 28H6.66667C5.95942 28 5.28115 27.719 4.78105 27.2189C4.28095 26.7189 4 26.0406 4 25.3333V13.3333Z"/>'),
    # Archive: the reference build's bookmarked-volume mark.
    "archive": ('28', '<path d="M11.6667 2.33333V11.6667L15.1667 8.16667L18.6667 11.6667V2.33333"/>'
                '<path d="M4.66667 22.75V5.25C4.66667 4.47645 4.97396 3.73459 5.52094 3.18761C6.06792 2.64062 6.80979 2.33333 7.58333 2.33333H22.1667C22.4761 2.33333 22.7728 2.45625 22.9916 2.67504C23.2104 2.89383 23.3333 3.19058 23.3333 3.5V24.5C23.3333 24.8094 23.2104 25.1062 22.9916 25.325C22.7728 25.5438 22.4761 25.6667 22.1667 25.6667H7.58333C6.80979 25.6667 6.06792 25.3594 5.52094 24.8124C4.97396 24.2654 4.66667 23.5235 4.66667 22.75ZM4.66667 22.75C4.66667 21.9765 4.97396 21.2346 5.52094 20.6876C6.06792 20.1406 6.80979 19.8333 7.58333 19.8333H23.3333"/>'),
    # Art: a framed picture with a horizon and a sun, which reads at 28px where a
    # palette-and-brush does not -- a palette becomes a blob below about 40.
    "art": ('28', '<path d="M4.66667 4.66667C4.66667 3.5621 5.5621 2.66667 6.66667 2.66667H21.3333C22.4379 2.66667 23.3333 3.5621 23.3333 4.66667V23.3333C23.3333 24.4379 22.4379 25.3333 21.3333 25.3333H6.66667C5.5621 25.3333 4.66667 24.4379 4.66667 23.3333V4.66667Z"/>'
            '<path d="M10.5 11.0833C11.4665 11.0833 12.25 10.2998 12.25 9.33333C12.25 8.36683 11.4665 7.58333 10.5 7.58333C9.5335 7.58333 8.75 8.36683 8.75 9.33333C8.75 10.2998 9.5335 11.0833 10.5 11.0833Z"/>'
            '<path d="M4.66667 19.8333L10.2083 14.2917C10.9894 13.5106 12.2556 13.5106 13.0367 14.2917L18.6667 19.9217"/>'
            '<path d="M16.9167 18.1667L18.7083 16.375C19.4894 15.5939 20.7556 15.5939 21.5367 16.375L23.3333 18.1717"/>'),
    # Resume: a sheet with ruled lines and a turned corner.
    "resume": ('28', '<path d="M16.3333 2.33333H8.16667C7.5478 2.33333 6.95434 2.57917 6.51675 3.01675C6.07917 3.45434 5.83333 4.0478 5.83333 4.66667V23.3333C5.83333 23.9522 6.07917 24.5457 6.51675 24.9832C6.95434 25.4208 7.5478 25.6667 8.16667 25.6667H19.8333C20.4522 25.6667 21.0457 25.4208 21.4832 24.9832C21.9208 24.5457 22.1667 23.9522 22.1667 23.3333V8.16667L16.3333 2.33333Z"/>'
               '<path d="M16.3333 2.33333V8.16667H22.1667"/>'
               '<path d="M10.5 14H17.5"/><path d="M10.5 18.6667H17.5"/><path d="M10.5 9.33333H12.25"/>'),
    "email": ('32', '<path d="M29.3333 9.33333L17.3453 16.9693C16.9385 17.2056 16.4764 17.3301 16.006 17.3301C15.5356 17.3301 15.0735 17.2056 14.6667 16.9693L2.66667 9.33333"/>'
              '<path d="M26.6667 5.33333H5.33333C3.86057 5.33333 2.66667 6.52724 2.66667 8V24C2.66667 25.4728 3.86057 26.6667 5.33333 26.6667H26.6667C28.1394 26.6667 29.3333 25.4728 29.3333 24V8C29.3333 6.52724 28.1394 5.33333 26.6667 5.33333Z"/>'),
}

LABELS = {"index": "Home", "archive": "Projects", "art": "Art",
          "resume": "Resume", "about": "About", "email": "Copy email"}
# Relative to the ROOT of the site. nav() and pill() prefix them, because half the
# pages now live one folder down and a bare "index.html" from art/ is art/index.html.
HREFS = {"index": "index.html", "archive": "index.html#projects", "art": "pages/art/",
         "resume": "resume.html", "about": "about.html"}

# The About page's own person mark, kept so that entry is unchanged.
ICONS["about"] = ('28', '<path d="M14 25.6667C20.4433 25.6667 25.6667 20.4433 25.6667 14C25.6667 7.55668 20.4433 2.33333 14 2.33333C7.55668 2.33333 2.33333 7.55668 2.33333 14C2.33333 20.4433 7.55668 25.6667 14 25.6667Z"/>'
                  '<path d="M14 15.1667C15.933 15.1667 17.5 13.5997 17.5 11.6667C17.5 9.73367 15.933 8.16667 14 8.16667C12.067 8.16667 10.5 9.73367 10.5 11.6667C10.5 13.5997 12.067 15.1667 14 15.1667Z"/>'
                  '<path d="M8.16667 24.1057V22.1667C8.16667 21.5478 8.4125 20.9543 8.85008 20.5167C9.28767 20.0792 9.88116 19.8333 10.5 19.8333H17.5C18.1188 19.8333 18.7123 20.0792 19.1499 20.5167C19.5875 20.9543 19.8333 21.5478 19.8333 22.1667V24.1057"/>')

ORDER = ["index", "archive", "art", "about", "email"]


def _svg(key):
    size, paths = ICONS[key]
    return ('<svg width="%s" height="%s" viewBox="0 0 %s %s" fill="none" '
            'stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            'stroke-linejoin="round">%s</svg>' % (size, size, size, size, paths))


def pill(current="index", indent="      ", root=""):
    """Render the pill with `current` in the labelled slot."""
    if current not in ORDER:
        current = "index"
    home = current
    rest = [k for k in ORDER if k != home]
    i = indent
    o = ['%s<div class="nav-inner">\n' % i,
         '%s  <div class="nav-home">\n' % i,
         '%s    <a href="%s" aria-label="%s" data-tip="%s">\n%s      %s\n%s    </a>\n'
         % (i, (root + HREFS.get(home, "#")), LABELS[home], LABELS[home], i, _svg(home), i),
         '%s    <span class="label">%s</span>\n' % (i, LABELS[home]),
         '%s  </div>\n' % i,
         '%s  <div class="nav-sep"></div>\n' % i,
         '%s  <div class="nav-icons">\n' % i]
    for k in rest:
        if k == "email":
            o.append('%s    <a href="#" aria-label="Email" data-tip="Copy email" '
                     'data-mail>\n%s      %s\n%s    </a>\n' % (i, i, _svg(k), i))
        else:
            o.append('%s    <a href="%s" aria-label="%s" data-tip="%s">\n%s      %s\n%s    </a>\n'
                     % (i, (root + HREFS[k]), LABELS[k], LABELS[k], i, _svg(k), i))
    o.append('%s  </div>\n%s</div>' % (i, i))
    return "".join(o)


def nav(current="index", indent="    ", root=""):
    return ('%s<nav class="nav" aria-label="Primary">\n%s\n%s</nav>'
            % (indent, pill(current, indent + "  ", root), indent))
