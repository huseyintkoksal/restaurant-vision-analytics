# KVKK / GDPR Compliance Checklist

> **This is not legal advice.** It is a practical checklist to help you deploy
> responsibly. Laws differ by jurisdiction and change over time. Consult a
> qualified professional (and your DPO, where applicable) for your situation.
> KVKK = Turkey's *Kişisel Verilerin Korunması Kanunu*; GDPR = EU General Data
> Protection Regulation.

## Why this is lighter than typical CCTV

This toolkit is designed to **minimize** personal-data processing: it produces
anonymous, aggregate metrics and does not perform facial recognition,
biometric identification, demographic inference, emotion detection, audio
recording, or persistent customer tracking, and it does not store raw frames by
default. That dramatically reduces — but does not automatically eliminate —
your obligations, because a camera operating in a space can still involve
processing under local law.

## Checklist

### 1. Camera notice / transparency
- [ ] Visible signage at entrances and monitored areas.
- [ ] Notice states the purpose: **anonymous operations analytics**, no
      identification or individual recording.
- [ ] A contact point and, where required, a privacy notice/policy reference.

### 2. Purpose limitation
- [ ] Document the specific, legitimate purpose (occupancy/queue/table
      analytics for operations).
- [ ] Do **not** repurpose the system for identification, profiling, or staff
      surveillance.

### 3. Data minimization
- [ ] Keep `ENABLE_RAW_FRAME_STORAGE=false`.
- [ ] Export only aggregate metrics.
- [ ] Draw zones to capture operational areas, not faces.

### 4. Retention
- [ ] Set `DATA_RETENTION_DAYS` to the shortest window that meets your needs.
- [ ] Verify pruning runs (see [DataRetention.md](DataRetention.md)).

### 5. Access controls
- [ ] Restrict who can view the dashboard and query the API.
- [ ] Network-isolate the backend; add authentication (RBAC is on the roadmap).
- [ ] Provide secrets via environment/secret manager, never in git.

### 6. Local processing
- [ ] Prefer on-prem, local-first deployment so data does not leave the venue.
- [ ] If using a database server, keep it within your trust boundary.

### 7. Security
- [ ] TLS for the API and dashboard.
- [ ] Keep dependencies updated; see [SECURITY.md](../SECURITY.md).
- [ ] Back up only aggregate data.

### 8. Vendor / component review
- [ ] If you add an optional detector (e.g. a YOLO adapter), review its license,
      model card, and data-handling. See [LICENSES.md](../LICENSES.md).
- [ ] Ensure no added component introduces identification or off-site data flow.

### 9. Incident response
- [ ] Have a plan for suspected data incidents.
- [ ] Know your breach-notification obligations under KVKK/GDPR.
- [ ] Keep an audit trail of configuration changes (especially raw-frame toggles).

### 10. Records & lawful basis
- [ ] Where required, document your lawful basis and processing records.
- [ ] Run a DPIA/assessment if your jurisdiction or scale calls for one.

---

Keeping the project's privacy defaults is the easiest path to a defensible
deployment — but compliance is ultimately the operator's responsibility.
