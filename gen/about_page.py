# -*- coding: utf-8 -*-
"""The About page, rebuilt to the reference design rather than on the case-study shell.

The first attempt reused the long-form case-study layout, which was a mistake: the
reference About is its own thing and the thing it does is the point. Two columns
on a warm gradient ground, a résumé down the left, and on the right a paragraph of
interests whose links each swing a polaroid into the well beside them. Hovering
the prose is what fills the picture frame.

That interaction is worth reproducing exactly because it solves a real problem
every About page has: a list of hobbies is boring to read and the photographs that
would make it interesting have nowhere to go. Tying them together makes the
paragraph worth hovering and gives eight images one frame to share.

The polaroids are the owner's own artwork (see gen-polaroids.py), which is the
part that could not be borrowed and the part that makes the page hers.
"""
import io
import os

# The canvas has to clear six entries in flow rather than the reference's six at a
# fixed 157px rhythm. Measured from the rendered page; re-measure after adding one.
#
# And after changing the TYPE, which is what caught it last time: bumping the body
# sizes a step pushed the lowest element 130px past a canvas that is overflow:hidden,
# and the whole resume link at the foot of the page simply stopped being drawn. No
# error, no scrollbar, just a missing block. 1546 is the lowest element's bottom plus
# the 44px of ground the design keeps under the last entry.
#
# To re-measure: load the page, then in the console take the largest
# getBoundingClientRect().bottom of everything inside .ab-canvas and add 44.
CANVAS = 1546

FOOT = "../assets/about"

# ---------------------------------------------------------------- content
INTRO = ("I&rsquo;m Kiara. <b>/kee-ar-uh/</b><br>Welcome to the corner of the internet "
         "I actually maintain.<br><br>I&rsquo;m an engineer who kept ending up in the "
         "design conversation and eventually stopped treating that as an accident. I "
         "like the layer underneath the product: the design system, the internal "
         "platform, the tool everyone reaches for without thinking about it. I write "
         "the code and I draw the thing, which usually makes me the one asking whether "
         "the component should exist at all.")

# (role, org, description, when), newest first. Taken from her own resume rather
# than reconstructed: the dates in the first pass were wrong in three places.
JOBS = [
    ("Software Engineer", "Capital One",
     "Built and shipped a React and TypeScript resource-inventory platform from "
     "scratch, owning research, design and rollout. Shipped the compliance event "
     "timeline and the GraphQL endpoint behind it, and led a 12,600-line design "
     "system overhaul unifying more than a dozen pages.",
     "2024 &ndash;"),
    ("Software Engineer Intern", "Capital One",
     "Stood up an EC2-based cloud-native deployment, and built a Spark pipeline on "
     "AWS Lambda that spins up ephemeral EMR clusters to aggregate into S3.",
     "2023"),
    ("UI/UX Intern", "Colgate-Palmolive",
     "Led full-stack development of internal apps for the compensation, learning "
     "and people-acquisition teams, replacing manual workflows. Built a dashboard "
     "builder for executives and HR partners on top of hardware telemetry.",
     "2022"),
    ("Software Engineer Intern", "BlackLine",
     "Built a C# API integration between the finance-automation and compliance "
     "systems so every active control could be seen in one place. Owned features "
     "end to end: design, build, test and rollout.",
     "2022"),
    ("B.Sc. Computer Science", "Brown University",
     "Computer science, 4.0.",
     "2020 &ndash; 2024"),
    ("Study Abroad", "Yonsei University",
     "A semester in Seoul.",
     "2023"),
]

# (key, label). The key ties a link to its polaroid in the well.
MOON = [
    ("painting", "bad painter"),
    ("food", "food enthusiast"),
    ("amc", "AMC A-Lister"),
    ("kpop", "reformed K-Pop superfan"),
    ("smiski", "collector of smiskis"),
    ("cats", "full-time cat person"),
]

# Kiara's own sentence, in her order. Six of the eleven carry a photograph and are
# the underlined ones; the other five are just true. Every key here must exist in
# MOON and every MOON key must have a plate in gen/polaroids.py, or the link points
# at a picture that was never cut.
MOON_TEXT = ("I also moonlight as: a {painting}, a {food}, a NYT games semi-solver, "
             "a Stardew capitalist, an {amc}, a {kpop}, a {smiski}, a worldbuilder, "
             "a retired yearbook editor, a Catan loser, and a {cats}.")

# Each polaroid gets its own tilt and sway so the well does not swap one rectangle
# for an identically-angled rectangle.
TILTS = [(-2.4, 7.5, -1.2), (1.8, 8.6, -3.4), (-1.3, 9.4, -0.5), (2.6, 7.9, -5.1),
         (-1.9, 8.2, -2.3), (1.2, 9.1, -6.0), (-2.1, 8.8, -4.2), (2.2, 7.6, -0.9)]

# The pill comes from nav.py so every page lists the same six entries and each
# has its own icon. Hardcoding it here is how the About page ended up with a
# different set from the index in the first place.
from gen import nav as _nv
NAV_ICONS = _nv.pill('about', '      ', '../')


def jobs_html():
    o = []
    for i, (role, org, desc, when) in enumerate(JOBS):
        o.append('''        <div class="ab-job" style="--i:%d">
          <div class="ab-job-main">
            <p class="ab-role">%s <span class="at">at</span> %s</p>
            <p class="ab-desc">%s</p>
          </div>
          <p class="ab-when">%s</p>
        </div>
''' % (i, role, org, desc, when))
    return "".join(o)


def moon_html():
    links = {k: '<a href="#" data-art="%s">%s</a>' % (k, label) for k, label in MOON}
    return MOON_TEXT.format(**links)


def art_html():
    o = []
    for i, (key, _) in enumerate(MOON):
        tilt, sway, delay = TILTS[i % len(TILTS)]
        o.append('''        <div class="ab-art" data-art="%s"
             style="--tilt:%sdeg;--sway:%ss;--sway-delay:%ss">
          <img src="%s/pol-%s.jpg" alt="A polaroid of my own work: %s"
               style="left:67.5px;top:-12px;width:427px;height:638.4px">
        </div>
''' % (key, tilt, sway, delay, FOOT, key, key))
    return "".join(o)


PAGE = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>About · Kiara Vong</title>
<meta name="description" content="Kiara Vong, an engineer who kept ending up in the design conversation.">
<link rel="icon" href="../assets/ui/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="../assets/ui/favicon.svg">
<meta name="theme-color" content="#649F25">
<!-- Critical, before the stylesheet: the ground here is a warm gradient, so a cold
     load would otherwise flash parchment before the image lands. This is the
     image's own mid tone. -->
<style>html{background:#7A5633}</style>
<link rel="stylesheet" href="../site.css">
<script src="../site-motion.js"></script>
<!-- The ground IS the page. Left to the parser it queues behind the fonts and
     arrives last, so the page shows flat brown and then changes colour under the
     reader. The two faces carrying the title and the body get the same treatment,
     so the type stops reflowing a second after it appears. -->
<link rel="preload" as="image" href="../assets/hero/about-bg.webp" fetchpriority="high">
<link rel="preload" as="font" type="font/woff2" href="../assets/fonts/giverny-italic.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="../assets/fonts/clover-400.woff2" crossorigin>
<!-- Same trick as every other page here: the scale is written as a stylesheet
     before anything paints, so the 1440-wide canvas never renders unscaled first. -->
<script>
(function(){
  var W = 1440, H = __CANVAS__ + 405;   // canvas + footer
  var s = Math.min(window.innerWidth / W, 1);
  var hs = Math.min(window.innerWidth / W, window.innerHeight / 861, 1);   /* the index's */
  var el = document.createElement('style');
  el.id = 'ab-initial-layout';
  el.textContent = window.innerWidth <= 760 ? '' :
    '#ab-stage{transform:scale(' + s + ');left:' +
      Math.max(0, (window.innerWidth - W * s) / 2) + 'px}' +
    '#ab-navwrap{transform:scale(' + hs + ');left:' +
      Math.max(0, (window.innerWidth - W * hs) / 2) + 'px}' +
    'body{height:' + (H * s) + 'px}';
  document.head.appendChild(el);
})();
</script>
<link rel="stylesheet" href="../about.css">
<!-- about.css hard-codes the reference canvas height, which was sized for six
     roles. This build has three; without the override the bottom third of the
     page is empty ground and the footer sits a long way below the last line. -->
<style>
/* about.css positions the left column by hand: the rule at a fixed 266px and each
   role at 308 + index * 157. Both were measured against the reference intro and
   its six entries, so with different copy the rule landed INSIDE the paragraph and
   the roles sat on top of it. The column is normal flow here, which puts the rule
   between the intro and the history whatever either of them is, and lets the
   number of roles change without a second number needing to change with it. */
.ab-left{display:flex;flex-direction:column}
.ab-rule{position:static;margin:34px 0 30px;width:100%%}
.ab-job{position:static;top:auto;margin-bottom:30px}
.ab-job:last-of-type{margin-bottom:0}
.ab-canvas{height:__CANVAS__px}

/* The résumé download, as a ticket stub rather than a button. The site's whole
   visual language is perforated card stock, and "take one" is a thing a stub
   already says, so it reads as part of the page instead of a control dropped on
   top of it. */
.ab-stub{position:relative;align-self:flex-start;display:inline-flex;align-items:center;
  gap:16px;margin-top:38px;padding:16px 24px 16px 22px;background:var(--parchment);
  color:var(--dusty-granite);text-decoration:none;border-radius:6px;
  box-shadow:0 10px 24px rgba(30,24,18,.28);
  transition:transform .3s cubic-bezier(.34,1.4,.5,1),box-shadow .3s ease}
/* The perforation, as a repeating notch down the left edge rather than an image,
   so the stub can be any height its label needs. */
.ab-stub::before{content:"";position:absolute;left:0;top:0;bottom:0;width:9px;
  background:radial-gradient(circle at 0 6px,transparent 0 4.5px,var(--parchment) 5px);
  background-size:9px 12px;background-repeat:repeat-y}
.ab-stub:hover{transform:translateY(-3px) rotate(-.8deg);
  box-shadow:0 16px 30px rgba(30,24,18,.34)}
.ab-stub-no{font-family:'Thistle',ui-monospace,monospace;font-weight:500;
  font-size:11px;letter-spacing:.10em;color:var(--accent);
  writing-mode:vertical-rl;transform:rotate(180deg);padding-left:6px}
.ab-stub-main{display:flex;flex-direction:column;gap:4px}
.ab-stub .t{font-family:'Laurel',Georgia,serif;font-weight:500;font-size:17px;
  line-height:1.2}
.ab-stub .s{font-family:'Thistle',ui-monospace,monospace;font-size:11px;
  color:var(--antique-gold)}
.ab-stub-arrow{margin-left:8px;color:var(--accent);
  transition:transform .3s cubic-bezier(.34,1.4,.5,1)}
.ab-stub:hover .ab-stub-arrow{transform:translateY(3px)}
@media (prefers-reduced-motion:reduce){
  .ab-stub,.ab-stub-arrow{transition:none}
  .ab-stub:hover{transform:none}
}
</style>
<link rel="stylesheet" href="../mobile.css">
</head>
<body>

<div id="ab-navwrap" aria-hidden="false">
  <nav class="nav" aria-label="Primary">
%s
  </nav>
</div>

<div id="ab-stage">
 <div class="ab-canvas">
  <img id="ab-bg" src="../assets/hero/about-bg.webp" alt="" fetchpriority="high" decoding="async">
  <div id="ab-wash" aria-hidden="true"></div>
  <a class="ab-back" href="../" aria-label="Back to the index">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5"/><path d="M12 19l-7-7 7-7"/></svg>
  </a>

  <div class="ab-page">
    <h1 class="ab-hello">Hello world!</h1>
    <p class="ab-aside">hover to bring<br>to life</p>

    <div class="ab-cols">
      <div class="ab-left">
        <p class="ab-intro">%s</p>
        <div class="ab-rule"></div>
%s        <a class="ab-stub" href="../assets/doc/Kiara-Vong-Resume.pdf" download>
          <span class="ab-stub-no">ADMIT ONE</span>
          <span class="ab-stub-main">
            <span class="t">Take the full r&eacute;sum&eacute;</span>
            <span class="s">PDF &middot; one page &middot; updated 2026</span>
          </span>
          <svg class="ab-stub-arrow" width="20" height="20" viewBox="0 0 24 24" fill="none"
               stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 4v12"/><path d="M6 14l6 6 6-6"/>
          </svg>
        </a>
      </div>

      <div class="ab-right">
        <!-- Mobile only. On the desktop canvas the two columns sit side by side so
             nothing divides them; stacked, the moonlighting list would run straight
             on from the last role with no break at all. -->
        <div class="ab-rule ab-rule-moon"></div>
        <p class="ab-moon">%s</p>

        <div class="ab-well">
          <svg class="ab-dash" viewBox="0 0 591 497" preserveAspectRatio="none" aria-hidden="true">
            <rect x="0.5" y="0.5" width="590" height="496" rx="23.5" ry="23.5"></rect>
          </svg>
          <div class="ab-rest">
            <img src="../assets/ui/about-rest.svg" alt="" aria-hidden="true">
            <p class="ab-hint">hover over a <span>link</span></p>
          </div>
%s        </div>
      </div>
    </div>
  </div>
 </div>

 <div id="site-footer" data-variant="about" data-flowers="foot-about.png"></div>
</div>

<script src="../site-footer.js"></script>
<script src="../site-nav.js"></script>
<script>
/* Swap the well's contents on hover. Pointer events rather than :hover so the art
   also responds to keyboard focus, and so leaving a link restores the resting
   state even if the pointer never crosses the well itself. */
(function(){
  var well = document.querySelector('.ab-well');
  if(!well) return;
  var arts = {};
  well.querySelectorAll('.ab-art').forEach(function(a){ arts[a.getAttribute('data-art')] = a; });
  var current = null;

  function show(key){
    if(current === key) return;
    if(current && arts[current]) arts[current].classList.remove('is-on');
    current = key;
    if(key && arts[key]){ arts[key].classList.add('is-on'); well.classList.add('is-showing'); }
    else { well.classList.remove('is-showing'); }
  }

  /* On a touch device "hover" means press-and-hold, so pointerenter/leave makes a
     tap flash the art and immediately drop it. There, a tap toggles instead, and a
     tap anywhere else clears the well. */
  var touch = window.matchMedia &&
    (matchMedia('(hover: none)').matches || matchMedia('(pointer: coarse)').matches);
  document.querySelectorAll('.ab-moon a').forEach(function(link){
    var key = link.getAttribute('data-art');
    if(touch){
      link.addEventListener('click', function(e){
        e.preventDefault();
        if(key) show(current === key ? null : key);
      });
    } else {
      link.addEventListener('pointerenter', function(){ if(key) show(key); });
      link.addEventListener('focus',        function(){ if(key) show(key); });
      link.addEventListener('pointerleave', function(){ if(key) show(null); });
      link.addEventListener('blur',         function(){ if(key) show(null); });
      link.addEventListener('click', function(e){ e.preventDefault(); });
    }
  });
  if(touch){
    document.addEventListener('click', function(e){
      if(!e.target.closest('.ab-moon a')) show(null);
    });
    var hint = document.querySelector('.ab-hint');
    if(hint) hint.innerHTML = hint.innerHTML.replace(/\\bhover over\\b/gi,'tap').replace(/\\bhover\\b/gi,'tap');
    var aside = document.querySelector('.ab-aside');
    if(aside) aside.innerHTML = aside.innerHTML.replace(/\\bhover\\b/gi,'tap');
  }
})();

/* Keep the 1440 canvas fitted on resize; the head script does the first paint. */
(function(){
  var W = 1440, H = __CANVAS__ + 405, stage = document.getElementById('ab-stage');
  var navwrap = document.getElementById('ab-navwrap');
  function fit(){
    /* Below 760 the page is stacked by mobile.css, not scaled, so give back every
       inline style this has written rather than leaving a stale transform behind. */
    if (window.innerWidth <= 760) {
      stage.style.transform = ''; stage.style.left = '';
      if (navwrap) { navwrap.style.transform = ''; navwrap.style.left = ''; }
      document.body.style.height = '';
      var init = document.getElementById('ab-initial-layout');
      if (init) init.textContent = '';
      return;
    }
    var s = Math.min(window.innerWidth / W, 1);
    stage.style.transform = 'scale(' + s + ')';
    stage.style.left = Math.max(0, (window.innerWidth - W * s) / 2) + 'px';
    document.body.style.height = (H * s) + 'px';
    /* The pill follows the INDEX's scale, not this page's, so the two sit on the
       same pixel between pages. The index's hero fits height as well as width;
       this canvas does not, and inside it the pill would drift on any window
       shorter than 861. */
    if (navwrap) {
      var hs = Math.min(window.innerWidth / W, window.innerHeight / 861, 1);
      navwrap.style.transform = 'scale(' + hs + ')';
      navwrap.style.left = Math.max(0, (window.innerWidth - W * hs) / 2) + 'px';
    }
  }
  window.addEventListener('resize', fit, { passive: true });
  fit();
})();
</script>
<script src="../mobile.js"></script>
</body>
</html>
'''

os.path.isdir("about") or os.makedirs("about")
io.open(os.path.join("about", "index.html"), "w", encoding="utf-8").write(
    PAGE.replace('__CANVAS__', str(CANVAS))
    % (NAV_ICONS, INTRO, jobs_html(), moon_html(), art_html()))
print("wrote about/index.html (%d roles, %d polaroids)" % (len(JOBS), len(MOON)))
