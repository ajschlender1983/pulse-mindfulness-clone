/* ============================================================
   Pulse — Repositioning demo layer
   - Toggle between Original and Repositioned copy
   - Hover any changed line for the rationale (Strategic Resolve + 5 EBI)
   - Repositioned mode reveals human-imagery placeholders whose
     generation prompts copy to the clipboard
   Non-destructive: original nodes are kept and restored on toggle.
   ============================================================ */
(function () {
  'use strict';

  var METHOD = 'Rationale from Strategic Resolve (4-expert panel: brand strategy, consumer psychology, copywriting, growth) refined through 5 EBI passes.';
  var IMG_WHY = 'Human imagery added. The page needs room for real people and real moments to build emotional resonance. This is a placeholder holding the exact generation prompt: approve the placement and type, then copy the prompt into your image or video generator.';

  /* ---- generation-prompt building blocks (from the master style system) ---- */
  var CORE = 'Warm natural golden-hour light, soft diffused sunlight with a gentle backlit halo and subtle lens bloom, shallow depth of field, soft focus falloff, dappled light. Muted warm grade in a cream, sand and honey palette with charcoal and soft brown accents. Medium-format film aesthetic, fine organic grain, low contrast, calm and unhurried mood. Minimalist composition with generous negative space. Serene, present, intimate, tactile. Editorial wellness lifestyle. The subject wears the Pulse ring, a smooth wide polished gold band on the finger, present as a natural incidental detail, discovered rather than showcased, catching a soft glint of warm light. Avoid text, logos, harsh light, oversaturation, and clutter.';
  var PHOTO = 'Still photograph, single quiet candid moment, editorial magazine quality, tack-sharp on the eyes or hands with everything else in soft bokeh.';
  var VIDEO = 'Cinematic slow motion, 24fps, locked tripod or a slow gentle push-in, one continuous take with breathing-paced motion, loopable 6 to 10 seconds. Let the motion reveal the ring as the hand drifts into frame or turns toward the light.';
  function prompt(scene, kind) { return scene + '\n\n' + CORE + '\n\n' + (kind === 'VIDEO' ? VIDEO : PHOTO); }

  function ready(fn) {
    if (document.readyState === 'complete') fn();
    else window.addEventListener('load', function () { setTimeout(fn, 350); });
  }

  ready(function () {
    /* -------------------------------------------------- collect copy changes */
    var defs = [];
    function byText(sel, needle) {
      var list = document.querySelectorAll(sel);
      for (var i = 0; i < list.length; i++) {
        if ((list[i].textContent || '').trim().indexOf(needle) === 0 ||
            (list[i].textContent || '').indexOf(needle) > -1) return list[i];
      }
      return null;
    }
    function add(el, updHTML, updText, reason) {
      if (!el) return;
      // make sure any intro-animation opacity does not hide restored originals
      el.querySelectorAll('[style*="opacity"]').forEach(function (n) { n.style.opacity = '1'; });
      if (getComputedStyle(el).opacity === '0') el.style.opacity = '1';
      defs.push({ el: el, orig: Array.prototype.slice.call(el.childNodes), upd: updHTML, updText: updText, reason: reason });
    }

    add(document.querySelector('h1.hero-title'),
      'A million moments.<br>None of them missed.',
      'A million moments. None of them missed.',
      'Leads with a loss-framed relational hook instead of the abstract attribute “presence.” Anticipated regret is the strongest driver in identity purchases and opens the funnel well beyond the mindfulness core.');

    add(document.querySelector('p.paragraph-medium.intro'),
      'A gentle pulse on your finger brings you back to the present, right when the moment is happening. No screens, no scores, no noise.',
      'A gentle pulse on your finger brings you back to the present, right when the moment is happening. No screens, no scores, no noise.',
      'Reframes the mechanism as the payoff (being brought back when it matters) and promotes the anti-data, anti-noise wedge into the first impression.');

    add(byText('p', 'Become Calm, Focused'),
      'Be here for the moment you are in.',
      'Be here for the moment you are in.',
      'Trades a flat three-attribute line for a single relational close that points to the outcome rather than the state.');

    add(byText('h2', 'micro-pause'),
      'A million moments pass while we are somewhere else. One gentle pause brings you back.',
      'A million moments pass while we are somewhere else. One gentle pause brings you back.',
      'Applies the loss to agency sequence: open on the miss, resolve on the return. Never end on the wound.');

    var benefits = document.querySelectorAll('h2.heading-medium.text-grad-blue');
    if (benefits.length >= 4) {
      add(benefits[0], 'Carry less,<br>notice more', 'Carry less, notice more',
        'Moves the benefit heading from a clinical attribute to a felt outcome. The mechanism stays in the line beneath as proof.');
      add(benefits[1], 'Your best work<br>needs all of you', 'Your best work needs all of you',
        'Reframes focus as presence, not hustle. “All of you” carries a double meaning — your full attention and your whole self in the room — tying the focus benefit back to the ring. This exact line was refined through 5 dedicated EBI passes.');
      add(benefits[2], 'Be there for<br>the people you love', 'Be there for the people you love',
        'Territory A: the relational payoff, the deepest pull and the highest-intent buyer.');
      add(benefits[3], 'Feel the joy<br>already here', 'Feel the joy already here',
        'Gain frame to close the ladder warm, after the loss hook up top.');
    }

    add(document.querySelector('h2.text-grad-green'),
      'Every other device buzzes to pull you out. Pulse buzzes to bring you back.',
      'Every other device buzzes to pull you out. Pulse buzzes to bring you back.',
      'Sharpens the anti-notification wedge with enemy-framing: the attention economy is the villain, Pulse is the antidote.');

    add(byText('h2.heading-large', 'Be in your moment'),
      'Be here for the moment you are in. <span style="opacity:.55">Love is right here.</span>',
      'Be here for the moment you are in. Love is right here.',
      'Replaces the “Not in your thoughts” negation, which reads as cliché, with a positive relational close and a warm gain line.');

    /* -------------------------------------------------- media placeholders */
    function frag(html) { return document.createRange().createContextualFragment(html); }

    function card(kind, title, placeholder, scene) {
      var wrap = document.createElement('article');
      wrap.className = 'rp-card' + (kind === 'VIDEO' ? ' rp-card--wide' : '');

      var frame = document.createElement('div');
      frame.className = 'rp-card__frame';
      var badge = document.createElement('span');
      badge.className = 'rp-card__type' + (kind === 'VIDEO' ? ' is-video' : '');
      badge.textContent = kind;
      var ph = document.createElement('div');
      ph.className = 'rp-card__ph';
      var phb = document.createElement('b'); phb.textContent = title;
      ph.appendChild(phb);
      ph.appendChild(document.createTextNode(placeholder));
      frame.appendChild(badge); frame.appendChild(ph);

      var body = document.createElement('div');
      body.className = 'rp-card__body';
      var trow = document.createElement('div'); trow.className = 'rp-card__title';
      var tl = document.createElement('span'); tl.textContent = title;
      var why = document.createElement('span'); why.className = 'rp-card__why'; why.textContent = 'why?';
      why._rpReason = IMG_WHY; why._rpTag = 'Imagery';
      trow.appendChild(tl); trow.appendChild(why);

      var full = prompt(scene, kind);
      var pre = document.createElement('div'); pre.className = 'rp-card__prompt'; pre.textContent = full;

      var btn = document.createElement('button'); btn.className = 'rp-copy'; btn.type = 'button';
      btn.textContent = 'Copy ' + (kind === 'VIDEO' ? 'video' : 'photo') + ' prompt';
      btn.addEventListener('click', function () { copy(full, btn); });

      body.appendChild(trow); body.appendChild(pre); body.appendChild(btn);
      wrap.appendChild(frame); wrap.appendChild(body);
      return wrap;
    }

    function band(opts) {
      var sec = document.createElement('section');
      sec.className = 'rp-media rp-band' + (opts.cream ? ' rp-band--cream' : '');
      if (opts.head) {
        var head = document.createElement('div'); head.className = 'rp-band__head';
        if (opts.eyebrow) { var e = document.createElement('div'); e.className = 'rp-band__eyebrow'; e.textContent = opts.eyebrow; head.appendChild(e); }
        var t = document.createElement('h2'); t.className = 'rp-band__title'; t.textContent = opts.head; head.appendChild(t);
        if (opts.sub) { var s = document.createElement('div'); s.className = 'rp-band__sub'; s.textContent = opts.sub; head.appendChild(s); }
        sec.appendChild(head);
      }
      var grid = document.createElement('div');
      grid.className = 'rp-grid' + (opts.cards.length === 1 ? ' rp-grid--one' : '');
      opts.cards.forEach(function (c) { grid.appendChild(c); });
      sec.appendChild(grid);
      return sec;
    }

    var mediaBands = [];
    function place(afterEl, sec, before) {
      if (!afterEl || !sec) return;
      if (before) afterEl.parentNode.insertBefore(sec, afterEl);
      else afterEl.parentNode.insertBefore(sec, afterEl.nextSibling);
      mediaBands.push(sec);
    }

    // Band 1: "A million moments" gallery, after the micro-pause section
    var microH2 = byText('h2', 'micro-pause');
    var microSection = microH2 ? microH2.closest('section') : null;
    place(microSection, band({
      head: 'A million moments', eyebrow: 'The ones we are somewhere else for',
      sub: 'Small, ordinary, recoverable. One gentle pause brings you back.',
      cards: [
        card('PHOTO', 'The drawing', 'Child shows a crayon drawing; a parent looks up and truly sees it.',
          'A young child holds up a crayon drawing toward a parent who has just looked up from a task and is truly seeing it, warm kitchen window light, the child proud, the parent softening.'),
        card('PHOTO', 'The small hand', 'A toddler’s hand closing around one finger.',
          'Extreme close macro of a toddler’s small hand closing around one adult finger, warm skin tones, soft window light, tender and quiet.'),
        card('PHOTO', 'Mid-story', 'A partner mid-story; the listener meets their eyes.',
          'A partner mid-story at a sunlit dinner table, the listener leaning in and meeting their eyes, two coffee cups, relaxed and intimate.')
      ]
    }));

    // Band 2: father + child, full-width video, after the Benefits section
    var benefitSection = benefits.length ? benefits[0].closest('section') : null;
    place(benefitSection, band({
      cream: true,
      head: 'Present with your kids', eyebrow: 'Relational moment',
      cards: [
        card('VIDEO', 'Golden-hour swing', 'A father watches his child’s face swing toward him.',
          'A father pushing his young child on a swing at golden hour, watching the child’s laughing face swing toward the camera, warm backlight and floating dust, both fully present.')
      ]
    }));

    // Band 3: partner moment, photo, before the closing line
    var closingH2 = byText('h2.heading-large', 'Be in your moment') || byText('h2', 'Be here for the moment');
    var closingSection = closingH2 ? closingH2.closest('section') : null;
    place(closingSection, band({
      head: 'Present with your partner', eyebrow: 'Relational moment',
      cards: [
        card('PHOTO', 'Morning close', 'Two partners close in soft morning light.',
          'Two partners close together on a sofa in soft morning light, foreheads nearly touching, one hand resting over the other, calm and unhurried.')
      ]
    }), true);

    /* -------------------------------------------------- tooltip */
    var tip = document.createElement('div'); tip.id = 'rp-tip';
    var tipTag = document.createElement('span'); tipTag.className = 'rp-tip-tag';
    var tipWhy = document.createElement('p'); tipWhy.className = 'rp-tip-why';
    var tipPrev = document.createElement('p'); tipPrev.className = 'rp-tip-preview';
    var tipMethod = document.createElement('p'); tipMethod.className = 'rp-tip-method';
    tip.appendChild(tipTag); tip.appendChild(tipWhy); tip.appendChild(tipPrev); tip.appendChild(tipMethod);
    document.body.appendChild(tip);

    function showTip(e, tag, why, preview, method) {
      tipTag.textContent = tag;
      tipWhy.textContent = why;
      if (preview) { tipPrev.style.display = ''; tipPrev.textContent = preview; }
      else tipPrev.style.display = 'none';
      if (method) { tipMethod.style.display = ''; tipMethod.textContent = method; }
      else tipMethod.style.display = 'none';
      tip.classList.add('rp-show');
      moveTip(e);
    }
    function moveTip(e) {
      var pad = 16, w = tip.offsetWidth, h = tip.offsetHeight;
      var x = e.clientX + pad, y = e.clientY + pad;
      if (x + w + 8 > window.innerWidth) x = e.clientX - w - pad;
      if (y + h + 8 > window.innerHeight) y = e.clientY - h - pad;
      tip.style.left = Math.max(8, x) + 'px';
      tip.style.top = Math.max(8, y) + 'px';
    }
    function hideTip() { tip.classList.remove('rp-show'); }

    // copy-change hover handlers (bound to the persistent element)
    defs.forEach(function (d) {
      d.el.addEventListener('mouseenter', function (e) {
        var repositioned = document.body.classList.contains('rp-mode-updated');
        if (repositioned)
          showTip(e, 'Repositioned', d.reason, null, METHOD);
        else
          showTip(e, 'Becomes', d.reason, '“' + d.updText + '”', METHOD);
      });
      d.el.addEventListener('mousemove', moveTip);
      d.el.addEventListener('mouseleave', hideTip);
    });
    // imagery "why?" hover
    document.querySelectorAll('.rp-card__why').forEach(function (w) {
      w.addEventListener('mouseenter', function (e) { showTip(e, w._rpTag, w._rpReason, null, null); });
      w.addEventListener('mousemove', moveTip);
      w.addEventListener('mouseleave', hideTip);
    });

    /* -------------------------------------------------- copy helper */
    function copy(text, btn) {
      function done() {
        var o = btn.textContent; btn.classList.add('rp-copied'); btn.textContent = 'Copied to clipboard';
        setTimeout(function () { btn.textContent = o; btn.classList.remove('rp-copied'); }, 1600);
      }
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(done).catch(function () { fallback(text, done); });
      } else fallback(text, done);
    }
    function fallback(text, done) {
      var ta = document.createElement('textarea'); ta.value = text;
      ta.style.position = 'fixed'; ta.style.opacity = '0'; document.body.appendChild(ta);
      ta.focus(); ta.select();
      try { document.execCommand('copy'); } catch (e) {}
      ta.remove(); done();
    }

    /* -------------------------------------------------- apply mode */
    function apply(mode) {
      var updated = mode === 'updated';
      defs.forEach(function (d) {
        if (updated) { d.el.replaceChildren(frag(d.upd)); d.el.classList.add('rp-changed'); }
        else { d.el.replaceChildren.apply(d.el, d.orig); d.el.classList.remove('rp-changed'); }
      });
      mediaBands.forEach(function (b) { b.style.display = updated ? 'block' : 'none'; });
      document.body.classList.toggle('rp-mode-updated', updated);
      btnOrig.classList.toggle('rp-on', !updated);
      btnNew.classList.toggle('rp-on', updated);
      toggle.classList.toggle('rp-updated', updated);
      try { localStorage.setItem('rp-mode', mode); } catch (e) {}
      if (window.ScrollTrigger) { try { window.ScrollTrigger.refresh(); } catch (e) {} }
    }

    /* -------------------------------------------------- toggle UI */
    var toggle = document.createElement('div'); toggle.id = 'rp-toggle';
    var sw = document.createElement('div'); sw.className = 'rp-switch';
    var lab = document.createElement('span'); lab.className = 'rp-lab'; lab.textContent = 'Positioning';
    var btnOrig = document.createElement('button'); btnOrig.type = 'button'; btnOrig.textContent = 'Original';
    var btnNew = document.createElement('button'); btnNew.type = 'button'; btnNew.textContent = 'Repositioned';
    sw.appendChild(lab); sw.appendChild(btnOrig); sw.appendChild(btnNew);
    var hint = document.createElement('div'); hint.className = 'rp-hint'; hint.textContent = 'Hover highlighted copy to see why it changed';
    toggle.appendChild(sw); toggle.appendChild(hint);
    document.body.appendChild(toggle);

    btnOrig.addEventListener('click', function () { apply('original'); });
    btnNew.addEventListener('click', function () { apply('updated'); });

    var saved = 'original';
    try { saved = localStorage.getItem('rp-mode') || 'original'; } catch (e) {}
    apply(saved);
  });
})();
