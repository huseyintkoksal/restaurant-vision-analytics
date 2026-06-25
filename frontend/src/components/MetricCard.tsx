import type { ReactNode } from "react";

interface MetricCardProps {
  label: string;
  value: ReactNode;
  hint?: string;
  accent?: "emerald" | "sky" | "amber" | "rose" | "slate";
}

const ACCENTS: Record<string, string> = {
  emerald: "text-emerald-300",
  sky: "text-sky-300",
  amber: "text-amber-300",
  rose: "text-rose-300",
  slate: "text-slate-100",
};

export default function MetricCard({ label, value, hint, accent = "slate" }: MetricCardProps) {
  return (
    <div className="panel">
      <div className="panel-title">{label}</div>
      <div className={`mt-2 text-3xl font-semibold tabular-nums ${ACCENTS[accent]}`}>{value}</div>
      {hint && <div className="mt-1 text-xs text-slate-500">{hint}</div>}
    </div>
  );
}
