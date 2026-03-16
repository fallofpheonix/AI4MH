import { memo } from "react";

export const LogList = memo(function LogList({ logs }) {
  return (
    <section>
      <h2>Logs</h2>
      <ul>
        {logs.map((l, i) => (
          <li key={i}>
            {l.timestamp} - {l.event}
          </li>
        ))}
      </ul>
    </section>
  );
});
