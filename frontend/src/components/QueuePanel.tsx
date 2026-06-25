import type { QueueMetrics } from "../types/analytics";

interface Props {
  queue?: QueueMetrics;
}

const STATUS_COLORS: Record<string, string> = {
  clear: "bg-emerald-500",
  moderate: "bg-sky-500",
  busy: "bg-amber-500",
  congested: "bg-rose-500",
};

export default function QueuePanel({ queue }: Props) {
  const pressure = queue?.pressure_score ?? 0;
  const pct = Math.round(pressure * 100);
  const status = queue?.status ?? "clear";
  const barColor = STATUS_COLORS[status] ?? "bg-slate-500";

  return (
    <div className="panel">
      <div className="flex items-center justify-between">
        <div className="panel-title">Queue pressure</div>
        <span className="text-xs capitalize text-slate-400">{status}</span>
      </div>

      <div className="mt-3 flex items-baseline gap-2">
        <span className="text-3xl font-semibold tabular-nums text-slate-100">{pct}%</span>
        <span className="text-sm text-slate-500">{queue?.count ?? 0} in line</span>
      </div>

      <div className="mt-3 h-2.5 w-full overflow-hidden rounded-full bg-ink-800">
        <div
          className={`h-full rounded-full transition-all duration-500 ${barColor}`}
          style={{ width: `${Math.min(pct, 100)}%` }}
        />
      </div>

      <div className="mt-2 text-xs text-slate-500">
        Estimated wait pressure: {queue?.estimated_wait_pressure ?? "low"}
      </div>
    </div>
  );
}
