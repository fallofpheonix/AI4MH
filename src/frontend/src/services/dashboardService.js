import { getJson, postJson } from "@/services/apiClient";

export async function fetchDashboardSnapshot() {
  const [posts, scores, alerts, logs] = await Promise.all([
    getJson("/posts?limit=20"),
    getJson("/scores"),
    getJson("/alerts"),
    getJson("/logs?limit=20"),
  ]);

  return {
    posts: posts.posts || [],
    scores: scores.scores || [],
    alerts: alerts.alerts || [],
    logs: logs.logs || [],
  };
}

export function ingestPosts(batchSize = 30) {
  return postJson(`/ingest?n=${batchSize}`);
}
