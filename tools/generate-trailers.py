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
   {"n":2,"gen":"Macro close on a phone screen's cold glow reflected in a pair of glasses, world blurred and rushing behind, lips moving silently as if rehearsing words already spoken.","vo":"You're replaying a conversation that already ended.","on":"","sfx":"A murmur, looped."},
   {"n":3,"gen":"A city crosswalk where every commuter is motion-blurred rushing except one woman standing pin-sharp and calm in the center, cool blue grade, warm rim light on her.","vo":"You've learned to move through your life…","on":"","sfx":"City roar, muffled."},
   {"n":4,"gen":"Coffee being poured, frozen mid-air — the stream and droplets suspended like glass above the cup, warm kitchen morning light, time stopped.","vo":"…so fast it stopped feeling real.","on":"","sfx":"All sound cuts."},
   {"n":5,"gen":"A warmly lit kitchen at night, two people mid-conversation, one leaning in with tension visibly easing from his shoulders, the room staying sharp while the edges of the frame soften into dream-blur.","vo":"Even mid-argument, presence finds you.","on":"","sfx":"A tense breath, then release."},
   {"n":6,"gen":"A sunlit residential street curling impossibly upward into a golden sky like a rising wave, houses and trees folding over, surreal but warm and beautiful.","vo":"","on":"WHAT IF TIME","sfx":"BRAAM."},
   {"n":7,"gen":"Dream-logic corridor: five identical arched doors down an impossibly long hallway, each glowing a different warm color from within — gold, blue-violet, ember, rose, deep violet — mist pooling at every threshold, Escher-like perspective.","vo":"","on":"PRESENCE · PEACE · POWER · PLEASURE · PURPOSE","sfx":"Five soft chimes, one per door."},
   {"n":8,"gen":"Extreme close-up of a human eye opening, a circle of warm gold light reflected in the iris, cinematic macro.","vo":"","on":"COULD OPEN","sfx":"A held breath."},
   {"n":9,"gen":"A woman at the base of a spiraling gold staircase in a sunlit dream atrium, glancing briefly down at a screen in her palm, then lifting her gaze upward toward the light.","vo":"There are only three reasons to look down. Every other reason, you look up.","on":"","sfx":"A soft pulse, then quiet."},
   {"n":10,"gen":"A man walking down the hallway of a warm family home while the hallway slowly rotates around him, gravity tilted, framed photos on the walls, dreamlike but cozy.","vo":"The fantastic was never somewhere else.","on":"","sfx":"Strings rising."},
   {"n":11,"gen":"Macro: breath fogging a cold windowpane in a warm room, the frost pattern rearranging itself like a slow kaleidoscope before clearing.","vo":"Breath is the door that's already open.","on":"","sfx":"A slow inhale."},
   {"n":12,"gen":"Rain suspended mid-air like beads of glass around a laughing child reaching upward in a backyard at golden hour.","vo":"It's the moment you're standing in.","on":"","sfx":"One piano note."},
   {"n":13,"gen":"A pendulum of warm light swinging slowly through dream fog, its arc gradually resolving into the steady rhythm of a heartbeat.","vo":"Pulse gives you rhythm. Rhythm gives you pause.","on":"","sfx":"A steady, warm pulse, like a heartbeat."},
   {"n":14,"gen":"A woman at a warm dinner table pausing mid-motion, eyes soft with wonder, steam rising frozen above the dish in front of her, dreamlike stillness.","vo":"Stop watching the movie of your mind.","on":"","sfx":"Time seems to hush."},
   {"n":15,"gen":"Macro: the spinning gold band slowing, beginning to wobble on the dark table, tension in the light.","vo":"","on":"","sfx":"A heartbeat, slowing."},
   {"n":16,"gen":"The same dinner table now fully alive and in motion — steam curling, laughter mid-breath, hands reaching for bread — sharp and real after the stillness.","vo":"Start making the movie of your life — the same footage, at the speed of being here.","on":"","sfx":"Sound returns, warm and full."},
   {"n":17,"gen":"Two hands almost touching across a table in soft morning light, neither pulling away, warm anticipation.","vo":"You may notice you're already looking for someone else's eyes.","on":"","sfx":"A shared breath."},
   {"n":18,"gen":"A title-card background: pure black with slow-drifting gold mist and a single thin horizontal streak of warm light. Abstract, textless.","vo":"","on":"PRESENCE","sfx":"Silence."},
   {"n":19,"gen":"Macro of warm gold light spreading outward from a steady open hand like ripples across still water, dream fog dissolving into soft real light.","vo":"Not to escape your life. To return, and serve it.","on":"","sfx":"The last note fades to warm silence."},
   {"n":20,"gen":"Macro: the gold band come to rest, perfectly still and flat on the dark walnut table, one warm glint along its edge.","vo":"When would now be a good time?","on":"This is not a dream.","sfx":"One soft pulse."}
  ]},
 {"id":"one-ring","title":"ONE RING TO UNITE THEM ALL","after":"after the epic",
  "logline":"An epic-fantasy homage built around the most famous ring shot in cinema — the slow fall onto the finger — recast with our hero user. Not a ring of power that corrupts, a ring of presence that returns. One ring to unite them all: with each other, with the present.",
  "grade":G_LOTR, "music":"A lone fiddle over drone, swelling to full orchestra at the fall, resolving to one warm sustained chord.",
  "social":"60s master · 16:9 + 9:16 crop-safe · hook = the molten-gold macro · captions burned",
  "shots":[
   {"n":1,"gen":"Extreme macro of the inside curve of "+RING+" catching firelight, warm reflections flowing along the polished metal like liquid light.","vo":"It begins with a gift.","on":"","sfx":"A whisper of wind."},
   {"n":2,"gen":"A firelit stone hall, a circle of travelers' hands resting one atop another at the center of a long wooden table, warm fellowship, epic candlelit shadow.","vo":"Not for power. For connection.","on":"","sfx":"A low horn, distant."},
   {"n":3,"gen":"Ultra slow-motion: "+RING+" falling through the air in a sunlit kitchen, dust motes hanging, the ring tumbling gently mid-fall.","vo":"","on":"","sfx":"Deep slow whoosh."},
   {"n":4,"gen":"Extreme slow motion close on a woman's eyes narrowing softly in concentration as a wide gold band falls toward her open hand, firelight catching her focus, shallow epic depth of field.","vo":"Focus was never the world going quiet.","on":"","sfx":"A single sustained string note."},
   {"n":5,"gen":"Macro slow-motion: the gold band landing perfectly onto the outstretched finger of a woman in a warm kitchen, the exact moment of the fit, shallow depth.","vo":"One ring.","on":"","sfx":"Orchestra hits, warm."},
   {"n":6,"gen":"A lone scout atop a windswept ridge glancing briefly down at a small glinting object in his palm, then lifting his eyes to the vast horizon, epic scale, long shadows.","vo":"There are only three reasons to look down on this road. Every other reason, you look up.","on":"","sfx":"Wind, then a horn answering."},
   {"n":7,"reuse":"library/peak/peak-summit-sunrise.png","vo":"Not to rule your life…","on":"","sfx":"Swelling strings."},
   {"n":8,"gen":"Five riders crossing a golden ridge at dusk in silhouette, each carrying a banner of a different warm color — gold, blue-violet, ember, rose, deep violet — against the setting sun, mythic scale.","vo":"Five gifts ride with them.","on":"PRESENCE · PEACE · POWER · PLEASURE · PURPOSE","sfx":"A choir rises softly."},
   {"n":9,"gen":"Sweeping aerial: a small line of friends walking single-file along a vast green mountain ridge at golden hour, epic fantasy scale, long shadows.","vo":"…to return you to it.","on":"","sfx":"Choir under strings."},
   {"n":10,"gen":"A traveler pausing alone at a mountain vista, head tilted back, chest rising in a slow deliberate breath, wind moving her hair, epic golden light.","vo":"They stop only to breathe.","on":"","sfx":"Wind easing to quiet."},
   {"n":11,"gen":"The sun flaring over a misty valley like a great benevolent eye of warm light, god-rays fanning across the land.","vo":"It sees you. And asks for nothing back.","on":"","sfx":"The swell holds."},
   {"n":12,"gen":"Two old friends on a narrow mountain trail, one raising his voice mid-argument then catching himself, his hand settling gently on the other's shoulder, golden-hour warmth.","vo":"Even old friends must learn to soften.","on":"","sfx":"Raised voices, then quiet."},
   {"n":13,"gen":"A long candlelit wooden table crowded with friends laughing, jugs and bread, firelight, fellowship warmth, epic-fantasy tavern glow.","vo":"","on":"ONE RING","sfx":"Fiddle, joyous."},
   {"n":14,"gen":"Firelit tavern scene: a traveler carving a small wooden token by candlelight while others cook and tune a battered stringed instrument nearby, unhurried, warm fellowship.","vo":"Some evenings, they make something instead of consuming it.","on":"","sfx":"A knife against wood, a soft chord."},
   {"n":15,"gen":"Close: a hand hanging at someone's side in a golden wheat field, the wide gold band glinting, wind moving the grass, epic warm light.","vo":"","on":"TO UNITE THEM ALL","sfx":"Orchestra pulls back."},
   {"n":16,"gen":"A traveler walking through a breathtaking valley unseeing, eyes distant and replaying some old argument, the landscape blurred behind him — then his gaze sharpens and the valley resolves into full golden clarity around him.","vo":"Stop watching the movie in your mind.","on":"","sfx":"A distant echo, then birdsong returns."},
   {"n":17,"gen":"Embers in a campfire pulsing gently brighter and dimmer in a slow, steady rhythm, sparks rising into a dark starlit sky.","vo":"Pulse gives you rhythm. Rhythm gives you pause.","on":"","sfx":"A slow drumbeat, matching the embers."},
   {"n":18,"gen":"A title-card background: golden god-rays breaking through mountain mist over a dark valley, abstract and epic, textless.","vo":"One ring to unite them all —","on":"","sfx":"One deep drum."},
   {"n":19,"gen":"The fellowship cresting a final summit together at sunrise, arms loose at their sides, faces lifted into the light, vast golden vista opening before them.","vo":"Not the ring that rules. The ring that returns you — charged, clear, and ready to serve.","on":"","sfx":"Full orchestra, warm and rising."},
   {"n":20,"gen":"A hand slowly raised into sunlight, the gold band catching a clean lens flare against a bright sky.","vo":"— with the present.","on":"Be Here WOW","sfx":"Warm sustained chord."}
  ]},
 {"id":"first-rule","title":"THE FIRST RULE","after":"after the anti-ad",
  "logline":"An anti-marketing film in the grammar of the cult classic: rules delivered straight to camera, gritty and direct. Except the rebellion isn't fighting — it's putting the phone down. Don't post about it. Don't tell your friends. Just be present, and receive the gift of your life. Hook lands in the first three seconds, POV, direct address.",
  "grade":G_FC, "music":"A single dirty bass note under the hook, then near-silence with room tone; one deep pulse at the ring tap.",
  "social":"30–40s master · built 9:16-first · HOOK 0:00–0:03 = shot 1 direct-to-camera · captions burned",
  "shots":[
   {"n":1,"gen":"POV direct-to-camera: a man leaning in close in a dim warm concrete basement, finger pointed straight at the lens, intense but calm eyes, single hanging bulb behind him.","vo":"The first rule of presence: you don't post about it.","on":"RULE 01","sfx":"Dirty bass note. HOOK 0:00–0:03."},
   {"n":2,"gen":"Macro: a smartphone dropping face-down onto a concrete floor, caught the instant before impact, gritty warm light.","vo":"The second rule: you don't post about it.","on":"RULE 02","sfx":"The slap of the phone landing."},
   {"n":3,"gen":"POV direct-to-camera: the same man in the dim concrete basement, calmer now, tapping two fingers against his own wrist where a wide gold band sits, single hanging bulb behind him.","vo":"The third rule: it's a pulse. That's the only word for it.","on":"RULE 03","sfx":"A dirty bass note."},
   {"n":4,"gen":"A night crowd on a street, every face underlit by phone screens except one man looking up at the sky, sodium-vapor warmth against darkness.","vo":"Everyone you know is somewhere else.","on":"","sfx":"Room tone."},
   {"n":5,"gen":"POV direct-to-camera: the man gesturing lightly toward his own temple, gritty warm basement light, steady unblinking eyes.","vo":"The fourth rule: stop watching the movie in your mind.","on":"RULE 04","sfx":"Room tone, then a slow breath."},
   {"n":6,"gen":"Extreme macro: a thumb hovering over a glowing screen, tension in the tendons, everything else in darkness.","vo":"You don't need witnesses.","on":"","sfx":"Silence."},
   {"n":7,"gen":"A cramped warm kitchen at night, one partner's raised hand lowering mid-gesture, shoulders dropping, tension leaving the room, the other partner watching quietly, gritty 35mm intimacy.","vo":"The pulse finds you right before you'd say something you'd regret.","on":"","sfx":"A held breath, then quiet."},
   {"n":8,"gen":"A beautiful dinner on a table, one hand gently pushing a hovering phone down and away from it, warm gritty kitchen light.","vo":"Eat the meal. Don't shoot it.","on":"","sfx":"A fork on a plate."},
   {"n":9,"gen":"POV direct-to-camera: the man leaning back slightly this time, counting on his fingers, dim basement light, calm authority.","vo":"The fifth rule: there are only three reasons to look down — to set your intention, to deepen your practice, to find the others. Every other reason, you look up.","on":"RULE 05","sfx":"A dirty bass note, harder this time."},
   {"n":10,"gen":"A circle of people standing quietly in a bare warm basement room, eyes closed, calm and unbothered, one hanging bulb, gritty warmth.","vo":"We meet where the feed can't find us.","on":"THE PRESENCE CIRCLE","sfx":"Low hum."},
   {"n":11,"gen":"Two people in the bare basement room opening their eyes at the same moment, catching each other's gaze, a small unguarded smile passing between them, no camera in sight, warm low light.","vo":"No one posts the best part.","on":"","sfx":"Quiet laughter, unrecorded."},
   {"n":12,"gen":"Golden-hour street: a man walking away from camera sliding his phone into his back pocket, long warm shadows, free.","vo":"Don't tell your friends.","on":"","sfx":"Street ambience returns."},
   {"n":13,"gen":"POV direct-to-camera: the man now standing near a high basement window with morning light bleeding in behind him, voice steadier, calmer stance.","vo":"The sixth rule: Pulse gives you rhythm. Rhythm gives you pause.","on":"RULE 06","sfx":"The bass note softens into a heartbeat."},
   {"n":14,"gen":"Macro: knuckles of a relaxed hand in the dark, the wide gold band emitting one soft pulse of warm light.","vo":"Don't review it.","on":"","sfx":"ONE deep pulse."},
   {"n":15,"gen":"Close on a pair of hands kneading dough alone in a warm kitchen at night, flour dust catching the light, no phone in the frame, unhurried focus.","vo":"Make something no one will ever see.","on":"","sfx":"The soft press of hands on dough."},
   {"n":16,"gen":"A title-card background: a single bare bulb swinging gently in a dark concrete room, warm halo, textless.","vo":"","on":"JUST BE HERE","sfx":"The bulb's creak."},
   {"n":17,"gen":"POV direct-to-camera: the man almost smiling now, fewer shadows, warmer light filling the basement behind him, voice quieter than before.","vo":"The last rule: you don't get credit for this one.","on":"RULE 07","sfx":"Silence, then the bulb's creak."},
   {"n":18,"gen":"Close on two hands passing a wide gold band gently between them in near-darkness, faces out of frame, warm and unhurried.","vo":"Not so you can prove it. So you can live it.","on":"","sfx":"A single warm pulse."},
   {"n":19,"gen":"A figure stepping out of the dim basement stairwell into full daylight, a phone left behind in soft focus on a table behind him, warm street sound rising.","vo":"You may notice how easy it was to leave it behind.","on":"","sfx":"Street sound rising, warm."},
   {"n":20,"gen":"Close portrait: a face half-lit in warm light, eyes open, the smallest beginning of a smile, completely present.","vo":"","on":"Receive the gift of your life.","sfx":"Silence. End card: This is not an ad. Pulse."}
  ]}
]

# ---- EBI: the mixed-media visual system (illustration ↔ photograph), tied to the motion-rule feet ----
# media per shot: photograph (handheld/lived) · illustration (multiplane/remembered) · hybrid (the turn)
MEDIA={
 "presence-06":"illustration","presence-08":"hybrid","presence-10":"illustration","presence-20":"hybrid",
 "one-ring-03":"illustration","one-ring-05":"hybrid","one-ring-09":"illustration","one-ring-11":"illustration","one-ring-18":"illustration","one-ring-20":"hybrid",
 "first-rule-04":"hybrid","first-rule-16":"illustration","first-rule-20":"hybrid",
}
def media_of(cid): return MEDIA.get(cid,"photograph")
# the pivotal beats regenerated in the brand's mixed-media grammar (the autopilot→presence TURN = the inflection)
_INK="No text, no lettering, no logos, no watermark. Centered, 9:16 crop-safe."
MEDIA_GEN={
 "presence-06":("A hand-painted ILLUSTRATION — gouache and soft screen-print texture, gentle cel-animation warmth, painterly 2.5D, dreamlike: a sunlit residential street curling impossibly upward into a golden sky like a rising wave, houses and trees folding over, surreal but warm. Steel-blue shadows against warm gold. "+_INK),
 "presence-08":("A circular camera APERTURE / iris in the center of the frame reveals a sharp warm PHOTOGRAPH of a human eye opening, a circle of warm gold light reflected in the iris; the surround is loose hand-painted illustration — the aperture focusing out of the drawing into the real. Steel-blue and gold, cinematic. "+_INK),
 "presence-20":("A single cinematic frame that resolves LEFT-to-RIGHT from a hand-painted illustration into a warm real PHOTOGRAPH of the same moment: a wide, smooth, polished gold ring come to rest, perfectly still on a dark walnut table, one warm glint along its edge. The painterly dream on the left settles into real light and texture on the right; the gold ring glints at the seam where illustration becomes photograph. Steel-blue easing to warm gold. "+_INK),
 "one-ring-03":("An epic hand-painted ILLUSTRATION — sweeping painterly gouache, golden god-rays: a wide gold ring falling slowly through the air in a sunlit kitchen, dust motes hanging, mythic and warm. "+_INK),
 "one-ring-05":("A single frame that resolves LEFT-to-RIGHT from an epic hand-painted illustration into a warm real PHOTOGRAPH of the same moment: a wide gold band landing perfectly onto the outstretched finger of a woman in a warm kitchen, the exact instant of the fit. The mythic painterly left settles into real skin and light on the right; the ring glints at the seam. Golden, epic. "+_INK),
 "one-ring-20":("A frame resolving from hand-painted illustration into warm real PHOTOGRAPH: a hand slowly raised into sunlight, the wide gold band catching a clean lens flare against a bright sky — painterly at the wrist becoming photographic at the fingers. Epic golden light. "+_INK),
 "first-rule-04":("A single frame split down the middle: the LEFT half a cold, gritty hand-painted illustration of a night street where every face is underlit by a phone screen; the RIGHT half a warm real PHOTOGRAPH of one man looking up at the sky, sodium-vapor warmth. The cold illustrated feed-world against the warm real present. "+_INK),
 "first-rule-20":("A single frame resolving LEFT-to-RIGHT from a gritty, cold hand-painted illustration into a warm real PHOTOGRAPH: a face half-lit in warm light, eyes open, the smallest beginning of a smile, completely present. The cold illustrated world on the left settles into a warm real present face on the right. Gritty-warm 35mm. "+_INK),
}

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
            med=media_of(cid)
            if "reuse" in s:
                shots.append({**{k:s[k] for k in ("n","vo","on","sfx")},"file":s["reuse"],"reused":True,"media":med})
                continue
            out=OUT/f"{cid}.png"
            shots.append({**{k:s[k] for k in ("n","vo","on","sfx")},"file":f"library/trailers/{cid}.png","media":med})
            if only and only!=cid: continue
            if out.exists() and not force: skip+=1; continue
            prompt=MEDIA_GEN[cid] if cid in MEDIA_GEN else f"{s['gen']} {t['grade']}"
            img=generate(model,key,prompt)
            if img: out.write_bytes(img); ok+=1; print(f"  ok {cid}",flush=True)
            else: failed.append(cid); print(f"  FAIL {cid}",flush=True)
            time.sleep(1)
        data.append({k:t[k] for k in ("id","title","after","logline","music","social")}|{"shots":shots})
    (ROOT/"trailers.json").write_text(json.dumps({"trailers":data},indent=1))
    print(f"\nDone. generated={ok} skipped={skip} failed={len(failed)} · trailers.json written",flush=True)
    if failed: print("failed:",",".join(failed),flush=True)

if __name__=="__main__": main()
