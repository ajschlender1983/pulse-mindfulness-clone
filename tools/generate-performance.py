#!/usr/bin/env python3
"""
Pulse — Performance: "the pause inside the effort" (5x)
=======================================================
The still, present breath in the middle of exertion or high-stakes performance.
8 originals kept + 32 new = 40. Skip-if-exists preserves the good originals;
delete a file (e.g. perf-piano.png) to regenerate it with the corrected prompt.

USAGE
  python3 tools/generate-performance.py [--only <id>] [--model gemini-3.1-flash-image] [--force]
Output: library/performance/<id>.png
"""
import os, sys, json, base64, urllib.request, urllib.error, pathlib, time

API_ROOT="https://generativelanguage.googleapis.com/v1beta"
ROOT=pathlib.Path(__file__).resolve().parent.parent
OUT=ROOT/"library"/"performance"

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
    return None

RING="a wide, smooth, polished gold band — the Pulse ring — on the finger"
STYLE=("Warm, editorial, un-staged — medium-format film, soft ambient natural light, honey and cream tones, "
       "fine grain, gentle highlight bloom, real and intimate. The pause inside the effort: a genuine, quiet, "
       "present breath in the middle of exertion or a high-stakes moment. "
       "ANATOMY: hands and bodies must be anatomically correct and natural — correct number of fingers, natural "
       "finger curl and wrist orientation, no reversed or backward hands, no distortion. "
       "No text, no logos, no watermark.")

PERF=[
 # --- 8 originals (kept via skip-if-exists; perf-piano rewritten & regenerated) ---
 ("perf-run","A runner stopped at the top of a hill at dawn, hands on knees then rising to stand tall, breathing, the city soft below, "+RING+" catching first light. The pause inside the effort."),
 ("perf-climb","A rock climber at a belay ledge, chalked hand resting on the rope, eyes closed for one breath before the next move, warm canyon light, "+RING+" on the resting hand."),
 ("perf-piano","A pianist seated at a grand piano in a sunlit hall, seen from a warm three-quarter angle, both hands resting lightly and naturally on the keys in correct playing position, the held silence before the phrase, dust drifting in the light, "+RING+" on one hand. Natural anatomically-correct hands, fingers curved naturally over the keys."),
 ("perf-surgeon","A surgeon at the scrub sink before the case, water running over still hands, a single steadying breath, clean bright clinical light softened, "+RING+" just visible."),
 ("perf-chef","A chef alone at the pass before service, both palms flat on the steel counter, head bowed for one grounding second, warm kitchen light, "+RING+" on one hand."),
 ("perf-dancer","A dancer in the wings, forehead resting against the cool pole, gathering stillness before the entrance, warm stage-edge glow, "+RING+" on the hand at rest."),
 ("perf-speaker","A founder backstage before a talk, standing quiet with eyes closed, one hand over the sternum, warm side light, "+RING+" on that hand — presence before performance."),
 ("perf-ice","An athlete stepping out of an ice bath, breath visible, shoulders dropping as the body settles, soft locker-room daylight, "+RING+" on a dripping hand."),
 # --- 32 new ---
 ("perf-swimmer","A swimmer paused at the pool wall between laps, goggles pushed up, one deep breath, water sheeting off the shoulders, bright natatorium light, "+RING+" on a hand on the lane rope."),
 ("perf-boxer","A boxer in the corner between rounds, gloved hands resting on the ropes, eyes closed for one steadying breath, warm arena light, sweat and stillness, "+RING+" implied on a wrapped hand."),
 ("perf-cyclist","A road cyclist stopped at a summit switchback, one foot down, chest heaving then softening, the valley far below in golden haze, "+RING+" on a hand on the bars."),
 ("perf-lifter","A weightlifter with chalked hands on the loaded barbell, forehead down near the bar, the still held second before the pull, warm gym light, "+RING+" on one hand."),
 ("perf-yoga","A person in a long yoga hold in a sunlit wooden studio, muscles trembling but face calm, one deep even breath, "+RING+" on a steadying hand."),
 ("perf-gymnast","A gymnast standing at the end of the runway, chalk on the hands, absolute stillness and focus before the vault, bright arena, "+RING+" on one hand."),
 ("perf-sprinter","A sprinter set in the starting blocks the instant before the gun, the held breath, dawn track light, "+RING+" on a fingertip on the line."),
 ("perf-rower","A single rower slumped over the oar handle at the finish line, then lifting the head to breathe, misty dawn water, "+RING+" on a hand on the oar."),
 ("perf-diver","A platform diver at the very edge, toes over, arms raised and still, eyes closed for one breath before the dive, bright pool light, "+RING+" on a raised hand."),
 ("perf-freediver","A freediver floating still at the surface before the descent, taking the last slow full breath, calm turquoise water, "+RING+" on a hand at the surface."),
 ("perf-violinist","A violinist with the bow lifted a beat off the strings, the held silence mid-phrase, eyes closed, warm hall light, "+RING+" on the bow hand, natural correct hands."),
 ("perf-cellist","A cellist resting the bow across the strings, eyes closed, breathing in the pause between movements, soft window light, "+RING+" on a hand, natural correct hands."),
 ("perf-singer","A singer at the microphone with eyes closed, one breath before the note, warm stage light and haze, "+RING+" on a hand near the mic."),
 ("perf-conductor","A conductor with the baton raised and held at the peak, the orchestra suspended in silence, the beat before the downbeat, warm hall light, "+RING+" on the baton hand."),
 ("perf-drummer","A drummer with the sticks crossed and still on the snare, one breath in the break, warm club light, "+RING+" on a hand, natural correct hands."),
 ("perf-painter","A painter with a loaded brush hovering just off the canvas, deciding, the pause before the stroke, bright studio window light, "+RING+" on the brush hand, natural correct hands."),
 ("perf-potter","A potter with wet hands lifted just off the spinning clay on the wheel, watching, one breath, warm studio light, "+RING+" on one hand, natural correct hands."),
 ("perf-calligrapher","A calligrapher at a wooden desk in warm window light, holding an ink brush just above a clean sheet of paper, pausing with a calm breath before the first stroke, an ink stone nearby, "+RING+" on the hand, natural correct hands."),
 ("perf-archer","An archer at full draw, the held moment before release, breath suspended, warm range light, "+RING+" on the drawing hand, natural correct hands."),
 ("perf-pilot","An airline pilot in the cockpit before pushback, hands resting off the yoke, one settling breath, dawn light across the tarmac, "+RING+" on a hand."),
 ("perf-nurse","An ER nurse pausing at the gel dispenser between rooms, eyes closed for one second, softened clinical light, "+RING+" on a hand."),
 ("perf-firefighter","A firefighter at the truck before the call, helmet under one arm, one grounding breath, warm bay light, "+RING+" on a hand."),
 ("perf-teacher","A teacher alone in the empty classroom before the bell, one hand flat on the desk, gathering, soft morning light through the windows, "+RING+" on that hand."),
 ("perf-trader","A trader stepping back from a wall of screens, both palms on the desk, one breath, cool morning light, "+RING+" on a hand."),
 ("perf-barista","A barista at the peak of the rush pausing with a hand on the espresso machine, one breath, steam and warm cafe light, "+RING+" on that hand."),
 ("perf-coder","A developer sitting back from the keyboard the moment before a big deploy, hands off the keys, one breath, warm desk light, the screen soft behind, "+RING+" on a hand."),
 ("perf-lawyer","A lawyer just outside a courtroom, one hand on the heavy door, eyes down for one breath before entering, warm corridor light, "+RING+" on that hand."),
 ("perf-welder","A welder lifting the visor, the metal still glowing, wiping the brow with a forearm, one breath in the workshop, warm sparks-dimmed light, "+RING+" on a gloved-off hand."),
 ("perf-carpenter","A carpenter with a hand plane resting on the board, the other hand flat on the wood feeling the grain, a pause, bright workshop window light, "+RING+" on the flat hand, natural correct hands."),
 ("perf-goalkeeper","A goalkeeper before the penalty, gloved hands on the knees then rising, the held focus, warm floodlit pitch, "+RING+" implied on a wrist."),
 ("perf-skater","A figure skater paused center-ice before the music starts, arms lowered, one breath, bright rink light, "+RING+" on a hand."),
 ("perf-mountaineer","A mountaineer pausing on a snow ridge, ice axe planted, breath clouding, looking out for one still second before moving on, cold gold light, "+RING+" on a mitt-off hand."),
]

def gallery():
    imgs=sorted(p.name for p in OUT.glob("*.png"))
    rows="".join(f'<figure><img loading=lazy src="{n}"/><figcaption>{n}</figcaption></figure>' for n in imgs)
    (OUT/"gallery.html").write_text("<!doctype html><meta charset=utf-8><title>Pulse — performance</title>"
     "<style>body{background:#EBE7D4;font-family:system-ui;margin:0;padding:30px}"
     ".grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}figure{margin:0}img{width:100%;display:block;border-radius:8px}"
     "figcaption{font:11px monospace;color:#6E6857;padding:5px}</style>"
     "<h2>Performance — the pause inside the effort ("+str(len(imgs))+")</h2><div class=grid>"+rows+"</div>")

def main():
    args=sys.argv[1:]
    forced=args[args.index("--model")+1] if "--model" in args else None
    only=args[args.index("--only")+1] if "--only" in args else None
    force="--force" in args
    key=get_key(); model=pick_model(key,forced); print("model:",model, flush=True)
    OUT.mkdir(parents=True,exist_ok=True)
    ok,failed,skip=0,[],0
    for cid,scene in PERF:
        if only and only!=cid: continue
        out=OUT/f"{cid}.png"
        if out.exists() and not force: skip+=1; continue
        img=generate(model,key,f"{scene} {STYLE} Aspect ratio 3:2.",aspect="3:2")
        if img: out.write_bytes(img); ok+=1; print(f"  ok {cid}", flush=True)
        else: failed.append(cid); print(f"  FAIL {cid}", flush=True)
        time.sleep(1)
    gallery()
    print(f"\nDone. generated={ok} skipped={skip} failed={len(failed)} total={len(PERF)}", flush=True)
    if failed: print("failed:", ",".join(failed), flush=True)

if __name__=="__main__": main()
