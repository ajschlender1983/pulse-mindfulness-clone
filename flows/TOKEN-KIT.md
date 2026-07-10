# Pulse Email Token Kit — for email build agents

Two golden references (copy their structure, CSS, and conventions EXACTLY):
- **Cream template** (human world): `emails/email-quiz-results.html`
- **Dark template** (product world): `emails/email-order-confirmed.html`

Decision rule: hero = Maya/life → cream. Hero = the ring/logistics → dark.
(Per-email world assignment is listed in your dispatch prompt.)

## Hard rules

1. Start from the golden file for your world. Keep: the full `<head>`, the table
   skeleton, class names (`pmf-card`, `email-header`, `email-meta`,
   `email-subject`, `email-body`, `prompts`/`order-card`, `pause-block`,
   `cta-wrap`, `btn-pill`, `signature`, `email-footer`, `cm-placeholder`),
   responsive rules, and the placeholder styling. Change only content and the
   content-specific blocks.
2. Hero image: `src="images/hero-<your-email-slug>.png"` — slug = filename
   without `.html`. Cream: inset `.hero-wrap` below the header (see cream
   golden). Dark: full-bleed at top with `.hero-fade` (see dark golden).
   Write a real, descriptive `alt`.
3. Senders. Personal/journey (founder voice): `Johan from Pulse
   <johan@pulsemindfulness.com>`, sig name "Johan", sig title "CEO, Pulse".
   Transactional/logistics: `Pulse <hello@pulsemindfulness.com>`, Reply-To
   `care@pulsemindfulness.com`, sig "The Pulse team". Spaces flow:
   `Johan from Pulse <partners@pulsemindfulness.com>`.
4. Merge tags: `{{first_name}}`, `{{order_number}}`, `{{ring_size}}`,
   `{{ship_city}}`, `{{order_total}}`, `{{archetype}}`,
   `{{reclaimable_hours}}`, `{{tracking_link}}`, `{{gift_sender}}`,
   `{{company_name}}`, `{{theme_name}}` — always wrapped in
   `<span class="cm-placeholder">{{tag}}</span>`. Use only tags that make sense
   for the email; invent a new `{{snake_case}}` tag if genuinely needed.
5. Voice (from flows/consult-brand.md §3 — read it):
   present tense, second person; one breath per sentence; NO exclamation
   points; "you may notice" never "you will feel"; no urgency/scarcity/
   countdown; concrete over cosmic (ban: journey, transform, unlock, elevate);
   **every email contains one written 10-second pause** (`.pause-block`).
6. Anti-data (from flows/BUILD-SPEC.md): never mention tracking, scores,
   streaks, wear detection, telemetry, app data. The app only sets vibration
   patterns and pulse windows. The quiz is the only measurement, and it's
   self-reported ("archetype", "reclaimable hours" — never a grade).
7. CTAs: max ONE lime `btn-pill` per email. Funnel links are relative from
   `emails/`: `../index.html` (buy — only in Convinced/Generous-phase emails),
   `../presence-quiz.html`, `../presence-experience.html`. In-email
   cross-links to other emails are not allowed (emails stand alone).
8. Footer: one "You're receiving this because <specific reason>." line,
   "Pulse · Amsterdam", and links (Unsubscribe · View in browser; transactional
   emails use Order status instead of Unsubscribe).
9. NO absolute URLs, no external images, no OPUS vocabulary (grep gate:
   opus|soundbed|feelopus|schenk|vibroacoust|transducer|session drop|hz).
   "Presence", "practice", "pause" are the house nouns.
10. Length: 120–260 words of body copy. These are letters. Short is right.

## Non-email assets

- `sms-*.html`: single small card mimicking a phone message (keep the source's
  sms file structure from voice-assets, reskinned cream). 1–2 sentences max,
  one link or none. No hero image.
- `call-script-*.html`: internal doc styling (cream card, DM Mono labels):
  goal, opening line, three beats, what NOT to say, close. No hero image.
- `landing-*.html`: standalone page in the site's look (cream, DM Sans display
  type, lime CTA) — see `simple/styles.css` tokens; these can be longer and may
  use their hero at top. Hero: `src="images/hero-<slug>.png"` if a matching
  image exists in your dispatch prompt, else no image.
