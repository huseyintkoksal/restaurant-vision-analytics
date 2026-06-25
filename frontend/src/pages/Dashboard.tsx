import { useEffect, useRef, useState } from "react";
import { api } from "../api/client";
import { connectLiveAnalytics } from "../api/websocket";
import AlertList from "../components/AlertList";
import CameraStatus from "../components/CameraStatus";
import HeatmapPanel from "../components/HeatmapPanel";
import MetricCard from "../components/MetricCard";
import OccupancyChart from "../components/OccupancyChart";
import QueuePanel from "../components/QueuePanel";
import TableMap from "../components/TableMap";
import type {
  Alert,
  Camera,
  HeatmapData,
  HistoryPoint,
  LiveSnapshot,
  Summary,
} from "../types/analytics";

export default function Dashboard() {
  const [live, setLive] = useState<LiveSnapshot | null>(null);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [history, setHistory] = useState<HistoryPoint[]>([]);
  const [heatmap, setHeatmap] = useState<HeatmapData | undefined>(undefined);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [cameras, setCameras] = useState<Camera[]>([]);
  const [connected, setConnected] = useState(false);
  const [demoMode, setDemoMode] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Live WebSocket feed.
  useEffect(() => {
    const conn = connectLiveAnalytics(setLive, setConnected);
    return () => conn.close();
  }, []);

  // Periodic polling for slower-moving aggregates.
  const timer = useRef<ReturnType<typeof setInterval> | null>(null);
  useEffect(() => {
    let cancelled = false;
    const load = async () => {
      try {
        const [s, h, hm, al, cam] = await Promise.all([
          api.summary(),
          api.history(),
          api.heatmap(),
          api.alerts(),
          api.cameras(),
        ]);
        if (cancelled) return;
        setSummary(s);
        setHistory(h.series);
        setHeatmap(hm);
        setAlerts(al);
        setCameras(cam);
        setError(null);
      } catch (e) {
        if (!cancelled) setError("Backend unreachable. Is the API running on :8000?");
      }
    };
    api
      .health()
      .then((hp) => setDemoMode(hp.demo_mode))
      .catch(() => undefined);
    load();
    timer.current = setInterval(load, 4000);
    return () => {
      cancelled = true;
      if (timer.current) clearInterval(timer.current);
    };
  }, []);

  const occupancyTotal = live?.occupancy.total ?? 0;
  const tables = live?.tables ?? [];
  const tableUsage = summary?.tables.occupancy_rate
    ? `${Math.round(summary.tables.occupancy_rate * 100)}%`
    : "—";

  return (
    <div className="mx-auto max-w-7xl">
      {/* Header row */}
      <div className="mb-5 flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-xl font-semibold text-white">Live Dashboard</h1>
          <p className="text-sm text-slate-400">
            Aggregate, anonymous restaurant operations metrics.
          </p>
        </div>
        {demoMode && (
          <span className="pill border border-amber-500/30 bg-amber-500/10 text-amber-300">
            <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-amber-400" />
            Demo mode · synthetic data
          </span>
        )}
      </div>

      {error && (
        <div className="mb-4 rounded-lg border border-rose-500/30 bg-rose-500/10 px-4 py-2 text-sm text-rose-300">
          {error}
        </div>
      )}

      {/* Metric cards */}
      <div className="grid grid-cols-2 gap-3 lg:grid-cols-3 xl:grid-cols-6">
        <MetricCard label="Live Occupancy" value={occupancyTotal} accent="emerald" />
        <MetricCard
          label="Visitors Today"
          value={summary?.estimated_visitors ?? "—"}
          hint="estimated"
          accent="sky"
        />
        <MetricCard
          label="Queue Pressure"
          value={`${Math.round((live?.queue.pressure_score ?? 0) * 100)}%`}
          accent="amber"
        />
        <MetricCard label="Avg Table Usage" value={tableUsage} accent="slate" />
        <MetricCard label="Peak Hour" value={summary?.peak_hour ?? "—"} accent="slate" />
        <MetricCard
          label="Peak Occupancy"
          value={summary?.occupancy.peak ?? "—"}
          accent="rose"
        />
      </div>

      {/* Main grid */}
      <div className="mt-4 grid grid-cols-1 gap-4 xl:grid-cols-3">
        <div className="xl:col-span-2">
          <OccupancyChart data={history} />
        </div>
        <QueuePanel queue={live?.queue} />
      </div>

      <div className="mt-4 grid grid-cols-1 gap-4 lg:grid-cols-2">
        <TableMap tables={tables} />
        <HeatmapPanel data={heatmap} />
      </div>

      <div className="mt-4 grid grid-cols-1 gap-4 lg:grid-cols-2">
        <AlertList alerts={alerts} />
        <CameraStatus cameras={cameras} connected={connected} />
      </div>
    </div>
  );
}
