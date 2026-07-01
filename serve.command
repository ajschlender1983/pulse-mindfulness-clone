#!/bin/bash
# Double-click to run the site locally. It must be served over http:// (not opened
# as a file://) because it loads Webflow's module scripts, which browsers block on file://.
cd "$(dirname "$0")"
PORT=8842
echo "Serving Pulse Mindfulness clone at http://localhost:$PORT"
echo "Press Control-C in this window to stop."
( sleep 1 && open "http://localhost:$PORT/index.html" ) &
python3 -m http.server $PORT
