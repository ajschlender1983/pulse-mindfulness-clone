# Pulse Cadence — Build Spec (synthesis of expert consults)

Adaptation of OPUS Voice Flows → Pulse Mindfulness. Exact functional copy of the
flow-map app + email library, rebranded and re-contented for the Pulse ring.

Source app: `/Users/adamschlenderwork/dev/opus-os/projects/opus-pulse/public/opus-voice-flow-map.html`
Source assets: `/Users/adamschlenderwork/dev/opus-os/projects/voice-assets/public/`
Target repo: this repo (`PulseMindfulness-Clone`), branch `agent/presence-voice-flows`.

## Product truth (non-negotiable)

- The Pulse ring: smooth, wide, polished gold band. Vibrates a few times an hour
  to bring the wearer back to the present moment.
- **Anti-data wedge is the brand spine**: no tracking, no scores, no metrics,
  no streaks, nothing to check. The app exists only to set vibration patterns,
  windows, and intention ("Smart without phone"). The ring never reports wear.
  → NO email may reference wear detection, pulses-received counts, streak
  numbers, leaderboards, or "your data."
- Measurement spine = the **presence quiz** (self-reported, re-takeable).
  Results are "a reclaimable number + a kind archetype, never a grade. Hope
  always leads; the gap is grey subtext."
- Lifecycle triggers must be engagement-based (email opens, app opens, quiz
  re-takes, replies) or time-based — never ring-telemetry-based.
- Persona: Maya, 38, charge nurse, mother of Priya (~6). Journey: Numb → Seen →
  Hopeful → Convinced → Relieved → Grateful → Generous.
- Gifting is a first-class wedge ("gift Pulse to the exact person they named in
  the quiz, so love becomes the referral").
- Nurture logic: ① the plan ② the moment you're missing ③ how a gentle pulse
  works (price once, calm, anchored to reclaimed life) → product page →
  Cost-of-the-Gap at CTA. Never sell during Seen.

## Naming

- Flow-map app: **Cadence** ("Pulse — Cadence"). Never "Journey" (collides with
  Pulse Journeys, a live in-app product name).
- Weekly release: **The Sunday Pause** (flow id `sunday-pause`). Subject pattern
  "The Sunday Pause — [theme]".
- Advocate circle: **The First Hundred**. Community: **the Presence Circle**.
- Senders: personal = "Elias from Pulse" <elias@pulsemindfulness.com>;
  transactional = "Pulse" <hello@pulsemindfulness.com>, Reply-To
  care@pulsemindfulness.com. Never no-reply.

## File layout (target repo root)

```
presence-flows.html      ← the Cadence app (port of opus-voice-flow-map.html)
emails/                  ← all email/sms/call/social/form/landing assets
email-images/            ← Gemini-generated heroes, <slug>.png
tools/generate-email-images.py   ← manifest-driven generator
flows/BUILD-SPEC.md      ← this file
```

assetRefs in SEEDED_FLOWS use relative paths `emails/<file>.html` (served from
repo root via python3 -m http.server 8842). Funnel links: `index.html`,
`presence-quiz.html`, `presence-experience.html` (repo root).

## Design tokens — Cadence app (cream editorial; replaces OPUS dark)

```css
--bg:#EBE7D4; --dark:#1A1C22; --accent:#E3F47D (always w/ #101828 text);
--midtone:#8a8578; --light:#F9F6E5; --ink:#1A1C22; --brown:#423D32;
--honey:#C9A227; --line:rgba(26,28,34,.09); --canvas-dot:#ddd7c3;
--shadow:0 12px 30px rgba(66,61,50,.08);
font: DM Sans; labels/pills: DM Mono 11px;
```

- Cards `--light` on `--bg`, radius 14–16px, `--shadow`. No glow, no neon.
- One dark surface: top app bar in `--ink` with lime logo dot.
- Connectors `--line` 1.5px; selected path `--honey`.

Channels: Email `#C9A227` · SMS `#7FA0B4` · Phone `#B0764F` · Website `#565D6E`
· Social `#97A93B`.

Phases (chip bg = 18% tint on cream, text = full value — the ramp IS the info):
Numb `#93A5B1` · Seen `#A3A493` · Hopeful `#B3A379` · Convinced `#C0A45D` ·
Relieved `#CCA94C` · Grateful `#D6AC3E` · Generous `#E0B036` (+1px #E3F47D ring).

Status: draft = bg `#E4DFC9` text `#6E6857` dashed `#c9c3ae`; in_review = bg
`rgba(201,162,39,.16)` text `#8A6D14`; approved = bg `#E3F47D` text `#101828`.

```js
var PRESENCE_SCORES = { Numb:0, Seen:15, Hopeful:30, Convinced:55, Relieved:75, Grateful:100, Generous:120 };
```

Audience pills (AUD_DEFS replacement):

| id | label | color / bg |
|---|---|---|
| quiz-lead | Quiz Lead | text #45606F / bg rgba(179,199,211,.35) |
| browser | Browser | text #565D6E / bg rgba(86,93,110,.12) |
| new-owner | New Owner | text #7A5B18 / bg rgba(201,162,39,.14) |
| owner | Owner | text #55611E / bg rgba(151,169,59,.16) |
| gift-giver | Gift Giver | text #8A6D14 / bg rgba(224,176,54,.16) |
| gift-recipient | Gift Recipient | text #6E8494 / bg rgba(127,160,180,.18) |
| lapsed | Lapsed | text #6E6857 / bg rgba(138,133,120,.16) |
| partner | Partner | text #45606F / bg rgba(69,96,111,.12) |

## Email design system

Cream "letter" template (default, human world) and dark "luxe" variant (product
world). **Decision rule: hero = Maya → cream; hero = the ring → dark.**
Arrival-day email is the deliberate crossover (cream template, product-in-life
hero). Full CSS values in flows/consult-brand.md (§1). Hero: 3:2 inset rounded
card (radius 16px) inside 640px letter card; dark variant may run 16:9
full-bleed. Lime pill CTA, max one per email. No exclamation points. Every email
contains one written 10-second pause ("Here, actually: ten seconds…").

Voice rules: present tense second person; one breath per sentence; invite never
instruct ("you may notice", never "you will feel"); concrete over cosmic (ban
journey/transform/unlock/elevate); no urgency/scarcity/countdown.

## Flows (8) — 60 touchpoints

Full touchpoint tables with day/channel/title/phase/intent/criteria: see
flows/consult-sage.md. Flow list:

1. `awakening` — Awakening Flow (quiz→purchase nurture; 11 tp; Numb→Convinced)
2. `true-fit` — True Fit Flow (order→confirmed fit, sizing fork + gift-giver; 6 tp)
3. `arrival` — Arrival Flow (ship→unbox→charge/pair→first pulse; 6 tp)
4. `first-25` — First 25 Days Flow (habit building, Day-4 fork; 12 tp)
5. `sunday-pause` — The Sunday Pause (weekly theme + lapse win-back; 5 tp)
6. `ripple` — Ripple Flow (review→referral→gift; 7 tp)
7. `inner-circle` — Inner Circle Flow (advocates, The First Hundred; 6 tp)
8. `spaces` — Spaces Flow (studios/corporate; 7 tp)

LINEAR_FLOWS = ['awakening','true-fit','arrival','first-25','ripple','inner-circle'];
SEPARATE_FLOWS = ['sunday-pause','spaces'];

### Anti-data corrections applied to SAGE's tables (binding)

- ff-01 "Day one: just wear it": success = email open, not "wear detection".
- ff-02 "Your pulse schedule": app push OK (setup task, not tracking).
- ff-08 "The pause is working": NO app-data playback. Reframe: reflection email
  — "count nothing; notice one moment you returned this week." Success = reply rate.
- ff-09 "Two weeks of returning": time-based recognition, no streak counts.
- ff-12 "Your presence report": quiz-delta self-report rendered as archetype
  shift + reclaimable-life framing. Never a grade, never telemetry.
- wp-04 lapse trigger: 21 days of zero email/app engagement (not wear data).
- sp-07 team report: aggregate self-reported quiz deltas only, anonymized.

### Funnel link placement (binding)

- presence-quiz.html: awakening tp1 (results), first-25 tp11 (re-take), spaces
  tp2 (team baseline); CTA in sunday-pause tp4 (win-back), ripple tp5.
- presence-experience.html: awakening tp8 primary; CTA in awakening tp2/tp6,
  ripple tp4, spaces tp3.
- index.html: awakening tp9/tp11 primary; CTA in true-fit tp5, ripple tp3/tp4,
  spaces tp5. Buy CTAs only in Convinced/Generous phases.

## Image pipeline

`tools/generate-email-images.py`: adapted from generate-journey-images.py.
Manifest-driven: EMAIL_IMAGES list of (slug, world, stage, aspect, concept).
Reuses Maya character reference + KEEP + STYLE + per-stage COLOR grammar for
cream-world images; dark-luxe base prompt for product-world images:
"The wide polished gold Pulse band resting on near-black honed stone, a single
warm rim light tracing its edge out of deep shadow, macro jewelry photography,
medium-format, faint gold reflection pooling beneath, everything else void."
Aspect: 3:2 cream heroes; 16:9 dark heroes. Output email-images/<slug>.png.
Per-email prompt fragments: flows/consult-brand.md §4.

## QA gates

- `grep -riE "opus|soundbed|feelopus|schenk|betrayed|amplifier|session drop|hz|frequenc" presence-flows.html emails/` → zero hits (allow "response"-style false positives by refining).
- No streak/score/tracking language: `grep -riE "streak|score(?!.*quiz)|tracked|tracking|data" emails/` reviewed by hand.
- Serve via http.server; flow map renders; every assetRef resolves (no 404s);
  detail panel opens; localStorage keys are pulse-namespaced.
- Every email opens standalone; hero image present; funnel links resolve.
