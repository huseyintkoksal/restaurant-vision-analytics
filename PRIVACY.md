# Privacy

Privacy is the headline feature of this project, enforced in the architecture
and in tests — not just promised in prose.

> **This project does not perform facial recognition, biometric identification,
> demographic inference, emotion detection, audio recording, or persistent
> customer tracking.**

## Core principles

1. **Anonymous by design.** The only thing the analytics layer ever receives is
   an anonymous person-shaped box (`bbox`, `confidence`, `label="person"`).
   There is no field — and no code path — for identity, face, biometrics, age,
   gender, ethnicity, or emotion.

2. **Ephemeral tracking only.** Track ids are short-lived anonymous integers
   with a TTL. There is **no re-identification**: leave and return, and you are
   a brand-new id. Tracks are never written to the database.

3. **Aggregate metrics only.** Everything exported is a count, a pressure score,
   a turnover number, or a coarse density grid. None can single out a person.

4. **No raw frame persistence by default.** `ENABLE_RAW_FRAME_STORAGE=false`.
   Every raw write is gated through a single function. Enabling it is an
   explicit, audited operator decision and turns on **no** identification.

5. **Debug frames are anonymized.** If debug imagery is enabled, person regions
   are blurred or masked before the frame leaves memory.

6. **Configurable retention.** Aggregate snapshots and alerts are pruned after
   `DATA_RETENTION_DAYS` (default 7).

7. **Local-first.** Default storage is local SQLite; the default detector needs
   no network. The whole stack can run on-prem with no data leaving the venue.

8. **Operator transparency.** Where cameras run, post visible signage explaining
   anonymous operations analytics and that no individual is identified or
   recorded.

## How the guarantees are enforced

- `backend/tests/test_privacy_no_identity_persistence.py` fails CI if a
  forbidden field/column (face, identity, biometric, embedding, age, gender,
  ethnicity, emotion, …) appears in the detection model or database schema.
- The database has exactly four tables — `cameras`, `zones`,
  `analytics_snapshots`, `alerts` — none of which represents a person.
- The tracker has no persistence and no re-identification logic.

## Data we store

| Category | Example | Personal? |
| --- | --- | --- |
| Camera config | name, location, status | No |
| Zone config | polygon, type, capacity | No |
| Aggregate analytics | occupancy total, queue pressure | No |
| Alerts | "queue pressure high" | No |
| Raw frames/video | — | **Not stored by default** |

## Compliance

See [docs/KVKK_GDPR_Checklist.md](docs/KVKK_GDPR_Checklist.md) for a practical
(non-legal-advice) checklist covering signage, purpose limitation, data
minimization, retention, access controls, local processing, and incident
response.

## Reporting a privacy concern

Open a **Privacy question** issue for general questions. For suspected security
or data-handling vulnerabilities, follow [SECURITY.md](SECURITY.md) instead of
filing a public issue.
