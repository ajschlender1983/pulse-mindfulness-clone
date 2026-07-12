#!/bin/bash
# Pulse — Motion rules: 3 "feet" x 5 clips. Cinematic rules per foot.
#   illustration = composed painterly camera, on rails, NO handheld shake (it's a memory, a painting that breathes)
#   transition   = the reel slowing: illustration resolving into photograph (travel the axis / come into focus / dissolve)
#   photograph   = handheld cell-phone camera motion (organic micro-drift + tilt + breathing) — the present moment, alive
set -e
cd "$(dirname "$0")/.."
ROOT="$(pwd)"
OUT="$ROOT/library/motion-rules"
mkdir -p "$OUT/illustration" "$OUT/transition" "$OUT/photograph"
FF="ffmpeg -y -hide_banner -loglevel error"
DUR=5; FPS=30
ENC="-c:v libx264 -pix_fmt yuv420p -preset medium -crf 20 -movflags +faststart -an"

ILL="$ROOT/library/illustrations"
SPEC="$ROOT/library/avatar-spectrum"
PEAK="$ROOT/library/peak"

# ---------- ILLUSTRATION FOOT (composed, smooth, no shake) ----------
# push-in
$FF -loop 1 -i "$ILL/illus-coll-embrace.png" -t $DUR -r $FPS -filter_complex \
"scale=2880:-1,zoompan=z='min(1.0+0.00092*on,1.14)':d=$((DUR*FPS)):x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=$FPS,format=yuv420p" $ENC "$OUT/illustration/ill-push-in.mp4"
# pull-out
$FF -loop 1 -i "$ILL/illus-coll-field-light.png" -t $DUR -r $FPS -filter_complex \
"scale=2880:-1,zoompan=z='max(1.14-0.00092*on,1.0)':d=$((DUR*FPS)):x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=$FPS,format=yuv420p" $ENC "$OUT/illustration/ill-pull-out.mp4"
# drift left->right
$FF -loop 1 -i "$ILL/illus-coll-festival.png" -t $DUR -r $FPS -filter_complex \
"scale=2880:-1,zoompan=z='1.12':d=$((DUR*FPS)):x='(iw-iw/zoom)*(on/($DUR*$FPS-1))':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=$FPS,format=yuv420p" $ENC "$OUT/illustration/ill-drift-lr.mp4"
# drift right->left
$FF -loop 1 -i "$ILL/illus-coll-dawn-crowd.png" -t $DUR -r $FPS -filter_complex \
"scale=2880:-1,zoompan=z='1.12':d=$((DUR*FPS)):x='(iw-iw/zoom)*(1-on/($DUR*$FPS-1))':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=$FPS,format=yuv420p" $ENC "$OUT/illustration/ill-drift-rl.mp4"
# breathing pulse
$FF -loop 1 -i "$ILL/illus-coll-table.png" -t $DUR -r $FPS -filter_complex \
"scale=2880:-1,zoompan=z='1.07+0.045*sin(on/23)':d=$((DUR*FPS)):x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=$FPS,format=yuv420p" $ENC "$OUT/illustration/ill-breathe.mp4"
echo "illustration foot: 5 clips"

# ---------- TRANSITION FOOT (illustration -> photograph) ----------
# travel the axis: pan left(illustration)->right(photograph) across a spectrum frame
$FF -loop 1 -i "$SPEC/avatar-01-spectrum.png" -t $DUR -r $FPS -filter_complex \
"scale=2880:-1,zoompan=z='1.10':d=$((DUR*FPS)):x='(iw-iw/zoom)*(on/($DUR*$FPS-1))':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=$FPS,format=yuv420p" $ENC "$OUT/transition/tr-travel.mp4"
# push in on the seam (the hinge)
$FF -loop 1 -i "$SPEC/avatar-05-spectrum.png" -t $DUR -r $FPS -filter_complex \
"scale=2880:-1,zoompan=z='min(1.0+0.0010*on,1.16)':d=$((DUR*FPS)):x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=$FPS,format=yuv420p" $ENC "$OUT/transition/tr-seam-push.mp4"
# come into focus: blurred -> sharp (the reel resolving into presence)
$FF -loop 1 -i "$PEAK/peak-summit-sunrise.png" -t $DUR -r $FPS -filter_complex \
"[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,split[a][b];[a]gblur=sigma=22[bl];[bl][b]xfade=transition=fade:duration=3.6:offset=0.6,format=yuv420p" $ENC "$OUT/transition/tr-focus.mp4"
# dissolve: illustration -> photograph (crossfade)
$FF -loop 1 -t $DUR -i "$ILL/illus-coll-turn.png" -loop 1 -t $DUR -i "$PEAK/peak-superbloom.png" -r $FPS -filter_complex \
"[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1[a];[1:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1[b];[a][b]xfade=transition=dissolve:duration=2.4:offset=1.3,format=yuv420p" $ENC "$OUT/transition/tr-dissolve.mp4"
# smooth wipe: illustration -> photograph (reel slowing)
$FF -loop 1 -t $DUR -i "$ILL/illus-coll-circle.png" -loop 1 -t $DUR -i "$PEAK/peak-alpine-swim.png" -r $FPS -filter_complex \
"[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1[a];[1:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1[b];[a][b]xfade=transition=smoothright:duration=2.6:offset=1.3,format=yuv420p" $ENC "$OUT/transition/tr-wipe.mp4"
echo "transition foot: 5 clips"

# ---------- PHOTOGRAPH FOOT (handheld cell-phone) ----------
handheld () { # $1=infile $2=outfile  seeds vary the drift phase
  local IN="$1" O="$2"
  $FF -loop 1 -i "$IN" -t $DUR -r $FPS -filter_complex \
"scale=2200:1238:force_original_aspect_ratio=increase,crop=2200:1238,\
rotate='0.011*sin(2*PI*t/4.7)':fillcolor=black,\
crop=1920:1080:x='(iw-1920)/2 + 46*sin(2*PI*t/3.3) + 24*sin(2*PI*t/1.9+1.1)':y='(ih-1080)/2 + 30*sin(2*PI*t/2.5) + 15*sin(2*PI*t/1.05+2.0)',\
zoompan=z='1.03+0.02*sin(on/48)':d=$((DUR*FPS)):x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=$FPS,format=yuv420p" $ENC "$O"
}
handheld "$PEAK/peak-aurora.png"        "$OUT/photograph/ph-handheld-01.mp4"
handheld "$PEAK/peak-canyon-rim.png"    "$OUT/photograph/ph-handheld-02.mp4"
handheld "$PEAK/peak-cliff-ocean.png"   "$OUT/photograph/ph-handheld-03.mp4"
handheld "$PEAK/peak-rooftop-dusk.png"  "$OUT/photograph/ph-handheld-04.mp4"
handheld "$PEAK/peak-forest-fog.png"    "$OUT/photograph/ph-handheld-05.mp4"
echo "photograph foot: 5 clips"

echo "--- done. clips under library/motion-rules/ ---"
find "$OUT" -name '*.mp4' | sort
