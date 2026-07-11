#!/usr/bin/env python3
"""
Pulse — Library expansion, round 2
==================================
Widens the library again:
  A. PERSONAS  (12 more storytellers)             -> library/avatars/avatar-11..22
  B. STORIES   (5 new stories, 6 frames each)     -> library/stories/<key>-N.png (+ ref)
  C. DEEPEN    (2 more frames for each of the 5    -> story-images/<key>-5,6.png
                original stories, reusing their refs)
  D. TEXTURE   (18 macro / subjective / symbolic)  -> library/texture/tex-*.png

USAGE
  python3 tools/generate-library-expansion-2.py [--group personas|stories|deepen|texture]
          [--only <id>] [--model gemini-3.1-flash-image] [--force]
"""
import os, sys, json, base64, urllib.request, urllib.error, pathlib, time

API_ROOT = "https://generativelanguage.googleapis.com/v1beta"
ROOT = pathlib.Path(__file__).resolve().parent.parent
LIB = ROOT / "library"
STORYIMG = ROOT / "story-images"

def get_key():
    k = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if k: return k.strip()
    f = pathlib.Path.home()/".gemini_api_key"
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
        if "3" in n and "pro" in n and "image" in n: return 0
        if "nano" in n and "banana" in n: return 1
        if "3.1" in n and "flash" in n and "image" in n and "lite" not in n: return 2
        if "flash" in n and "image" in n: return 3
        return 9
    img.sort(key=rank)
    if not img: sys.exit("no image models")
    return img[0]

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

# ---------------------------------------------------------------- grammar
RING=("a wide, smooth, polished gold band — the Pulse ring — on the finger")
SOFT=("Soft ambient natural light, diffuse and even, airy and breathable, lifted gentle shadows. "
      "Luminous cream, honey and warm oatmeal palette, faint dusty-blue only in the deepest shadow. "
      "Medium-format film photograph, fine natural grain, shallow depth of field, soft highlight bloom. "
      "Calm, unhurried, real and un-staged, editorial. The gold band reads as a discovered "
      "second-glance glint, never centered. No text, no logos, no watermark.")
SYMBOL=("Macro or near-macro, textural and subjective, poetic and symbolic — the feeling of a moment, "
        "not a catalogue shot. Larger than life yet real, slightly surreal. Warm golden-hour light, "
        "generous light leaks and soft bloom, drifting dust catching the sun, fine film grain, "
        "razor-shallow depth of field. Muted cream, honey and charcoal palette, dusty-blue in the "
        "deepest shadow. No text, no logos, no watermark.")
KEEP="Keep the exact same person as the reference image: identical face, hair, and features. "

# ---- A. personas ----
PERSONAS=[
 ("avatar-11","A 41-year-old white man, young dad, tired kind eyes, stubble, grey tee, a baby carrier on his chest, in a sunlit hallway, "+RING+", soft half-smile."),
 ("avatar-12","A 33-year-old Filipino nurse just off a night shift, scrubs, hair coming loose, sitting in a bright break room with a paper cup, "+RING+", exhausted but settled."),
 ("avatar-13","A 47-year-old Black woman using a wheelchair by a big studio window, bright headwrap, painter's smock, brushes in hand, "+RING+", luminous focus."),
 ("avatar-14","A 26-year-old white nonbinary barista behind a sunlit counter, apron, tattoos, easy grin, "+RING+", present and warm."),
 ("avatar-15","A 58-year-old Japanese man, fisherman, weathered face, canvas jacket, at a harbour in soft morning light, "+RING+", quiet and steady."),
 ("avatar-16","A 37-year-old Indian woman, schoolteacher, cardigan, chalk dust on her sleeve, in a bright empty classroom, "+RING+", gentle and attentive."),
 ("avatar-17","A 71-year-old white man and 69-year-old white woman, a retired couple, in a sunlit garden doorway, gardening clothes, both with a wide polished gold band, easy companionship."),
 ("avatar-18","A 22-year-old Black man, new graduate, in a bright bedroom with moving boxes, hoodie, hopeful open face, "+RING+", on the edge of something."),
 ("avatar-19","A 44-year-old Latino chef in whites at a sunlit prep bench, forearms tattooed, "+RING+", calm before the rush."),
 ("avatar-20","A 30-year-old Middle Eastern woman, translator, headphones round her neck, at a light-filled desk of books, "+RING+", thoughtful mid-pause."),
 ("avatar-21","A 63-year-old Black woman, choir director, bright scarf, in a sunlit church hall, hands mid-gesture, "+RING+", radiant and grounded."),
 ("avatar-22","A 35-year-old white woman, long-distance runner, on a bright porch stretching, "+RING+", breath still settling, quietly strong."),
]

# ---- B. new stories (key, who, [(frame_id, aspect, use_ref, concept)...]) ----
STORIES={
 "nadia":{"who":("A 34-year-old woman named Nadia, new mother. Warm tan skin, dark hair in a messy bun, "
                 "soft tired eyes, oversized grey nursing cardigan, and a wide polished gold band on her right ring finger."),
   "frames":[
    ("nadia-1","4:5",True,"Nadia at 3am nursing in a dim room, the cool blue of a phone face-down beside her, her eyes lifting from the screen to the baby's face — choosing the room over the feed."),
    ("nadia-2","3:2",True,"Nadia at a dawn window holding her baby against her shoulder, first warm light on both their faces, present for once instead of scrolling."),
    ("nadia-3","1:1",True,"Macro: the baby's tiny hand curled around Nadia's ringed finger, soft morning light, the gold band and the small fist."),
    ("nadia-4","3:2",True,"Nadia handing the baby to her partner in a sunlit kitchen, a real look passing between the two adults, a beat of shared presence."),
    ("nadia-5","4:5",True,"Nadia alone in the shower's steam for her one quiet minute, forehead to the tile, thumb finding the ring, breathing."),
    ("nadia-6","3:2",True,"Nadia laughing on the floor with her baby in warm afternoon light, phone nowhere, fully in the mess and the joy of it."),
   ]},
 "walter":{"who":("A 74-year-old man named Walter with a grandchild of about seven. Walter: white, silver hair, "
                  "flannel shirt, kind creased face, a wide polished gold band on his hand. The child: bright, curious, dungarees."),
   "frames":[
    ("walter-1","3:2",True,"Walter and his grandchild sitting on a porch step in golden afternoon light, Walter pointing gently at something far off, the child following his hand."),
    ("walter-2","4:5",True,"The child copying Walter's stillness on the step, both with eyes closed, faces turned to the warm sun, learning to notice."),
    ("walter-3","1:1",True,"Macro: Walter's old ringed hand and the child's small hand both resting on a single large green leaf, dappled light."),
    ("walter-4","3:2",True,"Walter crouched at the water's edge with the child, the held pause before a skipping stone leaves his ringed hand, low gold light."),
    ("walter-5","4:5",True,"Walter alone later on the same porch at dusk, turning the gold band on his finger, a soft remembering smile."),
    ("walter-6","3:2",False,"Two figures small in the frame, an old man and a child, walking away hand in hand down a sunlit path through long grass, unhurried."),
   ]},
 "sam":{"who":("A 39-year-old person named Sam, recovering from burnout. Androgynous, short cropped hair, "
               "soft olive overshirt, weary but softening face, and a wide polished gold band on the right ring finger."),
   "frames":[
    ("sam-1","3:2",True,"Sam sitting at a desk with the laptop deliberately closed, hands still, learning how to just sit, soft window light, a small hard exhale."),
    ("sam-2","4:5",True,"Sam on an aimless walk with coat open, no destination, looking up at bare branches against a bright sky, relearning slow."),
    ("sam-3","1:1",True,"Macro: a coffee going cold on purpose, Sam's ringed hand wrapped around the cool cup, steam long gone, soft light."),
    ("sam-4","3:2",True,"Sam repotting a plant at a sunlit table, hands deep in dark soil, fully absorbed in one small real task."),
    ("sam-5","4:5",True,"Sam lying back in bright grass looking straight up, arms open, the body finally unclenching in warm daylight."),
    ("sam-6","3:2",True,"Sam back at work but changed — one task on the screen, the window open, shoulders down, the ringed hand at rest on the desk."),
   ]},
 "mei-david":{"who":("A long-distance couple in their early 30s: Mei, an East Asian woman with a sleek bob, "
                     "and David, a Black man with short locs. Each wears a wide polished gold band on the right ring finger. "
                     "They are in two different cities."),"two":True,
   "frames":[
    ("mei-david-1","4:5",True,"Mei at her apartment window in cool morning light in one city, hand flat on the glass, the gold band catching the first sun, missing someone but present."),
    ("mei-david-2","4:5",True,"David in a different city at evening, warm lamp light, sitting at a small table taking the same breath at the same moment, his gold band lit."),
    ("mei-david-3","1:1",False,"Macro split feeling: two phones face-down on two different tables, two ringed hands resting beside them, one in cool light one in warm — the same pause in two places."),
    ("mei-david-4","3:2",False,"A laptop on a table showing a video call where nothing is being said, just two people breathing together across distance, soft light in the room."),
    ("mei-david-5","3:2",True,"Mei walking a busy street alone at golden hour, unhurried and unlonely, the ring on her hand, carried by a shared practice."),
    ("mei-david-6","3:2",True,"Reunion in a sunlit train station, Mei and David's two ringed hands finding each other first, before the embrace, warm light flaring."),
   ]},
 "tomas":{"who":("A 66-year-old man named Tomas, recently widowed. White, grey beard, heavy gentle eyes, "
                 "worn wool cardigan, and a wide polished gold wedding-style band on his right ring finger."),
   "frames":[
    ("tomas-1","3:2",True,"Tomas at a kitchen table set with one cup where there were once two, soft morning light, the empty chair opposite, breathing through it, not drowning."),
    ("tomas-2","4:5",True,"Tomas standing in the doorway of a sunlit room he can't quite enter yet, one hand on the frame, the ring visible, gathering himself."),
    ("tomas-3","1:1",True,"Macro: Tomas's ringed hand resting beside a small soft-focus framed photograph on a windowsill, warm light, tender and quiet."),
    ("tomas-4","3:2",True,"Tomas outside for the first time in weeks, sun full on his upturned face on a park bench, the smallest permission to feel it."),
    ("tomas-5","4:5",True,"Tomas tending a garden bed in golden light, ringed hands in the earth, giving care to something living."),
    ("tomas-6","3:2",True,"Tomas with a real small smile at a sudden memory, present with the grief rather than lost in it, warm afternoon light."),
   ]},
}

# ---- C. deepen the original 5 (reuse story-images/00-<key>-reference.png) ----
DEEPEN=[
 ("ingrid","ingrid-5","4:5","Ingrid pouring tea at a sunlit kitchen counter after class, steam rising, fully attentive to the small ritual, the gold band on her hand."),
 ("ingrid","ingrid-6","3:2","Ingrid on an evening walk home through soft low light, unhurried, noticing the sky, the day's practice still with her."),
 ("theo","theo-5","1:1","Macro: Theo's hand closing his laptop lid in soft daylight, deliberate, the gold band catching light — the choice to stop."),
 ("theo","theo-6","3:2","Theo actually listening to a friend across a cafe table, phone face-down, present in the conversation, warm window light."),
 ("rosa","rosa-5","4:5","Rosa reading her three lines back to herself at the end of the day by a warm lamp, a small satisfied smile, the notebook and the ring."),
 ("rosa","rosa-6","3:2","Rosa on a video call with her mother, both laughing, Rosa fully in it, warm afternoon light, ringed hand near her heart."),
 ("darius","darius-5","4:5","Darius playing on the floor with his kids after work, tie loosened, actually there, warm evening light, the ring on his hand."),
 ("darius","darius-6","1:1","Macro: Darius's ringed hand pressed flat and calm on a sunlit kitchen table, the tension gone out of it, soft light."),
 ("amara-ben","amara-ben-5","3:2","Amara and Ben cooking together in a sunlit kitchen, an easy unhurried rhythm between them, both present, two gold bands."),
 ("amara-ben","amara-ben-6","4:5","Amara and Ben on an evening walk, shoulders touching, no phones, mid-quiet-conversation, soft golden light."),
]

# ---- D. texture / symbol (no character ref) ----
TEXTURE=[
 ("tex-brushed","1:1","Extreme macro of the polished gold Pulse band's curved surface, one clean streak of warm light travelling across it, deep soft-focus shadow around, jewelry-macro."),
 ("tex-thumb","1:1","Macro: a thumb pressing gently into the side of the gold band on a finger, the small physical gesture of coming back to now, warm skin, soft light."),
 ("tex-wrist-pulse","3:2","Macro: the gold band on a hand laid over the opposite wrist's pulse point, bare skin, low warm light catching the band, the body's own rhythm."),
 ("tex-breath-glass","3:2","A bloom of breath-fog on cold glass with warm gold light behind it, a fingertip clearing one small circle back to clarity, dawn."),
 ("tex-concentric-sand","1:1","Concentric rings pressed into warm pale sand radiating outward from a small center, raking golden light, the pulse motif made earth."),
 ("tex-concentric-water","1:1","A single drop's concentric rings spreading on near-black still water, one gold rim of light tracing each ring, drifting dust above."),
 ("tex-eclipse","1:1","The gold band held up backlit against the sun so its rim glows into a thin ring of gold light like an eclipse, lens flare, deep surround."),
 ("tex-aperture","3:2","Warm gold light pouring through a slowly opening circular aperture into a dim space, the geometry of presence opening, dust in the beam."),
 ("tex-dust-spiral","3:2","A slow spiral of golden dust turning inside a single shaft of low sun in a quiet room, larger than life, physics gently bent."),
 ("tex-half-light","1:1","The gold band resting on a surface exactly half in cool blue shadow and half in warm gold light — the two states, numb and present, in one frame."),
 ("tex-shadow-long","3:2","The gold band alone on a pale surface at very low sun, casting a long soft golden shadow far longer than itself, symbolic and quiet."),
 ("tex-fingerprint","1:1","Extreme macro of a fingertip's whorl lit warm, its concentric ridges echoing the circle of the gold band just behind it in soft focus."),
 ("tex-dew-roll","1:1","Macro: a single dew drop rolling down a green blade of grass at dawn, holding a bead of gold sun, everything else soft."),
 ("tex-goosebumps","1:1","Macro of forearm skin as fine hairs lift and goosebumps rise, warm raking light, the body quietly noticing something — the felt sense of a pulse."),
 ("tex-water-tension","3:2","Extreme macro of water surface tension doming and just about to break at the edge of the gold band half-submerged, gold caustics beneath."),
 ("tex-eye-ring","1:1","Macro of a human eye, calm, with a tiny warm ring of reflected golden light held in the iris — presence reflected, subjective and intimate."),
 ("tex-leaf-vein","3:2","Backlit macro of a leaf's veins glowing gold, branching like a quiet nervous system, one lime-lit edge, drifting light."),
 ("tex-metronome","3:2","A brass metronome arm blurred to near-stillness at the center of its swing in warm lamplight, time softened toward a held pause."),
]

def gallery(outdir,title):
    imgs=sorted(p.name for p in outdir.glob("*.png"))
    rows="".join(f'<figure><img src="{n}"/><figcaption>{n}</figcaption></figure>' for n in imgs)
    outdir.joinpath("gallery.html").write_text(f"""<!doctype html><meta charset=utf-8><title>{title}</title>
<style>body{{background:#EBE7D4;font-family:'DM Sans',system-ui;margin:0;padding:40px;color:#1A1C22}}
h1{{font-weight:600;letter-spacing:-.04em}} .grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}}
figure{{margin:0;background:#F9F6E5;border-radius:14px;overflow:hidden;box-shadow:0 12px 30px rgba(66,61,50,.10)}}
img{{width:100%;display:block}} figcaption{{font:11px ui-monospace,monospace;color:#6E6857;padding:10px 12px}}</style>
<h1>{title}</h1><div class=grid>{rows}</div>""")

def b64(p): return base64.b64encode(p.read_bytes()).decode()

def main():
    args=sys.argv[1:]
    forced=args[args.index("--model")+1] if "--model" in args else None
    only=args[args.index("--only")+1] if "--only" in args else None
    group=args[args.index("--group")+1] if "--group" in args else None
    force="--force" in args
    key=get_key(); model=pick_model(key,forced); print("model:",model)
    ok,failed,skipped=0,[],0
    (LIB/"avatars").mkdir(parents=True,exist_ok=True)
    (LIB/"stories").mkdir(parents=True,exist_ok=True)
    (LIB/"texture").mkdir(parents=True,exist_ok=True)

    if group in (None,"personas"):
        for cid,concept in PERSONAS:
            if only and only!=cid: continue
            out=LIB/"avatars"/f"{cid}.png"
            if out.exists() and not force: skipped+=1; continue
            print(f"[personas/{cid}]"); img=generate(model,key,f"Editorial portrait. {concept} Looking softly toward camera, three-quarter view. {SOFT} Aspect ratio 4:5.",aspect="4:5")
            if img: out.write_bytes(img); ok+=1
            else: failed.append(cid)
            time.sleep(1)
        gallery(LIB/"avatars","Pulse library — avatars")

    if group in (None,"stories"):
        for skey,story in STORIES.items():
            refp=LIB/"stories"/f"00-{skey}-reference.png"; refb=None
            want=(not only) or only==skey or any(only==f[0] for f in story["frames"])
            if not want: continue
            keep=("Keep the exact same two people as the reference image: identical faces, hair, features. "
                  if story.get("two") else KEEP)
            if refp.exists() and not force: refb=b64(refp)
            else:
                print(f"[stories/{skey}] reference")
                n=("two people, both looking softly toward camera" if story.get("two") else "looking softly toward camera, three-quarter view")
                img=generate(model,key,f"Editorial character portrait. {story['who']} Neutral warm expression, {n}, even soft window light so the face reads clearly. {SOFT}",aspect="4:5")
                if img: refp.write_bytes(img); refb=b64(refp); ok+=1
                else: failed.append(f"00-{skey}")
                time.sleep(1)
            for fid,aspect,use_ref,concept in story["frames"]:
                if only and only not in (skey,fid): continue
                out=LIB/"stories"/f"{fid}.png"
                if out.exists() and not force: skipped+=1; continue
                print(f"[stories/{fid}]"); img=generate(model,key,f"{keep if use_ref else ''}{concept} {SOFT} Aspect ratio {aspect}.",aspect=aspect,ref_b64=(refb if use_ref else None))
                if img: out.write_bytes(img); ok+=1
                else: failed.append(fid)
                time.sleep(1)
        gallery(LIB/"stories","Pulse library — new stories")

    if group in (None,"deepen"):
        for skey,fid,aspect,concept in DEEPEN:
            if only and only!=fid: continue
            refp=STORYIMG/f"00-{skey}-reference.png"
            out=STORYIMG/f"{fid}.png"
            if out.exists() and not force: skipped+=1; continue
            refb=b64(refp) if refp.exists() else None
            print(f"[deepen/{fid}]"); img=generate(model,key,f"{KEEP}{concept} {SOFT} Aspect ratio {aspect}.",aspect=aspect,ref_b64=refb)
            if img: out.write_bytes(img); ok+=1
            else: failed.append(fid)
            time.sleep(1)

    if group in (None,"texture"):
        for cid,aspect,concept in TEXTURE:
            if only and only!=cid: continue
            out=LIB/"texture"/f"{cid}.png"
            if out.exists() and not force: skipped+=1; continue
            print(f"[texture/{cid}]"); img=generate(model,key,f"{concept} {SYMBOL} Aspect ratio {aspect}.",aspect=aspect)
            if img: out.write_bytes(img); ok+=1
            else: failed.append(cid)
            time.sleep(1)
        gallery(LIB/"texture","Pulse library — texture & symbol")

    print(f"\nDone. generated={ok} skipped={skipped} failed={len(failed)}")
    for f in failed: print("  failed:",f)

if __name__=="__main__": main()
