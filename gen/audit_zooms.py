# -*- coding: utf-8 -*-
"""Where does every zoom actually land?

Every push and every annotated label names a point as a percentage. Those
percentages are of the SLOT, not of the image, and the slot shows the image
through object-fit -- cover for a push, contain for an annotated plate. So a
number that looks reasonable in the source can point at empty space once the
crop is applied, and the only way to know is to run the number through the
same maths the browser does and look at the result.

This renders one marked frame per figure: the image, the region the slot
actually shows (red), the anchor (green cross), and the region left visible at
full zoom (blue) -- which is the frame someone actually reads.
"""
import os
import re
import sys

from PIL import Image, ImageDraw

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
OUT = sys.argv[2] if len(sys.argv) > 2 else "zoom-audit"

SLOT_W, SLOT_H = 799.0, 391.0          # .cs-media
ANN_RIGHT = 196.0                       # .ann-view right inset
ANN_W, ANN_H = SLOT_W - ANN_RIGHT, SLOT_H

PUSH_RE = re.compile(
    r'<div class="cs-media cam cam-push" style="([^"]+)">\s*'
    r'<img src="([^"]+)" alt="([^"]*)"', re.S)
ANNGROUP_RE = re.compile(
    r'<div class="ann-group" data-k="([^"]+)" style="([^"]+)">\s*'
    r'<div class="ann-row"><span class="ann-line"></span>'
    r'<span class="ann-note">([^<]*)</span>', re.S)
ANNVIEW_RE = re.compile(r'<div class="ann-view"><img src="([^"]+)"')


def var(style, name, default=None):
    m = re.search(r'--%s:\s*([^;"]+)' % name, style)
    return m.group(1).strip() if m else default


def pct(v, default=50.0):
    if v is None:
        return default
    return float(str(v).replace('%', '').strip())


def cover_map(W, H, slot_w, slot_h, fx, fy):
    """Slot-relative percentages -> image pixels, under object-fit:cover."""
    ia, sa = W / float(H), slot_w / float(slot_h)
    if ia > sa:
        fw, fh = sa / ia, 1.0
    else:
        fw, fh = 1.0, ia / sa
    x0, y0 = (1 - fw) / 2, (1 - fh) / 2
    return ((x0 + fx / 100.0 * fw) * W, (y0 + fy / 100.0 * fh) * H,
            (x0 * W, y0 * H, (x0 + fw) * W, (y0 + fh) * H))


def contain_map(W, H, slot_w, slot_h, fx, fy):
    """Same, under object-fit:contain -- the whole image is shown, letterboxed,
    so a slot percentage maps straight onto the image."""
    return (fx / 100.0 * W, fy / 100.0 * H, (0, 0, W, H))


def zoom_rect(vis, ax, ay, z):
    """What is left visible at scale z, anchored at (ax, ay).

    transform-origin holds the anchor still and everything scales around it, so
    the visible window shrinks by z toward that point."""
    x0, y0, x1, y1 = vis
    w, h = (x1 - x0) / z, (y1 - y0) / z
    return (ax - (ax - x0) / z, ay - (ay - y0) / z,
            ax - (ax - x0) / z + w, ay - (ay - y0) / z + h)


def mark(img_path, ax, ay, vis, zr, label, out_path):
    im = Image.open(img_path).convert("RGB")
    d = ImageDraw.Draw(im)
    d.rectangle(vis, outline=(220, 30, 30), width=5)
    d.rectangle(zr, outline=(40, 110, 240), width=5)
    r = max(14, im.size[0] // 60)
    d.line([ax - r, ay, ax + r, ay], fill=(0, 230, 60), width=5)
    d.line([ax, ay - r, ax, ay + r], fill=(0, 230, 60), width=5)
    d.ellipse([ax - 6, ay - 6, ax + 6, ay + 6], outline=(0, 240, 240), width=4)
    im.thumbnail((1100, 1100), Image.LANCZOS)
    im.save(out_path, quality=86)


def main():
    os.makedirs(os.path.join(ROOT, OUT), exist_ok=True)
    pages = []
    for d in ("projects", "work"):
        p = os.path.join(ROOT, d)
        if os.path.isdir(p):
            pages += [os.path.join(p, f) for f in sorted(os.listdir(p))
                      if f.endswith(".html")]

    rows = []
    for page in pages:
        html = open(page, encoding="utf-8").read()
        stem = os.path.splitext(os.path.basename(page))[0]

        for style, src, alt in PUSH_RE.findall(html):
            rel = src.replace("../", "")
            img = os.path.join(ROOT, rel)
            if not os.path.exists(img):
                rows.append((stem, "push", rel, "MISSING", "", ""))
                continue
            W, H = Image.open(img).size
            fx, fy = pct(var(style, "fx")), pct(var(style, "fy"))
            z = float(var(style, "z", "1.4"))
            ax, ay, vis = cover_map(W, H, SLOT_W, SLOT_H, fx, fy)
            zr = zoom_rect(vis, ax, ay, z)
            name = "%s__%s.jpg" % (stem, os.path.basename(rel).rsplit(".", 1)[0])
            mark(img, ax, ay, vis, zr, alt, os.path.join(ROOT, OUT, name))
            rows.append((stem, "push", os.path.basename(rel),
                         "fx=%g%% fy=%g%% z=%g" % (fx, fy, z),
                         "anchor=(%d,%d) of %dx%d" % (ax, ay, W, H), name))

        av = ANNVIEW_RE.search(html)
        if av:
            rel = av.group(1).replace("../", "")
            img = os.path.join(ROOT, rel)
            if os.path.exists(img):
                W, H = Image.open(img).size
                for k, style, note in ANNGROUP_RE.findall(html):
                    fx, fy = pct(var(style, "x")), pct(var(style, "y"))
                    z = float(var(style, "z", "1.6"))
                    ax, ay, vis = contain_map(W, H, ANN_W, ANN_H, fx, fy)
                    zr = zoom_rect(vis, ax, ay, z)
                    name = "%s__ann-%s.jpg" % (stem, k)
                    mark(img, ax, ay, vis, zr, note,
                         os.path.join(ROOT, OUT, name))
                    rows.append((stem, "ann:" + k, os.path.basename(rel),
                                 "x=%g%% y=%g%% z=%g" % (fx, fy, z),
                                 "anchor=(%d,%d) of %dx%d" % (ax, ay, W, H),
                                 name))

    w = max(len(r[0]) for r in rows)
    for r in rows:
        print("%-*s  %-14s %-42s %-26s %s" % (w, r[0], r[1], r[2], r[3], r[4]))
    print("\n%d figures -> %s/" % (len(rows), OUT))


main()
