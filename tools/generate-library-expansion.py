#!/usr/bin/env python3
"""
Pulse — Library expansion generator
====================================
Three collections that dramatically widen the image library:

  A. AVATARS      — a diverse cast of storytellers (soft ambient portraits),
                    the faces behind testimonials + email personas.
  B. PERFORMANCE  — the ring inside flow / peak-presence moments across
                    disciplines (run, climb, play, cook, create, compete).
  C. ETHEREAL     — the ring as a SYMBOL of presence: no people, surreal
                    light-leak B-roll where the band changes the light, the
                    water, the whole room. Editorial, subtle, larger-than-life.
                    (Grammar ported from the testimonial studio's PULSE_BROLL_STYLE.)

USAGE
  python3 tools/generate-library-expansion.py            # all missing
  python3 tools/generate-library-expansion.py --only <id>
  python3 tools/generate-library-expansion.py --collection ethereal
  python3 tools/generate-library-expansion.py --model gemini-3.1-flash-image
Outputs: library/{avatars,performance,ethereal}/<id>.png + per-collection galleries.
"""
import os, sys, json, base64, urllib.request, urllib.error, pathlib, time

API_ROOT = "https://generativelanguage.googleapis.com/v1beta"
ROOT = pathlib.Path(__file__).resolve().parent.parent
LIB = ROOT / "library"

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
    req.add_header("x-goog-api-key", key); req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode())

def pick_model(key, forced=None):
    if forced: return forced
    models = api("models", key).get("models", [])
    img = [m.get("name","").split("/")[-1] for m in models
           if "generateContent" in m.get("supportedGenerationMethods",[]) and "image" in m.get("name","").lower()]
    def rank(n):
        n=n.lower()
        if "3" in n and "pro" in n and "image" in n: return 0
        if "nano" in n and "banana" in n: return 1
        if "3.1" in n and "flash" in n and "image" in n and "lite" not in n: return 2
        if "flash" in n and "image" in n: return 3
        return 9
    img.sort(key=rank)
    if not img: sys.exit("No image models.")
    return img[0]

def generate(model, key, prompt, aspect="3:2", tries=3):
    base_body = {"contents": [{"role":"user","parts":[{"text":prompt}]}]}
    configs = [
        {"generationConfig": {"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":aspect}}},
        {"generationConfig": {"responseModalities":["TEXT","IMAGE"]}},
        {},
    ]
    last=None
    for cfg in configs:
        body=dict(base_body); body.update(cfg)
        for attempt in range(tries):
            try:
                resp=api(f"models/{model}:generateContent", key, body)
                for cand in resp.get("candidates",[]):
                    for p in cand.get("content",{}).get("parts",[]):
                        d=p.get("inlineData") or p.get("inline_data")
                        if d and d.get("data"): return base64.b64decode(d["data"])
                last="no image part"; break
            except urllib.error.HTTPError as e:
                last=f"HTTP {e.code}"
                if e.code in (429,500,503): time.sleep(3*(attempt+1)); continue
                break
            except Exception as e:
                last=str(e); time.sleep(2); continue
    print(f"    ! failed: {last}"); return None

# ---------------------------------------------------------------- grammar
RING = ("a wide, smooth, polished gold band — the Pulse ring — on the finger")

SOFT = ("Soft ambient natural light, diffuse and even, airy and breathable, lifted gentle shadows. "
        "Luminous cream, honey and warm oatmeal palette, a faint dusty-blue only in the deepest shadow. "
        "Medium-format film photograph, fine natural grain, shallow depth of field, soft highlight bloom. "
        "Calm, unhurried, real and un-staged, editorial. The gold band reads as a discovered "
        "second-glance glint, never centered. No text, no logos, no watermark.")

# The ethereal / B-roll grammar, ported from the studio's PULSE_BROLL_STYLE
ETHEREAL = ("Larger than life yet natural and real, slightly surreal — the way a moment feels in "
            "memory rather than how a camera saw it. Warm golden-hour light, generous natural light "
            "leaks and lens flares blooming across the frame, drifting dust and haze catching the sun. "
            "Medium-format film look, fine natural grain, shallow depth of field, soft highlight bloom. "
            "Muted cream, honey and charcoal palette with a faint dusty-blue in the deepest shadow. "
            "Poetic, ethereal, editorial and subtle. Scale and physics gently bend: light behaves like "
            "water, a room breathes with light. No text, no logos, no people, no watermark.")

# ---- Collection A: avatars (diverse storytellers) ----
AVATARS = [
 ("avatar-01","4:5","A 27-year-old East Asian man, warm smile, cropped hair, olive linen shirt, at a sunlit cafe table, "+RING+", relaxed and present, looking softly toward camera."),
 ("avatar-02","4:5","A 61-year-old Black woman with silver locs, reading glasses pushed up, mustard scarf, in a bright plant-filled room, "+RING+", serene and warm."),
 ("avatar-03","4:5","A 34-year-old Latina woman, dark wavy hair, freckles, cream turtleneck, by a large window, "+RING+", calm half-smile."),
 ("avatar-04","4:5","A 45-year-old white man with a greying beard, soft flannel, in a woodshop doorway in daylight, "+RING+", grounded and kind."),
 ("avatar-05","4:5","A 23-year-old South Asian woman, long dark hair, gold nose stud, sage sweater, on a bright balcony, "+RING+", quietly confident."),
 ("avatar-06","4:5","A 52-year-old Middle Eastern man, salt-and-pepper hair, open-collar shirt, in a light-filled study, "+RING+", thoughtful and settled."),
 ("avatar-07","4:5","A 30-year-old white woman with red curly hair, denim shirt, at a farmers-market stall in soft daylight, "+RING+", bright and open."),
 ("avatar-08","4:5","A 38-year-old Black man, clean fade, charcoal henley, in a sunlit kitchen, "+RING+", easy warmth, mid-laugh softening."),
 ("avatar-09","4:5","A 68-year-old white woman with a soft white bob, linen apron, in a bright pottery studio, "+RING+", peaceful and present."),
 ("avatar-10","4:5","A 29-year-old mixed-race nonbinary person, short curly hair, oversized oatmeal cardigan, by a rain-streaked window with soft light, "+RING+", gentle and self-possessed."),
]

# ---- Collection B: performance / flow (people, the pause inside peak presence) ----
PERFORMANCE = [
 ("perf-run","3:2","A runner stopped at the top of a hill at dawn, hands on knees then rising to stand tall, breathing, city soft below, "+RING+" catching first light. The pause inside the effort."),
 ("perf-climb","3:2","A rock climber at a belay ledge, chalked hand resting on the rope, eyes closed for one breath before the next move, warm canyon light, "+RING+" on the resting hand."),
 ("perf-piano","3:2","A pianist's hands lifted a beat above the keys in a sunlit hall, the held silence before the phrase, "+RING+" on one hand, dust in the light."),
 ("perf-surgeon","3:2","A surgeon at the scrub sink before the case, water running over still hands, a single steadying breath, clean bright clinical light softened, "+RING+" just visible."),
 ("perf-chef","3:2","A chef alone at the pass before service, both palms flat on the steel, head bowed for one grounding second, warm kitchen light, "+RING+" on one hand."),
 ("perf-dancer","3:2","A dancer in the wings, forehead resting against the cool pole, gathering stillness before the entrance, warm stage-edge glow, "+RING+" on the hand at rest."),
 ("perf-speaker","3:2","A founder backstage before a talk, standing quiet with eyes closed, one hand over the sternum, warm side light, "+RING+" on that hand — presence before performance."),
 ("perf-ice","3:2","An athlete stepping out of an ice bath, breath visible, shoulders dropping as the body settles, soft locker-room daylight, "+RING+" on a dripping hand."),
]

# ---- Collection C: ethereal / ring-as-presence B-roll (no people) ----
ETHEREAL_SET = [
 ("eth-water-drop","3:2","Extreme macro: a single water droplet clinging to the gold Pulse band on dark still water, the droplet refracting a whole golden-hour landscape inside it. Presence held in one drop."),
 ("eth-ripples","3:2","The gold Pulse band resting half-submerged in a shallow bowl of still water, concentric rings of light spreading outward from it across the surface, a room's warm light rippling on the water."),
 ("eth-tide","16:9","The gold band alone on wet sand at the edge of an impossibly golden tide, a thin sheet of luminous water sliding toward it and pausing, light leaking across the frame like memory."),
 ("eth-room-warms","16:9","A plain grey room at dawn with the gold band on a windowsill; from the band, warmth spreads across the walls, cool blue becoming honey gold, the room breathing with light. Environment changed by presence."),
 ("eth-threads","3:2","The gold band on dark linen with fine threads of golden light radiating outward from it into the shadow, like the pulse of a quiet signal made visible. Subtle, editorial."),
 ("eth-submerged","3:2","The gold band suspended in clear water, sunlight from above breaking into caustic gold nets across it and the sandy floor below, slow drifting particles, weightless and calm."),
 ("eth-condensation","3:2","Macro: the gold band on a cold windowpane at dawn, a bloom of condensation around it, and where its warmth touches, the fog clears into a small circle of golden morning beyond."),
 ("eth-leaf-light","3:2","The gold band resting in an open palm-shaped hollow of a large leaf, light through the canopy dappling it, one lime-lit translucent leaf edge, golden dust adrift. Nature holding presence."),
 ("eth-pool-dawn","16:9","The wide polished gold Pulse ring resting on the smooth stone edge of a still dawn pool, warm steam rising, the water a sheet of soft gold, one clean concentric ripple spreading outward from directly beneath the ring. Photographed on medium-format film, warm and soft, not CGI. Only ONE gold ring, clearly the wide band, no floating rectangles or frames."),
 ("eth-candle-mirror","3:2","The gold band on a dark reflective surface with one soft warm light source, its reflection doubling into a luminous figure-eight, honey bloom, deep quiet shadow. Product, elevated to symbol."),
 ("eth-sand-hourglass","3:2","The gold band lying in warm pale sand as a thin fall of golden sand streams past it and slows, hanging a beat too long in the light. Time softened around presence."),
 ("eth-window-tide","16:9","A calm interior at golden hour, warm light pouring through a window and pooling like liquid gold across a wooden floor, the wide polished gold Pulse ring resting in the brightest pool of light casting a long soft reflection. Medium-format film grain, soft and warm, painterly not CGI. One clear gold ring, large and legible in frame."),
]

COLLECTIONS = {
 "avatars": (AVATARS, SOFT, LIB/"avatars"),
 "performance": (PERFORMANCE, SOFT, LIB/"performance"),
 "ethereal": (ETHEREAL_SET, ETHEREAL, LIB/"ethereal"),
}

def build(concept, style, aspect):
    return f"{concept} Colour, light and feel: {style} Aspect ratio {aspect}."

def gallery(outdir, title):
    imgs=sorted(p.name for p in outdir.glob("*.png"))
    rows="".join(f'<figure><img src="{n}"/><figcaption>{n}</figcaption></figure>' for n in imgs)
    (outdir/"gallery.html").write_text(f"""<!doctype html><meta charset=utf-8><title>{title}</title>
<style>body{{background:#EBE7D4;font-family:'DM Sans',system-ui;margin:0;padding:40px;color:#1A1C22}}
h1{{font-weight:600;letter-spacing:-.04em}} .grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}}
figure{{margin:0;background:#F9F6E5;border-radius:14px;overflow:hidden;box-shadow:0 12px 30px rgba(66,61,50,.10)}}
img{{width:100%;display:block}} figcaption{{font:11px ui-monospace,monospace;color:#6E6857;padding:10px 12px}}</style>
<h1>{title}</h1><div class=grid>{rows}</div>""")

def main():
    args=sys.argv[1:]
    forced=args[args.index("--model")+1] if "--model" in args else None
    only=args[args.index("--only")+1] if "--only" in args else None
    coll=args[args.index("--collection")+1] if "--collection" in args else None
    force="--force" in args
    key=get_key(); model=pick_model(key, forced)
    print("Using model:", model)
    ok,failed,skipped=0,[],0
    for cname,(items,style,outdir) in COLLECTIONS.items():
        if coll and coll!=cname: continue
        outdir.mkdir(parents=True, exist_ok=True)
        for cid,aspect,concept in items:
            if only and only!=cid: continue
            out=outdir/f"{cid}.png"
            if out.exists() and not force: skipped+=1; continue
            print(f"[{cname}/{cid}] ...")
            img=generate(model,key,build(concept,style,aspect),aspect=aspect)
            if img: out.write_bytes(img); ok+=1; print(f"  -> {out.name}")
            else: failed.append(cid)
            time.sleep(1)
        gallery(outdir, f"Pulse library — {cname}")
    print(f"\nDone. generated={ok} skipped={skipped} failed={len(failed)}")
    for f in failed: print("  failed:", f)

if __name__=="__main__":
    main()
