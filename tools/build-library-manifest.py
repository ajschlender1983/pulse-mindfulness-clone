#!/usr/bin/env python3
"""
Pulse — library manifest + gallery builder (single source of truth)
===================================================================
Scans the real folders, writes library-manifest.json with honest per-collection
and grand-total counts, generates a complete contact-sheet gallery per
collection under library/gallery/, and stamps the atlas (image-library.html)
so its counts and "View all N" links can never drift from what exists on disk.

Run:  python3 tools/build-library-manifest.py
"""
import json, pathlib, re, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
GAL  = ROOT / "library" / "gallery"

# natural sort so foo-2 < foo-10
def nat(s): return [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', s)]

# collection definitions: key, label, globs, kind, curated hero picks (basenames)
COLLECTIONS = [
 {"key":"ethereal","label":"The ring as presence","kind":"mixed",
  "stills":["library/ethereal/*.png"], "motion":["library/ethereal/motion/*.mp4"],
  "curate":6},
 {"key":"avatars","label":"Storytellers","kind":"stills",
  "stills":["library/avatars/*.png"], "curate":10},
 {"key":"storytellers","label":"Storytellers, in life","kind":"stills",
  "stills":["library/storytellers/*.png"], "exclude":r"gallery", "curate":12},
 {"key":"inflection","label":"The inflection — illustration to photograph","kind":"stills",
  "stills":["library/inflection/*.png"], "exclude":r"gallery", "curate":10},
 {"key":"performance","label":"Performance — the pause inside effort","kind":"stills",
  "stills":["library/performance/*.png"], "curate":8},
 {"key":"stories","label":"User stories","kind":"stills",
  "stills":["story-images/*.png","library/stories/*.png"],
  "exclude":r"(00-.*-reference|gallery)", "curate":12},
 {"key":"journey","label":"The journey arc — numb to generous","kind":"stills",
  "stills":["journey-images/*.png"], "exclude":r"(reference|gallery|00b-)", "curate":7},
 {"key":"film-strip","label":"The Movie of Your Life","kind":"mixed",
  "stills":["film-strip/same/moment-*.png","film-strip/autopilot/auto-*.png"],
  "motion":["film-strip/motion/held-loop.mp4"], "curate":8},
 {"key":"email-heroes","label":"Email heroes — the lifecycle, illustrated","kind":"stills",
  "stills":["emails/images/*.png"], "exclude":r"(00-.*-reference|gallery)", "curate":12},
 {"key":"texture","label":"Texture, macro & symbol","kind":"stills",
  "stills":["library/texture/*.png"], "curate":18},
 {"key":"motion-loops","label":"Motion — funnel loops","kind":"motion",
  "motion":["motion/*.mp4"], "curate":8},
 {"key":"studio-broll","label":"Motion — ethereal b-roll","kind":"motion",
  "motion":["library/studio-broll/web/*.mp4"], "curate":6},
 {"key":"studio-films","label":"Finished testimonial films","kind":"motion",
  "motion":["library/studio-stories/*.mp4"], "curate":3},
]

def expand(globs, exclude):
    out=[]
    for g in globs:
        for p in ROOT.glob(g):
            rel=str(p.relative_to(ROOT))
            if exclude and re.search(exclude, p.name): continue
            out.append(rel)
    return sorted(set(out), key=nat)

def poster_for(mp4_rel):
    # b-roll/story posters live in library/posters/broll-<name>.jpg or story-<name>.jpg
    name=pathlib.Path(mp4_rel).stem
    for cand in [f"library/posters/broll-{name}.jpg", f"library/posters/story-{name}.jpg",
                 f"library/posters/{name}.jpg"]:
        if (ROOT/cand).exists(): return cand
    return None

def main():
    manifest={"generated":"BUILD", "collections":{}}
    total_stills=total_motion=0
    seen=set()
    for c in COLLECTIONS:
        exclude=c.get("exclude")
        stills=[f for f in expand(c.get("stills",[]), exclude) if f not in seen]
        motion=[f for f in expand(c.get("motion",[]), exclude) if f not in seen]
        for f in stills+motion: seen.add(f)
        total_stills+=len(stills); total_motion+=len(motion)
        cur=c.get("curate",8)
        # curated hero picks: evenly spaced across the set for variety
        pool=stills if stills else motion
        if len(pool)<=cur: picks=pool
        else:
            step=len(pool)/cur; picks=[pool[int(i*step)] for i in range(cur)]
        manifest["collections"][c["key"]]={
            "label":c["label"], "kind":c["kind"],
            "stills":len(stills), "motion":len(motion),
            "gallery":f"library/gallery/{c['key']}.html",
            "curated":picks, "files_stills":stills, "files_motion":motion}
    manifest["grand_total_stills"]=total_stills
    manifest["grand_total_motion"]=total_motion
    manifest["collection_count"]=len(COLLECTIONS)
    (ROOT/"library-manifest.json").write_text(json.dumps(manifest,indent=2))

    # generate one contact-sheet gallery per collection
    GAL.mkdir(parents=True, exist_ok=True)
    for key,c in manifest["collections"].items():
        tiles=[]
        for f in c["files_stills"]:
            tiles.append(f'<figure><img loading="lazy" src="../../{f}"><figcaption>{pathlib.Path(f).name}</figcaption></figure>')
        for f in c["files_motion"]:
            pos=poster_for(f); p=f' poster="../../{pos}"' if pos else ''
            tiles.append(f'<figure><video loading="lazy" src="../../{f}"{p} muted loop playsinline onmouseover="this.play()" onmouseout="this.pause()"></video><figcaption>{pathlib.Path(f).name}</figcaption></figure>')
        n=c["stills"]+c["motion"]
        (GAL/f"{key}.html").write_text(f"""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width, initial-scale=1">
<title>Pulse library — {c['label']} ({n})</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:opsz,wght@9..40,400;9..40,600&display=swap" rel=stylesheet>
<style>body{{background:#EBE7D4;font-family:'DM Sans',system-ui;margin:0;padding:clamp(24px,5vw,52px);color:#1A1C22;letter-spacing:-.02em}}
a{{color:#A67C00}} .top{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:8px}}
.top a{{font-family:'DM Mono',monospace;font-size:12px;text-decoration:none;color:#6E6857}} .top a:hover{{color:#1A1C22}}
h1{{font-weight:600;font-size:clamp(26px,5vw,40px);letter-spacing:-.04em;margin:10px 0 4px}}
.sub{{font-family:'DM Mono',monospace;font-size:12px;color:#6E6857;letter-spacing:.06em;text-transform:uppercase}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px;margin-top:26px}}
figure{{margin:0;background:#F9F6E5;border:1px solid rgba(26,28,34,.14);border-radius:12px;overflow:hidden;box-shadow:0 12px 30px rgba(66,61,50,.08)}}
img,video{{width:100%;display:block;aspect-ratio:3/2;object-fit:cover}}
figcaption{{font-family:'DM Mono',monospace;font-size:10.5px;color:#6E6857;padding:8px 11px}}</style></head>
<body><div class=top><a href="../../image-library.html">← Atlas</a><a href="../../builds.html">Builds</a></div>
<h1>{c['label']}</h1><div class=sub>{n} frames · complete set</div>
<div class=grid>{''.join(tiles)}</div></body></html>""")

    # build the collections-index grid (auto-honest cards, one per collection)
    cards=[]
    for key,c in manifest["collections"].items():
        n=c["stills"]+c["motion"]
        bits=[]
        if c["stills"]: bits.append(f"{c['stills']} stills")
        if c["motion"]: bits.append(f"{c['motion']} motion")
        cards.append(f'<a class="ci-card" href="{c["gallery"]}"><span class="ci-n">{n}</span>'
                     f'<span class="ci-label">{c["label"]}</span><span class="ci-sub">{" · ".join(bits)} · view all →</span></a>')
    index_html='<div class="ci-grid">'+''.join(cards)+'</div>'

    # stamp the atlas: fill totals tokens + inject collections index + View-all hrefs
    atlas=ROOT/"image-library.html"
    if atlas.exists():
        h=atlas.read_text()
        h=h.replace("{{STILLS_TOTAL}}",str(total_stills)).replace("{{MOTION_TOTAL}}",str(total_motion)).replace("{{COLLECTION_COUNT}}",str(len(COLLECTIONS)))
        h=re.sub(r'(<!--COLLECTIONS_INDEX_START-->).*?(<!--COLLECTIONS_INDEX_END-->)',
                 r'\1'+index_html+r'\2', h, flags=re.S)
        for key,c in manifest["collections"].items():
            n=c["stills"]+c["motion"]
            h=re.sub(r'(data-collection="'+re.escape(key)+r'"[^>]*>.*?<a class="viewall" href=")[^"]*(">View all <span class="count">)\d+(</span>)',
                     r'\g<1>'+c["gallery"]+r'\g<2>'+str(n)+r'\g<3>', h, flags=re.S)
        atlas.write_text(h)

    # print honest table
    print(f"{'collection':<28}{'stills':>7}{'motion':>7}")
    for key,c in manifest["collections"].items():
        print(f"{c['label'][:27]:<28}{c['stills']:>7}{c['motion']:>7}")
    print("-"*42)
    print(f"{'GRAND TOTAL':<28}{total_stills:>7}{total_motion:>7}")
    print(f"\nmanifest: library-manifest.json · galleries: library/gallery/*.html ({len(COLLECTIONS)})")

if __name__=="__main__":
    main()
