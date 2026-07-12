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

STYLE=("A stylized editorial ILLUSTRATION rendered from a real photograph — a recognizable, true-to-life "
 "likeness, then hand-illustrated: confident inked linework over warm gouache and soft screen-print "
 "shading, gentle painterly cel-animation finish, editorial and characterful. Keep the real person clearly "
 "recognizable (accurate face, proportions, signature look) but unmistakably an illustration, not a photo. "
 "Head-and-shoulders, face centered and facing forward, soft neutral cream-to-honey background, warm honey "
 "and gold palette, gentle rim light, a calm approachable expression. No text, no logos, no watermark. "
 "Square 1:1, framed for a circular avatar crop.")
# stylized illustrations OF the actual public figures (recognizable likeness, per Adam's direction)
ADV=[
 ("hormozi","Alex Hormozi, the entrepreneur and author of $100M Offers — a very muscular, powerfully built bald man in his mid-30s with a FULL thick dark well-groomed beard covering the jaw, a broad square face, thick neck, olive-tan skin, heavy dark eyebrows and an intense direct confident gaze, wearing a plain fitted black crew-neck t-shirt over big shoulders"),
 ("godin","Seth Godin, the marketing author of Purple Cow and This Is Marketing — a warm bald man in his 60s with round wire glasses, an animated knowing smile, often a bright yellow accent"),
 ("watts","Alan Watts, the British philosopher of Zen and presence — a serene man in his 50s-60s with swept-back greying hair and a trimmed goatee, twinkling amused eyes, mid-century intellectual air"),
 ("jobs","Steve Jobs, the Apple co-founder — a lean man with a short grey beard, round rimless glasses, and a simple black turtleneck, thoughtful intense expression"),
 ("sutherland","Rory Sutherland, Ogilvy vice-chairman and author of Alchemy — a genial ruddy-cheeked British man in his late 50s with tousled greying hair, round glasses, a rumpled jacket, and a wry warm smile"),
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
