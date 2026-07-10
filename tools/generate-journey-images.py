#!/usr/bin/env python3
"""
Pulse — Journey image generator (Nano Banana Pro / Gemini)
==========================================================
Generates an on-brand, character-consistent image set that illustrates the
customer journey across 7 stages x 3 lenses (STATE / TIME & PLACE / TEXTURE),
built from the five-creative-director synthesis.

USAGE
  1. Provide your key WITHOUT pasting it anywhere public:
       printf '%s' 'YOUR_KEY' > ~/.gemini_api_key && chmod 600 ~/.gemini_api_key
     (or: export GEMINI_API_KEY=YOUR_KEY)
  2. python3 tools/generate-journey-images.py
     optional: --model gemini-3-pro-image-preview   (force a model)
               --only 1a                            (generate one frame)
               --list-models                        (just list image models)

Outputs to ./journey-images/ plus a gallery.html contact sheet.
No key is ever printed or written to disk by this script.
"""
import os, sys, json, base64, urllib.request, urllib.error, pathlib, time

API_ROOT = "https://generativelanguage.googleapis.com/v1beta"
OUT = pathlib.Path(__file__).resolve().parent.parent / "journey-images"

# ----------------------------------------------------------------- key
def get_key():
    k = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if k:
        return k.strip()
    f = pathlib.Path.home() / ".gemini_api_key"
    if f.exists():
        return f.read_text().strip()
    sys.exit("No Gemini key found. Set GEMINI_API_KEY or write ~/.gemini_api_key")

def api(path, key, body=None):
    url = f"{API_ROOT}/{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method="POST" if body is not None else "GET")
    req.add_header("x-goog-api-key", key)
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode())

# ------------------------------------------------------------- model pick
def pick_model(key, forced=None):
    models = api("models", key).get("models", [])
    img = []
    for m in models:
        name = m.get("name", "").split("/")[-1]
        methods = m.get("supportedGenerationMethods", [])
        if "generateContent" in methods and "image" in name.lower():
            img.append(name)
    if forced:
        return forced, img
    # preference order: Nano Banana Pro (3 pro image) -> nano-banana -> flash-image
    def rank(n):
        n = n.lower()
        if "3" in n and "pro" in n and "image" in n: return 0
        if "nano" in n and "banana" in n and "pro" in n: return 1
        if "nano" in n and "banana" in n: return 2
        if "pro" in n and "image" in n: return 3
        if "flash" in n and "image" in n: return 4
        return 9
    img.sort(key=rank)
    if not img:
        sys.exit("No image-capable models on this key. Run with --list-models to inspect.")
    return img[0], img

# ------------------------------------------------------------- generate
def generate(model, key, prompt, aspect="4:5", ref_b64=None, tries=3):
    parts = [{"text": prompt}]
    if ref_b64:
        parts.append({"inlineData": {"mimeType": "image/png", "data": ref_b64}})
    base_body = {"contents": [{"role": "user", "parts": parts}]}
    # try a few config shapes for cross-model robustness
    configs = [
        {"generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": aspect}}},
        {"generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}},
        {},
    ]
    last = None
    for cfg in configs:
        body = dict(base_body); body.update(cfg)
        for attempt in range(tries):
            try:
                resp = api(f"models/{model}:generateContent", key, body)
                for cand in resp.get("candidates", []):
                    for p in cand.get("content", {}).get("parts", []):
                        d = p.get("inlineData") or p.get("inline_data")
                        if d and d.get("data"):
                            return base64.b64decode(d["data"])
                last = "no image part in response"
                break
            except urllib.error.HTTPError as e:
                last = f"HTTP {e.code}: {e.read().decode()[:300]}"
                if e.code in (429, 500, 503):
                    time.sleep(3 * (attempt + 1)); continue
                break
            except Exception as e:
                last = str(e); time.sleep(2); continue
    print(f"    ! failed: {last}")
    return None

# ------------------------------------------------------------- prompts
STYLE = ("Warm golden-hour light raking low from one side. Medium-format film photograph, "
         "fine natural grain, shallow depth of field, soft highlight bloom. Muted cream, honey and "
         "charcoal palette with soft brown, a faint dusty-blue only in the deepest shadow. Calm, "
         "unhurried, real and un-staged, editorial. The wide polished gold band on her right hand "
         "appears only as a discovered second-glance glint, never centered. No text, no logos, no watermark.")

CHARACTER = ("A 38-year-old woman named Maya. Warm light-brown skin of mixed South Asian heritage, "
             "dark brown hair in a soft low bun with a few loose strands framing her face, tired kind "
             "dark eyes, natural full brows, minimal makeup, gentle features, slim build. She wears a "
             "soft oatmeal knit cardigan over a simple cream top, small gold hoop earrings, and a wide "
             "polished gold band on her right ring finger.")

REF_PROMPT = ("Editorial character portrait. " + CHARACTER + " Neutral warm expression, looking softly "
              "toward camera, three-quarter view, even soft window light so her face reads clearly for "
              "later reference. " + STYLE)

KEEP = "Keep the exact same woman as the reference image: identical face, hair, and features. "

# the two children (kept consistent across all family frames via a family reference)
KIDS = ("Priya, her daughter, about six, warm light-brown skin like her mother, dark wavy shoulder-length "
        "hair and bright dark eyes; and a younger sibling, a toddler about two and a half, chubby cheeks, "
        "soft dark curls, the same warm skin.")
FAMILY = {"1a", "1b", "4b", "6a", "6b", "7b"}   # frames that show the children
FAMILY_REF = ("Editorial family reference photograph, a mother and her two children together, all three faces "
              "clear for later reference. " + CHARACTER + " With her two children: " + KIDS +
              " The three of them together in soft even window light, warm, calm and real. " + STYLE)
KEEP_FAMILY = ("Keep the exact same three people as the reference image: the same mother and her same two "
               "children, identical faces, hair, and features. ")

# color note per stage (from the color director)
COLOR = {
 1: "Cool grey-blue cast, near-monochrome low saturation, flat sourceless screen-like light, ashen skin, stale hazy air, no figure-ground separation.",
 2: "Mostly cool grey with one warm amber sidelight entering from the frame edge onto one cheek, saturation climbing, the first soft visible haze.",
 3: "Soft brown and pale honey rising through the midtones, early-morning window warmth, grey-blue retreating to the corners, one small lime glint of sun through a living leaf.",
 4: "Honey-cream and clear, the sharpest and cleanest frame of the set, one confident cool shadow giving the image a spine, crisp air.",
 5: "Warm cream, golden-hour beginning, low forgiving light softening every edge, a gentle warm haze, shoulders-down light.",
 6: "Full honey gold, rich golden-hour backlight and rim, golden dust drifting in the air, skin glowing warm and alive.",
 7: "Honey gold at its fullest with cream highlights blooming, luminous golden-hour flare, lime alive as sunlight through leaves onto two people, warmth spilling past her toward the person she is giving to.",
}

# aliveness of her eyes and face, blooming as she becomes present (dull early, warm late)
PRESENCE = {
 1: "Her eyes are distant and unlit, no warmth reaching her face, present in body but gone behind the eyes.",
 2: "The faintest warmth just returning to her face, her eyes beginning to soften.",
 3: "A small light waking in her eyes, the first real warmth touching her face.",
 4: "A clear, quiet brightness in her eyes and gentle warmth on her face, present and softly alert.",
 5: "Her face soft, warm and glowing, the released ease of a long-held breath let go.",
 6: "Her eyes bright and shining with feeling, her face warm and fully alive, deeply present and moved.",
 7: "Her eyes luminous and warm, her whole face glowing with presence, open, radiant and giving.",
}

# 21 frames: (id, stage, lens, aspect, use_ref, concept)
FRAMES = [
 ("1a", 1, "STATE", "4:5", True,
  "Maya at the kitchen counter at 6:50am in yesterday's cardigan, distracted, her attention caught by the phone in her hand, while her two children reach for her, unmet: her daughter Priya at her side holding up a crayon drawing and reaching up to be seen, and her toddler tugging at her leg. Maya's eyes stay on the phone, not on the children. Present in body, gone behind the eyes, their small hopes going unmet."),
 ("1b", 1, "TIME & PLACE", "3:2", True,
  "Wide dawn kitchen, cold north-window light. Maya stands distracted at the counter, half-looking at the phone in her hand, while her two young children reach up toward her and call for her attention, small and unmet: Priya at the table and the toddler at her feet. A lot of dead negative space and glass between them. Two children wanting their mother, and the mother somewhere else."),
 ("1c", 1, "TEXTURE", "1:1", False,
  "Extreme macro. Cold blue phone-glow flattening the side of an open hand and palm, skin drained grey, no warmth reaching it, the dull unlit gold ring at the soft frame edge."),

 ("2a", 2, "STATE", "4:5", True,
  "Maya sitting in her parked car in a dim hospital garage, engine off, not going in and not going home, for once not reaching for her phone, letting herself feel how tired she is. The first honey light through the windshield finds one cheek. Being seen begins with letting herself be seen."),
 ("2b", 2, "TIME & PLACE", "3:2", True,
  "6:40am, Maya on the edge of an unmade bed, creased sheets, a single warm lamp on in an otherwise cool room, the day not yet started. A quiet held moment before anything happens."),
 ("2c", 2, "TEXTURE", "1:1", True,
  "Macro. The first blade of warm sun crossing an open palm, one strip lit gold and the rest still in cool shadow, a fingertip resting near the warm gold ring, warmth noticed before it is understood."),

 ("3a", 3, "STATE", "4:5", True,
  "Maya standing at a window in early-morning light, one hand flat on the glass, weight shifting forward onto her toes, the smallest lift at the corner of her mouth, eyes up toward something not yet done. Warm rim light beginning on her hair. Anticipation."),
 ("3b", 3, "TIME & PLACE", "3:2", False,
  "A packed bag sitting by a front door, not yet lifted, and morning light falling on an empty chair where a child will sit. On the windowsill a small plant catches one lime-lit translucent leaf edge. A room about to begin. Future tense."),
 ("3c", 3, "TEXTURE", "1:1", False,
  "Macro. Breath fogging a cold windowpane at dawn, and a fingertip has just drawn one short upward line through the bloom, clear glass and warm light breaking through the stroke. Hope made an action."),

 ("4a", 4, "STATE", "4:5", True,
  "Maya mid-task at the lamp-lit kitchen sink, sleeves pushed up, stopped with one wet hand still on a bowl because she just caught herself actually hearing the rain and her daughter's voice from the next room. A small surprised stillness, her thumb finding the ring without looking. The clearest, sharpest light of the set."),
 ("4b", 4, "TIME & PLACE", "3:2", True,
  "Maya kneeling down to her two children's eye level at the front door, backpack still on her own shoulder, actually listening to a small urgent story from Priya while the toddler leans into her. The packed bag is now lifted. The same props from before, now in motion. Clean confident daylight, and she is fully with them."),
 ("4c", 4, "TEXTURE", "1:1", False,
  "Macro. A single water drop falling toward a perfectly still surface, caught the instant before contact, its ring not yet formed. The held breath before the shift lands. Everything crisp and clarifying."),

 ("5a", 5, "STATE", "4:5", True,
  "Maya slumped back alone in a sunlit corner chair, eyes closed, face turned up into soft golden light, jaw finally unclenched, one open hand resting on her chest. The exhale she did not know she was holding. Solitary release."),
 ("5b", 5, "TIME & PLACE", "3:2", True,
  "Late afternoon, Maya alone on the edge of a made bed in a quiet room, low forgiving golden-hour light through a window softening every edge, no one else present, shoulders-down calm."),
 ("5c", 5, "TEXTURE", "1:1", False,
  "Macro. A shoulder and jaw sinking into sun-warmed rumpled linen, muscle visibly letting go, honey shadow deep in every fold."),

 ("6a", 6, "STATE", "4:5", True,
  "Maya at the dinner table watching her two children, Priya laughing and the toddler beside her, Maya's own eyes wet, a hand pressed to her mouth, caught by how much she almost missed. Eyes open, turned fully toward her children. Warm backlight, skin glowing alive."),
 ("6b", 6, "TIME & PLACE", "3:2", True,
  "A warm practical-lit dinner, a lamp and low sun through curtains, Maya and her two children close together, Priya and the toddler, real food and a little mess on the table, Maya leaning in and fully present with them."),
 ("6c", 6, "TEXTURE", "1:1", True,
  "Macro. A hand laid flat over the heart on bare skin, low sun raking across, the pulse at the wrist catching light, the warm gold ring on the same hand."),

 ("7a", 7, "STATE", "4:5", True,
  "Maya on a porch at golden hour, no phone, both hands cupped warmly around a friend's hands across a small table, leaning in, giving the exact quality of attention she was once starved for. The ring catches light as she gives her attention away. She has become the warm light for someone else."),
 ("7b", 7, "TIME & PLACE", "3:2", True,
  "Golden-hour porch or shared green space, sunlight streaming through leaves, Maya fully turned toward a friend she is comforting while her two children, Priya and the toddler, play nearby. Warmth spilling outward past Maya toward the person receiving her presence."),
 ("7c", 7, "TEXTURE", "1:1", True,
  "Macro. Two hands, warm water poured from one cupped palm into another, the gold ring on the giving hand catching full golden sun mid-pour. Presence given away."),
]

def build_prompt(f, family=False):
    _id, stage, lens, aspect, use_ref, concept = f
    lead = ((KEEP_FAMILY if family else KEEP) if use_ref else "")
    face = lens in ("STATE", "TIME & PLACE")
    pres = (" " + PRESENCE[stage]) if face else ""
    return f"{lead}{concept} {CHARACTER if not use_ref and lens=='STATE' else ''} Colour and light: {COLOR[stage]}{pres} {STYLE} Aspect ratio {aspect}."

# ------------------------------------------------------------- main
def main():
    args = sys.argv[1:]
    forced = None; only = None
    if "--model" in args: forced = args[args.index("--model")+1]
    if "--only" in args: only = args[args.index("--only")+1]
    key = get_key()

    if "--list-models" in args:
        _, allimg = pick_model(key, None)
        print("Image-capable models on this key:")
        for m in allimg: print("  -", m)
        return

    model, allimg = pick_model(key, forced)
    print(f"Using model: {model}")
    print(f"(other image models available: {', '.join(m for m in allimg if m!=model) or 'none'})")
    OUT.mkdir(exist_ok=True)

    # 1) character reference
    ref_path = OUT / "00-maya-reference.png"
    ref_b64 = None
    if ref_path.exists() and not only:
        ref_b64 = base64.b64encode(ref_path.read_bytes()).decode()
        print("Reusing existing character reference.")
    elif not only or only == "ref":
        print("Generating Maya character reference ...")
        img = generate(model, key, REF_PROMPT, aspect="4:5")
        if img:
            ref_path.write_bytes(img); ref_b64 = base64.b64encode(img).decode()
            print(f"  -> {ref_path.name}")
        else:
            print("  reference failed; frames will run without a locked face.")
    else:
        if ref_path.exists():
            ref_b64 = base64.b64encode(ref_path.read_bytes()).decode()

    if only == "ref":
        return

    # family reference (mother + two children), locked so the kids stay consistent
    fam_path = OUT / "00b-family-reference.png"
    fam_b64 = None
    need_family = (only in FAMILY) or (only == "famref") or (not only)
    if need_family:
        if fam_path.exists() and only != "famref":
            fam_b64 = base64.b64encode(fam_path.read_bytes()).decode()
            if not only:
                print("Reusing existing family reference.")
        else:
            print("Generating family reference (mother + two children) ...")
            fimg = generate(model, key, KEEP + FAMILY_REF, aspect="3:2", ref_b64=ref_b64)
            if fimg:
                fam_path.write_bytes(fimg); fam_b64 = base64.b64encode(fimg).decode()
                print(f"  -> {fam_path.name}")
            else:
                print("  family reference failed; family frames will use the solo reference.")
    if only == "famref":
        return

    # 2) frames
    for f in FRAMES:
        _id = f[0]
        if only and only != _id:
            continue
        stage, lens, aspect, use_ref = f[1], f[2], f[3], f[4]
        is_family = _id in FAMILY
        rb = ((fam_b64 or ref_b64) if is_family else ref_b64) if use_ref else None
        out = OUT / f"{_id}-stage{stage}-{lens.split()[0].lower()}.png"
        print(f"[{_id}] stage {stage} · {lens} ...")
        img = generate(model, key, build_prompt(f, family=is_family), aspect=aspect, ref_b64=rb)
        if img:
            out.write_bytes(img); print(f"  -> {out.name}")
        time.sleep(1)

    build_gallery()
    print(f"\nDone. Open {OUT/'gallery.html'}")

def build_gallery():
    imgs = sorted(p.name for p in OUT.glob("*.png"))
    rows = "".join(
        f'<figure><img src="{n}" alt="{n}"/><figcaption>{n}</figcaption></figure>' for n in imgs)
    html = f"""<!doctype html><meta charset=utf-8><title>Pulse journey images</title>
<style>body{{background:#EBE7D4;font-family:system-ui;margin:0;padding:40px;color:#1A1C22}}
h1{{font-weight:600;letter-spacing:-.03em}} .grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}}
figure{{margin:0;background:#F9F6E5;border-radius:14px;overflow:hidden;box-shadow:0 12px 30px rgba(0,0,0,.06)}}
img{{width:100%;display:block}} figcaption{{font:11px ui-monospace,monospace;color:#8a8578;padding:10px 12px;letter-spacing:.04em}}</style>
<h1>Pulse — the journey, numb to generous</h1><div class=grid>{rows}</div>"""
    (OUT / "gallery.html").write_text(html)

if __name__ == "__main__":
    main()
