import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { AlertList } from "./components/AlertList";
import { PostTable } from "./components/PostTable";
import { LogList } from "./components/LogList";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";

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
        fetch(`${API_BASE_URL}/posts?limit=20`),
        fetch(`${API_BASE_URL}/scores`),
        fetch(`${API_BASE_URL}/alerts`),
        fetch(`${API_BASE_URL}/logs?limit=20`),
      ]);
      if (![p, s, a, l].every((response) => response.ok)) {
        throw new Error("One or more requests failed");
      }
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
      setError("Unable to reach the backend API");
    }
  }, []);

  const ingest = useCallback(async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/ingest?n=30`, { method: "POST" });
      if (!response.ok) {
        throw new Error("Ingest request failed");
      }
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
      <h1 style={{ marginBottom: 8 }}>AI4MH</h1>
      <p style={{ marginTop: 0, color: "#4b5563" }}>
        Lightweight dashboard for reviewing regional signals and alert activity.
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

      <AlertList alerts={alerts} />
      <PostTable posts={posts} scoreByRegion={scoreByRegion} />
      <LogList logs={logs} />
    </div>
  );
}

