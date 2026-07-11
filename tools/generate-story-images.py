#!/usr/bin/env python3
"""
Pulse — User-story image generator (soft ambient light)
=======================================================
Five user stories drawn from the Johan Matton conversation (customer segments:
yoga/meditation practitioners, ADHD & focus, habit chasers, anxiety/stress aid,
and the connection me->we pivot). Each story gets a character reference plus
four narrative frames, all in the SOFT ambient-natural-light grammar (an
deliberate departure from the moodier golden-hour set).

Also relights the darkest existing email heroes into soft variants
(saved as hero-<slug>-soft.png alongside the originals; swap at will).

USAGE
  python3 tools/generate-story-images.py            # everything missing
  python3 tools/generate-story-images.py --only <frame-id or story key>
  python3 tools/generate-story-images.py --force    # regenerate all
Outputs: story-images/<files> + story-images/gallery.html
         emails/images/hero-<slug>-soft.png (relights)
"""
import os, sys, json, base64, urllib.request, urllib.error, pathlib, time

API_ROOT = "https://generativelanguage.googleapis.com/v1beta"
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "story-images"
EMAIL_IMG = ROOT / "emails" / "images"

def get_key():
    k = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if k: return k.strip()
    f = pathlib.Path.home() / ".gemini_api_key"
    if f.exists(): return f.read_text().strip()
    sys.exit("No Gemini key found.")

def api(path, key, body=None):
    url = f"{API_ROOT}/{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method="POST" if body is not None else "GET")
    req.add_header("x-goog-api-key", key)
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode())

def pick_model(key, forced=None):
    models = api("models", key).get("models", [])
    img = [m.get("name","").split("/")[-1] for m in models
           if "generateContent" in m.get("supportedGenerationMethods",[]) and "image" in m.get("name","").lower()]
    if forced: return forced
    def rank(n):
        n=n.lower()
        if "3" in n and "pro" in n and "image" in n: return 0
        if "nano" in n and "banana" in n and "pro" in n: return 1
        if "nano" in n and "banana" in n: return 2
        if "pro" in n and "image" in n: return 3
        if "flash" in n and "image" in n: return 4
        return 9
    img.sort(key=rank)
    if not img: sys.exit("No image models on key.")
    return img[0]

def generate(model, key, prompt, aspect="3:2", ref_b64=None, tries=3):
    parts = [{"text": prompt}]
    if ref_b64: parts.append({"inlineData": {"mimeType": "image/png", "data": ref_b64}})
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
                        if d and d.get("data"): return base64.b64decode(d["data"])
                last = "no image part"; break
            except urllib.error.HTTPError as e:
                last = f"HTTP {e.code}"
                if e.code in (429,500,503): time.sleep(3*(attempt+1)); continue
                break
            except Exception as e:
                last = str(e); time.sleep(2); continue
    print(f"    ! failed: {last}")
    return None

# ---------------------------------------------------------------- grammar
SOFT = ("Soft ambient natural light: diffuse north-window daylight filling the room evenly, "
        "lifted gentle shadows, airy and breathable, luminous cream and warm oatmeal palette with "
        "quiet honey undertones, high-key but warm, no hard raking light, no heavy shadow, no dusk. "
        "Medium-format film photograph, fine natural grain, shallow depth of field, calm, unhurried, "
        "real and un-staged, editorial. The wide polished gold band appears as a discovered "
        "second-glance glint, never centered. No text, no logos, no watermark.")

KEEP = "Keep the exact same person as the reference image: identical face, hair, and features. "
KEEP2 = "Keep the exact same two people as the reference image: identical faces, hair, and features. "

STORIES = {
 # 1 — Yoga & meditation practitioner (segment 1)
 "ingrid": {
   "title": "Ingrid — from the mat into the day",
   "who": ("A 52-year-old yoga teacher named Ingrid. Silver-grey hair loosely pinned up, "
           "calm lined face, clear light-blue eyes, no makeup, linen wrap top in undyed flax, "
           "small silver stud earrings, and a wide polished gold band on her right ring finger."),
   "frames": [
     ("ingrid-1","3:2","Ingrid rolling up her mat by a bright studio window after morning practice, unhurried, the room full of even soft daylight."),
     ("ingrid-2","4:5","Ingrid mid-afternoon at a market stall choosing apples, paused with one in her hand, eyes soft — the practice arriving in an ordinary errand."),
     ("ingrid-3","1:1","Macro: her weathered hand resting on a linen knee in even window light, thumb touching the gold band, a mala bead bracelet beside it."),
     ("ingrid-4","3:2","Ingrid teaching, kneeling beside a student, fully attentive, bright airy studio, morning light spread evenly across the wooden floor."),
   ]},
 # 2 — ADHD & focus (segment 2, actively A/B tested)
 "theo": {
   "title": "Theo — one thing at a time",
   "who": ("A 29-year-old software developer named Theo. Short dark curly hair, light olive skin, "
           "wire-rim glasses, a soft sage-green overshirt over a white tee, and a wide polished "
           "gold band on his right ring finger."),
   "frames": [
     ("theo-1","3:2","Theo at a tidy desk by a big window, six browser tabs reflected in his glasses, hand hovering over the trackpad, caught at the exact moment of drift."),
     ("theo-2","4:5","Theo leaning back from the screen, eyes closed for one breath, morning light even across the desk, the noise settling."),
     ("theo-3","1:1","Macro: his hand back on the keyboard, steady, the gold band catching soft daylight, a single closed notebook beside the keyboard."),
     ("theo-4","3:2","Theo deep in one task, the room bright and calm around him, phone face-down and far away on the windowsill."),
   ]},
 # 3 — Habit chaser (segment 3: 'three things that bring me joy every day')
 "rosa": {
   "title": "Rosa — three things a day",
   "who": ("A 34-year-old woman named Rosa. Warm brown skin, black hair in a high bun, bright "
           "curious eyes, gold hoop earrings, a mustard cardigan over a cream top, and a wide "
           "polished gold band on her right ring finger."),
   "frames": [
     ("rosa-1","3:2","Rosa at a sunny kitchen table writing three short lines in a small notebook over coffee, morning light even and generous, a plant on the sill."),
     ("rosa-2","4:5","Rosa pausing on a walk to actually look at a street tree in flower, one hand touching a low branch, soft bright overcast light."),
     ("rosa-3","1:1","Macro: her hand on a warm coffee cup, steam rising in even window light, the gold band and the notebook's ribbon bookmark in frame."),
     ("rosa-4","3:2","Rosa laughing on a stoop with a neighbor in soft afternoon light, present in an unremarkable perfect moment."),
   ]},
 # 4 — Anxiety & stress aid ('I can't just meditate right now')
 "darius": {
   "title": "Darius — calm without the cushion",
   "who": ("A 44-year-old man named Darius. Deep brown skin, close-cropped greying hair and beard, "
           "kind heavy-lidded eyes, an open-collar chambray shirt, and a wide polished gold band "
           "on his right ring finger."),
   "frames": [
     ("darius-1","3:2","Darius on a crowded morning train, shoulders up around his ears, jaw tight, the carriage bright with soft diffuse daylight through big windows."),
     ("darius-2","4:5","Darius still on the same crowded rush-hour commuter train, standing and holding the overhead grab-pole, one breath later than his tension: shoulders visibly lowered, jaw unclenched, eyes softening on the city passing through the train window, the train interior and other standing passengers clearly around him."),
     ("darius-3","1:1","Macro: his hand flat on his chest over the shirt, even soft light, the gold band prominent as a quiet anchor."),
     ("darius-4","3:2","Darius arriving home in early evening, pausing at the door with his keys still in hand, taking the breath before he goes in to his family, light soft and forgiving."),
   ]},
 # 5 — Connection, me->we (shared pulse, gratitude together)
 "amara-ben": {
   "title": "Amara & Ben — the same pulse",
   "who": ("A couple in their mid-30s: Amara, a Black woman with short natural hair, warm open face, "
           "cream ribbed sweater; and Ben, a white man with sandy hair and stubble, soft flannel "
           "overshirt. Each wears a wide polished gold band on their right ring finger."),
   "two": True,
   "frames": [
     ("amara-ben-1","3:2","Amara and Ben in their kitchen on a slow morning, both pausing mid-task at the same moment — she at the counter, he at the table — catching each other's eye and smiling, even soft daylight everywhere."),
     ("amara-ben-2","4:5","Ben saying a quiet thank-you to Amara across the kitchen, her hand on his shoulder, both present, bright diffuse morning light."),
     ("amara-ben-3","1:1","Macro: their two hands loosely joined on a wooden table in even window light, the two gold bands almost touching."),
     ("amara-ben-4","3:2","Evening: the two of them on a sofa in soft lamp-warmed ambient light, phones nowhere, mid-conversation, fully with each other."),
   ]},
}

# Existing dark heroes to relight as -soft variants (scene, aspect, use maya ref)
RELIGHTS = [
 ("email-quiz-results","3:2",True,"Maya in her parked car, engine off, for once not reaching for her phone, gentle morning light filling the car evenly through the windshield, her face soft and clearly lit."),
 ("email-the-moment","3:2",True,"Maya at the kitchen counter at 6:50am buttering toast while her young daughter talks, present in body, the kitchen filled with soft even morning light."),
 ("email-autopilot-cost","3:2",True,"Maya on the sofa in early evening, phone loose in her hand, looking up and away from it toward the window, the room in soft ambient lamplight and daylight mix, gentle and breathable."),
 ("email-come-back-to-now","3:2",False,"The gold ring resting in a small ceramic dish on a bedside table in soft morning light, the room airy and calm, a made bed behind, warm and inviting rather than cold."),
 ("email-no-rush","3:2",True,"Maya's ring sitting on a dresser in soft bright daylight while she passes in the background unhurried, the room light and open."),
]

def main():
    args = sys.argv[1:]
    forced = args[args.index("--model")+1] if "--model" in args else None
    only = args[args.index("--only")+1] if "--only" in args else None
    force = "--force" in args
    key = get_key()
    model = pick_model(key, forced)
    print("Using model:", model)
    OUT.mkdir(exist_ok=True)

    ok, failed, skipped = 0, [], 0
    # story sets
    for skey, story in STORIES.items():
        ref_path = OUT / f"00-{skey}-reference.png"
        ref_b64 = None
        wanted = (not only) or only == skey or any(only == f[0] for f in story["frames"])
        if not wanted: continue
        keep = KEEP2 if story.get("two") else KEEP
        if ref_path.exists() and not force:
            ref_b64 = base64.b64encode(ref_path.read_bytes()).decode()
        else:
            print(f"[{skey}] character reference ...")
            n = "two people, both looking softly toward camera, three-quarter view" if story.get("two") else "looking softly toward camera, three-quarter view"
            img = generate(model, key, f"Editorial character portrait. {story['who']} Neutral warm expression, {n}, even soft window light so the face reads clearly for later reference. {SOFT}", aspect="4:5")
            if img:
                ref_path.write_bytes(img); ref_b64 = base64.b64encode(img).decode(); ok += 1
            else:
                failed.append(f"00-{skey}-reference")
            time.sleep(1)
        for fid, aspect, concept in story["frames"]:
            if only and only not in (skey, fid): continue
            out = OUT / f"{fid}.png"
            if out.exists() and not force:
                skipped += 1; continue
            print(f"[{fid}] ...")
            img = generate(model, key, f"{keep}{concept} {SOFT} Aspect ratio {aspect}.", aspect=aspect, ref_b64=ref_b64)
            if img: out.write_bytes(img); ok += 1
            else: failed.append(fid)
            time.sleep(1)

    # relights
    maya_ref = EMAIL_IMG / "00-maya-reference.png"
    maya_b64 = base64.b64encode(maya_ref.read_bytes()).decode() if maya_ref.exists() else None
    for slug, aspect, use_ref, concept in RELIGHTS:
        if only and only != slug: continue
        out = EMAIL_IMG / f"hero-{slug}-soft.png"
        if out.exists() and not force:
            skipped += 1; continue
        print(f"[relight {slug}] ...")
        img = generate(model, key, f"{KEEP if use_ref else ''}{concept} {SOFT} Aspect ratio {aspect}.",
                       aspect=aspect, ref_b64=(maya_b64 if use_ref else None))
        if img: out.write_bytes(img); ok += 1
        else: failed.append(f"relight-{slug}")
        time.sleep(1)

    gallery()
    print(f"\nDone. generated={ok} skipped={skipped} failed={len(failed)}")
    for f in failed: print("  failed:", f)

def gallery():
    imgs = sorted(p.name for p in OUT.glob("*.png"))
    rows = "".join(f'<figure><img src="{n}"/><figcaption>{n}</figcaption></figure>' for n in imgs)
    (OUT/"gallery.html").write_text(f"""<!doctype html><meta charset=utf-8><title>Pulse user stories</title>
<style>body{{background:#EBE7D4;font-family:'DM Sans',system-ui;margin:0;padding:40px;color:#1A1C22}}
h1{{font-weight:600;letter-spacing:-.04em}} .grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}}
figure{{margin:0;background:#F9F6E5;border-radius:14px;overflow:hidden;box-shadow:0 12px 30px rgba(66,61,50,.10)}}
img{{width:100%;display:block}} figcaption{{font:11px ui-monospace,monospace;color:#6E6857;padding:10px 12px}}</style>
<h1>Pulse — five user stories, soft light</h1><div class=grid>{rows}</div>""")

if __name__ == "__main__":
    main()
