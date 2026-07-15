#!/usr/bin/env python3
"""
Pulse — App UI storyboard, regenerated via Higgsfield's nano_banana_pro model
(direct image-reference conditioning, no Soul) after the pulse-123 Soul route
produced systemic defects: persistent phone-OS chrome despite negative
prompting, and garbled/illegible text on multi-line copy. nano_banana_pro
tested clean on both fronts (see $SCRATCH/hf-test/nbp-test.png,
nbp-text-test.png).

USAGE: python3 tools/generate-ui-screens-higgsfield.py [--only <id>]
Output: journey-images/ui-screens/<id>.png (overwrites the flawed pulse-123 versions)
"""
import subprocess, sys, pathlib, time, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "journey-images" / "ui-screens"
ANCHOR = ROOT / "journey-images" / "film-34-screen-breath-meter.png"

UI_STYLE = (
    "Extreme close-up, phone held in one hand, shallow depth of field, warm soft bokeh "
    "background (golden-hour light, blurred room or window). The phone screen glows warm "
    "cream/off-white edge to edge, filling the entire visible screen area — never white, "
    "never blue-lit, no status bar, no clock, no signal bars, no wifi icon, no battery icon, "
    "no back arrow, no icons of any kind, no bottom home-indicator bar, no nav bar, no tab bar. "
    "The single recurring visual device is a smooth, glowing warm-gold ring of light, "
    "hand-painted-soft at the edges like captured light rather than a flat vector. "
    "If text is specified, render it small, warm-grey, humanist sans-serif, crisp and "
    "perfectly legible, never more than two short lines. No app icons, no notification "
    "badges, no percentages, no numbers unless specified, no charts, no graphs, no colored "
    "status dots, no red anywhere. Photoreal, cinematic, medium-format film grain, warm "
    "color science. No logos, no watermark."
)

FRAMES = [
 ("home-nothing-to-check",
  "The home screen, entirely at rest. One soft gold ring glows very faintly at the center of "
  "an otherwise empty warm cream screen — nothing else on screen at all. No text. This is the "
  "app's resting state: deliberately, beautifully empty. " + UI_STYLE),

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
    OUT.mkdir(parents=True, exist_ok=True)
    ok, failed = [], []
    for fid, prompt in FRAMES:
        if only and only != fid:
            continue
        print(f"[{fid}] generating via Higgsfield (nano_banana_pro)...")
        cmd = [
            "higgsfield", "generate", "create", "nano_banana_pro",
            "--prompt", prompt,
            "--image-references", str(ANCHOR),
            "--aspect-ratio", "9:16",
            "--wait", "--wait-timeout", "3m",
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
        url = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
        if r.returncode != 0 or not url.startswith("http"):
            print(f"  FAIL {fid}: stdout={r.stdout!r} stderr={r.stderr!r}")
            failed.append(fid)
            continue
        out = OUT / f"{fid}.png"
        try:
            urllib.request.urlretrieve(url, out)
            print(f"  -> {fid}.png ({out.stat().st_size} bytes)")
            ok.append(fid)
        except Exception as e:
            print(f"  FAIL {fid} (download): {e}")
            failed.append(fid)
        time.sleep(1)

    print("\n=== summary ===")
    for fid, _ in FRAMES:
        if only and only != fid:
            continue
        print(f"{fid} {'OK' if fid in ok else 'FAILED'}")

if __name__ == "__main__":
    main()
