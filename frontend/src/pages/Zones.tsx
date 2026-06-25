import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { Zone } from "../types/analytics";

const TYPE_COLORS: Record<string, string> = {
  entrance: "#38bdf8",
  queue: "#f59e0b",
  cashier: "#a78bfa",
  dining_area: "#34d399",
  table: "#10b981",
  kitchen_pass: "#fb7185",
  pickup_area: "#facc15",
};

function pointsAttr(polygon: number[][]): string {
  return polygon.map(([x, y]) => `${x * 100},${y * 100}`).join(" ");
}

export default function Zones() {
  const [zones, setZones] = useState<Zone[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .zones()
      .then((z) => setZones(z))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="mx-auto max-w-5xl">
      <h1 className="mb-1 text-xl font-semibold text-white">Zones</h1>
      <p className="mb-5 text-sm text-slate-400">
        Zones are named polygons over a camera view. They describe <em>places</em> — entrances,
        queues, tables — never people.
      </p>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <div className="panel">
          <div className="panel-title mb-3">Floor plan</div>
          {loading ? (
            <div className="text-sm text-slate-500">Loading…</div>
          ) : (
            <svg viewBox="0 0 100 100" className="w-full rounded-lg bg-ink-950">
              {zones.map((z) => (
                <polygon
                  key={z.id}
                  points={pointsAttr(z.polygon)}
                  fill={`${TYPE_COLORS[z.type] ?? "#64748b"}22`}
                  stroke={TYPE_COLORS[z.type] ?? "#64748b"}
                  strokeWidth={0.4}
                />
              ))}
            </svg>
          )}
        </div>

        <div className="panel">
          <div className="panel-title mb-3">Configured zones ({zones.length})</div>
          <ul className="flex flex-col gap-2">
            {zones.map((z) => (
              <li
                key={z.id}
                className="flex items-center justify-between rounded-lg border border-ink-800 bg-ink-850 px-3 py-2"
              >
                <div className="flex items-center gap-2">
                  <span
                    className="h-2.5 w-2.5 rounded-sm"
                    style={{ backgroundColor: TYPE_COLORS[z.type] ?? "#64748b" }}
                  />
                  <span className="text-sm text-slate-200">{z.name}</span>
                </div>
                <span className="text-[11px] text-slate-500">
                  {z.type.replace(/_/g, " ")}
                  {z.capacity ? ` · cap ${z.capacity}` : ""}
                </span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="mt-4 rounded-lg border border-ink-800 bg-ink-850 p-4 text-sm text-slate-400">
        A drag-and-drop zone editor is planned for v0.2. For now, zones are seeded from the demo
        floor plan and can be created via <code className="text-slate-300">POST /api/zones</code>.
      </div>
    </div>
  );
}
