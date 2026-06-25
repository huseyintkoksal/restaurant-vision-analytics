"""WebSocket live-analytics payload schema."""

from __future__ import annotations


def test_websocket_emits_aggregate_snapshot(client):
    with client.websocket_connect("/ws/analytics") as ws:
        message = ws.receive_json()
    # Same aggregate schema as the REST live endpoint.
    assert {"timestamp", "camera_id", "occupancy", "queue", "tables", "privacy"}.issubset(
        message.keys()
    )
    assert message["privacy"]["identity_tracking"] is False
    assert message["privacy"]["raw_frame_storage"] is False
