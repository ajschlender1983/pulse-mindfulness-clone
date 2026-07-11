#!/usr/bin/env python3
"""
Pulse — generate storyteller + inflection collections via Runway Gen-4 Image.
Reuses the exact prompt sets from generate-storytellers.py and
generate-inflection.py (single source), swapping the backend to Runway.

USAGE
  python3 tools/generate-runway.py [--group storytellers|inflection] [--only <id>] [--force]
Output: library/storytellers/<id>.png , library/inflection/<id>.png
"""
import sys, importlib.util, pathlib, time

ROOT=pathlib.Path(__file__).resolve().parent.parent
TOOLS=ROOT/"tools"
sys.path.insert(0, str(TOOLS))
import runway_image as RW  # noqa: E402

def load(modfile):
    spec=importlib.util.spec_from_file_location(modfile.stem.replace("-","_"), modfile)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

ST=load(TOOLS/"generate-storytellers.py")
IN=load(TOOLS/"generate-inflection.py")

def build_storyteller(scene): return f"{scene} {ST.STYLE} Aspect ratio placeholder."[:0] or f"{scene} {ST.STYLE}"
def build_inflection(scene): return f"Scene: {scene}. {IN.INFLECT}"

GROUPS={
 "storytellers": (ST.OUT, ST.SCENES, lambda a,s: f"{s} {ST.STYLE}"),
 "inflection":   (IN.OUT, IN.SCENES, lambda a,s: f"Scene: {s}. {IN.INFLECT}"),
}

def main():
    args=sys.argv[1:]
    group=args[args.index("--group")+1] if "--group" in args else None
    only=args[args.index("--only")+1] if "--only" in args else None
    force="--force" in args
    ok,failed,skip=0,[],0
    for gname,(outdir,scenes,promptfn) in GROUPS.items():
        if group and group!=gname: continue
        outdir.mkdir(parents=True, exist_ok=True)
        for cid,aspect,scene in scenes:
            if only and only!=cid: continue
            out=outdir/f"{cid}.png"
            if out.exists() and not force: skip+=1; continue
            print(f"[{gname}/{cid}]")
            img=RW.generate(promptfn(aspect,scene), aspect=aspect)
            if img: out.write_bytes(img); ok+=1; print(f"  -> {out.name}")
            else: failed.append(cid)
            time.sleep(1)
    print(f"\nDone. generated={ok} skipped={skip} failed={len(failed)}")
    for f in failed: print("  failed:",f)

if __name__=="__main__": main()
