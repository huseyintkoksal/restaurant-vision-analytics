# Security Policy

## Supported versions

This project is in early development (`0.x`). Security fixes are applied to the
latest `main` and the most recent release.

| Version | Supported |
| --- | --- |
| `0.1.x` | ✅ |
| `< 0.1` | ❌ |

## Reporting a vulnerability

**Please do not open a public issue for security vulnerabilities.**

Instead, report privately:

1. Use GitHub's **[Private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability)**
   ("Report a vulnerability" under the repository's **Security** tab), or
2. Email the maintainers at the address listed on the repository profile.

Please include:

- A description of the issue and its impact.
- Steps to reproduce or a proof of concept.
- Affected version/commit and environment.

**Do not include real customer footage or personal data** in your report.

## What to expect

- We aim to acknowledge reports within a few business days.
- We will investigate, keep you updated, and credit you (if you wish) once a fix
  is released.
- Please give us reasonable time to remediate before any public disclosure.

## Scope notes

- **Secrets:** no API keys, tokens, camera credentials, or secrets are committed
  to this repository. If you find one, report it privately. Configuration is
  environment-driven; see [`.env.example`](.env.example).
- **Model weights** are never bundled and are not downloaded silently.
- **Optional dependencies** (e.g. OpenCV adapters) have their own security
  surfaces; review them before enabling. See [LICENSES.md](LICENSES.md).

## Hardening guidance

For deploying safely (TLS, CORS, access control, secrets handling), see
[docs/Deployment.md](docs/Deployment.md).
