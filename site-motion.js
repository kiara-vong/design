/* Page-level motion, shared across the site.

   1. Landing on a case study: the title reveals word by word, each word fading
      up out of a blur, after the kicker and before the intro.
   2. Leaving for another page in the site: the current page fades out first,
      so navigation feels continuous rather than a cut.

   Loaded from <head> without defer so the html class lands before first paint;
   anything needing the DOM waits for DOMContentLoaded. If this script never
   runs, every page still renders and every link still works. */
(function () {
  var root = document.documentElement;
  /* Unconditional, and before anything can return early: it lets CSS hide things that
     script will reveal, from the very first paint. Without it a page-bottom script
     arms too late and the content flashes in first. */
  root.classList.add('js');
  var reduce = window.matchMedia &&
               window.matchMedia('(prefers-reduced-motion:reduce)').matches;
  if (reduce) return;                       // no class, so none of the motion CSS applies
  root.classList.add('pt');

  function onReady(fn) {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
    else fn();
  }

  /* ---------- 1. case-study title reveal ----------
     Split to characters, not words. The reference this is modelled on staggers whole
     words, but its headline is eight words long, so the stagger reads as a wave. This
     title is two words; per-word gives two discrete pops instead of a reveal. Words
     still get a wrapper so they never break mid-word, and the space between them keeps
     a beat so the rhythm stays even.

     The spans are hidden from assistive tech and the full string is restored as an
     aria-label, so the title is not announced one letter at a time. */
  onReady(function () {
    var title = document.querySelector('.cs-title');
    if (!title) return;
    var text = title.textContent.trim();
    if (!text) return;
    var words = text.split(/\s+/);
    title.textContent = '';
    title.setAttribute('aria-label', text);
    var i = 0;
    words.forEach(function (word, wi) {
      var w = document.createElement('span');
      w.className = 'w';
      w.setAttribute('aria-hidden', 'true');
      word.split('').forEach(function (ch) {
        var c = document.createElement('span');
        c.className = 'c';
        c.textContent = ch;
        c.style.setProperty('--d', (0.12 + i * 0.035).toFixed(3) + 's');
        w.appendChild(c);
        i++;
      });
      title.appendChild(w);
      if (wi < words.length - 1) {
        title.appendChild(document.createTextNode(' '));
        i++;
      }
    });
  });

  /* ---------- 2. case-study hero: reveal the two devices together ----------
     Lives here, in the file that sets .js, on purpose: the mask
     (.js .cs-hero .hero-float{opacity:0}) is applied from the <head>, so whatever removes
     it must ship in the same file. A page-bottom script would leave the hero blank
     whenever it loaded slowly.

     It also must NOT wait on DOMContentLoaded. That event is blocked by the blocking
     script at the end of <body>, so waiting for it reintroduces the exact dependency
     this is avoiding. Instead we look for the element every frame while the document
     is still parsing, which finds it moments after it is written out. */
  (function findHero() {
    var hero = document.querySelector('.cs-hero');
    if (!hero) {
      if (document.readyState === 'loading') requestAnimationFrame(findHero);
      return;                                   // parsed, no hero: not a case study
    }
    /* The hero element can be parsed before its own children, and this used to give up
       for good the first time it found an empty one -- so on any page or connection where
       that race went the wrong way the entrance never fired, .hero-float stayed at the
       opacity 0 that .js sets, and the phones were invisible. Keep looking while the
       document is still parsing; only conclude there are none once it has finished. */
    /* Any image inside the float, not .hero-ph specifically. The payments studies hang
       phones here and Copilot hangs landscape application windows, and this only ever
       needed "the hero's images" -- keyed to the phone class it silently refused to
       reveal the Copilot hero at all, leaving it blank at the opacity .js sets. */
    var phones = hero.querySelectorAll('.hero-float img');
    if (!phones.length) {
      if (document.readyState === 'loading') requestAnimationFrame(findHero);
      return;
    }

    /* last resort: show the resting composition rather than animate it */
    var bail = setTimeout(function () {
      if (!hero.classList.contains('in')) hero.classList.add('shown');
    }, 10000);
    function go() { clearTimeout(bail); hero.classList.add('in'); }

    var decoded = Promise.all([].map.call(phones, function (img) {
      return new Promise(function (resolve) {
        if (img.complete && img.naturalWidth) {
          if (img.decode) img.decode().then(resolve, resolve); else resolve();
          return;
        }
        img.addEventListener('load', function () { resolve(); }, { once: true });
        img.addEventListener('error', function () { resolve(); }, { once: true });
      });
    }));

    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { io.disconnect(); decoded.then(go); }
        });
      }, { threshold: 0.25 });
      io.observe(hero);
    } else {
      decoded.then(go);
    }

    /* Scroll parallax on the stage: the pair drifts slower than the page as the hero
       leaves. It moves BOTH phones, so it can never open a gap at their overlap. Read
       and write are both inside one rAF, and only when the hero is on screen. */
    var stage = hero.querySelector('.hero-stage');
    if (!stage) return;
    /* Anchored at scrollY 0 so the pair sits exactly on the Figma geometry when the
       page opens; it only lags once you start scrolling. Mapping off the hero's
       distance from the viewport centre instead put it 8px out at rest. */
    var MAX = 14, RATE = 0.06, ticking = false;
    function apply() {
      ticking = false;
      var r = hero.getBoundingClientRect();
      if (r.bottom < 0 || r.top > window.innerHeight) return;
      var y = window.pageYOffset || document.documentElement.scrollTop || 0;
      var d = y * RATE;
      if (d > MAX) d = MAX;
      stage.style.transform = 'translate3d(0,' + d.toFixed(2) + 'px,0)';
    }
    function onScroll() {
      if (!ticking) { ticking = true; requestAnimationFrame(apply); }
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll, { passive: true });
    apply();
  })();

  /* ---------- 3. home hero entrance ----------
     The hero image is 1.29MB, so even with a placeholder behind it the page can sit
     dark-but-empty for a moment. Fading the three clusters in once it has decoded lets
     the page assemble instead of snapping. Opacity only: their transform is owned by
     fit(). */
  (function heroEntrance() {
    var groups = document.querySelectorAll('.hgroup');
    if (!groups.length) {
      if (document.readyState === 'loading') requestAnimationFrame(heroEntrance);
      return;
    }
    function go() { root.classList.add('hero-in'); }
    var img = document.getElementById('hero-bg');
    if (!img) { go(); return; }
    if (img.complete && img.naturalWidth) {
      (img.decode ? img.decode().then(go, go) : go());
    } else {
      img.addEventListener('load', go, { once: true });
      img.addEventListener('error', go, { once: true });
    }
    setTimeout(go, 2500);          // never leave the hero blank
  })();


  /* ---------- 3. fade out before navigating within the site ----------
     Only where the browser cannot do it itself. With cross-document view transitions
     available the browser owns the whole handoff, and intercepting the click would
     just layer a second, worse animation on top of it. */
  var nativeVT = window.CSS && CSS.supports && CSS.supports('view-transition-name', 'none');
  onReady(function () {
    if (nativeVT) return;
    document.addEventListener('click', function (e) {
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey ||
          e.shiftKey || e.altKey) return;
      var a = e.target.closest && e.target.closest('a');
      if (!a) return;
      var href = a.getAttribute('href');
      if (!href || a.target === '_blank' || a.hasAttribute('download')) return;
      if (href.charAt(0) === '#' || /^(mailto:|tel:)/.test(href)) return;
      var url = new URL(a.href, location.href);
      if (url.origin !== location.origin) return;          // external links leave immediately
      if (url.pathname === location.pathname) return;      // same page, let it be
      e.preventDefault();
      root.classList.add('pt-leaving');
      var went = false;
      function go() { if (!went) { went = true; location.href = a.href; } }
      /* Navigate only once the fade-out has actually ENDED, so every departure hands
         over at exactly the opacity pt-in starts from. Firing earlier makes the
         handoff depend on how fast the document arrives, which is what produced the
         occasional jump. animationend rather than a timer, so the two can never drift
         apart if the duration is edited; the timer is only a fallback for a
         backgrounded tab where animations do not run. */
      document.body.addEventListener('animationend', function h(ae) {
        if (ae.animationName === 'pt-out') {
          document.body.removeEventListener('animationend', h);
          go();
        }
      });
      setTimeout(go, 400);
    });
  });

  /* Warm the next document on hover. The fade-out is now a fixed 130ms of latency, so
     buy it back by having the HTML usually already cached by the time the click
     lands. Cheap, once per href, and harmless if the link is never followed. */
  onReady(function () {
    var done = {};
    document.addEventListener('pointerover', function (e) {
      var a = e.target.closest && e.target.closest('a');
      if (!a) return;
      var href = a.getAttribute('href');
      if (!href || href.charAt(0) === '#' || /^(mailto:|tel:)/.test(href)) return;
      if (a.target === '_blank' || a.hasAttribute('download')) return;
      var url;
      try { url = new URL(a.href, location.href); } catch (err) { return; }
      if (url.origin !== location.origin) return;
      if (url.pathname === location.pathname) return;
      if (done[url.href]) return;
      done[url.href] = true;
      var l = document.createElement('link');
      l.rel = 'prefetch';
      l.href = url.href;
      document.head.appendChild(l);
    }, { passive: true });
  });

  /* Restore visibility when returning via the back button (bfcache replays the
     page in whatever state it was left, including mid-fade). */
  window.addEventListener('pageshow', function () {
    root.classList.remove('pt-leaving');
  });
})();

/* Nav pill scale ---------------------------------------------------------------
   The pill is authored at 1440-canvas size, and on the home and About pages it
   rides inside a group that gets transform:scale(hs), so it shrinks with the
   viewport along with the rest of the hero. The Art, project and case-study pages
   are ordinary flowing documents, so the same pill rendered there at 1:1 and came
   out visibly bigger -- about 20% at 1280x720 -- which made the one element that
   is on every page the one element that changed size between them.

   So publish that same factor as --nav-k and let those pages scale the pill by it.
   The formula is copied from index.html's C.measure() deliberately: any other
   number would agree at some viewports and disagree at others, which is worse than
   being consistently wrong.

   Outside the motion IIFE above, which returns early under prefers-reduced-motion.
   This is layout, not motion, and a reduced-motion visitor should not get a
   differently sized menu. Set on documentElement, which exists while <head> is
   still parsing, so it lands before first paint and the pill never resizes on load.

   Below the mobile breakpoint mobile.css owns the pill and pins it at full size,
   so the factor goes back to 1 rather than shrinking a pill that is already
   sized for a phone. */
(function () {
  var W = 1440, HH = 861, MOBILE = 760;

  /* The pill's own unscaled width, measured once. It is the same markup on every
     page, so one measurement serves all of them; it is read rather than hardcoded
     because the label changes per page and so does the width. */
  var natural = 0;
  function measure() {
    var nav = document.querySelector('.nav');
    if (!nav) return 0;
    var prev = document.documentElement.style.getPropertyValue('--nav-k');
    document.documentElement.style.setProperty('--nav-k', '1');
    var w = nav.getBoundingClientRect().width;
    document.documentElement.style.setProperty('--nav-k', prev);
    return w;
  }

  function set() {
    var vw = window.innerWidth, vh = window.innerHeight, k;
    if (vw > MOBILE) {
      k = Math.min(vw / W, vh / HH, 1);
    } else {
      /* Below the breakpoint the pill is a fixed bar and the only thing that matters
         is that it fits. It was a flat .84, which is 362px of bar: fine on a 390px
         phone and clipped at both ends on a 320px one. Fit to the viewport with a
         gutter, and never grow past .84. */
      if (!natural) natural = measure();
      k = natural ? Math.min(0.84, (vw - 28) / natural) : 0.84;
    }
    document.documentElement.style.setProperty('--nav-k', k.toFixed(4));
  }
  set();
  /* Re-run once the pill exists, since the first call happens from <head>. */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { natural = 0; set(); });
  }
  window.addEventListener('resize', function () { natural = 0; set(); }, { passive: true });
  window.addEventListener('orientationchange', set);
})();

/* Celebration pop -------------------------------------------------------------
   A short fanfare for the two "Copied!" toasts, in the footer and in the glass menu.

   Same vocabulary as the sparks trailing the Coming soon toast on the home page:
   filled persimmon circles, 1.1 to 2.4px, a brief hold and then a long fade on the
   identical alpha curve. The only difference is that these travel outward from the
   point that was clicked instead of being dropped along a path, which is what makes
   one read as a wake and the other as a pop.

   Draws into a throwaway fixed canvas over the target and removes it when the last
   dot dies, so nothing lingers between clicks and nothing joins the layout. Silent
   under prefers-reduced-motion, where the toast is feedback enough.

   Rings the toast rather than radiating from a single point: the reach is taken from
   the toast's own box and is elliptical, so the dots clear a wide pill by the same
   margin at the sides as above and below. A circular reach around an 85x34 pill would
   have cleared it comfortably top and bottom and barely at all left and right.

   Colour is the caller's, and each toast passes its own SURFACE colour rather than a
   contrast colour. That makes dots landing on the toast invisible and dots beyond its
   edge visible, so the burst reads as coming from behind the label. Persimmon, which
   the trail sparks use, would have been invisible against the footer's red ground.

   Takes an element, or a plain {cx, cy, w, h} for a toast that has no element to
   measure -- the glass menu's is a ::after pseudo-element. */
(function () {
  var MARGIN = 20;                    /* how far past the toast's edge dots travel */
  var PAD = 14;                       /* room for a dot's own radius at full reach */

  window.sitePop = function (target, opts) {
    if (!target) return;
    if (window.matchMedia &&
        window.matchMedia('(prefers-reduced-motion:reduce)').matches) return;
    var b = target.getBoundingClientRect ? target.getBoundingClientRect() : null;
    var cx = b ? b.left + b.width / 2 : target.cx;
    var cy = b ? b.top + b.height / 2 : target.cy;
    var tw = b ? b.width : target.w, th = b ? b.height : target.h;
    if (!(tw > 0) && !(th > 0)) return;
    var rgb = (opts && opts.rgb) || '86,144,174';        /* --accent by default */

    var reachX = tw / 2 + MARGIN, reachY = th / 2 + MARGIN;
    var boxW = (reachX + PAD) * 2, boxH = (reachY + PAD) * 2;
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var cv = document.createElement('canvas');
    cv.width = Math.round(boxW * dpr);
    cv.height = Math.round(boxH * dpr);
    cv.setAttribute('aria-hidden', 'true');
    /* Above the glass menu, which is the highest thing a burst can be centred on. */
    cv.style.cssText = 'position:fixed;pointer-events:none;z-index:1200;' +
      'left:' + (cx - boxW / 2) + 'px;top:' + (cy - boxH / 2) + 'px;' +
      'width:' + boxW + 'px;height:' + boxH + 'px';
    var ctx = cv.getContext && cv.getContext('2d');
    if (!ctx) return;
    document.body.appendChild(cv);
    ctx.scale(dpr, dpr);

    /* Angles are spread evenly then jittered: an even ring reads as mechanical, a
       purely random one clumps and leaves bald patches. Reach and size vary per dot
       so the ring has a ragged edge rather than a rim. */
    var mx = boxW / 2, my = boxH / 2;
    var dots = [], N = 18, t0 = performance.now(), last = 0;
    for (var i = 0; i < N; i++) {
      dots.push({
        a: (i / N) * 6.2832 + (Math.random() - 0.5) * 0.40,
        d: 0.72 + Math.random() * 0.28,          /* fraction of the reach, per dot */
        r: 1.7 + Math.random() * 1.7,
        o: 0.68 + Math.random() * 0.29,
        dur: 460 + Math.random() * 300
      });
      if (dots[i].dur > last) last = dots[i].dur;
    }

    /* requestAnimationFrame stops in a backgrounded tab, and a canvas pinned at
       z-index 1200 must not outlive its burst -- click, switch tabs, come back, and it
       would still be sitting over the page. The timeout is the guarantee that it goes;
       rAF is only the fast path. Measured without it: six quick clicks left six
       canvases behind, none of which ever cleaned themselves up. */
    function drop() {
      clearTimeout(kill);
      if (cv.parentNode) cv.parentNode.removeChild(cv);
    }
    var kill = setTimeout(drop, last + 250);

    (function frame(now) {
      if (!cv.parentNode) return;                  /* the timeout got there first */
      ctx.clearRect(0, 0, boxW, boxH);
      var alive = 0;
      for (var k = 0; k < dots.length; k++) {
        var s = dots[k], u = (now - t0) / s.dur;
        if (u >= 1) continue;
        alive++;
        /* Out fast, then decelerating, so the pop has a leading edge. */
        var e = 1 - Math.pow(1 - u, 3);
        /* The trail sparks' alpha curve, unchanged: brief hold, long fade. */
        var a = u < 0.15 ? u / 0.15 : 1 - (u - 0.15) / 0.85;
        /* Radius rises with the alpha hold so each dot pops into being rather than
           arriving already full size, then holds. Cheaper to read than a scale-out. */
        var g = u < 0.15 ? 0.45 + 0.55 * (u / 0.15) : 1;
        ctx.fillStyle = 'rgba(' + rgb + ',' + (a * s.o).toFixed(3) + ')';
        ctx.beginPath();
        ctx.arc(mx + Math.cos(s.a) * reachX * s.d * e,
                my + Math.sin(s.a) * reachY * s.d * e,
                s.r * g, 0, 6.2832);
        ctx.fill();
      }
      if (alive) requestAnimationFrame(frame);
      else drop();
    })(t0);
  };
})();

/* Mini projects: develop into place -------------------------------------------
   One observer, one shot per card, then unobserve. See the .mini entrance block in
   site.css for why these get a scroll-driven arrival rather than the case studies'
   pointer-driven lift.

   The CSS holds the cards at opacity 0, so this file owes them a way to become visible
   in every case: no IntersectionObserver means show them all immediately. Failing open
   matters more than the animation does -- the cards must never be the thing that is
   missing because a browser was old. */
(function () {
  function ready(fn) {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
    else fn();
  }
  ready(function () {
    var cards = [].slice.call(document.querySelectorAll('.reads .mini'));
    if (!cards.length) return;
    function show(el) { el.classList.add('is-in'); }
    if (!('IntersectionObserver' in window)) { cards.forEach(show); return; }
    /* Pulling the bottom edge up 15% is what makes the entrance visible at all. On a
       plain threshold it fired as soon as a sliver of the card cleared the bottom of the
       window, so the whole 0.7s played in the corner of the eye and the card was already
       settled by the time it was somewhere you were looking. Triggering off a line 15%
       up from the bottom puts the motion in front of the reader instead. */
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        show(e.target);
        io.unobserve(e.target);
      });
    }, { threshold: 0, rootMargin: '0px 0px -15% 0px' });
    cards.forEach(function (c) { io.observe(c); });
  });
})();

/* Autoplaying tiles, stopped for anyone who asked for less motion.
   ---------------------------------------------------------------------------
   CSS can turn off an animation and cannot turn off a video, so the one thumbnail
   that is a recording has to be paused here. Pausing at currentTime 0 leaves the
   first frame showing, which for this clip is an empty grid -- so it seeks to the
   end instead, where the picture is a finished island and stands on its own. */
(function () {
  if (!(window.matchMedia &&
        window.matchMedia('(prefers-reduced-motion:reduce)').matches)) return;
  [].slice.call(document.querySelectorAll('.tile-view video')).forEach(function (v) {
    v.removeAttribute('autoplay');
    v.loop = false;
    function still() {
      v.pause();
      if (v.duration && isFinite(v.duration)) v.currentTime = v.duration - 0.05;
    }
    still();
    v.addEventListener('loadedmetadata', still);
  });
})();
