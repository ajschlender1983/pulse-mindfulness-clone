#!/usr/bin/env python3
"""
Pulse — Hybrid illustration<->photograph family (5x the combination style)
==========================================================================
The heart of the Filmmaker language: one frame that is BOTH illustration and
photograph. Illustration = autopilot / stylized memory; photograph = presence /
the moment fully lived; the ring is the hinge at the seam. Ten distinct
composition RULES x twenty present-moment scenes = 200 frames.

USAGE
  python3 tools/generate-hybrid.py [--only <id>] [--model gemini-3.1-flash-image] [--force]
Output: library/hybrid/<sNN>-<style>.png
"""
import os, sys, json, base64, urllib.request, urllib.error, pathlib, time

API_ROOT="https://generativelanguage.googleapis.com/v1beta"
ROOT=pathlib.Path(__file__).resolve().parent.parent
OUT=ROOT/"library"/"hybrid"

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
                if e.code==400: break
                break
            except Exception: time.sleep(2); continue
    return None

# illustration + photograph grammar
ILLUS="gouache and soft screen-print texture with confident inked linework, gentle cel-animation warmth, muted painterly 2.5D"
PHOTO="a warm real photograph, medium-format film, soft ambient natural light, honey and cream tones, fine grain, fully alive and present"
RING="the wide smooth polished gold Pulse ring on a finger catches a small spark of golden light"
TAIL="Same person and same moment across the whole frame. Warm cream and honey palette, editorial and poetic, no text, no lettering, no logos, no watermark."

# ten composition RULES for how illustration meets photograph
STYLES=[
 ("split", "A single frame split by one crisp VERTICAL seam: the LEFT half is "+ILLUS+"; the RIGHT half is "+PHOTO+". The subject continues unbroken across the seam. "+RING+" right at the seam."),
 ("dissolve", "One frame that DISSOLVES top-to-bottom: the upper portion is "+ILLUS+", melting through a seamless gradient into "+PHOTO+" in the lower portion. "+RING+" in the photographic zone."),
 ("rackfocus", "A rack-focus depth pull in one frame: the illustrated layer ("+ILLUS+") sits SOFT and out of focus while the photographic subject ("+PHOTO+") snaps SHARP and present — the lens focusing out of illustration into photograph. "+RING+" sharp in focus."),
 ("aperture", "A circular camera APERTURE / iris opening in the center of the frame reveals a sharp warm photograph ("+PHOTO+") of the present moment; the surround is loose illustration ("+ILLUS+") — the aperture expanding and focusing the lens on the scene. "+RING+" inside the aperture."),
 ("painted-edges", "A warm photograph ("+PHOTO+") at the center whose EDGES break apart into loose brushstrokes, drips and paper texture ("+ILLUS+"). "+RING+" in the photographic center."),
 ("torn-seam", "A torn-paper DIAGONAL seam splits the frame: one side is "+ILLUS+", the other side is "+PHOTO+", the ragged paper edge between them. "+RING+" beside the tear."),
 ("frame-in-frame", "An illustrated hand or painted film-frame ("+ILLUS+") holds a sharp warm PHOTOGRAPH ("+PHOTO+") of the moment inside it — a frame within the frame. "+RING+" in the inner photograph."),
 ("brushstroke", "A warm photograph ("+PHOTO+") being PAINTED into existence by visible brushstrokes over a faint illustrated underdrawing ("+ILLUS+") at the margins — half-finished, resolving into the real. "+RING+" in the finished photographic area."),
 ("double-exposure", "A soft double EXPOSURE: an illustration ("+ILLUS+") and a photograph ("+PHOTO+") of the same moment overlaid and ghosted together, one emerging from the other. "+RING+" glinting where they meet."),
 ("filmstrip", "A horizontal triptych film-strip of the SAME moment, left to right: panel one "+ILLUS+", panel two a half-painted transition, panel three "+PHOTO+" — autopilot resolving into presence. "+RING+" glinting in the photographic panel."),
]

# twenty present-moment scenes (person + moment; ring implied)
SCENES=[
 ("s01","3:2","a woman at a kitchen window at dawn holding a mug, steam rising into the light"),
 ("s02","3:2","a father lifting his laughing toddler overhead in a sunlit living room at golden hour"),
 ("s03","3:2","a man on a train resting his head against the window as the city slides past"),
 ("s04","3:2","a woman walking a forest trail with god-rays of morning light through the trees"),
 ("s05","3:2","a couple slow-dancing in a warm-lit kitchen in the evening"),
 ("s06","16:9","a runner pausing at a coastal overlook at sunrise, the ocean vast below"),
 ("s07","3:2","a woman reading in bed under soft lamplight, absorbed and calm"),
 ("s08","3:2","a chef plating a dish quietly in a warm kitchen, steam and low light"),
 ("s09","3:2","a musician mid-strum with eyes closed in a sunlit room, dust in the light"),
 ("s10","16:9","a hiker standing on a mountain summit at dawn above a sea of clouds"),
 ("s11","3:2","a mother reading a bedtime story to a child in lamplit calm"),
 ("s12","3:2","a painter at an easel by a bright window, brush lifted, absorbed"),
 ("s13","3:2","a swimmer surfacing in a turquoise alpine lake, gasping with joy"),
 ("s14","16:9","a woman on a rooftop at blue-gold dusk with the city lights below"),
 ("s15","3:2","an older man tending a garden in soft afternoon light, hands in the soil"),
 ("s16","3:2","a woman in a hammock in dappled forest light, one arm hanging, at ease"),
 ("s17","3:2","two friends laughing across a cafe table in warm window light"),
 ("s18","3:2","a woman in a slow yoga stretch in a sunlit wooden room"),
 ("s19","3:2","a surfer sitting on their board on glassy dawn water facing a pink horizon"),
 ("s20","3:2","a barista pausing behind the counter, steam and bright morning light"),
]

def gallery():
    imgs=sorted(p.name for p in OUT.glob("*.png"))
    rows="".join(f'<figure><img loading=lazy src="{n}"/><figcaption>{n}</figcaption></figure>' for n in imgs)
    (OUT/"gallery.html").write_text("<!doctype html><meta charset=utf-8><title>Pulse — hybrid</title>"
     "<style>body{background:#EBE7D4;font-family:system-ui;margin:0;padding:30px}"
     ".grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}figure{margin:0}img{width:100%;display:block;border-radius:8px}"
     "figcaption{font:11px monospace;color:#6E6857;padding:5px}</style>"
     "<h2>Hybrid — illustration ↔ photograph ("+str(len(imgs))+")</h2><div class=grid>"+rows+"</div>")

def main():
    args=sys.argv[1:]
    forced=args[args.index("--model")+1] if "--model" in args else None
    only=args[args.index("--only")+1] if "--only" in args else None
    force="--force" in args
    key=get_key(); model=pick_model(key,forced); print("model:",model, flush=True)
    OUT.mkdir(parents=True,exist_ok=True)
    ok,failed,skip=0,[],0
    for sid,aspect,scene in SCENES:
        for skey,comp in STYLES:
            cid=f"{sid}-{skey}"
            if only and only!=cid: continue
            out=OUT/f"{cid}.png"
            if out.exists() and not force: skip+=1; continue
            prompt=f"Scene: {scene}. {comp} {TAIL} Aspect ratio {aspect}."
            img=generate(model,key,prompt,aspect=aspect)
            if img: out.write_bytes(img); ok+=1; print(f"  ok {cid}", flush=True)
            else: failed.append(cid); print(f"  FAIL {cid}", flush=True)
            time.sleep(1)
    gallery()
    print(f"\nDone. generated={ok} skipped={skip} failed={len(failed)} total={len(SCENES)*len(STYLES)}", flush=True)
    if failed: print("failed:", ",".join(failed), flush=True)

if __name__=="__main__": main()
