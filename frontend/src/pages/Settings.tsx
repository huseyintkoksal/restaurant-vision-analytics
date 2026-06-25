import { useEffect, useState } from "react";
import { api, API_BASE_URL, type HealthResponse } from "../api/client";
import type { PrivacyStatus } from "../types/analytics";

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between border-b border-ink-800 py-2 last:border-0">
      <span className="text-sm text-slate-400">{label}</span>
      <span className="text-sm font-medium text-slate-200">{value}</span>
    </div>
  );
}

export default function Settings() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [privacy, setPrivacy] = useState<PrivacyStatus | null>(null);

  useEffect(() => {
    api.health().then(setHealth).catch(() => undefined);
    api.privacy().then(setPrivacy).catch(() => undefined);
  }, []);

  return (
    <div className="mx-auto max-w-2xl">
      <h1 className="mb-1 text-xl font-semibold text-white">Settings</h1>
      <p className="mb-5 text-sm text-slate-400">
        Runtime configuration (read-only). Change these via environment variables — see{" "}
        <code className="text-slate-300">.env.example</code>.
      </p>

      <div className="panel">
        <div className="panel-title mb-2">Runtime</div>
        <Row label="API base URL" value={API_BASE_URL} />
        <Row label="Version" value={health?.version ?? "—"} />
        <Row label="Demo mode" value={health ? (health.demo_mode ? "Enabled" : "Disabled") : "—"} />
        <Row
          label="Raw frame storage"
          value={privacy ? (privacy.raw_frame_storage ? "Enabled" : "Disabled (default)") : "—"}
        />
        <Row
          label="Data retention"
          value={privacy ? `${privacy.data_retention_days} days` : "—"}
        />
      </div>

      <div className="mt-4 rounded-lg border border-ink-800 bg-ink-850 p-4 text-sm text-slate-400">
        Raw frame storage is disabled by default and is a deliberate, audited operator decision.
        Enabling it does not turn on any identification feature — those do not exist in this
        toolkit.
      </div>
    </div>
  );
}
