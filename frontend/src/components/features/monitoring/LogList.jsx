import { memo } from "react";

export const LogList = memo(function LogList({ logs }) {
  return (
    <section className="panel">
      <h2 className="panel__title">Logs</h2>
      <ul className="log-list">
        {logs.map((log) => {
          const payloadKey = JSON.stringify(log.payload ?? {});
          return (
            <li
              className="log-list__item"
              key={`${log.timestamp}-${log.event}-${payloadKey}`}
            >
              {log.timestamp} - {log.event}
            </li>
          );
        })}
      </ul>
    </section>
  );
});
