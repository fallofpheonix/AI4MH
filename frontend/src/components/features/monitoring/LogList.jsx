import { memo } from "react";

export const LogList = memo(function LogList({ logs }) {
  return (
    <section className="panel">
      <h2 className="panel__title">Logs</h2>
      <ul className="log-list">
        {logs.map((log, index) => (
          <li className="log-list__item" key={index}>
            {log.timestamp} - {log.event}
          </li>
        ))}
      </ul>
    </section>
  );
});
