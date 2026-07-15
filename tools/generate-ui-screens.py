#!/usr/bin/env python3
"""
Pulse — App UI storyboard: 16 key touchpoints across the go-to-market narrative.
Anchored on the established gold-ring-of-light interface (film-34-screen-breath-meter.png,
film-44-daily-pulse-intention.png) for visual consistency — that ring is now the recurring
iconic device, referenced as an image input on every new generation.

USAGE: python3 tools/generate-ui-screens.py [--only <id>] [--force]
Output: journey-images/ui-screens/<id>.png + journey-images/ui-screens/index.html
"""
import os, sys, json, base64, urllib.request, urllib.error, pathlib, time

API = "https://generativelanguage.googleapis.com/v1beta"
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "journey-images" / "ui-screens"
ANCHOR = ROOT / "journey-images" / "film-34-screen-breath-meter.png"

def get_key():
    k = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if k: return k.strip()
    f = pathlib.Path.home() / ".gemini_api_key"
    if f.exists(): return f.read_text().strip()
    sys.exit("No Gemini key found.")

def call(path, key, body=None):
    req = urllib.request.Request(f"{API}/{path}", data=(json.dumps(body).encode() if body else None),
                                 method="POST" if body else "GET")
    req.add_header("x-goog-api-key", key); req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=180) as r: return json.loads(r.read().decode())

def generate(model, key, prompt, aspect="9:16", ref_b64=None):
    parts = [{"text": prompt}]
    if ref_b64: parts.append({"inlineData": {"mimeType": "image/png", "data": ref_b64}})
    base = {"contents": [{"role": "user", "parts": parts}]}
    for cfg in ({"generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": aspect}}},
                {"generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}}, {}):
        b = dict(base); b.update(cfg)
        for attempt in range(3):
            try:
                resp = call(f"models/{model}:generateContent", key, b)
                for c in resp.get("candidates", []):
                    for p in c.get("content", {}).get("parts", []):
                        d = p.get("inlineData") or p.get("inline_data")
                        if d and d.get("data"): return base64.b64decode(d["data"])
                break
            except urllib.error.HTTPError as e:
                if e.code in (429, 500, 503): time.sleep(3*(attempt+1)); continue
                break
            except Exception: time.sleep(2); continue
    print("    ! failed"); return None

# The locked visual language — every prompt below is this + its specific screen content.
# The reference image (breath-meter) is also passed on every call so the model anchors to
# the exact device render, hand style, warm bokeh field, and gold-ring rendering already
# established and loved.
UI_STYLE = (
    "Extreme close-up, phone held in one hand, shallow depth of field, warm soft bokeh "
    "background (golden-hour light, blurred room or window). The phone screen glows warm "
    "cream/off-white — never white, never blue-lit, never a cold interface. The single "
    "recurring visual device is a smooth, glowing warm-gold ring of light, hand-painted-soft "
    "at the edges like captured light rather than a flat vector — this ring (or a soft "
    "variation of it) is the entire visual language of the interface. No app icons, no "
    "notification badges, no nav bars, no tab bars, no percentages, no numbers unless "
    "specified, no charts, no graphs, no colored status dots, no red anywhere. Typography "
    "is minimal, warm grey, a humanist sans or soft serif, never more than two short lines. "
    "Photoreal, cinematic, same medium-format film grain and warm color science as a "
    "high-end product film. No text unless specified in the shot description. No logos, "
    "no watermark."
)

FRAMES = [
 ("home-nothing-to-check",
  "The home screen, entirely at rest. One soft gold ring glows very faintly at the center of "
  "an otherwise empty warm cream screen — nothing else on screen at all. No text, no icons, "
  "no clock, no status bar. This is the app's resting state: deliberately, beautifully empty. "
  + UI_STYLE),

 ("find-the-others",
  "A screen titled 'Find the Others' in small warm-grey text at the top. Below it, a soft "
  "gold ring with faint secondary rings of light drifting outward from it like ripples on "
  "water, a few small warm points of light scattered gently around the edges of the screen "
  "suggesting other nearby presences — no map, no pins, no names, no photos, no distances. "
  + UI_STYLE),

 ("the-recognition",
  "Two soft gold rings of light slowly overlapping and merging into one at the center of the "
  "screen, warm and gentle, like two ripples meeting. Small warm-grey text beneath, only: "
  "'You found each other.' " + UI_STYLE),

 ("pulse-map-selector",
  "A screen showing five small glowing points of warm gold light arranged in a soft, "
  "asymmetric constellation like a gentle compass — one point brighter than the rest, "
  "softly selected. Beneath each point, one small warm-grey word: Presence, Peace, Power, "
  "Pleasure, Purpose — tiny, quiet, not shouting. No icons, no numbers. " + UI_STYLE),

 ("core-radiance-reflection",
  "A quiet reflective screen: a single warm gold ring glowing softly at center, and around "
  "it, four short warm-grey phrases placed gently at the four compass points of the ring, "
  "each barely-there: 'connected', 'charged', 'clear', 'capable' — no bars, no scores, no "
  "percentages, no grades. Framed like a mirror, not a report card. " + UI_STYLE),

 ("couples-mode-send",
  "A screen mid-gesture: a thumb gently pressing a small warm gold ring icon at the bottom "
  "of the screen, and above it, two smaller linked rings of light drifting toward each other. "
  "Small warm-grey text: 'Sent.' No read receipt, no timestamp, no urgency. " + UI_STYLE),

 ("sync-event-invite",
  "A calm invitation screen. A large soft gold ring at center with a faint second ring just "
  "beginning to bloom around it. Small warm-grey text beneath: 'Join us at 6pm — wherever "
  "you are.' No countdown timer, no urgency styling, no red. " + UI_STYLE),

 ("gift-of-presence",
  "A screen showing a warm gold ring of light gently wrapped by a single soft ribbon-like "
  "curve of the same warm light, like a bow made of light rather than paper. Small warm-grey "
  "text beneath: 'A gift of presence.' No price, no cart icon, no urgency. " + UI_STYLE),

 ("the-guarantee",
  "A quiet reassurance screen after a purchase. A soft gold ring glowing steadily at center. "
  "Small warm-grey text beneath, two short lines only: 'Wear it a month.' and 'If it isn't "
  "for you, send it back — no reason needed.' No fine print visible, no logos, no upsell "
  "buttons. " + UI_STYLE),

 ("pause-is-working",
  "A gentle affirmation screen shown just after a short practice ends. The gold ring is "
  "settling, slightly dimming as if exhaling. Small warm-grey text beneath: 'You may notice "
  "a little more room to breathe.' No checkmark, no completion badge, no streak count. " + UI_STYLE),

 ("first-pulse-onboarding",
  "The very first screen a brand-new owner sees, moments after unboxing. A single warm gold "
  "ring is just beginning to bloom into existence at the center of the screen, soft and "
  "tentative, mid-fade-in. Small warm-grey text beneath: 'This is your first pulse.' No "
  "setup wizard, no progress bar, no permissions dialog visible. " + UI_STYLE),

 ("calendar-aware-softening",
  "A quiet contextual state: the gold ring is dimmer and slower than usual, visibly softened. "
  "Small warm-grey text beneath: 'Quieter during your meeting.' No calendar grid, no event "
  "list, no icons — just the ring itself changing its own behavior. " + UI_STYLE),

 ("the-gentle-nudge",
  "A screen shown after a long stretch of scrolling elsewhere. The gold ring appears with a "
  "single slow, deliberate pulse, warm and unhurried. Small warm-grey text beneath: 'You may "
  "notice you've been away a while.' No shame framing, no red alert styling, no lock icon, "
  "no timer. Kind, not punitive. " + UI_STYLE),

 ("charging-ambient",
  "The ring on its charging dock, seen through the phone screen as a companion view: a warm "
  "gold ring of light slowly, steadily filling like an ember catching, no percentage number "
  "visible anywhere, no lightning-bolt icon. Small warm-grey text beneath, only: 'Charging.' "
  + UI_STYLE),
]

def main():
    args = sys.argv[1:]
    only = args[args.index("--only")+1] if "--only" in args else None
    force = "--force" in args
    key = get_key()
    model = "gemini-3-pro-image-preview"
    OUT.mkdir(parents=True, exist_ok=True)
    ref_b64 = base64.b64encode(ANCHOR.read_bytes()).decode() if ANCHOR.exists() else None
    ok, failed, skipped = 0, [], 0
    for fid, prompt in FRAMES:
        if only and only != fid: continue
        out = OUT / f"{fid}.png"
        if out.exists() and not force:
            skipped += 1; continue
        print(f"[{fid}] ...")
        img = generate(model, key, prompt, aspect="9:16", ref_b64=ref_b64)
        if img:
            out.write_bytes(img); ok += 1; print(f"  -> {fid}.png")
        else:
            failed.append(fid); print(f"  FAIL {fid}")
        time.sleep(1)
    print(f"\nDone. generated={ok} skipped={skipped} failed={len(failed)}")
    if failed: print("failed:", ",".join(failed))

if __name__ == "__main__":
    main()
