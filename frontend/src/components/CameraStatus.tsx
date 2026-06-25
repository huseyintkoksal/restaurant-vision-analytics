import type { Camera } from "../types/analytics";

interface Props {
  cameras: Camera[];
  connected: boolean;
}

export default function CameraStatus({ cameras, connected }: Props) {
  return (
    <div className="panel">
      <div className="mb-3 flex items-center justify-between">
        <div className="panel-title">Camera health</div>
        <span
          className={`pill ${
            connected
              ? "bg-emerald-500/10 text-emerald-300"
              : "bg-slate-500/10 text-slate-400"
          }`}
        >
          <span
            className={`h-1.5 w-1.5 rounded-full ${connected ? "bg-emerald-400" : "bg-slate-500"}`}
          />
          {connected ? "Live" : "Reconnecting"}
        </span>
      </div>

      {cameras.length === 0 ? (
        <div className="py-6 text-center text-sm text-slate-500">No cameras configured.</div>
      ) : (
        <ul className="flex flex-col gap-2">
          {cameras.map((cam) => (
            <li
              key={cam.id}
              className="flex items-center justify-between rounded-lg border border-ink-800 bg-ink-850 px-3 py-2"
            >
              <div>
                <div className="text-sm font-medium text-slate-200">{cam.name}</div>
                <div className="text-[11px] text-slate-500">
                  {cam.location ?? "—"} · {cam.source_type}
                </div>
              </div>
              <span
                className={`pill ${
                  cam.status === "online"
                    ? "bg-emerald-500/10 text-emerald-300"
                    : cam.status === "offline"
                      ? "bg-rose-500/10 text-rose-300"
                      : "bg-slate-500/10 text-slate-400"
                }`}
              >
                {cam.status}
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
