/* ============================================================
   Pulse Mindfulness — interactions
   ============================================================ */

/* ---------- nav colour flip on scroll ---------- */
const nav = document.getElementById('nav');
const hero = document.querySelector('.hero');
const flip = () => {
  const past = window.scrollY > (hero ? hero.offsetHeight - 90 : 500);
  nav.classList.toggle('is-light', past);
};
window.addEventListener('scroll', flip, { passive: true });
flip();

/* ---------- slide-out menu ---------- */
const menu = document.getElementById('menu');
document.getElementById('burger').addEventListener('click', () => menu.classList.add('is-open'));
document.getElementById('menuClose').addEventListener('click', () => menu.classList.remove('is-open'));
menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => menu.classList.remove('is-open')));

/* ---------- expert drag slider ---------- */
const track = document.getElementById('expertTrack');
if (track) {
  let down = false, startX, scrollStart;
  track.addEventListener('mousedown', e => {
    down = true; track.classList.add('is-dragging');
    startX = e.pageX; scrollStart = track.scrollLeft;
  });
  window.addEventListener('mouseup', () => { down = false; track.classList.remove('is-dragging'); });
  window.addEventListener('mousemove', e => {
    if (!down) return;
    e.preventDefault();
    track.scrollLeft = scrollStart - (e.pageX - startX) * 1.4;
  });
  const dots = document.querySelectorAll('.experts__nav .dot');
  track.addEventListener('scroll', () => {
    const pct = track.scrollLeft / (track.scrollWidth - track.clientWidth || 1);
    const active = Math.round(pct * (dots.length - 1));
    dots.forEach((d, i) => d.classList.toggle('is-active', i === active));
  }, { passive: true });
  dots.forEach((d, i) => d.addEventListener('click', () => {
    track.scrollTo({ left: (track.scrollWidth - track.clientWidth) * (i / (dots.length - 1)), behavior: 'smooth' });
  }));
}

/* ---------- app feature switcher ---------- */
const appMenu = document.getElementById('appMenu');
if (appMenu) {
  const img = document.getElementById('appImg');
  const modeTitle = document.getElementById('appModeTitle');
  const body = document.getElementById('appBody');
  appMenu.querySelectorAll('li').forEach(li => {
    li.addEventListener('click', () => {
      appMenu.querySelector('.is-active')?.classList.remove('is-active');
      li.classList.add('is-active');
      img.src = li.dataset.img;
      modeTitle.textContent = li.dataset.title;
      body.textContent = li.dataset.body;
    });
  });
}

/* ---------- community review cards ---------- */
const REV_BASE = 'https://cdn.prod.website-files.com/6a06cb8e0574c88f0f7db097/';
const reviews = [
  { cover: '6a21af45e5609e76d1168dab_jon-prince-cover.webp', ava: '6a21aeb4daa2f7d4ac5f80f7_testimonials-ava-j.svg',
    quote: '“After the vibration I returned to really being there with my son.”', name: 'John Prince', role: 'Customer Review' },
  { cover: '6a293f2042dfc33f68c3432b_ben-cover.png', ava: '6a21999e6efdeab30196bcc4_testimonials-ava-b.svg',
    quote: '“It keeps me grounded throughout the day.”', name: 'Ben', role: 'Customer Review' },
  { cover: '6a21b1bc312d2a656434b374_michal-cover.webp', ava: '6a21b0eb54745e2fad39b705_testimonials-ava-m.svg',
    quote: '“In the first week I noticed I stopped reaching for my phone during deep work.”', name: 'Michal W.', role: 'Customer Review' },
  { cover: '6a2829ed123864bd903c9915_bela-cover.webp', ava: '6a28295eb1fdc901d730af2a_testimonials-ava-b.svg',
    quote: '“Pulse has changed how I move through my workdays.”', name: 'Bela', role: 'Client Review' },
  { cover: '6a21ae40b0010c2190a23ac2_daniel-cover.webp', ava: '6a21ae14fc2d173e473c2e64_testimonials-ava-d.svg',
    quote: '“Pulse helps me slow down, be present, and appreciate the moment I’m in.”', name: 'Daniel', role: 'Customer Review' },
  { cover: '6a21afaf9522034c0abf6b09_jonny-v-cover.webp', ava: '6a06d060ff8637c48bec1558_testimonials-ava-ad.svg',
    quote: '“Pulse brings me back into the moment.”', name: 'Jonny V.', role: 'Customer Review' },
  { cover: '6a21b0d17eb475bfd293469d_maja-cover.webp', ava: '6a21b0eb54745e2fad39b705_testimonials-ava-m.svg',
    quote: '“It feels like the missing puzzle piece in my personal development journey.”', name: 'Maja S.', role: 'Customer Review' },
  { cover: '6a21985d9a0c51bac1b5778e_alice-review.webp', ava: '6a21984bf43673988f0ec91e_testimonials-ava-a.svg',
    quote: '“Slowly started to build a bigger level of awareness.”', name: 'Alice', role: 'Customer Review' },
  { cover: '6a2198e935a9ae12faa3dc27_andy-d-cover.webp', ava: '6a06d060ff8637c48bec1558_testimonials-ava-ad.svg',
    quote: '“Just a tiny mental-health snack for me 😊”', name: 'Andy D.', role: 'Customer Review' },
  { cover: '6a282961c1e809d462464ba6_bhavna-ram-cover.webp', ava: '6a21999e6efdeab30196bcc4_testimonials-ava-b.svg',
    quote: '“A gentle nudge back to the present moment, even on the busiest days.”', name: 'Bhavna Ram', role: 'Client Review' },
  { cover: '6a21ac9e5f84b0b2c3072db5_calvin-cover.webp', ava: '6a21acefb23d113bef007bca_testimonials-ava-c.svg',
    quote: '“Pulse helps me feel more in control of my attention and my time.”', name: 'Calvin', role: 'Customer Review' },
  { cover: '6a2321583037413ae60cbc81_julia.webp', ava: '6a21b0eb54745e2fad39b705_testimonials-ava-m.svg',
    quote: '“Pulse has transformed the way I experience presence.”', name: 'Julia', role: 'Customer Review' },
];

const el = (tag, cls, text) => {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (text != null) n.textContent = text;
  return n;
};

const row = document.getElementById('reviewRow');
if (row) {
  reviews.forEach(r => {
    const card = el('article', 'rcard');

    const cover = el('div', 'rcard__cover');
    const coverImg = el('img');
    coverImg.src = REV_BASE + r.cover; coverImg.alt = r.name; coverImg.loading = 'lazy';
    const play = el('span', 'rcard__play'); play.textContent = '►';
    cover.append(coverImg, play);

    const body = el('div', 'rcard__body');
    body.append(
      el('div', 'rcard__stars', '★★★★★'),
      el('p', 'rcard__quote', r.quote)
    );

    const meta = el('div', 'rcard__meta');
    const ava = el('img', 'rcard__ava'); ava.src = REV_BASE + r.ava; ava.alt = '';
    const who = el('div');
    who.append(el('div', 'rcard__name', r.name), el('div', 'rcard__role', r.role));
    meta.append(ava, who);
    body.append(meta);

    card.append(cover, body);
    row.append(card);
  });
}
