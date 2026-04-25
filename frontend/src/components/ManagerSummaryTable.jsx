import React from "react";

export default function ManagerSummaryTable({ summary }) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>
          {summary.manager_name} — {summary.team_name} ({summary.month})
        </h2>
        <span className="badge">{summary.team_signal}</span>
      </div>

      <div className="team-summary">
        <div><strong>Team size:</strong> {summary.team_size}</div>
        <div><strong>Avg lead time:</strong> {summary.team_metrics.avg_lead_time_days ?? "N/A"} days</div>
        <div><strong>Avg cycle time:</strong> {summary.team_metrics.avg_cycle_time_days ?? "N/A"} days</div>
        <div><strong>Bug rate:</strong> {summary.team_metrics.bug_rate_pct}%</div>
        <div><strong>Deployments:</strong> {summary.team_metrics.prod_deployments}</div>
        <div><strong>Merged PRs:</strong> {summary.team_metrics.merged_prs}</div>
      </div>

      <table className="summary-table">
        <thead>
          <tr>
            <th>Developer</th>
            <th>Lead Time</th>
            <th>Cycle Time</th>
            <th>Bug Rate</th>
            <th>Deployments</th>
            <th>PRs</th>
            <th>Signal</th>
          </tr>
        </thead>
        <tbody>
          {summary.developers.map((dev) => (
            <tr key={dev.developer_id}>
              <td>{dev.developer_name}</td>
              <td>{dev.avg_lead_time_days ?? "N/A"}</td>
              <td>{dev.avg_cycle_time_days ?? "N/A"}</td>
              <td>{dev.bug_rate_pct}%</td>
              <td>{dev.prod_deployments}</td>
              <td>{dev.merged_prs}</td>
              <td>{dev.pattern_hint}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
