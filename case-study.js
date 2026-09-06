/* Behaviour shared by every case study page: fitting the 1440-authored canvas to
   the viewport, and the impact callout's count-up. Page-specific animations stay
   with their page. Lifted out of payments-home.html when the second study arrived.
*/

/* Scale the 1440-authored page to fit the viewport width, centre it, size the body,
   and lay the full-width accent bleed behind the (centred) footer. */
(function(){
  var STAGE_W = 1440;
  var stage = document.getElementById('cs-stage');
  var footer = document.getElementById('footer');
  var bgFooter = document.getElementById('bg-footer');
  if(!stage) return;
  function fit(){
    var vw = window.innerWidth;
    /* Stacked by mobile.css below this width, so every inline style written here
       has to come back off — including the rail's, which is positioned by hand. */
    if (vw <= 760) {
      stage.style.transform = ''; stage.style.left = '';
      document.body.style.height = '';
      ['.cs-nav', '.cs-back'].forEach(function(sel){
        var el = document.querySelector(sel);
        if(!el) return;
        el.style.left = ''; el.style.top = ''; el.style.transform = '';
      });
      if(bgFooter){ bgFooter.style.top = ''; bgFooter.style.height = ''; }
      return;
    }
    var ds = Math.min(vw / STAGE_W, 1);
    stage.style.transform = 'scale(' + ds + ')';
    var stageLeft = Math.max(0, (vw - STAGE_W * ds) / 2);
    stage.style.left = stageLeft + 'px';
    /* The section rail lives outside the stage so it can be position:fixed, so it has
       to be given the stage's scale and offset by hand to stay welded to the layout. */
    [['.cs-nav', 180], ['.cs-back', 31]].forEach(function (pair) {
      var el = document.querySelector(pair[0]);
      if (!el) return;
      el.style.left = (stageLeft + 33 * ds) + 'px';
      el.style.top = (pair[1] * ds) + 'px';
      el.style.transform = 'scale(' + ds + ')';
    });
    document.body.style.height = (stage.offsetHeight * ds) + 'px';
    if(footer && bgFooter){
      var el = footer, acc = 0;
      while(el && el !== stage){ acc += el.offsetTop; el = el.offsetParent; }
      bgFooter.style.top = (acc * ds) + 'px';
      bgFooter.style.height = (footer.offsetHeight * ds) + 'px';
    }
  }
  fit();
  window.addEventListener('resize', fit);
  window.addEventListener('load', fit);
  if(document.fonts && document.fonts.ready){ document.fonts.ready.then(fit); }
})();

/* Impact callout: play once when it reaches the reader — the stats rise in
   sequence and the numbers count up. Deliberately not looping; a metric that
   keeps re-animating reads as decoration rather than a result. */
(function(){
  var card=document.querySelector('.stats'); if(!card) return;
  var nums=[].slice.call(card.querySelectorAll('.stat-n'));
  var reduce=window.matchMedia && matchMedia('(prefers-reduced-motion:reduce)').matches;
  /* data-to carries its own precision ("4.8" counts to one decimal, "7" to none),
     and data-prefix defaults to "+" so a lift reads as one — set it to "" for a
     figure that is a share rather than a change. */
  function fmt(n, v){
    var raw = n.getAttribute('data-to') || '0';
    var dp = (raw.split('.')[1] || '').length;
    var pre = n.getAttribute('data-prefix');
    return (pre === null ? '+' : pre) + v.toFixed(dp) + (n.getAttribute('data-suffix') || '%');
  }
  function settle(){ nums.forEach(function(n){ n.textContent = fmt(n, parseFloat(n.getAttribute('data-to'))); }); }
  function play(){
    card.classList.add('is-in');
    if(reduce){ settle(); return; }
    var t0=null, DUR=1100;
    function step(ts){
      if(t0===null) t0=ts;
      var p=Math.min(1,(ts-t0)/DUR), e=1-Math.pow(1-p,3);   // ease-out
      nums.forEach(function(n){
        n.textContent = fmt(n, e * parseFloat(n.getAttribute('data-to')));
      });
      if(p<1) requestAnimationFrame(step); else settle();
    }
    requestAnimationFrame(step);
  }
  if(!('IntersectionObserver' in window)){ play(); return; }
  // Trigger when the card is genuinely in the reading area, not the instant its
  // top edge clears the fold — otherwise the count-up finishes before you reach it.
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){ if(e.isIntersecting){ play(); io.disconnect(); } });
  },{threshold:.55, rootMargin:'0px 0px -18% 0px'});
  io.observe(card);
})();


/* ---------------------------------------------------------------------------
   The section rail: which item is current, and standing down over the footer.

   This lived inline in payments-home.html and so never reached the second study,
   which had the same markup and the same stylesheet but none of the behaviour --
   no current item, no smooth scroll, and a rail that rode over the footer. It is
   shared code now, and every case study gets it from having a .cs-nav. */
/* Section menu: mark the section currently in view, and stand down over the footer.
   One item is current at a time -- the last section whose top has passed the reading
   line, which is steadier than "whichever is most visible" when sections differ
   wildly in height, as they do here (694px to 2828px). */
(function () {
  var nav = document.querySelector('.cs-nav');
  if (!nav) return;
  var links = [].slice.call(nav.querySelectorAll('a[href^="#"]'));
  if (!links.length) return;

  var targets = links.map(function (a) {
    return { link: a, el: document.getElementById(a.getAttribute('href').slice(1)) };
  }).filter(function (t) { return t.el; });
  if (!targets.length) return;

  var footer = document.getElementById('bg-footer');
  var reduce = window.matchMedia &&
               window.matchMedia('(prefers-reduced-motion:reduce)').matches;
  var ticking = false;

  /* Clicking a section scrolls to it with a little air above, so the heading is not
     jammed against the top edge. Overview goes to the very top of the document
     instead of to its own box, which sits below the hero and clipped it. */
  links.forEach(function (a, i) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href').slice(1);
      var el = document.getElementById(id);
      if (!el) return;
      e.preventDefault();
      var y = i === 0 ? 0
            : (window.pageYOffset || 0) + el.getBoundingClientRect().top - 40;
      window.scrollTo({ top: Math.max(0, y), behavior: reduce ? 'auto' : 'smooth' });
      if (history.replaceState) history.replaceState(null, '', '#' + id);
    });
  });

  function update() {
    ticking = false;
    var line = window.innerHeight * 0.35;      // the reading line
    var current = targets[0];
    targets.forEach(function (t) {
      if (t.el.getBoundingClientRect().top <= line) current = t;
    });
    targets.forEach(function (t) {
      t.link.classList.toggle('is-current', t === current);
    });
    /* Keep the parent lit while you are inside any of its subsections, so the rail
       still tells you which top-level section you are in. The parent is the nearest
       preceding item that is not itself a sub -- it used to be hardcoded to
       #key-decisions, which was true of both studies but only by coincidence. */
    var inSub = current && current.link.classList.contains('sub');
    var parent = null;
    if (inSub) {
      for (var i = links.indexOf(current.link) - 1; i >= 0; i--) {
        if (!links[i].classList.contains('sub')) { parent = links[i]; break; }
      }
    }
    links.forEach(function (a) { a.classList.toggle('is-parent', a === parent); });
    /* Stand aside only when the footer genuinely reaches the element. Keying off
       "footer is visible at all" hid them while they were still over parchment --
       on a 900px viewport the footer's 405px never climbs as high as the rail. */
    if (footer) {
      var f = footer.getBoundingClientRect();
      [nav, document.querySelector('.cs-back')].forEach(function (el) {
        if (!el) return;
        var r = el.getBoundingClientRect();
        el.classList.toggle('is-away', f.top < r.bottom + 24);
      });
    }
  }
  function onScroll() {
    if (!ticking) { ticking = true; requestAnimationFrame(update); }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
  update();
})();


/* ---------------------------------------------------------------------------
   Figures reveal as they come into view.

   One observer for the page. Each element fires once and is then unobserved, so
   nothing re-animates on the way back up -- a figure that replays every time it
   scrolls past reads as a glitch rather than an entrance.

   Nothing here is required for the page to be readable: the resting states are all
   written against .pt, which site-motion.js only adds when motion is allowed, so a
   reduced-motion visitor sees every figure already in place. The one thing script
   must do regardless is measure the series path, because its own length is what the
   draw animates from and CSS cannot ask an SVG how long it is. */
(function () {
  var els = [].slice.call(document.querySelectorAll('[data-reveal]'));
  if (!els.length) return;

  /* Hand the path its own length as a custom property. Done for everyone, including
     reduced motion, so the offset never falls back to the placeholder. */
  var line = document.querySelector('.pr-series .line');
  if (line && line.getTotalLength) {
    var len = Math.ceil(line.getTotalLength());
    line.style.strokeDasharray = len;
    line.style.setProperty('--len', len);
  }

  if (!('IntersectionObserver' in window)) {
    els.forEach(function (el) { el.classList.add('is-in'); });
    return;
  }
  /* Fires a little before the figure is centred, so the animation is already under
     way by the time it is the thing you are looking at. */
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      en.target.classList.add('is-in');
      io.unobserve(en.target);
    });
  }, { threshold: .2, rootMargin: '0px 0px -12% 0px' });
  els.forEach(function (el) { io.observe(el); });
})();

/* The dashboard's ring and prompt are an invitation to hover. Once that has happened
   the invitation is spent, so it is marked used and stays down from then on. */
(function () {
  var fig = document.querySelector('.cpd');
  if (!fig) return;
  var hit = fig.querySelector('.cpd-hit');
  if (!hit) return;
  function used() { fig.classList.add('hint-done'); }
  hit.addEventListener('pointerenter', used, { once: true });
  hit.addEventListener('focus', used, { once: true });
})();

/* Before/after ledger: same once-only reveal as the Impact callout, and for the
   same reason -- a block that replays every time it scrolls past reads as
   decoration rather than as something being said. */
(function(){
  var el = document.querySelector('.cs-ba'); if(!el) return;
  function play(){ el.classList.add('is-in'); }
  if(!('IntersectionObserver' in window)){ play(); return; }
  var io = new IntersectionObserver(function(es){
    es.forEach(function(e){ if(e.isIntersecting){ play(); io.disconnect(); } });
  }, {threshold:.25, rootMargin:'0px 0px -10% 0px'});
  io.observe(el);
})();

/* Annotated stills: point at a label, the picture pushes in on what it names.
   ---------------------------------------------------------------------------
   The zoom target lives on the LABEL, as --x/--y/--z, and the transform runs on the
   image. A custom property set on one element cannot be read by a sibling -- they
   inherit down, never sideways -- so the values are copied up to the container here,
   which is the whole reason this needs script at all.

   pointerenter/leave rather than :hover, and focus/blur alongside it, so tabbing
   through the labels drives exactly the same thing a mouse does. .used stops the
   first label's idle nudge for good once anyone has actually used it. */
(function () {
  var plates = [].slice.call(document.querySelectorAll('.ann'));
  if (!plates.length) return;

  plates.forEach(function (plate) {
    var groups = [].slice.call(plate.querySelectorAll('.ann-group'));

    function on(g) {
      plate.classList.add('used');
      groups.forEach(function (o) { o.classList.toggle('on', o === g); });
      plate.setAttribute('data-hover', g.getAttribute('data-k') || 'on');
      plate.style.setProperty('--fx', g.style.getPropertyValue('--x') || '50%');
      plate.style.setProperty('--fy', g.style.getPropertyValue('--y') || '50%');
      plate.style.setProperty('--z', g.style.getPropertyValue('--z') || '1.6');
    }

    function off() {
      groups.forEach(function (o) { o.classList.remove('on'); });
      plate.removeAttribute('data-hover');
    }

    groups.forEach(function (g) {
      var note = g.querySelector('.ann-note');
      if (!note) return;
      /* The note is the hit target, not the group: the group's box spans the full
         label column including the description that is not shown yet, so hovering
         anywhere in that empty space would fire it. */
      note.setAttribute('tabindex', '0');
      note.addEventListener('pointerenter', function () { on(g); });
      note.addEventListener('focus', function () { on(g); });
      note.addEventListener('blur', off);
    });
    plate.addEventListener('pointerleave', off);
  });
})();
