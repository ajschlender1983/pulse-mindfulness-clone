#!/usr/bin/env python3
"""
Pulse — real motion videos via Veo 3.1 (image-to-video), one per motion "foot".
Replaces the ffmpeg Ken-Burns fakes with actual generated video that obeys each rule:
  photograph  — handheld cell-phone motion, the subject alive
  illustration — Disney MULTIPLANE parallax: depth layers move at different speeds so the
                 2D artwork reveals its 3D space; characters alive and dimensional
  transition  — illustration resolving into live photograph, timed like a breath (the pulse)

15 clips (5 per foot) for the "prove the look" pass. Skip-if-exists; resumable.
USAGE: python3 tools/generate-motion-veo.py [--only <id>] [--model veo-3.1-fast-generate-preview]
Output: library/motion-rules/<foot>/<id>.mp4
"""
import sys, pathlib, importlib.util, time
ROOT=pathlib.Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location("veo","tools/veo_video.py"); veo=importlib.util.module_from_spec(spec); spec.loader.exec_module(veo)

# ---- the documented motion prompts (also mirrored in flows/motion-prompts.md) ----
P_HANDHELD=("Handheld cell-phone footage, as if filmed on a phone held in one hand: subtle organic camera "
 "drift, gentle micro-shake and a slight tilt, a breath of natural motion — never a locked tripod. The "
 "person is alive and present: a slow breath, hair and clothing moving in the air, a blink, a small shift "
 "of weight, the scene living quietly around them (water, light, distant movement). Warm medium-format film "
 "color, unhurried and intimate. No zoom punches, no cuts. {scene}")
P_MULTIPLANE=("Bring this hand-painted illustration to life with a classic Disney MULTIPLANE-camera effect: "
 "separate the scene into depth layers — foreground, midground, background — and glide them past the lens at "
 "different speeds so rich parallax opens up in every direction and the flat 2D artwork reveals its real 3D "
 "space. The characters are alive and three-dimensional: a soft breath, a blink, hair and fabric drifting, a "
 "small natural gesture — always enough gentle motion that they read as dimensional beings, never a static "
 "cut-out. Keep the painterly, gouache, cel-animation look intact; warm, unhurried, composed dimensional "
 "camera move; no cuts. {scene}")
P_TRANSITION=("Animate a transition from illustration to photograph: the image begins as a hand-painted "
 "illustration and resolves into a warm, living photograph of the same person and the same moment — the paint "
 "settling into real skin, light and texture. Time it like one slow breath, the pulse that slows the reel: "
 "cold and fast painterly on one side easing into warm, slow, handheld-real footage. Subtle parallax and the "
 "subject quietly coming alive as the medium changes. Warm, unhurried, no hard cuts. {scene}")

# (foot, id, source_image, scene-detail)
JOBS=[
 # photograph foot — handheld, from peak photos
 ("photograph","ph-veo-01","library/peak/peak-aurora.png","A person under a blazing aurora on a snowfield at night, breath visible."),
 ("photograph","ph-veo-02","library/peak/peak-canyon-rim.png","A hiker at the rim of an immense red canyon at golden hour."),
 ("photograph","ph-veo-03","library/peak/peak-cliff-ocean.png","A woman on a grassy sea cliff at golden hour, ocean glittering below."),
 ("photograph","ph-veo-04","library/peak/peak-rooftop-dusk.png","A young woman on a city rooftop at blue-gold dusk, skyline lit below, wind in her hair."),
 ("photograph","ph-veo-05","library/peak/peak-forest-fog.png","A hiker on a ridge as fog pours through a golden pine forest below."),
 # illustration foot — multiplane parallax, from illustration frames with characters
 ("illustration","il-veo-01","library/illustrations/illus-coll-embrace.png","Two people in a warm embrace, painterly."),
 ("illustration","il-veo-02","library/illustrations/illus-coll-field-light.png","A figure in a field of light, painterly."),
 ("illustration","il-veo-03","library/illustrations/illus-coll-festival.png","People at a festival in warm light, painterly crowd with depth."),
 ("illustration","il-veo-04","library/illustrations/illus-coll-dawn-crowd.png","A crowd at dawn, layered depth, painterly."),
 ("illustration","il-veo-05","library/illustrations/illus-coll-table.png","People around a warm table, painterly interior with depth."),
 # transition foot — illustration -> photograph, from avatar-spectrum frames
 ("transition","tr-veo-01","library/avatar-spectrum/avatar-01-spectrum.png","A young man at a warm cafe table."),
 ("transition","tr-veo-02","library/avatar-spectrum/avatar-05-spectrum.png","A young woman on a bright balcony."),
 ("transition","tr-veo-03","library/avatar-spectrum/avatar-09-spectrum.png","An older woman in a bright pottery studio."),
 ("transition","tr-veo-04","library/avatar-spectrum/avatar-14-spectrum.png","A barista behind a sunlit counter."),
 ("transition","tr-veo-05","library/avatar-spectrum/avatar-18-spectrum.png","A young graduate in a bright room."),
]
PROMPT={"photograph":P_HANDHELD,"illustration":P_MULTIPLANE,"transition":P_TRANSITION}

def main():
    a=sys.argv[1:]
    only=a[a.index("--only")+1] if "--only" in a else None
    model=a[a.index("--model")+1] if "--model" in a else "veo-3.1-fast-generate-preview"
    ok,fail,skip=0,[],0
    for foot,cid,src,scene in JOBS:
        if only and only!=cid: continue
        outdir=ROOT/"library"/"motion-rules"/foot; outdir.mkdir(parents=True,exist_ok=True)
        out=outdir/f"{cid}.mp4"
        if out.exists(): skip+=1; print("skip",cid,flush=True); continue
        if not (ROOT/src).exists(): fail.append(cid+"(no src)"); print("NO SRC",src,flush=True); continue
        prompt=PROMPT[foot].format(scene=scene)
        print(f"[{foot}] {cid} …",flush=True)
        res=veo.generate(str(ROOT/src), prompt, str(out), model=model, aspect="16:9")
        if res.get("ok"): ok+=1; print(f"  ok {cid} ({res.get('secs')}s)",flush=True)
        else: fail.append(cid); print(f"  FAIL {cid}: {res.get('error')}",flush=True)
        time.sleep(1)
    print(f"\nDone. generated={ok} skipped={skip} failed={len(fail)}",flush=True)
    if fail: print("failed:",fail,flush=True)

if __name__=="__main__": main()
