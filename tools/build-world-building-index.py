#!/usr/bin/env python3
"""
Build world-building-index.json from library-manifest.json (single source of truth).
Each collection -> {label, files:[stills... , motion...]}. Run after the manifest.
"""
import json, pathlib
ROOT=pathlib.Path(__file__).resolve().parent.parent
m=json.loads((ROOT/"library-manifest.json").read_text())
out={"collections":{}}
tot=0
for key,c in m["collections"].items():
    files=list(c.get("files_stills",[]))+list(c.get("files_motion",[]))
    out["collections"][key]={"label":c["label"],"files":files}
    tot+=len(files)
(ROOT/"world-building-index.json").write_text(json.dumps(out,indent=1))
print(f"world-building-index.json: {len(out['collections'])} collections, {tot} files")
