// Shared API types mirroring the backend's aggregate, anonymous schema.

export interface PrivacyFlags {
  identity_tracking: boolean;
  biometrics: boolean;
  raw_frame_storage: boolean;
}

export interface Occupancy {
  total: number;
  by_zone: Record<string, number>;
  by_type?: Record<string, number>;
}

export interface QueueMetrics {
  count: number;
  pressure_score: number;
  status: string;
  estimated_wait_pressure?: string;
}

export interface TableReading {
  zone_id: string;
  name: string;
  occupied: boolean;
  duration_seconds: number;
  turnover_count: number;
  idle: boolean;
}

export interface LiveSnapshot {
  timestamp: string;
  camera_id: string;
  occupancy: Occupancy;
  queue: QueueMetrics;
  tables: TableReading[];
  active_tracks?: number;
  privacy: PrivacyFlags;
}

export interface HistoryPoint {
  timestamp: string;
  total: number;
  queue_count: number;
  queue_pressure: number;
}

export interface Summary {
  camera_id: string;
  since: string;
  estimated_visitors: number;
  occupancy: {
    peak: number;
    average: number;
    samples: number;
    peak_by_zone: Record<string, number>;
  };
  peak_hour: string | null;
  tables: {
    tables: number;
    occupied: number;
    free: number;
    occupancy_rate: number;
    total_turnovers: number;
    avg_occupied_duration_seconds: number;
  };
  privacy: Record<string, boolean>;
}

export interface HeatmapData {
  rows: number;
  cols: number;
  max: number;
  cells: number[][];
}

export interface Alert {
  id: number;
  type: string;
  severity: "info" | "warning" | "critical";
  message: string;
  camera_id?: string | null;
  zone_id?: string | null;
  value?: number | null;
  created_at: string;
  resolved: boolean;
}

export interface Camera {
  id: string;
  name: string;
  location?: string | null;
  status: "online" | "offline" | "unknown";
  source_type: string;
  created_at: string;
  last_seen?: string | null;
}

export interface Zone {
  id: string;
  name: string;
  type: string;
  camera_id?: string | null;
  capacity?: number | null;
  polygon: number[][];
  attributes: Record<string, unknown>;
}

export interface PrivacyStatus {
  facial_recognition: boolean;
  biometric_identification: boolean;
  demographic_inference: boolean;
  emotion_detection: boolean;
  audio_recording: boolean;
  persistent_customer_tracking: boolean;
  raw_frame_storage: boolean;
  identity_persistence: boolean;
  ephemeral_tracking: boolean;
  local_first: boolean;
  data_retention_days: number;
  statement: string;
}
