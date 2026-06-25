# Ethics and Responsible Use

This project is built for **anonymous restaurant operations analytics**. Please
use it that way. This document is about intent and boundaries; it is not legal
advice.

## Intended use

- Measuring **anonymous** occupancy and crowd density.
- Estimating **queue pressure** to staff tills appropriately.
- Understanding **table usage** (occupied/free, dwell, turnover) to improve
  service and seating.
- Spotting operational conditions (long queues, idle tables, offline cameras).

## Misuse cases (do not do this)

- Trying to recognize, re-identify, or follow specific customers over time.
- Inferring or recording age, gender, ethnicity, emotion, or any personal trait.
- Bolting on facial recognition or biometric matching via a custom detector.
- Repurposing the tool to surveil or score individuals.

The architecture deliberately makes these hard: the analytics layer never
receives anything but anonymous geometry. Adding identification would mean
fighting the design — and our tests.

## Prohibited use

Do not use this software to build or operate systems whose purpose is covert
surveillance, biometric mass identification, social scoring, or any use that
violates applicable law or fundamental rights.

## Employee monitoring warning

This tool is **not** an employee-surveillance product. Using anonymous
operations analytics to individually track, rank, or discipline staff is a
misuse, may be unlawful in your jurisdiction, and harms trust. Aggregate
operational insight (e.g. "the lunch rush needs more till coverage") is the
intended outcome — never per-person performance policing.

## Customer transparency

Tell people. Where cameras run, post clear notices explaining that anonymous
operations analytics are in use and that no one is identified or recorded as an
individual. Transparency is both an ethical baseline and, in many places, a
legal requirement.

## Privacy by default

Keep the defaults: demo/anonymous processing, raw-frame storage off, short
retention, local-first. Changing a default is a decision you should document and
justify.

## Human oversight

Treat metrics as **decision support**, not automated judgment. Alerts and scores
are approximations from a simple pipeline (see [AnalyticsModel.md](AnalyticsModel.md)).
Keep a human in the loop for any operational action.
