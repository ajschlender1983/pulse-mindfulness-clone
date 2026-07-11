#!/bin/bash
# Generates the storyteller-in-life + inflection collections, resumably.
# Safe to re-run: skips anything already on disk. Rebuilds the manifest at the end.
cd "$(dirname "$0")/.."
M="gemini-3.1-flash-image"
# credit probe
ERR=$(python3 - <<'PY'
import json,urllib.request,urllib.error,pathlib
key=(pathlib.Path.home()/".gemini_api_key").read_text().strip()
req=urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",
 data=json.dumps({"contents":[{"role":"user","parts":[{"text":"hi"}]}]}).encode(),method="POST")
req.add_header("x-goog-api-key",key);req.add_header("Content-Type","application/json")
try: urllib.request.urlopen(req,timeout=60); print("OK")
except urllib.error.HTTPError as e: print("BLOCKED:",json.loads(e.read()).get("error",{}).get("message","")[:80])
PY
)
if [[ "$ERR" != "OK" ]]; then echo "Credits not available — $ERR"; echo "Top up at ai.studio/projects then re-run this script."; exit 1; fi
for i in $(seq 1 40); do
  echo "=== pass $i $(date '+%H:%M') ==="
  python3 tools/generate-storytellers.py --model $M 2>&1 | tail -2
  python3 tools/generate-inflection.py  --model $M 2>&1 | tail -2
  S=$(ls library/storytellers/*.png 2>/dev/null | grep -v gallery | wc -l | tr -d ' ')
  N=$(ls library/inflection/*.png 2>/dev/null | grep -v gallery | wc -l | tr -d ' ')
  echo "have storytellers=$S/40 inflection=$N/18"
  [ "$S" -ge 40 ] && [ "$N" -ge 18 ] && { echo "ALL COMPLETE"; break; }
  sleep 20
done
python3 tools/build-library-manifest.py 2>&1 | tail -4
echo "DONE"
