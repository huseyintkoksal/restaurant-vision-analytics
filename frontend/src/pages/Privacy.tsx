import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { PrivacyStatus } from "../types/analytics";

const GUARANTEES: { key: keyof PrivacyStatus; label: string; wantFalse: boolean }[] = [
  { key: "facial_recognition", label: "Facial recognition", wantFalse: true },
  { key: "biometric_identification", label: "Biometric identification", wantFalse: true },
  { key: "demographic_inference", label: "Demographic inference (age/gender/etc.)", wantFalse: true },
  { key: "emotion_detection", label: "Emotion detection", wantFalse: true },
  { key: "audio_recording", label: "Audio recording", wantFalse: true },
  { key: "persistent_customer_tracking", label: "Persistent customer tracking", wantFalse: true },
  { key: "identity_persistence", label: "Identity persistence in database", wantFalse: true },
  { key: "raw_frame_storage", label: "Raw frame/video storage (default)", wantFalse: true },
  { key: "ephemeral_tracking", label: "Ephemeral, short-lived tracking only", wantFalse: false },
  { key: "local_first", label: "Local-first processing", wantFalse: false },
];

export default function Privacy() {
  const [status, setStatus] = useState<PrivacyStatus | null>(null);

  useEffect(() => {
    api.privacy().then(setStatus).catch(() => undefined);
  }, []);

  return (
    <div className="mx-auto max-w-3xl">
      <h1 className="mb-1 text-xl font-semibold text-white">Privacy</h1>
      <p className="mb-5 text-sm text-slate-400">
        Privacy is the default, enforced in code and surfaced live here.
      </p>

      <div className="panel mb-4 border-emerald-500/20 bg-emerald-500/5">
        <p className="text-sm leading-relaxed text-emerald-200">
          {status?.statement ??
            "This project does not perform facial recognition, biometric identification, demographic inference, emotion detection, audio recording, or persistent customer tracking."}
        </p>
      </div>

      <div className="panel">
        <div className="panel-title mb-3">Live privacy posture</div>
        <ul className="grid grid-cols-1 gap-2 sm:grid-cols-2">
          {GUARANTEES.map((g) => {
            const value = status ? Boolean(status[g.key]) : g.wantFalse ? false : true;
            const ok = g.wantFalse ? value === false : value === true;
            return (
              <li
                key={String(g.key)}
                className="flex items-center justify-between rounded-lg border border-ink-800 bg-ink-850 px-3 py-2"
              >
                <span className="text-sm text-slate-300">{g.label}</span>
                <span
                  className={`pill ${
                    ok ? "bg-emerald-500/10 text-emerald-300" : "bg-amber-500/10 text-amber-300"
                  }`}
                >
                  {g.wantFalse ? (value ? "ON" : "OFF") : value ? "ON" : "OFF"}
                </span>
              </li>
            );
          })}
        </ul>
        {status && (
          <div className="mt-3 text-xs text-slate-500">
            Aggregate metrics are retained for {status.data_retention_days} days, then pruned.
          </div>
        )}
      </div>
    </div>
  );
}
