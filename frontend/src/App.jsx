import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { AlertList } from "./components/AlertList";
import { PostTable } from "./components/PostTable";
import { LogList } from "./components/LogList";

const API = "http://localhost:8000/api";

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
      <h1 style={{ marginBottom: 8 }}>AI4MH - Modular Crisis Monitor</h1>
      <p style={{ marginTop: 0, color: "#4b5563" }}>
        Production-ready frontend with React.memo and component isolation.
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

