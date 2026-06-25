# Licenses

## Core project

Restaurant Vision Analytics is licensed under the **MIT License** — see
[LICENSE](LICENSE). You are free to use, modify, and distribute it, including
commercially, subject to the MIT terms.

## Optional AI model adapters

This project ships a **modular detector interface**. The default
`SyntheticDetector` (demo mode) and the optional `OpenCVHOGDetector` rely only on
software included or installed as standard dependencies/extras.

If you add an **optional adapter** for a third-party model or framework (for
example a YOLO/Ultralytics wrapper), be aware:

- **Third-party licenses apply.** Some model frameworks and pretrained weights
  use licenses that differ from MIT (e.g. AGPL-style or research-only/non-
  commercial terms). Review and comply with them before use, especially for
  commercial deployments.
- **Model weights are not included** in this repository and are **not downloaded
  silently**. You are responsible for obtaining weights and accepting their
  terms.
- **You are responsible** for complying with the licenses of any model, dataset,
  framework, camera SDK, and with applicable privacy laws in your jurisdiction.

## Runtime dependencies

Backend and frontend dependencies are distributed under their own licenses
(predominantly MIT/BSD/Apache-2.0). Review them via:

```bash
pip install pip-licenses && pip-licenses          # Python deps
npm --prefix frontend ls --all                    # JS deps
```

## Your responsibilities (summary)

- Comply with the licenses of any optional model/tool/dataset you add.
- Do not commit model weights, datasets, secrets, or real customer footage.
- Comply with privacy and surveillance laws where you operate (see
  [docs/KVKK_GDPR_Checklist.md](docs/KVKK_GDPR_Checklist.md)). This is not legal
  advice.

## Trademarks

Product and company names referenced in documentation are the property of their
respective owners and are used for identification only.
