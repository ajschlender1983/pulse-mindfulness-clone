# Pulse Mindfulness — editable local recreation

A pixel-for-pixel, word-for-word local copy of https://www.pulsemindfulness.com/,
rebuilt so you can open it, run it, and edit it. All assets (CSS, JS, images,
videos) are downloaded locally. Tracking/analytics (Cookiebot, Klaviyo, Google
Tag Manager) have been stripped out.

## Run it

Double-click **`serve.command`**. It starts a tiny local web server and opens the
site in your browser at `http://localhost:8842`.

> It has to be served over `http://` — not opened directly as a file. The site
> uses Webflow's module scripts, and browsers block those on `file://`. That's
> why there's a server script instead of just double-clicking `index.html`.

Prefer the terminal? From this folder:

```bash
python3 -m http.server 8842
# then open http://localhost:8842
```

## What's here

```
index.html            The full page (the real Webflow markup, all copy)
assets/css/           webflow.css (all styles) + splide-core.min.css
assets/js/            jQuery, Webflow, GSAP + ScrollTrigger, Lenis, Splide, SplitType
assets/img/           every image (avif / webp / svg / png)
assets/video/         every video (hero, benefit clips, the 3D ring render, etc.)
simple/               A cleaner, hand-built version (see below)
```

Everything works: the smooth scrolling, the drag testimonial slider, the app-mode
switcher, the scroll-linked gold-ring "explode" animation, and the numbered
reveals — because this keeps the site's real code, just pointed at local files.

## Two versions, pick your editing style

**1. `index.html` (this folder) — the exact mirror.**
Identical to the live site. Best when you want to change *content* (text, images,
videos, links). Downsides for editing: it's Webflow-generated, so class names are
terse (`.padding-global`, `.max-width-large`) and the styles live in one big
minified `assets/css/webflow.css`.

- **Change text:** edit it directly in `index.html`.
- **Swap an image/video:** drop your file into `assets/img/` or `assets/video/`
  and update the `src` / `data-src` (and any `srcset`) in `index.html`.
- **Restyle:** add your own `<style>` block at the end of `<head>` to override
  the Webflow CSS — easier than editing the minified file.

**2. `simple/index.html` — the clean rebuild.**
A from-scratch version with readable HTML, a tokenized `styles.css` (all colors,
fonts, and spacing as CSS variables at the top), and a small `script.js`. Best
when you want to *restructure or restyle* freely. It approximates the ring
scroll-scrub with a plain looping video rather than the frame-by-frame Webflow
interaction. Open `simple/index.html` directly — it works on `file://`.

## Design tokens (both versions)

- Fonts: **DM Sans** (headings/body), **DM Mono** (small labels), loaded from Google Fonts
- Cream background `#EBE7D4`, light sections `#F9F6E5`
- Ink text `#1A1C22`, brown headings `#423D32`
- Accent lime pill `#E3F47D` on dark text `#101828`
- Dusty-blue divider `#B3C7D3`, dark ring section near-black
