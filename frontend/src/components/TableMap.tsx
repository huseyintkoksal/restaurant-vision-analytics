import type { TableReading } from "../types/analytics";

interface Props {
  tables: TableReading[];
}

function formatDuration(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  if (m <= 0) return `${s}s`;
  return `${m}m ${s.toString().padStart(2, "0")}s`;
}

export default function TableMap({ tables }: Props) {
  return (
    <div className="panel">
      <div className="mb-3 flex items-center justify-between">
        <div className="panel-title">Table map</div>
        <div className="flex items-center gap-3 text-[11px] text-slate-400">
          <Legend color="bg-emerald-500" label="Occupied" />
          <Legend color="bg-ink-700" label="Free" />
          <Legend color="bg-amber-500" label="Idle" />
        </div>
      </div>

      {tables.length === 0 ? (
        <div className="py-8 text-center text-sm text-slate-500">No table zones configured.</div>
      ) : (
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
          {tables.map((t) => {
            const color = t.idle
              ? "border-amber-500/40 bg-amber-500/10"
              : t.occupied
                ? "border-emerald-500/40 bg-emerald-500/10"
                : "border-ink-800 bg-ink-850";
            return (
              <div key={t.zone_id} className={`rounded-lg border p-3 ${color}`}>
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-slate-200">{t.name}</span>
                  <span
                    className={`h-2 w-2 rounded-full ${
                      t.occupied ? "bg-emerald-400" : "bg-slate-600"
                    }`}
                  />
                </div>
                <div className="mt-2 text-xs text-slate-400">
                  {t.occupied ? formatDuration(t.duration_seconds) : "Available"}
                </div>
                <div className="mt-0.5 text-[11px] text-slate-500">
                  {t.turnover_count} turnovers
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

function Legend({ color, label }: { color: string; label: string }) {
  return (
    <span className="inline-flex items-center gap-1">
      <span className={`h-2 w-2 rounded-full ${color}`} />
      {label}
    </span>
  );
}
