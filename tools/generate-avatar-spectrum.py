#!/usr/bin/env python3
"""
Pulse — Avatar full spectrum (illustration → real life)
=======================================================
For each of the 22 avatars, one frame that scales LEFT→RIGHT from a soft
hand-painted ILLUSTRATION of that person into a warm REAL PHOTOGRAPH of the
same person — the "scaling variation of illustration to real life" from the
Pulse Filmmaker world, applied per-avatar. The gold ring at the seam.

Reuses the avatar descriptions from the two expansion generators (single source).

USAGE
  python3 tools/generate-avatar-spectrum.py [--only <id>] [--model gemini-3.1-flash-image] [--force]
Output: library/avatar-spectrum/<avatar-id>-spectrum.png
"""
import os, sys, json, base64, urllib.request, urllib.error, pathlib, time, importlib.util

API_ROOT="https://generativelanguage.googleapis.com/v1beta"
ROOT=pathlib.Path(__file__).resolve().parent.parent
TOOLS=ROOT/"tools"
OUT=ROOT/"library"/"avatar-spectrum"

def load(f):
    spec=importlib.util.spec_from_file_location(f.stem.replace("-","_"), f)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
EXP1=load(TOOLS/"generate-library-expansion.py")   # AVATARS 01-10
EXP2=load(TOOLS/"generate-library-expansion-2.py")  # PERSONAS 11-22

# unify: [(id, description-without-ring-suffix)]
AVATARS=[]
for cid,aspect,concept in EXP1.AVATARS:           # (id, aspect, concept)
    AVATARS.append((cid, concept))
for cid,concept in EXP2.PERSONAS:                  # (id, concept)
    AVATARS.append((cid, concept))

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

SPECTRUM=("A single portrait image of ONE person that scales smoothly LEFT to RIGHT across its width. "
 "On the FAR LEFT: a soft hand-painted ILLUSTRATION of them — gouache and screen-print texture, gentle "
 "cel-animation warmth, 2.5D painterly, muted and dreamlike, Studio-Ghibli-warm brand-film restraint. "
 "Moving RIGHT it transitions through a looser sketch and painterly mid-tone into, on the FAR RIGHT, a "
 "warm REAL PHOTOGRAPH of the exact same person — medium-format film, golden light, fully alive and present. "
 "The same face, hair and features throughout. At the seam where illustration becomes real, the wide polished "
 "gold Pulse ring on their hand catches a spark of golden light. Warm cream and honey palette, editorial, "
 "poetic. No text, no lettering, no logos, no watermark.")

def gallery():
    imgs=sorted(p.name for p in OUT.glob("*.png"))
    rows="".join(f'<figure><img src="{n}"/><figcaption>{n}</figcaption></figure>' for n in imgs)
    (OUT/"gallery.html").write_text("<!doctype html><meta charset=utf-8><title>Pulse — avatar spectrum</title>"
     "<style>body{background:#EBE7D4;font-family:system-ui;margin:0;padding:30px}"
     ".grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}figure{margin:0}img{width:100%;display:block;border-radius:8px}"
     "figcaption{font:11px monospace;color:#6E6857;padding:5px}</style>"
     "<h2>Avatar spectrum — illustration → real</h2><div class=grid>"+rows+"</div>")

def main():
    args=sys.argv[1:]
    forced=args[args.index("--model")+1] if "--model" in args else None
    only=args[args.index("--only")+1] if "--only" in args else None
    force="--force" in args
    key=get_key(); model=pick_model(key,forced); print("model:",model)
    OUT.mkdir(parents=True,exist_ok=True)
    ok,failed,skip=0,[],0
    for cid,desc in AVATARS:
        fid=cid+"-spectrum"
        if only and only not in (cid,fid): continue
        out=OUT/f"{fid}.png"
        if out.exists() and not force: skip+=1; continue
        print(f"[{fid}]")
        # strip trailing ring clause; the SPECTRUM adds its own ring-at-seam
        person=desc.replace(EXP1.RING,"").replace(EXP2.RING,"").strip().rstrip(",")
        img=generate(model,key,f"The person: {person}. {SPECTRUM} Aspect ratio 16:9.",aspect="16:9")
        if img: out.write_bytes(img); ok+=1
        else: failed.append(fid)
        time.sleep(1)
    gallery()
    print(f"\nDone. generated={ok} skipped={skip} failed={len(failed)} total={len(AVATARS)}")
    for f in failed: print("  failed:",f)

if __name__=="__main__": main()
