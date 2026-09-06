# -*- coding: utf-8 -*-
"""What each figure actually looks like in its slot.

The audit scripts beside this one answer narrow questions -- where does the zoom
land, is there browser chrome in the file. This one answers the blunt one: if you
opened the page and looked at this figure, what would you see?

Every machine gets its resting frame, because that is the frame the reader spends
most of the loop looking at and the only one reduced motion ever shows:

  push    the whole plate, cover-cropped to the slot
  strip   the top of the plate, which is where the scroll starts and returns
  deal    the first layer, which never fades and is the sequence's own still
  wipe    the seam parked mid-frame, both halves showing
  clip    the poster, which is the clip's first frame and its loop point
  ann     the whole plate contained, which is the state before anyone hovers

Rendered at the slot's real 799x391 so the output is the composition, not the
asset. A plate can be a perfectly good screenshot and still be a bad figure.
"""
import os
import re
import sys

from PIL import Image, ImageDraw

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
OUT = sys.argv[2] if len(sys.argv) > 2 else "slot-audit"
SLOT_W, SLOT_H = 799, 391
ANN_W = SLOT_W - 196

FIG = re.compile(
    r'<div class="cs-media cam ([a-z\- ]+)"([^>]*)>(.*?)</div>\s*'
    r'<figcaption class="cs-caption">(.*?)</figcaption>', re.S)
SRC = re.compile(r'(?:src|poster)="([^"]+\.(?:webp|jpg|png))"')


def cover(im, w, h):
    ia, sa = im.size[0] / float(im.size[1]), w / float(h)
    if ia > sa:
        nw, nh = int(round(h * ia)), h
    else:
        nw, nh = w, int(round(w / ia))
    im = im.resize((nw, nh), Image.LANCZOS)
    return im.crop(((nw - w) // 2, (nh - h) // 2,
                    (nw - w) // 2 + w, (nh - h) // 2 + h))


def contain(im, w, h, bg=(246, 242, 230)):
    im = im.copy()
    im.thumbnail((w, h), Image.LANCZOS)
    out = Image.new("RGB", (w, h), bg)
    out.paste(im, ((w - im.size[0]) // 2, (h - im.size[1]) // 2))
    return out


def top(im, w, h):
    """A strip rests at its top edge, drawn at the slot's width."""
    nh = int(round(im.size[1] * w / float(im.size[0])))
    return im.resize((w, nh), Image.LANCZOS).crop((0, 0, w, min(h, nh)))


def main():
    os.makedirs(os.path.join(ROOT, OUT), exist_ok=True)
    pages = []
    for d in ("projects", "work"):
        p = os.path.join(ROOT, d)
        if os.path.isdir(p):
            pages += [os.path.join(p, f) for f in sorted(os.listdir(p))
                      if f.endswith(".html")]

    for page in pages:
        html = open(page, encoding="utf-8").read()
        stem = os.path.splitext(os.path.basename(page))[0]
        figs = FIG.findall(html)
        if not figs:
            continue
        cards = []
        for kind, attrs, inner, cap in figs:
            kind = kind.strip()
            srcs = SRC.findall(inner)
            if not srcs:
                continue
            rel = srcs[0].replace("../", "")
            path = os.path.join(ROOT, rel)
            if not os.path.exists(path):
                continue
            im = Image.open(path).convert("RGB")
            if "ann" in kind:
                frame = Image.new("RGB", (SLOT_W, SLOT_H), (246, 242, 230))
                frame.paste(contain(im, ANN_W, SLOT_H), (0, 0))
                ImageDraw.Draw(frame).line(
                    [(ANN_W, 0), (ANN_W, SLOT_H)], fill=(216, 210, 194), width=2)
            elif "cam-strip" in kind:
                frame = top(im, SLOT_W, SLOT_H)
            else:
                frame = cover(im, SLOT_W, SLOT_H)
            cards.append((kind, os.path.basename(rel), cap.strip(), frame))

        pad, gap, head = 16, 14, 46
        sheet = Image.new(
            "RGB", (SLOT_W + pad * 2,
                    head + (SLOT_H + head + gap) * len(cards) + pad),
            (252, 251, 239))
        d = ImageDraw.Draw(sheet)
        d.text((pad, 14), "%s  --  %d figures, resting frames"
               % (stem, len(cards)), fill=(20, 20, 20))
        y = head
        for kind, name, cap, frame in cards:
            d.text((pad, y - 24), "%s   %s" % (kind, name), fill=(90, 86, 81))
            sheet.paste(frame, (pad, y))
            d.rectangle([pad, y, pad + SLOT_W, y + SLOT_H],
                        outline=(216, 210, 194), width=1)
            d.text((pad, y + SLOT_H + 5), cap[:150], fill=(60, 56, 51))
            y += SLOT_H + head + gap
        out = os.path.join(ROOT, OUT, "%s.jpg" % stem)
        sheet.save(out, quality=88)
        print("%-22s %2d figures -> %s" % (stem, len(cards), out))


main()
