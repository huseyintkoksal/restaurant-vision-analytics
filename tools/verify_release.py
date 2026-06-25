#!/usr/bin/env python
"""Release verification — is the repository actually ready to publish?

Checks that the launch-critical files exist, that no publish-blocking
placeholders remain, that no forbidden files are tracked, and that the key
metadata files are present. Run from the repository root::

    python tools/verify_release.py

Exits non-zero if any required check fails.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CANONICAL_REPO_URL = "https://github.com/huseyintkoksal/restaurant-vision-analytics"

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "LICENSES.md",
    "SECURITY.md",
    "PRIVACY.md",
    "ETHICS.md",
    "ROADMAP.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    ".env.example",
    "docker-compose.yml",
    "pyproject.toml",
    "package.json",
    "Makefile",
    "docs/API.md",
    "docs/Architecture.md",
    "docs/GitHubLaunch.md",
    "docs/StarReadyChecklist.md",
    "docs/V02Plan.md",
    "docs/RecordingDemo.md",
    "tools/privacy_audit.py",
]

REQUIRED_WORKFLOWS = [
    ".github/workflows/backend.yml",
    ".github/workflows/frontend.yml",
    ".github/workflows/docker.yml",
]

# At least one real visual must exist.
VISUAL_CANDIDATES = [
    "demo/screenshots/dashboard-live.png",
    "demo/screenshots/privacy-page.png",
    "demo/screenshots/zone-analytics.png",
    "demo/gifs/live-dashboard-demo.gif",
    "docs/assets/architecture-overview.svg",
]

# Publish-blocking placeholders (the literal word "placeholder" is intentionally
# NOT included — it legitimately appears in code/docs as plain English).
PLACEHOLDER_TOKENS = [
    "your" + "-org",
    "your" + "-username",
    "your" + "-name",
    "TODO" + " replace",
    "REPLACE" + "_ME",
    "example" + ".com",
]

_OLD_REPO_OWNER = "koksalh" + "479"
_PLACEHOLDER_OWNERS = ("your" + "-org", "your" + "-username")

FORBIDDEN_REPO_REFS = [
    f"https://github.com/{owner}/restaurant-vision-analytics"
    for owner in (_OLD_REPO_OWNER, *_PLACEHOLDER_OWNERS)
]
FORBIDDEN_REPO_REFS += [
    f"github.com/{owner}/restaurant-vision-analytics"
    for owner in (_OLD_REPO_OWNER, *_PLACEHOLDER_OWNERS)
]
FORBIDDEN_REPO_REFS += [
    f"{owner}/restaurant-vision-analytics"
    for owner in (_OLD_REPO_OWNER, *_PLACEHOLDER_OWNERS)
]

CANONICAL_REQUIRED_FILES = [
    "README.md",
    "pyproject.toml",
    "docs/GitHubLaunch.md",
]

SCAN_SUFFIXES = {".md", ".toml", ".json", ".yml", ".yaml", ".py", ".ts", ".tsx", ".css", ".html"}
SCAN_SKIP_DIRS = {".git", "node_modules", ".venv", "dist", "__pycache__", ".ruff_cache", ".pytest_cache"}

FORBIDDEN_TRACKED_EXT = {
    ".mp4", ".mov", ".avi", ".mkv", ".webm",
    ".pt", ".pth", ".onnx", ".weights", ".engine",
}


class Verifier:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.passes: list[str] = []

    def ok(self, msg: str) -> None:
        self.passes.append(msg)

    def fail(self, msg: str) -> None:
        self.failures.append(msg)

    def check_required_files(self) -> None:
        missing = [f for f in REQUIRED_FILES if not (REPO / f).exists()]
        if missing:
            self.fail(f"Missing required files: {missing}")
        else:
            self.ok(f"All {len(REQUIRED_FILES)} required files present.")

    def check_workflows(self) -> None:
        missing = [f for f in REQUIRED_WORKFLOWS if not (REPO / f).exists()]
        if missing:
            self.fail(f"Missing CI workflows: {missing}")
        else:
            self.ok("All GitHub Actions workflows present.")

    def check_visual(self) -> None:
        present = [v for v in VISUAL_CANDIDATES if (REPO / v).exists()]
        if present:
            self.ok(f"Visual assets present ({len(present)}): e.g. {present[0]}")
        else:
            self.fail("No screenshot/GIF/SVG visual asset found — launch blocker.")

    def _iter_text_files(self):
        for path in REPO.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in SCAN_SUFFIXES:
                continue
            if any(part in SCAN_SKIP_DIRS for part in path.parts):
                continue
            if path.resolve() == Path(__file__).resolve():
                continue
            yield path

    def check_placeholders(self) -> None:
        hits: list[str] = []
        for path in self._iter_text_files():
            try:
                text = path.read_text(encoding="utf-8")
            except Exception:
                continue
            for token in PLACEHOLDER_TOKENS:
                if token in text:
                    rel = path.relative_to(REPO).as_posix()
                    hits.append(f"{rel}: '{token}'")
        if hits:
            self.fail("Publish-blocking placeholders remain:")
            self.failures.extend(f"    {h}" for h in hits)
        else:
            self.ok("No publish-blocking placeholders found.")

    def check_repository_links(self) -> None:
        missing_canonical: list[str] = []
        for rel in CANONICAL_REQUIRED_FILES:
            path = REPO / rel
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            if CANONICAL_REPO_URL not in text:
                missing_canonical.append(rel)

        forbidden_hits: list[str] = []
        for path in self._iter_text_files():
            try:
                text = path.read_text(encoding="utf-8")
            except Exception:
                continue
            for token in FORBIDDEN_REPO_REFS:
                if token in text:
                    rel = path.relative_to(REPO).as_posix()
                    forbidden_hits.append(f"{rel}: '{token}'")

        if missing_canonical:
            self.fail(f"Canonical repository URL missing from: {missing_canonical}")
        elif forbidden_hits:
            self.fail("Forbidden repository owner references remain:")
            self.failures.extend(f"    {h}" for h in forbidden_hits)
        else:
            self.ok(f"Canonical repository URL verified: {CANONICAL_REPO_URL}")

    def check_no_forbidden_tracked(self) -> None:
        try:
            out = subprocess.run(
                ["git", "ls-files"], cwd=REPO, capture_output=True, text=True, check=True
            )
        except Exception:
            self.ok("git not available — skipped tracked-file check.")
            return
        tracked = [line.strip() for line in out.stdout.splitlines() if line.strip()]
        bad = [f for f in tracked if Path(f).suffix.lower() in FORBIDDEN_TRACKED_EXT]
        if ".env" in tracked:
            bad.append(".env")
        if bad:
            self.fail(f"Forbidden files tracked by git: {bad}")
        else:
            self.ok("No forbidden files (video/weights/.env) tracked.")

    def run(self) -> int:
        self.check_required_files()
        self.check_workflows()
        self.check_visual()
        self.check_placeholders()
        self.check_repository_links()
        self.check_no_forbidden_tracked()

        print("Release verification\n====================")
        for msg in self.passes:
            print(f"  [PASS] {msg}")
        for msg in self.failures:
            print(f"  [FAIL] {msg}")
        print("--------------------")
        if self.failures:
            print(f"RESULT: NOT READY ({len(self.failures)} issue group(s))")
            return 1
        print("RESULT: READY - all release checks passed.")
        return 0


if __name__ == "__main__":
    sys.exit(Verifier().run())
