# XOFlipper — Landing (xoflip.com)

A tiny static site for the XOFlipper drop. Designed for Cloudflare Pages or any static host.

## Structure
```
/index.html          # Splash + traits + video embed + CTA
/styles.css          # Minimal styles
/public/             # Assets (banner, glyphs, favicon, video placeholder)
```

## Local preview
Use any static server, e.g.
```bash
python3 -m http.server 5173
# open http://localhost:5173
```

## Deploy — Cloudflare Pages
1. Create repo `xo-flip` under `xo-ecosystem`.
2. Push these files.
3. In Cloudflare Pages: **Create a project** → **Connect to Git** → select repo.
4. **Build settings**: Framework = *None (static)*, Build command = *(empty)*, Output dir = `/`.
5. Link your domain: **xoflip.com** → set CNAME to the Pages project.

## Swap in the real Pump.fun link
Edit `index.html` and update:
```js
// mint.href = 'https://pump.fun/coin/XXXX';
```

## Video
Replace `/public/xoflipper_teaser.mp4` with the final ≤30 MB MP4 when ready.
