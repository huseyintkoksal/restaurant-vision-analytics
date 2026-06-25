import { useEffect, useState } from "react";
import { api } from "../api/client";
import CameraStatus from "../components/CameraStatus";
import type { Camera } from "../types/analytics";

export default function Cameras() {
  const [cameras, setCameras] = useState<Camera[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .cameras()
      .then((c) => setCameras(c))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="mx-auto max-w-4xl">
      <h1 className="mb-1 text-xl font-semibold text-white">Cameras</h1>
      <p className="mb-5 text-sm text-slate-400">
        Camera configuration only. Connection credentials are never stored in the database —
        provide them through environment variables or a secrets manager at runtime.
      </p>

      {loading ? (
        <div className="panel text-sm text-slate-500">Loading…</div>
      ) : (
        <CameraStatus cameras={cameras} connected={true} />
      )}

      <div className="mt-4 rounded-lg border border-ink-800 bg-ink-850 p-4 text-sm text-slate-400">
        <div className="mb-1 font-medium text-slate-200">Adding a real camera (v0.2+)</div>
        RTSP and device sources are on the roadmap. The current release ships a fully working
        demo camera that generates synthetic, anonymous flow so you can evaluate the whole
        pipeline without hardware.
      </div>
    </div>
  );
}
