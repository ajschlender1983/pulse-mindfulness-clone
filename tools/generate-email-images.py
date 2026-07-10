#!/usr/bin/env python3
"""
Pulse — Email hero image generator (Nano Banana Pro / Gemini)
=============================================================
Generates one hero image per email from tools/email-image-manifest.json,
reusing the Maya-character golden-hour grammar from generate-journey-images.py
for cream-world heroes and the dark-luxe product grammar for dark-world heroes.

USAGE
  1. Key: printf '%s' 'YOUR_KEY' > ~/.gemini_api_key && chmod 600 ~/.gemini_api_key
     (or export GEMINI_API_KEY=YOUR_KEY)
  2. python3 tools/generate-email-images.py
     optional: --model <name>       force a model
               --only <slug>        generate one email's hero
               --force              regenerate even if the file exists
               --list-models        list image models on this key

Outputs to ./emails/images/hero-<slug>.png plus a gallery.html contact sheet.
Skips files that already exist (safe to rerun after a mid-batch failure).
Manifest entries sharing a "file" value are generated once and copied.
No key is ever printed or written to disk by this script.
"""
import os, sys, json, base64, urllib.request, urllib.error, pathlib, time, shutil

API_ROOT = "https://generativelanguage.googleapis.com/v1beta"
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "emails" / "images"
MANIFEST = pathlib.Path(__file__).resolve().parent / "email-image-manifest.json"
REF_PATH = OUT / "00-maya-reference.png"

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
def generate(model, key, prompt, aspect="3:2", ref_b64=None, tries=3):
    parts = [{"text": prompt}]
    if ref_b64:
        parts.append({"inlineData": {"mimeType": "image/png", "data": ref_b64}})
    base_body = {"contents": [{"role": "user", "parts": parts}]}
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

# ------------------------------------------------------------- prompt grammar
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

COLOR = {
 1: "Cool grey-blue cast, near-monochrome low saturation, flat sourceless screen-like light, ashen skin, stale hazy air, no figure-ground separation.",
 2: "Mostly cool grey with one warm amber sidelight entering from the frame edge onto one cheek, saturation climbing, the first soft visible haze.",
 3: "Soft brown and pale honey rising through the midtones, early-morning window warmth, grey-blue retreating to the corners, one small lime glint of sun through a living leaf.",
 4: "Honey-cream and clear, the sharpest and cleanest frame of the set, one confident cool shadow giving the image a spine, crisp air.",
 5: "Warm cream, golden-hour beginning, low forgiving light softening every edge, a gentle warm haze, shoulders-down light.",
 6: "Full honey gold, rich golden-hour backlight and rim, golden dust drifting in the air, skin glowing warm and alive.",
 7: "Honey gold at its fullest with cream highlights blooming, luminous golden-hour flare, lime alive as sunlight through leaves onto two people, warmth spilling past her toward the person she is giving to.",
}

DARK_STYLE = ("Macro jewelry photography, medium-format digital, razor-thin depth of field. "
              "Near-black void background, honed dark stone surface, a single warm gold rim light "
              "out of deep shadow, faint gold reflection pooling beneath the band. Luxurious, "
              "precise, silent. No text, no logos, no watermark, no hands, no people.")

def build_prompt(entry):
    world = entry.get("world", "cream")
    concept = entry["prompt"].strip()
    if world == "dark":
        return f"{concept} {DARK_STYLE} Aspect ratio {entry.get('aspect','16:9')}."
    stage = entry.get("stage") or 4
    lead = KEEP if entry.get("use_ref") else ""
    char = "" if entry.get("use_ref") else (CHARACTER + " " if "Maya" in concept else "")
    return (f"{lead}{concept} {char}Colour and light: {COLOR[int(stage)]} {STYLE} "
            f"Aspect ratio {entry.get('aspect','3:2')}.")

# ------------------------------------------------------------- main
def main():
    args = sys.argv[1:]
    forced = None; only = None; force = "--force" in args
    if "--model" in args: forced = args[args.index("--model")+1]
    if "--only" in args: only = args[args.index("--only")+1]
    key = get_key()

    if "--list-models" in args:
        _, allimg = pick_model(key, None)
        print("Image-capable models on this key:")
        for m in allimg: print("  -", m)
        return

    manifest = json.loads(MANIFEST.read_text())
    model, allimg = pick_model(key, forced)
    print(f"Using model: {model}")
    OUT.mkdir(parents=True, exist_ok=True)

    # character reference (only needed if any cream entry uses it)
    ref_b64 = None
    needs_ref = any(e.get("use_ref") for e in manifest)
    if needs_ref:
        if REF_PATH.exists():
            ref_b64 = base64.b64encode(REF_PATH.read_bytes()).decode()
            print("Reusing existing Maya reference.")
        else:
            print("Generating Maya character reference ...")
            img = generate(model, key, REF_PROMPT, aspect="4:5")
            if img:
                REF_PATH.write_bytes(img)
                ref_b64 = base64.b64encode(img).decode()
                print(f"  -> {REF_PATH.name}")
            else:
                print("  reference failed; ref-based frames will run without a locked face.")

    # generate unique files, then copy to any sharing slugs
    done_files = {}
    ok, failed, skipped = 0, [], 0
    for e in manifest:
        slug = e["slug"]
        if only and only != slug:
            continue
        target = OUT / f"hero-{slug}.png"
        canonical = e.get("file", f"hero-{slug}.png")
        can_path = OUT / canonical

        if target.exists() and not force and not only:
            skipped += 1; continue

        if canonical in done_files or (can_path.exists() and not force):
            if not target.exists() or force:
                if can_path != target:
                    shutil.copyfile(can_path, target)
                    print(f"[{slug}] copied shared {canonical}")
            ok += 1; continue

        print(f"[{slug}] {e.get('world','cream')}/{e.get('stage','-')} ...")
        img = generate(model, key, build_prompt(e),
                       aspect=e.get("aspect", "3:2"),
                       ref_b64=(ref_b64 if e.get("use_ref") else None))
        if img:
            can_path.write_bytes(img)
            done_files[canonical] = True
            if can_path != target:
                shutil.copyfile(can_path, target)
            print(f"  -> {can_path.name}")
            ok += 1
        else:
            failed.append(slug)
        time.sleep(1)

    build_gallery()
    print(f"\nDone. generated/copied={ok} skipped-existing={skipped} failed={len(failed)}")
    if failed:
        print("Failed slugs (rerun with --only <slug>):")
        for s in failed: print("  -", s)
    print(f"Gallery: {OUT/'gallery.html'}")

def build_gallery():
    imgs = sorted(p.name for p in OUT.glob("hero-*.png"))
    rows = "".join(
        f'<figure><img src="{n}" alt="{n}"/><figcaption>{n}</figcaption></figure>' for n in imgs)
    html = f"""<!doctype html><meta charset=utf-8><title>Pulse email heroes</title>
<style>body{{background:#EBE7D4;font-family:'DM Sans',system-ui;margin:0;padding:40px;color:#1A1C22}}
h1{{font-weight:400;letter-spacing:-.04em}} .grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}}
figure{{margin:0;background:#F9F6E5;border-radius:14px;overflow:hidden;box-shadow:0 12px 30px rgba(66,61,50,.08)}}
img{{width:100%;display:block}} figcaption{{font:11px ui-monospace,monospace;color:#8a8578;padding:10px 12px;letter-spacing:.04em}}</style>
<h1>Pulse — email heroes</h1><div class=grid>{rows}</div>"""
    (OUT / "gallery.html").write_text(html)

if __name__ == "__main__":
    main()
