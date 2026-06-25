import type { Alert } from "../types/analytics";

interface Props {
  alerts: Alert[];
}

const SEVERITY: Record<string, string> = {
  info: "border-sky-500/30 bg-sky-500/10 text-sky-300",
  warning: "border-amber-500/30 bg-amber-500/10 text-amber-300",
  critical: "border-rose-500/30 bg-rose-500/10 text-rose-300",
};

function timeAgo(iso: string): string {
  const seconds = Math.max(0, (Date.now() - new Date(iso).getTime()) / 1000);
  if (seconds < 60) return `${Math.floor(seconds)}s ago`;
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  return `${Math.floor(seconds / 3600)}h ago`;
}

export default function AlertList({ alerts }: Props) {
  return (
    <div className="panel">
      <div className="mb-3 flex items-center justify-between">
        <div className="panel-title">Alerts</div>
        <span className="text-[11px] text-slate-500">{alerts.length} recent</span>
      </div>

      {alerts.length === 0 ? (
        <div className="py-8 text-center text-sm text-slate-500">No active alerts.</div>
      ) : (
        <ul className="flex flex-col gap-2">
          {alerts.slice(0, 8).map((a) => (
            <li
              key={a.id}
              className={`flex items-start justify-between gap-3 rounded-lg border px-3 py-2 ${
                SEVERITY[a.severity] ?? SEVERITY.info
              }`}
            >
              <div className="min-w-0">
                <div className="truncate text-sm">{a.message}</div>
                <div className="mt-0.5 text-[11px] opacity-70">{a.type.replace(/_/g, " ")}</div>
              </div>
              <span className="shrink-0 text-[11px] opacity-70">{timeAgo(a.created_at)}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
