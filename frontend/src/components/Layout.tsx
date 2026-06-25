import { NavLink, Outlet } from "react-router-dom";
import PrivacyBadge from "./PrivacyBadge";

const NAV = [
  { to: "/", label: "Dashboard", end: true },
  { to: "/cameras", label: "Cameras", end: false },
  { to: "/zones", label: "Zones", end: false },
  { to: "/privacy", label: "Privacy", end: false },
  { to: "/settings", label: "Settings", end: false },
];

export default function Layout() {
  return (
    <div className="flex min-h-screen bg-ink-950 text-slate-200">
      {/* Sidebar */}
      <aside className="hidden w-60 shrink-0 flex-col border-r border-ink-800 bg-ink-900/60 px-4 py-6 md:flex">
        <div className="mb-8 px-2">
          <div className="flex items-center gap-2">
            <div className="grid h-9 w-9 place-items-center rounded-lg bg-emerald-500/15 text-emerald-400">
              <LensIcon />
            </div>
            <div>
              <div className="text-sm font-semibold leading-tight text-white">
                Restaurant Vision
              </div>
              <div className="text-[11px] leading-tight text-slate-400">Analytics</div>
            </div>
          </div>
        </div>

        <nav className="flex flex-col gap-1">
          {NAV.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                `rounded-lg px-3 py-2 text-sm font-medium transition ${
                  isActive
                    ? "bg-emerald-500/15 text-emerald-300"
                    : "text-slate-400 hover:bg-ink-800 hover:text-slate-200"
                }`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="mt-auto rounded-lg border border-ink-800 bg-ink-850 p-3 text-[11px] leading-relaxed text-slate-400">
          No facial recognition. No biometrics. No persistent customer tracking.
        </div>
      </aside>

      {/* Main */}
      <div className="flex min-w-0 flex-1 flex-col">
        <header className="sticky top-0 z-10 flex items-center justify-between border-b border-ink-800 bg-ink-950/80 px-6 py-3 backdrop-blur">
          <div className="flex items-center gap-3">
            <span className="text-sm font-semibold text-white md:hidden">
              Restaurant Vision Analytics
            </span>
            <span className="hidden text-sm text-slate-400 md:block">
              Operations Analytics
            </span>
          </div>
          <PrivacyBadge />
        </header>

        <main className="flex-1 px-4 py-5 sm:px-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

function LensIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <circle cx="12" cy="12" r="8" />
      <circle cx="12" cy="12" r="3" />
    </svg>
  );
}
