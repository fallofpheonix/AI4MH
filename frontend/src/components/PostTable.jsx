import { memo } from "react";

const threshold = 0.75;
function scoreColor(v) {
  if (v >= threshold) return "#dc2626";
  if (v >= 0.4) return "#d97706";
  return "#16a34a";
}

export const PostTable = memo(function PostTable({ posts, scoreByRegion }) {
  return (
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
  );
});
