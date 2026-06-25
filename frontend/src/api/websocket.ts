// WebSocket helper for the live analytics feed with auto-reconnect.

import { API_BASE_URL } from "./client";
import type { LiveSnapshot } from "../types/analytics";

function wsUrl(): string {
  const base = API_BASE_URL.replace(/^http/, "ws");
  return `${base}/ws/analytics`;
}

export interface LiveConnection {
  close: () => void;
}

/**
 * Subscribe to live aggregate snapshots. Reconnects automatically on drop.
 */
export function connectLiveAnalytics(
  onSnapshot: (snapshot: LiveSnapshot) => void,
  onStatus?: (connected: boolean) => void,
): LiveConnection {
  let socket: WebSocket | null = null;
  let reconnectTimer: ReturnType<typeof setTimeout> | null = null;
  let closedByCaller = false;

  const open = () => {
    socket = new WebSocket(wsUrl());

    socket.onopen = () => onStatus?.(true);

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data) as LiveSnapshot;
        onSnapshot(data);
      } catch {
        /* ignore malformed frames */
      }
    };

    socket.onclose = () => {
      onStatus?.(false);
      if (!closedByCaller) {
        reconnectTimer = setTimeout(open, 2000);
      }
    };

    socket.onerror = () => socket?.close();
  };

  open();

  return {
    close: () => {
      closedByCaller = true;
      if (reconnectTimer) clearTimeout(reconnectTimer);
      socket?.close();
    },
  };
}
