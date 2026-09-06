# -*- coding: utf-8 -*-
"""Cut the hero artwork off its paper and prepare it for the page.

The drawing arrives on a cream ground. The background-removal pass it was run
through set that ground to 50 percent alpha rather than removing it, which is worse
than leaving it alone: composited over the page's parchment it lands at (252,248,231)
against (253,251,239), so instead of a clean cutout there is a faint warm rectangle
with a hard edge, which is exactly the thing a cutout is for.

So the ground is keyed out here instead, and the key is a FLOOD FILL from the border
rather than a colour threshold. A threshold would work on the paper and then punch
holes through the laptop screen, the white chest fur and the pale sparkles, all of
which are close to the paper's colour and none of which are background. Filling
inward from the edge only removes ground that is actually connected to the outside.

The edge is then feathered. These are crayon strokes with soft, broken edges, and a
one-pixel binary alpha against them reads as a sticker.

Upscaled to 2x the slot on the way out. The source is 568x439 for a box that renders
at 530x410, so it is barely above 1x and will be soft on any modern screen. Lanczos
adds no detail and this is pastel texture rather than type, so it survives better
than most things would, but a 2x export from the original file would be better and
this is the one asset on the home page where that is worth doing.
"""
import io
import os
from collections import deque

from PIL import Image, ImageFilter

SRC = os.path.join("assets", "hero", "_src", "cats-hero.png")
OUT = os.path.join("assets", "hero", "cats-hero.webp")

# 2x the .mascot-wrap box in index.html, which is 530x410.
TARGET_W = 1060

# How far a pixel may sit from the sampled ground colour and still be ground. Wide
# enough for the paper's grain and its vignette, short of the sparkles.
TOL = 30

FEATHER = 1.1


def key_out(im):
    """Alpha from a border flood fill, feathered."""
    im = im.convert("RGBA")
    w, h = im.size
    rgb = im.convert("RGB")
    px = rgb.load()
    ground = px[1, 1]

    def near(p):
        return (abs(p[0] - ground[0]) <= TOL and abs(p[1] - ground[1]) <= TOL
                and abs(p[2] - ground[2]) <= TOL)

    seen = bytearray(w * h)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if near(px[x, y]):
                seen[y * w + x] = 1
                q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if not seen[y * w + x] and near(px[x, y]):
                seen[y * w + x] = 1
                q.append((x, y))
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx]:
                if near(px[nx, ny]):
                    seen[ny * w + nx] = 1
                    q.append((nx, ny))

    mask = Image.frombytes("L", (w, h),
                           bytes(0 if s else 255 for s in seen))
    mask = mask.filter(ImageFilter.GaussianBlur(FEATHER))
    im.putalpha(mask)
    return im, sum(seen) * 100.0 / (w * h)


def main():
    if not os.path.exists(SRC):
        print("  MISSING %s" % SRC)
        return
    im = Image.open(SRC)
    im, cut = key_out(im)
    w, h = im.size
    im = im.resize((TARGET_W, int(round(h * TARGET_W / float(w)))), Image.LANCZOS)
    im.save(OUT, "WEBP", quality=90, method=6, exact=True)
    print("  cats-hero.webp  %dx%d  %d%% keyed out  %dKB"
          % (im.size[0], im.size[1], round(cut), os.path.getsize(OUT) / 1024))


if __name__ == "__main__":
    main()
