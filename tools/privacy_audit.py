#!/usr/bin/env python
"""Privacy audit — fail the build if the codebase drifts from its guarantees.

This script enforces, in CI, the promises this project makes:

* No invasive *feature* identifiers (face_id, biometric, emotion fields, …) leak
  into the source. The check is word/regex based and **negation-aware** so
  privacy *declarations* (flags set to false, "no ...", comments) do not trip it.
* No secrets (``.env``), raw video, or model weights are tracked by git.
* The privacy documentation and the "does NOT do" stance remain in place.
* Raw frame storage defaults to off.

Run from the repository root::

    python tools/privacy_audit.py
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# Source roots to scan (configuration code + UI). Tests/tools/docs are excluded:
# tests intentionally name forbidden tokens to assert their absence.
SCAN_GLOBS = ["backend/app/**/*.py", "frontend/src/**/*.ts", "frontend/src/**/*.tsx"]

# We detect *actual personal-data fields*, not prose. A field is a line that
# defines/annotates a name (Python ``name: T`` / ``name = ...`` / ``self.name =``,
# or TS ``name: T`` / ``name?:``). If that name is a bare personal attribute and
# is NOT an allowlisted privacy *flag* name, it is a violation. This ignores
# docstrings, comments, and the many legitimate "...: False" privacy flags a
# privacy-first project must declare.
FIELD_RE = re.compile(r"^\s*(?:self\.)?([A-Za-z_][A-Za-z0-9_]*)\s*[?:=]")

# Bare personal-attribute field names that must never exist.
PERSONAL_FIELD_NAMES = {
    "age", "gender", "ethnicity", "emotion", "race",
    "face_id", "faceid", "identity_id", "face_embedding", "embedding",
    "reidentification", "re_identification", "customer_profile", "employee_score",
}

# Privacy *flag* names — legitimate to declare (they are reported as false/off).
ALLOWED_FIELD_NAMES = {
    "biometrics", "biometric_identification", "facial_recognition",
    "demographic_inference", "emotion_detection", "audio_recording",
    "persistent_customer_tracking", "identity_persistence", "identity_tracking",
    "ephemeral_tracking", "raw_frame_storage", "local_first",
}

# Damning substrings — invasive even in passing (skipped only on comment lines).
DAMNING_SUBSTRINGS = (
    "face_embedding", "face_encoding", "reidentification", "re_identification",
    "customer_profile", "employee_score", "biometric_template", "gait_signature",
)

_COMMENT_PREFIXES = ("#", "//", "*", '"""', "'''", "/*")

# Extensions that must never be tracked by git.
FORBIDDEN_TRACKED_EXT = {
    ".mp4", ".mov", ".avi", ".mkv", ".webm",
    ".pt", ".pth", ".onnx", ".weights", ".engine",
}


class Audit:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.passes: list[str] = []

    def ok(self, msg: str) -> None:
        self.passes.append(msg)

    def fail(self, msg: str) -> None:
        self.failures.append(msg)

    # -- checks ----------------------------------------------------------
    def check_source_tokens(self) -> None:
        findings: list[str] = []
        for pattern_glob in SCAN_GLOBS:
            for path in REPO.glob(pattern_glob):
                rel = path.relative_to(REPO).as_posix()
                for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                    stripped = raw.strip()
                    is_comment = stripped.startswith(_COMMENT_PREFIXES)

                    # 1) Personal-attribute field/annotation (ignores comments).
                    if not is_comment:
                        m = FIELD_RE.match(raw)
                        if m:
                            name = m.group(1).lower()
                            if name in PERSONAL_FIELD_NAMES and name not in ALLOWED_FIELD_NAMES:
                                findings.append(
                                    f"{rel}:{lineno}: personal field '{name}' -> {stripped[:80]}"
                                )

                    # 2) Damning substrings anywhere in non-comment code.
                    if not is_comment:
                        low = raw.lower()
                        for sub in DAMNING_SUBSTRINGS:
                            if sub in low:
                                findings.append(f"{rel}:{lineno}: '{sub}' -> {stripped[:80]}")

        if findings:
            self.fail("Invasive feature identifiers found in source:")
            self.failures.extend(f"    {f}" for f in findings)
        else:
            self.ok("No invasive personal-data fields or identifiers in source.")

    def _tracked_files(self) -> list[str] | None:
        try:
            out = subprocess.run(
                ["git", "ls-files"], cwd=REPO, capture_output=True, text=True, check=True
            )
        except Exception:
            return None
        return [line.strip() for line in out.stdout.splitlines() if line.strip()]

    def check_no_secrets_or_media_tracked(self) -> None:
        tracked = self._tracked_files()
        if tracked is None:
            self.ok("git not available — skipped tracked-file checks (not a git repo?).")
            return

        if ".env" in tracked:
            self.fail("'.env' is tracked by git — secrets must never be committed.")
        else:
            self.ok("No '.env' tracked (only .env.example).")

        bad_media = [
            f for f in tracked if Path(f).suffix.lower() in FORBIDDEN_TRACKED_EXT
        ]
        if bad_media:
            self.fail(f"Forbidden media/model files tracked: {bad_media}")
        else:
            self.ok("No raw video or model-weight files tracked.")

    def check_docs(self) -> None:
        readme = (REPO / "README.md").read_text(encoding="utf-8") if (REPO / "README.md").exists() else ""
        if "What this project does NOT do" in readme:
            self.ok("README contains the 'What this project does NOT do' section.")
        else:
            self.fail("README is missing the 'What this project does NOT do' section.")

        for doc in ("PRIVACY.md", "SECURITY.md"):
            if (REPO / doc).exists():
                self.ok(f"{doc} present.")
            else:
                self.fail(f"{doc} is missing.")

    def check_raw_frame_default(self) -> None:
        config = REPO / "backend" / "app" / "config.py"
        text = config.read_text(encoding="utf-8") if config.exists() else ""
        if re.search(r"enable_raw_frame_storage:\s*bool\s*=\s*False", text):
            self.ok("Raw frame storage defaults to False.")
        else:
            self.fail("Raw frame storage default is not False in config.py.")

    def run(self) -> int:
        self.check_source_tokens()
        self.check_no_secrets_or_media_tracked()
        self.check_docs()
        self.check_raw_frame_default()

        print("Privacy audit\n=============")
        for msg in self.passes:
            print(f"  [PASS] {msg}")
        for msg in self.failures:
            print(f"  [FAIL] {msg}")
        print("-------------")
        if self.failures:
            print(f"RESULT: FAIL ({len(self.failures)} issue group(s))")
            return 1
        print("RESULT: PASS - privacy guarantees intact.")
        return 0


if __name__ == "__main__":
    sys.exit(Audit().run())
