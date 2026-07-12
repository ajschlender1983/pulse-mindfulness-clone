#!/usr/bin/env python3
"""
Pulse — The Trailers workshop: 3 social-optimized brand films played on famous
trailer grammars (original parody copy in the Pulse voice — homage to tropes,
never reproduced dialogue). Emits trailers.json + one storyboard frame per shot.

  presence   — dream-thriller grade ("Inception" trope: the spinning totem, time
               dilation). Inversion: the ring SETTLING means you're here.
  one-ring   — epic-fantasy grade (the ring falling onto the finger, the trek).
               "One ring to unite them all — with the present."
  first-rule — gritty anti-marketing ("first rule" trope): don't post about it.

USAGE: python3 tools/generate-trailers.py [--only <trailer>-<nn>] [--force]
Output: library/trailers/<trailer>-<nn>.png + trailers.json
"""
import os, sys, json, base64, urllib.request, urllib.error, pathlib, time

API_ROOT="https://generativelanguage.googleapis.com/v1beta"
ROOT=pathlib.Path(__file__).resolve().parent.parent
OUT=ROOT/"library"/"trailers"

def get_key():
    k=os.environ.get("GEMINI_API_KEY")
    if k: return k.strip()
    return (pathlib.Path.home()/".gemini_api_key").read_text().strip()
def api(path,key,body=None):
    req=urllib.request.Request(f"{API_ROOT}/{path}",data=(json.dumps(body).encode() if body is not None else None),method="POST" if body is not None else "GET")
    req.add_header("x-goog-api-key",key); req.add_header("Content-Type","application/json")
    with urllib.request.urlopen(req,timeout=180) as r: return json.loads(r.read().decode())
def generate(model,key,prompt,tries=3):
    base={"contents":[{"role":"user","parts":[{"text":prompt}]}]}
    for cfg in [{"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"16:9"}}},
                {"generationConfig":{"responseModalities":["TEXT","IMAGE"]}}]:
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

RING="a wide, smooth, polished gold band"
SAFE="Centered composition safe for a vertical 9:16 crop. No text, no lettering, no logos, no watermark."
G_INC=("Cinematic dream-thriller film still, IMAX blockbuster grade, anamorphic, steel-blue shadows "
       "against warm gold highlights, dramatic volumetric light, pristine detail. "+SAFE)
G_LOTR=("Epic fantasy film still, sweeping painterly grade, golden-hour god-rays, vast landscape scale, "
        "mythic and warm, pristine cinematic detail. "+SAFE)
G_FC=("Gritty 35mm film still, warm sodium-vapor tones against deep shadow, high contrast, tactile grain, "
      "urban and raw but warm-hearted, handheld framing. "+SAFE)

TRAILERS=[
 {"id":"presence","title":"PRESENCE","after":"after the dream-thriller",
  "logline":"A dramatic trailer that borrows the grammar of the dream-heist epic — time dilating, the fantastic bleeding into the ordinary — and inverts its most famous anxiety: when the gold ring stops spinning and settles, you're not lost in a dream. You're finally here.",
  "grade":G_INC, "music":"Low braams, a ticking clock that slows with each shot, then total silence before the settle.",
  "social":"45s master · 16:9 + 9:16 crop-safe · hook = the spinning ring in shot 1 · captions burned",
  "shots":[
   {"n":1,"gen":"Extreme macro: "+RING+" spinning fast on a dark walnut table, motion-blurred rotation, one hard shaft of light from the left, steel-blue darkness behind.","vo":"","on":"","sfx":"BRAAM. Then the whir of the spin."},
   {"n":2,"gen":"A city crosswalk where every commuter is motion-blurred rushing except one woman standing pin-sharp and calm in the center, cool blue grade, warm rim light on her.","vo":"You've learned to move through your life…","on":"","sfx":"City roar, muffled."},
   {"n":3,"gen":"Coffee being poured, frozen mid-air — the stream and droplets suspended like glass above the cup, warm kitchen morning light, time stopped.","vo":"…so fast it stopped feeling real.","on":"","sfx":"All sound cuts."},
   {"n":4,"gen":"A sunlit residential street curling impossibly upward into a golden sky like a rising wave, houses and trees folding over, surreal but warm and beautiful.","vo":"","on":"WHAT IF TIME","sfx":"BRAAM."},
   {"n":5,"gen":"Extreme close-up of a human eye opening, a circle of warm gold light reflected in the iris, cinematic macro.","vo":"","on":"COULD OPEN","sfx":"A held breath."},
   {"n":6,"gen":"A man walking down the hallway of a warm family home while the hallway slowly rotates around him, gravity tilted, framed photos on the walls, dreamlike but cozy.","vo":"The fantastic was never somewhere else.","on":"","sfx":"Strings rising."},
   {"n":7,"gen":"Rain suspended mid-air like beads of glass around a laughing child reaching upward in a backyard at golden hour.","vo":"It's the moment you're standing in.","on":"","sfx":"One piano note."},
   {"n":8,"gen":"Macro: the spinning gold band slowing, beginning to wobble on the dark table, tension in the light.","vo":"","on":"","sfx":"A heartbeat, slowing."},
   {"n":9,"gen":"A title-card background: pure black with slow-drifting gold mist and a single thin horizontal streak of warm light. Abstract, textless.","vo":"","on":"PRESENCE","sfx":"Silence."},
   {"n":10,"gen":"Macro: the gold band come to rest, perfectly still and flat on the dark walnut table, one warm glint along its edge.","vo":"When would now be a good time?","on":"This is not a dream.","sfx":"One soft pulse."}
  ]},
 {"id":"one-ring","title":"ONE RING TO UNITE THEM ALL","after":"after the epic",
  "logline":"An epic-fantasy homage built around the most famous ring shot in cinema — the slow fall onto the finger — recast with our hero user. Not a ring of power that corrupts, a ring of presence that returns. One ring to unite them all: with each other, with the present.",
  "grade":G_LOTR, "music":"A lone fiddle over drone, swelling to full orchestra at the fall, resolving to one warm sustained chord.",
  "social":"60s master · 16:9 + 9:16 crop-safe · hook = the molten-gold macro · captions burned",
  "shots":[
   {"n":1,"gen":"Extreme macro of the inside curve of "+RING+" catching firelight, warm reflections flowing along the polished metal like liquid light.","vo":"It begins with a gift.","on":"","sfx":"A whisper of wind."},
   {"n":2,"gen":"Ultra slow-motion: "+RING+" falling through the air in a sunlit kitchen, dust motes hanging, the ring tumbling gently mid-fall.","vo":"","on":"","sfx":"Deep slow whoosh."},
   {"n":3,"gen":"Macro slow-motion: the gold band landing perfectly onto the outstretched finger of a woman in a warm kitchen, the exact moment of the fit, shallow depth.","vo":"One ring.","on":"","sfx":"Orchestra hits, warm."},
   {"n":4,"reuse":"library/peak/peak-summit-sunrise.png","vo":"Not to rule your life…","on":"","sfx":"Swelling strings."},
   {"n":5,"gen":"Sweeping aerial: a small line of friends walking single-file along a vast green mountain ridge at golden hour, epic fantasy scale, long shadows.","vo":"…to return you to it.","on":"","sfx":"Choir under strings."},
   {"n":6,"gen":"The sun flaring over a misty valley like a great benevolent eye of warm light, god-rays fanning across the land.","vo":"It sees you. And asks for nothing back.","on":"","sfx":"The swell holds."},
   {"n":7,"gen":"A long candlelit wooden table crowded with friends laughing, jugs and bread, firelight, fellowship warmth, epic-fantasy tavern glow.","vo":"","on":"ONE RING","sfx":"Fiddle, joyous."},
   {"n":8,"gen":"Close: a hand hanging at someone's side in a golden wheat field, the wide gold band glinting, wind moving the grass, epic warm light.","vo":"","on":"TO UNITE THEM ALL","sfx":"Orchestra pulls back."},
   {"n":9,"gen":"A title-card background: golden god-rays breaking through mountain mist over a dark valley, abstract and epic, textless.","vo":"One ring to unite them all —","on":"","sfx":"One deep drum."},
   {"n":10,"gen":"A hand slowly raised into sunlight, the gold band catching a clean lens flare against a bright sky.","vo":"— with the present.","on":"Be Here WOW","sfx":"Warm sustained chord."}
  ]},
 {"id":"first-rule","title":"THE FIRST RULE","after":"after the anti-ad",
  "logline":"An anti-marketing film in the grammar of the cult classic: rules delivered straight to camera, gritty and direct. Except the rebellion isn't fighting — it's putting the phone down. Don't post about it. Don't tell your friends. Just be present, and receive the gift of your life. Hook lands in the first three seconds, POV, direct address.",
  "grade":G_FC, "music":"A single dirty bass note under the hook, then near-silence with room tone; one deep pulse at the ring tap.",
  "social":"30–40s master · built 9:16-first · HOOK 0:00–0:03 = shot 1 direct-to-camera · captions burned",
  "shots":[
   {"n":1,"gen":"POV direct-to-camera: a man leaning in close in a dim warm concrete basement, finger pointed straight at the lens, intense but calm eyes, single hanging bulb behind him.","vo":"The first rule of presence: you don't post about it.","on":"RULE 01","sfx":"Dirty bass note. HOOK 0:00–0:03."},
   {"n":2,"gen":"Macro: a smartphone dropping face-down onto a concrete floor, caught the instant before impact, gritty warm light.","vo":"The second rule: you don't post about it.","on":"RULE 02","sfx":"The slap of the phone landing."},
   {"n":3,"gen":"A night crowd on a street, every face underlit by phone screens except one man looking up at the sky, sodium-vapor warmth against darkness.","vo":"Everyone you know is somewhere else.","on":"","sfx":"Room tone."},
   {"n":4,"gen":"Extreme macro: a thumb hovering over a glowing screen, tension in the tendons, everything else in darkness.","vo":"You don't need witnesses.","on":"","sfx":"Silence."},
   {"n":5,"gen":"A beautiful dinner on a table, one hand gently pushing a hovering phone down and away from it, warm gritty kitchen light.","vo":"Eat the meal. Don't shoot it.","on":"","sfx":"A fork on a plate."},
   {"n":6,"gen":"A circle of people standing quietly in a bare warm basement room, eyes closed, calm and unbothered, one hanging bulb, gritty warmth.","vo":"We meet where the feed can't find us.","on":"THE PRESENCE CIRCLE","sfx":"Low hum."},
   {"n":7,"gen":"Golden-hour street: a man walking away from camera sliding his phone into his back pocket, long warm shadows, free.","vo":"Don't tell your friends.","on":"","sfx":"Street ambience returns."},
   {"n":8,"gen":"Macro: knuckles of a relaxed hand in the dark, the wide gold band emitting one soft pulse of warm light.","vo":"Don't review it.","on":"","sfx":"ONE deep pulse."},
   {"n":9,"gen":"A title-card background: a single bare bulb swinging gently in a dark concrete room, warm halo, textless.","vo":"","on":"JUST BE HERE","sfx":"The bulb's creak."},
   {"n":10,"gen":"Close portrait: a face half-lit in warm light, eyes open, the smallest beginning of a smile, completely present.","vo":"","on":"Receive the gift of your life.","sfx":"Silence. End card: This is not an ad. Pulse."}
  ]}
]

def main():
    args=sys.argv[1:]
    only=args[args.index("--only")+1] if "--only" in args else None
    force="--force" in args
    key=get_key(); model="gemini-3.1-flash-image"
    OUT.mkdir(parents=True,exist_ok=True)
    ok,failed,skip=0,[],0
    data=[]
    for t in TRAILERS:
        shots=[]
        for s in t["shots"]:
            cid=f"{t['id']}-{s['n']:02d}"
            if "reuse" in s:
                shots.append({**{k:s[k] for k in ("n","vo","on","sfx")},"file":s["reuse"],"reused":True})
                continue
            out=OUT/f"{cid}.png"
            shots.append({**{k:s[k] for k in ("n","vo","on","sfx")},"file":f"library/trailers/{cid}.png"})
            if only and only!=cid: continue
            if out.exists() and not force: skip+=1; continue
            img=generate(model,key,f"{s['gen']} {t['grade']}")
            if img: out.write_bytes(img); ok+=1; print(f"  ok {cid}",flush=True)
            else: failed.append(cid); print(f"  FAIL {cid}",flush=True)
            time.sleep(1)
        data.append({k:t[k] for k in ("id","title","after","logline","music","social")}|{"shots":shots})
    (ROOT/"trailers.json").write_text(json.dumps({"trailers":data},indent=1))
    print(f"\nDone. generated={ok} skipped={skip} failed={len(failed)} · trailers.json written",flush=True)
    if failed: print("failed:",",".join(failed),flush=True)

if __name__=="__main__": main()
