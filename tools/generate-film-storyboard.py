#!/usr/bin/env python3
"""
Pulse — Hero film storyboard generator (Nano Banana Pro / Gemini)
Generates the key frames of the "Here & Now Together" brand film.
Reads the key from GEMINI_API_KEY or ~/.gemini_api_key. Prints no secrets.
Outputs to ./journey-images/ as film-NN-*.png plus film.html.
"""
import os, sys, json, base64, urllib.request, urllib.error, pathlib, time

API = "https://generativelanguage.googleapis.com/v1beta"
OUT = pathlib.Path(__file__).resolve().parent.parent / "journey-images"

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

def pick_model(key, forced=None):
    if forced: return forced
    names = [m.get("name","").split("/")[-1] for m in call("models", key).get("models", [])
             if "generateContent" in m.get("supportedGenerationMethods", []) and "image" in m.get("name","").lower()]
    def rank(n):
        n=n.lower()
        if "3" in n and "pro" in n and "image" in n: return 0
        if "pro" in n and "image" in n: return 1
        if "flash" in n and "image" in n: return 2
        return 9
    names.sort(key=rank)
    return names[0] if names else sys.exit("no image model")

def generate(model, key, prompt, aspect="16:9", ref_b64=None):
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

STYLE = ("Cinematic anamorphic film still, wide 2.39:1 feel, shallow depth of field, gentle lens flare and "
         "soft bloom, fine 35mm grain, medium-format film color. Muted cream, honey and charcoal palette with a "
         "single warm gold accent and a faint dusty-blue only in the deep shadow. Emotionally resonant, real and "
         "un-staged, an award-winning brand film. No text, no logos, no watermark.")
RIPPLE = ("A soft concentric ring of warm golden light ripples outward from the wide polished gold ring on the "
          "finger, the visual moment of coming back to the present. ")

# the world's own illustration grammar (matches tools/generate-hybrid.py ILLUS + the multiplane motion rule):
# gouache/cel-animation painterly, Disney MULTIPLANE depth layers. Used for the churn (cold) and the sync (warm).
ILLUS_COLD = ("A wide hand-painted illustration in gouache and soft screen-print texture with confident inked "
 "linework, gentle cel-animation warmth, muted painterly 2.5D, composed in classic Disney MULTIPLANE depth "
 "layers — foreground, midground and background gliding at different depths so the flat artwork reveals real "
 "dimensional space. Steel-blue, cool, desaturated palette, hazy dusk city light, painterly and dreamlike, "
 "deliberately melancholy. No text, no logos, no watermark, no lettering.")
ILLUS_WARM = ("A poetic wide hand-painted illustration in gouache and soft screen-print texture, confident "
 "inked linework, gentle cel-animation warmth, composed in classic Disney MULTIPLANE depth layers — "
 "foreground, midground and background at different depths, real dimensional space. Warm honey and gold "
 "palette, painterly and dreamlike. No text, no logos, no watermark, no lettering.")

# (id, aspect, ref_from, prompt)
FRAMES = [
 ("01-open", "16:9", None,
  "Opening film frame. A crowded commuter train at dusk, rows of people all looking down at their phones, each alone in a private bubble, cool desaturated flat light, a held quiet loneliness, no one meeting anyone's eyes. " + STYLE),
 ("02-cafe-before", "16:9", None,
  "A woman in her early thirties hunched over a laptop at a beautiful wooden cafe, shoulders up around her ears, stressed and somewhere else, the warm room full of strangers softly out of focus around her, cool desaturated light draining the warmth from her face. " + STYLE),
 ("03-cafe-return", "16:9", "02-cafe-before",
  "Keep the exact same woman as the reference image. She lifts her eyes from the laptop. " + RIPPLE +
  "The cafe racks from blur into warm focus, golden light pours through the windows, and she meets the eyes of a stranger across the room for the first time. The quiet moment of being truly seen. " + STYLE),
 ("04-father-return", "16:9", None,
  "A father at a dinner table setting his phone face down and coming down to his young child's eye level, finally fully present with them. " + RIPPLE + "Warm golden evening light, the child lighting up at being seen. " + STYLE),
 ("05-couple-return", "16:9", None,
  "A couple who were lying in bed apart, both on their phones, now turning toward each other with phones set down, foreheads nearly touching. " + RIPPLE + "Warm intimate low light, tenderness returning between them. " + STYLE),
 ("06-sync-festival", "16:9", None,
  "A wide cinematic frame of a conscious festival field in the mountains at golden hour, hundreds of people, strangers turning to embrace the person beside them at the same moment, warm gold light and floating dust, a collective wave of people landing in their bodies together. " + STYLE),
 ("07-field-of-light", "16:9", None,
  "An aerial view at dusk over a city and landscape where countless small warm-lit windows and gatherings are connected by delicate threads of warm golden light spreading across the whole map, countless strangers sharing one gentle moment at the same instant, one single field of light. Deep dimensional layers of rooftops, streets and hills. " + ILLUS_WARM),
 ("08-tag-ring", "16:9", None,
  "A single wide polished gold ring resting on a pure near-black background. " + RIPPLE + "Minimal, elegant, the final tag frame of a film, deep negative space. " + STYLE),
 # Act I — the churn, expanded into a multiplane illustration montage (EBI: "show the churn more",
 # weave in the world's illustration/hybrid grammar). Cold and universal, many lives at once, one painted world.
 ("18-churn-montage", "16:9", None,
  "A single continuous painted world showing many different people in the same instant, all quietly somewhere else: in a foreground window a father scrolls his phone at the dinner table while his child talks unseen beside him; through a midground window rows of train commuters sit head-down, lit by phone-glow; on a park bench in the mid-ground a woman doom-scrolls alone; in a background crosswalk a whole crowd crosses with eyes down; in another window a couple lie in bed back to back, both lit by phone-light. This is autopilot, painted as one shared world. " + ILLUS_COLD),
 ("19-churn-waiting-room", "16:9", None,
  "A waiting room at dusk: a row of people side by side, every one of them looking down at a phone, not one face lifted, empty chairs between them though the room is full. Cold and quiet. " + ILLUS_COLD),
 ("20-churn-recital", "16:9", None,
  "A child's dance recital on a small stage; in the audience, parents hold up phones filming instead of watching, screens glowing, the child performing to a wall of raised devices. Cold and quiet. " + ILLUS_COLD),
 # the mind movie — the churn was never only phones. A person can be fully present in body and
 # still gone, replaying or rehearsing a scene only they can see. Made literal: a small, faint,
 # translucent film-frame hovers just beside their head, its own private screening, dimmer and
 # cooler than the real room around them, no phone anywhere in the shot.
 ("22-mind-movie-commute", "16:9", None,
  "A man walking down a familiar sidewalk at dusk, no phone in his hand or pocket, his eyes open but glazed, physically here and mentally gone — replaying an old argument. Beside his head, faint and translucent, a small floating film-frame shows two tiny painted figures mid-argument, its own private screening only we can see, dimmer and cooler than the real street around him. Cold and quiet. " + ILLUS_COLD),
 ("23-mind-movie-chores", "16:9", None,
  "A woman washing dishes at a kitchen sink, hands moving on autopilot, no phone anywhere, staring through the window rather than at it — rehearsing a conversation that hasn't happened yet. Beside her head, faint and translucent, a small floating film-frame shows her painted figure mid-conversation with someone unseen, its own private screening only we can see, dimmer and cooler than the real kitchen around her. Cold and quiet. " + ILLUS_COLD),
 # shooting-board coverage pass — filling every shot that still had no dedicated reference still.
 # All live-action photographic beats (matches the medium marked in the shooting board table).
 ("24-father-before", "16:9", None,
  "A father at a home dinner table, phone in hand and completely absorbed, his young child mid-story beside him going totally unseen, her small hopeful face starting to fade. Cool, flat, blue-tinted dusk light draining the warmth from the room. " + STYLE),
 ("25-couple-bed-before", "16:9", None,
  "A high angle shot over a bed at night: a couple lying apart, both lit by the cold blue glow of their phones, backs almost touching, thumbs scrolling, no words passing between them. " + STYLE),
 ("26-quickcuts-busstop", "16:9", None,
  "A person standing alone at a bus stop at dusk, head down into their phone, an empty bench beside them, cool desaturated light, quietly isolated. " + STYLE),
 ("27-quickcuts-scrollingcrowd", "16:9", None,
  "A person walking through a busy crowded sidewalk, eyes fixed on their phone, scrolling, completely oblivious to the people passing inches away, cool flat city light. " + STYLE),
 ("28-quickcuts-table-devices", "16:9", None,
  "A restaurant table of friends, every single person looking down at their own phone, no one talking, plates untouched between them, cool blue-tinted light. " + STYLE),
 ("29-crosswalk-crowd", "16:9", None,
  "A slow-motion wide shot of a busy crosswalk crowd at dusk, dozens of people crossing at once, every one of them sealed in their own private bubble, eyes down, no eye contact between any two people. " + STYLE),
 ("30-building-dusk", "16:9", None,
  "A wide held shot of an apartment building at dusk, dozens of lit windows, each one a separate glowing life, no two windows touching, quiet and cool. " + STYLE),
 ("31-her-pov-stranger", "16:9", None,
  "Point of view across a warm, golden cafe: a stranger at a nearby table looks up at the exact same instant, eyes meeting yours for the first time, soft warm light, the quiet held moment of being truly seen. " + STYLE),
 ("32-rapid-sync-montage", "16:9", None,
  "A four-panel cinematic collage in one continuous frame: a rooftop, a kitchen, a train car, and a park, each showing a different person pausing at the exact same instant, eyes closing, shoulders dropping, landing fully present. Warm golden hour light unifies all four into one shared moment. " + STYLE),
 ("33-two-strangers-embrace", "16:9", None,
  "A close-up of two strangers at a festival embracing tightly, both visibly moved, golden hour light catching tears, a spontaneous and real human connection. " + STYLE),
 # "Finding the others" — a new scene bridging Act II into Act III. The screen was never the
 # enemy on its own; the film makes literal the three sanctioned reasons to look down (set your
 # intention, deepen your practice, find the others) by having its own churn-shot grammar
 # (a person on their phone, walking, seemingly checked out) return on purpose as a deliberate
 # misdirect — then reveal what the phone is actually being used for.
 ("34-screen-breath-meter", "16:9", None,
  "Extreme close-up of a phone screen held at chest height, showing the Pulse app's breath meter mid-session — a soft single ring of warm gold light slowly expanding and contracting like a breath, minimal, no numbers, no streaks, no red badges. A small quiet label reads 'Pulses scheduled: 3 today.' Warm, calm, intentional, nothing urgent about it. " + STYLE),
 ("35-eyes-opening", "16:9", None,
  "Extreme close-up on a woman's closed eyes, mid-breath, in warm soft light, as they gently begin to open — the exact instant of finishing a short guided practice, calm and unhurried, present. " + STYLE),
 ("36-pov-stranger-ring", "16:9", None,
  "A point-of-view wide shot walking down a sunlit sidewalk: up ahead, a stranger's hand catches the light for a moment, a glint of gold from a ring on his finger, barely noticeable unless you're looking. Warm, ordinary, unremarkable except for that one detail. " + STYLE),
 ("37-stranger-on-phone-misdirect", "16:9", None,
  "A man walking down a sunlit sidewalk, head down, looking at his phone — at a glance, exactly like the film's earlier churn shots of someone checked out and elsewhere. Warm daylight though, not cold — a visual echo meant to be misread. " + STYLE),
 ("38-screen-find-the-others", "16:9", None,
  "Extreme close-up of a phone screen: the Pulse app's 'Find the Others' view, a soft minimal map with a few gentle anonymous pins nearby, one of them pulsing warm gold as it grows closer, no names, no photos, no profiles — just presence, nearby. Warm, calm, intentional interface design. " + STYLE),
 ("39-the-recognition", "16:9", None,
  "Two-shot on a sunlit sidewalk: a man lowers his phone as a woman approaches, and they both notice the gold ring on each other's hand at the same instant — the smallest surprised, warm smile of recognition between two strangers. Golden hour light, intimate and unhurried. " + STYLE),
 ("40-constellation-field-of-light", "16:9", None,
  "An aerial illustrated view at dusk over a city and landscape where countless small warm-lit windows are connected by delicate threads of gold light — but now the threads are actively drawing themselves between distant strangers in real time, like a living map of people finding each other, thousands of quiet 'nice to be here with you' moments happening across the world in the same instant. Deep dimensional multiplane layers of rooftops, streets and hills. " + ILLUS_WARM),
 ("41-hybrid-ring-water", "16:9", None,
  "An extreme close-up macro shot of a gold ring resting exactly at the edge of still water at dusk, the frame split by an invisible vertical seam down the exact center: on the right half of the frame the water is rendered as sharp, photoreal cinematography — real ripples, real reflected light — while the ring resting in it is rendered in soft painterly gouache illustration, the brand's illustration grammar; on the left half of the frame the water is rendered in that same soft painterly illustration, while the ring itself is sharp, hyper-real photography. The ring appears to cross its own seam, half painted and half real, mirrored. Extremely minimal, near-black surroundings, warm gold light, the film's final signature image. No text, no logos, no watermark, no lettering."),
]

def build_gallery():
    imgs = sorted(p.name for p in OUT.glob("film-*.png"))
    rows = "".join(f'<figure><img src="{n}"/><figcaption>{n.replace("film-","").replace(".png","")}</figcaption></figure>' for n in imgs)
    (OUT / "film.html").write_text(
      "<!doctype html><meta charset=utf-8><title>Pulse film storyboard</title>"
      "<style>body{background:#0d0d0f;color:#F3EFE0;font-family:system-ui;margin:0;padding:44px}"
      "h1{font-weight:400;letter-spacing:-.03em}.g{display:grid;grid-template-columns:repeat(2,1fr);gap:20px;margin-top:24px}"
      "figure{margin:0;border-radius:14px;overflow:hidden;background:#16181d}img{width:100%;display:block}"
      "figcaption{font:11px ui-monospace,monospace;color:#8a8a8e;padding:10px 14px;letter-spacing:.08em;text-transform:uppercase}</style>"
      "<h1>Pulse — Hero film storyboard</h1><p style='color:#9a978c'>Here &amp; Now Together</p><div class=g>"+rows+"</div>")

def main():
    key = get_key(); only = sys.argv[sys.argv.index("--only")+1] if "--only" in sys.argv else None
    model = pick_model(key, None); print("model:", model)
    done = {}
    for fid, aspect, ref_from, prompt in FRAMES:
        if only and only != fid: continue
        ref = done.get(ref_from)
        if ref_from and ref is None:
            p = OUT / f"film-{ref_from}.png"
            if p.exists(): ref = base64.b64encode(p.read_bytes()).decode()
        print(f"[film-{fid}] ...")
        img = generate(model, key, prompt, aspect=aspect, ref_b64=ref)
        if img:
            (OUT / f"film-{fid}.png").write_bytes(img); done[fid] = base64.b64encode(img).decode()
            print(f"  -> film-{fid}.png")
        time.sleep(1)
    build_gallery(); print("Done. film.html written.")

if __name__ == "__main__":
    main()
