#!/bin/bash
# Stitch the 24 same-moment frames into a seamless "held moment" loop.
# The frames are generated independently, so framing drifts slightly between
# them — a hard 24fps cut would jitter. Instead we motion-BLEND (crossfade
# tween) them into a slow dreamy morph, then ping-pong for a seamless loop:
# the single moment, unfolding and breathing. This is "24 frames of one moment"
# rendered the way memory actually holds it.
set -uo pipefail
cd "$(dirname "$0")/.."
OUT=film-strip
SAME="$OUT/same"
mkdir -p "$OUT/motion"

n=$(ls "$SAME"/moment-*.png 2>/dev/null | wc -l | tr -d ' ')
if [ "$n" -lt 24 ]; then echo "need 24 same-moment frames, have $n"; exit 1; fi

# 1) normalize every frame to a uniform 1280x854 (cover-crop, no stretch)
tmp=$(mktemp -d); i=0
for f in $(ls "$SAME"/moment-*.png | sort); do
  printf -v idx "%03d" "$i"
  ffmpeg -y -loglevel error -i "$f" -vf "scale=1280:854:force_original_aspect_ratio=increase,crop=1280:854" "$tmp/f$idx.png"
  i=$((i+1))
done

# 2) load 24 frames at 3fps (8s of stills) and motion-blend up to 30fps.
#    mi_mode=blend = optical crossfade between frames (safe for faces; no warping).
ffmpeg -y -loglevel error -framerate 3 -i "$tmp/f%03d.png" \
  -vf "minterpolate=fps=30:mi_mode=blend,format=yuv420p" \
  -c:v libx264 -preset slow -crf 22 -movflags +faststart "$OUT/motion/held-fwd.mp4"

# 3) ping-pong so the loop returns to frame 1 seamlessly (moment breathes in and out)
ffmpeg -y -loglevel error -i "$OUT/motion/held-fwd.mp4" \
  -filter_complex "[0]reverse[r];[0][r]concat=n=2:v=1[v]" -map "[v]" \
  -c:v libx264 -preset slow -crf 22 -movflags +faststart "$OUT/motion/held-loop.mp4"

# 4) email-friendly gif
ffmpeg -y -loglevel error -i "$OUT/motion/held-loop.mp4" \
  -vf "fps=12,scale=560:-1:flags=lanczos,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4" \
  -loop 0 "$OUT/motion/held-loop.gif"

rm -rf "$tmp"
echo "made: film-strip/motion/held-loop.mp4 (+ .gif, held-fwd.mp4)"
ls -lh "$OUT/motion/"
