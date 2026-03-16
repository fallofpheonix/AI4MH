import { memo } from "react";

const threshold = 0.75;
function scoreColor(v) {
  if (v >= threshold) return "#dc2626";
  if (v >= 0.4) return "#d97706";
  return "#16a34a";
}

export const AlertList = memo(function AlertList({ alerts }) {
  return (
    <section style={{ marginBottom: 20 }}>
      <h2>Alerts</h2>
      {alerts.length === 0 ? (
        <div>No active crisis alerts</div>
      ) : (
        <ul>
          {alerts.map((a, i) => (
            <li key={`${a.region}-${i}`}>
              <strong>{a.region}</strong> - score <span style={{ color: scoreColor(a.score) }}>{a.score}</span> - {a.status}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
});
