export function MetricPill({ label, value }) {
  return (
    <div className="metric-pill">
      <span className="metric-pill__label">{label}</span>
      <strong className="metric-pill__value">{value}</strong>
    </div>
  );
}
