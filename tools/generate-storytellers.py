#!/usr/bin/env python3
"""
Pulse — Storytellers "in life" (dramatically expanded)
======================================================
The portrait avatars (library/avatars/) are the headshots. This is the big
scene collection: the same kind of real, diverse people, but LIVING — at
festivals, the gym, making music, painting, dancing, an intimate date night,
and more. Present in the moment, the wide gold Pulse ring a discovered glint.

Data-driven: to add more, append (id, scene) tuples to SCENES. The runner
skips anything already generated, so it resumes cleanly after a credit refill.

USAGE
  python3 tools/generate-storytellers.py [--only <id>] [--model gemini-3.1-flash-image] [--force]
Output: library/storytellers/<id>.png (+ gallery.html)
"""
import os, sys, json, base64, urllib.request, urllib.error, pathlib, time

API_ROOT="https://generativelanguage.googleapis.com/v1beta"
ROOT=pathlib.Path(__file__).resolve().parent.parent
OUT=ROOT/"library"/"storytellers"

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

RING="wearing a wide, smooth, polished gold band — the Pulse ring — clearly on the finger"
STYLE=("Warm ambient natural light, medium-format film photograph, fine natural grain, shallow depth "
       "of field, soft highlight bloom, luminous cream and honey palette with real colour where the "
       "scene calls for it. Editorial, alive, un-staged, emotionally true — never stocky. The gold "
       "band is a discovered second-glance glint. No text, no logos, no watermark.")

# (id, aspect, scene) — diverse people, present in a living moment. Grouped by activity.
SCENES=[
 # festivals
 ("fest-01","3:2","A 28-year-old Black woman at an outdoor music festival at golden hour, eyes closed, arms loosely raised, fully inside the music, warm dust and low sun, "+RING+"."),
 ("fest-02","3:2","A 45-year-old white man at a conscious wellness festival in a field, sitting cross-legged in a drum circle mid-beat, laughing, "+RING+"."),
 ("fest-03","4:5","A 23-year-old South Asian woman on a friend's shoulders at a festival crowd, backlit by stage light, pure joy, "+RING+"."),
 ("fest-04","3:2","A 34-year-old Latino man at a twilight festival, string lights bokeh behind, mid-laugh with friends, present, "+RING+"."),
 ("fest-05","3:2","A 60-year-old white woman with silver hair dancing barefoot on festival grass at sunset, skirt in motion, free, "+RING+"."),
 # gym / movement
 ("gym-01","4:5","A 30-year-old Black man resting between sets in a sunlit gym, chalked hands on a barbell, one grounding breath, "+RING+"."),
 ("gym-02","3:2","A 38-year-old white woman mid-stretch in a bright studio after a workout, calm and strong, sweat and soft light, "+RING+"."),
 ("gym-03","4:5","A 26-year-old Filipina woman climbing a bouldering wall, paused at a hold, focused and present, warm gym light, "+RING+"."),
 ("gym-04","3:2","A 52-year-old Middle Eastern man doing tai chi in a park at dawn, slow deliberate motion, mist and low sun, "+RING+"."),
 # playing music
 ("music-01","3:2","A 29-year-old white woman playing an upright piano by a sunlit window, lost in the phrase, "+RING+" on a hand on the keys."),
 ("music-02","4:5","A 40-year-old Black man playing acoustic guitar on a porch at golden hour, eyes closed, singing softly, "+RING+"."),
 ("music-03","3:2","A 33-year-old Korean woman with a cello in a warm rehearsal room, bow mid-stroke, fully absorbed, "+RING+"."),
 ("music-04","3:2","A 24-year-old Latino man at a drum kit in a sunlit garage, mid-fill, grinning, motion and warm light, "+RING+"."),
 ("music-05","4:5","A 67-year-old white man playing harmonica on a stoop, weathered joy, soft evening light, "+RING+"."),
 # painting / making
 ("art-01","3:2","A 47-year-old Black woman painting a large canvas in a bright studio, brush raised, paint on her hands, absorbed, "+RING+"."),
 ("art-02","4:5","A 31-year-old white man throwing clay on a wheel, hands wet and muddy, calm focus, warm studio light, "+RING+"."),
 ("art-03","3:2","A 55-year-old Japanese woman doing calligraphy at a sunlit table, brush poised, total presence, "+RING+"."),
 ("art-04","4:5","A 22-year-old mixed-race person sketching in a notebook in a cafe window, warm light, lost in it, "+RING+"."),
 # expanding / expansive
 ("expand-01","3:2","A 36-year-old white woman standing at a mountain ridge at sunrise, arms wide, breathing in the vast light, "+RING+"."),
 ("expand-02","3:2","A 44-year-old Black man on a rooftop at golden hour, face up to the sky, chest open, a full breath, "+RING+"."),
 ("expand-03","4:5","A 29-year-old Indian woman on a cliff path by the sea, wind and warm light, arms loose and open, alive, "+RING+"."),
 # dancing
 ("dance-01","3:2","A 32-year-old Black woman dancing alone in a sunlit kitchen, coffee forgotten, mid-spin, joy, "+RING+"."),
 ("dance-02","4:5","A 27-year-old Latina woman in a dance studio, mid-movement, warm window light, expressive and free, "+RING+"."),
 ("dance-03","3:2","A 58-year-old white couple slow-dancing in their living room at dusk, foreheads touching, tender, "+RING+" on both."),
 ("dance-04","3:2","A 24-year-old white man dancing at a house party in warm lamplight, head back, laughing, present, "+RING+"."),
 # date-night intimacy (tasteful, sensual)
 ("date-01","3:2","A couple in their 30s at an intimate candlelit dinner, leaning close across the table, eyes locked, tender charged attention, warm low light, "+RING+" on a hand touching a hand."),
 ("date-02","4:5","A couple at home on a low-lit evening, foreheads together on a sofa, a private laugh, sensual warmth and closeness, "+RING+"."),
 ("date-03","3:2","A tender morning-after moment, a couple wrapped in white linen in soft window light, one hand resting on the other's chest, intimate and warm, "+RING+"."),
 ("date-04","4:5","Two women in their 40s slow, close, cheek to cheek in golden kitchen light, a private tender moment, "+RING+"."),
 ("date-05","3:2","A couple on a rooftop at night sharing a blanket and a bottle, close and quiet under warm string lights, present with each other, "+RING+"."),
 # more of everyday life
 ("life-cook-01","3:2","A 50-year-old Latino man cooking with music on in a warm kitchen, tasting from a spoon, eyes closed, savoring, "+RING+"."),
 ("life-garden-01","4:5","A 63-year-old Black woman in her garden at golden hour, hands in soil, a satisfied pause, warm light, "+RING+"."),
 ("life-water-01","3:2","A 35-year-old white woman swimming in a lake at dawn, surfacing with a gasp and a grin, gold light on water, "+RING+"."),
 ("life-kids-01","3:2","A 39-year-old Indian man lifting a laughing toddler overhead in a sunlit backyard, both delighted, "+RING+"."),
 ("life-friends-01","3:2","Four friends of different ethnicities laughing hard around a rooftop table at sunset, mid-story, wine and warm light, "+RING+"."),
 ("life-read-01","4:5","A 70-year-old white man reading in a sunlit armchair, glasses down, caught smiling at a page, "+RING+"."),
 ("life-coffee-01","3:2","A 26-year-old Black woman at a cafe window with coffee, watching the street with soft open attention, warm light, "+RING+"."),
 ("life-hike-01","3:2","A 42-year-old Asian man pausing on a forest trail, hand on a mossy trunk, breathing the green light, "+RING+"."),
 ("life-yoga-01","4:5","A 48-year-old white woman in a gentle yoga pose on a sunlit wooden floor, eyes closed, serene, "+RING+"."),
 ("life-surf-01","3:2","A 31-year-old Latina woman sitting on a surfboard in calm dawn water, facing the sunrise, still and present, "+RING+"."),
]

def gallery():
    imgs=sorted(p.name for p in OUT.glob("*.png"))
    rows="".join(f'<figure><img src="{n}"/><figcaption>{n}</figcaption></figure>' for n in imgs)
    (OUT/"gallery.html").write_text(f"""<!doctype html><meta charset=utf-8><title>Pulse — storytellers in life</title>
<style>body{{background:#EBE7D4;font-family:'DM Sans',system-ui;margin:0;padding:40px;color:#1A1C22}}
h1{{font-weight:600;letter-spacing:-.04em}} .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px}}
figure{{margin:0;background:#F9F6E5;border-radius:12px;overflow:hidden;box-shadow:0 12px 30px rgba(66,61,50,.08)}}
img{{width:100%;display:block}} figcaption{{font:10.5px ui-monospace,monospace;color:#6E6857;padding:8px 11px}}</style>
<h1>Storytellers, in life ({len(imgs)})</h1><div class=grid>{rows}</div>""")

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
    print(f"\nDone. generated={ok} skipped={skip} failed={len(failed)} total_defined={len(SCENES)}")
    for f in failed: print("  failed:",f)

if __name__=="__main__": main()
