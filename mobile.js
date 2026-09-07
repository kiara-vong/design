/* The handful of things the mobile layout cannot express in CSS.

   CSS has no way to divide one length by another, so it cannot turn "this 529px
   block must fit a column of (100vw - 40px)" into a scale factor. Those factors are
   computed here and handed to mobile.css as custom properties. Above the breakpoint
   they are removed, so nothing lingers on desktop. */
(function () {
  var MOBILE = 760;
  var root = document.documentElement;

  /* Design widths of the blocks that are scaled whole rather than rebuilt. */
  var CARD_W = 529;      /* the phone mock inside a work card */
  var WELL_W = 591;      /* the illustration well on About */
  var MODAL_W = 1052, MODAL_H = 750;

  function apply() {
    var vw = window.innerWidth, vh = window.innerHeight;
    if (vw > MOBILE) {
      root.style.removeProperty('--card-k');
      root.style.removeProperty('--well-k');
      return;
    }
    var col = vw - 40;                       /* page padding, 20px each side */
    var cardCol = col - 32;                  /* the card adds 16px of its own */
    root.style.setProperty('--card-k', Math.min(cardCol / CARD_W, 1).toFixed(4));
    root.style.setProperty('--well-k', Math.min(col / WELL_W, 1).toFixed(4));
    /* The home page's fit() sets this from the hero scale and stands down here, so
       there would otherwise be no value at all on a phone. */
    root.style.setProperty('--modal-scale',
      (Math.min(vw / MODAL_W, vh / MODAL_H) * 0.94).toFixed(4));

    /* Calcifer's bubble sits above him, but it is positioned against #hg-left, and
       that column does not end where he does. Guessing the offset from his height
       put the bubble across his face, so it is measured. */
    var col = document.getElementById('hg-left');
    var cal = document.querySelector('.mascot');
    if (col && cal) {
      var gap = col.getBoundingClientRect().bottom - cal.getBoundingClientRect().top;
      root.style.setProperty('--bubble-bottom', Math.round(gap + 3) + 'px');
    }
  }

  apply();
  /* The measurement above depends on laid-out text, so take it again once the web
     fonts have swapped in and the column has settled. */
  window.addEventListener('load', apply);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(apply);
  window.addEventListener('resize', apply, { passive: true });
  window.addEventListener('orientationchange', apply, { passive: true });

  /* Without a pointer that hovers, "hover over a link" is an instruction nobody can
     follow. The word is swapped rather than the sentence rewritten, so the two stay
     in step if the copy changes. */
  /* (hover: none) alone misses a touch device that also reports a hover-capable
     pointer, and misses emulators entirely; a coarse pointer is the other half. */
  var touch = window.innerWidth <= MOBILE || (window.matchMedia &&
    (window.matchMedia('(hover: none)').matches ||
     window.matchMedia('(pointer: coarse)').matches));
  if (touch) {
    document.addEventListener('DOMContentLoaded', function () {
      document.querySelectorAll('.ab-hint, .ab-aside, .lb-hint').forEach(function (el) {
        /* "hover over a link" -> "tap a link", not "tap over a link": the longer
           phrase has to go first or the bare word eats it. */
        el.innerHTML = el.innerHTML
          .replace(/\bhover over\b/gi, 'tap')
          .replace(/\bhover\b/gi, 'tap');
      });
      /* About writes its own <span> around the noun and Library does not, so the two
         instructions read differently even once they say the same thing. This gives
         Library the same accented object word, and mobile.css matches the rest. */
      document.querySelectorAll('.lb-hint').forEach(function (el) {
        if (el.querySelector('span')) return;
        el.innerHTML = el.innerHTML.replace(/(\w+)(\s*)$/, '<span>$1</span>$2');
      });
      /* About's illustrations are bound to pointerenter AND pointerleave, and a tap fires
         both back to back -- so the art appeared and vanished inside the one gesture and
         tapping a link did nothing at all. The hint said "tap a link" and nothing happened.

         Library's books already tap to open and tap to dismiss, so About is brought to
         the same model rather than the two behaving differently. The state is read on
         pointerdown, before the browser's synthetic enter/leave pair runs, and the click
         then dispatches whichever of the two the gesture actually meant. */
      var artLinks = [].slice.call(document.querySelectorAll('.ab-moon a[data-art]'));
      if (artLinks.length) {
        var wasLive = false;
        artLinks.forEach(function (a) {
          a.addEventListener('pointerdown', function () {
            wasLive = a.classList.contains('is-live');
          }, { passive: true });
          a.addEventListener('click', function (e) {
            e.preventDefault(); e.stopPropagation();
            artLinks.forEach(function (o) { o.classList.remove('is-live'); });
            if (wasLive) {
              a.dispatchEvent(new MouseEvent('pointerleave'));
            } else {
              a.classList.add('is-live');
              a.dispatchEvent(new MouseEvent('pointerenter'));
            }
          });
        });
        /* Tapping anywhere else puts it away, the way the ticket and the bubble do. */
        document.addEventListener('click', function (e) {
          if (e.target.closest && e.target.closest('.ab-moon a[data-art]')) return;
          artLinks.forEach(function (o) {
            if (o.classList.contains('is-live')) {
              o.classList.remove('is-live');
              o.dispatchEvent(new MouseEvent('pointerleave'));
            }
          });
        });
      }

      /* Calcifer's bubble is bound to mouseenter/mouseleave, which pick a fresh
         message and never repeat two in a row. Rather than restate that list here,
         the tap just sends those two events, so the phone and the desktop stay one
         behaviour with one source of messages. */
      var rabbit = document.querySelector('.mascot');
      var bubble = document.querySelector('.bubble');
      var prompt = document.querySelector('.bubble-prompt');
      if (rabbit && bubble) {
        if (prompt) prompt.innerHTML = prompt.innerHTML.replace(/\bhover\b/gi, 'tap');
        rabbit.style.cursor = 'pointer';
        /* Every tap advances. This used to toggle, which meant reading a second prompt
           took two taps and a shut bubble in between, and there is no reason to make
           someone close him to hear him again. Dispatching mouseenter is all it takes:
           the desktop handler already picks a fresh message, never repeats twice running,
           and leaves the bubble up. Putting it away is a tap anywhere else, which is the
           gesture the ticket and the postcards already use.

           The relay is still doing real work. A tap does not produce a click on its own:
           the browser replays the touch as mouseover, mouseenter, mousedown, mouseup and
           only then click. That first mouseenter is real, so tap one opens the bubble on
           its own -- but every tap after lands on an element the browser already counts as
           hovered, so no further mouseenter arrives and the prompt would never change.

           Tap one therefore draws twice, once from the browser and once from here, and
           shows the second. That costs one unseen message while the bubble is still
           fading up, which is cheaper than tracking hover state to avoid it and then
           doing nothing at all on any browser that skips the synthetic enter. */
        rabbit.addEventListener('click', function (e) {
          e.preventDefault(); e.stopPropagation();
          rabbit.dispatchEvent(new MouseEvent('mouseenter'));
        });
        /* Tapping anywhere else puts it away, the way moving the cursor off does. */
        document.addEventListener('click', function (e) {
          if (!bubble.classList.contains('is-visible')) return;
          if (e.target === rabbit || rabbit.contains(e.target)) return;
          rabbit.dispatchEvent(new MouseEvent('mouseleave'));
        });
      }
    });
  }
})();

/* Case-study figures: scale to fit rather than scroll sideways -----------------
   Every figure on a case study is width:100% inside .cs-main, which is 799px wide, and
   the contents are laid out at absolute pixel coordinates tuned to that width. So the
   whole frame is scaled by one ratio, column over 799, and everything inside keeps its
   relationship to everything else.

   The first version of this measured each figure's widest descendant instead. That was
   wrong in two ways: the frame was squeezed to the phone column while its contents kept
   their 799 coordinates, and it read every overflow as a mistake. Some are the design --
   .cs-media is a 391px window onto a 280x600 phone placed at left 260, with a camera
   move that slides it around inside the crop. Measuring that phone and shrinking to fit
   it destroyed the shot. */
(function () {
  var MOBILE = 760;
  var CS_W = 799;                 /* .cs-main, the width every figure is authored against */

  function clear(el) {
    el.classList.remove('cs-fit');
    el.style.removeProperty('margin-bottom');
    if (el.parentElement) el.parentElement.style.removeProperty('--fig-k');
  }

  function fit() {
    var figs = document.querySelectorAll('.cs-figure');
    if (!figs.length) return;
    if (window.innerWidth > MOBILE) {
      figs.forEach(function (f) { if (f.firstElementChild) clear(f.firstElementChild); });
      return;
    }
    figs.forEach(function (fig) {
      var el = fig.firstElementChild;
      if (!el || el.tagName === 'IMG') return;
      clear(el);
      /* Impact opts out. It is a block of numbers and sentences, and shrinking type to
         44% is the opposite of what it needs; mobile.css gives it a stacked layout at
         full size instead. */
      if (el.classList.contains('stats') || el.classList.contains('cs-rules') ||
          el.classList.contains('cp-assume')) return;
      var avail = fig.clientWidth;
      if (!avail || avail >= CS_W) return;
      var k = avail / CS_W;
      el.classList.add('cs-fit');          /* pins the width to 799 before measuring */
      fig.style.setProperty('--fig-k', k.toFixed(4));
      /* offsetHeight is the unscaled height, which is exactly what has to be given back:
         transform does not affect layout, so the box still claims its full height. */
      el.style.marginBottom = Math.round(-el.offsetHeight * (1 - k)) + 'px';
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fit);
  else fit();
  window.addEventListener('load', fit);
  window.addEventListener('resize', fit, { passive: true });
  window.addEventListener('orientationchange', fit, { passive: true });
})();

/* Tap a figure to see it at size ----------------------------------------------
   Figures are scaled to the phone column, which is 0.438 of the 799px they were drawn
   against. That is enough to read a composition and not enough to read a diagram, so
   each one gets a button that opens it rotated into landscape, where the long edge of
   the screen gives it 844px instead of 350 -- 2.4x the room, close to its authored size.

   The figure is MOVED into the overlay and put back afterwards rather than cloned, so
   there is never a second copy to keep in step: the animations, the canvases and the
   interactive figures all carry their own state, and a clone would either freeze or run
   twice. A placeholder holds its slot in the page while it is away. */
(function () {
  var MOBILE = 760, CS_W = 799;
  if (!document.querySelector('.cs-figure')) return;

  var ICON_ZOOM = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 3h6v6"/><path d="M9 21H3v-6"/><path d="M21 3l-7 7"/><path d="M3 21l7-7"/></svg>';
  var ICON_CLOSE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M18 6 6 18M6 6l12 12"/></svg>';

  var lens, anim, stage, hint, slot, held, heldFig, flip, lockY = null;

  function build() {
    lens = document.createElement('div');
    lens.id = 'cs-lens';
    lens.setAttribute('role', 'dialog');
    lens.setAttribute('aria-modal', 'true');
    lens.hidden = false;
    anim = document.createElement('div');
    anim.className = 'lens-anim';
    stage = document.createElement('div');
    stage.className = 'lens-stage';
    anim.appendChild(stage);
    var close = document.createElement('button');
    close.className = 'lens-close';
    close.type = 'button';
    close.setAttribute('aria-label', 'Close');
    close.innerHTML = ICON_CLOSE;
    hint = document.createElement('p');
    hint.className = 'lens-hint';
    lens.appendChild(anim); lens.appendChild(close); lens.appendChild(hint);
    document.body.appendChild(lens);
    close.addEventListener('click', shut);
    /* "Tap anywhere" has to mean anywhere, which it did not: only the backdrop and the
       bare stage closed, so a tap on the figure or on the caption itself did nothing at
       all -- and the caption is the thing telling you to tap.

       The one exception is a real control inside the figure. Some of these compositions
       carry buttons, and expanding one should not be the moment they stop working. */
    lens.addEventListener('click', function (e) {
      if (e.target.closest('.lens-close')) return;
      if (stage.contains(e.target) &&
          e.target.closest('button, a, input, select, summary, [role="button"]')) return;
      shut();
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && held) shut(); });
  }

  function open(fig) {
    if (!lens) build();
    var el = fig.firstElementChild;
    if (!el) return;
    held = el; heldFig = fig;

    /* The placeholder goes exactly where the figure was, not on the end. Appending it
       meant the composition came back after its own caption, and the fitter -- which
       works on fig.firstElementChild -- then scaled the caption instead. */
    slot = document.createElement('div');
    slot.style.height = fig.getBoundingClientRect().height + 'px';
    fig.insertBefore(slot, el);

    el.classList.remove('cs-fit');
    el.style.width = CS_W + 'px';
    el.style.marginBottom = '';
    el.style.transform = '';
    el.style.transformOrigin = 'top left';
    stage.appendChild(el);              /* in the DOM before its height is asked for */

    /* Fit BOTH axes, and rotate only if rotating actually wins.

       This used to fit the width alone -- k = (longEdge - 24) / 799 -- and never looked at
       how tall the figure was. That is fine for a wide, shallow one, and badly wrong for
       a deep one: the four variants are 799 x 1381, so turned sideways they needed 1381px
       across a 390px screen and lost a third of themselves off both edges.

       Now both orientations are costed and the better one is used. The variants come out
       upright at 0.46; cs-media, at 799 x 391, still turns and gains 0.94 against 0.46.
       The 1.04 margin stops a rotation that is barely worth the tilt. */
    var PAD = 24, vw = window.innerWidth, vh = window.innerHeight;
    var figH = el.offsetHeight;
    var kFlat = Math.min((vw - PAD) / CS_W, (vh - PAD) / figH, 1);
    var kTurn = Math.min((vh - PAD) / CS_W, (vw - PAD) / figH, 1);
    var turn = kTurn > kFlat * 1.04;
    var k = turn ? kTurn : kFlat;

    el.style.transform = 'scale(' + k.toFixed(4) + ')';
    stage.style.width = CS_W * k + 'px';
    stage.style.height = figH * k + 'px';
    stage.style.transform = turn ? 'rotate(90deg)' : 'none';

    /* The caption stays upright while the figure is turned, because it has to be read
       before the phone is. Once the reader tilts, the figure comes up straight and this
       goes sideways, which is the right way round: by then it has done its job. It is
       only shown when the view is actually rotated -- on a phone already held landscape
       there is nothing to tilt. */
    hint.innerHTML = turn
      ? '<span>Tilt your phone to view \u00b7 tap to close</span>'
      : '<span>Tap anywhere to close</span>';

    lockY = window.pageYOffset || document.documentElement.scrollTop || 0;
    document.body.classList.add('lens-open');

    /* A short rise, not a flight. Two versions of this were wrong in opposite directions:
       the first only eased the last 5% of the size change, so the figure snapped and a
       fade played over the top; the second was a true FLIP that carried the rotation, and
       a rectangle rotating while it scales has a bounding box that peaks at 45 degrees --
       measured at 610px across in a 390 viewport. Correct, and far too much.

       This keeps the figure in its final orientation throughout and lets it settle the
       last short distance. The travel is the fade; the scale only has to stop the arrival
       reading as a cut. */
    lens.classList.add('is-on');
    flip = 'scale(.94)';
    anim.style.transition = 'none';
    anim.style.transform = flip;
    void anim.offsetWidth;                       /* commit the resting state */
    anim.style.transition = '';
    requestAnimationFrame(function () { anim.style.transform = 'none'; });
  }

  function shut() {
    if (!held) return;
    /* Back down the same path it came up. The figure returns to the page only once it
       has arrived, or it would reappear behind a backdrop that is still fading. */
    if (flip) anim.style.transform = flip;
    lens.classList.remove('is-on');
    var el = held, fig = heldFig, ph = slot;
    held = heldFig = slot = null;
    setTimeout(function () {
      anim.style.transition = 'none';
      anim.style.transform = 'none';
      /* The DOM move waits one more frame, so it never lands in the same frame as the
         transition ending. */
      requestAnimationFrame(function () {
        restore(el, fig, ph);
        document.body.classList.remove('lens-open');
        /* overflow:hidden does not hold the scroll position, so putting it back by hand
           is what stops the page appearing to jolt as the overlay clears. */
        if (lockY != null) { window.scrollTo(0, lockY); lockY = null; }
      });
    }, 340);
  }

  function restore(held, heldFig, slot) {
    held.style.transform = '';
    held.style.transformOrigin = '';
    held.style.width = '';

    /* This one figure is put back, and only this one. It used to end by dispatching a
       global resize, which was the hitch at the end of the close: that event re-runs the
       fitter over every figure on the page, re-runs the zoom-button pass, and wakes the
       hero parallax -- a full synchronous re-layout in the frame the overlay disappears.
       Everything needed here is already known. */
    var avail = heldFig.clientWidth;
    if (avail && avail < CS_W) {
      var k = avail / CS_W;
      held.classList.add('cs-fit');
      heldFig.style.setProperty('--fig-k', k.toFixed(4));
      held.style.marginBottom = Math.round(-held.offsetHeight * (1 - k)) + 'px';
    }
    if (slot && slot.parentNode) slot.parentNode.replaceChild(held, slot);
    else heldFig.insertBefore(held, heldFig.firstChild);
  }

  function sync() {
    var on = window.innerWidth <= MOBILE;
    document.querySelectorAll('.cs-figure').forEach(function (fig) {
      var btn = fig.querySelector('.cs-zoom');
      var el = fig.firstElementChild;
      var worth = el && el.tagName !== 'IMG' && !el.classList.contains('stats') &&
                  !el.classList.contains('cs-rules') && !el.classList.contains('cp-assume') &&
                  fig.clientWidth < CS_W;
      if (on && worth && !btn) {
        btn = document.createElement('button');
        btn.className = 'cs-zoom';
        btn.type = 'button';
        btn.setAttribute('aria-label', 'View this figure larger');
        btn.innerHTML = ICON_ZOOM;
        btn.addEventListener('click', function (e) { e.stopPropagation(); open(fig); });
        fig.appendChild(btn);
      }
      if (btn && el) {
        /* .cs-figure holds the artwork AND its caption, so bottom:8 put the button over
           the caption. Sit it on the artwork's own bottom-right instead. */
        var fr = fig.getBoundingClientRect(), er = el.getBoundingClientRect();
        btn.style.top = Math.max(8, Math.round(er.bottom - fr.top - 42)) + 'px';
        btn.style.bottom = 'auto';
      } else if ((!on || !worth) && btn) {
        btn.remove();
      }
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', sync);
  else sync();
  window.addEventListener('load', sync);
  /* Turning the phone is what the caption asks for, so it must not close the lens. The
     figure is re-laid-out for the new viewport instead: upright once there is width for
     it, still turned if there is not. */
  function relayout() {
    if (!held) return;
    var PAD = 24, vw = window.innerWidth, vh = window.innerHeight;
    held.style.transform = '';
    var figH = held.offsetHeight;
    var kFlat = Math.min((vw - PAD) / CS_W, (vh - PAD) / figH, 1);
    var kTurn = Math.min((vh - PAD) / CS_W, (vw - PAD) / figH, 1);
    var turn = kTurn > kFlat * 1.04;
    var k = turn ? kTurn : kFlat;
    held.style.transform = 'scale(' + k.toFixed(4) + ')';
    stage.style.width = CS_W * k + 'px';
    stage.style.height = figH * k + 'px';
    stage.style.transform = turn ? 'rotate(90deg)' : 'none';
    hint.innerHTML = turn
      ? '<span>Tilt your phone to view \u00b7 tap to close</span>'
      : '<span>Tap anywhere to close</span>';
  }
  window.addEventListener('orientationchange', function () { setTimeout(relayout, 120); });
  window.addEventListener('resize', function () { if (held) relayout(); });
})();
