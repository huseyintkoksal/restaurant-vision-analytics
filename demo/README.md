# Demo Assets

Everything here exists to let you evaluate the toolkit **without a camera** and
**without any real customer footage**. All demo data is synthetic and anonymous.

## Contents

| Path | What it is |
| --- | --- |
| `synthetic/generate_synthetic_flow.py` | Drives the synthetic detector and writes an aggregate event timeline. |
| `synthetic/sample_events.json` | A pre-generated, anonymous flow timeline (occupancy / queue / tables). |
| `floorplans/` | Three example zone layouts: small cafe, fast food, full-service restaurant. |
| `screenshots/` | Drop dashboard screenshots here for the README. |
| `gifs/` | Drop short demo GIFs here. |

## Regenerate the sample timeline

```bash
python demo/synthetic/generate_synthetic_flow.py --frames 120 --out demo/synthetic/sample_events.json
```

The output contains only aggregate numbers — there is no imagery, no identity,
and no personal attribute anywhere in this folder, by design.

## Floor plans

Each floor plan is a list of zones (named polygons in normalized 0–1
coordinates). You can post them to the running backend:

```bash
# Example: load one zone from a floor plan
curl -X POST http://localhost:8000/api/zones \
  -H "Content-Type: application/json" \
  -d '{"name":"Order Queue","type":"queue","capacity":6,"polygon":[[0.18,0.5],[0.42,0.5],[0.42,0.74],[0.18,0.74]]}'
```

> ⚠️ Do **not** add real customer videos or images to this folder. The project
> intentionally ships only synthetic data.
