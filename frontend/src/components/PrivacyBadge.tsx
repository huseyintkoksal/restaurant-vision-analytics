import { Link } from "react-router-dom";

/**
 * Always-visible privacy posture badge. The guarantees are a feature, not fine
 * print — so we surface them in the header on every page.
 */
export default function PrivacyBadge() {
  return (
    <Link
      to="/privacy"
      className="pill border border-emerald-500/30 bg-emerald-500/10 text-emerald-300 hover:bg-emerald-500/20"
      title="No facial recognition · No biometrics · No persistent tracking"
    >
      <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
      Privacy-first
    </Link>
  );
}
