// Minimal typed REST client for the analytics backend.

import type {
  Alert,
  Camera,
  HeatmapData,
  HistoryPoint,
  LiveSnapshot,
  PrivacyStatus,
  Summary,
  Zone,
} from "../types/analytics";

export const API_BASE_URL: string =
  (import.meta.env.VITE_API_BASE_URL as string | undefined) ?? "http://localhost:8000";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`);
  if (!res.ok) {
    throw new Error(`Request failed: ${res.status} ${path}`);
  }
  return (await res.json()) as T;
}

export interface HealthResponse {
  status: string;
  version: string;
  demo_mode: boolean;
  privacy: Record<string, boolean>;
  privacy_statement: string;
}

export const api = {
  health: () => get<HealthResponse>("/health"),
  live: () => get<LiveSnapshot>("/api/analytics/live"),
  summary: () => get<Summary>("/api/analytics/summary"),
  heatmap: () => get<HeatmapData>("/api/analytics/heatmap"),
  history: () => get<{ series: HistoryPoint[] }>("/api/analytics/history"),
  queue: () => get<LiveSnapshot["queue"]>("/api/analytics/queue"),
  tables: () => get<{ tables: LiveSnapshot["tables"]; summary: Summary["tables"] }>(
    "/api/analytics/tables",
  ),
  alerts: () => get<Alert[]>("/api/alerts"),
  cameras: () => get<Camera[]>("/api/cameras"),
  zones: () => get<Zone[]>("/api/zones"),
  privacy: () => get<PrivacyStatus>("/api/privacy"),
};
