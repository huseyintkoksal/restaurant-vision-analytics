# Example: Fast Food Counter

High-throughput counter service: a long order queue, two tills, a pickup area,
and booth seating.

- **Floor plan:** [`demo/floorplans/fast_food.json`](../../demo/floorplans/fast_food.json)
- **Best for:** stress-testing queue pressure alerts and pickup-area flow.

## Run

```bash
docker compose up --build      # backend :8000, frontend :5173
```

## What to look at

- **Queue Pressure** frequently reaches "busy"/"congested" — watch the
  **Alerts** panel for a `queue_too_long` alert (edge-triggered, de-duplicated).
- **Pickup Area** and **Cashier** zones show how non-table zones contribute to
  occupancy without double-counting.

All metrics are aggregate and anonymous.
