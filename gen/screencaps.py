# -*- coding: utf-8 -*-
"""Cut the delivered walkthrough clips out of a real screen recording.

gen/walkthroughs.py exists because the first round of captures were not screen
recordings at all: they were GIFs holding one screenshot per second, and the only
honest thing to do with those was to cross-dissolve between the states. Where a
real recording exists, that machine is the wrong one -- there is actual motion in
the file, and dissolving it would be throwing away the thing that makes it worth
having.

So this is the other pipeline. It takes one continuous capture and cuts the clips
out of it, which is a different job from assembling a clip out of stills:

  - the cut points are chosen so the last frame matches the first. These loop
    forever in the corner of someone's eye, and a run that ends where it started
    loops without needing a dissolve to hide the seam;
  - the crop is chosen per clip against what is on screen in THAT clip, not once
    for the recording. The locations grid tolerates losing the top and bottom of
    the viewport; the villager card is nearly as tall as the viewport and does
    not, so it keeps more height and is letterboxed instead;
  - dead time at the front is trimmed. The interesting thing should happen about a
    second in, because the reader arrives mid-loop as often as not.

The source is a 1080p capture kept in assets/video/_rec, which is gitignored for
the same reason assets/video/_gif is: every frame of it survives into the mp4s
beside it, and committing both pays twice for one thing. Re-run this when a new
recording lands. Needs ffmpeg.
"""
import io
import json
import os
import subprocess
import sys

SRC = os.path.join("assets", "video", "_rec")
OUT = os.path.join("assets", "video")

WIDTH = 1280            # ~1.6x the widest slot on the site, which is 799 CSS px
CRF = 26                # flat pixel art; the ceiling here is the source, not this

# name, source, segments, crop (x, y, w, h) in the source's own pixels.
#
# `segments` is a list of (start, duration). More than one splices a single run,
# which the fishing clip needs and nothing else does: casting, the bite and the
# catch bar are at the front of that recording and the fish is landed thirty
# seconds later, and thirty seconds of a bar going up and down is not a figure. The
# splice is one run with the middle taken out, not two runs pretending to be one.
#
# The crops: the capture is 1920x1080 and the window it plays in is 799x365, which
# is 2.19. Cropping to that exactly is right for the locations clip -- the top of
# the viewport is page chrome and the bottom is a half-visible row of tiles -- and
# wrong for the gift clip, where the villager card runs from y=130 to y=1020 and
# any crop tight enough to fill the window would cut its own heading off. That one
# keeps 950 rows and letterboxes on the ivory the window is already painted with.
# A still can be cropped to the slot because the plate was cut for it; a recording
# cannot, because the crop would be hiding part of what happened.
# The four arcade clips share a crop, because the modal they play in is the same
# box in all four captures: x 415-1507, y 159-918. It is framed with the dimmed
# page still visible around it, at the window's own 2.19 aspect, so the figure
# fills its frame -- and cropping tight to the modal instead would not make the
# canvas any bigger, because the height is what the fit is limited by either way.
ARCADE = (74, 125, 1774, 810)

# The whole viewport, uncropped. For the two games whose board fills the height of
# the capture there is no 2.19 crop that keeps the board AND the control bar above
# it, and cropping either one away removes the subject; clips fit whole rather than
# filling the slot, so the dark ground either side of the board is what shows.
FULL = (0, 0, 1920, 1080)

# The home page's thumbnails are a different shape and a different job: 644x496,
# and they have to say what the project IS at a glance rather than show a run.
# Cropped to the width that makes 1080 tall a 1.3 frame, so the whole board and
# the whole maze survive and only the dark surround is lost.
TILE = (258, 0, 1404, 1080)
TILE_W = 644

CUTS = [
    dict(name="stardew-locations", src="stardew-run.mp4",
         segments=[(3.9, 5.3)], crop=(0, 0, 1920, 877)),
    dict(name="stardew-gift-lookup", src="stardew-run.mp4",
         segments=[(13.2, 10.8)], crop=(0, 95, 1920, 950)),
    # The four cabinets. walkthroughs.py builds these from one-frame-per-second
    # GIFs and its own docstring says what that is worth on a game: nothing to
    # smooth and no amount of dissolving makes four frames a run. These are real
    # recordings, so they come through here instead and that machine no longer
    # touches them.
    dict(name="stardew-junimo-kart", src="stardew-junimo-kart-run.mp4",
         segments=[(3.6, 15.6)], crop=ARCADE, crf=28),
    dict(name="stardew-fishing", src="stardew-fishing-run.mp4",
         segments=[(4.0, 6.0), (31.0, 6.2)], crop=ARCADE, crf=28),
    dict(name="stardew-prairie-king", src="stardew-prairie-king-run.mp4",
         segments=[(1.8, 15.6)], crop=ARCADE, crf=28),
    dict(name="stardew-junimo-jamboree", src="stardew-junimo-jamboree-run.mp4",
         segments=[(1.6, 12.6)], crop=ARCADE, crf=28),
    # The whole page in one scroll, sped up: the argument is that it IS one page,
    # and twenty-two seconds of real-time scrolling proves that to nobody.
    dict(name="stardew-full-scroll", src="stardew-scroll-run.mp4",
         segments=[(0.6, 22.4)], crop=(0, 101, 1920, 877), speed=1.55, crf=31),
    # Chess and Pac-Man. Both were built from one-frame-per-second GIFs too, and
    # both are games. The chess run is at 1.8x because the subject is the SPEED
    # control being turned up, and a relative speed-up keeps a ramp a ramp.
    dict(name="chess-autoplay", src="chess-autoplay-run.mp4",
         segments=[(0.4, 31.4)], crop=FULL, speed=1.8, crf=27),
    # Two home-page tiles. Chess and Pac-Man were the last two thumbnails on the
    # site that were a still of a game, and a still of a game is a picture of a
    # thing that is not doing the one thing it does.
    dict(name="chess-tile", src="chess-autoplay-run.mp4", tile=True,
         segments=[(8.0, 16.0)], crop=TILE, speed=2.0, crf=30),
    dict(name="pacman-tile", src="pacman-gameplay-run.mp4", tile=True,
         segments=[(6.0, 12.0)], crop=TILE, speed=1.5, crf=30),
    dict(name="pacman-gameplay", src="pacman-gameplay-run.mp4",
         segments=[(4.0, 20.0)], crop=FULL, speed=1.15, crf=27),
    # The UXfolio hero, the About panel opening over it, and the panel closing
    # again. Cut so both ends are the hero: the panel is the event, and a loop
    # that starts or stops inside it reads as a clip that failed to load.
    # Nothing is cropped tight here for the same reason the villager card is not.
    # The panel is two columns running nearly the full height of the capture, and
    # any crop at the window's 2.19 would take the top off one of them.
    dict(name="uxfolio-about-panel", src="uxfolio-about-run.mp4",
         segments=[(5.6, 10.9)], crop=(0, 30, 1888, 1010), crf=27),
    # The two persona homepage clips are recorded from the PUBLIC RECREATION in
    # projects/persona-homepage, not from the internal tool. The internal captures
    # carry a division, an application identifier and a colleague's name in six
    # places per frame, several of which pass under an open menu, and a figure
    # whose safety depends on a rectangle staying put is a figure waiting to leak.
    # Rebuilding the page with invented data removes the question instead of
    # managing it, and the recreation is close enough that the figure still shows
    # what the real one does.
    dict(name="persona-edit-options", src="persona-edit-options-run.webm",
         segments=[(4.4, 8.0)], crop=(0, 0, 1280, 680), crf=25),
    dict(name="persona-scope-switch", src="persona-scope-switch-run.webm",
         segments=[(3.9, 10.6)], crop=(0, 0, 1280, 680), crf=25),
    dict(name="persona-widget-scope", src="persona-widget-scope-run.webm",
         segments=[(4.2, 13.4)], crop=(0, 0, 1280, 680), crf=25),
    # 4.0 to 24.0 starts on "Starting in 1" and ends on the next one, so the run,
    # the collision and the restart are all inside a loop with no visible seam.
]


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
        pass
    sys.exit("  ffmpeg not found; pip install imageio-ffmpeg")


def main():
    if not os.path.isdir(SRC):
        print("  no %s; nothing to cut" % SRC)
        return
    ff = ffmpeg()
    try:
        index = json.load(io.open("video-index.json", encoding="utf-8"))
    except Exception:
        index = {}

    for c in CUTS:
        src = os.path.join(SRC, c["src"])
        if not os.path.isfile(src):
            print("  missing %s; skipped %s" % (src, c["name"]))
            continue
        x, y, w, h = c["crop"]
        segs = c["segments"]
        dur = sum(d for _, d in segs)
        wide = TILE_W if c.get("tile") else WIDTH
        dest = os.path.join("assets", "tile") if c.get("tile") else OUT
        out_h = int(round(h * wide / float(w) / 2)) * 2
        vf = ("crop=%d:%d:%d:%d,scale=%d:%d:flags=lanczos,format=yuv420p"
              % (w, h, x, y, wide, out_h))
        mp4 = os.path.join(dest, c["name"] + ".mp4")
        # trim inside the filter graph rather than -ss/-t on the input: the cuts
        # are to a tenth of a second, and an input seek lands on the nearest
        # keyframe instead.
        parts = "".join(
            "[0:v]trim=start=%.3f:duration=%.3f,setpts=PTS-STARTPTS[s%d];"
            % (st, d, i) for i, (st, d) in enumerate(segs))
        chain = "".join("[s%d]" % i for i in range(len(segs)))
        speed = c.get("speed", 1.0)
        pace = ",setpts=PTS/%.4f" % speed if speed != 1.0 else ""
        graph = ("%s%sconcat=n=%d:v=1:a=0%s,%s[v]"
                 % (parts, chain, len(segs), pace, vf))
        dur = dur / speed
        subprocess.check_call(
            [ff, "-v", "error", "-y", "-i", src,
             "-filter_complex", graph, "-map", "[v]", "-an",
             "-c:v", "libx264", "-crf", str(c.get("crf", CRF)),
             "-preset", "slow", "-movflags", "+faststart", mp4])
        # The poster is the clip's own opening frame, which is also the frame it
        # loops back to, so a clip that has not started and one mid-cycle are the
        # same picture rather than two different ones.
        jpg = os.path.join(dest, c["name"] + "-poster.jpg")
        subprocess.check_call(
            [ff, "-v", "error", "-y", "-i", src, "-ss", "%.3f" % segs[0][0],
             "-frames:v", "1", "-vf", vf, "-q:v", "3", jpg])
        kb = os.path.getsize(mp4) / 1024.0
        if not c.get("tile"):
            index[c["name"]] = dict(w=wide, h=out_h, kb=int(kb),
                                    seconds=round(dur, 1),
                                    source="screen recording", needs_motion=False)
        print("  %-26s %dx%-4d %5.1fs  %5dKB" % (c["name"] + ".mp4", wide,
                                                 out_h, dur, kb))

    with io.open("video-index.json", "w", encoding="utf-8") as fh:
        fh.write(json.dumps(index, indent=1, sort_keys=True) + "\n")
    print("%d clips cut from the recording" % len(CUTS))


if __name__ == "__main__":
    main()
