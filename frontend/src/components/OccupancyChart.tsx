import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { HistoryPoint } from "../types/analytics";

interface Props {
  data: HistoryPoint[];
}

function formatTime(ts: string): string {
  const d = new Date(ts);
  return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
}

export default function OccupancyChart({ data }: Props) {
  const series = data.map((p) => ({
    time: formatTime(p.timestamp),
    occupancy: p.total,
    queue: p.queue_count,
  }));

  return (
    <div className="panel h-72">
      <div className="panel-title mb-3">Occupancy over time</div>
      <ResponsiveContainer width="100%" height="85%">
        <AreaChart data={series} margin={{ top: 4, right: 8, left: -20, bottom: 0 }}>
          <defs>
            <linearGradient id="occ" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#34d399" stopOpacity={0.5} />
              <stop offset="100%" stopColor="#34d399" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="que" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#38bdf8" stopOpacity={0.4} />
              <stop offset="100%" stopColor="#38bdf8" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid stroke="#1e293b" vertical={false} />
          <XAxis dataKey="time" tick={{ fill: "#64748b", fontSize: 11 }} minTickGap={32} />
          <YAxis tick={{ fill: "#64748b", fontSize: 11 }} allowDecimals={false} width={40} />
          <Tooltip
            contentStyle={{
              background: "#0f172a",
              border: "1px solid #1e293b",
              borderRadius: 8,
              color: "#e2e8f0",
            }}
          />
          <Area
            type="monotone"
            dataKey="occupancy"
            stroke="#34d399"
            strokeWidth={2}
            fill="url(#occ)"
          />
          <Area type="monotone" dataKey="queue" stroke="#38bdf8" strokeWidth={2} fill="url(#que)" />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
