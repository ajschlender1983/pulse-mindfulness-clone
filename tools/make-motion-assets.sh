#!/bin/bash
# Pulse — motion assets from stills (seamless breathing Ken Burns loops)
# For each source still: an 8-second seamless zoom-breathe loop as MP4 (small,
# for web <video>) and GIF (for email clients / quick embeds).
# Usage: bash tools/make-motion-assets.sh
set -uo pipefail
cd "$(dirname "$0")/.."
OUT=motion
mkdir -p "$OUT"

# source stills -> loop name (story leads + signature heroes)
SOURCES=(
  "story-images/ingrid-1.png:ingrid-mat"
  "story-images/theo-4.png:theo-focus"
  "story-images/rosa-1.png:rosa-notebook"
  "story-images/darius-1.png:darius-train"
  "story-images/amara-ben-3.png:amara-ben-hands"
  "emails/images/hero-email-charge-pair-breathe.png:arrival-unboxing"
  "emails/images/hero-email-give-a-month.png:referral-pour"
  "emails/images/hero-email-order-confirmed.png:luxe-ring"
  "emails/images/hero-email-sunday-pause.png:sunday-pause"
  "emails/images/hero-email-quiz-results-soft.png:maya-car-soft"
)

FPS=25; DUR=8
FRAMES=$((FPS*DUR))

made=0; missing=0
for pair in "${SOURCES[@]}"; do
  src="${pair%%:*}"; name="${pair##*:}"
  if [ ! -f "$src" ]; then echo "missing: $src"; missing=$((missing+1)); continue; fi
  mp4="$OUT/$name.mp4"; gif="$OUT/$name.gif"
  if [ -f "$mp4" ] && [ -f "$gif" ]; then continue; fi
  # seamless breathe: zoom oscillates over the loop (sin). Scale-to-COVER then
  # center-crop to a uniform 3:2 first, so portrait/square/wide sources are never
  # stretched — only cropped. (Bug fixed: zoompan s=WxH used to force-distort.)
  ffmpeg -y -loglevel error -loop 1 -i "$src" -t $DUR -vf "
    scale=1920:1280:force_original_aspect_ratio=increase,
    crop=1920:1280,
    zoompan=z='1.05+0.03*sin(2*PI*on/$FRAMES)':d=$FRAMES:fps=$FPS:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x854,
    format=yuv420p" -c:v libx264 -preset slow -crf 24 -movflags +faststart "$mp4" || { echo "mp4 fail: $name"; continue; }
  ffmpeg -y -loglevel error -i "$mp4" -vf "fps=12,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4" -loop 0 "$gif" || echo "gif fail: $name"
  echo "made: $name"
  made=$((made+1))
done
echo "motion done: made=$made missing=$missing"
du -sh "$OUT" 2>/dev/null
