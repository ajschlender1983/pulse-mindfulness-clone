# Pulse — Motion prompts (real video, Veo 3.1 image-to-video)

The three "feet" each have a distinct motion rule and a distinct video prompt. Feed a still
frame + the matching prompt to Veo 3.1 (`tools/veo_video.py` / `tools/generate-motion-veo.py`).
`{scene}` = a one-line description of the specific frame.

Engine note: Runway is out of credits — real video runs on **Veo 3.1 (`veo-3.1-fast-generate-preview`)
on the Gemini key**. ~8s / 720p / 24fps per clip, ~50s to generate, ~$1–1.5 each.

---

## 1. Photograph foot — handheld cell-phone

> Handheld cell-phone footage, as if filmed on a phone held in one hand: subtle organic camera
> drift, gentle micro-shake and a slight tilt, a breath of natural motion — never a locked tripod.
> The person is alive and present: a slow breath, hair and clothing moving in the air, a blink, a
> small shift of weight, the scene living quietly around them (water, light, distant movement).
> Warm medium-format film color, unhurried and intimate. No zoom punches, no cuts. **{scene}**

Rule: a lived moment has a pulse in the frame itself. Imperfect on purpose — the intimacy of a
real hand holding a real moment. Never the locked, gliding camera of the illustration foot.

## 2. Illustration foot — Disney multiplane parallax (characters alive, 3D-in-2D)

> Bring this hand-painted illustration to life with a classic Disney MULTIPLANE-camera effect:
> separate the scene into depth layers — foreground, midground, background — and glide them past the
> lens at different speeds so rich parallax opens up in every direction and the flat 2D artwork
> reveals its real 3D space. The characters are alive and three-dimensional: a soft breath, a blink,
> hair and fabric drifting, a small natural gesture — always enough gentle motion that they read as
> dimensional beings, never a static cut-out. Keep the painterly, gouache, cel-animation look
> intact; warm, unhurried, composed dimensional camera move; no cuts. **{scene}**

Rule: the illustration is a memory, painted — but it must **breathe in three dimensions**. Cut the
scene into depth planes and move them at different speeds (the multiplane camera) so the 2D world
shows its 3D space; keep the characters alive enough to feel dimensional. Composed and on rails,
never handheld.

## 3. Transition foot — illustration resolving into photograph (the reel slowing)

> Animate a transition from illustration to photograph: the image begins as a hand-painted
> illustration and resolves into a warm, living photograph of the same person and the same moment —
> the paint settling into real skin, light and texture. Time it like one slow breath, the pulse that
> slows the reel: cold and fast painterly on one side easing into warm, slow, handheld-real footage.
> Subtle parallax and the subject quietly coming alive as the medium changes. Warm, unhurried, no
> hard cuts. **{scene}**

Rule: the inflection. Use it once and let it land — it's the whole story (autopilot → presence) in
one move. The pulse is the hinge that slows the reel.

---

## When to use which — let the mood be intentional

Not a mechanical choice — a **mood** choice. Pick the foot by the feeling the moment should carry:

| Use… | When the mood is… | Because |
|---|---|---|
| **Illustration (multiplane)** | remembered, dreamlike, tender, universal, a little wistful — a feeling *about* life | it reads as memory and metaphor; the multiplane depth keeps it alive without pretending to be real |
| **Photograph (handheld)** | immediate, intimate, happening-right-now, true, embodied — a feeling you're *inside of* | handheld realism puts the viewer in the room; the moment has a pulse |
| **50/50 transition** | the turn itself — autopilot becoming presence, the missed moment being caught, before→after | the medium change *is* the message; only earn it at the hinge, never as decoration |

Guardrails: never mix the feet inside one shot except at a deliberate transition. Illustration is
composed/on-rails; photograph is handheld; the transition is the only place they touch. If a moment
could be either, ask what you want the viewer to *feel* — remembered vs. lived — and let that decide.
