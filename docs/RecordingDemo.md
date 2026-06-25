# Recording a Demo (Screenshots & GIF)

The repository already ships generated screenshots and a GIF in
[`demo/screenshots/`](../demo/screenshots) and [`demo/gifs/`](../demo/gifs). Use
this guide to refresh them or record your own short demo for the README, a
release, or a launch post.

Everything here uses **demo mode** — synthetic, anonymous data. Never record or
publish real customer footage.

## 1. Start the backend (demo mode)

```bash
# from the repo root
cp .env.example .env
pip install -e ".[dev]"
# A livelier scene reads better on camera:
DEMO_ARRIVAL_RATE=26 LIVE_UPDATE_INTERVAL_SECONDS=0.5 \
  uvicorn app.main:app --app-dir backend --port 8000
```

PowerShell (Windows):

```powershell
$env:DEMO_ARRIVAL_RATE=26; $env:LIVE_UPDATE_INTERVAL_SECONDS=0.5
python -m uvicorn app.main:app --app-dir backend --port 8000
```

## 2. Start the frontend

```bash
cd frontend
npm install
npm run dev      # http://localhost:5173
```

## 3. What demo mode looks like

Within ~30–60 seconds the dashboard fills in:

- **Live Occupancy** climbs as synthetic agents arrive.
- **Queue Pressure** moves through clear → moderate → busy → congested.
- **Table map** flips tables between free / occupied / idle and counts turnovers.
- **Crowd density heatmap** warms up.
- **Alerts** appear when the queue is long or occupancy crosses the threshold.

Let it run a minute before capturing so the charts have history.

## 4. Take screenshots

- Use your OS screenshot tool, or your browser's device toolbar for a clean
  viewport (1440×1024 looks good).
- Capture these three pages:
  - `http://localhost:5173/` → `demo/screenshots/dashboard-live.png`
  - `http://localhost:5173/privacy` → `demo/screenshots/privacy-page.png`
  - `http://localhost:5173/zones` → `demo/screenshots/zone-analytics.png`

### Optional: automate with a system browser + Playwright

If you have Chrome/Edge installed, Playwright can drive it without downloading
its own browser:

```bash
npm install playwright
node -e "const{chromium}=require('playwright');(async()=>{const b=await chromium.launch({channel:'chrome'});const p=await b.newPage({viewport:{width:1440,height:1024},deviceScaleFactor:2});await p.goto('http://localhost:5173');await p.waitForTimeout(6000);await p.screenshot({path:'demo/screenshots/dashboard-live.png'});await b.close();})()"
```

## 5. Record a GIF

**Easiest (screen recorder):** use ScreenToGif (Windows), Peek (Linux), or Kap
(macOS). Record the dashboard region for ~12–15 seconds while data changes, then
export an optimized GIF (target < 1 MB, width ~900px) to
`demo/gifs/live-dashboard-demo.gif`.

**From a frame sequence (Pillow):** capture ~18 screenshots ~0.9s apart, then:

```python
import glob
from PIL import Image
frames = [Image.open(p).convert("P", palette=Image.ADAPTIVE, colors=128)
          for p in sorted(glob.glob("frames/frame_*.png"))]
frames[0].save("demo/gifs/live-dashboard-demo.gif", save_all=True,
               append_images=frames[1:], duration=850, loop=0, optimize=True, disposal=2)
```

## 6. Suggested 30-second demo script

1. Open the **Dashboard**; let occupancy and the queue build (~10s).
2. Point out the **Queue Pressure** changing status and an **alert** appearing.
3. Switch to **Privacy** to show every invasive capability is OFF.
4. Switch to **Zones** to show the floor plan and that zones are *places*.

## 7. Add to the README

The README already references:

```md
![Live dashboard](demo/gifs/live-dashboard-demo.gif)
![Dashboard](demo/screenshots/dashboard-live.png)
```

Replacing the files updates the README automatically. Keep the
[`.gitignore`](../.gitignore) allow-list entries if you rename assets.

## 8. Troubleshooting

- If the backend fails to import `app.main`, run it from the repository root and
  keep `--app-dir backend`.
- If PowerShell blocks `npm`, use `npm.cmd install` and `npm.cmd run dev`.
- If the dashboard is empty, wait 30-60 seconds for demo history to accumulate
  and confirm `ENABLE_DEMO_MODE=true`.
- If the frontend cannot reach the backend, check that
  `VITE_API_BASE_URL=http://localhost:8000` and that `/health` returns `200`.
- If Playwright cannot download Chromium, use an installed Chrome or Edge
  channel, or capture screenshots manually with the system browser.
- If a GIF is too large, reduce the viewport width, frame count, color count, or
  duration before committing it.
