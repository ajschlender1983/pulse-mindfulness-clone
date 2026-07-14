# Pulse v2 — Market Research: RFID business model + the Pulse Pillow (EEG) platform

*Compiled 2026-07-14 to support the Pulse fundraising deck. Two questions: (1) what does the RFID
chip mean for the business model, and (2) is the Pulse Pillow's far-field-EEG + partnership thesis
credible. Sources cited inline. **Two hard caveats are flagged in bold — they are what a technical
investor will probe, and the deck must get ahead of them.***

---

## Part 1 — What RFID/NFC unlocks as a business model

**What the chip physically does in a ring.** NFC (the consumer subset of RFID) is a passive ~4cm
tap — no battery draw on the ring. Realistic uses, in order of fit for Pulse:
- **Tap-to-pair / device handoff** — tap the ring to the Pulse Pillow (or any partner device) to
  associate identity/state with zero pairing friction. *Strongest fit for the thesis.*
- **Presence / identity token** — "this is Adam's Pulse" to any compatible reader → check-in,
  personalization, access.
- **Access / check-in / loyalty** — unlock a studio, log a spa visit, gate a membership tier (proven; Token, NFC Ring, HID Global badge use).
- **Payments** — technically possible, commercially a graveyard (see risk). Treat as a distraction.
> **Caveat A (technical):** NFC is the *handshake*, not the *pipe*. Continuous biometric streaming
> between ring and pillow needs Bluetooth. "The ring talks to every wellness device" is a
> pairing/identity story, not a data-streaming one, unless Pulse ships a broader radio stack.

**Business-model patterns it unlocks:**
- **Hardware → platform / ecosystem lock-in — the Disney MagicBand case.** Disney spent ~$1B turning
  an RFID band into the connective tissue of the parks (key, ticket, payment, personalization); a tap
  replaced the friction *and the psychological sting* of paying; per-cap spend rose ~4%, Parks revenue
  +6% / operating income +16% the first quarter post-launch ([hoteltechreport](https://hoteltechreport.com/news/disneys-magicband), [d3.harvard.edu](https://d3.harvard.edu/platform-digit/submission/disneys-magical-big-data-transformation/)). This is exactly the "ring makes the Pillow feel like magic" mechanic — **but Disney won because it owned the whole closed venue. The moat was the ecosystem, not the RFID.**
- **Recurring-revenue attach — Whoop / Oura.** Whoop makes hardware ~free and charges $20–30/mo;
  subscriptions are ~85% of a ~$1.1B business, LTV:CAC ~4.5x, >50% daily use 18mo+ ([sacra](https://sacra.com/research/whoop-at-1b-year-growing-103-yoy/)). Validates "$200 ring as top-of-funnel for Pulse Plus." The chip's job is to *widen the surface area for the subscription* — every tap-enabled partner device is a new reason to stay subscribed.
- **Ingredient brand / interoperability — Oura's API + Dexcom.** Oura: 5.5M+ rings, ~80% share,
  $500M+ 2024 revenue → ~$1B projected 2025; a partner/API layer (50+ metrics, 800+ integrations) and a two-way Dexcom deal ($75M invested) ([businesswire](https://www.businesswire.com/news/home/20250922351288/en/), [fiercehealthcare](https://www.fiercehealthcare.com/digital-health/smart-ring-maker-oura-picks-75m-series-d-inks-strategic-partnership-dexcom)). The template for "every lie-down wellness brand is a partner" — **but Oura's leverage is data + installed base, not a tap.**

**Market signals (cite a range, not a point):** smart rings ~$0.41B (2025) → $1.14B (2030) at ~23.6% CAGR ([globenewswire/Mordor](https://www.globenewswire.com/news-release/2025/11/24/3193582/0/en/)); other firms say $2.5B by 2030. Oura alone ~$1B proves the *category* monetizes — as a data/subscription business, not an RFID one. Broader NFC is a mature ~$21.7B→$30.6B enabling tech, i.e. not scarce.

> **Caveat B (strategic) — RFID is a feature, not a moat.** NFC chips cost cents and are in every
> phone. The payment-ring category is a graveyard (Kerv collapsed in IP disputes; McLear barely
> survives) because the moat was never the chip ([wareable](https://www.wareable.com/wearable-tech/kerv-nfc-smart-ring-contactless-payments-1782)). **Defensibility must be located explicitly in three places, not the chip:** (1) owning the reader/venue side Disney-style (the Pillow + a proprietary tap-handshake partners adopt); (2) the Pulse Plus subscription + installed base Whoop/Oura-style; (3) a partner network with switching cost (each partner's product gets *better because of Pulse*). **Frame the chip honestly as the low-friction wedge that makes the platform legible — the moat lives in the ecosystem.**

---

## Part 2 — The Pulse Pillow: consumer EEG + biometrics-as-a-platform

**Market.** Consumer-grade EEG ~$1.9B (2023) → ~$3.8B (2031) at ~8.7% CAGR ([Verified Market Research](https://www.verifiedmarketresearch.com/product/consumer-grade-eeg-device-market/)); wearable-EEG ~$1.1B (2025), ~12.8% growth. **This is a niche next to the $6.8T wellness economy — lean into that: Pulse's TAM is wellness, EEG is the moat, not the market.**

**Players / models:** Muse (neurofeedback headband, ~$250–400, hardware + subscription — the closest model to Pulse Plus); Emotiv (research-grade, ~$850–1,000, data/SDK licensing); NeuroSky (low-cost OEM chip licensing); **Neurable MW75 Neuro ($699, 12-ch EEG in headphone earpads with fabric electrodes)** — the closest existing precedent to "EEG embedded in a comfortable everyday object"; sleep-tech headbands (Philips SmartSleep, Dreem).

> **Caveat C (credibility crux — the biggest risk in the whole raise):** "far-field EEG in a pillow"
> as usually imagined (brainwaves read at pillow distance, through hair, no contact) is **not
> credible at today's state of the art.** Scalp EEG is microvolts; capacitive non-contact electrodes
> show severe attenuation and "high sensitivity to motion artifacts," performance "highly dependent
> on electrode-scalp distance," and some literature calls them "unlikely to be appropriate for
> spontaneous EEG" ([ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0924424725012026), [PMC5371775](https://pmc.ncbi.nlm.nih.gov/articles/PMC5371775/)). In EEG, "far-field" normally means *deeper sources at the same electrode*, not "electrode far from head."
> **Reframe for the deck:** the Pillow is *gel-free textile / capacitive EEG where the head rests
> directly on the sensing surface* — occipital/temporal contact through fabric, no gel, no visible
> electrodes. That is defensible (dry/textile electrodes now rival wet for many uses — [AIP Advances 2025](https://pubs.aip.org/aip/adv/article/15/4/040703/3345166/)). Bundling the **Pulse ring is smart precisely because its proven PPG/HRV biometrics hedge the EEG-fidelity risk.**

**Ingredient-brand / SDK precedent is strong.** Oura exposes a REST API and reports **800+ partner
integrations**; Whoop runs a curated developer platform; aggregators (Terra, Thryve, Validic) resell
biometric streams — a real B2B2C market ([Oura API](https://cloud.ouraring.com/docs/), [Wareable](https://www.wareable.com/wearable-tech/oura-expands-integrations-with-library-of-partner-apps)). Ingredient branding (Intel Inside: 500+ OEMs by 1992; Dolby; Gore-Tex) wins on *affordable licensing + a visible badge* so partners prefer inclusion to exclusion. Pulse's edge would be *owning the brainwave-data layer spas/studios can't build themselves.*

**The "lie-down wellness" TAM — Pulse's strongest slide.** Global wellness economy **$6.8T (2024) →
$9.8T (2029)** ([Global Wellness Institute](https://globalwellnessinstitute.org/press-room/statistics-and-facts/)). The lie-down adjacencies are among the fastest-growing: sleep $107B (+12.5%/yr), meditation & mindfulness $7.1B (+18.9%/yr), spas (+14.6% YoY), mental wellness (+12.4%/yr). Every spa table, sound-bath mat, recovery lounge, and meditation studio already has a customer lying still with head supported — the exact posture textile EEG captures passively. Each venue becomes a distribution + data partner.

**Regulatory line.** Stay on the **FDA General Wellness** side — "track your meditation/sleep state"
is safe; "detect a disorder" triggers device regulation (tightened in 2026 guidance) ([FDA](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/general-wellness-policy-low-risk-devices), [Faegre Drinker](https://www.faegredrinker.com/en/insights/publications/2026/1/)).

**What makes investors believe the Pillow:** (1) a working signal-quality demo of textile EEG at rest
vs. a Muse baseline — not a render; (2) 2–3 signed lie-down-venue LOIs proving ingredient-brand pull;
(3) TAM framed as the $6.8T wellness economy with EEG as the moat; (4) the ring as fidelity insurance;
(5) explicit General-Wellness positioning to de-risk regulation.

---

## Implications for the Pulse fundraising narrative
1. **Sell the platform, not the chip.** RFID/EEG are wedges; the moat is the Pillow ecosystem + Pulse
   Plus subscription + partner switching cost. Say this out loud before an investor says it for you.
2. **The subscription is the venture-scale engine** (Whoop/Oura proof), with the ring as top-of-funnel
   and the Pillow as the partner/ingredient layer that compounds it.
3. **Get ahead of the two credibility risks** (RFID-as-commodity; EEG-fidelity) on-slide — reframe EEG
   as textile/contact, position RFID as the legibility wedge. Honesty here *raises* credibility.
4. **Lead the market slide with the $6.8T wellness economy and the lie-down wedge**, not the small EEG
   hardware TAM.
