#!/usr/bin/env python3
"""
Veo 3.1 image-to-video client (Gemini API) for the Pulse motion library.
Turns a still frame + a motion prompt into a real video clip.

Key: ~/.gemini_api_key (same as the image pipeline).
Usage as a module: veo_video.generate(image_path, prompt, out_path, model=..., seconds=..., aspect=...)
CLI test:  python3 tools/veo_video.py <image.png> "<prompt>" <out.mp4> [--model veo-3.1-fast-generate-preview] [--seconds 6]
"""
import os, sys, json, base64, time, urllib.request, urllib.error, pathlib

API="https://generativelanguage.googleapis.com/v1beta"
def key():
    k=os.environ.get("GEMINI_API_KEY")
    if k: return k.strip()
    return (pathlib.Path.home()/".gemini_api_key").read_text().strip()

def _post(path, body):
    r=urllib.request.Request(f"{API}/{path}", data=json.dumps(body).encode(), method="POST")
    r.add_header("x-goog-api-key", key()); r.add_header("Content-Type","application/json")
    return json.loads(urllib.request.urlopen(r, timeout=120).read())
def _get(path):
    r=urllib.request.Request(f"{API}/{path}")
    r.add_header("x-goog-api-key", key())
    return json.loads(urllib.request.urlopen(r, timeout=120).read())

def _extract_video_bytes(op):
    """Walk the finished operation for inline video bytes or a file uri."""
    resp=op.get("response",{})
    # common shapes
    cands=[]
    gvr=resp.get("generateVideoResponse") or resp
    for keyname in ("generatedSamples","generatedVideos","samples","videos"):
        if keyname in gvr: cands=gvr[keyname]; break
    if not cands and "video" in gvr: cands=[gvr]
    for c in cands:
        v=c.get("video") or c
        b=v.get("bytesBase64Encoded") or v.get("videoBytes") or v.get("imageBytes")
        if b: return ("bytes", b)
        uri=v.get("uri") or v.get("fileUri") or (v.get("file") or {}).get("uri")
        if uri: return ("uri", uri)
    return (None, json.dumps(resp)[:400])

def generate(image_path, prompt, out_path, model="veo-3.1-fast-generate-preview",
             seconds=6, aspect="16:9", audio=False, poll=8, timeout=420):
    img=pathlib.Path(image_path).read_bytes()
    b64=base64.b64encode(img).decode()
    mime="image/png" if str(image_path).lower().endswith(".png") else "image/jpeg"
    params={"aspectRatio":aspect}
    body={"instances":[{"prompt":prompt,"image":{"bytesBase64Encoded":b64,"mimeType":mime}}],
          "parameters":params}
    try:
        op=_post(f"models/{model}:predictLongRunning", body)
    except urllib.error.HTTPError as e:
        return {"ok":False,"error":f"HTTP {e.code}: {e.read().decode()[:300]}"}
    name=op.get("name")
    if not name: return {"ok":False,"error":"no operation name: "+json.dumps(op)[:300]}
    t0=time.time()
    while time.time()-t0 < timeout:
        time.sleep(poll)
        try: st=_get(name)
        except Exception as e: continue
        if st.get("done"):
            if "error" in st: return {"ok":False,"error":json.dumps(st["error"])[:400]}
            kind,val=_extract_video_bytes(st)
            if kind=="bytes":
                pathlib.Path(out_path).write_bytes(base64.b64decode(val)); return {"ok":True,"secs":round(time.time()-t0)}
            if kind=="uri":
                # download file uri (append key)
                u=val + (("&" if "?" in val else "?")+"key="+key())
                try:
                    data=urllib.request.urlopen(urllib.request.Request(u), timeout=120).read()
                    pathlib.Path(out_path).write_bytes(data); return {"ok":True,"secs":round(time.time()-t0),"via":"uri"}
                except Exception as e:
                    return {"ok":False,"error":"uri dl failed: "+str(e)[:200]+" uri="+val[:120]}
            return {"ok":False,"error":"done but no video: "+str(val)}
    return {"ok":False,"error":"timeout"}

if __name__=="__main__":
    a=sys.argv[1:]
    img,prompt,out=a[0],a[1],a[2]
    model=a[a.index("--model")+1] if "--model" in a else "veo-3.1-fast-generate-preview"
    secs=int(a[a.index("--seconds")+1]) if "--seconds" in a else 6
    print("generating…", model, secs,"s", flush=True)
    res=generate(img,prompt,out,model=model,seconds=secs)
    print(json.dumps(res))
