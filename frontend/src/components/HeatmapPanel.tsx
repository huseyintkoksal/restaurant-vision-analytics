import type { HeatmapData } from "../types/analytics";

interface Props {
  data?: HeatmapData;
}

/** Map a 0–1 intensity to a teal→amber heat color (no identities, just density). */
function heatColor(value: number): string {
  if (value <= 0.001) return "rgba(148,163,184,0.06)";
  // Interpolate hue from teal (170) to amber (40).
  const hue = 170 - value * 130;
  const light = 30 + value * 25;
  return `hsl(${hue}, 80%, ${light}%)`;
}

export default function HeatmapPanel({ data }: Props) {
  const cells = data?.cells ?? [];
  const cols = data?.cols ?? 0;

  return (
    <div className="panel">
      <div className="mb-3 flex items-center justify-between">
        <div className="panel-title">Crowd density heatmap</div>
        <span className="text-[11px] text-slate-500">Anonymous density · not individuals</span>
      </div>

      {cells.length === 0 ? (
        <div className="py-8 text-center text-sm text-slate-500">Collecting density data…</div>
      ) : (
        <div
          className="grid gap-[2px] rounded-lg bg-ink-950 p-2"
          style={{ gridTemplateColumns: `repeat(${cols}, minmax(0, 1fr))` }}
        >
          {cells.flatMap((row, r) =>
            row.map((value, c) => (
              <div
                key={`${r}-${c}`}
                className="aspect-square rounded-[2px]"
                style={{ backgroundColor: heatColor(value) }}
                title={`Density ${(value * 100).toFixed(0)}%`}
              />
            )),
          )}
        </div>
      )}
    </div>
  );
}
