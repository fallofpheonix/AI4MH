import { useCallback, useEffect, useMemo, useRef, useState } from "react";

const API = "http://localhost:8000/api";
const threshold = 0.75;

function scoreColor(v) {
  if (v >= threshold) return "#dc2626";
  if (v >= 0.4) return "#d97706";
  return "#16a34a";
}

export default function App() {
  const [posts, setPosts] = useState([]);
  const [scores, setScores] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [logs, setLogs] = useState([]);
  const [live, setLive] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const timerRef = useRef(null);

  const scoreByRegion = useMemo(() => {
    const m = new Map();
    scores.forEach((s) => m.set(s.region_id, s.crisis_score ?? 0));
    return m;
  }, [scores]);

  const fetchAll = useCallback(async () => {
    try {
      const [p, s, a, l] = await Promise.all([
        fetch(`${API}/posts?limit=20`),
        fetch(`${API}/scores`),
        fetch(`${API}/alerts`),
        fetch(`${API}/logs?limit=20`),
      ]);
      const [pj, sj, aj, lj] = await Promise.all([
        p.json(),
        s.json(),
        a.json(),
        l.json(),
      ]);
      setPosts(pj.posts || []);
      setScores(sj.scores || []);
      setAlerts(aj.alerts || []);
      setLogs(lj.logs || []);
      setError("");
    } catch (e) {
      setError("Backend not reachable on :8000");
    }
  }, []);

  const ingest = useCallback(async () => {
    setLoading(true);
    try {
      await fetch(`${API}/ingest?n=30`, { method: "POST" });
      await fetchAll();
      setError("");
    } catch (e) {
      setError("Ingest failed");
    } finally {
      setLoading(false);
    }
  }, [fetchAll]);

  useEffect(() => {
    fetchAll();
  }, [fetchAll]);

  useEffect(() => {
    if (!live) {
      clearInterval(timerRef.current);
      return () => {};
    }
    timerRef.current = setInterval(() => {
      ingest();
    }, 5000);
    return () => clearInterval(timerRef.current);
  }, [live, ingest]);

  return (
    <div style={{ fontFamily: "system-ui, sans-serif", maxWidth: 1100, margin: "0 auto", padding: 20 }}>
      <h1 style={{ marginBottom: 8 }}>AI4MH - Minimal Crisis Monitor</h1>
      <p style={{ marginTop: 0, color: "#4b5563" }}>
        Strict MVP: frontend + backend + scoring + logging
      </p>

      <div style={{ display: "flex", gap: 10, marginBottom: 16 }}>
        <button onClick={ingest} disabled={loading}>
          {loading ? "Ingesting..." : "Ingest Posts"}
        </button>
        <button onClick={() => setLive((v) => !v)}>{live ? "Pause" : "Resume"}</button>
        <span>Posts: {posts.length}</span>
        <span>Regions: {scores.length}</span>
        <span>Alerts: {alerts.length}</span>
      </div>

      {error && (
        <div style={{ color: "#b91c1c", marginBottom: 12 }}>
          {error}
        </div>
      )}

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

      <section style={{ marginBottom: 20 }}>
        <h2>Recent Posts</h2>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={{ textAlign: "left", borderBottom: "1px solid #d1d5db" }}>Text</th>
              <th style={{ textAlign: "left", borderBottom: "1px solid #d1d5db" }}>Region</th>
              <th style={{ textAlign: "left", borderBottom: "1px solid #d1d5db" }}>Sentiment</th>
              <th style={{ textAlign: "left", borderBottom: "1px solid #d1d5db" }}>Region Score</th>
            </tr>
          </thead>
          <tbody>
            {posts.map((p) => {
              const regionScore = scoreByRegion.get(p.region_id) ?? 0;
              return (
                <tr key={p.id}>
                  <td style={{ borderBottom: "1px solid #f3f4f6", padding: "6px 0" }}>{p.text}</td>
                  <td style={{ borderBottom: "1px solid #f3f4f6", padding: "6px 0" }}>{p.region_id}</td>
                  <td style={{ borderBottom: "1px solid #f3f4f6", padding: "6px 0" }}>{p.sentiment}</td>
                  <td style={{ borderBottom: "1px solid #f3f4f6", padding: "6px 0", color: scoreColor(regionScore) }}>
                    {regionScore.toFixed(3)}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </section>

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
    </div>
  );
}
