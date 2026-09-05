# Deploying to GitHub Pages on kiaravong.com

## Once

    git init
    git add .
    git commit -m "Portfolio"
    gh repo create kiaravong.com --public --source=. --push

Settings > Pages > Source: **Deploy from a branch**, branch `main`, folder `/ (root)`.

`CNAME` and `.nojekyll` are already in the repo. CNAME is what binds the custom
domain; .nojekyll stops GitHub running Jekyll over the site, which would otherwise
skip every path beginning with an underscore.

## DNS at the registrar

Four A records on the apex, all host `@`:

    185.199.108.153
    185.199.109.153
    185.199.110.153
    185.199.111.153

And one CNAME so the www form works too:

    www  ->  <your-github-username>.github.io

Then tick **Enforce HTTPS** in Settings > Pages once the certificate is issued,
which usually takes under an hour.

## Every time after

    python build.py          # regenerate and verify
    git add -A && git commit -m "..." && git push

The build must pass its own check before you push. It exits non-zero on a broken
link, so a failed build is a reason to stop.

## What this repo is carrying

  ~182 MB total, of which 135 MB is assets/video

GitHub Pages allows 100 MB per file and publishes sites up to 1 GB, so this fits.
The number to watch is the 100 GB/month bandwidth soft limit: sandsketch.mp4 is
62 MB, so roughly 1,600 full plays of that one file would reach it. Every player on
the site is preload="none" behind a poster, so nothing downloads until someone
presses play. If it ever becomes a problem, trim the two long films rather than
moving hosts.

## Before the domain points here

`assets/fonts/` holds 11 commercial font files being served from the origin:
PP Kyoto, ABC Diatype, Apercu Mono, P22 Mackinac, Monument Grotesk. That is invisible
on localhost and very visible on a public site under your own name. Buy the webfont
licences or delete the folder; every rule in site.css already names an open fallback,
so deleting degrades the typography and breaks nothing.
