#!/usr/bin/env python3
"""Pulse — advisory board profile icons (stylized painterly, non-photoreal archetypes).
Output: library/advisors/<id>.png  (square, face-centered for circular crop)."""
import os,sys,base64,json,urllib.request,urllib.error,pathlib,time
API="https://generativelanguage.googleapis.com/v1beta"
ROOT=pathlib.Path(__file__).resolve().parent.parent; OUT=ROOT/"library"/"advisors"
def key():
    f=pathlib.Path.home()/".gemini_api_key"; return f.read_text().strip()
def api(p,k,b=None):
    r=urllib.request.Request(f"{API}/{p}",data=(json.dumps(b).encode() if b else None),method="POST" if b else "GET")
    r.add_header("x-goog-api-key",k); r.add_header("Content-Type","application/json")
    return json.loads(urllib.request.urlopen(r,timeout=180).read())
def gen(m,k,prompt,tries=3):
    for cfg in [{"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"1:1"}}},
                {"generationConfig":{"responseModalities":["TEXT","IMAGE"]}}]:
        b={"contents":[{"role":"user","parts":[{"text":prompt}]}],**cfg}
        for a in range(tries):
            try:
                resp=api(f"models/{m}:generateContent",k,b)
                for c in resp.get("candidates",[]):
                    for part in c.get("content",{}).get("parts",[]):
                        d=part.get("inlineData") or part.get("inline_data")
                        if d and d.get("data"): return base64.b64decode(d["data"])
                break
            except urllib.error.HTTPError as e:
                if e.code in (429,500,503): time.sleep(3*(a+1)); continue
                break
    return None

STYLE=("Stylized hand-painted portrait, warm gouache and soft screen-print texture, gentle cel-animation "
 "warmth, editorial and dreamlike, clearly an ILLUSTRATION (not a photograph). Head-and-shoulders, face "
 "centered and facing forward, soft neutral cream-to-honey background, warm honey and gold palette, gentle "
 "rim light. A calm, wise, approachable expression. No text, no logos, no watermark. Square 1:1, framed for "
 "a circular avatar crop.")
# archetype descriptions — evoke the figure's signature look without photoreal likeness
ADV=[
 ("hormozi","a fit, bald man in his mid-30s with a short dark beard, broad shoulders, wearing a plain dark crew-neck t-shirt, direct confident gaze"),
 ("godin","a warm bald man with round wire glasses and a bright yellow scarf or collar accent, kind animated smile, mid-50s"),
 ("watts","a serene elderly man with swept-back silver hair and a trimmed grey goatee, twinkling amused eyes, soft earth-toned collar, 1960s intellectual air"),
 ("jobs","a lean man in his 40s with a short grey beard, round rimless glasses, a simple black turtleneck, thoughtful intense expression"),
 ("sutherland","a genial ruddy-cheeked British man in his 50s, tousled hair, round glasses, a slightly rumpled tweed jacket, wry warm smile"),
]
def main():
    k=key(); m="gemini-3.1-flash-image"; OUT.mkdir(parents=True,exist_ok=True)
    ok=0
    for cid,desc in ADV:
        out=OUT/f"{cid}.png"
        if out.exists() and "--force" not in sys.argv: print("skip",cid); continue
        print("[",cid,"]")
        img=gen(m,k,f"Portrait of {desc}. {STYLE}")
        if img: out.write_bytes(img); ok+=1
        else: print("  FAILED",cid)
        time.sleep(1)
    print("done",ok)
if __name__=="__main__": main()
