# Analytics Model

This page documents exactly how each metric is computed — and, just as
importantly, its **limitations**. We aim to be honest about accuracy: this is an
early, transparent, rule-based pipeline, not a black box.

## Inputs

For each frame the detector returns anonymous `Detection` boxes. We take each
box's **foot point** (bottom-center) as the person's floor position, and the
**centroid** for heatmaps. Everything below operates on these anonymous points.

## Occupancy

- **Per-zone count:** number of foot points inside each zone polygon.
- **Total:** number of distinct points inside *any* zone (each counted once, so
  nested table/dining overlaps don't double-count).
- **Peak / average:** running max and mean of total across the session.

## Zone model

A zone is a polygon; membership uses ray-casting point-in-polygon with
on-boundary treated as inside. See `app/utils/geometry.py`.

## Queue pressure model

```
pressure = min(count_in_queue_zones / comfortable_capacity, 1.0)
```

`comfortable_capacity` is the queue zone's `capacity` (default 6). Status bands:

| pressure | status | wait pressure |
| --- | --- | --- |
| `< 0.25` | clear | low |
| `< 0.55` | moderate | medium |
| `< 0.80` | busy | high |
| `≥ 0.80` | congested | very_high |

This is a **pressure proxy**, not a measured wait time in minutes.

## Table occupancy model

For each `table` zone:

- **occupied:** at least one foot point inside the table polygon.
- **duration_seconds:** time in the current state (dwell while occupied,
  vacancy while free).
- **turnover_count:** number of occupied→free transitions (completed seatings).
- **idle:** free continuously beyond `idle_threshold_seconds` (unused capacity).

## Heatmap grid

A coarse `rows × cols` grid over the normalized frame accumulates how often any
point fell in each cell, with mild temporal decay so recent activity dominates.
Output is normalized to `[0, 1]`. It encodes **where crowds form**, never who.

## Alert thresholds

| Alert | Condition (edge-triggered) |
| --- | --- |
| `queue_too_long` | queue pressure ≥ 0.8 |
| `occupancy_threshold` | total occupancy ≥ configured threshold |
| `table_idle` | a table is free beyond the idle threshold |
| `camera_offline` | camera stops reporting |

Alerts fire once on a rising edge and clear on the falling edge, so the feed
stays signal, not spam.

## Limitations

- **Counting accuracy** depends entirely on the detector. The default
  `SyntheticDetector` is a simulation; the optional `OpenCVHOGDetector` is a
  classic, modest-accuracy descriptor. Real-world precision varies with camera
  angle, lighting, occlusion, and crowd density.
- **No identity** means we cannot measure a specific person's true wait time or
  distinguish a returning customer from a new one — by design.
- **Foot-point heuristic** can misplace heavily occluded people.
- **Zone overlaps** are resolved by simple rules; complex layouts may need
  careful zone drawing.

## Accuracy notes

Treat all numbers as **operational estimates** for decision support, not exact
measurements. Calibrate thresholds to your venue, validate against manual counts
during setup, and keep a human in the loop. See
[EthicsAndResponsibleUse.md](EthicsAndResponsibleUse.md).
