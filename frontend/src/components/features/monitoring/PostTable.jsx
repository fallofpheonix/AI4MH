import { memo } from "react";

import { formatScore, scoreColor } from "@/utils/score";

export const PostTable = memo(function PostTable({ posts, scoreByRegion }) {
  return (
    <section className="panel">
      <h2 className="panel__title">Recent Posts</h2>
      <table className="data-table">
        <thead>
          <tr>
            <th>Text</th>
            <th>Region</th>
            <th>Sentiment</th>
            <th>Region Score</th>
          </tr>
        </thead>
        <tbody>
          {posts.map((post) => {
            const regionScore = scoreByRegion.get(post.region_id) ?? 0;
            return (
              <tr key={post.id}>
                <td>{post.text}</td>
                <td>{post.region_id}</td>
                <td>{post.sentiment}</td>
                <td style={{ color: scoreColor(regionScore) }}>{formatScore(regionScore)}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </section>
  );
});
