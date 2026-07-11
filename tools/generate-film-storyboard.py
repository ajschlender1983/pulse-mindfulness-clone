#!/usr/bin/env python3
"""
Pulse — Hero film storyboard generator (Nano Banana Pro / Gemini)
Generates the key frames of the "Somewhere Else, Together" brand film.
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
  "A poetic wide aerial at dusk over a city and landscape where many small warm-lit windows and gatherings are connected by delicate threads of warm golden light spreading across the map, countless strangers sharing one gentle moment at the same instant, one single field of light. " + STYLE),
 ("08-tag-ring", "16:9", None,
  "A single wide polished gold ring resting on a pure near-black background. " + RIPPLE + "Minimal, elegant, the final tag frame of a film, deep negative space. " + STYLE),
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
      "<h1>Pulse — Hero film storyboard</h1><p style='color:#9a978c'>Somewhere Else, Together</p><div class=g>"+rows+"</div>")

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
