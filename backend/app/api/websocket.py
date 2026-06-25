"""WebSocket endpoint for live aggregate analytics.

Subscribers receive the same anonymous, aggregate snapshots produced by the demo
loop (or, in a real deployment, the live pipeline). No imagery or identities are
ever transmitted.
"""

from __future__ import annotations

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.analytics_service import get_analytics_service

router = APIRouter(tags=["websocket"])


@router.websocket("/ws/analytics")
async def analytics_ws(websocket: WebSocket) -> None:
    service = get_analytics_service()
    await service.connections.connect(websocket)
    try:
        # Send the current snapshot immediately so new clients render at once.
        await websocket.send_json(service.get_engine().live())
        while True:
            # Keep the connection open; ignore inbound messages (read-only feed).
            await websocket.receive_text()
    except WebSocketDisconnect:
        service.connections.disconnect(websocket)
    except Exception:
        service.connections.disconnect(websocket)
