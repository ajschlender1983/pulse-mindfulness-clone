#!/usr/bin/env python3
"""
Pulse — The Inflection collection (illustration → photograph)
=============================================================
The dramatic, thematic device: a single frame that transitions from a loose,
muted ILLUSTRATION (the moment on autopilot, about to be missed) into warm,
luminous PHOTOGRAPHY (the same moment, fully present and alive) — with the wide
gold Pulse ring at the seam as the inflection point. A visible style-and-light
change carries the whole idea: the ring draws you into presence and joy in a
moment you would otherwise miss.

Each image is self-contained (before→after within one frame). Cool, flat,
grey-blue illustration on the "missed" side; golden, glowing, real photography
on the "present" side; the ring where one becomes the other.

USAGE
  python3 tools/generate-inflection.py [--only <id>] [--model gemini-3.1-flash-image] [--force]
Output: library/inflection/<id>.png (+ gallery.html)
"""
import os, sys, json, base64, urllib.request, urllib.error, pathlib, time

API_ROOT="https://generativelanguage.googleapis.com/v1beta"
ROOT=pathlib.Path(__file__).resolve().parent.parent
OUT=ROOT/"library"/"inflection"

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

# The signature style instruction — applied to every inflection frame.
INFLECT=("A single continuous image that transitions across its width from LEFT to RIGHT. "
 "On the LEFT: a loose, muted, unfinished ILLUSTRATION — flat cool grey-blue line-and-wash, "
 "sketchy pencil and pale watercolour, drained of colour and life, the moment on autopilot, "
 "about to be missed. On the RIGHT: the SAME scene as warm, luminous, full-colour PHOTOGRAPHY — "
 "medium-format film, golden light, rich and alive and present. The two blend seamlessly at a "
 "vertical inflection band in the middle where the drawing becomes real. Exactly at that seam, "
 "the wide polished gold Pulse ring catches a spark of golden light — the inflection point, the "
 "reason the grey drawing blooms into living colour. A dramatic light change across the frame: "
 "cool and flat on the illustrated side, warm and glowing on the photographic side. Poetic, "
 "cinematic, editorial. No text, no logos, no watermark.")

# (id, aspect, scene) — a moment you would miss, that the ring pulls you into.
SCENES=[
 ("inflect-child-laugh","3:2","a young child at a sunlit kitchen table laughing with pure delight, a parent seated close and truly watching them, the parent's ringed hand resting on the table — a warm, simple, tender everyday moment (keep the illustrated half a clean calm pencil line-drawing, never chaotic or scribbled)"),
 ("inflect-sunset","3:2","a person stopped on a city sidewalk, turning to face a blazing sunset between buildings they would have walked straight past"),
 ("inflect-first-snow","3:2","a person at a window as the first snow falls, palm and ringed hand rising to the cold glass"),
 ("inflect-lover-face","3:2","two people across a candlelit dinner table, one truly seeing the other's face for the first time in a while, ringed hand on the table"),
 ("inflect-street-music","3:2","a commuter on a sunlit street stopping to truly listen to a street musician with a guitar, bag lowered, ringed hand stilled at their side, other passersby blurred (the RIGHT half must be a clear warm real photograph, not a painting; no signs or lettering anywhere)"),
 ("inflect-morning-coffee","3:2","a mug of coffee with steam curling in low morning light, a ringed hand wrapped around it, someone finally noticing the warmth"),
 ("inflect-rain-window","3:2","rain running down a window in warm interior light, a ringed hand and forehead resting against the glass, watching it instead of the phone"),
 ("inflect-friend-story","3:2","a friend mid-story across a cafe table, hands alive, the listener fully leaning in, ringed hand around a cup"),
 ("inflect-ocean-dawn","3:2","a person at the shoreline at dawn as a golden wave slides in, ringed hand loose at their side, breath held"),
 ("inflect-child-sleep","3:2","a parent watching their child asleep, a ringed hand resting gently on the small back, the quiet enormity of it"),
 ("inflect-dance-kitchen","3:2","a couple beginning to dance in a kitchen as a song comes on, ringed hands finding each other"),
 ("inflect-grandparent-hands","3:2","two ringed hands, an elder's and a younger's, meeting on a sunlit table, a whole history in the touch"),
 ("inflect-garden-bloom","3:2","a single flower opening in a garden at golden hour, a ringed hand pausing just beside it, noticing"),
 ("inflect-city-look-up","3:2","a person on a busy street finally looking UP at the light between the buildings, ringed hand lowering a phone"),
 ("inflect-bath-steam","3:2","warm steam rising off a bath in soft evening light, a ringed hand trailing the surface, the day finally set down"),
 ("inflect-partner-doorway","3:2","someone arriving home and pausing in the doorway to actually see their partner across the room, ringed hand on the frame"),
 ("inflect-leaf-fall","3:2","a single autumn leaf caught mid-fall in golden light, a ringed hand rising as if to catch it, time slowing"),
 ("inflect-birdsong","3:2","a person stopping on a path, eyes closing to hear birdsong, ringed hand loose, the world suddenly loud with life"),
]

def gallery():
    imgs=sorted(p.name for p in OUT.glob("*.png"))
    rows="".join(f'<figure><img src="{n}"/><figcaption>{n}</figcaption></figure>' for n in imgs)
    (OUT/"gallery.html").write_text(f"""<!doctype html><meta charset=utf-8><title>Pulse — the inflection</title>
<style>body{{background:#1A1C22;font-family:'DM Sans',system-ui;margin:0;padding:40px;color:#F9F6E5}}
h1{{font-weight:600;letter-spacing:-.04em}} .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px}}
figure{{margin:0;background:#0d0d0f;border-radius:12px;overflow:hidden}} img{{width:100%;display:block}}
figcaption{{font:10.5px ui-monospace,monospace;color:#8d8a80;padding:8px 11px}}</style>
<h1>The inflection — illustration → photograph ({len(imgs)})</h1><div class=grid>{rows}</div>""")

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
        img=generate(model,key,f"Scene: {scene}. {INFLECT} Aspect ratio {aspect}.",aspect=aspect)
        if img: out.write_bytes(img); ok+=1
        else: failed.append(cid)
        time.sleep(1)
    gallery()
    print(f"\nDone. generated={ok} skipped={skip} failed={len(failed)} total_defined={len(SCENES)}")
    for f in failed: print("  failed:",f)

if __name__=="__main__": main()
