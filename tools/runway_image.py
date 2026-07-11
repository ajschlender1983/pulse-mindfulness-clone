#!/usr/bin/env python3
"""
Runway ML Gen-4 Image client — text-to-image for the Pulse library.
Submits a text_to_image task, polls to completion, downloads the PNG bytes.

Key resolution order: RUNWAY_API_KEY env → Pulse-Testimonial-Studio/.env.
Never prints the key.
"""
import os, re, json, time, urllib.request, urllib.error, pathlib

BASE="https://api.dev.runwayml.com/v1"; VER="2024-11-06"
# gen4_image supported ratios (closest to our aspect intents)
RATIO={"3:2":"1440:1080","4:5":"1080:1440","16:9":"1920:1080","1:1":"1024:1024",
       "9:16":"1080:1920","2:3":"1080:1440"}

def get_key():
    k=os.environ.get("RUNWAY_API_KEY")
    if k: return k.strip()
    for p in [pathlib.Path.home()/"Desktop"/"Pulse-Testimonial-Studio"/".env",
              pathlib.Path(__file__).resolve().parent.parent.parent/"Pulse-Testimonial-Studio"/".env"]:
        if p.exists():
            m=re.search(r'RUNWAY_API_KEY\s*=\s*["\']?([^"\'\n]+)', p.read_text())
            if m: return m.group(1).strip()
    raise SystemExit("No RUNWAY_API_KEY (env or studio .env)")

_KEY=None
def key():
    global _KEY
    if _KEY is None: _KEY=get_key()
    return _KEY

def _req(path, body=None):
    r=urllib.request.Request(f"{BASE}/{path}", data=(json.dumps(body).encode() if body else None),
                             method=("POST" if body else "GET"))
    r.add_header("Authorization",f"Bearer {key()}"); r.add_header("Content-Type","application/json")
    r.add_header("X-Runway-Version",VER)
    return urllib.request.urlopen(r, timeout=90)

def generate(prompt, aspect="3:2", model="gen4_image", poll_s=5, max_poll=48, tries=3):
    """Return PNG bytes, or None on failure. Retries submit on 429/5xx."""
    ratio=RATIO.get(aspect,"1440:1080")
    body={"model":model,"promptText":prompt[:1000],"ratio":ratio}
    tid=None
    for a in range(tries):
        try:
            resp=json.loads(_req("text_to_image", body).read()); tid=resp.get("id"); break
        except urllib.error.HTTPError as e:
            code=e.code; msg=e.read().decode()[:200]
            if code in (429,502,503):
                time.sleep(5*(a+1)); continue
            print(f"    ! submit HTTP {code}: {msg}"); return None
        except Exception as ex:
            time.sleep(3); continue
    if not tid: print("    ! submit failed"); return None
    for _ in range(max_poll):
        time.sleep(poll_s)
        try:
            t=json.loads(_req(f"tasks/{tid}").read())
        except Exception:
            continue
        st=t.get("status")
        if st=="SUCCEEDED":
            urls=t.get("output") or []
            if not urls: return None
            for _ in range(3):
                try:
                    return urllib.request.urlopen(urls[0], timeout=90).read()
                except Exception:
                    time.sleep(3)
            return None
        if st in ("FAILED","CANCELLED"):
            print(f"    ! task {st}: {t.get('failure') or ''} {t.get('failureCode') or ''}"); return None
    print("    ! poll timeout"); return None

def credits_ok():
    """Cheap liveness/credit probe: submit + immediately check for a hard error."""
    try:
        resp=json.loads(_req("text_to_image", {"model":"gen4_image","promptText":"a gold ring on stone","ratio":"1024:1024"}).read())
        return True, resp.get("id")
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}: {e.read().decode()[:160]}"
