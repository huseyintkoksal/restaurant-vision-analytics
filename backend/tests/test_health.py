"""Health endpoint and privacy posture."""

from __future__ import annotations


def test_health_ok(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert "version" in body
    assert body["demo_mode"] is True


def test_health_advertises_privacy_guarantees(client):
    body = client.get("/health").json()
    privacy = body["privacy"]
    # Every invasive capability must be reported as disabled.
    assert privacy["facial_recognition"] is False
    assert privacy["biometric_identification"] is False
    assert privacy["demographic_inference"] is False
    assert privacy["emotion_detection"] is False
    assert privacy["audio_recording"] is False
    assert privacy["persistent_customer_tracking"] is False
    assert privacy["raw_frame_storage"] is False
    assert "does not perform facial recognition" in body["privacy_statement"]


def test_privacy_endpoint(client):
    body = client.get("/api/privacy").json()
    assert body["facial_recognition"] is False
    assert body["identity_persistence"] is False
    assert body["ephemeral_tracking"] is True
    assert body["raw_frame_storage"] is False
