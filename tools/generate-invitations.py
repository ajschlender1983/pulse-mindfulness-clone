#!/usr/bin/env python3
"""
Pulse — "When would now be a good time?" · 20 invitations
=========================================================
Twenty small, tactile, easily-missed human moments — the ones where saying YES
costs nothing and returns everything. Each is a 3-frame photo-visual story:
  scene  — the wider human moment
  detail — the sensory macro (the warm soapy water, the citrus mist)
  face   — the quiet arrival, presence on the face
Warm, editorial, un-staged. The gold Pulse ring where a hand is naturally in frame.

USAGE
  python3 tools/generate-invitations.py [--only <id>] [--model gemini-3.1-flash-image] [--force]
Output: library/invitations/<NN>-<slug>-<frame>.png
"""
import os, sys, json, base64, urllib.request, urllib.error, pathlib, time

API_ROOT="https://generativelanguage.googleapis.com/v1beta"
ROOT=pathlib.Path(__file__).resolve().parent.parent
OUT=ROOT/"library"/"invitations"

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
def generate(model,key,prompt,aspect,tries=3):
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

STYLE=("Warm, editorial, un-staged — medium-format film, soft ambient natural light, honey and cream tones, "
       "fine grain, gentle highlight bloom, real and intimate, never stocky or posed. A quiet, ordinary, "
       "easily-missed moment made beautiful. Anatomy correct: natural hands, fingers and feet. "
       "No text, no lettering, no logos, no watermark.")
RING="a wide smooth polished gold band (the Pulse ring) on the finger catches a small spark of light"
# every frame carries the ring (audit fix: scenes/faces were shipping ringless or with thin bands)
RING_ALL=("On their ring finger sits a WIDE, smooth, polished gold band — the Pulse ring — clearly visible "
          "wherever a hand is in frame, catching one small warm glint. EXACTLY ONE ring in the entire image, "
          "on one finger of one hand only. Not a thin band, not ornate, no signet, no second band anywhere.")
# identity lock: the same person across all three frames of an invitation
PERSONAS={
 "01":"a woman in her mid-30s, dark hair in a loose low bun, cream sweater",
 "02":"a man in his early 40s, short dark hair, olive henley",
 "03":"a woman in her late 30s, curly brown hair, denim jacket",
 "04":"a woman in her early 30s, straight black hair, mustard cardigan",
 "05":"a man in his 50s, salt-and-pepper hair, grey crew-neck",
 "06":"a woman in her late 20s, auburn hair pulled back, white tee",
 "07":"a man in his 30s, short beard, flannel shirt",
 "08":"a father in his late 30s, stubble, chambray shirt",
 "09":"a woman in her 40s, shoulder-length blonde hair, navy blazer",
 "10":"a man in his early 30s, tousled brown hair, bare-shouldered towel",
 "11":"a woman in her 50s, silver-streaked hair, oatmeal shawl",
 "12":"a man in his late 20s, curly black hair, white linen shirt",
 "13":"a woman in her mid-30s, straight dark hair, sage blouse",
 "14":"a woman in her early 40s, wavy brown hair, soft grey lounge set",
 "15":"a man in his 40s, close-cropped hair, rust-colored tee",
 "16":"a woman in her early 30s, long dark braid, cream sleep set",
 "17":"a woman in her mid-30s, dark hair loose at the shoulders, moss-green sweater",
 "18":"a man in his 30s behind a small shop counter, short locs, canvas apron",
 "19":"a woman in her late 30s, chestnut hair in a low ponytail, wool coat",
 "20":"a woman in her 60s, soft grey bob, linen shirt",
}
# targeted prompt fixes from the audit (2 reds + physics/composition breaks)
FIXES={
 "05-kettle-scene":"standing at the stove in a quiet morning kitchen, a classic stovetop kettle on the lit burner just beginning to steam, warm early light",
 "05-kettle-face":"a portrait watching the same stovetop kettle on the stove, unhurried, present in the wait; his left hand rests on the counter wearing the single wide gold band, his right hand and arm completely bare with no jewelry at all",
 "18-change-detail":"macro of a few coins resting in an open palm as another hand gently closes over them to receive, fingers just brushing, "+RING,
 "17-rain-detail":"macro from inside the room: the first raindrops sliding down the windowpane outside the glass, a hand resting gently against the inside of the glass, warm room light, "+RING,
 "19-car-warm-face":"portrait inside the cold car, feeling the first warm air from the heater vent, shoulders loosening, a small relieved smile, breath faintly visible",
 "14-bare-feet-detail":"macro of a woman's bare feet settling onto a warm wooden floor just inside the front door, shoes slipped off nearby",
 "03-seatbelt-scene":"sitting in a parked car before driving, one hand resting on the fastened seatbelt at the chest, soft morning light through the windshield",
 "09-elevator-scene":"standing alone in an elevator between floors, plain brushed-metal walls with no visible displays or buttons, soft even light, calm",
 "09-elevator-face":"a close portrait alone in the elevator, eyes closed for one breath, plain metal wall behind, a private moment of stillness",
}

# (NN, slug, title, scene, detail-macro, face-beat)
INV=[
 ("01","dishes","The warm soapy water",
  "a person at a kitchen sink washing dishes in the evening, sleeves pushed up, warm window light",
  "extreme close macro of hands in warm soapy dishwater, iridescent suds and steam, "+RING,
  "a soft-focus portrait of the same person at the sink, eyes lowered, a small unguarded half-smile of noticing"),
 ("02","orange","Peeling an orange",
  "a person at a wooden table peeling a whole orange, warm afternoon light, a small pile of peel",
  "macro of a thumb breaking the orange peel with a fine mist of citrus oil catching the light, "+RING,
  "close portrait of the person about to eat a segment, eyes closed, quietly present"),
 ("03","seatbelt","One breath in the parked car",
  "a person sitting in a parked car before driving, hand on the seatbelt, soft morning light through the windshield",
  "macro of a hand clicking the seatbelt buckle home in warm cabin light, "+RING,
  "profile of the person taking one slow breath in the driver's seat, shoulders dropping, calm"),
 ("04","laundry","Warm laundry, just out of the dryer",
  "a person folding warm laundry on a bed in soft daylight, a basket of clean clothes",
  "macro of a warm folded shirt pressed against a forearm, soft fibers and light, "+RING,
  "portrait of the person holding folded laundry to their chest for a second, eyes soft, a faint smile"),
 ("05","kettle","Waiting for the kettle",
  "a person standing at the counter waiting for a kettle in a quiet morning kitchen, steam beginning",
  "macro of steam rising from a kettle spout in warm backlight, water droplets, "+RING+" on the hand near it",
  "portrait of the person watching the kettle, unhurried, present in the wait"),
 ("06","face-wash","Cold water at the end of the day",
  "a person at a bathroom sink at night rinsing their face, warm low light",
  "macro of cupped hands lifting cold water to a face, droplets falling, "+RING,
  "close portrait of the person, water on their skin, eyes just opening, awake and present"),
 ("07","dog","The dog leaning its weight into you",
  "a person crouched greeting a dog that leans its full weight against their leg, warm hallway light",
  "macro of a hand buried in a dog's fur, the dog pressing in, "+RING,
  "portrait of the person laughing softly as the dog leans in, fully in the moment"),
 ("08","child-asleep","A small hand going slack in yours",
  "a parent on a walk carrying a drowsy child at golden hour, the child's head on their shoulder",
  "macro of a small child's hand going limp inside an adult's hand as they fall asleep, "+RING,
  "tender close portrait of the parent noticing the child has fallen asleep, a quiet ache of presence"),
 ("09","elevator","The ten seconds between floors",
  "a person standing alone in an elevator between floors, soft even light, calm",
  "macro of a hand resting against a brushed-metal elevator wall, "+RING,
  "portrait of the person alone in the elevator, eyes closed for a breath, a private moment of stillness"),
 ("10","mirror","Wiping the steam from the mirror",
  "a person wiping fog from a steamy bathroom mirror, warm light, their reflection appearing",
  "macro of a hand dragging a clear streak across a fogged mirror, droplets, "+RING,
  "portrait of the person meeting their own reflection in the cleared mirror, calm recognition"),
 ("11","mug","The heavy warmth of a mug on cold fingers",
  "a person on a porch on a cool morning holding a warm mug with both hands, soft light, breath faintly visible",
  "macro of two cold hands wrapped around a warm ceramic mug, steam, "+RING,
  "portrait of the person over the rim of the mug, eyes soft, warmed and present"),
 ("12","toast","Buttering the toast",
  "a person buttering toast at a sunlit kitchen counter in the morning",
  "macro of a knife dragging butter across warm crisp toast, crumbs and melt, "+RING,
  "portrait of the person mid-task pausing to notice the smell of the toast, a small smile"),
 ("13","green-light","The second before the light turns",
  "a person at the wheel at a red light on a quiet street, warm light, hands resting",
  "macro of hands resting easy on a steering wheel, a green traffic light soft in the blurred background, "+RING,
  "profile of the driver taking one calm breath at the light, unhurried, present"),
 ("14","bare-feet","Bare feet on the floor at the door",
  "a person taking off their shoes just inside the front door after a long day, warm entry light",
  "macro of bare feet settling onto a warm wooden floor, shoes just slipped off nearby",
  "portrait of the person exhaling as they stand in bare feet at the door, home, present"),
 ("15","laughter","Laughter from the next room",
  "a person pausing in a warm hallway, glancing toward laughter coming from another room, soft light",
  "macro of a hand resting on a doorframe, warm light spilling from the next room, "+RING,
  "portrait of the person breaking into an involuntary smile at laughter they can't see"),
 ("16","stretch","The last stretch before bed",
  "a person by the bed in soft lamplight doing a long full-body stretch, arms up, a yawn",
  "macro of fingers spreading at the top of a reach, lamplight on skin, "+RING,
  "portrait of the person mid-yawn and stretch, eyes half-closed, letting the day go"),
 ("17","rain","The first taps of rain on the window",
  "a person standing at a window as rain begins, soft grey-warm light, hand near the glass",
  "macro of the first raindrops sliding down a windowpane, warm room reflected, a hand near the glass with "+RING,
  "portrait of the person watching the rain start, a slow soft breath, present with the sound"),
 ("18","change","Handing someone their change",
  "a warm exchange at a small shop counter, a person handing coins to another, soft daylight",
  "macro of coins passing from one hand to another, fingers just brushing, "+RING,
  "portrait of the person at the counter meeting the other's eyes with a genuine small smile"),
 ("19","car-warm","The heater's first warm push",
  "a person in a cold car in the morning waiting for it to warm up, breath fogging, soft light",
  "macro of a hand held in front of a car heater vent, warm air, cold-fogged window behind, "+RING,
  "portrait of the person feeling the first warm air, shoulders loosening, a small relieved smile"),
 ("20","plant","Watering the plant by the window",
  "a person watering a leafy houseplant by a bright window in the morning, soft light",
  "macro of water darkening potting soil, a bead on a green leaf, "+RING+" on the watering hand",
  "portrait of the person leaning close to the plant, noticing a new leaf, quietly delighted"),
]

FRAMES=[("scene","3:2"),("detail","3:2"),("face","4:5")]

def gallery():
    imgs=sorted(p.name for p in OUT.glob("*.png"))
    rows="".join(f'<figure><img loading=lazy src="{n}"/><figcaption>{n}</figcaption></figure>' for n in imgs)
    (OUT/"gallery.html").write_text("<!doctype html><meta charset=utf-8><title>Pulse — invitations</title>"
     "<style>body{background:#EBE7D4;font-family:system-ui;margin:0;padding:30px}"
     ".grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}figure{margin:0}img{width:100%;display:block;border-radius:8px}"
     "figcaption{font:11px monospace;color:#6E6857;padding:5px}</style>"
     "<h2>When would now be a good time? — 20 invitations ("+str(len(imgs))+")</h2><div class=grid>"+rows+"</div>")

def main():
    args=sys.argv[1:]
    forced=args[args.index("--model")+1] if "--model" in args else None
    only=args[args.index("--only")+1] if "--only" in args else None
    force="--force" in args
    key=get_key(); model=pick_model(key,forced); print("model:",model, flush=True)
    OUT.mkdir(parents=True,exist_ok=True)
    ok,failed,skip=0,[],0
    for nn,slug,title,scene,detail,face in INV:
        if only and only!=nn and only!=slug: continue
        for frame,aspect in FRAMES:
            cid=f"{nn}-{slug}-{frame}"
            out=OUT/f"{cid}.png"
            if out.exists() and not force: skip+=1; continue
            body={"scene":scene,"detail":detail,"face":face}[frame]
            if cid in FIXES: body=FIXES[cid]
            who=PERSONAS.get(nn,"")
            lead=f"The person in this moment: {who}. " if who else ""
            prompt=f"{lead}{body}. {RING_ALL} {STYLE} Aspect ratio {aspect}."
            img=generate(model,key,prompt,aspect)
            if img: out.write_bytes(img); ok+=1; print(f"  ok {cid}", flush=True)
            else: failed.append(cid); print(f"  FAIL {cid}", flush=True)
            time.sleep(1)
    gallery()
    print(f"\nDone. generated={ok} skipped={skip} failed={len(failed)} total={len(INV)*len(FRAMES)}", flush=True)
    if failed: print("failed:", ",".join(failed), flush=True)

if __name__=="__main__": main()
