"""Privacy status & retention schemas (not database tables).

These schemas describe the project's privacy guarantees in a machine-readable
form. They are surfaced through the API and the dashboard's privacy badge so the
guarantees are visible, not just documented.
"""

from __future__ import annotations

from sqlmodel import SQLModel

PRIVACY_STATEMENT = (
    "This project does not perform facial recognition, biometric identification, "
    "demographic inference, emotion detection, audio recording, or persistent "
    "customer tracking."
)


class PrivacyStatus(SQLModel):
    """Machine-readable summary of privacy guarantees."""

    facial_recognition: bool = False
    biometric_identification: bool = False
    demographic_inference: bool = False
    emotion_detection: bool = False
    audio_recording: bool = False
    persistent_customer_tracking: bool = False
    raw_frame_storage: bool = False
    identity_persistence: bool = False
    ephemeral_tracking: bool = True
    local_first: bool = True
    data_retention_days: int = 7
    statement: str = PRIVACY_STATEMENT


class RetentionPolicy(SQLModel):
    """Describes how long aggregate analytics are retained."""

    data_retention_days: int = 7
    raw_frame_storage: bool = False
    description: str = (
        "Only aggregate, anonymous metrics are retained. Raw frames are not "
        "stored by default. Snapshots older than the retention window are pruned."
    )
