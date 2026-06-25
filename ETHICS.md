# Ethics

Restaurant Vision Analytics exists to make **anonymous operations analytics**
useful without sliding into surveillance. This document states the project's
ethical position; deeper guidance is in
[docs/EthicsAndResponsibleUse.md](docs/EthicsAndResponsibleUse.md).

## Our position

- Analytics can be genuinely useful **and** respect people. We choose both.
- Identification is **not required** for occupancy, queue, and table insight —
  so we make it impossible by design.
- Honesty about limitations earns more trust than inflated claims.

## Intended use

Anonymous, aggregate operations analytics for restaurants: occupancy, queue
pressure, table usage, and crowd-flow heatmaps to inform staffing and seating.

## Prohibited / out-of-scope use

- Facial recognition, biometric identification, or re-identification.
- Inferring or recording age, gender, ethnicity, emotion, or other traits.
- Persistent tracking or profiling of individual customers.
- **Employee surveillance** or per-person performance policing.
- Covert monitoring, social scoring, or any unlawful or rights-violating use.

Feature requests in these directions will be declined; the architecture is built
to resist them.

## Operator responsibilities

- **Transparency:** visible signage where cameras operate.
- **Purpose limitation:** use only for the stated operational purpose.
- **Data minimization:** keep raw-frame storage off; export only aggregates.
- **Human oversight:** treat metrics as decision support, not automated judgment.
- **Legal compliance:** follow KVKK/GDPR and local law (see the checklist).

## A note to contributors

When in doubt, choose the option that keeps individuals anonymous and keeps the
operator honest. If a feature can only work by identifying people, it does not
belong here.
