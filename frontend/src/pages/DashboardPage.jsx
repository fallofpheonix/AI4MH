import { ErrorBanner } from "@/components/common/ErrorBanner";
import { MetricPill } from "@/components/common/MetricPill";
import { AlertList } from "@/components/features/alerts/AlertList";
import { LogList } from "@/components/features/monitoring/LogList";
import { PostTable } from "@/components/features/monitoring/PostTable";
import { AppShell } from "@/components/layout/AppShell";
import { useDashboardData } from "@/hooks/useDashboardData";

export function DashboardPage() {
  const {
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
  } = useDashboardData();

  return (
    <AppShell
      title="AI4MH"
      description="Lightweight dashboard for reviewing regional signals and alert activity."
      actions={
        <>
          <button onClick={() => void ingest()} disabled={loading} type="button">
            {loading ? "Ingesting..." : "Ingest Posts"}
          </button>
          <button onClick={() => setLive((value) => !value)} type="button">
            {live ? "Pause" : "Resume"}
          </button>
        </>
      }
      metrics={
        <>
          <MetricPill label="Posts" value={posts.length} />
          <MetricPill label="Regions" value={scores.length} />
          <MetricPill label="Alerts" value={alerts.length} />
        </>
      }
    >
      <ErrorBanner message={error} />
      <AlertList alerts={alerts} />
      <PostTable posts={posts} scoreByRegion={scoreByRegion} />
      <LogList logs={logs} />
    </AppShell>
  );
}
