#!/usr/bin/env python3
"""
Pulse — Peak experiences (out in the world, dramatic locations)
===============================================================
Doubling the user-story imagery with visually stunning, out-in-the-world,
peak-life moments: a real person fully PRESENT in a dramatic location — the
kind of moment the ring returns you to. Cinematic, breathtaking, but still the
Pulse grammar (warm, editorial, the gold ring a discovered glint).

USAGE
  python3 tools/generate-peak.py [--only <id>] [--model gemini-3.1-flash-image] [--force]
Output: library/peak/<id>.png
"""
import os, sys, json, base64, urllib.request, urllib.error, pathlib, time

API_ROOT="https://generativelanguage.googleapis.com/v1beta"
ROOT=pathlib.Path(__file__).resolve().parent.parent
OUT=ROOT/"library"/"peak"

def get_key():
    k=os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if k: return k.strip()
    f=pathlib.Path.home()/".gemini_api_key"
    if f.exists(): return f.read_text().strip()
    sys.exit("No Gemini key found.")
def api(path,key,body=None):
    req=urllib.request.Request(f"{API_ROOT}/{path}",data=(json.dumps(body).encode() if body is not None else None),method="POST" if body is not None else "GET")
    req.add_header("x-goog-api-key",key); req.add_header("Content-Type","application/json")
    with urllib.request.urlopen(req,timeout=180) as r: return json.loads(r.read().decode())
def pick_model(key,forced=None):
    if forced: return forced
    models=api("models",key).get("models",[])
    img=[m.get("name","").split("/")[-1] for m in models if "generateContent" in m.get("supportedGenerationMethods",[]) and "image" in m.get("name","").lower()]
    def rank(n):
        n=n.lower()
        if "3.1" in n and "flash" in n and "image" in n and "lite" not in n: return 0
        if "3" in n and "pro" in n and "image" in n: return 1
        if "flash" in n and "image" in n: return 2
        return 9
    img.sort(key=rank); return img[0] if img else sys.exit("no image models")
def generate(model,key,prompt,aspect="3:2",tries=3):
    base={"contents":[{"role":"user","parts":[{"text":prompt}]}]}
    for cfg in [{"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":aspect}}},
                {"generationConfig":{"responseModalities":["TEXT","IMAGE"]}},{}]:
        body=dict(base); body.update(cfg)
        for a in range(tries):
            try:
                resp=api(f"models/{model}:generateContent",key,body)
                for c in resp.get("candidates",[]):
                    for p in c.get("content",{}).get("parts",[]):
                        d=p.get("inlineData") or p.get("inline_data")
                        if d and d.get("data"): return base64.b64decode(d["data"])
                break
            except urllib.error.HTTPError as e:
                if e.code in (429,500,503): time.sleep(3*(a+1)); continue
                break
            except Exception: time.sleep(2); continue
    print("    ! failed"); return None

RING="wearing a wide, smooth, polished gold band — the Pulse ring — on the finger"
STYLE=("Breathtaking, cinematic, visually stunning — but real and un-staged, medium-format film, warm and "
       "editorial, never stocky. Vast natural drama with intimate human presence. Warm honey and cream tones "
       "even in cool light, fine grain, soft highlight bloom. The person is genuinely PRESENT in the moment, "
       "not posing. The gold ring reads as a discovered second-glance glint. No text, no logos, no watermark.")

# (id, aspect, scene) — a real person, fully present, in a stunning place.
SCENES=[
 ("peak-summit-sunrise","3:2","a hiker standing on a mountain summit at sunrise, arms loose, breathing the vast light spilling over a sea of clouds and distant peaks, "+RING+"."),
 ("peak-waterfall","3:2","a woman standing at the misty base of an enormous jungle waterfall, face tilted up into the spray and green light, awestruck and present, "+RING+"."),
 ("peak-aurora","16:9","a person on a snowfield at night under a blazing green-and-violet aurora, head tipped back in wonder, breath visible, "+RING+" catching the glow."),
 ("peak-dunes","3:2","a lone figure atop a towering desert dune at golden hour, wind lifting sand off the ridge, immense sky, still and awed, "+RING+"."),
 ("peak-cliff-ocean","16:9","a woman sitting on a grassy sea cliff at golden hour, legs over the edge, the ocean vast and glittering below, wholly at peace, "+RING+"."),
 ("peak-balloon","3:2","a man leaning from a hot-air-balloon basket at dawn over a patchwork valley and river of mist, mouth open in delight, "+RING+" on the rail hand."),
 ("peak-glacier","3:2","a climber pausing on a blue glacier under a huge sky, ice glowing, taking one breath of the enormity, "+RING+"."),
 ("peak-saltflat","16:9","a person standing on a mirror-still salt flat at sunset, sky and ground merging into endless gold, a single small figure, "+RING+"."),
 ("peak-redwoods","3:2","a woman standing small among towering redwoods with god-rays of morning light coming down through the canopy, head back, "+RING+"."),
 ("peak-alpine-swim","3:2","a swimmer surfacing in a turquoise alpine lake ringed by snow peaks, gasping with joy in the cold bright light, "+RING+" on a lifted hand."),
 ("peak-canyon-rim","16:9","a hiker at the rim of an immense red canyon at golden hour, sitting quietly with the vastness, warm light raking the walls, "+RING+"."),
 ("peak-rooftop-dusk","16:9","a young woman on a city rooftop at blue-gold dusk, the whole skyline lit below her, wind in her hair, fully alive, "+RING+"."),
 ("peak-festival-aerial","16:9","a joyful crowd at a music festival from a high angle at golden hour, dust and light, one person in the foreground arms raised, present, "+RING+"."),
 ("peak-sailing","3:2","a man at the bow of a small sailboat heeling into golden-hour swell, spray and light, laughing into the wind, "+RING+" on the rail hand."),
 ("peak-superbloom","3:2","a woman walking through a desert super-bloom of wildflowers to the horizon under soft dawn light, trailing a hand over the blooms, "+RING+"."),
 ("peak-bioluminescent","16:9","a person wading at night in a bioluminescent shoreline, blue light glowing around their steps under a milky-way sky, awed, "+RING+"."),
 ("peak-temple-dawn","3:2","a traveler sitting quietly on ancient temple steps at dawn as mist lifts over jungle and stone, deeply present, warm first light, "+RING+"."),
 ("peak-northern-fjord","16:9","a person on a rock over a still fjord at golden hour, sheer cliffs and mirror water, tiny against the scale, calm and full, "+RING+"."),
 ("peak-hammock-forest","3:2","a woman in a hammock strung between huge trees over a valley at golden hour, one arm hanging, utterly at ease, "+RING+"."),
 ("peak-surf-dawn","3:2","a surfer sitting on their board in glassy dawn swell facing a pink-gold horizon, still, breathing, "+RING+" on a hand resting on the board."),
 ("peak-meadow-storm","16:9","a person in a mountain meadow watching distant golden light break under a dramatic clearing storm, wildflowers around them, awed, "+RING+"."),
 ("peak-city-lookout","3:2","a couple at a mountain lookout above a glittering city at night, leaning together, the valley of lights below, present with each other, "+RING+" on both."),
 ("peak-desert-stars","16:9","a person lying back on warm desert rock under an overwhelming field of stars, arms wide, tiny and content, "+RING+"."),
 ("peak-riverbend","3:2","a fly-fisher standing mid-river in a golden canyon at first light, line curling, wholly absorbed in the moment, "+RING+"."),
 ("peak-lavender","16:9","a woman walking a path through endless rows of lavender to a distant hilltop at golden hour, hand trailing the blooms, serene, "+RING+"."),
 ("peak-iceberg-kayak","3:2","a kayaker paused among glowing blue icebergs in still water under soft arctic light, paddle resting, breath held, "+RING+"."),
 ("peak-terraces","16:9","a traveler standing on ancient rice terraces at dawn, mist in the valleys, green steps falling away for miles, quietly moved, "+RING+"."),
 ("peak-thermal-dawn","3:2","a person soaking in a steaming natural hot spring at dawn with snow peaks around, steam and gold light, deeply at rest, "+RING+" on a hand on the rim."),
 ("peak-cave-light","16:9","a caver standing in a shaft of daylight falling into a vast cavern, dust and glow, small against the scale, awed, "+RING+"."),
 ("peak-savanna","16:9","a traveler on a jeep roof at golden hour on the savanna, acacia silhouettes and a herd in the distance, wind and warm light, present, "+RING+"."),
 ("peak-cherry-blossom","3:2","a woman under a huge cherry tree in full bloom as petals fall in soft light, face up and eyes closed, catching the moment, "+RING+"."),
 ("peak-lighthouse-storm","16:9","a person on a headland by a lighthouse as golden light breaks over a big sea after a storm, coat whipping, alive, "+RING+"."),
 ("peak-vineyard-dusk","3:2","two friends walking a vineyard row at dusk with the hills gold behind, wine in hand, laughing, fully in the evening, "+RING+"."),
 ("peak-mountain-tent","3:2","a person sitting in the door of a tent at a high camp at golden hour, boots off, a mug in hand, the range glowing, content, "+RING+"."),
 ("peak-tide-pools","3:2","a woman crouched at glowing tide pools at sunset, fingers just touching the water, the sea gold behind, absorbed, "+RING+"."),
 ("peak-forest-fog","16:9","a hiker on a ridge trail as fog pours through a golden pine forest below, standing still to watch it move, "+RING+"."),
 ("peak-desert-road","16:9","a person standing on the roof of a van on an empty desert road at golden hour, arms out, immense sky, freedom, "+RING+"."),
 ("peak-glacial-river","3:2","a traveler crossing a footbridge over a roaring turquoise glacial river in a green valley, pausing mid-span to look, "+RING+"."),
 ("peak-monastery","3:2","a person on a cliffside monastery terrace at dawn, prayer flags in the wind, valley of cloud below, deeply still, "+RING+"."),
 ("peak-wheatfield-gold","16:9","a woman walking into a wheat field glowing at golden hour, hands brushing the tops, the sun huge and low, present, "+RING+"."),
 ("peak-frozen-lake","16:9","a skater alone on a vast frozen mountain lake at golden hour, long shadow, tiny in the scale, exhilarated and calm, "+RING+"."),
 ("peak-jungle-river","3:2","a traveler standing waist-deep in a clear jungle river pool beneath vines and light shafts, arms floating, awed, "+RING+"."),
 ("peak-mesa-sunset","16:9","a person seated cross-legged on a red mesa edge at sunset, the desert burning gold below, wholly at peace, "+RING+"."),
 ("peak-coastal-run","3:2","a runner cresting a coastal headland trail at sunrise, ocean vast and gold, stopping to breathe it in, "+RING+"."),
 ("peak-observatory","16:9","a person on a dark mountaintop beside a telescope under the milky way, head back in wonder, faint warm headlamp glow, "+RING+"."),
 ("peak-paddleboard-mist","3:2","a paddleboarder gliding across a mirror-still misty lake at dawn, one knee down, breath held in the quiet, "+RING+"."),
 ("peak-mountain-picnic","3:2","a couple on a blanket at a high alpine meadow with peaks and lake below at golden hour, leaning together, present, "+RING+" on both."),
 ("peak-dune-descent","16:9","a person running down a giant sand dune at sunset laughing, sand spraying gold, pure aliveness, "+RING+"."),
]

def gallery():
    imgs=sorted(p.name for p in OUT.glob("*.png"))
    rows="".join(f'<figure><img src="{n}"/><figcaption>{n}</figcaption></figure>' for n in imgs)
    (OUT/"gallery.html").write_text("<!doctype html><meta charset=utf-8><title>Pulse — peak</title>"
     "<style>body{background:#EBE7D4;font-family:system-ui;margin:0;padding:30px}"
     ".grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}figure{margin:0}img{width:100%;display:block;border-radius:8px}"
     "figcaption{font:11px monospace;color:#6E6857;padding:5px}</style>"
     "<h2>Peak experiences — out in the world</h2><div class=grid>"+rows+"</div>")

def main():
    args=sys.argv[1:]
    forced=args[args.index("--model")+1] if "--model" in args else None
    only=args[args.index("--only")+1] if "--only" in args else None
    force="--force" in args
    key=get_key(); model=pick_model(key,forced); print("model:",model)
    OUT.mkdir(parents=True,exist_ok=True)
    ok,failed,skip=0,[],0
    for cid,aspect,scene in SCENES:
        if only and only!=cid: continue
        out=OUT/f"{cid}.png"
        if out.exists() and not force: skip+=1; continue
        print(f"[{cid}]")
        img=generate(model,key,f"{scene} {STYLE} Aspect ratio {aspect}.",aspect=aspect)
        if img: out.write_bytes(img); ok+=1
        else: failed.append(cid)
        time.sleep(1)
    gallery()
    print(f"\nDone. generated={ok} skipped={skip} failed={len(failed)} total={len(SCENES)}")
    for f in failed: print("  failed:",f)

if __name__=="__main__": main()
