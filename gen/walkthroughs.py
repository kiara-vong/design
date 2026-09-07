# -*- coding: utf-8 -*-
"""Turn the captured state sequences into smooth, looping walkthrough video.

WHAT THE SOURCES ACTUALLY ARE, because it decides everything below.

They arrived as GIFs and they are not screen recordings. Each one holds between 3
and 48 frames spread over 5 to 40 seconds, which is about one frame per second, and
measuring the change between consecutive frames gives 95 to 100 percent of the
picture every time. Nothing is moving. They are sequences of discrete screenshots
with the intermediate motion missing, and a recorder that captures a still roughly
once a second is what produces that.

So "make them smooth" cannot mean re-encoding. There is no motion in the file to
recover, and interpolating between two unrelated screens invents a frame that never
existed and looks like it. What makes this material smooth is the transition: a hard
cut between two frames that differ everywhere reads as a glitch, and the same two
frames with a cross-dissolve between them read as one thing becoming another.

That is also what the sources are actually good for. A flow through an interface IS
a sequence of states, and the state-to-state dissolve is the honest way to show one.
It is the `deal` machine from CAPTURE.md Part 4 done in the encoder instead of in
CSS, which is the right place for it once a clip runs past three or four states:
twenty layered <img> elements cross-fading on a timer is a lot of page weight to
spend on something a 200KB video does better.

WHAT THIS DOES NOT FIX. Five of these are games and animations, where the motion is
the subject: the arcade cabinets, and the island solver resolving. At one frame per
second there is nothing to smooth, and no amount of dissolving makes four frames a
game. Those are marked NEEDS_MOTION below and want a real screen recorder rather
than a GIF tool. They are still built, because a dissolved sequence is better than
nothing on the page while that is arranged, but the document should say what they
are.

TIMING. Source delays run from 300ms to 3500ms, which is the recorder's pacing
rather than a decision, so they are re-timed here: every state gets the same hold
inside a clamp, and the dissolve is a fixed 320ms with a smoothstep on the alpha
rather than a linear ramp, because a linear cross-fade has a visible flat middle
where both frames are half-present and neither is readable.

Each clip also dissolves from its last state back to its first, so it loops without
a cut. That is worth more than it sounds on a page where the thing plays forever in
the corner of someone's eye.

SOURCES ARE NOT COMMITTED. assets/video/_gif/ is gitignored: the GIFs are 45MB and
every frame in them survives into the mp4, so committing both is paying twice for
one thing. This follows video.py, which reads its phone captures from outside the
repo too. Re-run this when new captures land.
"""
import io
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageChops, ImageSequence

SRC = os.path.join("assets", "video", "_gif")
OUT = os.path.join("assets", "video")

FPS = 30
WIDTH = 1280            # ~1.6x the widest slot on the site, which is 799 CSS px
FADE_MS = 320
HOLD_MS = 900           # every state, regardless of what the recorder chose
HOLD_FIRST_MS = 1500    # the opening state gets longer: it is the establishing shot

# Built from real screen recordings by gen/screencaps.py instead, and skipped here
# so a re-run cannot quietly replace 60fps of an actual run with a dissolve between
# four screenshots of one. Everything below about what this material is worth is
# still true of the material that is still here.
RECORDED = {
    "stardew-junimo-kart", "stardew-fishing", "stardew-prairie-king",
    "stardew-junimo-jamboree", "stardew-gift-lookup",
}

# The clips whose subject is motion. A one-frame-per-second capture cannot show it.
NEEDS_MOTION = {
    "stardew-junimo-kart", "stardew-prairie-king", "stardew-junimo-jamboree",
    "stardew-fishing", "island-generator-building",
    "chess-autoplay", "pacman-gameplay",
}

# Per-clip overrides, only where the default pacing is wrong for the content.
TUNING = {
    # 45 states of a solver filling a grid. Short holds so it reads as progress
    # rather than as a slideshow, and a long dissolve so consecutive grids melt into
    # each other, which is the closest this material gets to the real thing.
    "island-generator-building": dict(hold=240, fade=340, hold_first=900),
    # Clips with a lot of states run long at the default 900ms. The brief asks for 8
    # to 12 seconds, and a walkthrough nobody watches to the end proves nothing.
    "dashboard-hierarchy-drill": dict(hold=560),
    "dashboard-filters-persist": dict(hold=660),
    "uxfolio-loader-transition": dict(hold=430),
    "stardew-fishing": dict(hold=680),
    "dorms-quiz": dict(hold=700),
    # Three and four states respectively. Nothing to be done about that here, but
    # holding each one longer at least lets it be read as a still.
    "stardew-junimo-jamboree": dict(hold=1600),
    "stardew-junimo-kart": dict(hold=1500),
    "stardew-prairie-king": dict(hold=1300),
    # Five states of a board eating itself: an autoplay game going from an
    # opening position to chaos. Closer to island-generator-building's "read as
    # progress" problem than to the arcade titles' "only 3-4 states" one, so it
    # gets the same treatment -- a hold short enough that consecutive boards
    # read as one thing unravelling rather than a slideshow, and a fade longer
    # than the default so the melt between positions is legible as a melt.
    "chess-autoplay": dict(hold=520, fade=420, hold_first=1000),
    # Six states telling a small story -- countdown, chase, near-miss, death,
    # restart -- rather than one continuous action. A single hold can't favour
    # the death/restart beats over the chase without per-state timing, which
    # is more machinery than one clip justifies; splitting the difference
    # toward the arcade titles' longer holds (six sparse states, not thirty)
    # keeps every beat, including those two, readable.
    "pacman-gameplay": dict(hold=1050, fade=360),
}


def ffmpeg():
    for c in ("ffmpeg", "ffmpeg.exe"):
        try:
            subprocess.check_output([c, "-version"], stderr=subprocess.STDOUT)
            return c
        except Exception:
            pass
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("no ffmpeg: pip install imageio-ffmpeg")


def states(path):
    """Unique frames from a GIF, at delivery width.

    Coalesced by PIL's iterator, deduplicated because several of these hold the same
    picture across two GIF frames to make a longer pause, and that pause is being
    replaced by the retiming below.
    """
    im = Image.open(path)
    out, prev = [], None
    for fr in ImageSequence.Iterator(im):
        cur = fr.convert("RGB")
        if prev is not None and ImageChops.difference(cur, prev).getbbox() is None:
            continue
        prev = cur
        w, h = cur.size
        # Even height, because yuv420p cannot encode an odd one.
        nh = int(round(WIDTH * h / float(w)))
        out.append(cur.resize((WIDTH, nh - (nh % 2)), Image.LANCZOS))
    return out


def smoothstep(t):
    return t * t * (3.0 - 2.0 * t)


def timeline(frames, hold, hold_first, fade):
    """Yield finished frames at FPS: hold, dissolve, hold, ... and back to the start.

    Dissolving the last state back into the first is what makes the loop invisible.
    Without it the clip snaps from its end state to its opening one, which is the
    single most noticeable thing about a short looping video.
    """
    n = len(frames)
    hold_f = max(1, int(round(hold * FPS / 1000.0)))
    first_f = max(1, int(round(hold_first * FPS / 1000.0)))
    fade_f = max(1, int(round(fade * FPS / 1000.0)))
    for i, img in enumerate(frames):
        for _ in range(first_f if i == 0 else hold_f):
            yield img
        nxt = frames[(i + 1) % n]
        for k in range(1, fade_f + 1):
            yield Image.blend(img, nxt, smoothstep(k / float(fade_f + 1)))


def encode(ff, name, frames, size):
    mp4 = os.path.join(OUT, name + ".mp4")
    cmd = [ff, "-y",
           "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", "%dx%d" % size, "-r", str(FPS), "-i", "-",
           "-an",
           "-c:v", "libx264", "-profile:v", "high", "-preset", "slow",
           # Low CRF is cheap here: most frames are identical to the one before, so
           # the encoder spends almost nothing on them, and the dissolves are the
           # only place quality is visible.
           "-crf", "21", "-pix_fmt", "yuv420p",
           "-g", str(FPS * 2), "-movflags", "+faststart",
           mp4]
    log = tempfile.TemporaryFile()
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=log, stderr=log)
    n = 0
    try:
        for f in frames:
            p.stdin.write(f.tobytes())
            n += 1
        p.stdin.close()
    except IOError:
        pass
    if p.wait() != 0:
        log.seek(0)
        sys.stderr.write(log.read().decode("utf-8", "replace")[-3000:])
        raise SystemExit("ffmpeg failed on " + name)
    log.close()
    return mp4, n


def main():
    ff = ffmpeg()
    if not os.path.isdir(SRC):
        print("  no %s; nothing to build" % SRC)
        return
    index = {}
    names = sorted(f[:-4] for f in os.listdir(SRC)
                   if f.endswith(".gif") and f[:-4] not in RECORDED)
    for name in names:
        t = TUNING.get(name, {})
        frames = states(os.path.join(SRC, name + ".gif"))
        if not frames:
            print("  SKIP %s (no frames)" % name)
            continue
        size = frames[0].size
        seq = list(timeline(frames, t.get("hold", HOLD_MS),
                            t.get("hold_first", HOLD_FIRST_MS),
                            t.get("fade", FADE_MS)))
        mp4, n = encode(ff, name, seq, size)
        # Poster is the opening state, which is also the frame the clip returns to,
        # so a paused video and a playing one agree with each other.
        poster = os.path.join(OUT, name + "-poster.jpg")
        frames[0].save(poster, "JPEG", quality=82, optimize=True, progressive=True)
        index[name] = dict(states=len(frames), seconds=round(n / float(FPS), 1),
                           w=size[0], h=size[1],
                           kb=int(os.path.getsize(mp4) / 1024),
                           needs_motion=name in NEEDS_MOTION)
        print("  %-34s %2d states  %5.1fs  %4dKB%s"
              % (name, len(frames), n / float(FPS),
                 os.path.getsize(mp4) / 1024,
                 "   NEEDS A REAL RECORDING" if name in NEEDS_MOTION else ""))
    with io.open("video-index.json", "w", encoding="utf-8") as fh:
        fh.write(json.dumps(index, indent=1, sort_keys=True) + "\n")
    print("%d walkthroughs" % len(index))


if __name__ == "__main__":
    main()
