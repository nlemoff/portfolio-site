# nlemoff.com

My personal site: one 8-bit cross-section of my place in Oakland, from the sky down to a basement with three playable games.

Built with [Astro](https://astro.build) as a static site and deployed to GitHub Pages (`.github/workflows/deploy.yml`) on every push to `main`.

## Run it

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # static output in out/
```

## How it's put together

- `art/`: the pixel-art pipeline (Python 3 with `numpy` and `Pillow`). Every scene, sprite and the page layout are drawn in code from one palette.
  - `build.py` renders all images into `public/house/` and writes `art/layout.json`.
  - `page.py` turns the layout into `src/generated/house.html`, `src/styles/house.css` and `src/scripts/house.js`.
  - `npm run art` runs both. Edit the Python, not the generated files.
- `src/pages/index.astro`: the page shell (meta tags, font) around the generated house.
- `public/games/`: the three games (Time Trial, Aim Trainer, Ringfall), each a self-contained page loaded into the basement CRT. three.js 0.170.0 is vendored in `public/games/vendor/` (MIT).

Add `?date=YYYY-MM-DD&time=HH:MM` to the URL to preview seasons and time of day.
