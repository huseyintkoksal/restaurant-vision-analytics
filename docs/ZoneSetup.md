# Zone Setup

Zones are the core configuration concept. A **zone** is a named polygon over a
camera's field of view. Zones describe **places** — never people.

## Coordinate system

Polygons use **normalized coordinates** in `[0, 1]`:

- `x = 0.0` is the left edge, `x = 1.0` the right edge.
- `y = 0.0` is the top edge, `y = 1.0` the bottom edge.

Normalized coordinates make a zone layout resolution-independent.

## Zone types

| Type | Meaning |
| --- | --- |
| `entrance` | Where people enter/exit. |
| `dining_area` | General seating area. |
| `table` | A single table (often nested inside a dining area). |
| `queue` | An ordering/waiting line. |
| `cashier` | A till / point of sale. |
| `kitchen_pass` | Where finished orders are handed off. |
| `pickup_area` | Order collection area. |

## Creating a zone

```bash
curl -X POST http://localhost:8000/api/zones \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Order Queue",
        "type": "queue",
        "capacity": 6,
        "polygon": [[0.18,0.5],[0.42,0.5],[0.42,0.74],[0.18,0.74]]
      }'
```

- `capacity` (optional) is a soft comfort threshold used for queue pressure and
  occupancy utilization.
- `attributes` (optional) holds non-personal config like `{"seats": 4}`.

## Overlapping zones

A `table` is commonly nested inside a `dining_area`. The occupancy engine counts
each anonymous point **once** toward the total even if it falls in multiple
zones, while still reporting per-zone counts. So a seated guest counts toward
both `dining_area` and `table-1` per-zone, but only once in the overall total.

## Tips for good zones

- Draw the **queue** zone along the actual line, sized to its comfortable
  capacity.
- Make **table** zones snug around each table's seating footprint.
- Keep the **entrance** zone near the door so arrivals/departures register.

## Example floor plans

Three ready-made layouts live in
[`demo/floorplans/`](../demo/floorplans/): `small_cafe.json`, `fast_food.json`,
and `restaurant_floor.json`. The Zones page in the dashboard renders the active
layout as an SVG floor plan.

> A visual drag-and-drop zone editor is planned for v0.2.
