import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { fetchDashboardSnapshot, ingestPosts } from "@/services/dashboardService";

export function useDashboardData({ defaultBatchSize = 30, refreshIntervalMs = 5000 } = {}) {
  const [posts, setPosts] = useState([]);
  const [scores, setScores] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [logs, setLogs] = useState([]);
  const [live, setLive] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const timerRef = useRef(null);

  const scoreByRegion = useMemo(() => {
    const scoreMap = new Map();
    scores.forEach((score) => {
      scoreMap.set(score.region_id, score.crisis_score ?? 0);
    });
    return scoreMap;
  }, [scores]);

  const refresh = useCallback(async () => {
    try {
      const snapshot = await fetchDashboardSnapshot();
      setPosts(snapshot.posts);
      setScores(snapshot.scores);
      setAlerts(snapshot.alerts);
      setLogs(snapshot.logs);
      setError("");
    } catch {
      setError("Unable to reach the backend API");
    }
  }, []);

  const ingest = useCallback(async () => {
    setLoading(true);
    try {
      await ingestPosts(defaultBatchSize);
      await refresh();
      setError("");
    } catch {
      setError("Ingest failed");
    } finally {
      setLoading(false);
    }
  }, [defaultBatchSize, refresh]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  useEffect(() => {
    if (!live) {
      if (timerRef.current !== null) {
        window.clearInterval(timerRef.current);
      }
      return undefined;
    }

    timerRef.current = window.setInterval(() => {
      void ingest();
    }, refreshIntervalMs);

    return () => {
      if (timerRef.current !== null) {
        window.clearInterval(timerRef.current);
      }
    };
  }, [live, ingest, refreshIntervalMs]);

  return {
    alerts,
    error,
    ingest,
    live,
    loading,
    logs,
    posts,
    scoreByRegion,
    scores,
    setLive,
  };
}
