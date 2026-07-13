#!/usr/bin/env python3
"""
Pulse — real motion videos via Veo 3.1 (image-to-video), one per motion "foot".
Replaces the ffmpeg Ken-Burns fakes with actual generated video that obeys each rule:
  photograph  — handheld cell-phone motion, the subject alive
  illustration — Disney MULTIPLANE parallax: depth layers move at different speeds so the
                 2D artwork reveals its 3D space; characters alive and dimensional; composed,
                 dreamlike, never handheld — this is illustration once it has SETTLED
  churn       — the illustration foot's cold/blue distracted variant ONLY: frantic, ADHD,
                sweeping, seeking camera with a stop-motion stutter, never settling. Never use
                on the sync/field-of-light — those stay on the composed illustration rule.
  transition  — illustration resolving into live photograph on a push-in/pull-out along the
                lens axis (never a lateral pan), timed like a breath (the pulse)

18 clips (5 per photograph/illustration/transition foot + 3 churn) for the "prove the look"
pass. Skip-if-exists; resumable.
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
P_MULTIPLANE=("Animate this hand-painted illustration as a classic Disney MULTIPLANE-camera shot. The camera "
 "creeps forward extremely slowly and only a little — a very subtle, barely-perceptible dolly-in along the "
 "lens axis, easing forward like a held breath, never travelling deep into the scene — so the nearer painted "
 "planes drift outward just slightly faster than the far ones. That small difference between foreground, "
 "midground and background IS the parallax: gentle dimensional depth, not a journey. The camera stays locked, "
 "level and composed, never handheld. "
 "CRITICAL: keep the original framing and the main subject centred and present the whole time. No lateral "
 "sliding, no horizontal panning, tracking or trucking, no whip or swoop, no conveyor-belt or train-window "
 "motion; the people and objects stay exactly where they are and must NOT slide across the frame. Do NOT pull "
 "back, rise into an aerial or bird's-eye view, or fly over the scene, and do NOT lose or shrink the subject. "
 "The background stays one stable painted backdrop and must NEVER repeat, tile, multiply, or recede into a "
 "tunnel or hall of mirrors. "
 "The only movement in the subjects is small and human: a slow breath, a blink, hair and fabric stirring, "
 "steam rising, a candle flicker, leaves shifting, a tiny turn of the head. Keep the painterly gouache "
 "cel-animation look fully intact; warm, unhurried, dreamlike; no cuts. {scene}")
P_TRANSITION=("Animate a transition from illustration to photograph: the image begins as a hand-painted "
 "illustration and resolves into a warm, living photograph of the same person and the same moment — the paint "
 "settling into real skin, light and texture. The camera moves on a slow PUSH-IN or PULL-OUT along the lens "
 "axis — zooming toward or away from the seam where illustration meets photograph — never a lateral pan or "
 "sweep. Time it like one slow breath, the pulse that slows the reel: cold and fast painterly on one side "
 "easing into warm, slow, handheld-real footage. Subtle parallax and the subject quietly coming alive as the "
 "medium changes. Warm, unhurried, no hard cuts. {scene}")
P_CHURN=("Animate this hand-painted illustration with a frantic, ADHD camera — the one place the illustration "
 "foot is allowed to lose its composure. Instead of a smooth composed glide, the camera makes big sweeping "
 "SEARCHING swings across the depth planes: a whip-push toward one figure, then a jerk toward another before "
 "either resolves into focus, never settling into a held, composed frame. Give the movement a STOP-MOTION "
 "stutter — small held beats between the swings rather than one continuous glide, like the camera itself can't "
 "decide where to look. Still real multiplane depth (foreground/midground/background genuinely separate and "
 "gliding at different speeds) and the same painterly gouache cel-animation look — this is NOT handheld "
 "photography, it's illustration that can't sit still. Cold, steel-blue, desaturated, dreamlike but restless "
 "and scattered, never landing. No cuts, no text, no logos. {scene}")

# (foot, id, source_image, scene-detail)
JOBS=[
 # photograph foot — handheld, from peak photos
 ("photograph","ph-veo-01","library/peak/peak-aurora.png","A person under a blazing aurora on a snowfield at night, breath visible."),
 ("photograph","ph-veo-02","library/peak/peak-canyon-rim.png","A hiker at the rim of an immense red canyon at golden hour."),
 ("photograph","ph-veo-03","library/peak/peak-cliff-ocean.png","A woman on a grassy sea cliff at golden hour, ocean glittering below."),
 ("photograph","ph-veo-04","library/peak/peak-rooftop-dusk.png","A young woman on a city rooftop at blue-gold dusk, skyline lit below, wind in her hair."),
 ("photograph","ph-veo-05","library/peak/peak-forest-fog.png","A hiker on a ridge as fog pours through a golden pine forest below."),
 # illustration foot — multiplane parallax, from illustration frames with characters
 ("illustration","il-veo-01","library/illustrations/illus-coll-embrace.png","Two people holding a warm, still embrace, staying in place, soft painterly layers of the room receding behind them."),
 ("illustration","il-veo-02","library/illustrations/illus-coll-field-light.png","A painterly aerial view at dusk of rolling hills threaded with glowing golden paths and little lit villages, deep layers of land receding to distant hills."),
 ("illustration","il-veo-03","library/illustrations/illus-coll-festival.png","People standing together at a warm festival, staying where they are, strings of lanterns receding into deep painterly layers behind them."),
 ("illustration","il-veo-04","library/illustrations/illus-coll-dawn-crowd.png","A few people standing quietly at dawn, staying in place, soft painterly layers of landscape receding far behind them."),
 ("illustration","il-veo-05","library/illustrations/illus-coll-table.png","A group seated around a warm outdoor table, staying in their seats, foliage in the foreground and the sunlit trees receding in deep painterly layers behind them."),
 # transition foot — illustration -> photograph, from avatar-spectrum frames
 ("transition","tr-veo-01","library/avatar-spectrum/avatar-01-spectrum.png","A young man at a warm cafe table."),
 ("transition","tr-veo-02","library/avatar-spectrum/avatar-05-spectrum.png","A young woman on a bright balcony."),
 ("transition","tr-veo-03","library/avatar-spectrum/avatar-09-spectrum.png","An older woman in a bright pottery studio."),
 ("transition","tr-veo-04","library/avatar-spectrum/avatar-14-spectrum.png","A barista behind a sunlit counter."),
 ("transition","tr-veo-05","library/avatar-spectrum/avatar-18-spectrum.png","A young graduate in a bright room."),
 # churn foot — frantic ADHD camera, cold/blue distracted state only, from the film's churn stills
 ("churn","ch-veo-01","journey-images/film-18-churn-montage.png","A painted multiplane world of scattered distraction: a train car of downturned faces, a father scrolling at a dinner table, a couple lit by phone-glow in bed, a crosswalk crowd with every head down."),
 ("churn","ch-veo-02","journey-images/film-19-churn-waiting-room.png","A full waiting room at dusk, every face lit by a phone, not one looking up."),
 ("churn","ch-veo-03","journey-images/film-20-churn-recital.png","A child dancing on a small stage to a wall of raised phones and tablets, filming instead of watching."),
]
PROMPT={"photograph":P_HANDHELD,"illustration":P_MULTIPLANE,"transition":P_TRANSITION,"churn":P_CHURN}

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
