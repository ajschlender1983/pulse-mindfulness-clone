#!/usr/bin/env python3
"""
Pulse — Film-strip device source frames ("the movie of your life")
==================================================================
Makes the pulse-of-life device LITERAL instead of simulated:

  A. SAME-MOMENT x24  — 24 near-identical frames of ONE real second: Maya's face
                        crossing one small realization. Micro-variation only, so
                        played back they read as 24fps of a single held moment.
                        -> film-strip/same/moment-01..24.png  (+ a stitched loop)
  B. AUTOPILOT x24    — 24 genuinely DIFFERENT 1-second frames, cold and blurred:
                        the days that blur, one missed moment per frame.
                        -> film-strip/autopilot/auto-01..24.png

The SAME set uses the locked Maya reference so the face holds across all 24.

USAGE
  python3 tools/generate-film-strip.py [--group same|autopilot]
          [--only <id>] [--model gemini-3.1-flash-image] [--force]
Then: bash tools/make-film-strip-loop.sh   (stitches same/ into a 24fps loop)
"""
import os, sys, json, base64, urllib.request, urllib.error, pathlib, time

API_ROOT = "https://generativelanguage.googleapis.com/v1beta"
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "film-strip"
MAYA_REF = ROOT / "emails" / "images" / "00-maya-reference.png"

def get_key():
    k=os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if k: return k.strip()
    f=pathlib.Path.home()/".gemini_api_key"
    if f.exists(): return f.read_text().strip()
    sys.exit("No Gemini key found.")

def api(path,key,body=None):
    req=urllib.request.Request(f"{API_ROOT}/{path}", data=(json.dumps(body).encode() if body is not None else None),
                               method="POST" if body is not None else "GET")
    req.add_header("x-goog-api-key",key); req.add_header("Content-Type","application/json")
    with urllib.request.urlopen(req,timeout=180) as r: return json.loads(r.read().decode())

def pick_model(key,forced=None):
    if forced: return forced
    models=api("models",key).get("models",[])
    img=[m.get("name","").split("/")[-1] for m in models
         if "generateContent" in m.get("supportedGenerationMethods",[]) and "image" in m.get("name","").lower()]
    def rank(n):
        n=n.lower()
        if "3.1" in n and "flash" in n and "image" in n and "lite" not in n: return 0
        if "3" in n and "pro" in n and "image" in n: return 1
        if "flash" in n and "image" in n: return 2
        return 9
    img.sort(key=rank); return img[0] if img else sys.exit("no image models")

def generate(model,key,prompt,aspect="3:2",ref_b64=None,tries=3):
    parts=[{"text":prompt}]
    if ref_b64: parts.append({"inlineData":{"mimeType":"image/png","data":ref_b64}})
    base={"contents":[{"role":"user","parts":parts}]}
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

STYLE=("Warm soft ambient natural light, medium-format film photograph, fine natural grain, "
       "shallow depth of field, soft highlight bloom, luminous cream and honey palette. Editorial, "
       "calm, un-staged. No text, no logos, no watermark.")
KEEP="Keep the exact same woman as the reference image: identical face, hair, and features. "

# The single held moment. A tightly-locked ANCHOR frame is generated first, then
# every moment-NN is generated FROM the anchor as reference so the framing, cup,
# background, pose and light stay identical — only the micro-expression shifts.
# This makes it truly "24 frames of one moment" instead of 24 different photos.
ANCHOR_PROMPT=("Maya seated at a small wooden table by a bright window in soft warm morning light "
  "from the left, holding a plain cream stoneware mug in both hands just below her chin, a wide "
  "polished gold band on her right ring finger, medium chest-up shot, centred, plain warm wall "
  "behind her slightly out of focus, calm neutral expression looking softly at the middle distance. "
  "A quiet, still, ordinary morning moment.")
# Each frame reproduces the anchor EXACTLY, changing only the micro-expression.
LOCK=("Reproduce the reference photograph EXACTLY: identical framing and crop, identical cream "
      "stoneware mug held in both hands below the chin, identical wooden table and window, identical "
      "warm morning light from the left, identical hair, cardigan and wide gold ring, identical head "
      "position. Do not change the composition at all. The ONLY difference in this frame: ")
# 24 micro-beats (only the tiniest change each frame: an eyelid, a breath, a lip)
MICRO=[
 "eyes still soft and unfocused on the middle distance","the faintest settling of the shoulders",
 "a slow blink beginning","eyes half-closed mid-blink","eyes reopening, a fraction clearer",
 "focus just starting to gather","the smallest lift at one corner of the mouth",
 "a breath drawn in through the nose","the breath held for an instant","chin lowering a hair",
 "the eyes warming, recognition arriving","the mouth softening toward a smile",
 "a barely-there smile forming","the smile reaching the eyes","cheeks lifting a fraction",
 "a slow exhale beginning","shoulders dropping on the exhale","the gaze softening further, content",
 "a tiny nod, almost imperceptible","stillness, fully present now","the smile settling, easy",
 "eyes drifting closed for a beat of gratitude","eyes opening again, calm","held, at rest — the moment complete",
]

AUTO=[
 "a packed rush-hour subway platform blurred with motion","a laptop screen crowded with tabs and notifications",
 "a sink stacked with unwashed dishes in cold light","a phone lighting up face-down with alerts",
 "car brake lights in gridlock traffic at dusk","an overflowing email inbox on a monitor",
 "a calendar solid with back-to-back meeting blocks","a child's drawing slipping unnoticed off a fridge",
 "cold coffee abandoned beside a keyboard","a treadmill of grey commuter shoes on stairs",
 "a clock face with the second hand sweeping fast","a to-do list with items unchecked",
 "a microwave countdown blurring down","a hand scrolling a feed, thumb blurred",
 "a doorway rushed through, coat half on","a supermarket self-checkout beeping",
 "headphones and a slumped seat on a late train","a desk lamp on past midnight",
 "keys dropped in a bowl without looking","a text left on read, screen dimming",
 "rain on a bus window, city smeared past","a lift door closing on a crowd",
 "a printer spitting pages nobody reads","a bed unmade in a room already left",
]

def gallery(d,title):
    imgs=sorted(p.name for p in d.glob("*.png"))
    rows="".join(f'<figure><img src="{n}"/><figcaption>{n}</figcaption></figure>' for n in imgs)
    d.joinpath("gallery.html").write_text(f"""<!doctype html><meta charset=utf-8><title>{title}</title>
<style>body{{background:#0d0d0f;font-family:system-ui;margin:0;padding:30px;color:#eee}}
.grid{{display:grid;grid-template-columns:repeat(6,1fr);gap:6px}} figure{{margin:0}}
img{{width:100%;display:block;border-radius:2px}} figcaption{{font:9px monospace;color:#888;padding:3px}}</style>
<h3>{title}</h3><div class=grid>{rows}</div>""")

def main():
    args=sys.argv[1:]
    forced=args[args.index("--model")+1] if "--model" in args else None
    only=args[args.index("--only")+1] if "--only" in args else None
    group=args[args.index("--group")+1] if "--group" in args else None
    force="--force" in args
    key=get_key(); model=pick_model(key,forced); print("model:",model)
    (OUT/"same").mkdir(parents=True,exist_ok=True); (OUT/"autopilot").mkdir(parents=True,exist_ok=True)
    ref=base64.b64encode(MAYA_REF.read_bytes()).decode() if MAYA_REF.exists() else None
    ok,failed,skip=0,[],0

    if group in (None,"same"):
        # 1) the locked anchor (uses the Maya face ref); everything else uses the anchor
        anchor_path=OUT/"same"/"00-anchor.png"; anchor_b64=None
        if anchor_path.exists() and not force:
            anchor_b64=base64.b64encode(anchor_path.read_bytes()).decode()
        elif not only or only=="anchor":
            print("[same/00-anchor]")
            img=generate(model,key,f"{KEEP}{ANCHOR_PROMPT} {STYLE} Aspect ratio 3:2.",aspect="3:2",ref_b64=ref)
            if img: anchor_path.write_bytes(img); anchor_b64=base64.b64encode(img).decode(); ok+=1
            else: failed.append("00-anchor")
            time.sleep(1)
        if anchor_b64 is None and anchor_path.exists():
            anchor_b64=base64.b64encode(anchor_path.read_bytes()).decode()
        # 2) 24 frames FROM the anchor — composition locked, only expression varies
        for i,beat in enumerate(MICRO,1):
            cid=f"moment-{i:02d}"
            if only and only not in (cid,"same"): continue
            out=OUT/"same"/f"{cid}.png"
            if out.exists() and not force: skip+=1; continue
            print(f"[same/{cid}]")
            img=generate(model,key,f"{LOCK}{beat}. {STYLE} Aspect ratio 3:2.",aspect="3:2",ref_b64=anchor_b64)
            if img: out.write_bytes(img); ok+=1
            else: failed.append(cid)
            time.sleep(1)
        gallery(OUT/"same","Film strip — the same moment x24")

    if group in (None,"autopilot"):
        for i,scene in enumerate(AUTO,1):
            cid=f"auto-{i:02d}"
            if only and only!=cid: continue
            out=OUT/"autopilot"/f"{cid}.png"
            if out.exists() and not force: skip+=1; continue
            print(f"[autopilot/{cid}]")
            img=generate(model,key,f"{scene}, cold desaturated blue-grey light, slight motion blur, "
                         f"flat and hurried, no people's faces, documentary snapshot. {STYLE} Aspect ratio 3:2.",aspect="3:2")
            if img: out.write_bytes(img); ok+=1
            else: failed.append(cid)
            time.sleep(1)
        gallery(OUT/"autopilot","Film strip — autopilot x24")

    print(f"\nDone. generated={ok} skipped={skip} failed={len(failed)}")
    for f in failed: print("  failed:",f)

if __name__=="__main__": main()
