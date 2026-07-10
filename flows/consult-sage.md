# SAGE (PM) — Pulse Voice Flows Adaptation Spec

**PM position:** OPUS Voice is a *recovery* system. Pulse has no debt to repay, so the same energy goes to the top of the funnel: **the Awakening Flow (quiz-lead nurture) is the new center of gravity**. In-Queue and Delivery compress into **True Fit** (sizing = #1 DTC ring failure mode) and **Arrival**. Freed budget goes to dormancy win-back — a mindfulness ring's existential churn risk is the drawer.

## 1. Flow Mapping — OPUS → Pulse

| # | OPUS flow | Pulse flow id | Pulse name | Description | Arc phases | Cut / transformed |
|---|---|---|---|---|---|---|
| 1 | resolution | `awakening` | Awakening Flow | Pre-purchase nurture from presence-quiz completion to first order. | Numb → Convinced | Cut apology posture, refund pivot, backlog forms. Keep: instant acknowledgment, one-record-per-person, no-pressure dual-CTA. |
| 2 | in-queue | `true-fit` | True Fit Flow | Order confirmation through sizing fork to confirmed fit; free-exchange safety net. | Convinced → Relieved | Refund-vs-delivery fork becomes know-my-size vs need-a-sizer fork. |
| 3 | delivery | `arrival` | Arrival Flow | Ship notice through unboxing, charging, app pairing, first pulse. | Relieved | Cut weeks of wait-justification. Keep ceremonial ship email, prep, arrival-day pair, entry ritual. |
| 4 | engagement | `first-30` | First 30 Days Flow | New owner builds the wear-charge-notice habit; ends with a felt presence shift. | Relieved → Grateful | 60d → 25d. Keep Day-4 newcomer/listener fork intact (best pattern in OPUS system). |
| 5 | session-drop | `sunday-pause` | The Sunday Pause | Recurring Sunday theme release plus dormancy win-back triggers. | Grateful (re-entry Numb→Seen) | Friday → Sunday evening. Add lapse-detection branch — no OPUS equivalent. |
| 6 | user-amplifier | `ripple` | Ripple Flow | Reviews, referrals, gifting, shareable presence stories. | Grateful → Generous | Cut crisis recovery ask. Add gift prompt. |
| 7 | advocacy | `inner-circle` | Inner Circle Flow | Manually enrolled advocates: recognition, story capture, co-creation. | Generous | "Founding Circle" → "The First Hundred". |
| 8 | commercial | `spaces` | Spaces Flow | Studios, spas, corporate wellness. | Seen → Grateful | Practice assessment → space/team assessment; impact report → aggregate team presence report (self-reported quiz deltas). |

## 2. Audience Segments (replaces AUD_DEFS)

| id | Label | Definition |
|---|---|---|
| quiz-lead | Quiz Lead | Completed presence-quiz.html; no purchase yet. |
| browser | Browser | Visited/carted on index.html without finishing; no quiz. |
| new-owner | New Owner | Order placed through Day 30 post-activation. |
| owner | Owner | Day 26+, engaged (funnel stage 6, Believer). |
| gift-giver | Gift Giver | Purchased for someone else; never wears the ring. |
| gift-recipient | Gift Recipient | Activated a gifted ring; needs its own welcome. |
| lapsed | Lapsed | Owner with 21+ days of zero email/app engagement. |
| partner | Partner | Studio, spa, or corporate wellness buyer. |

## 3. Touchpoint Tables (60 touchpoints)

### Flow 1 — awakening (dayOrigin: quiz-day) · quiz-lead, browser
| # | Day | Channel | Title | Phase | Intent | Success | Source |
|---|---|---|---|---|---|---|---|
| 1 | 0 | Email + Page | Your presence score | Seen | Deliver quiz results instantly; first proof someone noticed. Archetype + reclaimable number, never a grade. | Open > 55%; results-page time > 90s | res-tp-03 |
| 2 | 1 | Email | The moment you noticed | Seen | Mirror the reader's autopilot day (Maya's Tuesday) so they feel named, not sold to. | Read > 60s; CTR to presence-experience > 12% | NEW |
| 3 | 3 | Email | What autopilot costs | Seen | Problem education: attention residue, days that blur. No product mention. | Open > 45% | NEW |
| 4 | 5 | Email | A pulse instead of a ping | Hopeful | Mechanism: gentle physical pulse, no screen, no notification, nothing to check. | CTR > 10% | del-tp-03 |
| 5 | 7 | Email | One reader's Tuesday, after | Hopeful | Social proof story matched to quiz archetype. | CTR > 8% | del-tp-02 |
| 6 | 10 | Email | Try this before you buy anything | Hopeful | Free 60-second presence practice; generosity before commerce. | Practice completion > 25% | NEW |
| 7 | 14 | Email | Your questions, answered | Convinced | Objections: sizing, battery, "another device?", returns, water. | Open > 40%; reply > 3% | com-tp-04 |
| 8 | 18 | Email | The Presence Experience | Convinced | Longform immersion invite (presence-experience.html). | Scroll depth > 60% | NEW |
| 9 | 21 | Email | When you're ready | Convinced | Soft close: guarantee, free size exchange, single calm CTA to index.html. No scarcity. | Conversion > 3% | res-tp-12 pattern |
| 10 | 30 | Email | We'll be here | Convinced | Downshift to monthly; explicit opt-down. Respecting attention IS the brand. | Unsub < 1% | NEW |
| 11 | trigger | Email | Still thinking it over | Convinced | Cart-abandon (browser): guarantee + sizing safety net, one CTA. | Recovery > 8% | NEW |

### Flow 2 — true-fit (dayOrigin: order-day) · new-owner, gift-giver
| 1 | 0 | Email | Your ring is coming | Convinced | Order confirmation; the decision was the first act of presence. | Open > 60% | iq-tp-01 |
| 2 | 0 | Email (fork) | First, the right fit | Convinced | Fork: confirmed size ships now; unsure gets sizing kit. One question. | Fork response > 85% in 48h | iq fork |
| 3 | 3 | Email + SMS | Your sizing kit is here | Convinced | Teach the measure: wear sizer overnight, knuckle check, dominant hand. | Kit-to-size > 75% | NEW |
| 4 | 5 | Email | Confirm your size | Convinced | One-tap confirmation; one record per customer. | Confirmation > 90% | res-tp-02 |
| 5 | 0 | Email (gift) | A gift of presence | Generous | Gift-giver: confirmation, gift-note capture, discreet recipient sizing link. | Note completion > 60% | NEW |
| 6 | trigger | Email | Exchange, made simple | Relieved | Free size exchange; kills the #1 return reason. | Exchange < 8%; NPS ≥ 8 | iq refund→exchange |

### Flow 3 — arrival (dayOrigin: ship-day) · new-owner, gift-recipient
| 1 | Shipped | Email | It's on its way | Relieved | Ceremonial ship notice + permission to slow down. | Open > 65% | del-tp-05 |
| 2 | Transit | Email | Before it arrives | Relieved | Prep: download app, pick a charging spot you'll see nightly. | Pre-install > 40% | del-tp-04 |
| 3 | Delivery | SMS + Email | It's here | Relieved | Open it when you have five quiet minutes. | Confirm > 95% | del-tp-06 |
| 4 | Day 0 | Email | Charge, pair, breathe | Relieved | Unbox ritual: full charge, app pairing, one breath before first wear. | Pairing in 24h > 80% | NEW |
| 5 | Day 0 | Website | Your first pulse | Relieved | Guided 90-second first-pulse arrival ritual page. | Completion > 85% | eng-tp-02 Threshold |
| 6 | trigger | Email | Someone thought of you | Seen | Gift-recipient welcome: who sent it and why (opt-in note), own setup path. They start at Seen. | Activation > 70% | NEW |

### Flow 4 — first-30 (dayOrigin: pairing-day) · new-owner, gift-recipient
| 1 | 1 | Email | Day one: just wear it | Relieved | Zero-goal start; the only job is the ring on your finger. | Open > 60% | eng-tp-01 |
| 2 | 2 | Website | Your pulse windows | Relieved | Set three daily pulse windows anchored to real moments (commute, lunch, bedtime). Setup, not tracking. | Windows set > 75% | NEW |
| 3 | 3 | Email | What did you notice? | Relieved | First reflection: one word before, one after. | Reply > 40% | eng-tp-04 |
| 4 | 4 | Email (fork A) | No rush | Seen | Not-yet-paired variant: unhurried founder note. | Reply > 10% | eng-tp-13 |
| 5 | 4 | Email (fork B) | How is it going with your ring? | Relieved | Active variant: one 1–10 feeling rating + comment ask. | Rating > 30% | eng-tp-13b |
| 6 | 5 | SMS | Charge while you shower | Relieved | Anchor charging to an existing ritual; a dead ring is a dead practice. | — | NEW |
| 7 | 7 | Email | Week one: what to notice | Relieved | Somatic education: the pulse works before you register it. | Open > 45% | eng-tp-06 |
| 8 | 10 | Email | The pause is working | Grateful | Reflection: count nothing; recall one moment you returned this week. (NO app data playback.) | Reply rate | eng-tp-07 |
| 9 | 14 | Email | Two weeks of returning | Grateful | Time-based recognition (no streak counts) + pulse-window tune-up prompt. | Adjustment > 20% | eng-tp-08 |
| 10 | 21 | Email | The 21-day threshold | Grateful | Habit science: what repetition does in the nervous system. | Open > 45% | eng-tp-09 |
| 11 | 25 | Email | Thirty days present | Grateful | Milestone + quiz re-take invite; measure the shift they can feel. | Re-take > 35% | eng-tp-10 |
| 12 | 25 | Website | Your presence report | Grateful | Before/after quiz delta as archetype shift + reclaimed-life framing. Never a grade, never telemetry. Graduates to owner. | View > 60%; share > 10% | NEW |

### Flow 5 — sunday-pause (cadence weekly, anchor Sunday) · owner, new-owner, lapsed
| 1 | Sun | Email | The Sunday Pause — Arrive | Grateful | Sunday-evening theme + matching pulse pattern in app. | Activation > 30% | sd-tp-01 |
| 2 | Wed | SMS | Midweek return | Grateful | One line: the theme lives in the body, not the inbox. | — | sd-tp-03 |
| 3 | Fri | Email | What others noticed this week | Grateful | Community reflections; quiet social proof, no leaderboard. | Open > 35% | sd-tp-02 |
| 4 | trigger 21d silent | Email | Come back to now | Numb→Seen | Win-back: no guilt, one small step — charge it tonight, wear it tomorrow. | Re-engage in 7d > 20% | NEW |
| 5 | +7d | Email | One minute, no ring required | Seen | Ringless 60-second practice; re-enter through practice, not product. Then quiet 30 days. | Completion > 15% | NEW |

### Flow 6 — ripple (dayOrigin: graduation-day) · owner
| 1 | 0 | Email | Your first impression, in your words | Grateful | Review ask while Day-30 glow is fresh. | Review > 12% | ua-tp-01 |
| 2 | 7 | Email | Your story matters | Grateful | Testimonial ask; feeds Friday community email + site proof. | > 5% | ua-tp-02 |
| 3 | 14 | Email | Give a month of presence | Generous | Referral link, gift-framed. | Share > 15% | ua-tp-03 |
| 4 | 21 | Email | Someone you love is on autopilot too | Generous | Direct gift prompt — gift the person you named in the quiz. | Gift conv > 2% | NEW |
| 5 | 30 | Email | What you've given yourself | Generous | Shareable presence story card. | Share > 10% | ua-tp-04 |
| 6 | 45 | Email + Social | Join the Presence Circle | Generous | Community invite, earned at six weeks. | Join > 20% | ua-tp-05 |
| 7 | 60 | Email | Your story kit | Generous | Assets + language to tell their journey their way. | Engagement > 25% | ua-tp-06 |

### Flow 7 — inner-circle (trigger: manual enrollment) · owner
| 1 | 0 | Email | We noticed your practice | Generous | Founder recognition of their journey, not their purchase. | Reply > 30% | adv-tp-01 |
| 2 | 3 | Email | Here's what you can share | Generous | Share kit: language, prompts, assets. Equip, don't script. | Use > 40% | adv-tp-02 |
| 3 | 7 | Email + Phone | Can we tell your story? | Generous | Personal founder ask for filmed/longform story. | > 50% of asked | adv-tp-03 |
| 4 | 14 | Email | You're showing others the way | Generous | Amplify what they shared; celebration, not extraction. | Repeat > 30% | adv-tp-04 |
| 5 | 30 | Email | The First Hundred | Generous | Named early-advocate circle: early pattern access, founder line. | Accept > 80% | adv-tp-05 |
| 6 | 60 | Email | Help shape what's next | Generous | Co-creation: beta patterns, app input, named in release notes. | > 50% | adv-tp-06 |

### Flow 8 — spaces (dayOrigin: inquiry-day) · partner
| 1 | 0 | Email | We received your inquiry | Seen | Warm acknowledgment; studio/spa vs corporate path from first touch. | Response > 60% | com-tp-01 |
| 2 | 1 | Email + Phone | Your space assessment | Seen | 8-minute assessment; routes proposal; optional team baseline quiz. | > 50% | com-tp-02 |
| 3 | 3 | Email | Your proposal | Hopeful | Studio bundle or team program with sizing-day logistics. | Open > 80% | com-tp-03 |
| 4 | 7 | Email | Questions answered | Hopeful | Objections: pricing, hygiene, sizing at scale, ROI. | Re-engage > 25% | com-tp-04 |
| 5 | 14 | Phone / Zoom | Decision call | Convinced | Human decision call. | Close > 30% | com-tp-05 |
| 6 | 21 | Email | Your launch kit | Relieved | Sizing day plan, team pairing guide, intro session script. | Launch in 30d > 90% | com-tp-06 |
| 7 | 30 | Email | Month one: your team's presence report | Grateful | Aggregate anonymized self-reported quiz deltas + founder check-in. | Review booked > 70% | com-tp-07 |

## 5. Scores

```js
var PRESENCE_SCORES = { Numb: 0, Seen: 15, Hopeful: 30, Convinced: 55, Relieved: 75, Grateful: 100, Generous: 120 };
```
Relieved=75: the Convinced(55)→Relieved gap is the activation chasm, biggest single jump.

## 6. Build notes

- dayOrigin values: quiz-day, order-day, ship-day, pairing-day, graduation-day, enrollment-day, inquiry-day; weekly anchor sunday.
- Port the eng-tp-13/13b fork pattern exactly (same sequence 1/2 + triggerCondition strings) for first-30 tp4/tp5 and true-fit tp2.
- Buy CTAs only in Convinced/Generous phases — never during Seen.
