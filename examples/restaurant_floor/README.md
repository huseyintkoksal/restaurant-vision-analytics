# Example: Full-Service Restaurant

A sit-down restaurant with a host/waiting area, a kitchen pass, a cashier, and
eight tables of varying sizes.

- **Floor plan:** [`demo/floorplans/restaurant_floor.json`](../../demo/floorplans/restaurant_floor.json)
- **Best for:** table-usage analytics — dwell time, turnover, and idle-table
  detection across many tables.

## Run

```bash
make backend         # :8000
make frontend        # :5173
```

## What to look at

- **Table map** shows per-table dwell time and turnover counts.
- **Avg Table Usage** and **Peak Occupancy** summary cards.
- **Idle** tables (empty beyond the threshold) are highlighted and can raise a
  `table_idle` alert.

The system tracks *tables*, never the guests sitting at them.
