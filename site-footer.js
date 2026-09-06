/* The site footer: one source of truth for its markup and its behaviour.
   A page drops in <div id="site-footer"></div> and loads this before its own
   scripts; this renders the footer, then starts the clock and the plant garden. */
/* How far down we are, as a prefix to put in front of every path in this file.

   These used to be written root-relative ("assets/ui/...", "index.html"), which was
   correct while every page sat at the root. Half of them are one folder down now, so
   on art/, work/ and projects/ the flowers resolved to art/assets/... and every nav
   link pointed at a page inside the folder it was already in. Nothing errored; the
   icons were simply absent and the links went nowhere.

   Derived from the page's own stylesheet link rather than from location.pathname,
   which would be wrong the moment the site is served from a subdirectory. Whatever
   prefix a page uses to reach site.css is the prefix its footer needs.

   At file scope because this file has four separate IIFEs and two of them need it. */
var SITE_ROOT = (function () {
  var l = document.querySelector('link[rel="stylesheet"][href$="site.css"]');
  return l ? l.getAttribute('href').replace(/site\.css$/, '') : '';
})();

(function(){
  var slot = document.getElementById("site-footer");
  if(!slot) return;
  /* A page can ask for a variant with data-variant, e.g. the About page's green
     one. Everything but the colours, the flower tiles and which nav item reads as
     current is shared, so the variant is a class rather than a second footer. */
  var variant = slot.getAttribute('data-variant') || '';

  slot.outerHTML = '<section id="footer"' + (variant ? ' class="is-' + variant + '"' : '') + '>\n   <div class="plant-layer" aria-hidden="true"></div>\n   <div class="foot-inner">\n    <div class="foot-left">\n      <div class="flowers" aria-hidden="true">\n        <img class="fl f1" src="' + SITE_ROOT + 'assets/ui/footer-flowers.svg" alt="">\n        <img class="fl f2" src="' + SITE_ROOT + 'assets/ui/footer-flowers.svg" alt="">\n        <img class="fl f3" src="' + SITE_ROOT + 'assets/ui/footer-flowers.svg" alt="">\n      </div>\n      <p class="quote">Most of the work is deciding what not to build.</p>\n    </div>\n\n    <div class="foot-right">\n      <div class="foot-links">\n        <a href="#" data-mail><span class="lbl">Email</span>\n          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 8H10C8.89543 8 8 8.89543 8 10V20C8 21.1046 8.89543 22 10 22H20C21.1046 22 22 21.1046 22 20V10C22 8.89543 21.1046 8 20 8Z"/><path d="M4 16C2.9 16 2 15.1 2 14V4C2 2.9 2.9 2 4 2H14C15.1 2 16 2.9 16 4"/></svg>\n          <span class="foot-toast" aria-hidden="true">Copied!</span>\n        </a>\n        <a href="https://www.linkedin.com/in/kiara-vong/" target="_blank" rel="noopener"><span class="lbl">LinkedIn</span>\n          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h6"/></svg>\n        </a>\n      </div>\n      <nav class="foot-nav">\n        <a href="' + SITE_ROOT + 'index.html" class="index">Home</a>\n        <a href="' + SITE_ROOT + 'index.html#projects">Projects</a>\n        <a href="' + SITE_ROOT + 'art/">Art</a>\n<a href="' + SITE_ROOT + 'about.html">About</a>\n      </nav>\n    </div>\n\n    <div class="weather">\n      <span class="dot"></span>\n      <p>Sunny, 72°     <span id="clock">2:13:11 PM ET</span></p>\n    </div>\n   </div>\n  </section>';

  /* Same reason as the nav: the address is never present in this file as a whole
     string, so fetching the source does not yield it. */
  /* The persimmon footer draws its three tiles from one sprite via object-position.
     The About footer's three tiles are identical in the design (Figma 358:1299), so
     they all point at one asset rather than at a sprite or a pair. */
  /* The persimmon footer draws its three tiles from one sprite via object-position.
     The variants each have a single tile repeated three times in the design, so they
     point all three at one asset instead. Library's two groups in Figma (358:1256
     and 358:1263) are the same flower, checked pixel for pixel. */
  var TILE = { about: SITE_ROOT + 'assets/ui/foot-flower-about.svg',
               library: SITE_ROOT + 'assets/ui/foot-flower-alt.svg' };
  if (TILE[variant]) {
    document.querySelectorAll('#footer .flowers .fl').forEach(function(img){
      img.src = TILE[variant];
    });
  }

  /* Which of the three reads as current, taken from the page itself rather than
     from the variant. It used to be handled inside the About branch alone, which
     was survivable while Home and Library went nowhere; now that all three
     navigate, every other page would have shown Home as the one you were on. */
  (function(){
    var here = (location.pathname.split('/').pop() || 'index.html');
    document.querySelectorAll('#footer .foot-nav a').forEach(function(a){
      a.classList.remove('index');
      a.classList.toggle('current', a.getAttribute('href') === here);
    });
  })();

  /* The address is never written out whole. Scrapers work on fetched source far more
     than on a rendered page, so keeping the "@" out of the file and the halves apart
     is enough to miss the usual pattern. A browser puts it back together before
     anyone can click. */
  var mail = document.querySelector('#footer a[data-mail]');
  if (mail) {
    var address = ['vong','kiara','real'].reverse().join('') + '\u0040' + ['gmail','com'].join('.');
    mail.setAttribute('href', 'mailto:' + address);
    var toast = mail.querySelector('.foot-toast');
    var hide = null;

    function show(msg, ms){
      if (!toast) return;
      toast.textContent = msg;
      toast.classList.add('is-on');
      clearTimeout(hide);
      hide = setTimeout(function(){ toast.classList.remove('is-on'); }, ms || 1700);
      /* Only a real copy earns the fanfare. Gated on the message rather than on the
         call site because both the clipboard path and the execCommand fall-back can
         succeed, while the third case shows the address itself and has not copied
         anything.

         Parchment, matching the toast's own face, because the default footer ground is
         persimmon and the trail sparks' persimmon would vanish into it. The About
         footer swaps that ground for pear, where parchment on pale yellow-green is
         almost as weak, so it takes slate instead -- the colour that variant already
         recolours all of its text to. */
      if (msg === 'Copied!' && window.sitePop) {
        var onPear = mail.closest('#footer') &&
                     mail.closest('#footer').classList.contains('is-about');
        window.sitePop(toast, { rgb: onPear ? '120,128,143'      /* --slate */
                                            : '253,251,239' });  /* --parchment */
      }
    }
    /* Falling back to the address itself holds longer: "Copied!" only has to be seen,
       whereas an address has to be read and typed. That path is for a non-secure
       origin, or Safari withholding clipboard permission. */
    function legacy(text){
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.setAttribute('readonly','');
      ta.style.cssText = 'position:fixed;top:-1000px;opacity:0';
      document.body.appendChild(ta);
      ta.select();
      var done = false;
      try { done = document.execCommand('copy'); } catch(e){}
      document.body.removeChild(ta);
      return done;
    }
    mail.addEventListener('click', function(e){
      e.preventDefault();
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(address).then(
          function(){ show('Copied!'); },
          function(){ show(legacy(address) ? 'Copied!' : address, 5000); });
      } else {
        show(legacy(address) ? 'Copied!' : address, 5000);
      }
    });
  }
})();

// Live Washington DC clock in the footer weather line. The suffix is derived
// rather than hardcoded, so it reads EDT in summer and EST in winter instead
// of being wrong for half the year.
(function(){
  var el = document.getElementById('clock');
  if(!el) return;
  function tick(){
    var now = new Date();
    var t = now.toLocaleTimeString('en-US', {timeZone:'America/New_York', hour:'numeric', minute:'2-digit', second:'2-digit', hour12:true});
    /* Ask the formatter what it would CALL this zone right now, rather than
       assuming: en-US short timeZoneName yields "EST" or "EDT" on the correct
       side of the switchover, and falls back to "ET" if the runtime declines. */
    var zone = 'ET';
    try {
      var parts = new Intl.DateTimeFormat('en-US', {timeZone:'America/New_York',
        timeZoneName:'short'}).formatToParts(now);
      for (var i = 0; i < parts.length; i++) {
        if (parts[i].type === 'timeZoneName') { zone = parts[i].value; break; }
      }
    } catch (e) {}
    el.textContent = t + ' ' + zone;
  }
  tick();
  setInterval(tick, 1000);
})();

/* Footer garden: clicking anywhere in the footer (but not on a link) stamps the
   plant motif at that spot and lets it grow sprout -> stem -> flower by itself. */
(function(){
  var footer=document.getElementById('footer');
  var layer=footer && footer.querySelector('.plant-layer');
  if(!footer || !layer) return;
  /* The About footer's ground is pale, so the light plant would vanish into it.
     Same three stages, dark artwork. */
  /* One set now. The About footer used to be a pale green band that needed the
     dark sprouts; it is the same painting as every other footer since, so a second
     set of artwork would be two answers to a question that now has one. */
  var PLANTS = false
    ? [SITE_ROOT + 'assets/ui/plant-dark-sm.svg', SITE_ROOT + 'assets/ui/plant-dark-med.svg',
       SITE_ROOT + 'assets/ui/plant-dark-lg.svg']
    : [SITE_ROOT + 'assets/ui/plant-sm.svg', SITE_ROOT + 'assets/ui/plant-med.svg',
       SITE_ROOT + 'assets/ui/plant-lg.svg'];
  PLANTS.forEach(function(s){ var i=new Image(); i.src=s; });
  var reduce=window.matchMedia && matchMedia('(prefers-reduced-motion:reduce)').matches;
  var stamps=[], MAX=48;
  function plant(x,y){
    var s=document.createElement('div'); s.className='plant-stamp';
    s.style.left=x+'px'; s.style.top=y+'px';
    s.innerHTML='<img class="p1" src="'+PLANTS[0]+'" alt="">'
              +'<img class="p2" src="'+PLANTS[1]+'" alt="">'
              +'<img class="p3" src="'+PLANTS[2]+'" alt="">';
    layer.appendChild(s);
    var a=s.children[0], b=s.children[1], c=s.children[2];
    if(reduce){ c.classList.add('grow'); }
    else{
      requestAnimationFrame(function(){ a.classList.add('grow'); });
      setTimeout(function(){ b.classList.add('grow'); a.classList.add('fade'); }, 1300);
      setTimeout(function(){ c.classList.add('grow'); b.classList.add('fade'); }, 2600);
    }
    stamps.push(s); if(stamps.length>MAX){ stamps.shift().remove(); }
  }
  footer.addEventListener('click', function(e){
    if(e.target.closest && e.target.closest('a')) return;   // leave links alone
    var r=footer.getBoundingClientRect(); var scale=r.width/1440 || 1;
    plant((e.clientX-r.left)/scale, (e.clientY-r.top)/scale);
  });
})();

/* Back to top. Lives with the footer because it is site chrome, not page content, and
   because its visibility depends on where the footer is. Appears once you are a screen
   down, hides again as the footer arrives. */
(function () {
  if (document.querySelector('.to-top')) return;
  var btn = document.createElement('button');
  btn.className = 'to-top';
  btn.type = 'button';
  btn.setAttribute('aria-label', 'Back to top');
  btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">' +
    '<path d="M6 15L12 9L18 15" stroke="#A7A58F" stroke-width="2" ' +
    'stroke-linecap="round" stroke-linejoin="round"/></svg>';
  document.body.appendChild(btn);

  var reduce = window.matchMedia &&
               window.matchMedia('(prefers-reduced-motion:reduce)').matches;

  btn.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
  });

  var ticking = false;
  function update() {
    ticking = false;
    var y = window.pageYOffset || document.documentElement.scrollTop || 0;
    /* Measure whichever footer element is actually laid out. #bg-footer is only a
       decorative backdrop: on the home page at phone widths it collapses to height 0
       near the top of the document, so preferring it reported "the footer is here"
       from the first pixel and the button never appeared at all. Prefer the real
       footer, fall back to the backdrop, and ignore either one if it has no height.
       And on a page barely taller than the window there is nothing worth a shortcut,
       so it stays away entirely. */
    var real = document.getElementById('footer'), bg = document.getElementById('bg-footer');
    var footer = (real && real.getBoundingClientRect().height) ? real
               : (bg && bg.getBoundingClientRect().height) ? bg
               : (real || bg);
    var footerNear = false;
    if (footer) {
      var r = footer.getBoundingClientRect();
      footerNear = r.top < window.innerHeight - 24;
    }
    var scrollable = document.documentElement.scrollHeight - window.innerHeight;
    var worthIt = scrollable > window.innerHeight;
    btn.classList.toggle('is-on', worthIt && y > window.innerHeight * 0.75 && !footerNear);
  }
  function onScroll() {
    if (!ticking) { ticking = true; requestAnimationFrame(update); }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
  update();
})();
