# Example: Small Cafe

A compact counter-service cafe with a short order queue and four tables.

- **Floor plan:** [`demo/floorplans/small_cafe.json`](../../demo/floorplans/small_cafe.json)
- **Best for:** evaluating queue pressure and table turnover at small scale.

## Run

```bash
# 1. Start the stack in demo mode (synthetic, anonymous flow)
make demo            # backend on :8000
make frontend        # dashboard on :5173
```

The default seeded floor plan already approximates this layout. To load the
small-cafe zones explicitly, POST each zone in
`demo/floorplans/small_cafe.json` to `POST /api/zones` (see
[demo/README.md](../../demo/README.md)).

## What to look at

- **Queue Pressure** card rises as the synthetic queue fills.
- **Table map** flips tables between free / occupied / idle.
- **Occupancy over time** chart shows the quiet→busy cycle.

No facial recognition, biometrics, or persistent tracking is involved — only
anonymous counts.
