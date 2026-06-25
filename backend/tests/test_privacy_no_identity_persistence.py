"""Privacy guarantees: no identity, biometrics, or persistence of people.

These tests encode the project's core promises as executable checks so a future
change that tries to add a face/identity/biometric column or attribute fails CI.
"""

from __future__ import annotations

import re
from dataclasses import fields

from sqlmodel import SQLModel

from app.vision.detector_base import Detection

# Vocabulary that must never appear as a *token* in the persisted schema or the
# detection model. Token-based (not substring) so e.g. "message" never trips on
# "age".
FORBIDDEN_TOKENS = {
    "face",
    "facial",
    "identity",
    "biometric",
    "biometrics",
    "embedding",
    "embeddings",
    "fingerprint",
    "age",
    "gender",
    "ethnicity",
    "race",
    "emotion",
    "recognition",
    "demographic",
}


def _tokens(name: str) -> set[str]:
    return set(re.split(r"[^a-z0-9]+", name.lower()))


def test_detection_has_no_personal_attributes():
    field_names = {f.name for f in fields(Detection)}
    # Only geometry + confidence + a constant label.
    assert field_names == {"bbox", "confidence", "label"}
    for name in field_names:
        assert not (_tokens(name) & FORBIDDEN_TOKENS)


def test_no_database_table_stores_identities():
    # Importing models registers every table on the shared metadata.
    import app.models  # noqa: F401

    table_names = set(SQLModel.metadata.tables.keys())
    # Only configuration + aggregate tables exist.
    assert table_names == {"cameras", "zones", "analytics_snapshots", "alerts"}

    for table in SQLModel.metadata.tables.values():
        for column in table.columns:
            offending = _tokens(column.name) & FORBIDDEN_TOKENS
            assert not offending, f"forbidden token {offending} in {table.name}.{column.name}"


def test_engine_snapshot_marks_identity_tracking_off():
    from app.services.analytics_service import AnalyticsService

    service = AnalyticsService()
    snapshot = service.tick_once()
    assert snapshot["privacy"]["identity_tracking"] is False
    assert snapshot["privacy"]["biometrics"] is False
    assert snapshot["privacy"]["raw_frame_storage"] is False


def test_persisted_snapshot_payload_is_aggregate_only():
    from app.services.analytics_service import AnalyticsService

    service = AnalyticsService()
    snapshot = service.tick_once()
    # The payload we persist has only aggregate keys — no tracks/identities.
    payload_keys = {"occupancy", "queue", "tables"}
    assert payload_keys.issubset(set(snapshot.keys()))
    assert "tracks" not in snapshot
    assert "identities" not in snapshot
    assert "embeddings" not in snapshot
