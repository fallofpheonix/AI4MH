import { memo } from "react";

import { formatScore, scoreColor } from "@/utils/score";

export const AlertList = memo(function AlertList({ alerts }) {
  return (
    <section className="panel">
      <h2 className="panel__title">Alerts</h2>
      {alerts.length === 0 ? (
        <div className="panel__empty">No active crisis alerts</div>
      ) : (
        <ul className="alert-list">
          {alerts.map((alert, index) => (
            <li className="alert-list__item" key={`${alert.region}-${index}`}>
              <strong>{alert.region}</strong>
              <span>
                score{" "}
                <span style={{ color: scoreColor(alert.score) }}>
                  {formatScore(alert.score)}
                </span>
              </span>
              <span>{alert.status}</span>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
});
