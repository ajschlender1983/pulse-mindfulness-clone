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
    function add(el, updHTML, updText, reason, conn) {
      if (!el) return;
      // make sure any intro-animation opacity does not hide restored originals
      el.querySelectorAll('[style*="opacity"]').forEach(function (n) { n.style.opacity = '1'; });
      if (getComputedStyle(el).opacity === '0') el.style.opacity = '1';
      conn = conn || {};
      defs.push({ el: el, orig: Array.prototype.slice.call(el.childNodes),
        upd: updHTML, updText: updText, reason: reason,
        conn: conn.html || updHTML, connText: conn.text || updText, connReason: conn.reason || reason });
    }

    add(document.querySelector('h1.hero-title'),
      'A million moments.<br>Don’t miss this one.',
      'A million moments. Don’t miss this one.',
      'Leads with a loss-framed relational hook instead of the abstract attribute “presence.” “A million moments” becomes the ownable signature; the turn to “this one” makes the stakes concrete.',
      { html: 'Come back<br>to each other.', text: 'Come back to each other.',
        reason: 'Connection state: leads we-centric. Names the drift between people and the way back to each other, not just back to the moment.' });

    add(document.querySelector('p.paragraph-medium.intro'),
      'A gentle pulse brings you back to the present. No screens, no scores, no noise.',
      'A gentle pulse brings you back to the present. No screens, no scores, no noise.',
      'Tightened: drops the redundant time-stamp, keeps the mechanism and the anti-noise wedge in one clean line.',
      { html: 'A gentle pulse brings you back to the person in front of you. Send one to someone far away, and you are present together.',
        text: 'A gentle pulse brings you back to the person in front of you. Send one to someone far away, and you are present together.',
        reason: 'Introduces the shared mechanism: couples mode and a vibration you can send, so presence becomes something two people feel at the same time.' });

    add(byText('p', 'Become Calm, Focused'),
      'Be here for it.',
      'Be here for it.',
      'Cut to the shortest possible relational tag, and it frees “be here for the moment you are in” so it is not echoed at the close.',
      { html: 'You are not in this alone.', text: 'You are not in this alone.',
        reason: 'Anti-isolation tag: the we-centric turn, aimed at the loneliness that is the real pain under “connection.”' });

    add(byText('h2', 'micro-pause'),
      'So much passes while we’re somewhere else. One pulse brings you back.',
      'So much passes while we’re somewhere else. One pulse brings you back.',
      'Loss to agency sequence, de-duplicated: “a million moments” now lives only in the hero so it stays an ownable signature.',
      { html: 'We are all somewhere else, together and alone. One pulse brings us back to each other.',
        text: 'We are all somewhere else, together and alone. One pulse brings us back to each other.',
        reason: 'Collective loss-to-agency: names the shared drift and the shared return, moving me to we.' });

    var benefits = document.querySelectorAll('h2.heading-medium.text-grad-blue');
    if (benefits.length >= 4) {
      add(benefits[0], 'Carry less,<br>notice more', 'Carry less, notice more',
        'Moves the benefit heading from a clinical attribute to a felt outcome. The mechanism stays in the line beneath as proof.',
        { html: 'Feel less<br>alone', text: 'Feel less alone', reason: 'Reframes the calm benefit as the relief of loneliness, the real pain under connection.' });
      add(benefits[1], 'Your best work<br>needs all of you', 'Your best work needs all of you',
        'Reframes focus as presence, not hustle. “All of you” carries a double meaning — your full attention and your whole self in the room — tying the focus benefit back to the ring. This exact line was refined through 5 dedicated EBI passes.',
        { html: 'Be all the way<br>here for them', text: 'Be all the way here for them', reason: 'Focus reframed toward being fully with your people, not just your own work.' });
      add(benefits[2], 'Be there for<br>the people you love', 'Be there for the people you love',
        'Territory A: the relational payoff, the deepest pull and the highest-intent buyer.',
        { html: 'Come back to<br>the ones you love', text: 'Come back to the ones you love', reason: 'The relational core, said as a return to each other.' });
      add(benefits[3], 'The joy is<br>already here', 'The joy is already here',
        'Gain frame to close the benefit ladder warm. It sets up the closing line, where “here” blossoms into more than joy.',
        { html: 'Feel each<br>other again', text: 'Feel each other again', reason: 'Joy reframed as a shared feeling between people, the we-centric gain.' });
    }

    add(document.querySelector('h2.text-grad-green'),
      'Other devices pull you away. Pulse brings you back.',
      'Other devices pull you away. Pulse brings you back.',
      'The anti-notification wedge, tightened to its cleanest contrast: the attention economy pulls you away, Pulse pulls you back.',
      { html: 'Other devices pull you apart. Pulse brings you back to each other.',
        text: 'Other devices pull you apart. Pulse brings you back to each other.',
        reason: 'The anti-notification wedge with the connection twist: the attention economy pulls people apart, Pulse brings them back to each other.' });

    add(byText('h2.heading-large', 'Be in your moment'),
      '<span class="rp-cycle"><span class="rp-cycle__w">joy</span></span><br>is right here',
      'Joy is right here.',
      'The closing gain line. The first word cycles slowly and softly through joy, love, family, purpose, and pleasure, so the brand quietly claims all of them as things that are already here.');

    /* -------------------------------------------------- media placeholders */
    function frag(html) { return document.createRange().createContextualFragment(html); }

    function card(kind, title, placeholder, scene, dims) {
      var wrap = document.createElement('article');
      wrap.className = 'rp-card' + (kind === 'VIDEO' ? ' rp-card--wide' : '');

      var frame = document.createElement('div');
      frame.className = 'rp-card__frame';
      var badge = document.createElement('span');
      badge.className = 'rp-card__type' + (kind === 'VIDEO' ? ' is-video' : '');
      badge.textContent = kind;
      var dchip = document.createElement('span');
      dchip.className = 'rp-card__dims'; dchip.textContent = dims;
      var ph = document.createElement('div');
      ph.className = 'rp-card__ph';
      var phb = document.createElement('b'); phb.textContent = title;
      ph.appendChild(phb);
      ph.appendChild(document.createTextNode(placeholder));
      frame.appendChild(badge); frame.appendChild(dchip); frame.appendChild(ph);

      var body = document.createElement('div');
      body.className = 'rp-card__body';
      var trow = document.createElement('div'); trow.className = 'rp-card__title';
      var tl = document.createElement('span'); tl.textContent = title;
      var why = document.createElement('span'); why.className = 'rp-card__why'; why.textContent = 'why?';
      why._rpReason = IMG_WHY; why._rpTag = 'Imagery';
      trow.appendChild(tl); trow.appendChild(why);

      // include the dimensions in the copyable prompt itself
      var fmt = dims.replace(/ · /g, ', ').replace(/×/g, 'x');
      var full = prompt(scene, kind) + '\n\nFormat: ' + fmt + '.';

      // real, selectable field so the prompt can always be copied (button or manual select)
      var ta = document.createElement('textarea');
      ta.className = 'rp-card__prompt'; ta.readOnly = true; ta.rows = 6;
      ta.setAttribute('spellcheck', 'false'); ta.value = full;
      ta.addEventListener('focus', function () { ta.select(); });
      ta.addEventListener('click', function () { ta.select(); });

      var btn = document.createElement('button'); btn.className = 'rp-copy'; btn.type = 'button';
      btn.textContent = 'Copy ' + (kind === 'VIDEO' ? 'video' : 'photo') + ' prompt';
      btn._label = btn.textContent;
      btn.addEventListener('click', function () { copyFromField(ta, btn); });

      body.appendChild(trow); body.appendChild(ta); body.appendChild(btn);
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

    // Connection state: a "presence you feel together" band, shown only in Connection mode
    var connBands = [];
    (function () {
      var closeH2 = byText('h2.heading-large', 'Be in your moment') || byText('h2', 'Be here for the moment');
      var closeSec = closeH2 ? closeH2.closest('section') : null;
      if (!closeSec) return;
      var sec = document.createElement('section');
      sec.className = 'rp-media rp-band rp-connband';
      var head = document.createElement('div'); head.className = 'rp-band__head';
      var e = document.createElement('div'); e.className = 'rp-band__eyebrow'; e.textContent = 'Presence you feel together';
      var t = document.createElement('h2'); t.className = 'rp-band__title'; t.textContent = 'Connection is right here.';
      var s = document.createElement('div'); s.className = 'rp-band__sub'; s.textContent = 'Quiet by design. Once a day, so it stays a signal and never noise.';
      head.appendChild(e); head.appendChild(t); head.appendChild(s); sec.appendChild(head);
      var grid = document.createElement('div'); grid.className = 'rp-grid';
      [['Couples mode', 'Two rings, one pulse. You and your person feel the same gentle moment at the same time, wherever you are.'],
       ['A vibration you can send', 'Send one quiet pulse to someone you love. A secret “I am thinking of you,” felt on their finger, once a day.'],
       ['A moment, together', 'Once in a while, everyone wearing Pulse feels it at once. A breath, a thank-you, a hug for whoever is beside you. You are not alone in it.']
      ].forEach(function (p) {
        var c = document.createElement('article'); c.className = 'rp-feat';
        var h = document.createElement('h3'); h.textContent = p[0];
        var d = document.createElement('p'); d.textContent = p[1];
        c.appendChild(h); c.appendChild(d); grid.appendChild(c);
      });
      sec.appendChild(grid);
      closeSec.parentNode.insertBefore(sec, closeSec);
      connBands.push(sec);
    })();

    // Band 1: "A million moments" gallery, after the micro-pause section
    var microH2 = byText('h2', 'micro-pause');
    var microSection = microH2 ? microH2.closest('section') : null;
    place(microSection, band({
      head: 'A million moments', eyebrow: 'The ones we are somewhere else for',
      sub: 'Small, ordinary, recoverable. One gentle pause brings you back.',
      cards: [
        card('PHOTO', 'The drawing', 'Child shows a crayon drawing; a parent looks up and truly sees it.',
          'A young child holds up a crayon drawing toward a parent who has just looked up from a task and is truly seeing it, warm kitchen window light, the child proud, the parent softening.',
          'Portrait · 4:5 · 1600 × 2000px'),
        card('PHOTO', 'The small hand', 'A toddler’s hand closing around one finger.',
          'Extreme close macro of a toddler’s small hand closing around one adult finger, warm skin tones, soft window light, tender and quiet.',
          'Portrait · 4:5 · 1600 × 2000px'),
        card('PHOTO', 'Mid-story', 'A partner mid-story; the listener meets their eyes.',
          'A partner mid-story at a sunlit dinner table, the listener leaning in and meeting their eyes, two coffee cups, relaxed and intimate.',
          'Portrait · 4:5 · 1600 × 2000px')
      ]
    }));

    // Band 2: father + child, full-width video, after the Benefits section
    var benefitSection = benefits.length ? benefits[0].closest('section') : null;
    place(benefitSection, band({
      cream: true,
      head: 'Present with your kids', eyebrow: 'Relational moment',
      cards: [
        card('VIDEO', 'Golden-hour swing', 'A father watches his child’s face swing toward him.',
          'A father pushing his young child on a swing at golden hour, watching the child’s laughing face swing toward the camera, warm backlight and floating dust, both fully present.',
          'Landscape · 16:9 · 1920 × 1080px · 6–10s loop')
      ]
    }));

    // Band 3: partner moment, photo, before the closing line
    var closingH2 = byText('h2.heading-large', 'Be in your moment') || byText('h2', 'Be here for the moment');
    var closingSection = closingH2 ? closingH2.closest('section') : null;
    place(closingSection, band({
      head: 'Present with your partner', eyebrow: 'Relational moment',
      cards: [
        card('PHOTO', 'Morning close', 'Two partners close in soft morning light.',
          'Two partners close together on a sofa in soft morning light, foreheads nearly touching, one hand resting over the other, calm and unhurried.',
          'Portrait · 4:5 · 1600 × 2000px')
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
        var m = document.body.getAttribute('data-rp-mode');
        if (m === 'connection')
          showTip(e, 'Connection', d.connReason, null, METHOD);
        else if (m === 'updated')
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
    function copyFromField(ta, btn) {
      var done = function () {
        btn.classList.add('rp-copied'); btn.textContent = 'Copied to clipboard';
        setTimeout(function () { btn.textContent = btn._label; btn.classList.remove('rp-copied'); }, 1600);
      };
      // select the visible field first: gives feedback and a manual-copy fallback
      ta.focus(); ta.select();
      try { ta.setSelectionRange(0, ta.value.length); } catch (e) {}
      var okExec = false;
      try { okExec = document.execCommand('copy'); } catch (e) {}
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(ta.value).then(done, function () { done(); });
      } else { done(); }
      if (okExec) done();
    }
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

    /* -------------------------------------------------- cycling closing word
       Only the first word changes. Slow, soft, easy: a long dwell with a slow
       blur/fade cross-transition. Edit CYCLE_WORDS or the timings to taste. */
    var CYCLE_WORDS = ['joy', 'love', 'family', 'purpose', 'pleasure'];
    var CYCLE_HOLD = 4600;   // ms a word stays before it begins fading out
    var CYCLE_GAP = 1600;    // ms of empty space between fade-out and next fade-in
    var cycleTimers = [];
    function stopCycle() { cycleTimers.forEach(clearTimeout); cycleTimers = []; }
    function startCycle() {
      stopCycle();
      var w = document.querySelector('.rp-cycle__w');
      if (!w) return;
      var i = 0;
      w.classList.remove('rp-vis');
      function step() {
        w.textContent = CYCLE_WORDS[i];
        requestAnimationFrame(function () { requestAnimationFrame(function () { w.classList.add('rp-vis'); }); });
        cycleTimers.push(setTimeout(function () {
          w.classList.remove('rp-vis');
          cycleTimers.push(setTimeout(function () {
            i = (i + 1) % CYCLE_WORDS.length;
            step();
          }, CYCLE_GAP));
        }, CYCLE_HOLD));
      }
      step();
    }

    /* -------------------------------------------------- apply mode */
    function apply(mode) {
      var changed = (mode === 'updated' || mode === 'connection');
      defs.forEach(function (d) {
        if (mode === 'connection') { d.el.replaceChildren(frag(d.conn)); d.el.classList.add('rp-changed'); }
        else if (mode === 'updated') { d.el.replaceChildren(frag(d.upd)); d.el.classList.add('rp-changed'); }
        else { d.el.replaceChildren.apply(d.el, d.orig); d.el.classList.remove('rp-changed'); }
      });
      mediaBands.forEach(function (b) { b.style.display = changed ? 'block' : 'none'; });
      connBands.forEach(function (b) { b.style.display = (mode === 'connection') ? 'block' : 'none'; });
      document.body.classList.toggle('rp-mode-updated', changed);
      document.body.setAttribute('data-rp-mode', mode);
      btnOrig.classList.toggle('rp-on', mode === 'original');
      btnNew.classList.toggle('rp-on', mode === 'updated');
      btnConn.classList.toggle('rp-on', mode === 'connection');
      toggle.classList.toggle('rp-updated', changed);
      try { localStorage.setItem('rp-mode', mode); } catch (e) {}
      if (changed) startCycle(); else stopCycle();
      if (window.ScrollTrigger) { try { window.ScrollTrigger.refresh(); } catch (e) {} }
    }

    /* -------------------------------------------------- toggle UI */
    var toggle = document.createElement('div'); toggle.id = 'rp-toggle';
    var sw = document.createElement('div'); sw.className = 'rp-switch';
    var lab = document.createElement('span'); lab.className = 'rp-lab'; lab.textContent = 'Positioning';
    var btnOrig = document.createElement('button'); btnOrig.type = 'button'; btnOrig.textContent = 'Original';
    var btnNew = document.createElement('button'); btnNew.type = 'button'; btnNew.textContent = 'Repositioned';
    var btnConn = document.createElement('button'); btnConn.type = 'button'; btnConn.textContent = 'Connection';
    sw.appendChild(lab); sw.appendChild(btnOrig); sw.appendChild(btnNew); sw.appendChild(btnConn);
    var hint = document.createElement('div'); hint.className = 'rp-hint'; hint.textContent = 'Hover highlighted copy to see why it changed';
    toggle.appendChild(sw); toggle.appendChild(hint);
    document.body.appendChild(toggle);

    btnOrig.addEventListener('click', function () { apply('original'); });
    btnNew.addEventListener('click', function () { apply('updated'); });
    btnConn.addEventListener('click', function () { apply('connection'); });

    var saved = 'original';
    try { saved = localStorage.getItem('rp-mode') || 'original'; } catch (e) {}
    apply(saved);
  });
})();
