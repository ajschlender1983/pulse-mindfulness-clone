# Brand Creative Director — Pulse Email System, App Reskin, Voice, Image, Naming

New derived token used throughout: **`--honey: #C9A227`** — the journey's destination color.

## 1. Email Design System

### Cream "letter" template (default — the human world)

```css
/* frame */
--email-bg:        #EBE7D4;                       /* outer body */
--email-card:      #F9F6E5;                       /* letter card, max-width 640px */
border-radius:     26px;
box-shadow:        0 30px 80px rgba(66,61,50,.10);
padding:           40px 44px;                     /* 34px 24px under 520px */

/* meta header (From/To block) */
font:              12px "DM Mono";  color: #8a8578;  line-height: 1.7;
strong:            color: #423D32;  font-weight: 500;
border-bottom:     1px solid rgba(66,61,50,.14);  padding-bottom: 20px;

/* subject */
font:              400 24px/1.1 "DM Sans";  letter-spacing: -0.04em;
color:             #423D32;                       /* brown. NEVER lime — lime is never text */

/* body */
font:              17px/1.7 "DM Sans";  letter-spacing: -0.02em;
color:             #575344;
strong:            #1A1C22;  font-weight: 500;
links:             color: #C9A227; underline; text-underline-offset: 3px;

/* prompt box (reflection prompts) */
background:        #EBE7D4;  border-radius: 16px;  padding: 24px 28px;
label:             11px "DM Mono" uppercase, ls .12em, color #8a8578;
prompt items:      border-left: 2px solid #C9A227;  padding-left: 16px;  color: #423D32;

/* CTA — lime pill. The brand's only loud object; ONE per email, max */
background: #E3F47D;  color: #101828;  border-radius: 100px;  padding: 15px 36px;
font: 500 15px "DM Sans";

/* signature */
border-top: 1px solid rgba(66,61,50,.12);  margin-top: 40px; padding-top: 24px;
name: 15px/500 #1A1C22;   title: 12px "DM Mono" #8a8578;

/* footer */
font: 11px "DM Mono";  color: rgba(66,61,50,.45);  line-height: 1.9;  links underlined same color;
divider (mid-email): 1px, max-width 200px, centered, background #ddd7c3;
```

**Hero placement:** inset rounded card, NOT full-bleed. 3:2 image, border-radius 16px, inside the letter card ~28px below the meta header, full card-width. These are letters, not campaigns.

### Dark "luxe" variant (the product world)

```css
--email-bg: #0d0d0f;  --email-card: #141416;
headings: #F9F6E5;  body: rgba(249,246,229,.72);  meta/footer: #6d6f74;
accent + links: #C9A227;  card borders: 1px solid rgba(201,162,39,.18);
CTA: unchanged lime pill (#E3F47D on #101828);
prompt/info card: #1A1C22 with border-left 2px solid rgba(201,162,39,.4);
hero: may run full-bleed to card edge with bottom gradient into body; 16:9 allowed.
```

**Decision rule: if the hero is Maya, the email is cream. If the hero is the ring, the email is dark.**
Money-and-logistics (order confirmation, shipping, gift *purchase*, studio/corporate) = dark luxe. Everything *felt* = cream. **Arrival day is the deliberate crossover**: cream template, product-in-golden-hour-life hero — the handoff between worlds; the customer should feel the temperature change.

## 2. Flow-Map App Reskin

```css
:root {
  --bg:        #EBE7D4;   /* was rgb(14,10,20) */
  --dark:      #1A1C22;
  --accent:    #E3F47D;   /* ALWAYS paired with #101828 text */
  --midtone:   #8a8578;
  --light:     #F9F6E5;
  --ink: #1A1C22;  --brown: #423D32;  --honey: #C9A227;
  --line: rgba(26,28,34,.09);
  --canvas-dot: #ddd7c3;
  --shadow: 0 12px 30px rgba(66,61,50,.08);
  --font: "DM Sans", sans-serif;  --mono: "DM Mono", monospace;
}
```
Cards `--light` on `--bg`, radius 14–16px, `--shadow`; pills/labels DM Mono 11px; connectors `--line` 1.5px, `--honey` selected. Teal/magenta neon disappears — nothing glows on cream. One dark surface: top app bar in `--ink` with lime logo dot.

```css
/* channels */
--ch-email: #C9A227;  --ch-sms: #7FA0B4;  --ch-phone: #B0764F;
--ch-website: #565D6E;  --ch-social: #97A93B;

/* phases — chip bg = 18% tint on cream; text = full value. The ramp IS the information. */
--ph-numb: #93A5B1;  --ph-seen: #A3A493;  --ph-hopeful: #B3A379;
--ph-convinced: #C0A45D;  --ph-relieved: #CCA94C;  --ph-grateful: #D6AC3E;
--ph-generous: #E0B036;   /* + 1px #E3F47D outer ring on the chip */

/* status */
draft:     bg #E4DFC9, text #6E6857, border 1px dashed #c9c3ae;
in_review: bg rgba(201,162,39,.16), text #8A6D14;
approved:  bg #E3F47D, text #101828;
```

## 3. Voice — five rules (each with OPUS → Pulse example)

1. **Present tense, second person, right now.**
   OPUS: "It's been 48 hours since your SoundBed arrived. I wanted to reach out personally."
   Pulse: "Your ring has been on your finger for two days. Before you read on — one breath. Notice where you are."
2. **One breath per sentence.** No exclamation points, ever.
   OPUS: "...that's the moment that matters more than anything we could say in an email."
   Pulse: "The first pulse is small. That's the point."
3. **Invite, don't instruct or promise.** "You may notice," never "you will feel." No urgency, scarcity, countdowns.
   OPUS: "You'll feel the difference." → Pulse: "You might notice the difference. You might not yet. Both are fine."
4. **Concrete over cosmic.** Kitchen counters, car parks, 6:50am toast. Ban "journey," "transform," "unlock," "elevate."
   OPUS: "It's designed to deepen what your first session started." → Pulse: "Wear it while you make the coffee tomorrow. That's the whole practice."
5. **Every email contains one real pause.** A written 10-second micro-pause somewhere in the body ("Here, actually: ten seconds. Feel your feet. We'll wait."). No email ships without it.

**Senders.** Personal/journey: "Johan from Pulse" <johan@pulsemindfulness.com>, sig "Johan — CEO, Pulse". Transactional: "Pulse" <hello@pulsemindfulness.com>, Reply-To care@pulsemindfulness.com. Never no-reply.

## 4. Image Direction

**3:2 for all cream email heroes** (the TIME & PLACE lens). Dark luxe product renders may run 16:9 full-bleed. Ring is always the "discovered second-glance glint" — except dark luxe, where the ring is the only subject.

**Dark luxe base prompt:** "The wide polished gold Pulse band resting on near-black honed stone, a single warm rim light tracing its edge out of deep shadow, macro jewelry photography, medium-format, faint gold reflection pooling beneath, everything else void." No Maya, no rooms, no cream.

| Email | World | Stage grammar | Prompt fragment (append stage COLOR + STYLE blocks from generator) |
|---|---|---|---|
| Welcome / quiz result | Cream | 2 Seen | Maya in her parked car, engine off, for once not reaching for her phone, first honey light through the windshield finding one cheek. |
| Order confirmation | Dark | — | Luxe base + the ring casting one long warm reflection across the stone, a held promise in the dark. |
| Shipping | Dark | — | Macro: ring nested in undyed linen inside a kraft box in near-darkness, lid half-shadowing, one blade of gold light finding the band. |
| Unboxing / arrival day | Cream (crossover) | 3 Hopeful | Opened box on a windowsill in early-morning light, tissue folded back, ring catching its first real sun, lime-lit leaf edge on the sill plant. No hands — the moment before. |
| First pulse | Cream | 4 Convinced | Maya stopped mid-task at the lamp-lit sink, one wet hand still on a bowl, small surprised stillness, thumb finding the ring without looking. Clearest, sharpest light of the set. |
| Week 1 — Noticing | Cream | 3 | Breath fogging a cold windowpane at dawn, a fingertip drawing one short upward line through the bloom. |
| Week 2 — Returning | Cream | 4 | Maya kneeling at a child's eye level at the front door, backpack still on her shoulder, actually listening. Clean confident daylight. |
| Week 3 — Softening | Cream | 5 Relieved | Maya slumped in a sunlit corner chair, eyes closed, jaw unclenched, one open hand on her chest. The exhale she didn't know she was holding. |
| Week 4 — Arriving | Cream | 6 Grateful | Warm practical-lit dinner, Maya and her daughter close in a two-shot, real food and a little mess, Maya leaning in and present. |
| Milestone (time-based) | Cream | 6 | Macro: hand flat over the heart on bare skin, low sun raking, the pulse at the wrist catching light, the warm gold ring on the same hand. |
| Review / story ask | Cream | 6→7 | Maya at the table watching her daughter laugh, her own eyes wet, hand pressed to her mouth — caught by how much she almost missed. |
| Referral | Cream | 7 Generous | Macro: warm water poured from one cupped palm into another, the ring on the giving hand catching full golden sun mid-pour. Presence given away. |
| Gift (buyer) | Dark | — | Luxe base + ring in an open gift box, ribbon undone, one gold rim light — an intention about to leave your hands. |
| Gift (recipient) | Cream | 2 | An unopened box on a hallway table in cool morning light, one warm sidelight just arriving across it from a doorway. Someone thought of you. |
| Studio / corporate | Dark | — | Wide 16:9: five rings in a precise row on black stone, one shared raking gold light, architectural shadow. Practice, at scale. |
| Re-engagement / win-back | Cream | 1→2 | The ring unworn on a bedside dish in cool grey-blue morning light, near-monochrome — one thin blade of warm amber entering from the frame edge, just reaching the band. The only cream email allowed to open cold; the amber blade is the offer. |

## 5. Naming

- Flow-map product: **"Cadence"** ("Open Cadence," "This flow lives in Cadence"). Avoid "Journey" — Pulse Journeys is a live in-app product name; collision is a real headache. Runner-up: "The Current."
- Weekly release: **"The Sunday Pause"** — "Pause" is the brand's own noun; a fixed day converts a content release into a ritual. Subject pattern: "The Sunday Pause — [theme]". Fallback if day floats: "This Week's Pause".
