/* The glass menu's behaviour, shared by every page that carries one.

   Only the copy-email icon needs script. The rest of the pill is links and CSS, and
   each page supplies its own markup because which entry sits in the labelled slot
   changes with the page. Load this after the nav. */
(function(){
  // Copy-email nav icon. The tooltip says "Copy email", so it copies rather than
  // opening a mail client. The href stays a real mailto: — with JS off the link
  // still works, and right-click > Copy Link Address still yields the address.
  var link = document.querySelector('.nav a[data-mail]');
  if(!link) return;
  /* Assembled at runtime, never written out whole. Scrapers overwhelmingly work on
     fetched source rather than a rendered page, so keeping the "@" out of the file
     (it is @ here) and the halves apart is enough to miss the usual regex.
     A browser reconstructs it before anyone can click. */
  var address = ['vong','kiara','real'].reverse().join('') + '@' + ['gmail','com'].join('.');
  link.setAttribute('href', 'mailto:' + address);
  var resting = link.getAttribute('data-tip');
  var revert = null;

  /* Failure holds longer than success: "Copied!" only needs to be seen, whereas the
     fall-back shows the address itself and has to stay up long enough to read and
     type. That path fires when the browser refuses the clipboard — a non-secure
     origin, or Safari withholding permission. */
  function flash(msg, ms){
    link.setAttribute('data-tip', msg);
    /* Mobile hides every menu tooltip, because a tap leaves hover stuck on a touch
       device and they would hang there unexplained. This one is not a hover tooltip
       though, so it is marked while it is up and mobile.css lets it through. */
    link.classList.add('is-copied');
    clearTimeout(revert);
    revert = setTimeout(function(){
      link.setAttribute('data-tip', resting);
      link.classList.remove('is-copied');
    }, ms || 1600);
    /* Only a real copy earns the fanfare. Gated on the message rather than on the call
       site because both the clipboard path and the execCommand fall-back can succeed,
       while the third case shows the address itself and has not copied anything.

       The colour is the pill's own face, so dots landing on the pill vanish and dots past
       its edge show, and the burst reads as coming from behind the label. It is read off
       the ::after rather than hardcoded because Library recolours its whole menu to
       new-leaf-green, where a persimmon sprinkle would be a stray site colour. */
    if (msg === 'Copied!' && window.sitePop) {
      var box = tipBox();
      /* The pill's own face, which Library recolours: that page's menu answers in
         new-leaf-green rather than the site's persimmon, and the sprinkle is read off
         the ::after it bursts from so it always matches whatever the pill is wearing. */
      if (box) {
        var face = getComputedStyle(link, '::after').backgroundColor;
        var m = face && face.match(/(\d+)[,\s]+(\d+)[,\s]+(\d+)/);
        window.sitePop(box, { rgb: m ? m[1] + ',' + m[2] + ',' + m[3] : '242,81,26' });
      }
    }
  }

  /* The preview is a ::after, so there is no element to measure. Everything needed is
     still readable off the pseudo's computed style, which Chrome resolves to used
     values, so this follows the CSS rather than restating it: only the horizontal
     centring is assumed, and that is the one part the stylesheet spells out as
     intentional (left:50% then -50% of its own width). Returns null rather than
     guessing if the browser gives nothing back. */
  function tipBox(){
    if (!window.getComputedStyle) return null;
    var cs = getComputedStyle(link, '::after');
    if (!cs) return null;
    var w = parseFloat(cs.width), h = parseFloat(cs.height);
    if (!(w > 0) || !(h > 0)) return null;
    if (cs.boxSizing !== 'border-box') {
      w += (parseFloat(cs.paddingLeft) || 0) + (parseFloat(cs.paddingRight) || 0);
      h += (parseFloat(cs.paddingTop) || 0) + (parseFloat(cs.paddingBottom) || 0);
    }
    var r = link.getBoundingClientRect();
    var up = parseFloat(cs.bottom);
    if (!isFinite(up)) return null;
    return { cx: r.left + r.width / 2, cy: r.bottom - up - h / 2, w: w, h: h };
  }
  function ok(){ flash('Copied!'); }
  function fail(){ flash(legacy(address) ? 'Copied!' : address, 5000); }
  function legacy(text){
    // Safari without clipboard permission, and any non-secure origin.
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly','');
    ta.style.cssText = 'position:fixed;top:-1000px;opacity:0';
    document.body.appendChild(ta);
    ta.select();
    var ok = false;
    try { ok = document.execCommand('copy'); } catch(e){}
    document.body.removeChild(ta);
    return ok;
  }

  link.addEventListener('click', function(e){
    e.preventDefault();
    if(navigator.clipboard && window.isSecureContext){
      navigator.clipboard.writeText(address).then(ok, fail);
    } else {
      fail();
    }
  });
  // The tooltip is the only feedback, so make sure it is showing when it changes.
  link.addEventListener('mouseleave', function(){
    clearTimeout(revert);
    link.setAttribute('data-tip', resting);
    link.classList.remove('is-copied');
  });
})();

/* ---------------------------------------------------------------------------
   Sticky menu.

   The pill is fixed on every page that has one, so it travels with the reader.
   It stands down when the footer arrives: the footer carries the same three
   links, so the pill would only be repeating itself, and its glass surface goes
   nearly invisible against the pale About footer. The trigger is the same one
   payments-home uses for its chrome — the footer's top crossing the pill's
   bottom, with 24px of margin. */
(function(){
  var pill = document.querySelector('.nav');
  if (!pill) return;
  /* Every page that floats the pill registers its wrapper here. Pages built
     as normal flowing documents (Art, the case studies, the mockups) use
     #pg-navwrap / #cs-navwrap; leaving them out meant this whole function
     bailed on those pages, so the pill neither stood down at the footer nor
     picked up its light-ground surface. */
  var wrap = pill.closest('#hg-center, #ab-navwrap, #lb-navwrap, #pg-navwrap, #cs-navwrap');
  var footer = document.getElementById('footer');
  if (!wrap || !footer) return;

  /* The page's photographic ground. Past its bottom edge the pill is over parchment
     and needs a surface — see .nav.on-light. */
  var ground = document.querySelector('#hero, .ab-canvas, .lb-screen');

  /* A page with no photographic ground at all is light from top to bottom, so the
     pill is over parchment the whole way down and needs its surface permanently.
     Without this the label is parchment on parchment and simply is not there --
     which is what was happening on every page that is not the index or About. */
  if (!ground) pill.classList.add('on-light');

  var ticking = false;
  function park(){
    ticking = false;
    /* Below the breakpoint the pill is already a fixed bottom bar and the footer
       runs under it by design, so leave it alone. */
    if (window.innerWidth <= 760) {
      wrap.classList.remove('is-away');
      pill.classList.remove('on-light');   /* mobile.css gives the bar its own surface */
      return;
    }
    var f = footer.getBoundingClientRect();
    var p = pill.getBoundingClientRect();
    wrap.classList.toggle('is-away', f.top < p.bottom + 24);
    if (ground) pill.classList.toggle('on-light', ground.getBoundingClientRect().bottom < p.bottom);

  }
  function onScroll(){
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(park);
  }
  park();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(park);
})();

/* The Art index's back arrow -------------------------------------------------
   It starts over the painted band and ends over parchment, so it switches colour at
   the band's bottom edge. Same class name as the pill's, same idea, but deliberately
   its own block: the pill's runs behind `if (!wrap || !footer) return`, and an arrow
   in the top-left corner has no business depending on whether a footer exists. It
   did, briefly, and simply never fired. */
(function () {
  var back = document.querySelector('.ap-back');
  var band = document.querySelector('.ai-hero');
  if (!back || !band) return;
  var ticking = false;
  function mark() {
    ticking = false;
    /* Below the breakpoint the arrow is in the flow on parchment, not over the band. */
    if (window.innerWidth <= 760) { back.classList.add('on-light'); return; }
    var b = back.getBoundingClientRect();
    back.classList.toggle('on-light', band.getBoundingClientRect().bottom < b.top + 4);
  }
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(mark);
  }
  mark();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
})();
