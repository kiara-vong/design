# -*- coding: utf-8 -*-
"""Transcode the source .mov files into web-deliverable MP4.

The sources are phone captures: 665MB of HEVC for SandSketch alone, and two of the
four are 10-bit HLG. Neither the codec nor the transfer curve is safe to serve --
HEVC in <video> is Safari-only in practice, and an HLG file handed to a browser as
if it were bt709 comes out grey and flat, because the browser applies no inverse
curve at all.

So: tonemap HLG to bt709 properly through a linear light stage, rather than the
usual shortcut of forcing pixel format and hoping. Hable rather than reinhard,
which holds the highlights -- these are lit scenes where the blown highlight IS the
subject in half the shots.

720p because the widest a video is ever drawn on this site is about 760 CSS px, and
a portfolio that costs someone 400MB to browse is a portfolio nobody browses. The
pages pair every one of these with preload="none" and a poster frame, so a visitor
who does not press play downloads none of it.

Posters are existing stills from assets/art/, not new grabs: those frames were
already chosen and captioned, and a poster that matches the still above it reads as
the same piece of work rather than a second one.

Needs ffmpeg. pip install imageio-ffmpeg supplies one if the system has none.
"""
import os
import subprocess
import sys
import tempfile

SRC = os.path.join("..", "website", "art")
OUT = os.path.join("assets", "video")

# (source, output stem, is the source HLG/bt2020)
JOBS = [
    (os.path.join(SRC, "sandsketch", "SANDSKETCH.mov"), "sandsketch", True),
    (os.path.join(SRC, "iphone movie making", u"A Goose’s Life P2.mov"), "fm-goose", True),
    (os.path.join(SRC, "iphone movie making", "Grocery Shopping.mov"), "fm-grocery", False),
    (os.path.join(SRC, "iphone movie making", "Torah.mov"), "fm-torah", False),
]

# Scale first, tonemap second: tonemapping is the expensive per-pixel stage and there
# is no reason to run it on 4K pixels that are about to be thrown away.
FIT = "scale=-2:720:flags=lanczos"
HLG = (FIT + ",zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,"
       "tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
SDR = FIT + ",format=yuv420p"


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


def main():
    ff = ffmpeg()
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    for src, stem, hlg in JOBS:
        if not os.path.exists(src):
            print("  MISSING %s" % src)
            continue
        dst = os.path.join(OUT, stem + ".mp4")
        cmd = [ff, "-y", "-i", src,
               "-vf", HLG if hlg else SDR,
               "-c:v", "libx264", "-profile:v", "high", "-preset", "medium",
               "-crf", "26",
               # A cap as well as a quality target. CRF alone lets a busy shot spike
               # to a bitrate that stalls on a normal connection, and every one of
               # these has motion in every frame.
               "-maxrate", "2600k", "-bufsize", "5200k",
               "-g", "60",
               "-c:a", "aac", "-b:a", "128k", "-ac", "2",
               # Metadata at the FRONT, so playback can start before the file has
               # finished arriving. Without it a browser fetches the whole thing to
               # find the index, which for a 7-minute file is the entire download.
               "-movflags", "+faststart",
               dst]
        print("  %s ..." % stem)
        # stderr to a FILE, never to a pipe. ffmpeg writes a progress line per
        # second, and check_call does not drain what it opens -- so with
        # stderr=PIPE the 64KB pipe buffer fills after a minute or two and ffmpeg
        # blocks on write forever. It looks exactly like a slow encode: the process
        # is alive, the output file is 0 bytes, and its CPU time stops climbing.
        log = tempfile.TemporaryFile()
        try:
            subprocess.check_call(cmd, stdout=log, stderr=log)
        except subprocess.CalledProcessError:
            log.seek(0)
            sys.stderr.write(log.read().decode("utf-8", "replace")[-4000:])
            raise
        finally:
            log.close()
        print("     %s  %.1f MB" % (dst, os.path.getsize(dst) / 1048576.0))


if __name__ == "__main__":
    main()
