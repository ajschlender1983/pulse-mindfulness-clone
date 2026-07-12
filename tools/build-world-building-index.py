#!/usr/bin/env python3
"""
Build world-building-index.json (v2) — grouped, kind-tagged, persona-derived.
Single source of truth the World-Building app reads. Run after build-library-manifest.py.

Schema:
{
  "groups":[{id,label,blurb,order}],
  "collections":[
    {id, group, kind:"gallery|sequence|persona|link", title, description,
     count, thumb, bio?(persona), link?(link),
     items:[{file, caption?, order?}]}
  ],
  "counts":{groups,collections,files}
}
Personas (bios + captions) are HARVESTED from the generator prompts — zero hand-maintenance.
"""
import json, pathlib, re, importlib.util

ROOT = pathlib.Path(__file__).resolve().parent.parent
def nat(s): return [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', s)]
def load(f):
    s=importlib.util.spec_from_file_location(f.stem.replace('-','_'),f); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def globs(*pats, exclude=None):
    out=[]
    for p in pats:
        for f in ROOT.glob(p):
            if exclude and re.search(exclude,f.name): continue
            out.append(str(f.relative_to(ROOT)))
    return sorted(set(out), key=nat)
def first_sentence(s):
    s=re.sub(r'\s+',' ',s).strip()
    m=re.split(r'(?<=[.!?]) ', s)
    return (m[0] if m else s).strip()

GROUPS=[
 ("people","The People","Who Pulse is for — the faces, the personas, the cast.",1),
 ("stories","The Stories","Ordered narratives you scroll frame by frame.",2),
 ("moments","The Moments","The felt experience — unordered pools of the world.",3),
 ("craft","The Craft","Rendering and style studies — how the world is drawn.",4),
 ("motion","In Motion","Moving image — loops, b-roll, and the motion rules.",5),
 ("message","The Message","Deployment-ready surfaces.",6),
]

# section collections: manifest-key -> (group, kind, description, link?)
SECTION_META={
 "storytellers":("people","gallery","The wider cast, out in the world — forty candid, in-life moments."),
 "invitations":("stories","link","“When would now be a good time?” — the manifesto and twenty three-frame invitation stories.","now-a-good-time.html"),
 "film-strip":("stories","sequence","The Movie of Your Life — autopilot as a strip running too fast, the pulse slowing it to one held moment."),
 "inflection":("stories","gallery","The inflection — illustration resolving into photograph, the ring as the hinge into presence."),
 "peak":("moments","gallery","Out-in-the-world peak experiences — summits, waterfalls, aurora, dunes, alpine swims."),
 "ethereal":("moments","gallery","The ring as presence — ethereal light-leak stills and motion, the world warming."),
 "hybrid":("moments","gallery","Illustration ↔ photograph — two hundred hybrid frames across ten composition rules."),
 "illustrations":("craft","gallery","The painterly journey — one hundred hand-illustrated frames, gouache and cel-warmth."),
 "studio-frames":("craft","gallery","Pulse Filmmaker hero frames — the light-thread b-roll stills."),
 "texture":("craft","gallery","Texture, macro & symbol — the sensory close-ups the world is built from."),
 "performance":("craft","gallery","The pause inside effort — presence held under pressure."),
 "email-heroes":("message","gallery","The lifecycle, illustrated — one hero per email across the two visual worlds."),
 "motion-loops":("motion","gallery","Funnel motion loops — breathing Ken-Burns and same-moment morphs."),
 "studio-broll":("motion","gallery","Ethereal b-roll — the ring-as-presence in gentle motion."),
 "motion-illustration":("motion","gallery","Motion rule · the illustration foot — composed camera, on rails, no handheld."),
 "motion-transition":("motion","gallery","Motion rule · the transition — illustration resolving into photograph, timed to the pulse."),
 "motion-photograph":("motion","gallery","Motion rule · the photograph foot — handheld cell-phone motion, alive and present."),
 "studio-films":("motion","gallery","Finished testimonial films — the full cut."),
}
# manifest collections folded into personas (dropped as flat collections)
SUBSUMED={"avatars","avatar-spectrum","stories","journey"}

def build_personas():
    personas=[]
    # --- named storytellers (bios + captions harvested) ---
    story_dicts=[]
    for gen in ["generate-story-images.py","generate-library-expansion-2.py"]:
        try: story_dicts.append(load(ROOT/"tools"/gen).STORIES)
        except Exception: pass
    merged={}
    for d in story_dicts:
        for k,v in d.items(): merged[k]=v
    for name,info in merged.items():
        cap={}
        for fr in info.get("frames",[]):
            fid=fr[0]; caption=fr[-1] if isinstance(fr[-1],str) else ""
            cap[fid]=caption
        files=globs(f"library/stories/{name}-[0-9]*.png", f"story-images/{name}-[0-9]*.png", exclude=r"reference")
        if not files: continue
        items=[]
        for i,f in enumerate(files):
            stem=pathlib.Path(f).stem
            items.append({"file":f,"order":i+1,"caption":first_sentence(cap.get(stem,""))[:90]})
        title=info.get("title","").split(" — ")[0].strip() or name.replace("-"," ").title()
        title=name.split("-")[0].title() if not title else title
        bio=first_sentence(info.get("who","")).replace("A ","",1)
        personas.append({"id":f"persona-{name}","group":"people","kind":"persona",
            "title":title if "—" not in title else title.split("—")[0].strip(),
            "description":f"{len(items)}-frame story · a named Pulse persona.",
            "bio":bio, "count":len(items), "thumb":items[0]["file"], "items":items})
    # --- Maya (the journey arc) ---
    maya=globs("journey-images/*.png", exclude=r"(reference|gallery|00b-|00-)")
    if maya:
        items=[{"file":f,"order":i+1,"caption":re.sub(r'[-_]',' ',pathlib.Path(f).stem)} for i,f in enumerate(maya)]
        personas.append({"id":"persona-maya","group":"people","kind":"persona","title":"Maya",
            "description":"The journey arc · numb → generous, seven stages.","bio":"38, charge nurse, mother to Priya — the brand's north-star persona, from numb to generous.",
            "count":len(items),"thumb":items[0]["file"],"items":items})
    # --- 22 avatars (portrait + illustration→real) ---
    av_bios={}
    try:
        e1=load(ROOT/"tools"/"generate-library-expansion.py")
        for cid,asp,c in e1.AVATARS: av_bios[cid]=first_sentence(c).replace("A ","",1)
    except Exception: pass
    try:
        e2=load(ROOT/"tools"/"generate-library-expansion-2.py")
        for cid,c in e2.PERSONAS: av_bios[cid]=first_sentence(c).replace("A ","",1)
    except Exception: pass
    for n in range(1,23):
        aid=f"avatar-{n:02d}"
        port=f"library/avatars/{aid}.png"; spec=f"library/avatar-spectrum/{aid}-spectrum.png"
        items=[]
        if (ROOT/port).exists(): items.append({"file":port,"order":1,"caption":"portrait"})
        if (ROOT/spec).exists(): items.append({"file":spec,"order":2,"caption":"illustration → real life"})
        if not items: continue
        bio=av_bios.get(aid,"A member of the Pulse cast.")
        # title: a short human label — strip the leading age, take up to the first comma
        lbl=re.sub(r'^\d+-year-old\s+','',bio).split(',')[0].strip()
        lbl=re.sub(r'\band\b.*$','',lbl).strip()
        if len(lbl)>32: lbl=lbl[:32].rsplit(' ',1)[0]+"…"
        title=(lbl[:1].upper()+lbl[1:]) if lbl else f"Cast · {aid.split('-')[1]}"
        personas.append({"id":f"persona-{aid}","group":"people","kind":"persona","title":title,
            "description":f"{len(items)} frames · portrait and illustration↔real.","bio":bio,
            "count":len(items),"thumb":items[0]["file"],"items":items})
    return personas

def main():
    man=json.loads((ROOT/"library-manifest.json").read_text())
    collections=[]
    # section collections (from manifest, folded to v2)
    for key,c in man["collections"].items():
        if key in SUBSUMED: continue
        meta=SECTION_META.get(key)
        if not meta:  # any unmapped -> moments gallery (never drop)
            meta=("moments","gallery",c["label"],None)
        group,kind,desc=meta[0],meta[1],meta[2]
        link=meta[3] if len(meta)>3 else None
        files=list(c.get("files_stills",[]))+list(c.get("files_motion",[]))
        if not files and kind!="link": continue
        thumb=files[len(files)//2] if files else None
        col={"id":key,"group":group,"kind":kind,"title":c["label"],"description":desc,
             "count":len(files),"thumb":thumb,"items":[{"file":f} for f in files]}
        if link: col["link"]=link
        collections.append(col)
    # personas
    collections.extend(build_personas())
    # order: by group order then personas last within people
    gorder={g[0]:g[3] for g in GROUPS}
    collections.sort(key=lambda c:(gorder.get(c["group"],9), 0 if c["kind"]!="persona" else 1, c["title"]))

    total=sum(c["count"] for c in collections)
    out={"groups":[{"id":g[0],"label":g[1],"blurb":g[2],"order":g[3]} for g in GROUPS],
         "collections":collections,
         "counts":{"groups":len(GROUPS),"collections":len(collections),"files":total}}
    (ROOT/"world-building-index.json").write_text(json.dumps(out,indent=1))
    # report
    from collections import Counter
    bg=Counter(c["group"] for c in collections); bk=Counter(c["kind"] for c in collections)
    print(f"world-building-index.json v2: {len(collections)} collections, {total} items")
    print("  by group:", dict(bg)); print("  by kind:", dict(bk))
    print("  personas:", sum(1 for c in collections if c["kind"]=="persona"))

if __name__=="__main__": main()
