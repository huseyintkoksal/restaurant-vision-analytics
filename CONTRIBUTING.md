# Contributing

Thanks for your interest in improving Restaurant Vision Analytics! Contributions
of all sizes are welcome — code, docs, examples, bug reports, and ideas.

## The one rule that overrides everything

**Keep analytics anonymous and aggregate.** Any contribution that adds facial
recognition, biometric identification, demographic/emotion inference, audio
recording, or persistent per-person tracking is out of scope and will be
declined. When in doubt, open an issue first.

## Good first contributions

- Detector **adapters** that satisfy the `Detector` interface (e.g. a YOLO
  wrapper) — without bundling weights.
- **Dashboard** polish (accessibility, responsiveness, charts).
- **Docs** improvements and examples.
- **Tests** for edge cases in the analytics modules.

## Development setup

```bash
# Backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
ruff check backend

# Frontend
cd frontend && npm install
npm run build      # tsc --noEmit + vite build
```

See [docs/GettingStarted.md](docs/GettingStarted.md) for more.

## Project standards

- **Python:** type hints, docstrings, `ruff` clean (`ruff check backend` and
  `ruff format backend`). Keep the vision core dependency-light; heavy backends
  (OpenCV, etc.) stay optional and import-guarded.
- **TypeScript:** strict mode; `npm run build` must pass.
- **Tests:** add/adjust tests for behavior changes. The privacy tests are a hard
  gate — don't weaken them.

## Pull request process

1. Fork and create a feature branch.
2. Make focused changes with clear commits.
3. Ensure `pytest`, `ruff`, and the frontend build pass.
4. Update docs if behavior or APIs changed.
5. Open a PR using the template; complete the **privacy & scope** checklist.
6. Never commit secrets, credentials, real customer footage, or model weights.

## Reporting bugs & requesting features

Use the issue templates (Bug report, Feature request, Privacy question). Please
never attach real customer imagery or personal data.

## Code of Conduct

By participating you agree to our [Code of Conduct](CODE_OF_CONDUCT.md).

## License

By contributing, you agree your contributions are licensed under the project's
[MIT License](LICENSE).
