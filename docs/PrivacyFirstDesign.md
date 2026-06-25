# Privacy-First Design

Privacy here is not a policy bolted on top — it is a property of the
architecture. This document explains how the design makes invasive behavior
impossible-by-default rather than merely discouraged.

> **This project does not perform facial recognition, biometric identification,
> demographic inference, emotion detection, audio recording, or persistent
> customer tracking.**

## Design goals

1. Derive useful **operations** metrics (occupancy, queue, tables, flow).
2. Make those metrics **aggregate and anonymous**.
3. Keep raw imagery out of storage **by default**.
4. Encode the guarantees in code and tests, not just prose.

## No biometrics

The `Detection` value object has exactly three fields: `bbox`, `confidence`,
`label` (always `"person"`). There is no field — and no code path — for a face,
gait, clothing signature, embedding, age, gender, ethnicity, or emotion. A
regression test (`test_privacy_no_identity_persistence.py`) fails CI if anyone
adds one.

## No identity persistence

The database schema has four tables: `cameras`, `zones`, `analytics_snapshots`,
`alerts`. None stores a person. Snapshots contain only counts and pressures. A
test asserts the table set and scans every column name for forbidden tokens.

## Ephemeral tracking

The tracker exists only to connect detections across a few frames so dwell time
and flow can be estimated. Track ids are anonymous integers with a short TTL.
There is **no re-identification**: leave and return, and you are a brand-new id.
Tracks are never written to the database.

## Aggregated analytics

Every exported metric is an aggregate: a total, a per-zone count, a pressure
score, a turnover count, a density grid. None can single out an individual.

## Raw frame policy

`ENABLE_RAW_FRAME_STORAGE` defaults to `false`. The codebase routes any raw
write through a single gate (`anonymizer.may_store_raw_frame`). Enabling it is a
deliberate, audited operator decision — and even then, it turns on **no**
identification feature, because none exist.

## Data retention policy

Aggregate snapshots and alerts are pruned after `DATA_RETENTION_DAYS` (default
7) by the retention service. See [DataRetention.md](DataRetention.md).

## Local-first deployment

The default database is local SQLite and the default detector needs no network.
You can run the entire stack on a single on-prem machine with no data leaving
the premises.

## Debug-frame anonymization

If you enable debug imagery, `app/vision/anonymizer.py` blurs or masks every
detected person region before the frame leaves memory. The privacy-preserving
path is the default path.

## Signage recommendation

Where cameras operate, display clear, visible notices that the area is monitored
for **anonymous occupancy/operations analytics** and that no identification or
recording of individuals takes place. See
[KVKK_GDPR_Checklist.md](KVKK_GDPR_Checklist.md).

## Operator responsibility

This toolkit gives you privacy-preserving defaults, but the operator is
responsible for lawful, transparent deployment: signage, purpose limitation,
access control, retention, and compliance with local law. See
[EthicsAndResponsibleUse.md](EthicsAndResponsibleUse.md).
