# Data Retention

## What is stored

Only **aggregate, anonymous** data:

- **Configuration:** cameras (no credentials), zones (polygons).
- **Aggregate analytics:** `analytics_snapshots` rows — totals, per-zone counts,
  queue pressure, a small aggregate payload.
- **Alerts:** operational alert records.

What is **not** stored: raw frames/video (off by default), faces, identities,
biometrics, demographics, emotions, audio, or per-person tracks.

## Retention window

`DATA_RETENTION_DAYS` (default **7**) controls how long aggregate snapshots and
alerts are kept. The `RetentionService` prunes anything older than the cutoff.

```
cutoff = now - DATA_RETENTION_DAYS days
delete snapshots, alerts where timestamp < cutoff
```

- Set `DATA_RETENTION_DAYS=0` (or negative) to **disable pruning** (keep
  everything). Use deliberately.
- Pruning runs periodically inside the analytics loop and can also be invoked
  programmatically via `RetentionService.prune(session)`.

## Raw frames

`ENABLE_RAW_FRAME_STORAGE=false` by default. The codebase gates every raw-frame
write through `anonymizer.may_store_raw_frame()`. If you ever enable it:

- It is an explicit, audited decision.
- Debug frames are blurred/masked before leaving memory.
- It enables **no** identification feature.

## Choosing a window

- Keep it as short as your operations need.
- Align it with your privacy policy and local law (see
  [KVKK_GDPR_Checklist.md](KVKK_GDPR_Checklist.md)).
- Longer windows are for trend analysis of **aggregate** numbers only.

## Deleting everything

- SQLite: stop the app and delete the database file (default `./data/rva.db`),
  or `docker compose down -v` to drop the volume.
- Postgres: truncate the `analytics_snapshots` and `alerts` tables.
